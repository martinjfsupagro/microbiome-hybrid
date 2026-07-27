#!/bin/bash -l
#SBATCH --job-name=qc_depth
#SBATCH --account=ondemand@biomics
#SBATCH --partition=cpu-ondemand
#SBATCH --time=02:00:00
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
set -eEuo pipefail

# 09-qc_depth.sh — QC profondeur de lecture + courbes de rarefaction
# Sur la table decontaminee de reference (seuil 0.1 : asv_table_analysis.tsv).
# But : distribution des profondeurs (global, par tissu/site/run), choix d'un
# seuil de rarefaction, liste des echantillons perdus a differents seuils.
# Independant de l'arbre et d'Andre.
#
# Sorties results/qc_depth/ :
#   depth_per_sample.tsv, depth_summary.txt,
#   rarefaction_curves.tsv, depth_thresholds.tsv,
#   fig_depth_hist.png, fig_depth_by_tissue.png, fig_rarefaction.png

PROJECT="$HOME/work/projects/microbiome-hybrid"; cd "$PROJECT"
OUT="results/qc_depth"; mkdir -p "$OUT"
export PATH="$HOME/bin/envs/dada2/bin:$PATH"
GIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo nogit)
printf "%s | qc_depth_%s | START | %s | %s | rarefaction table p01\n" \
  "$(date -Iseconds)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log
trap 'printf "%s | qc_depth_%s | FAIL | %s | %s | exit $?\n" "$(date -Iseconds)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log' ERR

Rscript - <<'EOF'
suppressPackageStartupMessages({library(vegan)})

tab  <- read.delim("results/decontam/asv_table_analysis.tsv", row.names=1, check.names=FALSE)
meta <- read.csv("metadata/samples_all.csv", check.names=FALSE)
rownames(meta) <- meta$dada2_id

# table : ASV x echantillons -> samples en lignes
mat <- t(as.matrix(tab))                 # samples x ASV
meta <- meta[rownames(mat), ]
stopifnot(all(rownames(meta)==rownames(mat)))

depth <- rowSums(mat)
rich  <- rowSums(mat > 0)
df <- data.frame(dada2_id=rownames(mat), depth=depth, observed_asv=rich,
                 tissue=meta$tissue, site=meta$site, run=meta$run_label,
                 taxon=meta$taxon_code, check.names=FALSE)
write.table(df, file.path("results/qc_depth","depth_per_sample.tsv"),
            sep="\t", quote=FALSE, row.names=FALSE)

# --- resume + seuils ---
thr <- c(1000,2000,3000,5000,8000,10000,15000,20000)
keep <- sapply(thr, function(t) sum(depth>=t))
tt <- data.frame(seuil=thr, echantillons_retenus=keep,
                 pct=round(100*keep/length(depth),1),
                 echantillons_perdus=length(depth)-keep)
write.table(tt, file.path("results/qc_depth","depth_thresholds.tsv"),
            sep="\t", quote=FALSE, row.names=FALSE)

sink("results/qc_depth/depth_summary.txt")
cat("QC PROFONDEUR — table decontaminee (seuil 0.1)\n")
cat("Echantillons biologiques :", nrow(mat), "\n\n")
cat("Profondeur (lectures/echantillon) :\n")
print(summary(depth))
cat("\nRichesse (ASV observes/echantillon) :\n")
print(summary(rich))
cat("\nProfondeur mediane par tissu :\n")
print(tapply(depth, meta$tissue, median))
cat("\nProfondeur mediane par run :\n")
print(tapply(depth, meta$run_label, median))
cat("\nEchantillons retenus selon le seuil de rarefaction :\n")
print(tt, row.names=FALSE)
cat("\nEchantillons a tres faible profondeur (<1000) :", sum(depth<1000), "\n")
if (sum(depth<1000)>0) print(head(sort(depth[depth<1000]), 20))
sink()

# --- courbes de rarefaction (echantillon d'un sous-ensemble pour lisibilite) ---
set.seed(1)
step <- 500
maxd <- 20000
# rarecurve sur un sous-echantillon aleatoire de 60 pour la figure
idx <- sample(seq_len(nrow(mat)), min(60, nrow(mat)))
png("results/qc_depth/fig_rarefaction.png", width=1500, height=1100, res=150)
rarecurve(mat[idx,], step=step, sample=10000, label=FALSE,
          xlab="Profondeur (lectures)", ylab="ASV observes",
          main="Courbes de rarefaction (60 echantillons, ligne = seuil 10 000)")
abline(v=10000, lty=2, col="red")
dev.off()

# --- histogramme profondeur ---
png("results/qc_depth/fig_depth_hist.png", width=1400, height=900, res=150)
hist(log10(depth+1), breaks=50, col="grey70", border="white",
     xlab="log10(profondeur+1)", main="Distribution des profondeurs")
abline(v=log10(10000), lty=2, col="red")
dev.off()

# --- profondeur par tissu (boxplot) ---
png("results/qc_depth/fig_depth_by_tissue.png", width=1300, height=900, res=150)
boxplot(depth ~ meta$tissue, log="y", col="lightblue",
        ylab="Profondeur (log)", xlab="Tissu", main="Profondeur par tissu")
abline(h=10000, lty=2, col="red")
dev.off()

# --- table rarefaction (moyenne ASV vs profondeur, pour usage hors R) ---
depths_grid <- seq(step, maxd, by=step)
rc <- sapply(depths_grid, function(d){
  ok <- depth>=d
  if(!any(ok)) return(NA)
  mean(rarefy(mat[ok,,drop=FALSE], sample=d))
})
write.table(data.frame(depth=depths_grid, mean_observed_asv=round(rc,1)),
            "results/qc_depth/rarefaction_curves.tsv", sep="\t", quote=FALSE, row.names=FALSE)
cat("termine\n")
EOF

for f in depth_summary.txt depth_per_sample.tsv depth_thresholds.tsv rarefaction_curves.tsv \
         fig_depth_hist.png fig_depth_by_tissue.png fig_rarefaction.png; do
  cp "results/qc_depth/$f" ./ 2>/dev/null || true
done
ls -lh ./*.png ./*.tsv ./*.txt 2>/dev/null

printf "%s | qc_depth_%s | END | %s | %s | rarefaction table p01\n" \
  "$(date -Iseconds)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log
cat results/qc_depth/depth_summary.txt
