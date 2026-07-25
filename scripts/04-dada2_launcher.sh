#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Lanceur DADA2 : un job par run.
# Usage :
#   cd ~/work/projects/microbiome-hybrid && bash scripts/04-dada2_launcher.sh
#   # ou, pour enchaîner après le retrait 12S (une fois par run) :
#   bash scripts/04-dada2_launcher.sh --after JID1:JID2:JID3   (afterok, ordre = $RUNS)
# ─────────────────────────────────────────────────────────────────────────────

set -eEuo pipefail
: "${WORK:=$HOME/work}"
: "${SCRATCH:=$HOME/scratch_biomics}"
source "$WORK/projects/microbiome-hybrid/config/project.env"

WORKER="$PROJECT_DIR/scripts/04-dada2_worker.sh"
[[ -f "$WORKER" ]] || { echo "ERREUR : $WORKER introuvable"; exit 1; }

# Dépendances afterok optionnelles, une par run dans l'ordre de $RUNS.
DEPS=""
if [[ "${1:-}" == "--after" ]]; then DEPS="$2"; shift 2; fi
read -ra DEP_ARR <<< "${DEPS//:/ }"

if ! git -C "$PROJECT_DIR" diff-index --quiet HEAD -- . ':(exclude)runs.log'; then
    echo "ERREUR : changements non commités — commit avant de soumettre."; exit 1
fi

i=0
for RUN in $RUNS; do
    dep_opt=()
    if [[ -n "$DEPS" && -n "${DEP_ARR[$i]:-}" ]]; then
        dep_opt=(--dependency=afterok:"${DEP_ARR[$i]}")
        echo "→ dada2_${RUN} dépend de ${DEP_ARR[$i]}"
    else
        [[ -d "$SCRATCH_DIR/clean/$RUN" ]] || { echo "ERREUR : $SCRATCH_DIR/clean/$RUN absent — lancer 02 d'abord (ou --after)"; exit 1; }
    fi
    jid=$(sbatch --parsable --job-name="dada2_${RUN}" "${dep_opt[@]}" \
                 --export=ALL,RUN="$RUN" "$WORKER")
    echo "→ soumis : dada2_${RUN}  (job $jid)"
    i=$((i+1))
done
echo "✓ Suivi : squeue -u $USER   |   tables → $SCRATCH_DIR/dada2_shared/"
