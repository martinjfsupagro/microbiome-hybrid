#!/bin/bash -l
#SBATCH --job-name=recat_witness_n
#SBATCH --account=ondemand@biomics
#SBATCH --qos=cpu-ondemand-long
#SBATCH --partition=cpu-ondemand
#SBATCH --time=03:00:00
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
set -eEuo pipefail
# 27-recat_witness_effectif.sh — TEMOIN D'EFFECTIF pour la passe 1 (2026-09-25)
#
# QUESTION. Passer de la passe 2 (n=180) a la passe 1 (n=158) retire 22 poissons ET ce sont
# les 22 quasi-purs : effectif et definition de Hy changent ensemble. Ce temoin les separe.
# On part de la passe 2 (etiquettes de septembre, 42 Hy) et on retire 22 individus TIRES AU
# HASARD parmi les 158 non quasi-purs (NREP tirages). Si un resultat de la passe 1 est
# reproduit par ces retraits aleatoires, il tient a l'effectif ; s'il ne l'est pas, il tient a
# l'IDENTITE des poissons retires, c'est-a-dire a la definition des hybrides.
# Modeles : ceux du script 20, a l'identique (memes strates, meme construction de md) :
#   ordre MIN avec position (pos + st + cat), categorie a station bloquee apres position,
#   et leurs versions sans position (st + cat ; cat a station bloquee).
# Sortie : results/recat/temoin_effectif/witness.tsv (une ligne par tirage x strate x modele).
cd "$HOME/work/projects/microbiome-hybrid"
OUT=results/recat/temoin_effectif; mkdir -p "$OUT" logs
GIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo NA)
printf '%s\tSTART\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log
$HOME/bin/envs/dada2/bin/Rscript - <<'RS' 2>&1 | tee "$OUT"/witness.txt
suppressMessages({library(vegan); library(permute); library(parallel)})
NREP <- as.integer(Sys.getenv("NREP", "20")); NPERM <- 999
NCPU <- as.integer(Sys.getenv("SLURM_CPUS_PER_TASK", "8"))
OUT <- "results/recat/temoin_effectif"; TSV <- file.path(OUT, "witness.tsv")
MD <- read.csv("metadata/analysis_metadata.csv", stringsAsFactors = FALSE)
stopifnot(all(c("categorie","inclus_passe1","individual_id","col_rank_station") %in% names(MD)))
rownames(MD) <- MD$dada2_id
nonqp <- unique(MD$individual_id[as.character(MD$inclus_passe1) %in% c("True","TRUE")])
stopifnot(length(nonqp) == 158, length(unique(MD$individual_id)) == 180)
set.seed(20260926)
drops <- lapply(seq_len(NREP), function(i) sample(nonqp, 22))
cat(sprintf("NREP=%d tirages de 22 individus parmi %d non quasi-purs | NPERM=%d | %d CPU\n",
            NREP, length(nonqp), NPERM, NCPU))
cat("metrique\trep\trun\ttissu\tn\tn_Hy\tmodele\tR2\tp\n", file = TSV)
gv <- function(a) { if (is.null(a)) return(c(NA,NA)); d <- as.data.frame(a); i <- match("cat", rownames(d))
  c(d$R2[i], d[[grep("^Pr", names(d))[1]]][i]) }
safe <- function(e) tryCatch(e, error = function(x) NULL)
for (f in Sys.glob("results/rarefaction/beta_mean_*.rds")) {
  met <- sub("^beta_mean_(.*)_N[0-9]+\\.rds$", "\\1", basename(f))
  M <- as.matrix(readRDS(f)); lab <- rownames(M)
  res <- mclapply(seq_len(NREP), function(i) {
    set.seed(1000L * i + nchar(met))
    keepMD <- MD[!MD$individual_id %in% drops[[i]], ]
    out <- character(0)
    for (run in c("durance1","durance2","durance3")) for (tis in c("caudale","branchie","midgut","hindgut")) {
      base <- lab[lab %in% keepMD$dada2_id]; md0 <- keepMD[base, ]
      ids <- base[md0$run_label == run & md0$tissue == tis]
      if (length(ids) < 30) next
      md <- keepMD[ids, ]; md$cat <- factor(md$categorie); md$st <- factor(md$station)
      md$pos <- as.numeric(md$col_rank_station)
      if (nlevels(md$cat) < 2 || nlevels(md$st) < 2) next
      D <- as.dist(M[ids, ids]); n <- length(ids); h <- how(nperm = NPERM, blocks = md$st)
      L <- list(ordre_MIN_pos_st_cat          = safe(adonis2(D ~ pos + st + cat, data = md, permutations = NPERM, by = "terms")),
                cat_apres_pos_station_bloquee = safe(adonis2(D ~ pos + cat, data = md, permutations = h, by = "terms")),
                sanspos_MIN_st_cat            = safe(adonis2(D ~ st + cat, data = md, permutations = NPERM, by = "terms")),
                sanspos_cat_station_bloquee   = safe(adonis2(D ~ cat, data = md, permutations = h, by = "terms")))
      for (mo in names(L)) { v <- gv(L[[mo]])
        out <- c(out, sprintf("%s\t%d\t%s\t%s\t%d\t%d\t%s\t%s\t%s", met, i, run, tis, n, sum(md$cat == "Hy"), mo,
                              format(v[1], digits = 5), format(v[2], digits = 5))) }
    }
    out
  }, mc.cores = NCPU)
  bad <- vapply(res, function(z) inherits(z, "try-error") || is.null(z), logical(1))
  if (any(bad)) stop(sprintf("%d tirage(s) en erreur pour %s : %s", sum(bad), met,
                             paste(unique(sapply(res[bad], function(z) as.character(z))), collapse = " | ")))
  cat(unlist(res), sep = "\n", file = TSV, append = TRUE); cat("\n", file = TSV, append = TRUE)
  cat(sprintf("%s : %d lignes ecrites\n", met, length(unlist(res))))
}
cat("TERMINE\n")
RS
printf '%s\tEND\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log
