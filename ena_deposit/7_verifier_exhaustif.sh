#!/bin/bash
# Verification EXHAUSTIVE de la correction : les 727 echantillons, les 3472 champs.
# Interroge l'API de rapport Webin par lots. Lecture seule.
#
#   bash 7_verifier_exhaustif.sh
#
# 6_etat_du_depot.sh sonde 12 echantillons — utile pour trancher vite.
# Celui-ci controle TOUT, et produit un rapport archivable.

set -uo pipefail
D=/home/martinj/work/projects/microbiome-hybrid/ena_deposit
cd "$D" || exit 1

U=""; P=""
while [ -z "$U" ]; do printf "Identifiant Webin : " > /dev/tty; IFS= read -r U < /dev/tty; U="${U//[[:space:]]/}"; done
while [ -z "$P" ]; do printf "Mot de passe Webin : " > /dev/tty; IFS= read -rs P < /dev/tty; echo > /dev/tty; done
echo

TD=$(mktemp -d); trap 'rm -rf "$TD"' EXIT
mapfile -t ACCS < <(cut -f2 ena_corrections.tsv | tail -n +2 | sort -u)
echo "echantillons a verifier : ${#ACCS[@]}"

LOT=100; i=0; n=0
while [ $i -lt ${#ACCS[@]} ]; do
  IDS=$(printf "%s," "${ACCS[@]:$i:$LOT}" | sed 's/,$//')
  n=$((n+1))
  code=$(curl -sS --connect-timeout 30 --max-time 300 --retry 2 -u "$U:$P" \
          -w '%{http_code}' -o "$TD/lot_$n.xml" \
          "https://www.ebi.ac.uk/ena/submit/report/samples/xml/$IDS")
  rc=$?
  if [ "$rc" -ne 0 ] || [ "$code" != "200" ] || [ ! -s "$TD/lot_$n.xml" ]; then
    echo "  lot $n : ECHEC (HTTP $code, rc=$rc) — verification incomplete"; unset P; exit 1
  fi
  printf "  lot %d : %d echantillons\n" "$n" "$(grep -c '<SAMPLE ' "$TD/lot_$n.xml")"
  i=$((i+LOT))
done
unset P
echo

python3 - "$TD" <<'PY'
import sys, os, csv, glob, collections
import xml.etree.ElementTree as ET
TD = sys.argv[1]

courant = {}
for f in sorted(glob.glob(os.path.join(TD, "lot_*.xml"))):
    for s in ET.parse(f).getroot().iter("SAMPLE"):
        courant[s.get("accession")] = {
            x.find("TAG").text: (x.find("VALUE").text if x.find("VALUE") is not None else None)
            for x in s.iter("SAMPLE_ATTRIBUTE")}

lignes = list(csv.DictReader(open("ena_corrections.tsv", newline="", encoding="utf-8"), delimiter="\t"))
ok = ko = absent = 0
ecarts = []
par_champ = collections.Counter()
for r in lignes:
    a = r["accession"]
    if a not in courant:
        absent += 1; continue
    cur = courant[a].get(r["champ"])
    if cur == r["valeur_corrigee"]:
        ok += 1; par_champ[r["champ"]] += 1
    else:
        ko += 1
        ecarts.append((a, r["champ"], r["valeur_corrigee"], cur, r["valeur_deposee"]))

print(f"echantillons interroges : {len(courant)}")
print(f"champs verifies         : {len(lignes)}")
print(f"  conformes a la correction : {ok}")
print(f"  non conformes             : {ko}")
print(f"  echantillons introuvables : {absent}")
print()
for c, v in sorted(par_champ.items()):
    print(f"  {c:45s} {v}")
if ecarts:
    print(f"\n{len(ecarts)} ecart(s), 10 premiers :")
    for e in ecarts[:10]:
        etat = "valeur INITIALE" if e[3] == e[4] else "valeur INATTENDUE"
        print(f"  {e[0]} | {e[1]}\n     attendu={e[2]!r}  courant={e[3]!r}  ({etat})")

rap = "verification_exhaustive_%s.txt" % __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M")
with open(rap, "w") as f:
    f.write(f"Verification exhaustive du depot PRJEB124417\n")
    f.write(f"echantillons {len(courant)} | champs {len(lignes)} | conformes {ok} | ecarts {ko}\n")
    for c, v in sorted(par_champ.items()): f.write(f"{c}\t{v}\n")
    for e in ecarts: f.write("ECART\t" + "\t".join(str(x) for x in e) + "\n")
print(f"\nrapport : {rap}")
print()
if ko == 0 and absent == 0:
    print("LES 3472 CORRECTIONS SONT APPLIQUEES, sur les 727 echantillons.")
else:
    print("Correction INCOMPLETE — me transmettre le rapport.")
PY
