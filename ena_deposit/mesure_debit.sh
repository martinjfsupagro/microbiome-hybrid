#!/bin/bash
# Mesure honnete du debit sortant vers l'EBI, sur un volume representatif.
# La mesure precedente (1,1 ko/s) portait sur un fichier de quelques centaines
# d'octets : elle etait dominee par la latence, pas par le debit.

echo "=== Debit sortant vers l'EBI ==="
echo

# Fichier de reference d'une taille utile, via le FTP anonyme (pas d'identifiants)
for U in \
  "https://ftp.ebi.ac.uk/pub/databases/ena/sequence/con/README" \
  "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_45/gencode.v45.annotation.gtf.gz"
do
  echo "-> $(basename $U)"
  curl -sS -o /dev/null -m 120 -w "   taille=%{size_download} o | debit=%{speed_download} o/s | temps=%{time_total} s\n" "$U" 2>&1 | tail -1
done

echo
echo "=== Conversion en estimation de transfert ==="
D=$(curl -sS -o /dev/null -m 120 -w "%{speed_download}" \
    "https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_45/gencode.v45.annotation.gtf.gz" 2>/dev/null)
if [ -n "$D" ] && [ "${D%.*}" -gt 0 ] 2>/dev/null; then
  MBS=$(awk -v d="$D" 'BEGIN{printf "%.1f", d/1048576}')
  H=$(awk -v d="$D" 'BEGIN{printf "%.1f", 11700000000/d/3600}')
  echo "  debit mesure   : $MBS Mo/s"
  echo "  11,7 Go -> environ $H h en sequentiel"
  echo "  (le transfert reel se fait en parallele : compter nettement moins)"
else
  echo "  mesure non concluante"
fi
echo
echo "Note : ce test mesure la DESCENTE (download). La MONTEE peut differer,"
echo "mais l'ordre de grandeur reste indicatif."
