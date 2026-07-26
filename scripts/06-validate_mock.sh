#!/bin/bash -l
#SBATCH --job-name=validate_mock
#SBATCH --account=ondemand@biomics
#SBATCH --partition=cpu-ondemand
#SBATCH --time=00:20:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
set -eo pipefail

# 06-validate_mock.sh — Validation des communautés mock ZymoBIOMICS (contrôle positif ASV)
# Compare les ASV présents dans les échantillons mock à la référence 16S Zymo
# (ancien lot ZR160406, souches 2014-2015) par blastn, et résume la complétude
# (8 espèces attendues), la pureté (% lectures Zymo) et les ASV parasites.
#
# Usage : sbatch scripts/06-validate_mock.sh
# Entrées : results/dada2_final/{asv_table_filtered.tsv,asv.fasta,taxonomy.tsv}
#           refs/zymo_mock/zymo_mock_8bact_16S_ZR160406.fasta
# Sorties : results/mock_validation/{mock_asv_abundance.tsv,mock_blast.tsv,mock_validation_summary.txt}

PROJECT="$HOME/work/projects/microbiome-hybrid"
cd "$PROJECT"
OUT="results/mock_validation"
mkdir -p "$OUT"

ASV_TABLE="results/dada2_final/asv_table_filtered.tsv"
ASV_FASTA="results/dada2_final/asv.fasta"
TAXO="results/dada2_final/taxonomy.tsv"
ZYMO_REF="refs/zymo_mock/zymo_mock_8bact_16S_ZR160406.fasta"

echo "[1/4] Extraction des ASV des echantillons mock"
python3 - "$ASV_TABLE" "$ASV_FASTA" "$OUT" <<'PY'
import sys
asv_table, asv_fasta, out = sys.argv[1], sys.argv[2], sys.argv[3]
# header -> mock column indices
with open(asv_table) as f:
    header = f.readline().rstrip("\n").split("\t")
mock_idx = [i for i,c in enumerate(header) if c.split("__")[0] in ("Mock-1","Mock-2")]
mock_names = [header[i] for i in mock_idx]
print("  colonnes mock:", mock_names)
abund = {}   # asv -> {mockname: reads}
with open(asv_table) as f:
    f.readline()
    for line in f:
        p = line.rstrip("\n").split("\t")
        asv = p[0]
        vals = {header[i]: int(p[i]) for i in mock_idx}
        tot = sum(vals.values())
        if tot > 0:
            vals["_total"] = tot
            abund[asv] = vals
print("  ASV presents dans au moins un mock:", len(abund))
# write abundance skeleton (annotated later) and the fasta subset
seqs = {}
name=None
with open(asv_fasta) as f:
    for line in f:
        if line.startswith(">"):
            name=line[1:].strip().split()[0]; seqs[name]=[]
        else:
            seqs[name].append(line.strip())
seqs={k:"".join(v) for k,v in seqs.items()}
with open(f"{out}/mock_asvs.fasta","w") as fh:
    for asv in abund:
        fh.write(f">{asv}\n{seqs[asv]}\n")
# stash order + columns for later
import json
json.dump({"mock_names":mock_names,"abund":abund}, open(f"{out}/_mock_abund.json","w"))
PY

echo "[2/4] blastn des ASV mock contre la reference Zymo"
module load blast/2.13.0
makeblastdb -in "$ZYMO_REF" -dbtype nucl -out "$OUT/zymo_db" >/dev/null
blastn -query "$OUT/mock_asvs.fasta" -db "$OUT/zymo_db" \
  -perc_identity 90 -max_target_seqs 5 -num_threads 4 \
  -outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen" \
  > "$OUT/mock_blast.tsv"
echo "  hits blast: $(wc -l < "$OUT/mock_blast.tsv")"

echo "[3/4] Synthese"
python3 - "$OUT" "$TAXO" <<'PY'
import sys, json
from collections import defaultdict
out, taxo = sys.argv[1], sys.argv[2]
d = json.load(open(f"{out}/_mock_abund.json"))
mock_names, abund = d["mock_names"], d["abund"]

# SILVA genus per ASV
genus = {}
with open(taxo) as f:
    f.readline()
    for line in f:
        p = line.rstrip("\n").split("\t")
        genus[p[0]] = p[6] if len(p)>6 and p[6] else "NA"

# best blast hit per ASV (>=99% id, >=240 aln = confident V4 match)
best = {}
allhits = defaultdict(list)
with open(f"{out}/mock_blast.tsv") as f:
    for line in f:
        p=line.rstrip("\n").split("\t")
        q,s,pid,length = p[0],p[1],float(p[2]),int(p[3])
        allhits[q].append((pid,length,s))
        if (q not in best) or (pid,length) > (best[q][0],best[q][1]):
            best[q]=(pid,length,s)

def species_of(sseqid):
    # strip trailing _1/_2 copy suffix and _16S
    base = sseqid.replace("_16S","")
    for suf in ("_1","_2","_3"):
        if base.endswith(suf): base=base[:-2]
    return base

EXPECTED = ["Bacillus_subtilis","Enterococcus_faecalis","Escherichia_coli",
            "Lactobacillus_fermentum","Listeria_monocytogenes","Pseudomonas_aeruginosa",
            "Salmonella_enterica","Staphylococcus_aureus"]

# annotated per-ASV table
rows=[]
for asv,vals in sorted(abund.items(), key=lambda kv:-kv[1]["_total"]):
    b=best.get(asv)
    if b:
        pid,length,s=b; sp=species_of(s); hit=f"{sp} ({pid:.1f}%/{length}bp)"
        conf = (pid>=99.0 and length>=240)
    else:
        sp="-"; hit="no hit >=90%"; conf=False
    rows.append((asv, vals["_total"], [vals.get(m,0) for m in mock_names],
                 genus.get(asv,"NA"), sp, hit, conf))

with open(f"{out}/mock_asv_abundance.tsv","w") as fh:
    fh.write("ASV\ttotal_mock_reads\t"+"\t".join(mock_names)+"\tSILVA_genus\tzymo_species\tbest_hit\tconfident\n")
    for asv,tot,per,g,sp,hit,conf in rows:
        fh.write(f"{asv}\t{tot}\t"+"\t".join(map(str,per))+f"\t{g}\t{sp}\t{hit}\t{conf}\n")

# per-sample summary
def summ(colname=None):
    lines=[]
    for m in mock_names:
        tot=sum(abund[a].get(m,0) for a in abund)
        zymo=sum(abund[a].get(m,0) for a in abund
                 if best.get(a) and best[a][0]>=99.0 and best[a][1]>=240)
        recov=set()
        for a in abund:
            if abund[a].get(m,0)>0 and best.get(a) and best[a][0]>=99.0 and best[a][1]>=240:
                recov.add(species_of(best[a][2]))
        # spurious = abundant ASV (>=1% of sample) with no confident Zymo hit
        spur=[a for a in abund if abund[a].get(m,0)>=0.01*max(tot,1)
              and not (best.get(a) and best[a][0]>=99.0 and best[a][1]>=240)]
        pct = 100*zymo/tot if tot else 0
        lines.append((m,tot,zymo,pct,len(recov & set(EXPECTED)),sorted(recov & set(EXPECTED)),
                      sorted(set(EXPECTED)-recov),len(spur)))
    return lines

with open(f"{out}/mock_validation_summary.txt","w") as fh:
    fh.write("VALIDATION DES MOCKS ZymoBIOMICS (reference ancien lot ZR160406, souches 2014-2015)\n")
    fh.write("Critere de match confiant : identite >=99% ET longueur alignee >=240 pb (V4)\n")
    fh.write("8 especes attendues : "+", ".join(EXPECTED)+"\n\n")
    for m,tot,zymo,pct,nrec,rec,missing,nspur in summ():
        fh.write(f"== {m} ==\n")
        fh.write(f"  lectures totales      : {tot:,}\n")
        fh.write(f"  lectures Zymo (conf.) : {zymo:,} ({pct:.1f}%)\n")
        fh.write(f"  especes recuperees    : {nrec}/8  {rec}\n")
        if missing: fh.write(f"  especes MANQUANTES    : {missing}\n")
        fh.write(f"  ASV parasites (>=1%, non-Zymo) : {nspur}\n\n")
    # top ASVs overall
    fh.write("TOP 15 ASV (toutes colonnes mock confondues) :\n")
    fh.write(f"{'ASV':9} {'reads':>8}  {'SILVA_genus':22} {'best_hit':40}\n")
    for asv,tot,per,g,sp,hit,conf in rows[:15]:
        fh.write(f"{asv:9} {tot:>8}  {g:22.22} {hit:40.40}\n")

import os
os.remove(f"{out}/_mock_abund.json")
print("  synthese ecrite")
PY

echo "[4/4] Trace runs.log"
GITHASH=$(git rev-parse --short HEAD 2>/dev/null || echo "nogit")
printf "%s | validate_mock_%s | END | %s | %s | mock validation Zymo\n" \
  "$(date -Iseconds)" "${SLURM_JOB_ID:-local}" "$GITHASH" "$(basename "$0")" >> runs.log

echo "=== RESUME ==="
cat "$OUT/mock_validation_summary.txt"
