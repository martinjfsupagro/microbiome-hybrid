# 65-ordination_categories.R — ordinations pour une figure supplémentaire « points communs et différences »
# (proposition d'André, 2026-10-06 ; JF : « les deux versions de b, pour choisir sur pièces avec André »).
#
# Règles (fixées avant calcul) :
#  - distance : Jaccard moyen sur 400 raréfactions à 3 000 lectures (BETA-JAC, results/rarefaction/
#    beta_mean_jaccard_N400.rds), la métrique principale des tests ; mêmes échantillons et même jointure que
#    scripts/20 (rownames = dada2_id de metadata/analysis_metadata.csv) ;
#  - passe 2 : catégories Cn / Hy (42) / Pt (colonne categorie) ; run principal durance1 ;
#  - a  : PCoA (wcmdscale) de tous les échantillons du run, 4 tissus ;
#  - b1 : PCoA par tissu, restreinte aux stations portant les trois catégories parmi les 180 individus (3 attendues) ;
#  - b2 : par tissu, 9 stations, db-RDA capscale(D ~ Condition(station)) : axes NON contraints (MDS1, MDS2) après
#         retrait de la station — la catégorie n'intervient pas dans la construction des axes ;
#         témoin : part d'inertie contrainte par la catégorie dans capscale(D ~ categorie + Condition(station)),
#         à comparer au R² de la catégorie à station bloquée des PERMANOVA (results/recat/2/...) ;
#  - pourcentages d'axes : valeur propre / somme des valeurs propres positives (Jaccard non euclidien : la part
#    des valeurs propres négatives est écrite à côté) ;
#  - témoin de run : mêmes ordinations sur durance2 et durance3, concordance avec durance1 par Procruste (protest,
#    999 permutations) sur les échantillons communs, appariés par individu x tissu.
# Sorties : results/ordination/{coords.tsv, axes.tsv, procrustes.tsv, contrainte_categorie.tsv, resume.txt}
# Rscript de ~/bin/envs/dada2 (vegan 2.7.5). Lancer depuis la racine du dépôt.
suppressPackageStartupMessages(library(vegan))
set.seed(20261006L)
OUT <- "results/ordination/"; dir.create(OUT, showWarnings = FALSE, recursive = TRUE)
MD <- read.csv("metadata/analysis_metadata.csv", stringsAsFactors = FALSE)
for (cn in c("dada2_id", "individual_id", "run_label", "tissue", "station", "categorie")) stopifnot(cn %in% names(MD))
rownames(MD) <- MD$dada2_id
M <- as.matrix(readRDS("results/rarefaction/beta_mean_jaccard_N400.rds"))
lab <- rownames(M); stopifnot(identical(lab, colnames(M)))
base <- lab[lab %in% MD$dada2_id]
cat(sprintf("matrice %d x %d ; %d dans les métadonnées\n", nrow(M), ncol(M), length(base)))
ind <- MD[!duplicated(MD$individual_id), ]
stopifnot(nrow(ind) == 180, all(table(ind$categorie)[c("Cn", "Hy", "Pt")] == c(59, 42, 79)))
TRI <- sort(names(which(tapply(ind$categorie, ind$station, function(x) all(c("Cn", "Hy", "Pt") %in% x)))))
stopifnot(length(TRI) == 3); cat("stations à trois catégories :", paste(TRI, collapse = " | "), "\n")
TIS <- c("caudale", "branchie", "hindgut", "midgut")

pcoa <- function(ids) {
  o <- wcmdscale(as.dist(M[ids, ids]), k = 2, eig = TRUE)
  ev <- o$eig; pos <- sum(ev[ev > 0])
  list(sc = o$points[, 1:2], pct = 100 * ev[1:2] / pos, neg = 100 * sum(abs(ev[ev < 0])) / sum(abs(ev)))
}
partial <- function(ids) {
  md <- MD[ids, ]; md$st <- factor(md$station)
  o <- capscale(as.dist(M[ids, ids]) ~ Condition(st), data = md)
  ev <- o$CA$eig; sc <- scores(o, display = "sites", choices = 1:2, scaling = 1)
  list(sc = sc, pct = 100 * ev[1:2] / sum(ev[ev > 0]), neg = NA_real_)
}
ids_of <- function(run, tis = NULL, st = NULL) {
  m <- MD[base, ]; k <- m$run_label == run
  if (!is.null(tis)) k <- k & m$tissue == tis
  if (!is.null(st)) k <- k & m$station %in% st
  base[k]
}
key <- function(ids) sub("__.*$", "", ids)   # appariement entre runs : nom d'échantillon sans run (les « -bis » restent distincts, comme dans scripts/20)
sets <- list(list(panel = "a", tissu = "tous", f = pcoa, st = NULL))
for (t in TIS) sets[[length(sets) + 1]] <- list(panel = "b1", tissu = t, f = pcoa, st = TRI)
for (t in TIS) sets[[length(sets) + 1]] <- list(panel = "b2", tissu = t, f = partial, st = NULL)

CO <- list(); AX <- list(); PR <- list()
for (s in sets) {
  tis <- if (s$tissu == "tous") NULL else s$tissu
  res <- list()
  for (run in c("durance1", "durance2", "durance3")) {
    ids <- ids_of(run, tis, s$st)
    stopifnot(!anyDuplicated(key(ids)))
    res[[run]] <- c(s$f(ids), list(ids = ids))
    AX[[length(AX) + 1]] <- data.frame(panel = s$panel, tissu = s$tissu, run = run, n = length(ids),
                                       pct1 = res[[run]]$pct[1], pct2 = res[[run]]$pct[2], pct_neg = res[[run]]$neg)
  }
  r1 <- res$durance1
  CO[[length(CO) + 1]] <- data.frame(panel = s$panel, tissu_panneau = s$tissu, dada2_id = r1$ids,
                                     individual_id = MD[r1$ids, "individual_id"], tissue = MD[r1$ids, "tissue"],
                                     station = MD[r1$ids, "station"], categorie = MD[r1$ids, "categorie"],
                                     ax1 = r1$sc[, 1], ax2 = r1$sc[, 2], row.names = NULL)
  for (run in c("durance2", "durance3")) {
    k1 <- key(r1$ids); k2 <- key(res[[run]]$ids); com <- intersect(k1, k2)
    p <- protest(r1$sc[match(com, k1), ], res[[run]]$sc[match(com, k2), ], permutations = 999)
    PR[[length(PR) + 1]] <- data.frame(panel = s$panel, tissu = s$tissu, run = run, n_communs = length(com),
                                       r_procruste = p$t0, p = p$signif)
  }
}
CO <- do.call(rbind, CO); AX <- do.call(rbind, AX); PR <- do.call(rbind, PR)

# témoin b2 : part d'inertie contrainte par la catégorie, station en condition (durance1)
CC <- list()
for (t in TIS) {
  ids <- ids_of("durance1", t); md <- MD[ids, ]; md$st <- factor(md$station); md$cat <- factor(md$categorie)
  o <- capscale(as.dist(M[ids, ids]) ~ cat + Condition(st), data = md)
  CC[[length(CC) + 1]] <- data.frame(tissu = t, n = length(ids), inertie_totale = o$tot.chi,
                                     part_station = o$pCCA$tot.chi / o$tot.chi, part_categorie = o$CCA$tot.chi / o$tot.chi)
}
CC <- do.call(rbind, CC)
write.table(CO, paste0(OUT, "coords.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
write.table(AX, paste0(OUT, "axes.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
write.table(PR, paste0(OUT, "procrustes.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
write.table(CC, paste0(OUT, "contrainte_categorie.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
sink(paste0(OUT, "resume.txt"))
cat("stations à trois catégories :", paste(TRI, collapse = " | "), "\n\n")
print(AX[AX$run == "durance1", ], row.names = FALSE, digits = 3)
cat("\nProcruste durance1 vs durance2/3 :\n"); print(PR, row.names = FALSE, digits = 3)
cat("\nPart d'inertie (capscale, durance1) :\n"); print(CC, row.names = FALSE, digits = 3)
sink()
cat(readLines(paste0(OUT, "resume.txt")), sep = "\n")
