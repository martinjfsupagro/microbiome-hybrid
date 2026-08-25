#!/bin/bash
# TEST DECISIF ASPERA : webin-cli -ascp peut-il transferer ?
#
# Le FTP Webin est hors service depuis des mois (confirme par un collegue).
# Aspera est la voie de remplacement. Ce script cree une etude + un echantillon
# reels sur le SERVEUR DE TEST de l'ENA (via HTTPS), puis lance webin-cli avec
# l'option -ascp : il ira donc jusqu'au transfert.
#
#   module load bioinfo-cirad && module load ena-webin-cli/9.0.3
#   source test_aspera.sh
#
# Rien n'est publie : serveur de test, purge automatique, un seul fichier.

shopt -s expand_aliases
SRC=/home/martinj/work/projects/microbiome-hybrid/consolidated_dataset
DEV=https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit/

# ascp doit etre dans le PATH : c'est l'exigence de l'option -ascp
export PATH=$HOME/.aspera/sdk:$PATH
if ! command -v ascp >/dev/null 2>&1; then
  echo "ERREUR : ascp introuvable dans le PATH."
  echo "  attendu : $HOME/.aspera/sdk/ascp"
  return 1 2>/dev/null || exit 1
fi
echo "ascp : $(command -v ascp)"
ascp -A 2>&1 | head -3

CLI=""
for n in ena-webin-cli webin-cli; do type "$n" >/dev/null 2>&1 && { CLI="$n"; break; }; done
[ -z "$CLI" ] && { echo "ERREUR: chargez les modules puis relancez avec 'source'"; return 1 2>/dev/null || exit 1; }
echo "outil : $CLI"
echo

U=""; P=""
while [ -z "$U" ]; do printf "Identifiant Webin : " > /dev/tty; IFS= read -r U < /dev/tty; U="${U//[[:space:]]/}"; done
while [ -z "$P" ]; do printf "Mot de passe Webin : " > /dev/tty; IFS= read -rs P < /dev/tty; echo > /dev/tty; done
echo "  -> '$U' (${#U} car.), mot de passe ${#P} car."
echo

W=$(mktemp -d); BACK=$PWD; cd "$W" || return 1
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
  cd "$BACK"; rm -rf "$W"; unset P; return 1 2>/dev/null || exit 1
fi
echo

echo "=== ETAPE 2 : transfert via $CLI -ascp (ASPERA) ==="
R1=$(ls -S $SRC/durance1/*_R1_001.fastq.gz | tail -1); R2=${R1/_R1_/_R2_}
cp "$R1" "$R2" . 2>/dev/null
printf 'STUDY\t%s\nSAMPLE\t%s\nNAME\t%s\nINSTRUMENT\tIllumina MiSeq\nLIBRARY_SOURCE\tMETAGENOMIC\nLIBRARY_SELECTION\tPCR\nLIBRARY_STRATEGY\tAMPLICON\nFASTQ\t%s\nFASTQ\t%s\n' \
  "$PRJ" "$ERS" "run_$TAG" "$(basename "$R1")" "$(basename "$R2")" > manifest.txt
echo "  fichier : $(basename "$R1") ($(du -h "$R1"|cut -f1))"
echo
$CLI -context reads -manifest manifest.txt -userName "$U" -password "$P" -test -submit -ascp < /dev/null 2>&1 | tail -30

cd "$BACK"; rm -rf "$W"; unset P
echo
echo "============================================================"
echo "  'submission has been completed successfully'  -> ASPERA FONCTIONNE :"
echo "        je reecris toute la procedure de depot autour d'Aspera."
echo "  erreur d'authentification Aspera / ascp        -> jeton Aspera requis : support ENA."
echo "  retour au FTP dans les logs                    -> l'option -ascp n'a pas ete prise."
