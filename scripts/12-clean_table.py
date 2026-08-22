#!/usr/bin/env python3
# scripts/12-clean_table.py — table ASV propre unique (point de depart canonique aval)
# Applique les decisions figees (reunion Andre 2026-07-27) sur la table decontaminee :
#   1. EXCLURE les echantillons mock_confirme_andre (6 : Cab1021/Cab1022 x3 runs) — mocks, pas poissons.
#   2. RETIRER les 10 ASV du mock Zymo de TOUS les echantillons (decision_mock_removal.md).
#   3. RETIRER les ASV devenus entierement nuls apres (1)+(2).
# NE rarefie PAS (mode tirage unique vs repete non tranche — decision_rarefaction.md).
# NE modifie PAS samples_all.csv. Entree : results/decontam/asv_table_analysis.tsv.
import csv, sys

MOCK={'ASV0030','ASV0037','ASV0055','ASV0056','ASV0091','ASV0092','ASV0100','ASV0150','ASV0262','ASV0508'}
flags={r['dada2_id']:r['qc_flag'] for r in csv.DictReader(open('metadata/sample_qc_flags.csv'))}
drop_cols={s for s,f in flags.items() if f=='mock_confirme_andre'}

inp='results/decontam/asv_table_analysis.tsv'
out='results/decontam/asv_table_clean.tsv'

with open(inp) as f, open(out,'w',newline='') as o:
    rd=csv.reader(f,delimiter='\t'); w=csv.writer(o,delimiter='\t')
    hdr=next(rd)
    keep_idx=[0]+[i for i,c in enumerate(hdr) if i>0 and c not in drop_cols]
    new_hdr=[hdr[i] for i in keep_idx]
    w.writerow(new_hdr)
    n_asv_in=0; n_asv_out=0; n_mock_asv=0; n_empty=0
    reads_out=0
    for row in rd:
        n_asv_in+=1
        asv=row[0]
        if asv in MOCK:
            n_mock_asv+=1; continue                      # retrait ASV mock (etape 2)
        vals=[row[i] for i in keep_idx]                  # colonnes gardees (etape 1)
        s=sum(int(x) for x in vals[1:])
        if s==0:
            n_empty+=1; continue                         # ASV devenu vide (etape 3)
        w.writerow(vals); n_asv_out+=1; reads_out+=s

with open('results/decontam/clean_table_summary.txt','w') as o:
    o.write("TABLE PROPRE — asv_table_clean.tsv (decisions reunion Andre 2026-07-27)\n\n")
    o.write(f"Echantillons : {len(hdr)-1} -> {len(new_hdr)-1} "
            f"(retire {len(hdr)-len(new_hdr)} mock_confirme_andre : {sorted(drop_cols)})\n")
    o.write(f"ASV          : {n_asv_in} -> {n_asv_out}\n")
    o.write(f"  dont ASV mock Zymo retires (etape 2)     : {n_mock_asv}\n")
    o.write(f"  dont ASV devenus vides retires (etape 3) : {n_empty}\n")
    o.write(f"Lectures conservees : {reads_out:,}\n")
    o.write("\nNB : non rarefiee. Les 20 echantillons mock_contaminated sont conserves,\n")
    o.write("ASV mock retires ; certains passeront sous 3000 lectures a la rarefaction (attendu).\n")

print(open('results/decontam/clean_table_summary.txt').read())
