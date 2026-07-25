#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Lanceur retrait 12S : un job SLURM par run (3)
# Usage : cd ~/work/projects/microbiome-hybrid && bash scripts/02-remove_12S_launcher.sh
# ─────────────────────────────────────────────────────────────────────────────

set -eEuo pipefail

: "${WORK:=$HOME/work}"
: "${SCRATCH:=$HOME/scratch_biomics}"
source "$WORK/projects/microbiome-hybrid/config/project.env"
source "$PROJECT_DIR/scripts/lib_samples.sh"

WORKER="$PROJECT_DIR/scripts/02-remove_12S_worker.sh"
[[ -f "$WORKER" ]] || { echo "ERREUR : $WORKER introuvable"; exit 1; }

# ── Validations globales avant de soumettre quoi que ce soit ──────────────────
for RUN in $RUNS; do
    IN_DIR="$RAW_DIR/$RUN"
    [[ -d "$IN_DIR" ]] || { echo "ERREUR : $IN_DIR introuvable"; exit 1; }
    echo "→ $RUN : $(lister_R1 "$IN_DIR" | wc -l) échantillons"
    verifier_paires "$IN_DIR" || exit 1
    noms_dupliques  "$IN_DIR" || exit 1
done

# Intégrité gzip : 10 fichiers au hasard sur l'ensemble.
echo "→ contrôle gzip (10 fichiers au hasard)"
corrompus=0
while IFS= read -r f; do
    gzip -t "$f" 2>/dev/null || { echo "  ✗ corrompu : $f"; corrompus=$((corrompus+1)); }
done < <(find "$RAW_DIR" -name '*_R1_*.fastq.gz' | shuf -n 10)
(( corrompus == 0 )) || { echo "ERREUR : $corrompus fichier(s) corrompu(s)"; exit 1; }
echo "  ✓ aucun fichier corrompu"

# runs.log exclu : chaque job y écrit sa ligne START.
if ! git -C "$PROJECT_DIR" diff-index --quiet HEAD -- . ':(exclude)runs.log'; then
    echo "ERREUR : changements non commités dans $PROJECT_DIR — commit avant de soumettre."
    exit 1
fi

# ── Soumission : un worker par run ────────────────────────────────────────────
echo ""
for RUN in $RUNS; do
    jid=$(sbatch --parsable --job-name="rm12S_${RUN}" --export=ALL,RUN="$RUN" "$WORKER")
    echo "→ soumis : rm12S_${RUN}  (job $jid)"
done

echo ""
echo "✓ Suivi : squeue -u $USER    |    bash scripts/check_run.sh results/rm12S_<RUN>_<JOBID>"
