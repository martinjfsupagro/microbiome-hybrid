#!/bin/bash -l
#SBATCH --job-name=decontam
#SBATCH --account=ondemand@biomics
#SBATCH --partition=cpu-ondemand
#SBATCH --time=00:30:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
set -eEuo pipefail

# 07-decontam.sh — Decontamination des ASV (decontam, methode prevalence)
# Question resolue via manuscrit d'origine :
#   - temoins negatifs EXTRACTION : Blanc-* (4 tissus x 3 runs = 12)
#   - temoins negatifs PCR         : T-1..T-8 (8 x 3 runs = 24)
#   -> 36 negatifs combines pour decontam::isContaminant(method="prevalence")
#   - mocks (positifs) et empty (crosstalk) EXCLUS de decontam
# Traitement PAR RUN (batch = run) : 3 sequencages MiSeq distincts.
# Deux seuils compares : 0.1 (defaut, conservateur) et 0.5 (agressif, blancs fiables).
#
# Entrees : results/dada2_final/asv_table_filtered.tsv ; metadata/samples_all.csv
# Sorties : results/decontam/{asv_table_decontam_p01.tsv, asv_table_decontam_p05.tsv,
#           decontam_scores.tsv, decontam_summary.txt}

PROJECT="$HOME/work/projects/microbiome-hybrid"
cd "$PROJECT"
OUT="results/decontam"; mkdir -p "$OUT"
export PATH="$HOME/bin/envs/dada2/bin:$PATH"

GIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo nogit)
printf "%s | decontam_%s | START | %s | %s | prevalence 36 neg\n" \
  "$(date -Iseconds)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log
trap 'printf "%s | decontam_%s | FAIL | %s | %s | exit $?\n" "$(date -Iseconds)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log' ERR

Rscript - <<'EOF'
suppressPackageStartupMessages({library(decontam)})

asv_file <- "results/dada2_final/asv_table_filtered.tsv"
meta_file <- "metadata/samples_all.csv"

# --- table ASV : lignes = ASV, colonnes = echantillons {dada2_id} ---
cat("Lecture table ASV...\n")
tab <- read.delim(asv_file, row.names=1, check.names=FALSE)
# decontam attend samples en LIGNES, features en COLONNES
mat <- t(as.matrix(tab))                       # samples x ASV
cat("  dim (samples x ASV):", dim(mat)[1], "x", dim(mat)[2], "\n")

# --- metadonnees, jointure par dada2_id ---
meta <- read.csv(meta_file, check.names=FALSE)
rownames(meta) <- meta$dada2_id
meta <- meta[rownames(mat), ]                  # aligne sur la table
stopifnot(all(rownames(meta) == rownames(mat)))

# --- definir les temoins negatifs (extraction Blanc-* + PCR T-1..T-8) ---
is_blank  <- meta$sample_type == "blank"                     # extraction
is_temoin <- meta$sample_type == "temoin"                    # PCR
is_neg <- is_blank | is_temoin
# exclure mocks et empty de l'analyse (ni echantillon, ni negatif de reactifs)
keep <- meta$sample_type %in% c("biological","blank","temoin")
cat("Negatifs : extraction(Blanc)=", sum(is_blank), " PCR(T)=", sum(is_temoin),
    " total neg=", sum(is_neg), "\n", sep="")
cat("Echantillons biologiques :", sum(meta$sample_type=="biological"), "\n")
cat("Exclus (mock/empty) :", sum(!keep), "\n")

mat_k  <- mat[keep, , drop=FALSE]
meta_k <- meta[keep, , drop=FALSE]
neg_k  <- meta_k$sample_type %in% c("blank","temoin")
batch_k <- factor(meta_k$run_label)            # par run

# --- decontam prevalence, par run (batch), deux seuils ---
run_decontam <- function(thr){
  ic <- isContaminant(mat_k, method="prevalence", neg=neg_k,
                       batch=batch_k, threshold=thr)
  ic
}
cat("\n=== isContaminant prevalence, batch=run ===\n")
ic01 <- run_decontam(0.1)
ic05 <- run_decontam(0.5)
n01 <- sum(ic01$contaminant, na.rm=TRUE)
n05 <- sum(ic05$contaminant, na.rm=TRUE)
cat("Contaminants @0.1 :", n01, "/", nrow(ic01), "ASV\n")
cat("Contaminants @0.5 :", n05, "/", nrow(ic05), "ASV\n")

# --- tables decontaminees (on retire les ASV contaminants ; biologiques seulement) ---
bio <- meta$sample_type == "biological"
bio_ids <- rownames(mat)[bio]
write_clean <- function(ic, path){
  keep_asv <- rownames(ic)[!ic$contaminant %in% TRUE]
  clean <- tab[keep_asv, bio_ids, drop=FALSE]   # ASV x echantillons biologiques
  # retirer ASV devenus vides sur les biologiques
  clean <- clean[rowSums(clean) > 0, , drop=FALSE]
  write.table(data.frame(ASV=rownames(clean), clean, check.names=FALSE),
              path, sep="\t", quote=FALSE, row.names=FALSE)
  nrow(clean)
}
k01 <- write_clean(ic01, paste0("results/decontam/asv_table_decontam_p01.tsv"))
k05 <- write_clean(ic05, paste0("results/decontam/asv_table_decontam_p05.tsv"))

# --- scores par ASV (pour inspection) ---
sc <- data.frame(ASV=rownames(ic01),
                 p_prev_thr01=ic01$p, contaminant_01=ic01$contaminant,
                 contaminant_05=ic05$contaminant,
                 prev=ic01$prev)
write.table(sc, "results/decontam/decontam_scores.tsv",
            sep="\t", quote=FALSE, row.names=FALSE)

# --- lectures retirees ---
tot_reads_bio <- sum(tab[, bio_ids])
reads_after01 <- sum(read.delim("results/decontam/asv_table_decontam_p01.tsv", row.names=1, check.names=FALSE))
reads_after05 <- sum(read.delim("results/decontam/asv_table_decontam_p05.tsv", row.names=1, check.names=FALSE))

sink("results/decontam/decontam_summary.txt")
cat("DECONTAMINATION (decontam, methode prevalence, batch = run)\n")
cat("Temoins negatifs : 12 extraction (Blanc-*) + 24 PCR (T-1..T-8) = 36\n")
cat("Mocks et puits vides exclus.\n\n")
cat(sprintf("ASV en entree (table filtree)            : %d\n", ncol(mat)))
cat(sprintf("Contaminants identifies @ seuil 0.1      : %d (%.2f%%)\n", n01, 100*n01/ncol(mat)))
cat(sprintf("Contaminants identifies @ seuil 0.5      : %d (%.2f%%)\n", n05, 100*n05/ncol(mat)))
cat(sprintf("\nASV conserves (biologiques) @0.1         : %d\n", k01))
cat(sprintf("ASV conserves (biologiques) @0.5         : %d\n", k05))
cat(sprintf("\nLectures biologiques totales             : %d\n", tot_reads_bio))
cat(sprintf("Lectures conservees @0.1                 : %d (%.3f%%)\n", reads_after01, 100*reads_after01/tot_reads_bio))
cat(sprintf("Lectures conservees @0.5                 : %d (%.3f%%)\n", reads_after05, 100*reads_after05/tot_reads_bio))
cat("\nTop 15 contaminants @0.1 (plus faible p = plus probable contaminant) :\n")
top <- sc[order(sc$p_prev_thr01), ][1:15, c("ASV","p_prev_thr01","contaminant_01","contaminant_05")]
print(top, row.names=FALSE)
sink()
cat("\n--- termine ---\n")
EOF

# rapatrier au workdir pour moisson
cp results/decontam/decontam_summary.txt ./ 2>/dev/null || true
cp results/decontam/decontam_scores.tsv ./ 2>/dev/null || true
cp results/decontam/asv_table_decontam_p01.tsv ./ 2>/dev/null || true
cp results/decontam/asv_table_decontam_p05.tsv ./ 2>/dev/null || true
ls -lh ./*.txt ./*.tsv 2>/dev/null

printf "%s | decontam_%s | END | %s | %s | prevalence 36 neg\n" \
  "$(date -Iseconds)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log
cat results/decontam/decontam_summary.txt
