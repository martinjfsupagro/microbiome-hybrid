#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Fusion des 3 tables d'ASV + chimères + taxonomie
# Usage : cd ~/work/projects/microbiome-hybrid && sbatch scripts/05-merge_taxonomy.sh
#
# 1. mergeSequenceTables(seqtab_durance1/2/3) — les échantillons sont suffixés
#    par run (__durance1…) : les 3 séquençages des mêmes 768 librairies restent
#    DISTINCTS (2304 colonnes), pour pouvoir estimer l'effet run en aval.
# 2. removeBimeraDenovo sur la table fusionnée (pratique DADA2 multi-run).
# 3. assignTaxonomy SILVA (si $SILVA_TRAIN renseigné) + filtre de sécurité
#    Mitochondria / Chloroplast / Eukaryota (cf. co-contamination 12S/hôte).
#
# Sorties dans results/<run_id>/ ET results/dada2_final/ (stable) :
#   seqtab_nochim.rds, asv.fasta, asv_table.tsv, track_all.csv,
#   taxonomy.tsv + asv_table_filtered.tsv (si SILVA)
# ─────────────────────────────────────────────────────────────────────────────

#SBATCH --job-name=dada2_merge_tax
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=jean-francois.martin@supagro.fr
#SBATCH --cpus-per-task=16
#SBATCH --mem=256G
#SBATCH --account=ondemand@biomics
#SBATCH --qos=cpu-ondemand-long
#SBATCH --time=12:00:00
# NB : assignTaxonomy réplique la base SILVA (~452 k réfs) par thread → gros pic
# mémoire. 64G était insuffisant (OOM à 16 threads) ; les nœuds cpu-ondemand
# ont ~1,4 To, 256G est confortable.

set -eEuo pipefail

: "${WORK:=$HOME/work}"
: "${SCRATCH:=$HOME/scratch_biomics}"
source "$WORK/projects/microbiome-hybrid/config/project.env"
export PATH="$R_ENV/bin:$PATH"
command -v Rscript >/dev/null || { echo "ERREUR : Rscript introuvable dans $R_ENV/bin" >&2; exit 1; }

SHARED_DIR="$SCRATCH_DIR/dada2_shared"
for RUN in $RUNS; do
    [[ -f "$SHARED_DIR/seqtab_$RUN.rds" ]] || { echo "ERREUR : $SHARED_DIR/seqtab_$RUN.rds absent — lancer 04 pour $RUN" >&2; exit 1; }
done

RUN_ID="${SLURM_JOB_NAME}_${SLURM_JOB_ID}"
RUN_SCRATCH="$SCRATCH_DIR/$RUN_ID"
RUN_RESULTS="$PROJECT_DIR/results/$RUN_ID"
FINAL_DIR="$PROJECT_DIR/results/dada2_final"
mkdir -p "$RUN_SCRATCH" "$RUN_RESULTS" "$FINAL_DIR"
GIT_HASH=$(git -C "$PROJECT_DIR" rev-parse --short HEAD 2>/dev/null || echo "no-git")
cp "$0" "$RUN_RESULTS/job_script.sh"
_log() { echo "$(date -Iseconds) | $RUN_ID | $1 | $GIT_HASH | $(basename "$0") | ${2:-}" >> "$PROJECT_DIR/runs.log"; }
trap '_log FAIL "exit $?"' ERR
_log START

export R_RUNS="$RUNS" R_SHARED_DIR="$SHARED_DIR" R_OUT="$RUN_RESULTS" \
       R_FINAL="$FINAL_DIR" R_SILVA_TRAIN="$SILVA_TRAIN" R_SILVA_SPECIES="$SILVA_SPECIES"

Rscript - <<'EOF'
suppressPackageStartupMessages(library(dada2))

runs     <- strsplit(Sys.getenv("R_RUNS"), "\\s+")[[1]]
shared   <- Sys.getenv("R_SHARED_DIR")
out      <- Sys.getenv("R_OUT")
final    <- Sys.getenv("R_FINAL")
silva    <- Sys.getenv("R_SILVA_TRAIN")
silvasp  <- Sys.getenv("R_SILVA_SPECIES")
nthreads <- as.integer(Sys.getenv("SLURM_CPUS_PER_TASK", unset = "8"))

# ── 1. Fusion, échantillons suffixés par run ──────────────────────────────────
cat("=== mergeSequenceTables ===\n")
tabs <- lapply(runs, function(r) {
    st <- readRDS(file.path(shared, sprintf("seqtab_%s.rds", r)))
    rownames(st) <- paste0(rownames(st), "__", r)   # garde les 3 runs distincts
    cat(sprintf("  %s : %d échantillons × %d ASV\n", r, nrow(st), ncol(st)))
    st
})
seqtab <- if (length(tabs) == 1) tabs[[1]] else do.call(mergeSequenceTables, tabs)
cat(sprintf("  fusion : %d échantillons × %d ASV\n\n", nrow(seqtab), ncol(seqtab)))

# ── 2. Chimères ───────────────────────────────────────────────────────────────
cat("=== removeBimeraDenovo ===\n")
seqtab_nochim <- removeBimeraDenovo(seqtab, method = "consensus",
                                    multithread = nthreads, verbose = TRUE)
cat(sprintf("  %d → %d ASV (%.1f %% des reads conservés)\n\n",
            ncol(seqtab), ncol(seqtab_nochim),
            100 * sum(seqtab_nochim) / sum(seqtab)))
cat("  distribution des longueurs d'ASV :\n"); print(table(nchar(getSequences(seqtab_nochim))))
cat("\n")

# ── Sorties de base (indépendantes de la taxonomie) ───────────────────────────
seqs <- getSequences(seqtab_nochim)
ids  <- sprintf("ASV%04d", seq_along(seqs))
save_all <- function(dir) {
    saveRDS(seqtab_nochim, file.path(dir, "seqtab_nochim.rds"))
    writeLines(as.vector(rbind(paste0(">", ids), seqs)), file.path(dir, "asv.fasta"))
    m <- t(seqtab_nochim); rownames(m) <- ids
    write.table(data.frame(ASV = ids, m, check.names = FALSE),
                file.path(dir, "asv_table.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
}
save_all(out); save_all(final)
cat(sprintf("  %d ASV, %d échantillons → asv_table.tsv / asv.fasta\n\n",
            length(seqs), nrow(seqtab_nochim)))

# ── Suivi des reads : concatène les track_<run>.csv de l'étape 04 ─────────────
tr <- do.call(rbind, lapply(runs, function(r) {
    fs <- list.files(dirname(Sys.getenv("R_OUT")), pattern = sprintf("^track_%s\\.csv$", r),
                     recursive = TRUE, full.names = TRUE)
    if (length(fs)) { d <- read.csv(fs[1]); d$run <- r; d } else NULL
}))
if (!is.null(tr)) {
    key <- paste0(tr$sample, "__", tr$run)
    tr$nonchim <- rowSums(seqtab_nochim)[key]
    write.csv(tr, file.path(final, "track_all.csv"), row.names = FALSE)
    write.csv(tr, file.path(out,   "track_all.csv"), row.names = FALSE)
    cat("  suivi des reads → track_all.csv\n\n")
}

# ── 3. Taxonomie SILVA (si disponible) ────────────────────────────────────────
if (nzchar(silva) && file.exists(silva)) {
    cat("=== assignTaxonomy (SILVA) ===\n")
    taxa <- assignTaxonomy(seqtab_nochim, silva, multithread = nthreads, tryRC = TRUE)
    if (nzchar(silvasp) && file.exists(silvasp)) taxa <- addSpecies(taxa, silvasp)
    rownames(taxa) <- ids
    write.table(data.frame(ASV = ids, taxa, check.names = FALSE),
                file.path(final, "taxonomy.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)

    # Filtre de sécurité : hors-cible co-amplifiés (cf. 12S hôte).
    tx <- as.data.frame(taxa)
    kingdom <- if ("Kingdom" %in% names(tx)) tx$Kingdom else tx[[1]]
    bad <- (is.na(kingdom) | kingdom %in% c("Eukaryota")) |
           (!is.na(tx$Order)  & tx$Order  == "Chloroplast") |
           (!is.na(tx$Family) & tx$Family == "Mitochondria")
    cat(sprintf("  filtre hors-cible : %d ASV retirés (mito/chloro/euk/non assignés)\n",
                sum(bad)))
    stf <- seqtab_nochim[, !bad, drop = FALSE]
    idf <- ids[!bad]
    mf <- t(stf); rownames(mf) <- idf
    write.table(data.frame(ASV = idf, mf, check.names = FALSE),
                file.path(final, "asv_table_filtered.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
    saveRDS(stf, file.path(final, "seqtab_nochim_filtered.rds"))
    cat(sprintf("  table filtrée : %d ASV × %d échantillons\n", ncol(stf), nrow(stf)))
} else {
    cat("=== Taxonomie SAUTÉE : SILVA_TRAIN non renseigné dans project.env ===\n")
    cat("    Table d'ASV et fasta produits ; relancer 05 une fois SILVA disponible.\n")
}
cat("\n✓ Terminé.\n")
EOF

rsync -a "$RUN_SCRATCH/" "$RUN_RESULTS/" 2>/dev/null || true
echo "✓ Résultats → $RUN_RESULTS   |   stables → $FINAL_DIR"
_log END
