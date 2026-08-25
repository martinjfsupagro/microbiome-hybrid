#!/bin/bash
# Soumission des metadonnees ENA (XML) via l'API Webin.
# A LANCER DEPUIS LA FRONTALE MESO, APRES le transfert FTP complet des 4608 fichiers.
#
#   bash submit_ena.sh test     -> validation seule, contre le serveur de test (RIEN n'est publie)
#   bash submit_ena.sh prod     -> soumission reelle
#
# Toujours lancer "test" en premier et corriger jusqu'a obtenir success="true".

set -uo pipefail
MODE="${1:-test}"
DIR="$(cd "$(dirname "$0")" && pwd)/ena_submission"

case "$MODE" in
  test) URL="https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit/" ;;
  prod) URL="https://www.ebi.ac.uk/ena/submit/drop-box/submit/" ;;
  *) echo "Usage: $0 [test|prod]"; exit 1 ;;
esac

for f in project sample experiment run submission; do
  [ -f "$DIR/$f.xml" ] || { echo "ERREUR : $DIR/$f.xml introuvable"; exit 1; }
done

read -rp  "Identifiant Webin (ex. Webin-12345) : " WEBIN_USER
read -rsp "Mot de passe Webin : " WEBIN_PASS; echo
echo "Mode : $MODE  ->  $URL"
[ "$MODE" = prod ] && { read -rp "Soumission REELLE. Taper OUI pour confirmer : " c; [ "$c" = OUI ] || exit 1; }

STAMP=$(date +%Y%m%d_%H%M)
RECEIPT="$DIR/receipt_${MODE}_${STAMP}.xml"

curl -sS -u "$WEBIN_USER:$WEBIN_PASS" \
  -F "SUBMISSION=@$DIR/submission.xml" \
  -F "PROJECT=@$DIR/project.xml" \
  -F "SAMPLE=@$DIR/sample.xml" \
  -F "EXPERIMENT=@$DIR/experiment.xml" \
  -F "RUN=@$DIR/run.xml" \
  "$URL" -o "$RECEIPT"

echo "Recu ecrit dans : $RECEIPT"; echo
python3 - "$RECEIPT" <<'PY'
import sys, xml.etree.ElementTree as ET
r = ET.parse(sys.argv[1]).getroot()
ok = r.get("success")
print("success =", ok)
for tag in ("ERROR", "INFO"):
    for m in r.iter(tag):
        print(f"[{tag}] {m.text}")
if ok == "true":
    for tag, label in (("PROJECT","PRJ"),("SAMPLE","ERS"),("EXPERIMENT","ERX"),("RUN","ERR")):
        n = [e for e in r.iter(tag)]
        print(f"{tag:11s}: {len(n)} accession(s)")
        for e in n[:3]:
            print("   ", e.get("alias"), "->", e.get("accession"))
PY
