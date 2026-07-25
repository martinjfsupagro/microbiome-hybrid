#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# FastQC + MultiQC — UN run (données brutes consolidées)
# Ne pas lancer directement — soumis par 01-quality_check_launcher.sh
# Variable reçue via --export : RUN
# ─────────────────────────────────────────────────────────────────────────────

#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=jean-francois.martin@supagro.fr
#SBATCH --cpus-per-task=8
#SBATCH --mem=8G
#SBATCH --account=ondemand@biomics
#SBATCH --qos=cpu-ondemand-long
#SBATCH --time=6:00:00

set -eEuo pipefail

: "${WORK:=$HOME/work}"
: "${SCRATCH:=$HOME/scratch_biomics}"
source "$WORK/projects/microbiome-hybrid/config/project.env"
source "$PROJECT_DIR/scripts/lib_samples.sh"

: "${RUN:?RUN non défini — soumettre via 01-quality_check_launcher.sh}"
[[ -r "$SIF_FASTQC"  ]] || { echo "ERREUR : $SIF_FASTQC introuvable"  >&2; exit 1; }
[[ -r "$SIF_MULTIQC" ]] || { echo "ERREUR : $SIF_MULTIQC introuvable" >&2; exit 1; }

IN_DIR="$RAW_DIR/$RUN"
[[ -d "$IN_DIR" ]] || { echo "ERREUR : $IN_DIR introuvable" >&2; exit 1; }

RUN_ID="${SLURM_JOB_NAME}_${SLURM_JOB_ID}"
RUN_SCRATCH="$SCRATCH_DIR/$RUN_ID"
RUN_RESULTS="$PROJECT_DIR/results/$RUN_ID"
mkdir -p "$RUN_SCRATCH/fastqc" "$RUN_RESULTS"
GIT_HASH=$(git -C "$PROJECT_DIR" rev-parse --short HEAD 2>/dev/null || echo "no-git")
cp "$0" "$RUN_RESULTS/job_script.sh"
_log() { echo "$(date -Iseconds) | $RUN_ID | $1 | $GIT_HASH | $(basename "$0") | ${2:-}" >> "$PROJECT_DIR/runs.log"; }
trap '_log FAIL "exit $?"' ERR
_log START "run=$RUN"

echo "==> FastQC sur $IN_DIR"
singularity exec --cleanenv -B "$RAW_DIR" -B "$RUN_SCRATCH" "$SIF_FASTQC" \
    fastqc --threads "$SLURM_CPUS_PER_TASK" -o "$RUN_SCRATCH/fastqc" "$IN_DIR"/*.fastq.gz

echo "==> MultiQC"
singularity exec --cleanenv -B "$RUN_SCRATCH" "$SIF_MULTIQC" \
    multiqc -o "$RUN_SCRATCH" -n "multiqc_${RUN}" "$RUN_SCRATCH/fastqc"

# Rapatrie le rapport MultiQC + les zip FastQC (légers), pas les html individuels.
rsync -a "$RUN_SCRATCH/multiqc_${RUN}.html" "$RUN_SCRATCH/multiqc_${RUN}_data" "$RUN_RESULTS/"
rsync -a "$RUN_SCRATCH/fastqc/" "$RUN_RESULTS/fastqc/" --include='*.zip' --include='*/' --exclude='*'
echo "✓ Rapport → $RUN_RESULTS/multiqc_${RUN}.html"
_log END "run=$RUN"
