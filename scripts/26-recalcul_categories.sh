#!/bin/bash -l
#SBATCH --job-name=recat_2passes
#SBATCH --account=ondemand@biomics
#SBATCH --qos=cpu-ondemand-long
#SBATCH --partition=cpu-ondemand
#SBATCH --time=04:00:00
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
set -uo pipefail
# 26-recalcul_categories.sh — relance des analyses par categorie en deux passes (2026-09-25)
#
# CLASSIFICATION. metadata/analysis_metadata.csv (script 19, version du 2026-09-25) porte
# categorie (septembre, 25 chr), categorie_aout_12chr et inclus_passe1. Chaque script lit
# la variable PASSE :
#   aout   : classes d'aout, n=180      -> TEMOIN DE REPRODUCTION pour 20 (et 24 approx.)
#   2      : septembre, 42 Hy, n=180
#   1      : septembre, 22 quasi-purs EXCLUS (non reverses), n=158
#   morpho : taxon morphologique (17, 18 seulement) -> TEMOIN DE REPRODUCTION pour 17 et 18,
#            qui n'ont JAMAIS lu la categorie genotypique : leur version d'aout utilisait le
#            taxon morphologique de samples_all.csv.
# Les sorties d'aout (results/position_effect, var_partition_cat, var_partition_cat_d500,
# permdisp) ne sont PAS ecrasees : tout va sous results/recat/<passe>/.
#
# ETAPES INDEPENDANTES : un echec n'arrete pas les autres, il est trace dans
# results/recat/status.tsv (etape, passe, code retour, duree).
cd "$HOME/work/projects/microbiome-hybrid"
mkdir -p results/recat logs
ST=results/recat/status.tsv
printf 'etape\tpasse\tcode\tsecondes\n' > "$ST"
step() {  # step <etiquette> <passe> <cmd...>
  local lab=$1 ps=$2; shift 2; local t0=$(date +%s)
  echo "===== $lab | PASSE=$ps | $(date -Is)"
  env PASSE="$ps" "$@"; local rc=$?
  printf '%s\t%s\t%s\t%s\n' "$lab" "$ps" "$rc" "$(( $(date +%s) - t0 ))" >> "$ST"
  echo "===== $lab | PASSE=$ps | code $rc"
}
for ps in morpho aout 2 1; do
  d=results/recat/$ps; mkdir -p "$d/position_effect"
  step 17-position "$ps" env POS_OUTDIR="$d/position_effect" bash scripts/17-position_effect.sh
  step 18-control  "$ps" env POS_OUTDIR="$d/position_effect" bash scripts/18-position_control.sh
done
for ps in aout 2 1; do
  d=results/recat/$ps; mkdir -p "$d/var_partition_cat" "$d/var_partition_cat_d500" "$d/permdisp"
  step 20-partition      "$ps" env CATPART_OUTDIR="$d/var_partition_cat" bash scripts/20-variance_partition_category.sh
  step 20-partition-d500 "$ps" env CATPART_OUTDIR="$d/var_partition_cat_d500" \
       CATPART_GLOB="results/rarefaction_d500/beta_mean_*.rds" bash scripts/20-variance_partition_category.sh
  step 24-permdisp       "$ps" env PERMDISP_OUTDIR="$d/permdisp" bash scripts/24-permdisp.sh
done
echo; cat "$ST"
