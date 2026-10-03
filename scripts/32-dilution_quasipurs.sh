#!/bin/bash -l
#SBATCH --job-name=dilution_qp
#SBATCH --account=ondemand@biomics
#SBATCH --qos=cpu-ondemand-long
#SBATCH --partition=cpu-ondemand
#SBATCH --time=04:00:00
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
set -eEuo pipefail
# 32-dilution_quasipurs.sh — test (b) de docs/plan_tests_2026-10-03.md (declare a priori, commit bd6ba3d)
#
# HYPOTHESE (R22). Le signal caudal en UniFrac pondere, present en passe 1 et absent en passe 2,
# disparait parce que les 19 quasi-purs a fond Pt, etiquetes Hy en passe 2, ont une composition de
# type Pt et diluent le contraste Hy-Pt.
#  b2 (test direct) : QPpt (19) contre Pt purs (79) et contre INT (20 intermediaires), par metrique x run
#     x tissu ; D ~ pos + grp (blocs station) et D ~ grp (blocs station).
#  b1 (injection temoin) : passe 1 (158) + 19 Pt et 3 Cn tires dans les MEMES stations et en memes
#     nombres que QPpt / QPcn, reetiquetes Hy ; 20 tirages + reference sans injection (rep 0).
#     Modeles du script 27, a l'identique.
# Variables : TESTS_OUTDIR, NPERM (999), NREP (20), SMOKE=1 (WUF, durance1, caudale, 2 tirages, 99 perm).
# Sorties : <OUT>/dilution/{b2_direct.tsv, b1_injection.tsv, b1_tirages.tsv, dilution.txt}
cd "$HOME/work/projects/microbiome-hybrid"
OUT="${TESTS_OUTDIR:-results/tests_20261003}/dilution"; mkdir -p "$OUT" logs
GIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo NA)
printf '%s\tSTART\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log
export OUT
$HOME/bin/envs/dada2/bin/Rscript - <<'RS' 2>&1 | tee "$OUT"/dilution.txt
suppressMessages({library(vegan); library(permute); library(parallel)})
SMOKE <- Sys.getenv("SMOKE", "") == "1"
NPERM <- if (SMOKE) 99L else as.integer(Sys.getenv("NPERM", "999"))
NREP  <- if (SMOKE) 2L else as.integer(Sys.getenv("NREP", "20"))
NCPU  <- as.integer(Sys.getenv("SLURM_CPUS_PER_TASK", "8"))
OUT   <- Sys.getenv("OUT")
MD <- read.csv("metadata/analysis_metadata.csv", stringsAsFactors = FALSE)
need <- c("dada2_id","individual_id","run_label","tissue","station","categorie","col_rank_station","type_genome","index_mediane_andre","inclus_passe1")
stopifnot(all(need %in% names(MD)))
rownames(MD) <- MD$dada2_id
MD$grp <- with(MD, ifelse(type_genome == "quasi-pur" & index_mediane_andre < 0.5, "QPpt",
                  ifelse(type_genome == "quasi-pur" & index_mediane_andre >= 0.5, "QPcn",
                  ifelse(type_genome == "intermediaire", "INT",
                  ifelse(type_genome == "pur" & categorie == "Pt", "Ptpur",
                  ifelse(type_genome == "pur" & categorie == "Cn", "Cnpur", NA))))))
U <- MD[!duplicated(MD$individual_id), ]
print(table(U$grp, useNA = "ifany"))
stopifnot(sum(U$grp == "QPpt", na.rm = TRUE) == 19, sum(U$grp == "QPcn", na.rm = TRUE) == 3,
          sum(U$grp == "INT", na.rm = TRUE) == 20, sum(U$grp == "Ptpur", na.rm = TRUE) == 79, !any(is.na(U$grp)))
files <- Sys.glob("results/rarefaction/beta_mean_*_N400.rds"); stopifnot(length(files) == 4)
runs <- c("durance1","durance2","durance3"); tissus <- c("caudale","branchie","midgut","hindgut")
if (SMOKE) { files <- files[grepl("unifrac_weighted", files)]; runs <- "durance1"; tissus <- "caudale" }
safe <- function(e) tryCatch(e, error = function(x) NULL)
gv <- function(a, term) { if (is.null(a)) return(c(NA, NA)); d <- as.data.frame(a); i <- match(term, rownames(d))
  c(d$R2[i], d[[grep("^Pr", names(d))[1]]][i]) }

# ------------------------------------------------------------------ b2 : test direct
T2 <- file.path(OUT, "b2_direct.tsv")
cat("metrique\tcomparaison\trun\ttissu\tn\tn_stations_deux_groupes\tmodele\tR2\tp\n", file = T2)
for (f in files) {
  met <- sub("^beta_mean_(.*)_N[0-9]+\\.rds$", "\\1", basename(f)); M <- as.matrix(readRDS(f)); lab <- rownames(M)
  for (cmp in list(c("QPpt","Ptpur"), c("QPpt","INT"))) for (run in runs) for (tis in tissus) {
    ids <- lab[lab %in% MD$dada2_id]; ids <- ids[MD[ids,"run_label"] == run & MD[ids,"tissue"] == tis & MD[ids,"grp"] %in% cmp]
    md <- MD[ids, ]; md$grp <- factor(md$grp, levels = cmp); md$st <- factor(md$station); md$pos <- as.numeric(md$col_rank_station)
    nboth <- sum(tapply(md$grp, md$st, function(x) length(unique(x))) == 2)
    lab_cmp <- paste(cmp, collapse = "_vs_"); n <- length(ids)
    if (n < 10 || nlevels(droplevels(md$grp)) < 2 || nboth == 0) {
      for (mo in c("pos_grp_station_bloquee","sanspos_grp_station_bloquee"))
        cat(sprintf("%s\t%s\t%s\t%s\t%d\t%d\t%s\tNA\tNA\n", met, lab_cmp, run, tis, n, nboth, mo), file = T2, append = TRUE)
      next }
    D <- as.dist(M[ids, ids]); h <- how(nperm = NPERM, blocks = md$st)
    set.seed(20261003)
    a1 <- gv(safe(adonis2(D ~ pos + grp, data = md, permutations = h, by = "terms", parallel = NCPU)), "grp")
    a2 <- gv(safe(adonis2(D ~ grp, data = md, permutations = h, by = "terms", parallel = NCPU)), "grp")
    cat(sprintf("%s\t%s\t%s\t%s\t%d\t%d\t%s\t%.6g\t%.6g\n", met, lab_cmp, run, tis, n, nboth, "pos_grp_station_bloquee", a1[1], a1[2]), file = T2, append = TRUE)
    cat(sprintf("%s\t%s\t%s\t%s\t%d\t%d\t%s\t%.6g\t%.6g\n", met, lab_cmp, run, tis, n, nboth, "sanspos_grp_station_bloquee", a2[1], a2[2]), file = T2, append = TRUE)
  }
}
cat("b2 termine\n")

# ------------------------------------------------------------------ b1 : injection temoin
P1 <- MD[as.character(MD$inclus_passe1) %in% c("True","TRUE"), ]
U1 <- P1[!duplicated(P1$individual_id), ]
stopifnot(nrow(U1) == 158, sum(U1$categorie == "Hy") == 20)
need_pt <- table(U$station[U$grp == "QPpt"]); need_cn <- table(U$station[U$grp == "QPcn"])
draw <- function(pool_cat, need) {   # tire dans les memes stations, complete ailleurs si besoin
  chosen <- character(0); short <- 0L
  for (s in names(need)) { cand <- U1$individual_id[U1$categorie == pool_cat & U1$station == s]
    k <- min(need[[s]], length(cand)); short <- short + (need[[s]] - k)
    if (k > 0) chosen <- c(chosen, if (length(cand) == 1) cand else sample(cand, k)) }
  if (short > 0) { rest <- setdiff(U1$individual_id[U1$categorie == pool_cat], chosen); chosen <- c(chosen, sample(rest, short)) }
  list(ids = chosen, short = short) }
set.seed(20261004)
tir <- lapply(seq_len(NREP), function(i) { a <- draw("Pt", need_pt); b <- draw("Cn", need_cn); list(ids = c(a$ids, b$ids), short_pt = a$short, short_cn = b$short) })
write.table(data.frame(rep = seq_len(NREP), complement_hors_station_Pt = sapply(tir, `[[`, "short_pt"),
                       complement_hors_station_Cn = sapply(tir, `[[`, "short_cn"),
                       individus = sapply(tir, function(z) paste(z$ids, collapse = ";"))),
            file.path(OUT, "b1_tirages.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
T1 <- file.path(OUT, "b1_injection.tsv")
cat("metrique\trep\trun\ttissu\tn\tn_Hy\tmodele\tR2\tp\n", file = T1)
for (f in files) {
  met <- sub("^beta_mean_(.*)_N[0-9]+\\.rds$", "\\1", basename(f)); M <- as.matrix(readRDS(f)); lab <- rownames(M)
  res <- mclapply(0:NREP, function(i) {
    set.seed(1000L * i + nchar(met))
    md1 <- P1; if (i > 0) md1$categorie[md1$individual_id %in% tir[[i]]$ids] <- "Hy"
    out <- character(0)
    for (run in runs) for (tis in tissus) {
      base <- lab[lab %in% md1$dada2_id]; md0 <- md1[base, ]
      ids <- base[md0$run_label == run & md0$tissue == tis]; if (length(ids) < 30) next
      md <- md1[ids, ]; md$cat <- factor(md$categorie); md$st <- factor(md$station); md$pos <- as.numeric(md$col_rank_station)
      if (nlevels(md$cat) < 2 || nlevels(md$st) < 2) next
      D <- as.dist(M[ids, ids]); n <- length(ids); h <- how(nperm = NPERM, blocks = md$st)
      L <- list(ordre_MIN_pos_st_cat          = safe(adonis2(D ~ pos + st + cat, data = md, permutations = NPERM, by = "terms")),
                cat_apres_pos_station_bloquee = safe(adonis2(D ~ pos + cat, data = md, permutations = h, by = "terms")),
                sanspos_MIN_st_cat            = safe(adonis2(D ~ st + cat, data = md, permutations = NPERM, by = "terms")),
                sanspos_cat_station_bloquee   = safe(adonis2(D ~ cat, data = md, permutations = h, by = "terms")))
      for (mo in names(L)) { v <- gv(L[[mo]], "cat")
        out <- c(out, sprintf("%s\t%d\t%s\t%s\t%d\t%d\t%s\t%s\t%s", met, i, run, tis, n, sum(md$cat == "Hy"), mo, format(v[1], digits = 5), format(v[2], digits = 5))) }
    }
    out }, mc.cores = NCPU)
  bad <- vapply(res, function(z) inherits(z, "try-error") || is.null(z), logical(1))
  if (any(bad)) stop(sprintf("%d tirage(s) en erreur pour %s", sum(bad), met))
  cat(unlist(res), sep = "\n", file = T1, append = TRUE); cat("\n", file = T1, append = TRUE)
  cat(sprintf("b1 %s : %d lignes\n", met, length(unlist(res))))
}
cat("TERMINE\n")
RS
printf '%s\tEND\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log
