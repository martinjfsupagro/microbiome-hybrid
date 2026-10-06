# 66-controle_campagne.R — contrôle « campagne de pêche » des tests de catégorie (plan
# docs/plan_controle_campagne_2026-10-06.md, règles fixées avant calcul).
# T0 référence (station bloquée, séquence et graine de scripts/20) ; T1 blocs station x campagne ; T2 R² de la
# catégorie après station x campagne ; T3 effet de campagne chez les parentaux, stations pêchées deux fois.
# Rscript de ~/bin/envs/dada2 (vegan 2.7.5). Lancer depuis la racine du dépôt.
suppressPackageStartupMessages(library(vegan))
NPERM <- 999; NCPU <- as.integer(Sys.getenv("NCPU", "4"))
OUT <- "results/controle_campagne/"; dir.create(OUT, showWarnings = FALSE, recursive = TRUE)
MD0 <- read.csv("metadata/analysis_metadata.csv", stringsAsFactors = FALSE)
for (cn in c("dada2_id", "individual_id", "run_label", "tissue", "station", "categorie", "annee", "individual", "inclus_passe1"))
  stopifnot(cn %in% names(MD0))
rownames(MD0) <- MD0$dada2_id
# ---- campagne (plan : station x année ; Pertuis scindée par série d'après André, 2026-09-30)
camp <- paste(MD0$station, MD0$annee)
per <- MD0$station == "Pertuis"
num <- suppressWarnings(as.integer(MD0$individual))
stopifnot(!any(is.na(num[per])), all(num[per] %in% c(1011:1014, 2011:2015)))
camp[per] <- ifelse(num[per] <= 1014, "Pertuis 2014-07-07", "Pertuis 2014-08-20")
MD0$blk <- camp
ind <- MD0[!duplicated(MD0$individual_id), ]
B <- as.data.frame.matrix(table(ind$blk, ind$categorie)); B$bloc <- rownames(B)
write.table(B[, c("bloc", "Cn", "Hy", "Pt")], paste0(OUT, "blocs.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
stopifnot(length(unique(MD0$blk)) == 14)
two <- names(which(tapply(ind$blk, ind$station, function(x) length(unique(x))) == 2))
cat("blocs :", length(unique(MD0$blk)), "| stations pêchées deux fois :", paste(two, collapse = " | "), "\n")

REF <- rbind(cbind(passe = "1", read.delim("results/recat/1/var_partition_cat/category_partition.tsv", strip.white = TRUE)),
             cbind(passe = "2", read.delim("results/recat/2/var_partition_cat/category_partition.tsv", strip.white = TRUE)))
REF <- REF[REF$sous_ensemble == "complet" & REF$terme == "cat", ]
gv <- function(a, term, col = "R2") if (is.null(a)) NA else a[term, if (col == "p") "Pr(>F)" else col]
safe <- function(e) tryCatch(e, error = function(err) { cat("   ERREUR:", conditionMessage(err), "\n"); NULL })

files <- Sys.glob("results/rarefaction/beta_mean_*_N400.rds"); stopifnot(length(files) == 4)
R <- list(); P3 <- list()
for (f in files) {
  met <- sub("^beta_mean_(.*)_N[0-9]+\\.rds$", "\\1", basename(f))
  M <- as.matrix(readRDS(f)); lab <- rownames(M)
  cat("\n#####", met, "#####\n")
  for (passe in c("1", "2")) {
    MD <- if (passe == "1") MD0[as.character(MD0$inclus_passe1) %in% c("True", "TRUE"), ] else MD0
    for (run in c("durance1", "durance2", "durance3")) for (tis in c("caudale", "branchie", "midgut", "hindgut")) {
      base <- lab[lab %in% MD$dada2_id]; md0 <- MD[base, ]
      ids <- base[md0$run_label == run & md0$tissue == tis]
      if (length(ids) < 30) next
      md <- MD[ids, ]; md$cat <- factor(md$categorie); md$st <- factor(md$station); md$blk <- factor(md$blk)
      D <- as.dist(M[ids, ids])
      # T0 : séquence de scripts/20 (aN1, aN2, aN3) sous la même graine
      .k <- utf8ToInt(paste(met, run, tis)); set.seed(20260925L + sum(.k * seq_along(.k)))
      aN1 <- safe(adonis2(D ~ st + cat, data = md, permutations = NPERM, by = "terms", parallel = NCPU))
      aN2 <- safe(adonis2(D ~ cat + st, data = md, permutations = NPERM, by = "terms", parallel = NCPU))
      aN3 <- safe(adonis2(D ~ cat, data = md, permutations = how(nperm = NPERM, blocks = md$st), by = "terms", parallel = NCPU))
      # T1 : blocs station x campagne, même graine
      set.seed(20260925L + sum(.k * seq_along(.k)))
      aT1 <- safe(adonis2(D ~ cat, data = md, permutations = how(nperm = NPERM, blocks = md$blk), by = "terms", parallel = NCPU))
      # T2 : R² de la catégorie après station x campagne
      aT2 <- safe(adonis2(D ~ blk + cat, data = md, permutations = NPERM, by = "terms", parallel = NCPU))
      ref <- REF[REF$passe == passe & REF$metrique == met & REF$run == run & REF$tissu == tis, ]
      r0 <- ref[ref$modele == "sanspos_cat_station_bloquee", ]; r1 <- ref[ref$modele == "sanspos_MIN_st_cat", ]
      R[[length(R) + 1]] <- data.frame(metrique = met, passe = passe, run = run, tissu = tis, n = length(ids),
        n_blocs_infos = sum(tapply(md$cat, md$blk, function(x) length(unique(x))) >= 2),
        R2_cat = gv(aN3, "cat"), p_station = gv(aN3, "cat", "p"), p_station_ref = if (nrow(r0)) r0$p else NA,
        R2_station_ref = if (nrow(r0)) r0$R2 else NA, p_campagne = gv(aT1, "cat", "p"),
        R2_cat_apres_station = gv(aN1, "cat"), R2_cat_apres_station_ref = if (nrow(r1)) r1$R2 else NA,
        R2_cat_apres_campagne = gv(aT2, "cat"), R2_blocs_campagne = gv(aT2, "blk"))
      # T3 : parentaux seuls, stations pêchées deux fois, effet de campagne à station x catégorie bloquées (passe 2 seulement)
      if (passe == "2") {
        k3 <- md$categorie %in% c("Cn", "Pt") & md$station %in% two
        m3 <- md[k3, ]; m3$sc <- factor(paste(m3$station, m3$categorie))
        m3$camp <- factor(ifelse(m3$station == "Pertuis", as.character(m3$blk), paste0("y", m3$annee)))
        ok <- tapply(m3$camp, m3$sc, function(x) length(unique(x)) >= 2); keep <- m3$sc %in% names(ok)[ok]
        m3 <- m3[keep, ]
        if (nrow(m3) >= 10) {
          set.seed(20261006L + sum(.k * seq_along(.k)))
          a3 <- safe(adonis2(as.dist(M[rownames(m3), rownames(m3)]) ~ camp, data = m3,
                             permutations = how(nperm = NPERM, blocks = droplevels(m3$sc)), by = "terms", parallel = NCPU))
          P3[[length(P3) + 1]] <- data.frame(metrique = met, run = run, tissu = tis, n = nrow(m3),
            n_cellules = nlevels(droplevels(m3$sc)), R2_campagne = gv(a3, "camp"), p_campagne = gv(a3, "camp", "p"))
        }
      }
      cat(sprintf("%s p%s %s %-8s n=%3d | p station %.3f (ref %.3f) | p campagne %.3f | R2 cat apres st %.4f / apres camp %.4f\n",
                  met, passe, run, tis, length(ids), gv(aN3, "cat", "p"), if (nrow(r0)) r0$p else NA, gv(aT1, "cat", "p"),
                  gv(aN1, "cat"), gv(aT2, "cat")))
    }
  }
}
R <- do.call(rbind, R); P3 <- do.call(rbind, P3)
# précision de la référence : p à 3 décimales, R² à 5 chiffres significatifs (format de scripts/20)
rel <- function(x, r) abs(x - r) <= 1e-4 * abs(r) + 1e-12
R$temoin_ok <- abs(R$p_station - R$p_station_ref) <= 5e-4 + 1e-9 & rel(R$R2_cat, R$R2_station_ref) &
  rel(R$R2_cat_apres_station, R$R2_cat_apres_station_ref)
write.table(R, paste0(OUT, "campagne_tests.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
write.table(P3, paste0(OUT, "campagne_parentaux.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
write.table(R[, c("metrique", "passe", "run", "tissu", "p_station", "p_station_ref", "R2_cat", "R2_station_ref", "temoin_ok")],
            paste0(OUT, "temoin_montage.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
sink(paste0(OUT, "resume.txt"))
cat(sprintf("strates : %d | témoin de montage (T0 = results/recat) : %d / %d\n", nrow(R), sum(R$temoin_ok, na.rm = TRUE), nrow(R)))
agg <- aggregate(cbind(det_station = p_station < 0.05, det_campagne = p_campagne < 0.05) ~ metrique + passe + tissu, data = R, FUN = sum)
cat("\nruns significatifs (sur 3), station bloquée vs station x campagne bloquée :\n"); print(agg, row.names = FALSE)
cat(sprintf("\nR² catégorie après station : médiane %.4f | après station x campagne : médiane %.4f\n",
            median(R$R2_cat_apres_station), median(R$R2_cat_apres_campagne)))
cat("\nT3 parentaux, effet de campagne (stations pêchées deux fois, station x catégorie bloquées) :\n"); print(P3, row.names = FALSE, digits = 3)
sink()
cat(readLines(paste0(OUT, "resume.txt")), sep = "\n")
