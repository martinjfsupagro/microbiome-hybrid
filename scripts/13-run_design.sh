#!/bin/bash -l
#SBATCH --job-name=run_design
#SBATCH --account=ondemand@biomics
#SBATCH --qos=cpu-ondemand-long
#SBATCH --partition=cpu-ondemand
#SBATCH --time=02:00:00
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
set -eEuo pipefail

# 13-run_design.sh — caracterisation de la structure reelle des 3 runs
#
# QUESTION : quelles paires de runs partagent le meme pool d'amplicons ?
#
# Deux temoins independants, tous deux calcules a PROFONDEUR EGALE (rarefaction
# a 3000) pour que la probabilite de detection soit identique par construction :
#
#  1. DISSIMILARITE INTRA-ECHANTILLON entre versions d'un meme echantillon
#     (Bray-Curtis + Jaccard). Deux sequencages du MEME pool ne different que par
#     l'echantillonnage multinomial -> dissimilarite minimale. Une PCR
#     independante introduit en plus une variance d'amplification -> plus grande.
#
#  2. RECAPTURE DES ASV RARES. Les variants rares (1-3 lectures) d'un pool
#     resequence proviennent des MEMES molecules -> forte recapture. Une PCR
#     independante genere ses propres variants rares (erreurs, chimeres)
#     -> recapture faible.
#
# Le CONTROLE NEGATIF du raisonnement : si les trois runs etaient tous des
# resequencages du meme pool, les trois paires seraient indistinguables. Le test
# n'a de valeur que parce que ce desaccord etait possible.
#
# Entree : results/decontam/asv_table_clean.tsv (table propre, non rarefiee)
# Sorties : results/run_design/{run_design_summary.txt, pairwise_per_sample.tsv}

cd "$HOME/work/projects/microbiome-hybrid"
source config/project.env 2>/dev/null || true
OUT=results/run_design
mkdir -p "$OUT" logs

RSCRIPT=$HOME/bin/envs/dada2/bin/Rscript
GIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo NA)
printf '%s\tSTART\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log

"$RSCRIPT" - <<'RS'
suppressMessages(library(vegan))
set.seed(20260822)
DEPTH <- 3000
tabf  <- "results/decontam/asv_table_clean.tsv"
runs  <- c("durance1","durance2","durance3")

cat("=== lecture de la table ===\n")
hdr  <- strsplit(readLines(tabf, n = 1L), "\t")[[1]]
nc   <- length(hdr)
dat  <- scan(tabf, what = c(list(""), rep(list(0L), nc - 1L)),
             sep = "\t", skip = 1L, quiet = TRUE)
asv  <- dat[[1]]
m    <- matrix(0L, nrow = length(asv), ncol = nc - 1L,
               dimnames = list(asv, hdr[-1]))
for (j in 2:nc) m[, j - 1L] <- dat[[j]]
rm(dat); gc(verbose = FALSE)
cat(sprintf("  %d ASV x %d colonnes\n", nrow(m), ncol(m)))

samp <- sub("__durance[123]$", "", colnames(m))
tb   <- table(samp)
common <- names(tb)[tb == 3L]
cat(sprintf("  echantillons presents dans les 3 runs : %d\n", length(common)))

depth <- colSums(m)
D <- sapply(runs, function(r) depth[match(paste0(common, "__", r), colnames(m))])
rownames(D) <- common

cat("\n=== TEMOIN 0 : correlation des profondeurs brutes (Spearman) ===\n")
for (i in 1:2) for (j in (i+1):3) {
  rho <- cor(D[, i], D[, j], method = "spearman")
  cat(sprintf("  %s vs %s : rho = %.4f\n", runs[i], runs[j], rho))
}

keep <- common[apply(D, 1, function(x) all(x >= DEPTH))]
cat(sprintf("\nechantillons retenus (>= %d lectures dans les 3 runs) : %d\n", DEPTH, length(keep)))

cat("\n=== rarefaction a profondeur egale ===\n")
R <- list()
for (r in runs) {
  idx <- match(paste0(keep, "__", r), colnames(m))
  X   <- t(m[, idx, drop = FALSE]); rownames(X) <- keep
  R[[r]] <- rrarefy(X, DEPTH)
}
rm(m); gc(verbose = FALSE)

bc  <- function(a, b) sum(abs(a - b)) / sum(a + b)
jac <- function(a, b) { A <- a > 0; B <- b > 0; 1 - sum(A & B) / sum(A | B) }
recap <- function(a, b, lo = 1L, hi = 3L) {
  s <- a >= lo & a <= hi
  if (!any(s)) return(NA_real_)
  mean(b[s] > 0)
}

pairs <- list(c("durance1","durance2"), c("durance1","durance3"), c("durance2","durance3"))
res <- list()
for (p in pairs) {
  A <- R[[p[1]]]; B <- R[[p[2]]]
  n <- nrow(A)
  v_bc <- numeric(n); v_ja <- numeric(n); v_r1 <- numeric(n); v_r2 <- numeric(n)
  for (i in seq_len(n)) {
    a <- A[i, ]; b <- B[i, ]
    v_bc[i] <- bc(a, b); v_ja[i] <- jac(a, b)
    v_r1[i] <- recap(a, b); v_r2[i] <- recap(b, a)
  }
  res[[paste(p, collapse = "|")]] <- data.frame(
    sample = keep, pair = paste(p, collapse = " vs "),
    bray = v_bc, jaccard = v_ja,
    recapture = rowMeans(cbind(v_r1, v_r2), na.rm = TRUE),
    stringsAsFactors = FALSE)
}
allres <- do.call(rbind, res)
write.table(allres, file.path("results/run_design", "pairwise_per_sample.tsv"),
            sep = "\t", quote = FALSE, row.names = FALSE)

cat("\n=== TEMOIN 1 + 2 : dissimilarite intra-echantillon et recapture des ASV rares ===\n")
cat(sprintf("%-24s %14s %14s %14s\n", "paire de runs", "Bray-Curtis", "Jaccard", "recapt. rares"))
for (k in names(res)) {
  d <- res[[k]]
  cat(sprintf("%-24s %6.4f (sd %.3f) %6.4f (sd %.3f) %6.3f (sd %.3f)\n",
      gsub("\\|", " vs ", k),
      mean(d$bray), sd(d$bray), mean(d$jaccard), sd(d$jaccard),
      mean(d$recapture, na.rm = TRUE), sd(d$recapture, na.rm = TRUE)))
}

cat("\n=== tests appariés (Wilcoxon signed-rank) ===\n")
k12 <- "durance1|durance2"; k13 <- "durance1|durance3"; k23 <- "durance2|durance3"
cmp <- function(ka, kb, var) {
  a <- res[[ka]][[var]]; b <- res[[kb]][[var]]
  w <- wilcox.test(a, b, paired = TRUE)
  cat(sprintf("  %-8s : %s (%.4f) vs %s (%.4f)  diff=%+.4f  p=%.3g\n",
      var, gsub("\\|","-",ka), mean(a), gsub("\\|","-",kb), mean(b),
      mean(a) - mean(b), w$p.value))
}
for (v in c("bray","jaccard","recapture")) {
  cmp(k12, k23, v); cmp(k13, k23, v); cmp(k12, k13, v)
}

cat("\n=== richesse observee a profondeur egale ===\n")
for (r in runs) cat(sprintf("  %s : %.1f ASV/echantillon (sd %.1f)\n",
    r, mean(rowSums(R[[r]] > 0)), sd(rowSums(R[[r]] > 0))))

sink(file.path("results/run_design","run_design_summary.txt"))
cat("CARACTERISATION DE LA STRUCTURE DES 3 RUNS\n")
cat(sprintf("Profondeur de rarefaction : %d ; echantillons : %d\n\n", DEPTH, length(keep)))
cat("Dissimilarite intra-echantillon entre versions d'un meme echantillon,\n")
cat("et recapture des ASV rares (1-3 lectures), a profondeur egale.\n\n")
cat(sprintf("%-24s %10s %10s %10s\n","paire","Bray","Jaccard","recapt."))
for (k in names(res)) {
  d <- res[[k]]
  cat(sprintf("%-24s %10.4f %10.4f %10.3f\n", gsub("\\|"," vs ",k),
      mean(d$bray), mean(d$jaccard), mean(d$recapture, na.rm=TRUE)))
}
cat("\nCorrelation de Spearman des profondeurs brutes :\n")
for (i in 1:2) for (j in (i+1):3)
  cat(sprintf("  %s vs %s : rho = %.4f\n", runs[i], runs[j],
      cor(D[,i], D[,j], method="spearman")))
cat("\nRichesse observee a profondeur egale :\n")
for (r in runs) cat(sprintf("  %s : %.1f ASV/ech.\n", r, mean(rowSums(R[[r]] > 0))))
sink()
cat("\n=== termine ===\n")
RS

printf '%s\tEND\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log
cat results/run_design/run_design_summary.txt
