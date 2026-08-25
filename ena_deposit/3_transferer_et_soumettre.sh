#!/bin/bash
# ETAPE 3/3 : transferer les fichiers et soumettre les runs, via Aspera.
#
# Appelle webin-cli DANS son conteneur singularity avec ascp dans le PATH du
# conteneur : sans cela, webin-cli retombe silencieusement sur le FTP (hors service).
#
#   tmux new -s ena                                  # attention : "new", pas "-s" seul
#   bash 3_transferer_et_soumettre.sh test           # valide tout, ne publie rien
#   bash 3_transferer_et_soumettre.sh prod           # POUR DE VRAI
#
# RELANCABLE : les runs deja soumis sont notes dans done_runs_<mode>.txt et ignores.
# Parallelisme : PAR=8 bash 3_transferer_et_soumettre.sh test

set -uo pipefail
MODE="${1:-}"
[ "$MODE" = "test" ] || [ "$MODE" = "prod" ] || { echo "Usage : bash $0 test|prod"; exit 1; }

D=/home/martinj/work/projects/microbiome-hybrid/ena_deposit
SRC=/home/martinj/work/projects/microbiome-hybrid/consolidated_dataset
SIF=/storage/replicated/cirad/binaries/img/ena-webin-cli/9.0.3/ena-webin-cli-9.0.3--hdfd78af_0.sif
ASPERA=$HOME/.aspera/sdk
CPATH="$ASPERA:/usr/local/bin:/usr/bin:/bin"
MAN=$D/manifests
OUT=$D/webin_out_$MODE
DONE=$D/done_runs_${MODE}.txt
LOG=$D/submit_${MODE}_$(date +%Y%m%d_%H%M).log
PAR=${PAR:-4}

[ -x "$ASPERA/ascp" ] || { echo "ERREUR : $ASPERA/ascp introuvable"; exit 1; }
[ -f "$SIF" ]         || { echo "ERREUR : $SIF introuvable"; exit 1; }
[ -d "$MAN" ]         || { echo "ERREUR : $MAN introuvable — lancer 2_construire_manifestes.py"; exit 1; }
N=$(ls "$MAN"/*.txt 2>/dev/null | wc -l)
[ "$N" -gt 0 ] || { echo "ERREUR : aucun manifeste dans $MAN"; exit 1; }

TESTFLAG=""; [ "$MODE" = "test" ] && TESTFLAG="-test"
touch "$DONE"; mkdir -p "$OUT"
DEJA=$(wc -l < "$DONE")

echo "=== Transfert + soumission des runs ($MODE) ==="
echo "  manifestes   : $N"
echo "  deja soumis  : $DEJA"
echo "  a traiter    : $((N - DEJA))"
echo "  parallelisme : $PAR   (ajustable : PAR=8 bash $0 $MODE)"
echo "  rapports     : $OUT"
echo "  journal      : $LOG"
echo
echo "  Duree : chaque run demande un demarrage de JVM + validation (~15-30 s)."
echo "  Le transfert lui-meme est rapide (7 Mo/s mesures). Compter 2 a 4 h a PAR=4,"
echo "  moins a PAR=8. Le script est relancable : une coupure ne perd rien."
echo

if [ "$MODE" = "prod" ] && [ "${NONINTERACTIF:-0}" != "1" ]; then
  echo "ATTENTION : soumission REELLE. Les donnees seront publiques."
  printf "Taper OUI pour confirmer : "; read -r C
  [ "$C" = "OUI" ] || { echo "annule."; exit 1; }
  echo
fi

# Identifiants : soit par variables (job SLURM via 3c_lancer_en_job.sh),
# soit au clavier (execution interactive).
if [ "${NONINTERACTIF:-0}" = "1" ]; then
  U="${WEBIN_USER:?WEBIN_USER absent}"
  PWF="${WEBIN_PWF:?WEBIN_PWF absent}"
  [ -r "$PWF" ] || { echo "ERREUR : fichier de mot de passe $PWF illisible"; exit 1; }
  echo "  identifiant : $U (mode non interactif)"
else
  U=""; P=""
  while [ -z "$U" ]; do printf "Identifiant Webin : " > /dev/tty; IFS= read -r U < /dev/tty; U="${U//[[:space:]]/}"; done
  while [ -z "$P" ]; do printf "Mot de passe Webin : " > /dev/tty; IFS= read -rs P < /dev/tty; echo > /dev/tty; done
  # Mot de passe transmis par fichier en droits 600 (-passwordFile) : jamais dans la
  # ligne de commande, donc absent de "ps" et des journaux.
  PWF=$(mktemp); chmod 600 "$PWF"; printf '%s' "$P" > "$PWF"; unset P
  trap 'rm -f "$PWF"' EXIT INT TERM
fi
echo

# Brider la JVM : sinon _JAVA_OPTIONS=-Xmx8g x PAR sature la frontale
export SINGULARITYENV_JAVA_TOOL_OPTIONS="-Xmx2g"

soumettre() {
  local m="$1" nom out acc
  nom=$(basename "$m" .txt)
  grep -qxF "$nom" "$DONE" 2>/dev/null && return 0
  mkdir -p "$OUT/$nom"                      # webin-cli exige un outputDir EXISTANT
  out=$(singularity exec --env PATH="$CPATH" "$SIF" ena-webin-cli \
          -context reads -manifest "$m" -inputDir "$SRC" -outputDir "$OUT/$nom" \
          -userName "$U" -passwordFile "$PWF" -submit -ascp $TESTFLAG 2>&1)
  if printf '%s' "$out" | grep -q 'completed successfully'; then
    acc=$(printf '%s' "$out" | grep -oE '(ERR|ERX)[0-9]+' | sort -u | tr '\n' ',' | sed 's/,$//')
    printf '%s\tOK\t%s\n' "$nom" "$acc" >> "$LOG"
    echo "$nom" >> "$DONE"
    printf '.'
  else
    { printf '%s\tECHEC\n' "$nom"
      printf '%s' "$out" | grep -E '^ERROR' | head -3 | sed "s|^|  [$nom] |"
    } >> "$LOG"
    printf 'x'
  fi
}
export -f soumettre
export DONE LOG OUT SIF CPATH SRC U PWF TESTFLAG

echo "Transfert en cours ( . = run soumis, x = echec )"
ls "$MAN"/*.txt | xargs -P "$PAR" -I{} bash -c 'soumettre "$@"' _ {}
echo; echo

OK=$(grep -cP '\tOK\t' "$LOG" 2>/dev/null || true); OK=${OK:-0}
KO=$(grep -cP '\tECHEC' "$LOG" 2>/dev/null || true); KO=${KO:-0}
TOT=$(wc -l < "$DONE")
echo "=== Bilan ==="
echo "  runs soumis  : $OK"
echo "  echecs       : $KO"
echo "  cumul total  : $TOT / $N"
if [ "$KO" -gt 0 ]; then
  echo
  echo "Premieres erreurs :"
  grep -A1 -P '\tECHEC' "$LOG" | head -12
  echo
  echo "Relancez la meme commande : seuls les runs non aboutis seront retentes."
fi
if [ "$TOT" -eq "$N" ]; then
  echo
  if [ "$MODE" = "test" ]; then
    echo "Validation complete des $N runs. Vous pouvez lancer :"
    echo "    bash $0 prod"
  else
    echo "DEPOT TERMINE. Accessions dans : $LOG"
    echo "Transmettez-moi ce fichier : je consolide et redige le Data availability."
  fi
fi
