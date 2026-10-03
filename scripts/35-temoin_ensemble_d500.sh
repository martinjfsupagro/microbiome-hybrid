#!/bin/bash -l
#SBATCH --job-name=ensemble_d500
#SBATCH --account=ondemand@biomics
#SBATCH --qos=cpu-ondemand-long
#SBATCH --partition=cpu-ondemand
#SBATCH --time=02:00:00
#SBATCH --cpus-per-task=16
#SBATCH --mem=32G
set -eEuo pipefail
# 35-temoin_ensemble_d500.sh — test (a2) de docs/plan_tests_2026-10-03.md (declare a priori, commit bd6ba3d)
#
# QUESTION. En passe 1, le signal caudal en UniFrac pondere est robuste a 3 000 lectures et partiel a
# 500. A 500 lectures davantage d'echantillons passent le seuil : l'ensemble n'est pas le meme. On
# compare a ENSEMBLE CONSTANT : (i) 3 000 ; (ii) 500 restreint aux echantillons presents a 3 000 ;
# (iii) 500 complet. Modeles du script 27 a l'identique, passe 1, UniFrac pondere, 4 tissus
# (critere principal : caudale).
# Variables : TESTS_OUTDIR, NPERM (999), SMOKE=1. Sortie : <OUT>/ensemble_d500/{ensemble.tsv, ensemble.txt}
cd "$HOME/work/projects/microbiome-hybrid"
OUT="${TESTS_OUTDIR:-results/tests_20261003}/ensemble_d500"; mkdir -p "$OUT" logs
GIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo NA)
printf '%s\tSTART\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log
export OUT
$HOME/bin/envs/dada2/bin/Rscript - <<'RS' 2>&1 | tee "$OUT"/ensemble.txt
suppressMessages({library(vegan); library(permute)})
SMOKE <- Sys.getenv("SMOKE", "") == "1"
NPERM <- if (SMOKE) 99L else as.integer(Sys.getenv("NPERM", "999"))
NCPU  <- as.integer(Sys.getenv("SLURM_CPUS_PER_TASK", "8"))
OUT   <- Sys.getenv("OUT"); TSV <- file.path(OUT, "ensemble.tsv")
MD <- read.csv("metadata/analysis_metadata.csv", stringsAsFactors = FALSE)
stopifnot(all(c("dada2_id","individual_id","run_label","tissue","station","categorie","col_rank_station","inclus_passe1") %in% names(MD)))
MD <- MD[as.character(MD$inclus_passe1) %in% c("True","TRUE"), ]; rownames(MD) <- MD$dada2_id
stopifnot(length(unique(MD$individual_id)) == 158)
M3 <- as.matrix(readRDS("results/rarefaction/beta_mean_unifrac_weighted_N400.rds"))
M5 <- as.matrix(readRDS("results/rarefaction_d500/beta_mean_unifrac_weighted_N400.rds"))
cat(sprintf("echantillons : 3000=%d, 500=%d, 3000 inclus dans 500 : %s\n", nrow(M3), nrow(M5), all(rownames(M3) %in% rownames(M5))))
versions <- list(i_3000 = list(M = M3, keep = rownames(M3)),
                 ii_500_ensemble_3000 = list(M = M5, keep = intersect(rownames(M5), rownames(M3))),
                 iii_500_complet = list(M = M5, keep = rownames(M5)))
runs <- c("durance1","durance2","durance3"); tissus <- c("caudale","branchie","midgut","hindgut")
if (SMOKE) { runs <- "durance1"; tissus <- "caudale" }
safe <- function(e) tryCatch(e, error = function(x) NULL)
gv <- function(a) { if (is.null(a)) return(c(NA, NA)); d <- as.data.frame(a); i <- match("cat", rownames(d)); c(d$R2[i], d[[grep("^Pr", names(d))[1]]][i]) }
cat("version\trun\ttissu\tn\tn_Hy\tmodele\tR2\tp\n", file = TSV)
for (vn in names(versions)) { M <- versions[[vn]]$M; lab <- versions[[vn]]$keep
  for (run in runs) for (tis in tissus) {
    ids <- lab[lab %in% MD$dada2_id]; ids <- ids[MD[ids,"run_label"] == run & MD[ids,"tissue"] == tis]; if (length(ids) < 30) next
    md <- MD[ids, ]; md$cat <- factor(md$categorie); md$st <- factor(md$station); md$pos <- as.numeric(md$col_rank_station)
    D <- as.dist(M[ids, ids]); n <- length(ids); h <- how(nperm = NPERM, blocks = md$st)
    set.seed(20261005)
    L <- list(ordre_MIN_pos_st_cat          = safe(adonis2(D ~ pos + st + cat, data = md, permutations = NPERM, by = "terms", parallel = NCPU)),
              cat_apres_pos_station_bloquee = safe(adonis2(D ~ pos + cat, data = md, permutations = h, by = "terms", parallel = NCPU)),
              sanspos_MIN_st_cat            = safe(adonis2(D ~ st + cat, data = md, permutations = NPERM, by = "terms", parallel = NCPU)),
              sanspos_cat_station_bloquee   = safe(adonis2(D ~ cat, data = md, permutations = h, by = "terms", parallel = NCPU)))
    for (mo in names(L)) { v <- gv(L[[mo]])
      cat(sprintf("%s\t%s\t%s\t%d\t%d\t%s\t%s\t%s\n", vn, run, tis, n, sum(md$cat == "Hy"), mo, format(v[1], digits = 5), format(v[2], digits = 5)), file = TSV, append = TRUE) }
    cat(sprintf("%s %s %s n=%d\n", vn, run, tis, n))
  } }
cat("TERMINE\n")
RS
printf '%s\tEND\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log
