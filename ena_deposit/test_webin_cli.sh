#!/bin/bash
# Test d'authentification avec l'outil officiel ENA (ena-webin-cli).
#
# A LANCER AVEC "source" (l'outil est un alias, invisible dans un sous-shell) :
#
#   module load bioinfo-cirad
#   module load ena-webin-cli/9.0.3
#   source test_webin_cli.sh
#
# Ne soumet rien : mode -test (serveur de validation) et un seul fichier.

shopt -s expand_aliases
SRC=/home/martinj/work/projects/microbiome-hybrid/consolidated_dataset

CLI=""
for n in ena-webin-cli webin-cli; do
  if type "$n" >/dev/null 2>&1; then CLI="$n"; break; fi
done
if [ -z "$CLI" ]; then
  echo "ERREUR : ni 'ena-webin-cli' ni 'webin-cli' n'est disponible dans ce shell."
  echo "  module load bioinfo-cirad && module load ena-webin-cli/9.0.3"
  echo "  puis : source test_webin_cli.sh"
  return 1 2>/dev/null || exit 1
fi
echo "outil : $CLI"

# --- Saisie AVANT tout appel a l'outil : le conteneur Java absorbe l'entree ---
# Lecture explicite sur /dev/tty, avec controle de non-vacuite.
U=""; P=""
while [ -z "$U" ]; do
  printf "Identifiant Webin (ex. Webin-51841) : " > /dev/tty
  IFS= read -r U < /dev/tty
  U="${U//[[:space:]]/}"
  [ -z "$U" ] && echo "  (saisie vide, recommencez)" > /dev/tty
done
while [ -z "$P" ]; do
  printf "Mot de passe Webin : " > /dev/tty
  IFS= read -rs P < /dev/tty; echo > /dev/tty
  [ -z "$P" ] && echo "  (saisie vide, recommencez)" > /dev/tty
done
echo "  -> identifiant '$U' (${#U} car.), mot de passe ${#P} car."
echo

W=$(mktemp -d)
R1=$(ls -S $SRC/durance1/*_R1_001.fastq.gz | tail -1)
R2=${R1/_R1_/_R2_}
cp "$R1" "$R2" "$W"/ 2>/dev/null
BACK=$PWD; cd "$W" || return 1
printf 'STUDY\tERP000000\nSAMPLE\tERS0000000\nNAME\ttest_auth_%s\nINSTRUMENT\tIllumina MiSeq\nLIBRARY_SOURCE\tMETAGENOMIC\nLIBRARY_SELECTION\tPCR\nLIBRARY_STRATEGY\tAMPLICON\nFASTQ\t%s\nFASTQ\t%s\n' \
  "$(date +%s)" "$(basename "$R1")" "$(basename "$R2")" > manifest.txt

echo "=== 1. $CLI -validate (mode -test, rien n'est publie) ==="
$CLI -context reads -manifest manifest.txt -userName "$U" -password "$P" -test -validate < /dev/null 2>&1 | tail -25
echo
echo "=== 2. $CLI -submit (mode -test) : etape qui declenche le transfert ==="
$CLI -context reads -manifest manifest.txt -userName "$U" -password "$P" -test -submit < /dev/null 2>&1 | tail -30

cd "$BACK"; rm -rf "$W"; unset P
echo
echo "============================================================"
echo "LECTURE DU RESULTAT :"
echo "  - 'Invalid submission account' / authentification -> compte ou FTP en cause"
echo "  - STUDY/SAMPLE introuvables -> NORMAL (accessions bidon) = AUTH REUSSIE :"
echo "                                 le blocage venait de notre client FTP"
echo "  - erreur de transfert/upload -> meme blocage qu'avec curl"
