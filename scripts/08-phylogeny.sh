#!/bin/bash -l
#SBATCH --job-name=phylogeny
#SBATCH --account=ondemand@biomics
#SBATCH --qos=cpu-ondemand-long
#SBATCH --partition=cpu-ondemand
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=32
#SBATCH --mem=120G
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
set -eEuo pipefail

# 08-phylogeny.sh — Arbre phylogenetique de novo (MAFFT + FastTree2) via QIIME2
# Sur les ASV survivant a la decontamination (table p01, 44 256 ASV).
# Debloque UniFrac (beta) et Faith PD (alpha). Independant de l'effet run et d'Andre.
#
# Entrees : results/dada2_final/asv.fasta ; results/decontam/asv_table_analysis.tsv
# Sorties : results/phylogeny/{rooted_tree.qza, tree.nwk, aligned masked qza, filtered_asv.fasta}

PROJECT="$HOME/work/projects/microbiome-hybrid"; cd "$PROJECT"
OUT="results/phylogeny"; mkdir -p "$OUT"
IMG="$HOME/work/shared_softwares/qiime2/amplicon_2026.1.sif"
GIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo nogit)
printf "%s | phylogeny_%s | START | %s | %s | mafft-fasttree ASV decontam\n" \
  "$(date -Iseconds)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log
trap 'printf "%s | phylogeny_%s | FAIL | %s | %s | exit $?\n" "$(date -Iseconds)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log' ERR

# 1) liste des ASV decontamines (1re colonne de la table p01, sans header) -> filtrer le fasta
cut -f1 results/decontam/asv_table_analysis.tsv | tail -n +2 > "$OUT/keep_asvs.txt"
echo "ASV a inserer : $(wc -l < "$OUT/keep_asvs.txt")"
# extraire ces sequences de asv.fasta (fasta lineaire : >ASVxxxx puis 1 ligne seq)
awk 'NR==FNR{k[$1]=1; next}
     /^>/{h=substr($1,2); keep=(h in k)}
     keep{print}' "$OUT/keep_asvs.txt" results/dada2_final/asv.fasta > "$OUT/filtered_asv.fasta"
echo "sequences filtrees : $(grep -c '>' "$OUT/filtered_asv.fasta")"

# 2) import QIIME2
apptainer exec "$IMG" qiime tools import \
  --input-path "$OUT/filtered_asv.fasta" \
  --output-path "$OUT/rep_seqs.qza" \
  --type 'FeatureData[Sequence]'

# 3) MAFFT + mask + FastTree2 + midpoint root
apptainer exec "$IMG" qiime phylogeny align-to-tree-mafft-fasttree \
  --i-sequences "$OUT/rep_seqs.qza" \
  --p-n-threads "${SLURM_CPUS_PER_TASK:-8}" \
  --o-alignment "$OUT/aligned.qza" \
  --o-masked-alignment "$OUT/masked_aligned.qza" \
  --o-tree "$OUT/unrooted_tree.qza" \
  --o-rooted-tree "$OUT/rooted_tree.qza" \
  --verbose

# 4) exporter l'arbre enracine en Newick (utilisable hors QIIME2 : phyloseq, R)
apptainer exec "$IMG" qiime tools export \
  --input-path "$OUT/rooted_tree.qza" --output-path "$OUT/exported_tree"
cp "$OUT/exported_tree/tree.nwk" "$OUT/tree.nwk"
echo "=== arbre enracine ==="
echo "feuilles: $(grep -o 'ASV[0-9]*' "$OUT/tree.nwk" | sort -u | wc -l)"
head -c 300 "$OUT/tree.nwk"; echo

# rapatrier au workdir pour moisson (le .nwk est petit ; les .qza restent sur le cluster)
cp "$OUT/tree.nwk" ./ 2>/dev/null || true
ls -lh "$OUT"/*.qza "$OUT/tree.nwk"

printf "%s | phylogeny_%s | END | %s | %s | leaves=%s\n" \
  "$(date -Iseconds)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" \
  "$(grep -o 'ASV[0-9]*' "$OUT/tree.nwk" | sort -u | wc -l)" >> runs.log
