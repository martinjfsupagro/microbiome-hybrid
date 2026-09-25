#!/usr/bin/env python3
# scripts/19-analysis_metadata.py
# Construit metadata/analysis_metadata.csv : POINT D'ENTREE UNIQUE de l'analyse ecologique.
#
# POURQUOI. Les corrections du projet passaient par trois tables de jointure separees
# (sample_qc_flags.csv, station_mapping.csv, individual_corrections.csv). Un script
# d'analyse qui en oublie une produit des resultats faux SANS erreur visible. Cette
# table les applique toutes, une fois, de facon verifiable.
#
# SOURCE DES CATEGORIES. metadata/genotypes_andre_aout2026.csv, conversion VERBATIM de
# "nouveau tableau_AG_Aout_2026.xlsx" (Andre Gilles, aout 2026). Aucune transformation
# a la conversion : seule l'ecriture en CSV.
#
# DECISION (JF Martin, 2026-08-30) : la categorie retenue est la colonne P du fichier,
# `taxon_code_index` (Cn / Hy / Pt), et NON la mediane d'index de la colonne Q.
#
# Justification verifiee dans les donnees : la mediane d'index ne suffit pas a
# identifier les hybrides. 9 des 30 Hy ont une mediane EXTREME (< 0.05 ou > 0.95) et ne
# seraient donc pas detectes par un seuil sur Q ; ce sont leurs deltas inter-chromosomes
# qui les trahissent (delta median 0.366 pour ces 9, contre 0.030 chez les Cn purs et
# 0.011 chez les Pt purs). Utiliser Q ferait passer ces 9 individus pour des parentaux.
#
# AVERTISSEMENT SUR LA COLONNE Q. Son orientation est l'INVERSE de celle demandee dans
# metadata/index_hybride_andre.csv (qui specifiait 0 = hotu, 1 = toxostome) :
#   Cn (hotu)      -> mediane 0.9999
#   Pt (toxostome) -> mediane 0.0001
# Elle est reportee VERBATIM dans la table sous `index_mediane_andre` (orientation
# 1 = Cn, 0 = Pt). Quiconque l'utilisera comme gradient doit soit l'inverser, soit
# adapter l'interpretation. Aucune valeur n'en est derivee ici.
#
# LIGNE ECARTEE. Le fichier d'Andre porte 181 lignes : il a ete rempli sur la version
# ANTERIEURE du CSV, qui contenait l'individu fantome `2015_Per_2015` issu de la coquille
# d'annee sur 15Per2015Ch03A (cf docs/decision_stations.md §3). Andre n'a retourne AUCUN
# genotype pour cette ligne (categorie et mediane vides) - ce qui corrobore la correction :
# ce n'etait pas un poisson distinct. La ligne est ecartee, l'effectif reste 180.
#
# COVARIABLE DE POSITION. L'effet de la position dans la plaque sur la composition est
# etabli (docs/decision_position_effect.md). Deux rangs sont produits :
#   `col_rank_site`    rang de la colonne parmi celles occupees par le SITE
#   `col_rank_station` idem par STATION
# Le rang intra-site est celui sous lequel l'effet a ete etabli (permutations bloquees
# par site) ; le rang intra-station est le pendant pour les modeles spatiaux passes a la
# station. Les deux sont fournis, le choix appartient au modele.
#
# Sortie : metadata/analysis_metadata.csv, une ligne par ECHANTILLON sequence
#          (echantillon x run), avec l'individu et sa categorie.
#
# ---------------------------------------------------------------------------------------
# MISE A JOUR 2026-09-25 — CLASSIFICATION A 25 CHROMOSOMES (septembre)
# ---------------------------------------------------------------------------------------
# Source : metadata/genotypes_verifies_sept_180.csv (Andre, septembre 2026, verifie contre
# les Q-values par chromosome). Colonnes utilisees : individual_id, classe_sept_25chr,
# type_genome, classe_aout_12chr, Qvalues_presentes.
#
#   `categorie`             = classe_sept_25chr   (59 Cn / 42 Hy / 79 Pt)  <- NOUVELLE valeur
#   `categorie_aout_12chr`  = colonne P du fichier d'aout (59 / 30 / 91), CONSERVEE pour
#                             la tracabilite, jamais ecrasee
#   `type_genome`           = intermediaire (20) / quasi-pur (22) / pur (138)
#   `inclus_passe1`         = False pour les 22 quasi-purs
#
# DECISION D1 (Andre, 2026-09-25) : deux passes. Passe 1 = 20 hybrides intermediaires, les
# 22 quasi-purs EXCLUS (pas reverses dans leur classe parentale), n = 158. Passe 2 = les 42
# hybrides, n = 180. Le filtre de passe est applique par les scripts d'analyse, pas ici :
# cette table porte les 180 individus.
#
# TEMOIN. Le fichier de septembre porte aussi la classe d'aout (classe_aout_12chr). Elle
# doit concorder avec la colonne P du fichier d'aout pour les 180 individus : un desaccord
# signalerait une jointure mal alignee ou une version differente des sources.
#
# 5 individus sans Q-values (2014_Bue_1001, 2014_Bue_1002, 2015_Bue_1014, 2015_Cab_1011,
# 2015_Jus_1008), tous purs, identifies a partir d'autres tissus que le foie : conserves.

import csv, collections, sys, os

os.chdir(os.path.expanduser("~/work/projects/microbiome-hybrid"))

def load(path):
    # les tables du projet sont en CRLF : on nettoie les valeurs a la lecture
    with open(path, newline="") as fh:
        return [{k: (v.strip() if isinstance(v, str) else v) for k, v in r.items()}
                for r in csv.DictReader(fh)]

# --- sources ---
samples = load("metadata/samples_all.csv")
flags   = {r["dada2_id"]: r["qc_flag"] for r in load("metadata/sample_qc_flags.csv")}
geno    = load("metadata/genotypes_andre_aout2026.csv")
stmap   = load("metadata/station_mapping.csv")
corr    = load("metadata/individual_corrections.csv")
stref   = load("metadata/station_reference.csv")

# --- verification des colonnes attendues (ne rien supposer) ---
need_s = {"dada2_id","site","year","individual","tissue","run_label","sample_type","well","plate","taxon_code"}
missing = need_s - set(samples[0])
assert not missing, f"colonnes absentes de samples_all.csv : {missing}"
COL_CAT = "taxon_code_index"          # colonne P
COL_MED = "mediane des Index par chromosome"   # colonne Q
COL_DEL = "delta_mediane_quart"       # colonne R
for cname in (COL_CAT, COL_MED, COL_DEL, "individual_id"):
    assert cname in geno[0], f"colonne absente du fichier genotypes : {cname!r}"

# --- categorie par individu (colonne P), ligne fantome ecartee ---
cat, med, dlt = {}, {}, {}
skipped = []
for r in geno:
    iid = r["individual_id"].strip()
    c = (r[COL_CAT] or "").strip()
    if not c:
        skipped.append(iid); continue
    assert c in ("Cn","Hy","Pt"), f"categorie inattendue {c!r} pour {iid}"
    cat[iid] = c
    med[iid] = (r[COL_MED] or "").strip()
    dlt[iid] = (r[COL_DEL] or "").strip()
print(f"genotypes lus      : {len(cat)} individus")
print(f"lignes ecartees    : {len(skipped)} -> {skipped}")
assert skipped == ["2015_Per_2015"], f"ligne ecartee inattendue : {skipped}"

# --- classification de septembre (25 chromosomes) ---
with open("metadata/genotypes_verifies_sept_180.csv", newline="", encoding="utf-8-sig") as fh:
    sept = [{k: (v or "").strip() for k, v in r.items()} for r in csv.DictReader(fh)]
for cname in ("individual_id","classe_sept_25chr","type_genome","classe_aout_12chr","Qvalues_presentes"):
    assert cname in sept[0], f"colonne absente de genotypes_verifies_sept_180.csv : {cname!r}"
sept = {r["individual_id"]: r for r in sept}
assert set(sept) == set(cat), (
    f"individus differents entre aout et septembre : "
    f"{sorted(set(sept) ^ set(cat))[:5]}")
# temoin : la classe d'aout portee par le fichier de septembre == la colonne P d'aout
dis = [(i, cat[i], sept[i]["classe_aout_12chr"]) for i in cat if cat[i] != sept[i]["classe_aout_12chr"]]
assert not dis, f"classe d'aout discordante entre les deux fichiers : {dis[:5]}"
for i, r in sept.items():
    assert r["classe_sept_25chr"] in ("Cn","Hy","Pt"), f"classe inattendue {r['classe_sept_25chr']!r} pour {i}"
    assert r["type_genome"] in ("intermediaire","quasi-pur","pur"), f"type inattendu {r['type_genome']!r} pour {i}"
    # un quasi-pur ou un intermediaire est Hy ; un pur est parental
    assert (r["type_genome"] == "pur") == (r["classe_sept_25chr"] != "Hy"), f"incoherence classe/type pour {i}"
print(f"septembre lus      : {len(sept)} individus | classe d'aout concordante pour les {len(cat)}")
print(f"changements aout -> septembre : {sum(1 for i in cat if cat[i] != sept[i]['classe_sept_25chr'])}")

# --- station et corrections d'identite ---
# station_mapping.csv : colonnes reelles year, site, individual, station
for cname in ("year","site","individual","station"):
    assert cname in stmap[0], f"colonne absente de station_mapping.csv : {cname!r}"
station = {(r["year"], r["site"], r["individual"]): r["station"] for r in stmap}

# individual_corrections.csv : colonnes reelles dada2_sample, champ, valeur_fichier,
# valeur_corrigee, motif -> table de corrections champ par champ
for cname in ("dada2_sample","champ","valeur_corrigee"):
    assert cname in corr[0], f"colonne absente de individual_corrections.csv : {cname!r}"
sample_corr = collections.defaultdict(dict)
for r in corr:
    sample_corr[r["dada2_sample"]][r["champ"]] = r["valeur_corrigee"]

# station_reference.csv : colonnes reelles site_code, station, river,
# latitude_WGS84, longitude_WGS84, collection_date, source
for cname in ("station","river","latitude_WGS84","longitude_WGS84","collection_date"):
    assert cname in stref[0], f"colonne absente de station_reference.csv : {cname!r}"
# ATTENTION : station_reference.csv a une ligne par (site_code, station), et le
# collection_date DIFFERE entre elles — Ain/Pont-d'Ain = 2014-08-12 mais
# Cab/Pont-d'Ain = 2015-08-26. Indexer sur la station seule (ce que faisait la
# premiere version) ecrasait la date 2015 du Suran par celle de 2014 : les 19
# individus Cab portaient une date de collecte fausse d'un an.
assert "site_code" in stref[0], "colonne site_code absente de station_reference.csv"
stinfo = {(r["site_code"], r["station"]): r for r in stref}
# garde-fou : les lignes d'un meme couple ne doivent pas se contredire
_bystn = collections.defaultdict(set)
for r in stref:
    _bystn[r["station"]].add((r["latitude_WGS84"], r["longitude_WGS84"], r["river"]))
for k, v in _bystn.items():
    assert len(v) == 1, f"coordonnees contradictoires pour la station {k!r} : {v}"

# --- construction, echantillons biologiques uniquement ---
rows, drop = [], collections.Counter()
for s in samples:
    sid = s["dada2_id"]
    if s["sample_type"] != "biological":
        drop["non_biologique"] += 1; continue
    fl = flags.get(sid, "")
    if fl.startswith("mock_confirme"):
        drop["mock_requalifie"] += 1; continue
    # correction d'annee eventuelle (coquille 15Per2015Ch03A)
    # dada2_id porte le suffixe __<run> ('15Per2015Ch03A__durance1') alors que la
    # table de corrections est indexee sur le nom d'echantillon nu ('15Per2015Ch03A').
    # Oublier ce decoupage faisait perdre silencieusement les 3 echantillons corriges.
    base_sid = sid.split("__")[0]
    year = sample_corr.get(base_sid, {}).get("year") or s["year"]
    iid  = f"{year}_{s['site']}_{s['individual']}"
    if iid not in cat:
        drop["sans_genotype"] += 1
        print(f"  ATTENTION sans genotype : {sid} -> {iid}", file=sys.stderr)
        continue
    stn = station.get((year, s["site"], s["individual"]), "")
    assert stn, f"station manquante pour {iid}"
    si = stinfo.get((s["site"], stn))
    assert si is not None, f"pas de ligne station_reference pour ({s['site']!r}, {stn!r})"
    rows.append({
        "dada2_id": sid, "individual_id": iid, "run_label": s["run_label"],
        "library": "A" if s["run_label"] == "durance1" else "B",
        "tissue": s["tissue"], "site_code": s["site"], "annee": year,
        "individual": s["individual"], "station": stn,
        "riviere": si.get("river",""), "latitude": si.get("latitude_WGS84",""),
        "longitude": si.get("longitude_WGS84",""), "date_collecte": si.get("collection_date",""),
        "categorie": sept[iid]["classe_sept_25chr"],          # septembre, 25 chromosomes
        "categorie_aout_12chr": cat[iid],                      # aout, 12 chromosomes (trace)
        "type_genome": sept[iid]["type_genome"],
        "inclus_passe1": str(sept[iid]["type_genome"] != "quasi-pur"),
        "qvalues_foie": sept[iid]["Qvalues_presentes"],
        "index_mediane_andre": med[iid],       # colonne Q, VERBATIM (1 = Cn, 0 = Pt)
        "delta_mediane_quart": dlt[iid],
        "taxon_code_avant_genotypage": s["taxon_code"],
        "plate": s["plate"], "well": s["well"],
        "well_row": (s["well"] or "")[:1],
        "well_col": (s["well"] or "")[1:],
        "qc_flag": fl,
    })
print(f"\nechantillons retenus : {len(rows)}")
print("ecartes :", dict(drop))
# Un echantillon biologique perdu faute de genotype signale une jointure cassee, pas une
# donnee manquante : il doit faire echouer le script, pas disparaitre dans un compteur.
assert drop["sans_genotype"] == 0, (
    f"{drop['sans_genotype']} echantillon(s) biologique(s) sans genotype : jointure cassee")

# --- rangs de colonne (position), calcul explicite par groupe ---
for key, out in (("site_code","col_rank_site"), ("station","col_rank_station")):
    bygrp = collections.defaultdict(set)
    for r in rows:
        if r["well_col"].isdigit(): bygrp[r[key]].add(int(r["well_col"]))
    ranks = {g: {c: i+1 for i, c in enumerate(sorted(cs))} for g, cs in bygrp.items()}
    for r in rows:
        r[out] = ranks[r[key]][int(r["well_col"])] if r["well_col"].isdigit() else ""
    assert all(r[out] != "" for r in rows), f"rang manquant pour {out}"

FIELDS = ["dada2_id","individual_id","run_label","library","tissue","site_code","station",
          "riviere","latitude","longitude","date_collecte","annee","individual","categorie",
          "categorie_aout_12chr","type_genome","inclus_passe1","qvalues_foie",
          "index_mediane_andre","delta_mediane_quart","taxon_code_avant_genotypage",
          "plate","well","well_row","well_col","col_rank_site","col_rank_station","qc_flag"]
with open("metadata/analysis_metadata.csv","w",newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=FIELDS); w.writeheader(); w.writerows(rows)

# --- controles de coherence ---
print("\n=== CONTROLES ===")
ind = {r["individual_id"] for r in rows}
print(f"individus : {len(ind)} (attendu 180)")
assert len(ind) == 180, f"effectif individu inattendu : {len(ind)}"
cnt_sept = collections.Counter(sept[i]["classe_sept_25chr"] for i in ind)
cnt_aout = collections.Counter(cat[i] for i in ind)
cnt_type = collections.Counter(sept[i]["type_genome"] for i in ind)
print("categorie septembre (individus) :", dict(cnt_sept))
print("categorie aout      (individus) :", dict(cnt_aout))
print("type_genome         (individus) :", dict(cnt_type))
assert (cnt_sept["Cn"], cnt_sept["Hy"], cnt_sept["Pt"]) == (59, 42, 79), f"septembre : {cnt_sept}"
assert (cnt_aout["Cn"], cnt_aout["Hy"], cnt_aout["Pt"]) == (59, 30, 91), f"aout : {cnt_aout}"
assert (cnt_type["intermediaire"], cnt_type["quasi-pur"], cnt_type["pur"]) == (20, 22, 138), f"type : {cnt_type}"
n_p1 = sum(1 for i in ind if sept[i]["type_genome"] != "quasi-pur")
print(f"passe 1 (quasi-purs exclus) : {n_p1} individus")
assert n_p1 == 158, f"passe 1 : {n_p1}"
print("par run (echantillons)    :",
      dict(collections.Counter(r["run_label"] for r in rows)))
print("par tissu (echantillons)  :",
      dict(collections.Counter(r["tissue"] for r in rows)))

# les echantillons de la table propre sont-ils tous couverts ?
with open("results/decontam/asv_table_clean.tsv") as fh:
    hdr = fh.readline().rstrip("\n").split("\t")[1:]
have = {r["dada2_id"] for r in rows}
print(f"\ntable propre : {len(hdr)} echantillons")
print(f"  couverts par analysis_metadata : {len(set(hdr) & have)}")
manquants = sorted(set(hdr) - have)
print(f"  absents de analysis_metadata   : {len(manquants)}")
assert not manquants, f"echantillons de la table propre non couverts : {manquants[:5]}"

# categories par station : le controle qui decide de la faisabilite, pour chaque definition
first = {}
for r in rows:
    first.setdefault(r["individual_id"], r)
for label, col, keep in (("AOUT (12 chr)", "categorie_aout_12chr", lambda r: True),
                         ("PASSE 2 (42 Hy)", "categorie", lambda r: True),
                         ("PASSE 1 (20 Hy, quasi-purs exclus)", "categorie",
                          lambda r: r["inclus_passe1"] == "True")):
    bys = collections.defaultdict(collections.Counter)
    for r in first.values():
        if keep(r): bys[r["station"]][r[col]] += 1
    print(f"\n=== {label} : categories par STATION (individus) ===")
    print(f"{'station':26} {'Cn':>4} {'Hy':>4} {'Pt':>4} {'tot':>5}  categories")
    for stn in sorted(bys):
        c = bys[stn]; n3 = sum(1 for k in ("Cn","Hy","Pt") if c[k] > 0)
        print(f"{stn:26} {c['Cn']:4} {c['Hy']:4} {c['Pt']:4} {sum(c.values()):5}  {n3}")
    full = [s for s in bys if all(bys[s][k] > 0 for k in ("Cn","Hy","Pt"))]
    print(f"stations a gradient complet : {len(full)} -> {sorted(full)} | "
          f"individus : {sum(sum(bys[s].values()) for s in full)}")
print("\nOK -> metadata/analysis_metadata.csv")
