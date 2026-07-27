#!/usr/bin/env python3
# scripts/11-flag_mock_samples.py — annotation QC des echantillons a composition mock
# NE MODIFIE PAS samples_all.csv. Produit une table de jointure metadata/sample_qc_flags.csv
# (jointure par dada2_id), sur le meme principe que site_mapping.csv.
#
# Deux categories, fondees sur : fraction de lectures = ASV du mock Zymo, ET nombre de
# tissus distincts de l'individu (un vrai poisson = 4 tissus).
#   - probable_mock         : frac >= 0.70 ET individu SANS tissu intestinal/branchial
#                             (n'a que la caudale) -> n'est pas un poisson, exclure du biologique
#   - mock_contaminated     : 0.20 <= frac < 0.70 sur un puits-tissu d'un VRAI poisson
#                             (autres tissus propres) -> garder le poisson, signaler le puits
import csv, collections

MOCK={'ASV0030','ASV0037','ASV0055','ASV0056','ASV0091','ASV0092','ASV0100','ASV0150','ASV0262','ASV0508'}
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

# nb de tissus distincts par individu biologique (site+annee+individu)
tissues=collections.defaultdict(set)
for cid,m in meta.items():
    if m.get('sample_type')=='biological':
        key=(m['site'],m['year'],m['individual'])
        if m.get('tissue'): tissues[key].add(m['tissue'])

rows=[]
for cid,m in meta.items():
    if m.get('sample_type')!='biological': continue
    fr=frac.get(cid,0.0)
    if fr<0.20: continue
    key=(m['site'],m['year'],m['individual'])
    ntis=len(tissues[key])
    if fr>=0.70 and ntis<=1:
        flag='probable_mock'
        reason=f'{100*fr:.0f}% lectures mock ; individu sans tissu digestif/branchial (n_tissus={ntis}) ; puits {m["well"]} i7 {m["i7_id"]} co-localise mocks'
    elif fr>=0.70:
        flag='probable_mock'
        reason=f'{100*fr:.0f}% lectures mock (n_tissus={ntis})'
    else:
        flag='mock_contaminated'
        reason=f'{100*fr:.0f}% lectures mock sur ce puits-tissu ; vrai poisson (n_tissus={ntis}, autres tissus propres) ; puits {m["well"]}'
    rows.append((cid, m['sample_type'], f'{fr:.4f}', ntis, m['tissue'], flag, reason))

rows.sort(key=lambda r:(r[5], -float(r[2])))
with open('metadata/sample_qc_flags.csv','w',newline='') as o:
    w=csv.writer(o)
    w.writerow(['dada2_id','sample_type_original','mock_fraction','n_tissus_individu','tissu','qc_flag','reason'])
    for r in rows: w.writerow(r)

nb_pm=sum(1 for r in rows if r[5]=='probable_mock')
nb_mc=sum(1 for r in rows if r[5]=='mock_contaminated')
print(f'probable_mock : {nb_pm} | mock_contaminated : {nb_mc} | total flagge : {len(rows)}')
for r in rows:
    print(f'  {r[5]:18} {r[0]:28} frac={float(r[2])*100:5.1f}% n_tis={r[3]} {r[4]}')
