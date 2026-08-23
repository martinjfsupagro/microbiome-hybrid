#!/bin/bash -l
#SBATCH --job-name=var_partition
#SBATCH --account=ondemand@biomics
#SBATCH --qos=cpu-ondemand-long
#SBATCH --partition=cpu-ondemand
#SBATCH --time=04:00:00
#SBATCH --cpus-per-task=16
#SBATCH --mem=96G
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
set -eEuo pipefail

# 14-variance_partition.sh — part de variance biologique vs technique
#
# OBJET : quantifier ce que le lot technique explique, face a la biologie, sur le
# jeu REELLEMENT analyse (et non sur les seuls echantillons complets dans les 3 runs,
# qui sont les plus profonds donc les plus reproductibles — ce sous-ensemble
# sous-estimerait la composante technique).
#
# STRUCTURE DU DESIGN (etablie par 13-run_design.sh, cf docs/decision_run_design.md) :
#   librairie A (PCR 1) -> durance1
#   librairie B (PCR 2) -> durance2, durance3
# donc sequencage NICHE dans preparation de librairie : library/run.
#
# PRECAUTION D'INTERPRETATION : les termes techniques sont places EN PREMIER dans le
# modele sequentiel. En PERMANOVA sequentielle chaque terme prend ce qui reste apres
# les precedents ; placer le technique d'abord lui attribue le MAXIMUM possible.
# C'est le choix conservateur pour une demonstration "le technique est petit".
# Le modele marginal (by="margin") est aussi rapporte : contribution unique de chaque
# terme, une fois tous les autres ajustes.
#
# NB : rarefaction unique a 3000 (graine fixee). Le MODE d'application definitif
# (tirage unique vs rarefactions repetees) n'est PAS arrete — cf decision_rarefaction.md.
# Ce calcul est un diagnostic technique, pas l'analyse ecologique finale.
#
# Sorties : results/var_partition/{variance_partition.txt, pcoa_coords.tsv,
#           technical_vs_biological_distances.tsv}

cd "$HOME/work/projects/microbiome-hybrid"
OUT=results/var_partition
mkdir -p "$OUT" logs

RSCRIPT=$HOME/bin/envs/dada2/bin/Rscript
GIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo NA)
printf '%s\tSTART\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log

"$RSCRIPT" - <<'RS'
suppressMessages(library(vegan))
set.seed(20260823)
DEPTH <- 3000
NPERM <- 499
NCPU  <- as.integer(Sys.getenv("SLURM_CPUS_PER_TASK", "8"))

cat("=== lecture ===\n")
tabf <- "results/decontam/asv_table_clean.tsv"
hdr  <- strsplit(readLines(tabf, n = 1L), "\t")[[1]]
nc   <- length(hdr)
dat  <- scan(tabf, what = c(list(""), rep(list(0L), nc - 1L)),
             sep = "\t", skip = 1L, quiet = TRUE)
m <- matrix(0L, nrow = length(dat[[1]]), ncol = nc - 1L,
            dimnames = list(dat[[1]], hdr[-1]))
for (j in 2:nc) m[, j - 1L] <- dat[[j]]
rm(dat); gc(verbose = FALSE)
cat(sprintf("  %d ASV x %d echantillons\n", nrow(m), ncol(m)))

meta <- read.csv("metadata/samples_all.csv", stringsAsFactors = FALSE)
rownames(meta) <- meta$dada2_id
md <- meta[colnames(m), c("site","year","individual","tissue","run_label"), drop = FALSE]
md$library <- ifelse(md$run_label == "durance1", "A", "B")
md$fish    <- paste(md$year, md$site, md$individual, sep = "_")
md$unit    <- paste(md$fish, md$tissue, sep = "_")   # echantillon biologique

# --- rarefaction sur TOUT le jeu analyse (pas seulement les triplets complets) ---
depth <- colSums(m)
keep  <- colnames(m)[depth >= DEPTH]
cat(sprintf("\n=== rarefaction a %d : %d/%d echantillons retenus (%.1f%%) ===\n",
            DEPTH, length(keep), ncol(m), 100*length(keep)/ncol(m)))
X <- t(m[, keep, drop = FALSE])
rm(m); gc(verbose = FALSE)
X <- rrarefy(X, DEPTH)
X <- X[, colSums(X) > 0, drop = FALSE]
md <- md[keep, , drop = FALSE]
cat(sprintf("  matrice rarefiee : %d echantillons x %d ASV\n", nrow(X), ncol(X)))
cat("  repartition par librairie :\n"); print(table(md$library))
cat("  repartition par run :\n");       print(table(md$run_label))
cat("  repartition par tissu :\n");     print(table(md$tissue))

cat("\n=== distances Bray-Curtis ===\n")
D <- vegdist(X, method = "bray")
cat(sprintf("  matrice %d x %d\n", nrow(X), nrow(X)))

# ---------- 1. partition de variance ----------
cat("\n=== PERMANOVA sequentielle — technique EN PREMIER (conservateur) ===\n")
f_seq <- as.formula("D ~ library + run_label + tissue + fish")
a_seq <- adonis2(f_seq, data = md, permutations = NPERM, by = "terms", parallel = NCPU)
print(a_seq)

# ATTENTION : `library` est entierement determine par `run_label` (durance1 EST la
# librairie A). Un test MARGINAL sur `library` serait donc aliase — contribution nulle
# par construction, non interpretable. On ne demande le marginal que sur les termes
# biologiques, ou l'aliasing ne se pose pas (chaque poisson est dans les deux
# librairies : technique et biologie sont croises, pas confondus).
cat("\n=== PERMANOVA marginale sur les termes BIOLOGIQUES seuls ===\n")
cat("(library non testable en marginal : alias parfait avec run_label)\n")
a_mar <- adonis2(D ~ tissue + fish, data = md,
                 permutations = NPERM, by = "margin", parallel = NCPU)
print(a_mar)

# controle d'aliasing explicite : croisement library x fish
cat("\n=== controle : technique et biologie sont-ils croises ? ===\n")
tt <- table(md$library, md$tissue)
cat("library x tissue :\n"); print(tt)
nfish_both <- sum(tapply(md$library, md$fish, function(x) length(unique(x)) == 2))
cat(sprintf("poissons presents dans les DEUX librairies : %d / %d\n",
            nfish_both, length(unique(md$fish))))
cat("-> si ce nombre est eleve, le lot technique n'est pas confondu avec la biologie,\n")
cat("   et un effet aleatoire suffit (pas de correction de batch necessaire).\n")

# ---------- 2. distances techniques vs biologiques ----------
cat("\n=== distances techniques vs biologiques ===\n")
Dm  <- as.matrix(D)
sn  <- rownames(Dm)
u   <- md[sn, "unit"]; lib <- md[sn, "library"]; tis <- md[sn, "tissue"]; fh <- md[sn, "fish"]
iu  <- match(u, unique(u))
n   <- length(sn)
set.seed(7)
S   <- if (n > 1200) sort(sample(n, 1200)) else seq_len(n)   # sous-echantillon pour le O(n^2)
tech_same_lib <- c(); tech_diff_lib <- c(); bio_same_tis <- c(); bio_diff_tis <- c()
for (a in seq_along(S)) for (b in seq_along(S)) if (b > a) {
  i <- S[a]; j <- S[b]; d <- Dm[i, j]
  if (iu[i] == iu[j]) {
    if (lib[i] == lib[j]) tech_same_lib <- c(tech_same_lib, d) else tech_diff_lib <- c(tech_diff_lib, d)
  } else if (fh[i] != fh[j]) {
    if (tis[i] == tis[j]) bio_same_tis <- c(bio_same_tis, d) else bio_diff_tis <- c(bio_diff_tis, d)
  }
}
cmp <- data.frame(
  comparaison = c("TECHNIQUE meme librairie (d2 vs d3)",
                  "TECHNIQUE librairies differentes (d1 vs d2/d3)",
                  "BIOLOGIQUE poissons differents, meme tissu",
                  "BIOLOGIQUE poissons differents, tissus differents"),
  n    = c(length(tech_same_lib), length(tech_diff_lib), length(bio_same_tis), length(bio_diff_tis)),
  moy  = c(mean(tech_same_lib), mean(tech_diff_lib), mean(bio_same_tis), mean(bio_diff_tis)),
  med  = c(median(tech_same_lib), median(tech_diff_lib), median(bio_same_tis), median(bio_diff_tis)),
  sd   = c(sd(tech_same_lib), sd(tech_diff_lib), sd(bio_same_tis), sd(bio_diff_tis)))
print(cmp, row.names = FALSE)
write.table(cmp, file.path("results/var_partition","technical_vs_biological_distances.tsv"),
            sep = "\t", quote = FALSE, row.names = FALSE)

# ---------- 3. PCoA pour la figure ----------
cat("\n=== PCoA ===\n")
pc <- cmdscale(D, k = 3, eig = TRUE)
eig <- pc$eig[pc$eig > 0]
varexp <- 100 * eig[1:3] / sum(eig)
cat(sprintf("  variance expliquee : PCo1 %.1f%%  PCo2 %.1f%%  PCo3 %.1f%%\n", varexp[1], varexp[2], varexp[3]))
co <- data.frame(sample = rownames(pc$points),
                 PCo1 = pc$points[,1], PCo2 = pc$points[,2], PCo3 = pc$points[,3],
                 unit = md[rownames(pc$points), "unit"],
                 fish = md[rownames(pc$points), "fish"],
                 tissue = md[rownames(pc$points), "tissue"],
                 run = md[rownames(pc$points), "run_label"],
                 library = md[rownames(pc$points), "library"],
                 stringsAsFactors = FALSE)
write.table(co, file.path("results/var_partition","pcoa_coords.tsv"),
            sep = "\t", quote = FALSE, row.names = FALSE)
writeLines(sprintf("%.4f", varexp), file.path("results/var_partition","pcoa_varexp.txt"))

# ---------- synthese ----------
sink(file.path("results/var_partition","variance_partition.txt"))
cat("PARTITION DE VARIANCE — BIOLOGIQUE vs TECHNIQUE\n")
cat(sprintf("Table propre rarefiee a %d lectures ; %d echantillons sur %d (%.1f%%).\n",
            DEPTH, nrow(X), length(depth), 100*nrow(X)/length(depth)))
cat(sprintf("Distance Bray-Curtis ; PERMANOVA %d permutations.\n", NPERM))
cat("Design : sequencage niche dans preparation de librairie (A -> durance1 ;\n")
cat("B -> durance2 + durance3).\n\n")
cat("--- PERMANOVA sequentielle, termes techniques en premier (conservateur) ---\n")
print(a_seq)
cat("\n--- PERMANOVA marginale, termes biologiques seuls ---\n")
print(a_mar)
cat("\n--- distances moyennes par type de comparaison ---\n")
print(cmp, row.names = FALSE)
cat(sprintf("\nPCoA : PCo1 %.1f%%  PCo2 %.1f%%  PCo3 %.1f%%\n", varexp[1], varexp[2], varexp[3]))
sink()
cat("\n=== termine ===\n")
RS

printf '%s\tEND\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log
cat results/var_partition/variance_partition.txt
