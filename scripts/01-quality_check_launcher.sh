#!/usr/bin/env bash
# Lanceur FastQC/MultiQC : un job par run.
# Usage : cd ~/work/projects/microbiome-hybrid && bash scripts/01-quality_check_launcher.sh
set -eEuo pipefail
: "${WORK:=$HOME/work}"
: "${SCRATCH:=$HOME/scratch_biomics}"
source "$WORK/projects/microbiome-hybrid/config/project.env"

WORKER="$PROJECT_DIR/scripts/01-quality_check_worker.sh"
[[ -f "$WORKER" ]] || { echo "ERREUR : $WORKER introuvable"; exit 1; }
if ! git -C "$PROJECT_DIR" diff-index --quiet HEAD -- . ':(exclude)runs.log'; then
    echo "ERREUR : changements non commités — commit avant de soumettre."; exit 1
fi

for RUN in $RUNS; do
    [[ -d "$RAW_DIR/$RUN" ]] || { echo "ERREUR : $RAW_DIR/$RUN introuvable"; exit 1; }
    jid=$(sbatch --parsable --job-name="fastqc_${RUN}" --export=ALL,RUN="$RUN" "$WORKER")
    echo "→ soumis : fastqc_${RUN}  (job $jid)"
done
echo "✓ Suivi : squeue -u $USER"
