#!/bin/bash
# Determine l'etat REEL des metadonnees du depot PRJEB124417.
#
# A lancer apres une soumission dont le recu est vide ou illisible : interroge
# l'API de rapport Webin (authentifiee) et compare l'etat courant de plusieurs
# echantillons aux valeurs AVANT et APRES correction.
#
#   bash 6_etat_du_depot.sh
#
# Ne modifie RIEN : lecture seule.

set -uo pipefail
D=/home/martinj/work/projects/microbiome-hybrid/ena_deposit
cd "$D" || exit 1

U=""; P=""
while [ -z "$U" ]; do printf "Identifiant Webin : " > /dev/tty; IFS= read -r U < /dev/tty; U="${U//[[:space:]]/}"; done
while [ -z "$P" ]; do printf "Mot de passe Webin : " > /dev/tty; IFS= read -rs P < /dev/tty; echo > /dev/tty; done
echo

# 12 accessions couvrant les differentes stations et les deux etats du nom d'hote
IDS=$(python3 - <<'PY'
import csv, collections
lignes = list(csv.DictReader(open("ena_corrections.tsv", newline="", encoding="utf-8"), delimiter="\t"))
par_station = collections.defaultdict(list)
for r in lignes:
    if r["champ"] == "geographic location (latitude)":
        par_station[r["valeur_corrigee"]].append(r["accession"])
sel = []
for st in sorted(par_station):
    sel.append(sorted(par_station[st])[0])
# + quelques hybrides
hyb = sorted({r["accession"] for r in lignes
              if r["champ"] == "host scientific name" and " x " in r["valeur_corrigee"]})[:3]
print(",".join(dict.fromkeys(sel + hyb)))
PY
)
echo "echantillons interroges : $(echo $IDS | tr ',' '\n' | wc -l)"

TMP=$(mktemp); trap 'rm -f "$TMP"' EXIT
CODE=$(curl -sS -u "$U:$P" -w '%{http_code}' -o "$TMP" \
        "https://www.ebi.ac.uk/ena/submit/report/samples/xml/$IDS")
RC=$?; unset P
echo "reponse HTTP $CODE (curl rc=$RC, $(wc -c < "$TMP") octets)"
if [ "$RC" -ne 0 ] || [ "$CODE" != "200" ] || [ ! -s "$TMP" ]; then
  echo "Interrogation impossible. Verifier les identifiants et le reseau."
  exit 1
fi
echo

python3 - "$TMP" <<'PY'
import sys, csv, collections
import xml.etree.ElementTree as ET

# --- etat courant, tel que l'ENA le sert
root = ET.parse(sys.argv[1]).getroot()
courant = {}
for s in root.iter("SAMPLE"):
    acc = s.get("accession")
    courant[acc] = {x.find("TAG").text: (x.find("VALUE").text if x.find("VALUE") is not None else None)
                    for x in s.iter("SAMPLE_ATTRIBUTE")}
if not courant:
    sys.exit("Aucun SAMPLE dans la reponse — format inattendu.")

# --- valeurs avant / apres, depuis la table de correction
avant, apres = collections.defaultdict(dict), collections.defaultdict(dict)
for r in csv.DictReader(open("ena_corrections.tsv", newline="", encoding="utf-8"), delimiter="\t"):
    avant[r["accession"]][r["champ"]] = r["valeur_deposee"]
    apres[r["accession"]][r["champ"]] = r["valeur_corrigee"]

n_av = n_ap = n_autre = 0
details = []
for acc, attrs in sorted(courant.items()):
    for champ, vnew in apres.get(acc, {}).items():
        vcur = attrs.get(champ)
        vold = avant[acc][champ]
        if vcur == vnew:   n_ap += 1
        elif vcur == vold: n_av += 1
        else:
            n_autre += 1
            details.append((acc, champ, vold, vnew, vcur))

tot = n_av + n_ap + n_autre
print(f"champs compares : {tot}  (sur {len(courant)} echantillons)")
print(f"  a la valeur CORRIGEE : {n_ap}")
print(f"  a la valeur INITIALE : {n_av}")
print(f"  ni l'une ni l'autre  : {n_autre}")
for d in details[:6]:
    print(f"     {d[0]} | {d[1]}\n        avant={d[2]!r} apres={d[3]!r} courant={d[4]!r}")
print()
if n_ap == tot:
    print("VERDICT : la correction EST APPLIQUEE. Le recu vide etait un incident")
    print("de transport, sans consequence. Rien a refaire.")
elif n_av == tot:
    print("VERDICT : la correction N'A PAS ETE APPLIQUEE. Le depot est dans son")
    print("etat initial. Relancer :  bash 4_corriger_metadonnees.sh prod")
else:
    print("VERDICT : etat MIXTE — une partie seulement des champs est corrigee.")
    print("Ne pas relancer a l'aveugle ; me transmettre cette sortie.")
PY
