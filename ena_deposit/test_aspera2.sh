#!/bin/bash
# TEST ASPERA v2 — en passant le PATH DANS le conteneur singularity.
#
# Pourquoi v2 : le module ena-webin-cli est un wrapper singularity. L'option -ascp
# cherche "ascp" dans le PATH *du conteneur*, ou il etait absent : webin-cli
# retombait silencieusement sur FTP. On appelle donc singularity directement,
# avec --env PATH incluant ~/.aspera/sdk.
#
#   bash test_aspera2.sh          (plus besoin de 'source' ni des modules)

SIF=/storage/replicated/cirad/binaries/img/ena-webin-cli/9.0.3/ena-webin-cli-9.0.3--hdfd78af_0.sif
ASPERA=$HOME/.aspera/sdk
SRC=/home/martinj/work/projects/microbiome-hybrid/consolidated_dataset
DEV=https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit/
CPATH="$ASPERA:/usr/local/bin:/usr/bin:/bin"

[ -x "$ASPERA/ascp" ] || { echo "ERREUR : $ASPERA/ascp introuvable"; exit 1; }
[ -f "$SIF" ]         || { echo "ERREUR : image $SIF introuvable"; exit 1; }

wcli() { singularity exec --env PATH="$CPATH" "$SIF" ena-webin-cli "$@"; }

echo "=== verification : ascp visible dans le conteneur ==="
singularity exec --env PATH="$CPATH" "$SIF" bash -c 'command -v ascp && ascp -A 2>&1|head -2'
echo

U=""; P=""
while [ -z "$U" ]; do printf "Identifiant Webin : " > /dev/tty; IFS= read -r U < /dev/tty; U="${U//[[:space:]]/}"; done
while [ -z "$P" ]; do printf "Mot de passe Webin : " > /dev/tty; IFS= read -rs P < /dev/tty; echo > /dev/tty; done
echo "  -> '$U' (${#U} car.), mot de passe ${#P} car."
echo

W=$(mktemp -d); BACK=$PWD; cd "$W" || exit 1
TAG="asp$(date +%s)"

cat > project.xml <<EOF
<PROJECT_SET><PROJECT alias="proj_$TAG">
<TITLE>Aspera connectivity test - please ignore</TITLE>
<DESCRIPTION>Temporary test submission on the ENA test server.</DESCRIPTION>
<SUBMISSION_PROJECT><SEQUENCING_PROJECT/></SUBMISSION_PROJECT>
</PROJECT></PROJECT_SET>
EOF
cat > sample.xml <<EOF
<SAMPLE_SET><SAMPLE alias="samp_$TAG">
<TITLE>Aspera connectivity test sample</TITLE>
<SAMPLE_NAME><TAXON_ID>496924</TAXON_ID><SCIENTIFIC_NAME>fish metagenome</SCIENTIFIC_NAME></SAMPLE_NAME>
<SAMPLE_ATTRIBUTES>
<SAMPLE_ATTRIBUTE><TAG>ENA-CHECKLIST</TAG><VALUE>ERC000011</VALUE></SAMPLE_ATTRIBUTE>
<SAMPLE_ATTRIBUTE><TAG>collection date</TAG><VALUE>2017</VALUE></SAMPLE_ATTRIBUTE>
<SAMPLE_ATTRIBUTE><TAG>geographic location (country and/or sea)</TAG><VALUE>France</VALUE></SAMPLE_ATTRIBUTE>
</SAMPLE_ATTRIBUTES>
</SAMPLE></SAMPLE_SET>
EOF
cat > submission.xml <<'EOF'
<SUBMISSION><ACTIONS><ACTION><ADD/></ACTION></ACTIONS></SUBMISSION>
EOF

echo "=== ETAPE 1 : creer etude + echantillon (HTTPS, serveur de test) ==="
curl -sS -u "$U:$P" -F "SUBMISSION=@submission.xml" -F "PROJECT=@project.xml" -F "SAMPLE=@sample.xml" \
     "$DEV" -o receipt.xml 2>&1
if grep -q 'success="true"' receipt.xml 2>/dev/null; then
  PRJ=$(grep -o 'accession="ERP[0-9]*"' receipt.xml | head -1 | cut -d'"' -f2)
  ERS=$(grep -o 'accession="ERS[0-9]*"' receipt.xml | head -1 | cut -d'"' -f2)
  echo "  OK  study=$PRJ  sample=$ERS"
else
  echo "  ECHEC :"; grep -o '<ERROR>[^<]*</ERROR>' receipt.xml | head -3 | sed 's/^/    /'
  cd "$BACK"; rm -rf "$W"; unset P; exit 1
fi
echo

echo "=== ETAPE 2 : transfert via -ascp, ascp visible dans le conteneur ==="
R1=$(ls -S $SRC/durance1/*_R1_001.fastq.gz | tail -1); R2=${R1/_R1_/_R2_}
cp "$R1" "$R2" . 2>/dev/null
printf 'STUDY\t%s\nSAMPLE\t%s\nNAME\t%s\nINSTRUMENT\tIllumina MiSeq\nLIBRARY_SOURCE\tMETAGENOMIC\nLIBRARY_SELECTION\tPCR\nLIBRARY_STRATEGY\tAMPLICON\nFASTQ\t%s\nFASTQ\t%s\n' \
  "$PRJ" "$ERS" "run_$TAG" "$(basename "$R1")" "$(basename "$R2")" > manifest.txt
echo "  fichier : $(basename "$R1") ($(du -h "$R1"|cut -f1))"
echo
wcli -context reads -manifest manifest.txt -userName "$U" -password "$P" -test -submit -ascp < /dev/null 2>&1 | tail -30

cd "$BACK"; rm -rf "$W"; unset P
echo
echo "============================================================"
echo "  'Connecting to Aspera' / 'completed successfully' -> ASPERA OK, on bascule tout."
echo "  'Connecting to FTP server'                        -> -ascp encore ignore."
echo "  erreur d authentification Aspera                  -> jeton requis, support ENA."
