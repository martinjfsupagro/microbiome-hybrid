#!/bin/bash
# Mesure le temps unitaire d'un run avant de lancer les 2304.
# Soumet 4 runs sur le serveur de TEST et chronometre.
#
#   bash 3b_chronometrer.sh

set -uo pipefail
D=/home/martinj/work/projects/microbiome-hybrid/ena_deposit
SRC=/home/martinj/work/projects/microbiome-hybrid/consolidated_dataset
SIF=/storage/replicated/cirad/binaries/img/ena-webin-cli/9.0.3/ena-webin-cli-9.0.3--hdfd78af_0.sif
CPATH="$HOME/.aspera/sdk:/usr/local/bin:/usr/bin:/bin"
O=/tmp/martinj/bench_$$
mkdir -p "$O"
export SINGULARITYENV_JAVA_TOOL_OPTIONS="-Xmx2g"

U=""; P=""
while [ -z "$U" ]; do printf "Identifiant Webin : " > /dev/tty; IFS= read -r U < /dev/tty; U="${U//[[:space:]]/}"; done
while [ -z "$P" ]; do printf "Mot de passe Webin : " > /dev/tty; IFS= read -rs P < /dev/tty; echo > /dev/tty; done
PWF=$(mktemp); chmod 600 "$PWF"; printf '%s' "$P" > "$PWF"; unset P
trap 'rm -f "$PWF"; rm -rf "$O"' EXIT INT TERM
echo

echo "=== Chronometrage de 4 runs (serveur de TEST) ==="
T0=$(date +%s)
n=0; ok=0
for M in $(ls "$D"/manifests/*.txt | head -4); do
  nom=$(basename "$M" .txt); mkdir -p "$O/$nom"
  t0=$(date +%s)
  out=$(singularity exec --env PATH="$CPATH" "$SIF" ena-webin-cli \
          -context reads -manifest "$M" -inputDir "$SRC" -outputDir "$O/$nom" \
          -userName "$U" -passwordFile "$PWF" -submit -ascp -test 2>&1)
  t=$(( $(date +%s) - t0 )); n=$((n+1))
  if printf '%s' "$out" | grep -q 'completed successfully'; then
    ok=$((ok+1))
    acc=$(printf '%s' "$out" | grep -oE '(ERR|ERX)[0-9]+' | sort -u | tr '\n' ' ')
    ftp=$(printf '%s' "$out" | grep -c 'Connecting to FTP server' || true)
    echo "  $nom : OK en ${t}s  [$acc]  (retombe sur FTP: $ftp)"
  else
    echo "  $nom : ECHEC en ${t}s"
    printf '%s' "$out" | grep -E '^ERROR' | head -2 | sed 's/^/      /'
  fi
done
TT=$(( $(date +%s) - T0 ))

echo
echo "=== Estimation ==="
if [ "$n" -gt 0 ] && [ "$TT" -gt 0 ]; then
  MOY=$(awk -v t="$TT" -v n="$n" 'BEGIN{printf "%.0f", t/n}')
  echo "  succes            : $ok / $n"
  echo "  temps moyen/run   : ${MOY}s (en sequentiel)"
  for p in 4 8 16; do
    H=$(awk -v m="$MOY" -v p="$p" 'BEGIN{printf "%.1f", 2304*m/p/3600}')
    echo "  2304 runs a PAR=$p : ~${H} h"
  done
fi
echo
echo "Choisissez PAR puis lancez :  PAR=8 bash 3_transferer_et_soumettre.sh test"
