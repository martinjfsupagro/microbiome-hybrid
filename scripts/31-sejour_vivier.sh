#!/bin/bash -l
#SBATCH --job-name=sejour_vivier
#SBATCH --account=ondemand@biomics
#SBATCH --qos=cpu-ondemand-long
#SBATCH --partition=cpu-ondemand
#SBATCH --time=04:00:00
#SBATCH --cpus-per-task=16
#SBATCH --mem=32G
set -eEuo pipefail
# 31-sejour_vivier.sh — test (e) de docs/plan_tests_2026-10-03.md (declare a priori, commit bd6ba3d)
#
# QUESTION. L'effet de position (R14) est-il un artefact de plaque ou un effet de la duree de
# sejour en vivier avant dissection ? Andre (2026-10-03) : poissons gardes vivants jusqu'a la
# dissection, 4-6 min par poisson, numeros = ordre de traitement. A 5 stations sur 9 colonne et
# ordre sont inseparables (rho 0,87-0,95) ; on teste aux 4 stations ou ils se decouplent.
#
# VARIABLES. camp = station x annee ; rang = rang du numero d'individu dans la campagne (1 = premier
# traite, ~5 min par rang) ; pos = col_rank_station (comme scripts 20, 27).
# MODELES par metrique x run x tissu :
#   M1 (4 stations, n >= 20) : adonis2(D ~ camp + cat + pos + rang, by="margin"), blocs = camp
#   M2 (Chavannes seule, 19 Pt, n >= 10) : adonis2(D ~ camp + pos + rang, by="margin"), blocs = camp
# La regle de lecture est appliquee ensuite par scripts/36-lecture_tests.py.
# Variables : TESTS_OUTDIR (defaut results/tests_20261003), NPERM (999), SMOKE=1 (une strate, 99 perm).
# Sorties : <OUT>/sejour_vivier/{sejour_tests.tsv, spearman_rang_pos.tsv, sejour.txt}
cd "$HOME/work/projects/microbiome-hybrid"
OUT="${TESTS_OUTDIR:-results/tests_20261003}/sejour_vivier"; mkdir -p "$OUT" logs
GIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo NA)
printf '%s\tSTART\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log
export OUT
$HOME/bin/envs/dada2/bin/Rscript - <<'RS' 2>&1 | tee "$OUT"/sejour.txt
suppressMessages({library(vegan); library(permute)})
set.seed(20261003)
SMOKE <- Sys.getenv("SMOKE", "") == "1"
NPERM <- if (SMOKE) 99L else as.integer(Sys.getenv("NPERM", "999"))
NCPU  <- as.integer(Sys.getenv("SLURM_CPUS_PER_TASK", "8"))
OUT   <- Sys.getenv("OUT"); TSV <- file.path(OUT, "sejour_tests.tsv")
STATIONS <- c("Chavannes-sur-Suran", "Pont-d'Ain", "Avignon", "Confluence Buech-Meouge")
MD <- read.csv("metadata/analysis_metadata.csv", stringsAsFactors = FALSE)
need <- c("dada2_id","individual_id","individual","annee","run_label","tissue","station","categorie","col_rank_station")
stopifnot(all(need %in% names(MD)))
MD <- MD[MD$station %in% STATIONS, ]
stopifnot(setequal(unique(MD$station), STATIONS))
cat(sprintf("individus dans les 4 stations : %d\n", length(unique(MD$individual_id))))
stopifnot(length(unique(MD$individual_id)) == 92)
MD$camp <- paste(MD$station, MD$annee, sep = "_")
ind <- unique(MD[, c("individual_id", "camp", "individual")])
stopifnot(!any(duplicated(ind$individual_id)))
ind$rang <- ave(as.integer(ind$individual), ind$camp, FUN = function(x) rank(x, ties.method = "first"))
MD$rang <- ind$rang[match(MD$individual_id, ind$individual_id)]
MD$pos  <- as.numeric(MD$col_rank_station); stopifnot(!any(is.na(MD$pos)), !any(is.na(MD$rang)))
rownames(MD) <- MD$dada2_id
print(table(ind$camp))

# controle prealable : rang x pos par campagne et tissu (un echantillon par individu et tissu, durance1)
sp <- do.call(rbind, lapply(split(MD[MD$run_label == "durance1", ], list(MD$camp[MD$run_label == "durance1"], MD$tissue[MD$run_label == "durance1"]), drop = TRUE),
  function(s) data.frame(camp = s$camp[1], tissu = s$tissue[1], n = nrow(s),
                         rho = if (nrow(s) >= 4 && sd(s$pos) > 0) suppressWarnings(cor(s$rang, s$pos, method = "spearman")) else NA)))
write.table(sp, file.path(OUT, "spearman_rang_pos.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
cat("Spearman rang x pos (durance1) :\n"); print(sp, row.names = FALSE)

cat("metrique\tmodele\trun\ttissu\tn\tn_camp\tterme\tdf\tR2\tF\tp\n", file = TSV)
emit <- function(a, met, mo, run, tis, n, ncamp) {
  if (is.null(a)) { cat(sprintf("%s\t%s\t%s\t%s\t%d\t%d\tNA\tNA\tNA\tNA\tNA\n", met, mo, run, tis, n, ncamp), file = TSV, append = TRUE); return(invisible()) }
  d <- as.data.frame(a); pc <- grep("^Pr", names(d))[1]; fc <- grep("^F", names(d))[1]
  for (i in seq_len(nrow(d))) { tn <- rownames(d)[i]; if (tn %in% c("Residual","Total")) next
    cat(sprintf("%s\t%s\t%s\t%s\t%d\t%d\t%s\t%s\t%.6g\t%.6g\t%.6g\n", met, mo, run, tis, n, ncamp, tn, d$Df[i], d$R2[i], d[[fc]][i], d[[pc]][i]), file = TSV, append = TRUE) }
}
safe <- function(e) tryCatch(e, error = function(x) { cat("   ERREUR:", conditionMessage(x), "\n"); NULL })
files <- Sys.glob("results/rarefaction/beta_mean_*_N400.rds"); stopifnot(length(files) == 4)
runs <- c("durance1","durance2","durance3"); tissus <- c("caudale","branchie","midgut","hindgut")
if (SMOKE) { files <- files[grepl("unifrac_weighted", files)]; runs <- "durance1"; tissus <- "caudale" }
for (f in files) {
  met <- sub("^beta_mean_(.*)_N[0-9]+\\.rds$", "\\1", basename(f))
  M <- as.matrix(readRDS(f)); lab <- rownames(M)
  for (run in runs) for (tis in tissus) {
    ids <- lab[lab %in% MD$dada2_id]; ids <- ids[MD[ids, "run_label"] == run & MD[ids, "tissue"] == tis]
    md <- MD[ids, ]; md$camp <- factor(md$camp); md$cat <- factor(md$categorie)
    n <- length(ids); cat(sprintf("%s %s %s : n=%d, %d campagnes, %d categories\n", met, run, tis, n, nlevels(md$camp), nlevels(md$cat)))
    if (n >= 20) {
      D <- as.dist(M[ids, ids]); h <- how(nperm = NPERM, blocks = md$camp)
      fo <- if (nlevels(md$cat) >= 2) D ~ camp + cat + pos + rang else D ~ camp + pos + rang
      emit(safe(adonis2(fo, data = md, permutations = h, by = "margin", parallel = NCPU)), met, "M1_4stations", run, tis, n, nlevels(md$camp))
    } else emit(NULL, met, "M1_4stations", run, tis, n, nlevels(md$camp))
    ic <- ids[md$station == "Chavannes-sur-Suran"]
    if (length(ic) >= 10) {
      mc <- MD[ic, ]; mc$camp <- factor(mc$camp); Dc <- as.dist(M[ic, ic]); hc <- how(nperm = NPERM, blocks = mc$camp)
      emit(safe(adonis2(Dc ~ camp + pos + rang, data = mc, permutations = hc, by = "margin", parallel = NCPU)), met, "M2_Chavannes", run, tis, length(ic), nlevels(mc$camp))
    } else emit(NULL, met, "M2_Chavannes", run, tis, length(ic), length(unique(MD[ic, "camp"])))
  }
}
cat("TERMINE\n")
RS
printf '%s\tEND\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log
