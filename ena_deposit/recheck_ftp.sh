#!/bin/bash
# Re-test du FTP Webin avec le NOUVEAU mot de passe.
# Ne transfere rien. A lancer normalement :  bash recheck_ftp.sh

echo "=== Re-test FTP Webin (nouveau mot de passe) ==="
U=""; P=""
while [ -z "$U" ]; do printf "Identifiant Webin : " > /dev/tty; IFS= read -r U < /dev/tty; U="${U//[[:space:]]/}"; done
while [ -z "$P" ]; do printf "Mot de passe Webin : " > /dev/tty; IFS= read -rs P < /dev/tty; echo > /dev/tty; done
echo "  -> '$U' (${#U} car.), mot de passe ${#P} car."
echo

OK=0
for H in webin2.ebi.ac.uk webin.ebi.ac.uk; do
  OUT=$(curl -sS --ssl-reqd -m 40 -u "$U:$P" "ftp://$H/" -l 2>&1); RC=$?
  if [ $RC -eq 0 ]; then
    N=$(printf '%s\n' "$OUT" | grep -c .)
    echo "  FTPS $H : CONNEXION OK ($N entree(s) dans le dropbox)"
    OK=1
  else
    echo "  FTPS $H : ECHEC -> $(printf '%s' "$OUT" | head -1)"
  fi
done
unset P
echo
echo "============================================================"
if [ $OK -eq 1 ]; then
  echo "FTP OPERATIONNEL. Vous pouvez lancer le transfert :"
  echo "    tmux new -s ena"
  echo "    ./upload_ena_ftp.sh"
else
  echo "FTP toujours refuse alors que webin-cli s'authentifie."
  echo "-> le compte est bon ; c'est le service FTP qui pose probleme."
  echo "   Deux options : envoyer mail_support_ena.txt, ou passer par webin-cli"
  echo "   (dites-le moi, je reecris la procedure autour de webin-cli)."
fi
