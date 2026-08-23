#!/bin/bash -l
#SBATCH --job-name=raref_converge
#SBATCH --account=ondemand@biomics
#SBATCH --qos=cpu-ondemand-long
#SBATCH --partition=cpu-ondemand
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=32
#SBATCH --mem=180G
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
set -eEuo pipefail

# 15-rarefaction_converge.sh — rarefactions repetees : alpha a N=1000, et
# convergence de la matrice beta pour fixer N.
#
# MODE RETENU (utilisateur) : rarefactions repetees, on moyenne les METRIQUES
# (jamais les tables — moyenner les tables gonflerait la richesse par union des
# detections sur les tirages, ce qui annulerait l'effet de la rarefaction).
#
# COMMENT LA CONVERGENCE EST MESUREE — point methodologique :
# comparer la moyenne cumulee a N contre celle a 2N est TROMPEUR : les deux
# partagent les N premiers tirages, sont donc autocorrelees, et l'ecart
# sous-estime l'erreur reelle. On lance donc DEUX CHAINES INDEPENDANTES
# (graines disjointes) et on compare leurs moyennes au meme N. L'ecart
# inter-chaines est une estimation honnete de l'erreur de Monte-Carlo.
#
# Sorties : results/rarefaction/
#   alpha_mean_1000.tsv        moyenne + ecart-type par echantillon, 1000 tirages
#   beta_convergence.tsv       ecart inter-chaines par palier et par metrique
#   beta_mean_bray_N<final>.rds / beta_mean_jaccard_N<final>.rds
#   rarefaction_summary.txt

cd "$HOME/work/projects/microbiome-hybrid"
OUT=results/rarefaction
mkdir -p "$OUT" logs

RSCRIPT=$HOME/bin/envs/dada2/bin/Rscript
GIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo NA)
printf '%s\tSTART\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log

"$RSCRIPT" - <<'RS'
suppressMessages({library(vegan); library(parallel)})
NCPU  <- as.integer(Sys.getenv("SLURM_CPUS_PER_TASK", "8"))
DEPTH <- 3000
N_ALPHA <- 1000
CHECKPOINTS <- c(25, 50, 100, 200)   # paliers de convergence beta, par chaine
OUT <- "results/rarefaction"

cat(sprintf("=== %d coeurs ===\n", NCPU))
tabf <- "results/decontam/asv_table_clean.tsv"
hdr <- strsplit(readLines(tabf, n = 1L), "\t")[[1]]; nc <- length(hdr)
dat <- scan(tabf, what = c(list(""), rep(list(0L), nc - 1L)), sep = "\t", skip = 1L, quiet = TRUE)
m <- matrix(0L, nrow = length(dat[[1]]), ncol = nc - 1L, dimnames = list(dat[[1]], hdr[-1]))
for (j in 2:nc) m[, j - 1L] <- dat[[j]]
rm(dat); gc(verbose = FALSE)

keep <- colnames(m)[colSums(m) >= DEPTH]
X <- t(m[, keep, drop = FALSE]); rm(m); gc(verbose = FALSE)
NS <- nrow(X)
cat(sprintf("matrice : %d echantillons x %d ASV (seuil %d)\n", NS, ncol(X), DEPTH))

# ---------------------------------------------------------------- ALPHA (N=1000)
cat(sprintf("\n=== ALPHA : %d rarefactions ===\n", N_ALPHA))
t0 <- Sys.time()
alpha_one <- function(s) {
  set.seed(s)
  R <- rrarefy(X, DEPTH)
  cbind(richness = specnumber(R), shannon = diversity(R, "shannon"),
        invsimpson = diversity(R, "invsimpson"))
}
res_a <- mclapply(seq_len(N_ALPHA), alpha_one, mc.cores = NCPU, mc.preschedule = TRUE)
bad <- !vapply(res_a, is.matrix, logical(1))
if (any(bad)) stop(sprintf("%d iterations alpha ont echoue", sum(bad)))
A <- simplify2array(res_a)                       # NS x 3 x N
alpha_mean <- apply(A, c(1,2), mean)
alpha_sd   <- apply(A, c(1,2), sd)
colnames(alpha_mean) <- paste0(colnames(alpha_mean), "_mean")
colnames(alpha_sd)   <- paste0(colnames(alpha_sd),   "_sd")
adf <- data.frame(sample = rownames(X), alpha_mean, alpha_sd, check.names = FALSE)
write.table(adf, file.path(OUT, "alpha_mean_1000.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
cat(sprintf("  fait en %.1f min\n", as.numeric(difftime(Sys.time(), t0, units = "mins"))))
cat("  ecart-type de Monte-Carlo (median sur les echantillons) :\n")
for (k in 1:3) cat(sprintf("    %-12s sd_MC = %.3f  (moyenne = %.2f)\n",
    dimnames(A)[[2]][k], median(alpha_sd[,k]), median(alpha_mean[,k])))
rm(A, res_a); gc(verbose = FALSE)

# ------------------------------------------------------- BETA : deux chaines
cat("\n=== BETA : convergence par deux chaines independantes ===\n")
NMAX <- max(CHECKPOINTS)
beta_one <- function(s) {
  set.seed(s)
  R <- rrarefy(X, DEPTH)
  list(bray = as.vector(vegdist(R, "bray")),
       jaccard = as.vector(vegdist(R, "jaccard", binary = TRUE)))
}
run_chain <- function(seed_base) {
  acc_b <- NULL; acc_j <- NULL; snaps <- list()
  done <- 0L
  for (cp in CHECKPOINTS) {
    need <- cp - done
    idx <- seed_base + done + seq_len(need)
    rr <- mclapply(idx, beta_one, mc.cores = NCPU, mc.preschedule = TRUE)
    ok <- vapply(rr, function(z) is.list(z) && !is.null(z$bray), logical(1))
    if (!all(ok)) stop(sprintf("%d iterations beta ont echoue (chaine %d)", sum(!ok), seed_base))
    sb <- Reduce(`+`, lapply(rr, `[[`, "bray"))
    sj <- Reduce(`+`, lapply(rr, `[[`, "jaccard"))
    acc_b <- if (is.null(acc_b)) sb else acc_b + sb
    acc_j <- if (is.null(acc_j)) sj else acc_j + sj
    done <- cp
    snaps[[as.character(cp)]] <- list(bray = acc_b / cp, jaccard = acc_j / cp)
    cat(sprintf("  chaine %d : palier %d atteint (%s)\n", seed_base, cp, format(Sys.time(), "%H:%M:%S")))
  }
  snaps
}
t1 <- Sys.time()
ch1 <- run_chain(10000L)
ch2 <- run_chain(90000L)
cat(sprintf("  beta fait en %.1f min\n", as.numeric(difftime(Sys.time(), t1, units = "mins"))))

rows <- list()
for (cp in CHECKPOINTS) {
  k <- as.character(cp)
  for (met in c("bray","jaccard")) {
    a <- ch1[[k]][[met]]; b <- ch2[[k]][[met]]
    d <- abs(a - b)
    rows[[length(rows)+1]] <- data.frame(
      N_par_chaine = cp, metrique = met,
      ecart_max = max(d), ecart_moyen = mean(d),
      ecart_p99 = quantile(d, 0.99, names = FALSE),
      correlation = cor(a, b),
      # erreur de Monte-Carlo de la moyenne d'UNE chaine, deduite de l'ecart
      # inter-chaines : sd(diff) = sqrt(2) * se_chaine
      se_chaine = sd(a - b) / sqrt(2),
      distance_moyenne = mean(a))
  }
}
conv <- do.call(rbind, rows)
conv$se_relative <- conv$se_chaine / conv$distance_moyenne
write.table(conv, file.path(OUT, "beta_convergence.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
cat("\n--- convergence beta (ecart entre deux chaines independantes) ---\n")
print(conv, row.names = FALSE, digits = 4)

# matrice moyenne au palier max, chaines fusionnees (2*NMAX tirages)
for (met in c("bray","jaccard")) {
  v <- (ch1[[as.character(NMAX)]][[met]] + ch2[[as.character(NMAX)]][[met]]) / 2
  D <- structure(v, class = "dist", Size = NS, Labels = rownames(X), Diag = FALSE, Upper = FALSE)
  saveRDS(D, file.path(OUT, sprintf("beta_mean_%s_N%d.rds", met, 2*NMAX)))
}
cat(sprintf("\nmatrices moyennes sauvees (N = %d tirages fusionnes)\n", 2*NMAX))

sink(file.path(OUT, "rarefaction_summary.txt"))
cat("RAREFACTIONS REPETEES — moyenne des METRIQUES\n")
cat(sprintf("Profondeur %d ; %d echantillons ; %d ASV.\n", DEPTH, NS, ncol(X)))
cat(sprintf("ALPHA : %d rarefactions. Ecart-type de Monte-Carlo median par indice :\n", N_ALPHA))
for (k in 1:3) cat(sprintf("  %-12s sd_MC = %.3f  (moyenne mediane = %.2f)\n",
    colnames(alpha_sd)[k], median(alpha_sd[,k]), median(alpha_mean[,k])))
cat("\nBETA : convergence mesuree par DEUX CHAINES INDEPENDANTES comparees au meme N.\n")
cat("(comparer une moyenne cumulee a N contre 2N serait autocorrele et\n")
cat(" sous-estimerait l'erreur ; se_chaine = sd(chaine1 - chaine2)/sqrt(2).)\n\n")
print(conv, row.names = FALSE, digits = 4)
cat(sprintf("\nMatrices moyennes conservees au palier %d par chaine, fusionnees (%d tirages).\n", NMAX, 2*NMAX))
sink()
cat("\n=== termine ===\n")
RS

printf '%s\tEND\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log
cat results/rarefaction/rarefaction_summary.txt
