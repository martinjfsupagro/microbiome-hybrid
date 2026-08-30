#!/usr/bin/env python3
# scripts/16-station_metadata.py
# Integre les reponses d'Andre (2026-08-30) : stations reelles, coordonnees, dates,
# et corrige la coquille d'annee sur 15Per2015Ch03A.
#
# Produit :
#   metadata/station_reference.csv      station physique -> riviere, coord, dates
#   metadata/individual_corrections.csv corrections d'identite (jointure, pas de renommage)
#   metadata/site_mapping.csv           mis a jour (rivieres reelles, structure 2 stations)
#   metadata/index_hybride_andre.csv    regenere : 180 individus, colonne station
#
# REGLE PROJET : les noms d'echantillons ne sont JAMAIS modifies. La coquille d'annee
# est portee par une table de jointure ; le dada2_id reste la cle vers la table ASV.
import csv, collections, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = lambda *p: os.path.join(ROOT, "metadata", *p)

# ---------------------------------------------------------------- 1. stations
STATIONS = [
 # site_code, station, river, lat, lon, date
 ("Ain","Pont-d'Ain",             "Suran",   46.048000, 5.324000, "2014-08-12"),
 ("Ain","Chavannes-sur-Suran",    "Suran",   46.264389, 5.429444, "2014-08-12"),
 ("Cab","Pont-d'Ain",             "Suran",   46.048000, 5.324000, "2015-08-26"),
 ("Cab","Chavannes-sur-Suran",    "Suran",   46.264389, 5.429444, "2015-08-26"),
 ("Avi","Avignon",                "Durance", 43.913000, 4.820722, "2014-07-17;2015-07-10"),
 ("Per","Pertuis",                "Durance", 43.668139, 5.493000, "2014-07-07;2014-08-20"),
 ("Caa","Canal (usine du Largue)","Canal",   43.853389, 5.858444, "2015-09-08"),
 ("Man","Manosque-Oraison",       "Durance", 43.919667, 5.896278, "2014-07-23"),
 ("Bue","Confluence Buech-Meouge","Buech",   44.262000, 5.828000, "2014-07-03;2015-07-17"),
 ("Jus","Saint-Just-d'Ardeche",   "Ardeche", 44.286000, 4.597833, "2015-07-21"),
 ("Bau","Rosieres",               "Beaume",  44.475000, 4.264000, "2015-07-22"),
]
with open(M("station_reference.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["site_code","station","river","latitude_WGS84","longitude_WGS84",
                "collection_date","source"])
    for r in STATIONS:
        w.writerow(list(r) + ["Andre 2026-08-30 (DMS converti)"])

# ------------------------------------------------- 2. corrections d'identite
# 15Per2015Ch03A : Pertuis n'a PAS ete echantillonne en 2015 (Andre : 07/07/2014 et
# 20/08/2014). Les 3 autres tissus du meme individu portent l'annee 2014, meme numero
# (2015), meme puits E11. Le prefixe "15" est une coquille pour "14".
CORRECTIONS = [
    {"dada2_sample":"15Per2015Ch03A", "champ":"year",
     "valeur_fichier":"2015", "valeur_corrigee":"2014",
     "motif":"coquille de prefixe : Pertuis non echantillonne en 2015 (Andre 2026-08-30) ; "
             "les 3 autres tissus du meme individu (num 2015, puits E11) portent 2014"},
]
with open(M("individual_corrections.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["dada2_sample","champ","valeur_fichier",
                                        "valeur_corrigee","motif"])
    w.writeheader(); w.writerows(CORRECTIONS)
CORR_YEAR = {c["dada2_sample"]: c["valeur_corrigee"] for c in CORRECTIONS
             if c["champ"]=="year"}

# ------------------------------------------------------------ 3. site_mapping
SITE_MAP = [
 # code, site_nom, riviere, stations, role_propose, annees, statut
 ("Ain","Suran (2 stations)","Suran","Pont-d'Ain;Chavannes-sur-Suran","Cn+Hy aval / Pt amont","2014",
  "Andre 2026-08-30 : DEUX stations, barriere infranchissable (seuil 2,5 m) entre elles"),
 ("Cab","Suran (2 stations)","Suran","Pont-d'Ain;Chavannes-sur-Suran","Cn+Hy aval / Pt amont","2015",
  "Andre 2026-08-30 : idem Ain, annee 2015 ; 1001-1010 aval, 1011-1019 amont"),
 ("Avi","Avignon","Durance","Avignon","asym. Hotu","2014,2015","effectif confirme"),
 ("Bau","Rosieres","Beaume","Rosieres","asym. Toxo","2015",
  "Andre 2026-08-30 : riviere = Beaume (et non Ardeche) ; station Rosieres"),
 ("Bue","Confluence Buech-Meouge","Buech","Confluence Buech-Meouge","sympatrie+hyb","2014,2015",
  "Andre 2026-08-30 : riviere = Buech (et non Durance)"),
 ("Caa","Canal (usine du Largue)","Canal","Canal (usine du Largue)","allopatrie","2015",
  "Andre 2026-08-30 : canal de l'usine du Largue (et non Durance)"),
 ("Jus","Saint-Just-d'Ardeche","Ardeche","Saint-Just-d'Ardeche","sympatrie+hyb","2015",
  "confirme ; Andre : Pt faits en premier, puis les Cn atypiques"),
 ("Man","Manosque-Oraison","Durance","Manosque-Oraison","a statuer","2014",
  "Andre 2026-08-30 : station Manosque-Oraison"),
 ("Per","Pertuis","Durance","Pertuis","a statuer","2014",
  "Andre 2026-08-30 : SEULE annee 2014, deux campagnes (07/07 et 20/08) ; "
  "l'annee 2015 du fichier vient d'une coquille"),
]
with open(M("site_mapping.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["site_code","site_nom","riviere","stations","role_propose",
                "annees_sequencees","statut"])
    w.writerows(SITE_MAP)

# --------------------------------------------------- 4. index hybride (Andre)
rows = list(csv.DictReader(open(M("samples_all.csv"))))
flags = {f["dada2_id"]: f["qc_flag"]
         for f in csv.DictReader(open(M("sample_qc_flags.csv")))}
stmap = {(s["year"], s["site"], s["individual"]): s["station"]
         for s in csv.DictReader(open(M("station_mapping.csv")))}
smap  = {s["site_code"]: s for s in csv.DictReader(open(M("site_mapping.csv")))}
ESP = {"Cn":"Chondrostoma nasus","Pt":"Parachondrostoma toxostoma",
       "Ch":"Chondrostoma sp."}

ind = collections.defaultdict(lambda: {"tissus": set()})
for r in rows:
    if r["sample_type"] != "biological": continue
    if flags.get(r["dada2_id"], "").startswith("mock_confirme"): continue
    stem = r["dada2_id"].split("__")[0]
    year = CORR_YEAR.get(stem, r["year"])          # <-- correction d'annee
    key = (year, r["site"], r["individual"])
    d = ind[key]
    d["tissus"].add(r["tissue"])
    for k, col in (("sexe","sex"), ("taille_cm","size_cm"), ("poids_g","weight_g")):
        if r.get(col) and not d.get(k): d[k] = r[col]
    d["taxon"] = r["taxon_code"] if r.get("taxon_code") else \
                 {"hotu":"Cn","toxostome":"Pt","chondrostome":"Ch"}.get(r["taxon"],"Ch")

with open(M("index_hybride_andre.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["individual_id","site_code","site_nom","riviere","station",
                "role_population","annee","individual","taxon_code_actuel",
                "espece_actuelle","sexe","taille_cm","poids_g","n_tissus_sequences",
                "tissus","index_hybride","index_hybride_source"])
    for (y, s, i), d in sorted(ind.items(), key=lambda x: (x[0][1], x[0][0], int(x[0][2]))):
        sm = smap.get(s, {})
        tx = d.get("taxon", "Ch")
        # index connu par definition pour les taxons deja identifies
        idx = {"Cn": "0", "Pt": "1"}.get(tx, "")
        src = "connu (taxon identifie)" if idx else "A_REMPLIR_ANDRE"
        w.writerow([f"{y}_{s}_{i}", s, sm.get("site_nom",""), sm.get("riviere",""),
                    stmap.get((y, s, i), ""), sm.get("role_propose",""), y, i, tx,
                    ESP.get(tx, ""), d.get("sexe",""), d.get("taille_cm",""),
                    d.get("poids_g",""), len(d["tissus"]),
                    ";".join(sorted(d["tissus"])), idx, src])

print(f"station_reference.csv      : {len(STATIONS)} lignes ({len(set(s[1] for s in STATIONS))} stations physiques)")
print(f"individual_corrections.csv: {len(CORRECTIONS)} correction(s)")
print(f"site_mapping.csv          : {len(SITE_MAP)} sites")
print(f"index_hybride_andre.csv   : {len(ind)} individus")
n_fill = sum(1 for d in ind.values() if d.get("taxon","Ch") == "Ch")
print(f"   dont a genotyper par Andre : {n_fill}")
print(f"   dont index deja connu      : {len(ind) - n_fill}")
per = {k: v for k, v in ind.items() if k[1] == "Per"}
print(f"   controle Per : {len(per)} individus (10 avant correction)")
n4 = sum(1 for d in per.values() if len(d["tissus"]) == 4)
print(f"      dont 4 tissus complets  : {n4}")
