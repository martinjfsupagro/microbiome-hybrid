
# Conversion des matrices UniFrac au format et a la convention de nommage du projet
# (beta_mean_<metrique>_N<N>.rds, objet dist), pour que le script 20 les balaie sans
# modification. Produit par 21-unifrac_faith.sh (N=400, deux chaines de 200).
for (m in c("unweighted","weighted")) {
  f <- sprintf("results/phylo_diversity/unifrac_%s_mean.tsv.gz", m)
  x <- as.matrix(read.table(gzfile(f), header=TRUE, row.names=1, sep="\t", check.names=FALSE))
  stopifnot(nrow(x) == ncol(x), all(rownames(x) == colnames(x)))
  stopifnot(all(abs(diag(x)) < 1e-9))
  # symetrie : la moyenne de matrices symetriques l'est, on le verifie
  asym <- max(abs(x - t(x)))
  cat(sprintf("%-12s %d x %d | asymetrie max = %.2e | min=%.4f max=%.4f\n",
              m, nrow(x), ncol(x), asym, min(x[upper.tri(x)]), max(x[upper.tri(x)])))
  stopifnot(asym < 1e-6)
  D <- as.dist(x)
  out <- sprintf("results/rarefaction/beta_mean_unifrac_%s_N400.rds", m)
  saveRDS(D, out)
  cat("  ->", out, "\n")
}
# controle : les jeux d'echantillons coincident avec les matrices taxonomiques
a <- attr(readRDS("results/rarefaction/beta_mean_bray_N400.rds"), "Labels")
b <- attr(readRDS("results/rarefaction/beta_mean_unifrac_unweighted_N400.rds"), "Labels")
cat("\nechantillons : bray", length(a), "| unifrac", length(b),
    "| identiques et dans le meme ordre :", identical(a, b), "\n")
stopifnot(identical(a, b))
