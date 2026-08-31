#!/bin/bash
# Verifie, apres correction, que l'ENA sert bien les nouvelles valeurs.
#   bash 5_verifier_correction.sh
#
# Le portail met quelques heures a refleter une modification. Un ecart juste
# apres la soumission n'est pas forcement un echec : relancer plus tard.

D=/home/martinj/work/projects/microbiome-hybrid/ena_deposit
python3 - "$D" <<'PY'
import sys, csv, json, urllib.request, collections, os
D = sys.argv[1]
corr = os.path.join(D, "ena_corrections.tsv")

attendu = collections.defaultdict(dict)
with open(corr, newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        attendu[r["accession"]][r["champ"]] = r["valeur_corrigee"]

# echantillon de controle : 8 accessions couvrant plusieurs stations
accs = sorted(attendu)[::max(1, len(attendu)//8)][:8]
print(f"verification sur {len(accs)} echantillons parmi {len(attendu)}\n")

MAP = {"lat": "geographic location (latitude)",
       "lon": "geographic location (longitude)",
       "collection_date": "collection date",
       "host_scientific_name": "host scientific name"}

url = ("https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJEB124417"
       "&result=read_run&fields=sample_accession,lat,lon,collection_date,host_scientific_name"
       "&format=tsv&limit=0")
try:
    txt = urllib.request.urlopen(url, timeout=60).read().decode("utf8", "replace")
except Exception as e:
    sys.exit(f"portail injoignable : {type(e).__name__}: {e}")

lignes = [l.split("\t") for l in txt.strip().split("\n")]
if len(lignes) < 2:
    print("Le portail ne renvoie encore aucune ligne pour PRJEB124417.")
    print("C'est attendu tant que l'etude n'est pas publique, ou dans les heures")
    print("qui suivent une modification. Relancer plus tard.")
    sys.exit(0)

head = lignes[0]
vus = {}
for l in lignes[1:]:
    d = dict(zip(head, l))
    vus.setdefault(d.get("sample_accession"), d)

ok = ko = absent = 0
for a in accs:
    d = vus.get(a)
    if not d:
        print(f"  {a} : absent du portail"); absent += 1; continue
    for col, champ in MAP.items():
        if champ not in attendu[a]: continue
        att, obs = attendu[a][champ], (d.get(col) or "").strip()
        if obs == att or (col in ("lat","lon") and obs and abs(float(obs)-float(att)) < 1e-6):
            ok += 1
        else:
            ko += 1
            print(f"  {a} | {champ}\n      attendu={att!r}  observe={obs!r}")

print(f"\nchamps conformes : {ok} | ecarts : {ko} | echantillons absents : {absent}")
if ko == 0 and ok > 0:
    print("La correction est visible sur le portail public.")
elif ko:
    print("Ecarts : si la soumission est recente (< 24 h), relancer plus tard.")
PY
