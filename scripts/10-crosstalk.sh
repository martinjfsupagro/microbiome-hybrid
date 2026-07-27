#!/bin/bash -l
#SBATCH --job-name=crosstalk
#SBATCH --account=ondemand@biomics
#SBATCH --qos=cpu-ondemand-long
#SBATCH --partition=cpu-ondemand
#SBATCH --time=01:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
set -eEuo pipefail

# 10-crosstalk.sh — Quantification du crosstalk (saut d'index) via les puits vides
#   et les traceurs mock (taxons Zymo, exogenes).
# Independant d'Andre. Table d'entree : results/dada2_final/asv_table_filtered.tsv
#   (contient TOUS les echantillons : biologiques + empty + mock + temoins).
#
# Sorties results/crosstalk/ :
#   empty_totals.tsv          — lectures parasites par puits vide
#   crosstalk_summary.txt     — taux global + fuite des traceurs mock
#   mock_leakage.tsv          — repartition des lectures des ASV mock par type d'echantillon

PROJECT="$HOME/work/projects/microbiome-hybrid"; cd "$PROJECT"
OUT="results/crosstalk"; mkdir -p "$OUT"
export PATH="$HOME/bin/envs/dada2/bin:$PATH"
GIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo nogit)
printf "%s | crosstalk_%s | START | %s | %s | empties+mock tracers\n" \
  "$(date -Iseconds)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log
trap 'printf "%s | crosstalk_%s | FAIL | %s | %s | exit $?\n" "$(date -Iseconds)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log' ERR

python3 - <<'PY'
import csv, statistics
MOCK_ASV = {"ASV0030","ASV0037","ASV0055","ASV0056","ASV0091","ASV0092","ASV0100","ASV0150","ASV0262","ASV0508"}

# metadonnees : type par dada2_id + index i7/i5
meta={}
with open("metadata/samples_all.csv") as f:
    for r in csv.DictReader(f):
        meta[r["dada2_id"]]=r

tbl="results/dada2_final/asv_table_filtered.tsv"
with open(tbl) as f:
    rd=csv.reader(f,delimiter="\t")
    cols=next(rd)[1:]            # dada2_id des echantillons
    # type par colonne
    typ=[meta.get(c,{}).get("sample_type","?") for c in cols]
    run=[meta.get(c,{}).get("run_label","?") for c in cols]
    # accumulateurs
    col_tot=[0]*len(cols)                    # total lectures par echantillon
    mock_by_type={}                          # lectures des ASV mock par type
    mock_by_col={}                           # lectures mock par colonne (pour puits bio contamines)
    for row in rd:
        asv=row[0]; vals=row[1:]
        v=[int(x) for x in vals]
        for i,x in enumerate(v): col_tot[i]+=x
        if asv in MOCK_ASV:
            for i,x in enumerate(v):
                if x>0:
                    mock_by_type[typ[i]]=mock_by_type.get(typ[i],0)+x
                    mock_by_col[i]=mock_by_col.get(i,0)+x

# --- 1) puits vides : lectures parasites ---
empty_idx=[i for i,t in enumerate(typ) if t=="empty"]
bio_idx  =[i for i,t in enumerate(typ) if t=="biological"]
mock_idx =[i for i,t in enumerate(typ) if t=="mock"]
grand_tot=sum(col_tot)
empty_reads=sum(col_tot[i] for i in empty_idx)

with open("results/crosstalk/empty_totals.tsv","w") as o:
    o.write("dada2_id\trun\treads_parasites\n")
    for i in sorted(empty_idx,key=lambda i:-col_tot[i]):
        o.write(f"{cols[i]}\t{run[i]}\t{col_tot[i]}\n")

# --- 2) fuite des traceurs mock ---
mock_total=sum(mock_by_type.values())
mock_in_mock=mock_by_type.get("mock",0)
mock_leak=mock_total-mock_in_mock
with open("results/crosstalk/mock_leakage.tsv","w") as o:
    o.write("sample_type\treads_ASV_mock\tpct_du_total_mock\n")
    for t,x in sorted(mock_by_type.items(),key=lambda kv:-kv[1]):
        o.write(f"{t}\t{x}\t{100*x/mock_total:.4f}\n")

# taux de contamination mock par echantillon biologique (crosstalk entrant)
bio_mock=[(cols[i],mock_by_col.get(i,0),col_tot[i]) for i in bio_idx if mock_by_col.get(i,0)>0]
bio_mock.sort(key=lambda t:-t[1])

with open("results/crosstalk/crosstalk_summary.txt","w") as o:
    o.write("QUANTIFICATION DU CROSSTALK (saut d'index) — projet microbiome-hybrid\n\n")
    o.write("=== 1) Puits vides (aucune librairie chargee -> tout read = fuite) ===\n")
    o.write(f"Puits vides : {len(empty_idx)}\n")
    o.write(f"Lectures parasites totales dans les vides : {empty_reads:,}\n")
    o.write(f"Total lectures (tous echantillons)        : {grand_tot:,}\n")
    o.write(f"Taux de crosstalk (vides / total)         : {100*empty_reads/grand_tot:.4f} %\n")
    ev=[col_tot[i] for i in empty_idx]
    o.write(f"Par puits vide : median {int(statistics.median(ev)):,} | max {max(ev):,} | min {min(ev):,}\n\n")
    o.write("=== 2) Traceurs mock (8 taxons Zymo, exogenes -> hors mock = fuite) ===\n")
    o.write(f"Lectures totales des ASV mock             : {mock_total:,}\n")
    o.write(f"  dans les puits mock (attendu)           : {mock_in_mock:,} ({100*mock_in_mock/mock_total:.3f} %)\n")
    o.write(f"  FUITE hors mock                         : {mock_leak:,} ({100*mock_leak/mock_total:.3f} %)\n")
    o.write("Repartition de la fuite par type :\n")
    for t,x in sorted(mock_by_type.items(),key=lambda kv:-kv[1]):
        if t!="mock": o.write(f"   {t:12} {x:>8,} lectures\n")
    o.write(f"\nEchantillons biologiques contamines par des ASV mock : {len(bio_mock)}/{len(bio_idx)}\n")
    if bio_mock:
        fr=[m/tot for _,m,tot in bio_mock if tot>0]
        o.write(f"Fraction mock dans ces echantillons : median {100*statistics.median(fr):.4f} % | max {100*max(fr):.3f} %\n")
        o.write("Top 10 echantillons bio les plus contamines :\n")
        for cid,m,tot in bio_mock[:10]:
            o.write(f"   {cid:28} {m:>6,} / {tot:>7,} lectures ({100*m/tot:.3f} %)\n")

print("termine")
PY

for f in crosstalk_summary.txt empty_totals.tsv mock_leakage.tsv; do
  cp "results/crosstalk/$f" ./ 2>/dev/null || true
done
ls -lh ./*.tsv ./*.txt 2>/dev/null

printf "%s | crosstalk_%s | END | %s | %s | empties+mock tracers\n" \
  "$(date -Iseconds)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log
cat results/crosstalk/crosstalk_summary.txt
