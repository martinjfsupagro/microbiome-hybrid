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
# rarefaction a 500 / 1000 / 2000, comparaison a la reference a 3000.
#
# REFERENCE = beta_mean_bray_N400.rds. Le script 15 l'a produite avec exactement le meme
# appel (rrarefy(X, DEPTH) puis vegdist(R,"bray")) : c'est donc bien le meme code, et la
# recalculer serait payer 20 tirages a 7 min piece pour rien.
#
# TEMOIN QUI PEUT ECHOUER. Un petit recalcul a 3000 (3 tirages) est compare a cette
# reference. Un desaccord signalerait une erreur de lecture de table ou d'appariement
# d'identifiants — pas un manque d'iterations.
#
# COUT. Un tirage (rrarefy + vegdist sur 1784 x 44200) prend ~7 min en serie : la premiere
# version de ce script, serielle et a N=20 par profondeur, demandait ~10 h et n'ecrivait
# qu'a la fin. Corrige : tirages repartis par mclapply, N = 10 par profondeur, et ecriture
# incrementale apres chaque profondeur.
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
REF_DEPTH <- 3000; DEPTHS <- c(500, 1000, 2000); NDRAW <- 10
NWORK <- min(NCPU, 16L)   # rrarefy alloue une matrice complete par worker
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

# --- moyenne de matrices Bray sur ndraw tirages, tirages repartis sur les coeurs ---
mean_bray <- function(depth, ndraw, seed0) {
  out <- mclapply(seq_len(ndraw), function(k) {
    set.seed(seed0 + k)
    as.vector(vegdist(rrarefy(X, depth), "bray"))
  }, mc.cores = NWORK)
  # mclapply rend des objets d'erreur SANS lever : sans ce controle la moyenne serait fausse
  bad <- which(!vapply(out, is.numeric, logical(1)))
  if (length(bad)) stop("mclapply a echoue sur ", length(bad), " tirage(s) : ",
                        paste(utils::head(as.character(out[[bad[1]]]), 1), collapse=" "))
  Reduce(`+`, out) / ndraw
}

# REFERENCE : la matrice N=400 du script 15 (meme appel rrarefy + vegdist)
lg("=== reference : beta_mean_bray_N400.rds ===")
D400 <- readRDS("results/rarefaction/beta_mean_bray_N400.rds")
stopifnot(identical(attr(D400, "Labels"), rownames(X)))  # meme ordre, sinon tout est faux
ref <- as.vector(D400)
lg("   ", length(ref), " paires | distance moyenne ", sprintf("%.4f", mean(ref)))

# TEMOIN : petit recalcul a 3000 avec le code d'ici
lg("=== temoin : recalcul a ", REF_DEPTH, " (3 tirages) vs la reference ===")
chk <- mean_bray(REF_DEPTH, 3L, seed0 = 90000)
r_w <- cor(chk, ref)
lg("   r = ", sprintf("%.6f", r_w), " | ecart absolu moyen = ",
   sprintf("%.5f", mean(abs(chk - ref))))
stopifnot(r_w > 0.999)
lg("   -> lecture de table et appariement confirmes")

TSV <- file.path(OUT, "bray_depth_agreement.tsv")
cat("profondeur\tmetrique\tr_pearson\tbiais_moyen\tecart_absolu_moyen\tdistance_moyenne_ref\tecart_relatif\n",
    file = TSV)
rows <- list()
for (d in DEPTHS) {
  lg("=== profondeur ", d, " ===")
  v <- mean_bray(d, NDRAW, seed0 = 1000 * d)
  r <- cor(ref, v); bias <- mean(v - ref); mad <- mean(abs(v - ref))
  rows[[length(rows) + 1]] <- data.frame(
    profondeur = d, metrique = "bray", r_pearson = r, biais_moyen = bias,
    ecart_absolu_moyen = mad, distance_moyenne_ref = mean(ref),
    ecart_relatif = mad / mean(ref))
  cat(sprintf("%d\tbray\t%.6f\t%.6f\t%.6f\t%.6f\t%.6f\n",
              d, r, bias, mad, mean(ref), mad / mean(ref)), file = TSV, append = TRUE)
  lg("  bray  r=", sprintf("%.4f", r), " | biais ", sprintf("%+.4f", bias),
     " | ecart abs moyen ", sprintf("%.4f", mad),
     " (", sprintf("%.1f", 100 * mad / mean(ref)), " % de la distance moyenne)")
}
lg("TERMINE")
RS

printf '%s\tEND\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log
