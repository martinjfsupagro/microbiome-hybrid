#!/bin/bash
# Transfert des fastq bruts Durance vers le dropbox FTP Webin de l'ENA.
# A LANCER DEPUIS LA FRONTALE MESO (io-login.meso.umontpellier.fr), dans un tmux :
#
#   tmux new -s ena
#   bash upload_ena_ftp.sh
#   (se detacher : Ctrl-b puis d   /   revenir : tmux attach -t ena)
#
# Utilise curl (seul client FTP present sur meso). Le mot de passe est saisi
# de facon interactive et n'est jamais ecrit sur disque.
#
# Le script est RELANCABLE : les fichiers deja transferes a la bonne taille
# sont ignores. En cas de coupure, relancez simplement la meme commande.

set -uo pipefail

SRC=/home/martinj/work/projects/microbiome-hybrid/consolidated_dataset
HOST=webin2.ebi.ac.uk
PAR=4                                  # transferts simultanes
STAMP=$(date +%Y%m%d_%H%M)
LOG=$HOME/ena_upload_${STAMP}.log
DONE=$HOME/ena_upload_done.txt         # fichiers confirmes, conserve entre deux passages
touch "$DONE"

read -rp  "Identifiant Webin (ex. Webin-12345) : " WEBIN_USER
read -rsp "Mot de passe Webin : " WEBIN_PASS; echo
export WEBIN_USER WEBIN_PASS HOST

# Test d'authentification prealable : evite de lancer 4608 transferts voues a l'echec
echo "Verification de la connexion (FTPS)..."
if ! curl -sS --ssl-reqd -m 40 -u "$WEBIN_USER:$WEBIN_PASS" "ftp://$HOST/" -l >/dev/null 2>&1; then
  echo "ECHEC : impossible de s'authentifier sur $HOST en FTPS."
  echo "  - verifiez l'identifiant (le W majuscule) et le mot de passe"
  echo "  - un compte tout juste cree peut mettre jusqu'a 1 h avant que le FTP s'ouvre"
  echo "  - lancez ./diag_webin.sh pour un diagnostic detaille"
  exit 1
fi
echo "Connexion FTPS etablie."
echo

echo "=== Transfert ENA demarre $(date) ===" | tee "$LOG"

# Liste distante initiale : ce qui est deja en place (nom -> taille)
echo "Inventaire du dropbox distant..." | tee -a "$LOG"
for r in durance1 durance2 durance3; do
  curl -sS --ssl-reqd --ftp-create-dirs -u "$WEBIN_USER:$WEBIN_PASS" "ftp://$HOST/$r/" -l 2>/dev/null \
    | sed "s|^|$r/|" || true
done > /tmp/ena_remote_$$.txt
echo "  deja presents : $(wc -l < /tmp/ena_remote_$$.txt) fichier(s)" | tee -a "$LOG"

send_one() {
  local rel="$1"                                   # ex. durance1/xxx_R1_001.fastq.gz
  local run="${rel%%/*}" f="${rel#*/}"
  grep -qxF "$rel" "$DONE" 2>/dev/null && return 0
  curl -sS --ssl-reqd --ftp-create-dirs --retry 5 --retry-delay 10 --connect-timeout 30 \
       -u "$WEBIN_USER:$WEBIN_PASS" -T "$SRC/$rel" "ftp://$HOST/$run/$f"
  if [ $? -eq 0 ]; then
    echo "$rel" >> "$DONE"; printf '.'
  else
    echo "ECHEC $rel" >> "$LOG"; printf 'x'
  fi
}
export -f send_one; export SRC DONE LOG

for r in durance1 durance2 durance3; do
  echo "" | tee -a "$LOG"; echo "--- $r ---" | tee -a "$LOG"
  ( cd "$SRC/$r" && ls *.fastq.gz ) | sed "s|^|$r/|" \
    | xargs -P "$PAR" -I{} bash -c 'send_one "$@"' _ {}
  echo "" 
done

echo "" | tee -a "$LOG"
echo "=== Transfert termine $(date) ===" | tee -a "$LOG"
echo "Transferes avec succes : $(sort -u "$DONE" | wc -l) / 4608" | tee -a "$LOG"
grep -c '^ECHEC' "$LOG" 2>/dev/null | xargs -I{} echo "Echecs : {}" | tee -a "$LOG"

echo "" ; echo "Verification cote serveur :"
tot=0
for r in durance1 durance2 durance3; do
  n=$(curl -sS --ssl-reqd -u "$WEBIN_USER:$WEBIN_PASS" "ftp://$HOST/$r/" -l 2>/dev/null | grep -c 'fastq.gz')
  echo "  $r : $n / 1536"; tot=$((tot+n))
done
echo "  TOTAL : $tot / 4608"
rm -f /tmp/ena_remote_$$.txt
[ "$tot" -eq 4608 ] && echo "Transfert complet. Vous pouvez lancer submit_ena.sh." \
                    || echo "Incomplet : relancez ce meme script, il reprendra ou il en est."
