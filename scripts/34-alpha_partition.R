#!/usr/bin/env Rscript
# 34-alpha_partition.R — test (d) de docs/plan_tests_2026-10-03.md (declare a priori, commit bd6ba3d).
# Remplace R8, qui n'avait pas de script (diagnostic de conversation, docs/diagnostic_questions_recherche.md).
# Par echantillon (tous runs), quatre indices : lm(log(x) ~ tissue + site_annee + individu + library + run)
#   site_annee = site_code x annee ; library = A (durance1) / B (durance2, durance3) ; run distingue
#   durance2 de durance3 dans B (1 ddl apres library).
# Parts de somme des carres : sequentielles (ordre ci-dessus) et marginales (drop1). Les termes emboites
# (site_annee dans individu, library dans run) n'ont pas de part marginale propre : NA, et l'on rapporte
# en plus la part marginale conjointe du bloc technique (library + run).
# A lancer depuis la racine : $HOME/bin/envs/dada2/bin/Rscript scripts/34-alpha_partition.R
OUT <- file.path(Sys.getenv("TESTS_OUTDIR", "results/tests_20261003"), "alpha_partition"); dir.create(OUT, recursive = TRUE, showWarnings = FALSE)
MD <- read.csv("metadata/analysis_metadata.csv", stringsAsFactors = FALSE)
stopifnot(all(c("dada2_id","individual_id","site_code","annee","tissue","run_label") %in% names(MD)))
AL <- read.delim("results/phylo_diversity/alpha_phylo_mean.tsv", stringsAsFactors = FALSE)
IDX <- c(richness_mean = "richesse observee", shannon_mean = "Shannon", invsimpson_mean = "inverse Simpson", faith_pd_mean = "Faith PD")
stopifnot(all(c("sample", names(IDX)) %in% names(AL)))
d <- merge(AL, MD, by.x = "sample", by.y = "dada2_id")
cat(sprintf("echantillons joints : %d sur %d\n", nrow(d), nrow(AL)))
d$site_annee <- factor(paste(d$site_code, d$annee, sep = "_")); d$individu <- factor(d$individual_id)
d$library <- factor(ifelse(d$run_label == "durance1", "A", "B")); d$run <- factor(d$run_label); d$tissue <- factor(d$tissue)
TERMS <- c("tissue", "site_annee", "individu", "library", "run")
rows <- list()
for (col in names(IDX)) {
  s <- d[d[[col]] > 0, ]; s$y <- log(s[[col]])
  fit <- lm(y ~ tissue + site_annee + individu + library + run, data = s)
  a <- anova(fit); sst <- sum(a[["Sum Sq"]])
  dr <- drop1(fit)
  rss_full <- deviance(fit)
  tech <- deviance(lm(y ~ tissue + site_annee + individu, data = s)) - rss_full
  for (tn in TERMS) {
    seqss <- if (tn %in% rownames(a)) a[tn, "Sum Sq"] else NA
    mss <- if (tn %in% rownames(dr) && !is.na(dr[tn, "Df"]) && dr[tn, "Df"] > 0) dr[tn, "Sum of Sq"] else NA
    rows[[length(rows) + 1]] <- data.frame(indice = IDX[[col]], n = nrow(s), terme = tn,
      ddl_sequentiel = if (tn %in% rownames(a)) a[tn, "Df"] else NA,
      part_sequentielle = seqss / sst, part_marginale = mss / sst)
  }
  rows[[length(rows) + 1]] <- data.frame(indice = IDX[[col]], n = nrow(s), terme = "technique_library_plus_run",
    ddl_sequentiel = NA, part_sequentielle = NA, part_marginale = tech / sst)
  rows[[length(rows) + 1]] <- data.frame(indice = IDX[[col]], n = nrow(s), terme = "residuel",
    ddl_sequentiel = a["Residuals", "Df"], part_sequentielle = a["Residuals", "Sum Sq"] / sst, part_marginale = NA)
}
res <- do.call(rbind, rows)
write.table(res, file.path(OUT, "alpha_partition.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
print(res, row.names = FALSE, digits = 4)
cat("TERMINE\n")
