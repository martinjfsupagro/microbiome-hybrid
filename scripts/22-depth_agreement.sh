#!/bin/bash -l
#SBATCH --job-name=depth_agreement
#SBATCH --account=ondemand@biomics
#SBATCH --qos=cpu-ondemand-long
#SBATCH --partition=cpu-ondemand
#SBATCH --time=04:00:00
#SBATCH --cpus-per-task=32
#SBATCH --mem=128G
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
set -eEuo pipefail

# 22-depth_agreement.sh — a quelle profondeur les metriques cessent-elles de mesurer
#                          la meme chose qu'a 3000 ?
#
# POURQUOI. Le seuil de rarefaction fait DEUX choses a la fois : il egalise la
# profondeur (but de la rarefaction) et il decide quels echantillons entrent
# (filtre de selection). Le filtre est oriente : dans la caudale, 57 % des hybrides
# passent 3000 contre 87 % des Pt (+30 points), et l'ecart atteint +53 points a
# Buech-Meouge, l'une des trois stations a gradient complet. Baisser le seuil corrige
# la selection mais degrade les metriques.
#
# CE QUE CE JOB MESURE. Sur un jeu d'echantillons FIXE (les 1 784 retenus a 3000), on
# rarefie a 1000, 1500 et 2000 et on compare aux matrices de reference a 3000. Le jeu
# etant identique, l'ecart mesure l'effet de la PROFONDEUR seule, sans melange avec la
# selection. C'est ce qui permet de choisir le seuil de sensibilite sur une mesure.
#
# METRIQUES TESTEES. Les deux metriques de PRESENCE (Jaccard, UniFrac non pondere) sont
# celles dont la validite est en cause a faible profondeur : elles dependent des taxons
# rares, les premiers perdus. UniFrac PONDERE est inclus comme temoin de contraste — s'il
# reste stable la ou les metriques de presence se degradent, cela confirme que la
# degradation vient bien de la perte des rares et non d'un artefact general.
# Bray-Curtis n'est PAS teste ici (vegdist n'est pas disponible dans l'image) : c'est une
# metrique ponderee, son comportement est encadre par celui d'UniFrac pondere, mais ce
# n'est pas verifie.
#
# N = 20 tirages par profondeur : l'erreur de Monte-Carlo etait deja sous 0.1 % a N = 25
# sur ce jeu (results/rarefaction/beta_convergence.tsv, et phylo_convergence.tsv pour
# UniFrac), donc tres inferieure aux ecarts entre profondeurs qu'on cherche a mesurer.
#
# Sortie : results/depth_agreement/depth_agreement.tsv + .txt

cd "$HOME/work/projects/microbiome-hybrid"
OUT=results/depth_agreement
mkdir -p "$OUT" logs
IMG="$HOME/work/shared_softwares/qiime2/amplicon_2026.1.sif"
GIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo NA)
printf '%s\tSTART\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-8}"
export TMPDIR=/scratch/users/martinj/tmp_depth_${SLURM_JOB_ID:-local}
mkdir -p "$TMPDIR"

apptainer exec "$IMG" python - <<'PY' 2>&1 | tee results/depth_agreement/depth_agreement.txt
import os, sys, time, gzip
import numpy as np, h5py, biom, unifrac
from scipy.sparse import csc_matrix

T0=time.time()
REF_DEPTH=3000; DEPTHS=[1000,1500,2000]; NDRAW=20
OUT="results/depth_agreement"; TREE="results/phylogeny/tree.nwk"
TABLE="results/decontam/asv_table_clean.tsv"
def log(*a): print(f"[{time.time()-T0:7.1f}s]",*a); sys.stdout.flush()

log("lecture de la table propre...")
with open(TABLE) as fh: samples=fh.readline().rstrip("\n").split("\t")[1:]
n_s=len(samples); feat=[]; ri=[]; ci=[]; vv=[]
with open(TABLE) as fh:
    fh.readline()
    for i,line in enumerate(fh):
        tab=line.index("\t"); feat.append(line[:tab])
        v=np.array(line[tab+1:].rstrip("\n").split("\t"),dtype=np.int64)
        nz=np.flatnonzero(v)
        if nz.size:
            ri.append(np.full(nz.size,i,dtype=np.int64)); ci.append(nz); vv.append(v[nz])
n_f=len(feat)
Mat=csc_matrix((np.concatenate(vv),(np.concatenate(ri),np.concatenate(ci))),shape=(n_f,n_s))
depths=np.asarray(Mat.sum(axis=0)).ravel()
keep=np.where(depths>=REF_DEPTH)[0]
Mat=Mat[:,keep]; kept=[samples[j] for j in keep]; N_S=len(kept)
log(f"  jeu FIXE : {N_S} echantillons (ceux retenus a {REF_DEPTH})")
col_idx=[Mat.indices[Mat.indptr[j]:Mat.indptr[j+1]] for j in range(N_S)]
col_val=[Mat.data[Mat.indptr[j]:Mat.indptr[j+1]].astype(np.int64) for j in range(N_S)]

from bp import parse_newick
with open(TREE) as fh: TREE_OBJ=parse_newick(fh.read())
BPATH=os.path.join(os.environ["TMPDIR"],"r.biom")
IU=np.triu_indices(N_S,1)

def rarefy(rng,depth):
    a,b,c=[],[],[]
    for j in range(N_S):
        sub=rng.multivariate_hypergeometric(col_val[j],depth,method="marginals")
        nz=sub>0
        a.append(col_idx[j][nz]); b.append(np.full(nz.sum(),j,dtype=np.int64)); c.append(sub[nz])
    return csc_matrix((np.concatenate(c),(np.concatenate(a),np.concatenate(b))),shape=(n_f,N_S))

def jaccard(R):
    """Jaccard binaire par produit matriciel creux : |A inter B| = B Bt."""
    Bm=(R.T.tocsr()>0).astype(np.float64)          # echantillons x ASV
    inter=np.asarray((Bm@Bm.T).todense())
    sz=np.asarray(Bm.sum(axis=1)).ravel()
    union=sz[:,None]+sz[None,:]-inter
    with np.errstate(invalid="ignore",divide="ignore"):
        J=1.0-inter/union
    J[union==0]=0.0; np.fill_diagonal(J,0.0)
    return J

def uni(fn,R):
    present=np.unique(R.indices)
    tab=biom.Table(R.tocsr()[present,:],[feat[i] for i in present],kept)
    with h5py.File(BPATH,"w") as h5: tab.to_hdf5(h5,"22-depth")
    D=fn(BPATH,TREE)
    if list(D.ids)!=kept: D=D.filter(kept)
    return D.data

def mean_over(depth,nd,seed):
    acc={"jaccard":np.zeros((N_S,N_S)),"unifrac_unweighted":np.zeros((N_S,N_S)),
         "unifrac_weighted":np.zeros((N_S,N_S)),"richness":np.zeros(N_S)}
    for k in range(nd):
        R=rarefy(np.random.default_rng(seed+k),depth)
        acc["jaccard"]+=jaccard(R)
        acc["unifrac_unweighted"]+=uni(unifrac.unweighted,R)
        acc["unifrac_weighted"]+=uni(unifrac.weighted_normalized,R)
        acc["richness"]+=np.asarray((R>0).sum(axis=0)).ravel()
    return {k:v/nd for k,v in acc.items()}

# --- references a 3000 : les matrices deja produites, restreintes au meme jeu ---
log("lecture des references a 3000...")
REF={}
import csv as _csv
def read_sq(path):
    with gzip.open(path,"rt") as fh:
        hdr=fh.readline().rstrip("\n").split("\t")[1:]
        idx={s:i for i,s in enumerate(hdr)}
        M=np.zeros((len(hdr),len(hdr)))
        for i,line in enumerate(fh):
            M[i]=np.array(line.rstrip("\n").split("\t")[1:],dtype=float)
    order=[idx[s] for s in kept]
    return M[np.ix_(order,order)]
REF["unifrac_unweighted"]=read_sq("results/phylo_diversity/unifrac_unweighted_mean.tsv.gz")
REF["unifrac_weighted"]=read_sq("results/phylo_diversity/unifrac_weighted_mean.tsv.gz")
log("  UniFrac charges")
# Jaccard de reference : recalcule ICI a 3000 avec le meme code, pour que la comparaison
# porte sur la profondeur et non sur une difference d'implementation.
log("  Jaccard de reference recalcule a 3000 (meme code que les profondeurs testees)")
ref3=mean_over(REF_DEPTH,NDRAW,seed=101)
REF["jaccard"]=ref3["jaccard"]
REF_RICH=ref3["richness"]

# TEMOIN QUI PEUT ECHOUER : le meme calcul UniFrac refait ici a 3000 (N=20) doit
# reproduire les matrices de reference (N=400) lues et REORDONNEES par read_sq. Si
# read_sq s'etait trompe d'ordre, la correlation s'effondrerait. C'est le controle de
# l'appariement des identifiants, pas seulement de la convergence.
log("  temoin d'appariement : UniFrac recalcule a 3000 vs reference N=400")
for met in ("unifrac_unweighted","unifrac_weighted"):
    a=REF[met][IU]; b=ref3[met][IU]
    rr_=np.corrcoef(a,b)[0,1]
    log(f"    {met:20} r={rr_:.6f} | ecart absolu moyen {np.abs(b-a).mean():.5f}")
    assert rr_>0.999, (f"desaccord sur {met} (r={rr_:.4f}) : l'ordre des echantillons "
                       f"lu par read_sq est probablement faux")
log("    -> appariement des identifiants confirme")

rows=[]
for d in DEPTHS:
    log(f"=== profondeur {d} ===")
    m=mean_over(d,NDRAW,seed=1000*d)
    for met in ("jaccard","unifrac_unweighted","unifrac_weighted"):
        a=REF[met][IU]; b=m[met][IU]
        r=np.corrcoef(a,b)[0,1]
        bias=(b-a).mean(); mad=np.abs(b-a).mean()
        rows.append({"profondeur":d,"metrique":met,"r_pearson":r,
                     "biais_moyen":bias,"ecart_absolu_moyen":mad,
                     "distance_moyenne_ref":a.mean(),
                     "ecart_relatif":mad/a.mean()})
        log(f"  {met:20} r={r:.4f} | biais {bias:+.4f} | ecart abs moyen {mad:.4f} "
            f"({100*mad/a.mean():.1f} % de la distance moyenne)")
    rr=m["richness"]
    rows.append({"profondeur":d,"metrique":"richness","r_pearson":np.corrcoef(REF_RICH,rr)[0,1],
                 "biais_moyen":(rr-REF_RICH).mean(),"ecart_absolu_moyen":np.abs(rr-REF_RICH).mean(),
                 "distance_moyenne_ref":REF_RICH.mean(),
                 "ecart_relatif":np.abs(rr-REF_RICH).mean()/REF_RICH.mean()})
    log(f"  {'richness':20} r={np.corrcoef(REF_RICH,rr)[0,1]:.4f} | "
        f"{REF_RICH.mean():.0f} ASV a 3000 -> {rr.mean():.0f} a {d} "
        f"({100*(rr.mean()-REF_RICH.mean())/REF_RICH.mean():+.0f} %)")

ks=["profondeur","metrique","r_pearson","biais_moyen","ecart_absolu_moyen",
    "distance_moyenne_ref","ecart_relatif"]
with open(os.path.join(OUT,"depth_agreement.tsv"),"w") as fh:
    fh.write("\t".join(ks)+"\n")
    for r_ in rows: fh.write("\t".join(str(r_[k]) for k in ks)+"\n")
log("TERMINE")
PY

rm -rf "$TMPDIR"
printf '%s\tEND\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log
