#!/usr/bin/env python3
# scripts/25-ena_corrections.py
# Construit la table de correction du depot ENA PRJEB124417.
#
# POURQUOI. Les coordonnees deposees etaient des extrapolations depuis des noms de
# communes (confirme par JF Martin le 2026-08-30), pas des releves de terrain. Cinq
# rivieres sont fausses et six positions decalees de plus de 5 km, jusqu'a 41,4 km. Par
# ailleurs les dates de collecte ont ete deposees a l'annee alors que les dates exactes
# sont connues, et deux codes de site (Ain, Cab) recouvrent en realite DEUX stations
# distinctes avec des coordonnees differentes : la correction est donc par ECHANTILLON,
# pas par site.
#
# ENTREES  : ena_deposit/ena_samples.tsv        (ce qui a ete depose, 768 echantillons)
#            ena_deposit/sample_accessions.tsv  (alias -> accession ERS)
#            ena_deposit/ENA_sites_completes.csv (les coordonnees fausses, pour l'avant)
#            metadata/analysis_metadata.csv     (station, coordonnees et dates reelles)
# SORTIE   : ena_deposit/ena_corrections.tsv    une ligne par echantillon a modifier
#
# Ne modifie rien a l'ENA : produit seulement la table des changements.

import csv, os, sys, collections

D = "ena_deposit"
def load(path, delim=","):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return [{k: (v.strip() if isinstance(v, str) else v) for k, v in r.items()}
                for r in csv.DictReader(fh, delimiter=delim)]

samples = load(f"{D}/ena_samples.tsv", "\t")
sites   = load(f"{D}/ENA_sites_completes.csv")
meta    = load("metadata/analysis_metadata.csv")

acc = {}
if os.path.exists(f"{D}/sample_accessions.tsv"):
    with open(f"{D}/sample_accessions.tsv") as fh:
        for line in fh:
            p = line.rstrip("\n").split("\t")
            if len(p) >= 2 and p[0] and not p[0].startswith("#"):
                acc[p[0]] = p[1]

# --- etat DEPOSE, par code de site ---
old = {}
for r in sites:
    old[r["site_code"]] = {
        "lat": r.get("latitude_WGS84_A_REMPLIR", ""),
        "lon": r.get("longitude_WGS84_A_REMPLIR", ""),
        "loc": r.get("commune_ou_lieu_dit_A_REMPLIR", ""),
        "riv": r.get("riviere", ""),
    }

# --- etat REEL, par echantillon (le nom nu, sans suffixe de run) ---
new = {}
for r in meta:
    stem = r["dada2_id"].split("__")[0]
    if stem in new:
        continue
    new[stem] = r

CATNAME = {"Cn": "Chondrostoma nasus",
           "Pt": "Parachondrostoma toxostoma",
           "Hy": "Chondrostoma nasus x Parachondrostoma toxostoma"}

cols = ["alias", "accession", "stem", "sample_type", "champ",
        "valeur_deposee", "valeur_corrigee", "motif"]
rows = []
stats = collections.Counter()
sans_meta = []

for s in samples:
    alias, stem = s["alias"], s["stem"]
    st = s["sample_type_ena"]
    if st != "biological":
        stats["controle_inchange"] += 1
        continue
    m = new.get(stem)
    if m is None:
        sans_meta.append(stem)
        continue
    o = old.get(s["site_code"], {})
    a = acc.get(alias, "")

    def add(champ, dep, cor, motif):
        if str(dep).strip() != str(cor).strip():
            rows.append(dict(zip(cols, [alias, a, stem, st, champ, dep, cor, motif])))
            stats[champ] += 1

    add("geographic location (latitude)", o.get("lat", ""), m["latitude"],
        "coordonnee extrapolee remplacee par le releve de terrain ; station %s" % m["station"])
    add("geographic location (longitude)", o.get("lon", ""), m["longitude"],
        "coordonnee extrapolee remplacee par le releve de terrain ; station %s" % m["station"])
    add("geographic location (region and locality)", o.get("loc", ""),
        "%s, %s" % (m["station"], m["riviere"]),
        "commune extrapolee remplacee par la station et la riviere reelles")
    # La station porte toutes ses dates ("2014-07-03;2015-07-17"). L'annee de l'individu
    # etant connue, on RESOUT la date au lieu de pousser la liste. Seul Pertuis a deux
    # dates la MEME annee : la l'assignation par individu est inconnue et on le signale.
    cand = [d for d in str(m["date_collecte"]).split(";") if d]
    same_year = [d for d in cand if d.startswith(str(m["annee"]))]
    if len(same_year) == 1:
        date_cor, motif_d = same_year[0], "date exacte connue ; l'annee seule avait ete deposee"
    elif len(same_year) > 1:
        date_cor = "/".join(same_year)
        motif_d = ("A TRANCHER : %d dates la meme annee a cette station, assignation par "
                   "individu inconnue - demander a Andre avant de soumettre" % len(same_year))
        stats["date_ambigue"] += 1
    else:
        date_cor = ";".join(cand)
        motif_d = ("A VERIFIER : aucune date de la station ne correspond a l'annee %s de "
                   "l'individu" % m["annee"])
        stats["date_annee_incoherente"] += 1
    add("collection date", s["collection_date"], date_cor, motif_d)
    add("host scientific name", s["host_scientific_name"], CATNAME[m["categorie"]],
        "identite resolue par genotypage (categorie %s)" % m["categorie"])

    stats["echantillons_biologiques"] += 1

with open(f"{D}/ena_corrections.tsv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t")
    w.writeheader()
    for r in rows:
        w.writerow(r)

print("=== couverture ===")
print("  echantillons deposes            :", len(samples))
print("  biologiques traites             :", stats["echantillons_biologiques"])
print("  controles laisses inchanges     :", stats["controle_inchange"])
print("  sans metadonnees d'analyse      :", len(sans_meta), sans_meta[:5])
print("  accessions ERS disponibles      :", len(acc))
assert not sans_meta, "des echantillons deposes n'ont pas de metadonnees : %s" % sans_meta[:5]

print("\n=== changements par attribut ===")
for k in ("geographic location (latitude)", "geographic location (longitude)",
          "geographic location (region and locality)", "collection date",
          "host scientific name"):
    print("  %-46s %4d" % (k, stats[k]))
print("  %-46s %4d" % ("TOTAL de lignes de correction", len(rows)))

alias_touches = len({r["alias"] for r in rows})
print("\n  echantillons concernes par au moins un changement :", alias_touches)
print("  echantillons biologiques inchanges                :",
      stats["echantillons_biologiques"] - alias_touches)

print("\n=== dates de collecte deposees -> corrigees ===")
dd = collections.Counter((r["valeur_deposee"], r["valeur_corrigee"])
                         for r in rows if r["champ"] == "collection date")
for (a_, b_), n in sorted(dd.items()):
    flag = "   <-- DEUX DATES, assignation par individu inconnue" if ";" in b_ else ""
    print("  %-8s -> %-26s %4d%s" % (a_, b_, n, flag))

print("\n=== nom d'hote depose -> corrige ===")
hh = collections.Counter((r["valeur_deposee"], r["valeur_corrigee"])
                         for r in rows if r["champ"] == "host scientific name")
for (a_, b_), n in sorted(hh.items()):
    print("  %-28s -> %-46s %4d" % (a_, b_, n))

print("\nOK -> %s/ena_corrections.tsv (%d lignes)" % (D, len(rows)))
