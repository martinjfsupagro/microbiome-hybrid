#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# DADA2 — UN run, du filtrage à la table d'ASV (SANS retrait chimères)
# Ne pas lancer directement — soumis par 04-dada2_launcher.sh
# Variable reçue via --export : RUN
#
# Entrée  : $SCRATCH_DIR/clean/$RUN/{SAMPLE}_R{1,2}.fastq.gz  (V4, 12S retiré)
# Sortie  : $SCRATCH_DIR/dada2_shared/seqtab_$RUN.rds   (table brute makeSequenceTable)
#           track_$RUN.csv, quality_$RUN.pdf → results/
#
# Modèle d'erreur appris PAR RUN (learnErrors) : les trois runs sont trois
# séquençages MiSeq distincts, leurs profils d'erreur diffèrent. Les chimères
# sont retirées en 05, sur la table fusionnée (pratique DADA2 multi-run).
# ─────────────────────────────────────────────────────────────────────────────

#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=jean-francois.martin@supagro.fr
#SBATCH --cpus-per-task=16
#SBATCH --mem=48G
#SBATCH --account=ondemand@biomics
#SBATCH --qos=cpu-ondemand-long
#SBATCH --time=18:00:00

set -eEuo pipefail

: "${WORK:=$HOME/work}"
: "${SCRATCH:=$HOME/scratch_biomics}"
source "$WORK/projects/microbiome-hybrid/config/project.env"

: "${RUN:?RUN non défini — soumettre via 04-dada2_launcher.sh}"
export PATH="$R_ENV/bin:$PATH"
command -v Rscript >/dev/null || { echo "ERREUR : Rscript introuvable dans $R_ENV/bin" >&2; exit 1; }

CLEAN_DIR="$SCRATCH_DIR/clean/$RUN"
SHARED_DIR="$SCRATCH_DIR/dada2_shared"
[[ -d "$CLEAN_DIR" ]] || { echo "ERREUR : $CLEAN_DIR introuvable — lancer 02 d'abord" >&2; exit 1; }

RUN_ID="${SLURM_JOB_NAME}_${SLURM_JOB_ID}"
RUN_SCRATCH="$SCRATCH_DIR/$RUN_ID"
RUN_RESULTS="$PROJECT_DIR/results/$RUN_ID"
mkdir -p "$RUN_SCRATCH" "$RUN_RESULTS" "$SHARED_DIR"
GIT_HASH=$(git -C "$PROJECT_DIR" rev-parse --short HEAD 2>/dev/null || echo "no-git")
cp "$0" "$RUN_RESULTS/job_script.sh"
_log() { echo "$(date -Iseconds) | $RUN_ID | $1 | $GIT_HASH | $(basename "$0") | ${2:-}" >> "$PROJECT_DIR/runs.log"; }
trap '_log FAIL "exit $?"' ERR
_log START "run=$RUN"

export R_RUN="$RUN" R_CLEAN_DIR="$CLEAN_DIR" R_SCRATCH="$RUN_SCRATCH" \
       R_SHARED_DIR="$SHARED_DIR" R_RESULTS="$RUN_RESULTS" \
       R_TRUNC_F="$TRUNC_F" R_TRUNC_R="$TRUNC_R"

Rscript - <<'EOF'
suppressPackageStartupMessages(library(dada2))

run       <- Sys.getenv("R_RUN")
clean_dir <- Sys.getenv("R_CLEAN_DIR")
scratch   <- Sys.getenv("R_SCRATCH")
shared    <- Sys.getenv("R_SHARED_DIR")
results   <- Sys.getenv("R_RESULTS")
truncF    <- as.integer(Sys.getenv("R_TRUNC_F"))
truncR    <- as.integer(Sys.getenv("R_TRUNC_R"))
nthreads  <- as.integer(Sys.getenv("SLURM_CPUS_PER_TASK", unset = "8"))

cat(sprintf("=== DADA2 — run %s | truncLen c(%d,%d) ===\n\n", run, truncF, truncR))

R1 <- sort(list.files(clean_dir, pattern = "_R1\\.fastq\\.gz$", full.names = TRUE))
R2 <- sort(list.files(clean_dir, pattern = "_R2\\.fastq\\.gz$", full.names = TRUE))
if (length(R1) == 0) stop("Aucun R1 dans ", clean_dir)

# Écarter les fichiers vides (contrôles négatifs après retrait 12S).
keep <- file.size(R1) > 100 & file.size(R2) > 100
R1 <- R1[keep]; R2 <- R2[keep]
snames <- sub("_R1\\.fastq\\.gz$", "", basename(R1))
cat(sprintf("  %d échantillon(s) non vide(s)\n\n", length(snames)))

# ── Profil qualité (documentation) ────────────────────────────────────────────
pdf(file.path(results, sprintf("quality_%s.pdf", run)), width = 10, height = 5)
print(plotQualityProfile(R1[seq_len(min(6, length(R1)))]) + ggplot2::ggtitle("R1"))
print(plotQualityProfile(R2[seq_len(min(6, length(R2)))]) + ggplot2::ggtitle("R2"))
invisible(dev.off())

# ── filterAndTrim ─────────────────────────────────────────────────────────────
cat("=== filterAndTrim ===\n")
filt_dir <- file.path(scratch, "filtered")
dir.create(filt_dir, showWarnings = FALSE, recursive = TRUE)
filt_R1 <- file.path(filt_dir, paste0(snames, "_R1_filt.fastq.gz"))
filt_R2 <- file.path(filt_dir, paste0(snames, "_R2_filt.fastq.gz"))

out <- filterAndTrim(
    R1, filt_R1, R2, filt_R2,
    truncLen    = c(truncF, truncR),
    maxN        = 0,
    maxEE       = c(2, 2),
    truncQ      = 2,
    rm.phix     = TRUE,
    compress    = TRUE,
    multithread = nthreads
)
cat(sprintf("  %d → %d reads (%.1f %% conservés)\n\n",
            sum(out[, 1]), sum(out[, 2]), 100 * sum(out[, 2]) / sum(out[, 1])))

# filterAndTrim peut vider un échantillon : resynchroniser.
ok <- file.exists(filt_R1) & file.exists(filt_R2)
ok <- ok & file.size(filt_R1) > 100 & file.size(filt_R2) > 100
filt_R1 <- filt_R1[ok]; filt_R2 <- filt_R2[ok]; snames <- snames[ok]
if (length(filt_R1) == 0) stop("Plus aucun read après filtrage pour ", run)
names(filt_R1) <- snames; names(filt_R2) <- snames

# ── learnErrors (par run) ─────────────────────────────────────────────────────
cat("=== learnErrors ===\n")
err_fwd <- learnErrors(filt_R1, multithread = nthreads, verbose = FALSE)
err_rev <- learnErrors(filt_R2, multithread = nthreads, verbose = FALSE)
saveRDS(err_fwd, file.path(shared, sprintf("err_fwd_%s.rds", run)))
saveRDS(err_rev, file.path(shared, sprintf("err_rev_%s.rds", run)))
pdf(file.path(results, sprintf("errors_%s.pdf", run)), width = 9, height = 7)
print(plotErrors(err_fwd, nominalQ = TRUE)); print(plotErrors(err_rev, nominalQ = TRUE))
invisible(dev.off())
cat("  modèles d'erreur estimés\n\n")

# ── dada + mergePairs ─────────────────────────────────────────────────────────
cat("=== dada + mergePairs ===\n")
dada_fwd <- dada(filt_R1, err = err_fwd, multithread = nthreads, verbose = FALSE)
dada_rev <- dada(filt_R2, err = err_rev, multithread = nthreads, verbose = FALSE)
mergers  <- mergePairs(dada_fwd, filt_R1, dada_rev, filt_R2, verbose = FALSE)

seqtab <- makeSequenceTable(mergers)
if (length(snames) == 1) rownames(seqtab) <- snames
cat(sprintf("  %d échantillon(s) × %d ASV\n", nrow(seqtab), ncol(seqtab)))
cat("  distribution des longueurs d'ASV :\n"); print(table(nchar(getSequences(seqtab))))
cat("\n")

# Table BRUTE (chimères retirées en 05 sur la table fusionnée des 3 runs).
saveRDS(seqtab, file.path(shared, sprintf("seqtab_%s.rds", run)))

# ── Suivi des reads ───────────────────────────────────────────────────────────
getN <- function(x) sum(getUniques(x))
countN <- function(x) if (length(snames) == 1) getN(x) else sapply(x, getN)
track <- data.frame(
    sample    = snames,
    input     = out[ok, 1],
    filtered  = out[ok, 2],
    denoisedF = countN(dada_fwd),
    denoisedR = countN(dada_rev),
    merged    = countN(mergers),
    row.names = NULL
)
write.csv(track, file.path(results, sprintf("track_%s.csv", run)), row.names = FALSE)
cat(sprintf("  fusion médiane : %.1f %% des reads filtrés\n",
            100 * median(track$merged / track$filtered, na.rm = TRUE)))
cat(sprintf("\n✓ %s : %d ASV bruts, table → seqtab_%s.rds\n", run, ncol(seqtab), run))
EOF

rsync -a "$RUN_SCRATCH/" "$RUN_RESULTS/" --exclude 'filtered/'
echo "✓ Résultats → $RUN_RESULTS   |   table → $SHARED_DIR/seqtab_$RUN.rds"
_log END "run=$RUN"
