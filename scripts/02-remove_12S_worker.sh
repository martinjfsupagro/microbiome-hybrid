#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Retrait du 12S hôte co-amplifié — UN run, tous ses échantillons
# Ne pas lancer directement — soumis par 02-remove_12S_launcher.sh
# Variable reçue via --export : RUN (durance1|durance2|durance3)
#
# Les amorces 16S V4 (Caporaso 515F/806R) co-amplifient le 12S mitochondrial de
# l'hôte (poisson) : 15-67 % des lectures selon l'échantillon (mesuré). On ne
# peut pas le filtrer après DADA2 (truncLen unique inadapté à deux longueurs
# d'insert ; la queue d'adaptateur du 12S entre dans learnErrors comme du signal
# et ressort en ASV parasites). On le retire donc en amont, par la LONGUEUR.
#
# Principe (établi sur le projet Apron, même assay) : l'insert V4 réel (~253 pb)
# n'est jamais entièrement lu par un read de 251 pb, donc l'amorce opposée
# n'apparaît pas en 3' → le read reste à ~251 pb. Le 12S (~190 pb) est lu de
# part en part : l'amorce opposée apparaît en 3', cutadapt la retire, le read
# tombe à ~172 pb et passe sous --minimum-length 240 → écarté. Les dimères
# d'amorces tombent à ~3-5 pb, écartés de même.
#   -a = complément inverse de 806R ; -A = complément inverse de 515F.
# Les lectures écartées sont CONSERVÉES (--too-short-output) : le 12S est un
# signal hôte exploitable, pas un déchet.
# ─────────────────────────────────────────────────────────────────────────────

#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=jean-francois.martin@supagro.fr
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G
#SBATCH --account=ondemand@biomics
#SBATCH --qos=cpu-ondemand-long
#SBATCH --time=6:00:00

set -eEuo pipefail

: "${WORK:=$HOME/work}"
: "${SCRATCH:=$HOME/scratch_biomics}"
source "$WORK/projects/microbiome-hybrid/config/project.env"
source "$PROJECT_DIR/scripts/lib_samples.sh"

: "${RUN:?RUN non défini — soumettre via 02-remove_12S_launcher.sh}"
[[ -r "$SIF_CUTADAPT" ]] || { echo "ERREUR : conteneur introuvable : $SIF_CUTADAPT" >&2; exit 1; }

IN_DIR="$RAW_DIR/$RUN"
CLEAN_DIR="$SCRATCH_DIR/clean/$RUN"
TOOSHORT_DIR="$CLEAN_DIR/too_short_12S"
[[ -d "$IN_DIR" ]] || { echo "ERREUR : $IN_DIR introuvable" >&2; exit 1; }

# Le dossier de sortie est VIDÉ avant d'écrire : sinon les fastq d'un run
# précédent y survivraient et seraient traités par DADA2 comme le jeu courant.
# Données dérivées, regénérables.
if [[ -d "$CLEAN_DIR" ]]; then
    n_avant=$(find "$CLEAN_DIR" -name '*.fastq.gz' | wc -l)
    (( n_avant > 0 )) && { echo "==> $CLEAN_DIR contenait $n_avant fichier(s) — effacés"; rm -rf "$CLEAN_DIR"; }
fi
mkdir -p "$CLEAN_DIR" "$TOOSHORT_DIR"

# ── Répertoires / traçabilité (ne pas modifier) ───────────────────────────────
RUN_ID="${SLURM_JOB_NAME}_${SLURM_JOB_ID}"
RUN_SCRATCH="$SCRATCH_DIR/$RUN_ID"
RUN_RESULTS="$PROJECT_DIR/results/$RUN_ID"
mkdir -p "$RUN_SCRATCH" "$RUN_RESULTS"
GIT_HASH=$(git -C "$PROJECT_DIR" rev-parse --short HEAD 2>/dev/null || echo "no-git")
cp "$0" "$RUN_RESULTS/job_script.sh"
_log() { echo "$(date -Iseconds) | $RUN_ID | $1 | $GIT_HASH | $(basename "$0") | ${2:-}" >> "$PROJECT_DIR/runs.log"; }
trap '_log FAIL "exit $?"' ERR
_log START "run=$RUN"

# ── Retrait du 12S ────────────────────────────────────────────────────────────
# Compléments inverses des amorces (voir en-tête). Dérivés de PRIMER_515F/806R.
RC_806R="ATTAGAWACCCBDGTAGTCC"   # rc de GGACTACHVGGGTWTCTAAT
RC_515F="TTACCGCGGCKGCTGGCAC"    # rc de GTGCCAGCMGCCGCGGTAA
MIN_LEN=240

mapfile -t R1_LIST < <(lister_R1 "$IN_DIR")
(( ${#R1_LIST[@]} > 0 )) || { echo "ERREUR : aucun R1 dans $IN_DIR" >&2; exit 1; }
verifier_paires "$IN_DIR" || exit 1
noms_dupliques "$IN_DIR" || exit 1
echo "==> $RUN : ${#R1_LIST[@]} échantillons à nettoyer (12S)"
echo ""

N=0; TOT_IN=0; TOT_V4=0; TOT_12S=0
for R1 in "${R1_LIST[@]}"; do
    R2="$(fichier_R2 "$R1")"
    SAMPLE="$(nom_echantillon "$R1")"

    rapport=$(singularity exec --cleanenv -B "$RAW_DIR" -B "$SCRATCH_DIR" "$SIF_CUTADAPT" \
        cutadapt \
            -a "$RC_806R" -A "$RC_515F" \
            -e 0.1 -O 10 \
            --minimum-length "$MIN_LEN" \
            --cores "$SLURM_CPUS_PER_TASK" \
            --too-short-output       "$TOOSHORT_DIR/${SAMPLE}_R1.fastq.gz" \
            --too-short-paired-output "$TOOSHORT_DIR/${SAMPLE}_R2.fastq.gz" \
            -o "$CLEAN_DIR/${SAMPLE}_R1.fastq.gz" \
            -p "$CLEAN_DIR/${SAMPLE}_R2.fastq.gz" \
            --json "$RUN_SCRATCH/${SAMPLE}.12s.json" \
            "$R1" "$R2" 2>&1)

    # `|| true` : sur un fichier vide (contrôle négatif), cutadapt n'écrit pas
    # « Pairs written » ; grep échouerait et set -e tuerait le job.
    tin=$(grep -oP 'Total read pairs processed:\s+\K[\d,]+'        <<< "$rapport" | tr -d ',' || true)
    v4=$( grep -oP 'Pairs written \(passing filters\):\s+\K[\d,]+' <<< "$rapport" | tr -d ',' || true)
    tin="${tin:-0}"; v4="${v4:-0}"; s12=$(( tin - v4 ))
    pct=0; (( tin > 0 )) && pct=$(( 100 * s12 / tin ))
    printf "  %-18s : %7d lus  %7d V4  %7d 12S/dimères (%d%%)\n" "$SAMPLE" "$tin" "$v4" "$s12" "$pct"

    (( TOT_IN += tin, TOT_V4 += v4, TOT_12S += s12, N++ )) || true
done

echo ""
pct=0; (( TOT_IN > 0 )) && pct=$(( 100 * TOT_12S / TOT_IN ))
echo "==> $RUN terminé : $N échantillons | $TOT_IN lus | $TOT_V4 V4 conservés | $TOT_12S 12S/dimères écartés ($pct%)"
echo "    V4 propres     → $CLEAN_DIR"
echo "    12S conservés  → $TOOSHORT_DIR"

# ── Contrôle : longueur des V4 conservés (doit rester ~251, pas de 12S résiduel)
echo ""
echo "==> Longueur des R1 conservés sur 5 fichiers (doit être ~250-251) :"
while IFS= read -r f; do
    printf "  %-40s : " "$(basename "$f")"
    zcat "$f" | awk 'NR%4==2{print length($0)}' | sort -n | uniq -c | sort -rn | head -1 | awk '{printf "pic %s pb (%s reads)\n",$2,$1}'
done < <(find "$CLEAN_DIR" -maxdepth 1 -name '*_R1.fastq.gz' | shuf -n 5)

# JSON/logs → results (les fastq nettoyés restent en scratch, lus par DADA2)
rsync -a "$RUN_SCRATCH/" "$RUN_RESULTS/"
echo ""
echo "✓ JSON/logs → $RUN_RESULTS"
_log END "run=$RUN samples=$N in=$TOT_IN v4=$TOT_V4 rm12S=$TOT_12S"
