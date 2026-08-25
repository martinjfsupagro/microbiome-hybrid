#!/bin/bash
# ETAPE 1/3 : soumettre l'etude et les 768 echantillons par HTTPS.
#
# Le FTP Webin etant hors service, on n'utilise QUE des voies qui fonctionnent :
#   - HTTPS pour les metadonnees (etude + echantillons)  <- ce script
#   - Aspera via webin-cli pour les fichiers             <- etapes 2 et 3
#
#   bash 1_soumettre_metadonnees.sh test    # serveur de test, rien n'est publie
#   bash 1_soumettre_metadonnees.sh prod    # POUR DE VRAI
#
# Produit : receipt_<mode>_<date>.xml  et  sample_accessions.tsv (alias -> ERS)

set -uo pipefail
MODE="${1:-}"
D=/home/martinj/work/projects/microbiome-hybrid/ena_deposit
XML=$D/ena_submission

case "$MODE" in
  test) URL=https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit/ ;;
  prod) URL=https://www.ebi.ac.uk/ena/submit/drop-box/submit/ ;;
  *) echo "Usage : bash $0 test|prod"; exit 1 ;;
esac

for f in submission.xml project.xml sample.xml; do
  [ -f "$XML/$f" ] || { echo "ERREUR : $XML/$f introuvable"; exit 1; }
done

echo "=== Soumission des metadonnees ($MODE) ==="
echo "  etude      : $(grep -c '<PROJECT ' $XML/project.xml) projet(s)"
echo "  echantillons: $(grep -c '<SAMPLE ' $XML/sample.xml)"
echo "  cible      : $URL"
echo

if [ "$MODE" = "prod" ]; then
  echo "ATTENTION : soumission REELLE sur le serveur de production."
  printf "Taper OUI pour confirmer : "; read -r C
  [ "$C" = "OUI" ] || { echo "annule."; exit 1; }
  echo
fi

U=""; P=""
while [ -z "$U" ]; do printf "Identifiant Webin : " > /dev/tty; IFS= read -r U < /dev/tty; U="${U//[[:space:]]/}"; done
while [ -z "$P" ]; do printf "Mot de passe Webin : " > /dev/tty; IFS= read -rs P < /dev/tty; echo > /dev/tty; done
echo

R=$D/receipt_${MODE}_$(date +%Y%m%d_%H%M).xml
echo "Envoi en cours (768 echantillons, quelques minutes)..."
curl -sS -u "$U:$P" \
     -F "SUBMISSION=@$XML/submission.xml" \
     -F "PROJECT=@$XML/project.xml" \
     -F "SAMPLE=@$XML/sample.xml" \
     "$URL" -o "$R"
unset P
echo "  recu : $R"
echo

python3 - "$R" <<'PY'
import sys, xml.etree.ElementTree as ET, csv, os
r = ET.parse(sys.argv[1]).getroot()
ok = r.get("success")
print(f"  success = {ok}")
errs = [e.text for e in r.iter("ERROR")]
if errs:
    print(f"  {len(errs)} erreur(s) :")
    for e in errs[:15]: print("    -", e)
    if len(errs) > 15: print(f"    ... et {len(errs)-15} autres")
if ok != "true":
    print("\n  -> rien n'a ete cree. Corriger les erreurs ci-dessus avant de recommencer.")
    sys.exit(1)

prj = [(p.get("alias"), p.get("accession")) for p in r.iter("PROJECT")]
sam = [(s.get("alias"), s.get("accession")) for s in r.iter("SAMPLE")]
print(f"  etude      : {prj}")
print(f"  echantillons crees : {len(sam)}")

out = os.path.join(os.path.dirname(sys.argv[1]), "sample_accessions.tsv")
with open(out, "w", newline="") as f:
    w = csv.writer(f, delimiter="\t"); w.writerow(["alias","accession"])
    for a, acc in sam: w.writerow([a, acc])
    for a, acc in prj: w.writerow([a, acc])
print(f"  correspondances ecrites : {out}")
PY

echo
echo "Etape suivante : bash 2_construire_manifestes.sh"
