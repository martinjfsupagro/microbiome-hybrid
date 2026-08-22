#!/usr/bin/env python3
# scripts/11-flag_mock_samples.py — annotation QC des echantillons a composition mock
# NE MODIFIE PAS samples_all.csv. Produit metadata/sample_qc_flags.csv (jointure par dada2_id).
#
# Categories :
#   - mock_confirme_andre : Cab1021 & Cab1022 (Ain 2015) = MOCKS confirmes par Andre
#       (mal etiquetes, plaque 1, index serie 711). A traiter/interpreter comme MOCKS,
#       PAS comme poissons. -> Ain 2015 = 19 poissons (21 - 2), total biologique 181.
#   - mock_contaminated   : vrais poissons (4 tissus, tissus digestifs ~0% mock) dont UN
#       puits-tissu est contamine (fraction mock 0.20-0.70). Contamination de puits
#       confirmee par Andre. -> retirer les ASV mock, garder les ASV legitimes.
import csv, collections

MOCK={'ASV0030','ASV0037','ASV0055','ASV0056','ASV0091','ASV0092','ASV0100','ASV0150','ASV0262','ASV0508'}
CONFIRMED_MOCK={('Cab','2015','1021'),('Cab','2015','1022')}  # confirme Andre 2026-07-27
meta={r['dada2_id']:r for r in csv.DictReader(open('metadata/samples_all.csv'))}

with open('results/dada2_final/asv_table_filtered.tsv') as f:
    rd=csv.reader(f,delimiter='\t'); cols=next(rd)[1:]
    tot=[0]*len(cols); mk=[0]*len(cols)
    for row in rd:
        v=[int(x) for x in row[1:]]
        for i,x in enumerate(v): tot[i]+=x
        if row[0] in MOCK:
            for i,x in enumerate(v): mk[i]+=x
frac={cols[i]:(mk[i]/tot[i] if tot[i] else 0.0) for i in range(len(cols))}

tissues=collections.defaultdict(set)
for cid,m in meta.items():
    if m.get('sample_type')=='biological':
        tissues[(m['site'],m['year'],m['individual'])].add(m.get('tissue',''))

rows=[]
for cid,m in meta.items():
    if m.get('sample_type')!='biological': continue
    key=(m['site'],m['year'],m['individual'])
    fr=frac.get(cid,0.0)
    if key in CONFIRMED_MOCK:
        flag='mock_confirme_andre'
        reason=f'MOCK confirme par Andre (mal etiquete, plaque 1, puits {m["well"]} i7 {m["i7_id"]}) ; {100*fr:.0f}% lectures mock, tissu unique. A interpreter comme MOCK, pas poisson.'
        rows.append((cid,m['sample_type'],f'{fr:.4f}',len(tissues[key]),m['tissue'],flag,reason)); continue
    if fr<0.20: continue
    ntis=len(tissues[key])
    flag='mock_contaminated'
    reason=f'{100*fr:.0f}% lectures mock sur ce puits-tissu ; vrai poisson (n_tissus={ntis}, autres tissus propres) ; puits {m["well"]}. Contamination confirmee Andre -> retirer ASV mock, garder legitimes.'
    rows.append((cid,m['sample_type'],f'{fr:.4f}',ntis,m['tissue'],flag,reason))

order={'mock_confirme_andre':0,'mock_contaminated':1}
rows.sort(key=lambda r:(order.get(r[5],9), -float(r[2])))
with open('metadata/sample_qc_flags.csv','w',newline='') as o:
    w=csv.writer(o)
    w.writerow(['dada2_id','sample_type_original','mock_fraction','n_tissus_individu','tissu','qc_flag','reason'])
    for r in rows: w.writerow(r)

c=collections.Counter(r[5] for r in rows)
print('mock_confirme_andre:',c['mock_confirme_andre'],'| mock_contaminated:',c['mock_contaminated'],'| total:',len(rows))
