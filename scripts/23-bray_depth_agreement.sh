#!/bin/bash -l
#SBATCH --job-name=bray_depth
#SBATCH --account=ondemand@biomics
#SBATCH --qos=cpu-ondemand-long
#SBATCH --partition=cpu-ondemand
#SBATCH --time=06:00:00
#SBATCH --cpus-per-task=32
#SBATCH --mem=128G
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
set -eEuo pipefail

# 23-bray_depth_agreement.sh — Bray-Curtis manque a la mesure du script 22
#
# POURQUOI. Le script 22 a mesure l'accord entre profondeurs pour Jaccard, UniFrac non
# pondere et UniFrac pondere, mais PAS Bray-Curtis : vegdist n'est pas dans l'image
# QIIME2. La note decision_depth_threshold.md declare explicitement que le comportement
# de Bray-Curtis est "vraisemblablement proche de celui d'UniFrac pondere, mais ce n'est
# pas verifie". Ce job leve ce point : Bray-Curtis ne peut entrer dans l'analyse de
# sensibilite a 500 que s'il y est mesure comme invariant a la profondeur.
#
# PROTOCOLE IDENTIQUE AU SCRIPT 22. Jeu d'echantillons FIXE (les 1 784 retenus a 3000),
# rarefaction a 500 / 1000 / 2000, N = 20 tirages, comparaison a une reference recalculee
# a 3000 AVEC LE MEME CODE (et non a la matrice N=400 existante) pour que l'ecart mesure
# la profondeur et non une difference d'implementation.
#
# TEMOIN QUI PEUT ECHOUER. La reference recalculee ici a 3000 (N=20, vegdist) est en plus
# comparee a beta_mean_bray_N400.rds. Un desaccord signalerait une erreur de lecture de
# table ou d'appariement d'identifiants, pas un manque d'iterations.
#
# Lecture de la table : meme methode que le script 15 (scan typé), qui fonctionne.
#
# Sortie : results/depth_agreement/bray_depth_agreement.{tsv,txt}

cd "$HOME/work/projects/microbiome-hybrid"
OUT=results/depth_agreement
mkdir -p "$OUT" logs
GIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo NA)
printf '%s\tSTART\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log

$HOME/bin/envs/dada2/bin/Rscript - <<'RS' 2>&1 | tee results/depth_agreement/bray_depth_agreement.txt
suppressMessages({library(vegan); library(parallel)})
NCPU <- as.integer(Sys.getenv("SLURM_CPUS_PER_TASK", "8"))
REF_DEPTH <- 3000; DEPTHS <- c(500, 1000, 2000); NDRAW <- 20
OUT <- "results/depth_agreement"
t0 <- Sys.time()
lg <- function(...) { cat(sprintf("[%6.1fs] ", as.numeric(difftime(Sys.time(), t0, units="secs"))),
                          ..., "\n", sep=""); flush.console() }

tabf <- "results/decontam/asv_table_clean.tsv"
hdr <- strsplit(readLines(tabf, n = 1L), "\t")[[1]]; nc <- length(hdr)
lg("lecture de la table...")
dat <- scan(tabf, what = c(list(""), rep(list(0L), nc - 1L)), sep = "\t", skip = 1L, quiet = TRUE)
m <- matrix(0L, nrow = length(dat[[1]]), ncol = nc - 1L, dimnames = list(dat[[1]], hdr[-1]))
for (j in 2:nc) m[, j - 1L] <- dat[[j]]
rm(dat); gc(verbose = FALSE)

keep <- colnames(m)[colSums(m) >= REF_DEPTH]
X <- t(m[, keep, drop = FALSE]); rm(m); gc(verbose = FALSE)
NS <- nrow(X)
lg("jeu FIXE : ", NS, " echantillons x ", ncol(X), " ASV")
stopifnot(NS == 1784)

# --- une moyenne de matrices Bray sur NDRAW tirages, a une profondeur donnee ---
mean_bray <- function(depth, ndraw, seed0) {
  acc <- NULL
  for (k in seq_len(ndraw)) {
    set.seed(seed0 + k)
    R <- rrarefy(X, depth)
    v <- as.vector(vegdist(R, "bray"))
    acc <- if (is.null(acc)) v else acc + v
    if (k %% 5 == 0) lg("   ", depth, " : tirage ", k, "/", ndraw)
  }
  acc / ndraw
}

lg("=== reference recalculee a ", REF_DEPTH, " (meme code) ===")
ref <- mean_bray(REF_DEPTH, NDRAW, seed0 = 90000)

# TEMOIN : accord avec la matrice N=400 existante (lecture + appariement)
lg("=== temoin : accord avec beta_mean_bray_N400.rds ===")
D400 <- readRDS("results/rarefaction/beta_mean_bray_N400.rds")
lab400 <- attr(D400, "Labels")
stopifnot(identical(lab400, rownames(X)))   # meme ordre : sinon la comparaison est fausse
v400 <- as.vector(D400)
r_w <- cor(ref, v400)
lg("   r = ", sprintf("%.6f", r_w), " | ecart absolu moyen = ",
   sprintf("%.5f", mean(abs(ref - v400))))
stopifnot(r_w > 0.999)
lg("   -> lecture de table et appariement confirmes")

rows <- list()
for (d in DEPTHS) {
  lg("=== profondeur ", d, " ===")
  v <- mean_bray(d, NDRAW, seed0 = 1000 * d)
  r <- cor(ref, v); bias <- mean(v - ref); mad <- mean(abs(v - ref))
  rows[[length(rows) + 1]] <- data.frame(
    profondeur = d, metrique = "bray", r_pearson = r, biais_moyen = bias,
    ecart_absolu_moyen = mad, distance_moyenne_ref = mean(ref),
    ecart_relatif = mad / mean(ref))
  lg("  bray  r=", sprintf("%.4f", r), " | biais ", sprintf("%+.4f", bias),
     " | ecart abs moyen ", sprintf("%.4f", mad),
     " (", sprintf("%.1f", 100 * mad / mean(ref)), " % de la distance moyenne)")
}
res <- do.call(rbind, rows)
write.table(res, file.path(OUT, "bray_depth_agreement.tsv"), sep = "\t",
            quote = FALSE, row.names = FALSE)
lg("TERMINE")
RS

printf '%s\tEND\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log
