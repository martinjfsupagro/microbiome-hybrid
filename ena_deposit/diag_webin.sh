#!/bin/bash
# Diagnostic de l'authentification FTP Webin (erreur 530).
# Ne transfere aucun fichier, ne modifie rien. Le mot de passe est saisi au clavier.

echo "=== Diagnostic authentification Webin ==="
read -rp  "Identifiant Webin : " U
read -rsp "Mot de passe Webin : " P; echo
echo

# Longueur et caracteres speciaux : detecte un copier-coller tronque ou une espace parasite
echo "Identifiant saisi  : '$U'  (${#U} caracteres)"
echo "Mot de passe       : ${#P} caracteres"
case "$P" in
  *" ") echo "  ATTENTION : le mot de passe se termine par une ESPACE" ;;
  " "*) echo "  ATTENTION : le mot de passe commence par une ESPACE" ;;
esac
echo

for H in webin2.ebi.ac.uk webin.ebi.ac.uk; do
  echo "--- $H (FTPS) ---"
  OUT=$(curl -sS --ssl-reqd -m 30 -u "$U:$P" "ftp://$H/" -l 2>&1)
  RC=$?
  if [ $RC -eq 0 ]; then
    echo "  CONNEXION REUSSIE"
    N=$(printf '%s\n' "$OUT" | grep -c . )
    echo "  entrees a la racine du dropbox : $N"
    printf '%s\n' "$OUT" | head -5 | sed 's/^/    /'
  else
    echo "  ECHEC (code curl $RC)"
    printf '%s\n' "$OUT" | head -3 | sed 's/^/    /'
  fi
  echo
done

# L'API Webin utilise les MEMES identifiants : distingue "compte invalide"
# de "compte valide mais acces FTP indisponible"
echo "--- Verification du compte via l'API Webin (HTTPS) ---"
CODE=$(curl -sS -m 30 -o /tmp/webin_auth_$$.txt -w '%{http_code}' \
  -X POST -H "Content-Type: application/json" \
  -d "{\"authRealms\":[\"ENA\"],\"password\":\"$P\",\"username\":\"$U\"}" \
  https://www.ebi.ac.uk/ena/submit/webin/auth/token 2>&1)
case "$CODE" in
  200) echo "  Identifiants VALIDES (l'API a delivre un jeton)."
       echo "  -> le compte est bon ; le probleme est specifique au FTP." ;;
  401|403) echo "  Identifiants REFUSES par l'API (code $CODE)."
       echo "  -> identifiant ou mot de passe incorrect, ou mot de passe change recemment." ;;
  *) echo "  Reponse inattendue : code $CODE"; head -c 200 /tmp/webin_auth_$$.txt ;;
esac
rm -f /tmp/webin_auth_$$.txt
echo
echo "=== Fin du diagnostic ==="
