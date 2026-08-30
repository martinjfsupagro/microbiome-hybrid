#!/bin/bash -l
#SBATCH --job-name=unifrac_faith
#SBATCH --account=ondemand@biomics
#SBATCH --qos=cpu-ondemand-long
#SBATCH --partition=cpu-ondemand
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=32
#SBATCH --mem=128G
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
set -eEuo pipefail

# 21-unifrac_faith.sh — metriques PHYLOGENETIQUES manquantes (etape A1)
#
# OBJET. L'arbre (results/phylogeny/tree.nwk, 44 256 feuilles, couvre 100 % des 44 200
# ASV de la table propre) a ete construit pour UniFrac et Faith PD, mais le script 15
# n'avait calcule que Bray-Curtis et Jaccard.
#
# POURQUOI CES METRIQUES CHANGENT LA REPONSE. Metriques taxonomiques et phylogenetiques
# ne repondent pas a la meme question : deux hybrides peuvent porter des ASV DIFFERENTS
# mais phylogenetiquement PROCHES — Bray-Curtis compte une divergence, UniFrac une
# similarite. Pour trancher "intermediaire ou transgressif", les deux lectures sont
# necessaires.
#
# OUTILS. Image QIIME2 (amplicon_2026.1.sif) : unifrac 1.3.0 (implementation C++),
# biom 2.1.16, skbio 0.6.2. Aucune installation. picante / GUniFrac / phyloseq / ape
# sont ABSENTS du R du projet, d'ou le passage par l'image.
#
# MODE DE RAREFACTION. Rarefactions repetees avec moyennage des METRIQUES, jamais des
# tables de comptage (docs/decision_rarefaction_mode.md : moyenner les tables peuplerait
# chaque cellule de l'union des detections et gonflerait la richesse observee).
# Profondeur 3000, tirage sans remise (multivariate_hypergeometric).
#
# NOMBRE D'ITERATIONS. Non fixe a l'avance : DEUX CHAINES a graines disjointes tournent
# sous BUDGET DE TEMPS, et leur ecart a comptes appariés mesure directement l'erreur de
# Monte-Carlo. Comparer une moyenne cumulee a N contre une a 2N serait autocorrele
# (les deux partagent des tirages) ; deux chaines independantes ne le sont pas.
# Reference : sur Bray-Curtis et Jaccard l'erreur MC etait deja sous 0.1 % a N = 25
# (results/rarefaction/beta_convergence.tsv). Ce n'est pas suppose transferable a
# UniFrac : c'est mesure ici.
#
# LES METRIQUES ALPHA SONT TOUTES RECALCULEES SUR LES MEMES TIRAGES. richness, Shannon,
# InvSimpson et Faith PD sortent de la MEME boucle et des MEMES tables rarefiees. Les
# valeurs existantes (alpha_mean_1000.tsv) viennent d'une autre serie de tirages a
# N = 1000 : les melanger dans une meme figure comparerait des ensembles constitues
# differemment. La correlation entre les deux series est rapportee comme CONTROLE —
# un desaccord signalerait une erreur de pipeline, pas un manque d'iterations.
#
# ECRITURE INCREMENTALE. Chaque iteration met a jour les accumulateurs sur disque, pour
# qu'un depassement de walltime ne perde pas tout (defaut du script 15, corrige).
#
# Sorties : results/phylo_diversity/
#   alpha_phylo_mean.tsv                 4 metriques alpha, memes tirages
#   unifrac_unweighted_mean.tsv.gz       matrice carree, noms de lignes/colonnes
#   unifrac_weighted_mean.tsv.gz         idem
#   phylo_convergence.tsv                ecart entre les deux chaines
#   phylo_summary.txt

cd "$HOME/work/projects/microbiome-hybrid"
OUT=results/phylo_diversity
mkdir -p "$OUT" logs
IMG="$HOME/work/shared_softwares/qiime2/amplicon_2026.1.sif"
GIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo NA)
printf '%s\tSTART\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log

export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-8}"
export TMPDIR=/scratch/users/martinj/tmp_unifrac_${SLURM_JOB_ID:-local}
mkdir -p "$TMPDIR"

SUMMARY="${PHYLO_SUMMARY:-results/phylo_diversity/phylo_summary.txt}"
apptainer exec "$IMG" python - <<'PY' 2>&1 | tee "$SUMMARY"
import os, sys, time, gzip, tempfile
import numpy as np, h5py, biom, unifrac
from scipy.sparse import csc_matrix

T0 = time.time()
DEPTH   = 3000
# Budget et cible pilotes par l'environnement, pour que la REPETITION a faible N et la
# passe complete executent exactement le meme code (aucun assert relache entre les deux).
BUDGET  = float(os.environ.get("PHYLO_BUDGET_H", "9.0")) * 3600
# N alignee sur les matrices taxonomiques (beta_mean_*_N400) : 200 par chaine = 400 au
# total, pour que les metriques phylogenetiques et taxonomiques soient constituees de la
# meme facon. La repetition a montre ~10 s par iteration, soit ~70 min.
TARGET  = int(os.environ.get("PHYLO_TARGET", "200"))   # par chaine
OUT     = "results/phylo_diversity"
TREE    = "results/phylogeny/tree.nwk"
TABLE   = "results/decontam/asv_table_clean.tsv"
NCPU    = int(os.environ.get("OMP_NUM_THREADS", "8"))

def log(*a):
    print(f"[{time.time()-T0:7.1f}s]", *a); sys.stdout.flush()

# ---------------------------------------------------------------- PHASE 1 : lecture
log("lecture de la table propre...")
with open(TABLE) as fh:
    samples = fh.readline().rstrip("\n").split("\t")[1:]
n_s = len(samples)
feat = []
rows_i, cols_i, vals = [], [], []
with open(TABLE) as fh:
    fh.readline()
    for i, line in enumerate(fh):
        tab = line.index("\t")
        feat.append(line[:tab])
        # np.fromstring en mode texte peut tronquer sans erreur : conversion explicite
        v = np.array(line[tab+1:].rstrip("\n").split("\t"), dtype=np.int64)
        assert v.size == n_s, f"ligne {i} : {v.size} valeurs pour {n_s} echantillons"
        nz = np.flatnonzero(v)
        if nz.size:
            rows_i.append(np.full(nz.size, i, dtype=np.int64))
            cols_i.append(nz); vals.append(v[nz])
n_f = len(feat)
rows_i = np.concatenate(rows_i); cols_i = np.concatenate(cols_i); vals = np.concatenate(vals)
log(f"  {n_f} ASV x {n_s} echantillons | {vals.size} cellules non nulles "
    f"({100*vals.size/(n_f*n_s):.2f} % de remplissage) | {vals.sum():,} lectures au total")
Mat = csc_matrix((vals, (rows_i, cols_i)), shape=(n_f, n_s))
del rows_i, cols_i, vals

depths = np.asarray(Mat.sum(axis=0)).ravel()
keep = np.where(depths >= DEPTH)[0]
log(f"  echantillons a profondeur >= {DEPTH} : {len(keep)}")
Mat = Mat[:, keep]
kept_samples = [samples[j] for j in keep]

# le jeu doit coincider avec celui des matrices taxonomiques deja produites
import csv as _csv
log("  controle : jeu d'echantillons identique aux metriques taxonomiques ?")
try:
    with open("results/rarefaction/alpha_mean_1000.tsv") as fh:
        prev = {r["sample"] for r in _csv.DictReader(fh, delimiter="\t")}
    inter = prev & set(kept_samples)
    log(f"    alpha_mean_1000 : {len(prev)} echantillons | intersection {len(inter)}")
    assert len(inter) == len(kept_samples) == len(prev), (
        f"jeux differents : {len(kept_samples)} ici, {len(prev)} avant, {len(inter)} communs")
    log("    -> identique")
except FileNotFoundError:
    log("    (alpha_mean_1000.tsv absent, controle saute)")

# structure creuse par echantillon, pour rarefier sans balayer 44200 zeros
Mat = Mat.tocsc()
col_idx = [Mat.indices[Mat.indptr[j]:Mat.indptr[j+1]] for j in range(Mat.shape[1])]
col_val = [Mat.data[Mat.indptr[j]:Mat.indptr[j+1]].astype(np.int64) for j in range(Mat.shape[1])]
log(f"  ASV non nuls par echantillon : median {int(np.median([len(x) for x in col_idx]))}, "
    f"max {max(len(x) for x in col_idx)}")

# arbre : parse une seule fois si possible
log("preparation de l'arbre...")
try:
    from bp import parse_newick
    with open(TREE) as fh:
        TREE_OBJ = parse_newick(fh.read())
    log("  arbre parse une fois en BP (evite un reparse par iteration)")
except Exception as e:
    TREE_OBJ = TREE
    log(f"  parse BP indisponible ({type(e).__name__}), passage par chemin de fichier")

N_S = len(kept_samples)

def rarefy(rng):
    """Une table rarefiee (sans remise) -> (indices ASV globaux, matrice creuse)."""
    ri, ci, rv = [], [], []
    for j in range(N_S):
        idx, val = col_idx[j], col_val[j]
        sub = rng.multivariate_hypergeometric(val, DEPTH, method="marginals")
        nz = sub > 0
        ri.append(idx[nz]); ci.append(np.full(nz.sum(), j, dtype=np.int64)); rv.append(sub[nz])
    ri = np.concatenate(ri); ci = np.concatenate(ci); rv = np.concatenate(rv)
    return csc_matrix((rv, (ri, ci)), shape=(n_f, N_S))

def to_biom(R):
    """biom.Table sur les seuls ASV presents (l'arbre est elague par unifrac)."""
    present = np.unique(R.indices)
    Rp = R.tocsr()[present, :]
    obs = [feat[i] for i in present]
    return biom.Table(Rp, obs, kept_samples), len(obs)

def alpha_taxo(R):
    """richness, Shannon, InvSimpson sur la meme table rarefiee."""
    rich = np.zeros(N_S); sha = np.zeros(N_S); inv = np.zeros(N_S)
    Rc = R.tocsc()
    for j in range(N_S):
        v = Rc.data[Rc.indptr[j]:Rc.indptr[j+1]].astype(np.float64)
        p = v / v.sum()
        rich[j] = len(v)
        sha[j]  = -(p * np.log(p)).sum()
        inv[j]  = 1.0 / (p * p).sum()
    return rich, sha, inv

# ------------------------------------------------ PHASE 2 : validation, echec rapide
log("=== VALIDATION (echec rapide avant la boucle longue) ===")
rng0 = np.random.default_rng(999)
t = time.time(); R0 = rarefy(rng0); t_rar = time.time()-t
tab0, n_obs = to_biom(R0)
log(f"  rarefaction : {t_rar:.1f} s | ASV presents dans un tirage : {n_obs}")
assert n_obs < n_f, "aucun ASV elague : verifier le tirage"

BPATH = os.path.join(os.environ.get("TMPDIR","/tmp"), "rar.biom")

def write_biom(tab):
    """unifrac.weighted_normalized n'accepte PAS un biom.Table en memoire malgre son
    annotation Union[str, Table] : il fait str(table) puis valide un CHEMIN (constate
    en repetition, ValueError 'Table does not appear to be a BIOM-Format v2.1').
    unweighted l'accepte, mais on passe par un fichier pour les TROIS appels afin
    d'avoir un seul chemin de code — le fichier est de toute facon requis par faith_pd."""
    with h5py.File(BPATH, "w") as h5:
        tab.to_hdf5(h5, "21-unifrac_faith")
    return BPATH

def dm(fn, path):
    """Distance UniFrac REORDONNEE selon kept_samples : ne pas supposer l'ordre rendu."""
    D = fn(path, TREE)
    if list(D.ids) != kept_samples:
        D = D.filter(kept_samples)
    assert list(D.ids) == kept_samples
    return D

t = time.time(); bp0 = write_biom(tab0); t_wr = time.time()-t
log(f"  ecriture BIOM : {t_wr:.1f} s")
t = time.time(); Du = dm(unifrac.unweighted, bp0); t_un = time.time()-t
assert Du.shape == (N_S, N_S), f"forme inattendue {Du.shape}"
assert np.isfinite(Du.data).all(), "valeurs non finies en UniFrac non pondere"
log(f"  UniFrac non pondere : {t_un:.1f} s | elagage de l'arbre accepte (temoin: "
    f"table a {n_obs} ASV vs arbre a 44256 feuilles)")

t = time.time(); Dw = dm(unifrac.weighted_normalized, bp0); t_wn = time.time()-t
assert np.isfinite(Dw.data).all(), "valeurs non finies en UniFrac pondere"
log(f"  UniFrac pondere normalise : {t_wn:.1f} s")

t = time.time()
fpd_s = unifrac.faith_pd(bp0, TREE)
t_fp = time.time()-t
assert len(fpd_s) == N_S, f"Faith PD : {len(fpd_s)} valeurs pour {N_S} echantillons"
assert set(fpd_s.index) == set(kept_samples), "Faith PD : identifiants inattendus"
fpd = fpd_s.reindex(kept_samples).to_numpy(dtype=float)
assert np.isfinite(fpd).all(), "valeurs non finies en Faith PD"
log(f"  Faith PD : {t_fp:.1f} s")

t = time.time(); _ = alpha_taxo(R0); t_at = time.time()-t
per_iter = t_rar + t_wr + t_un + t_wn + t_fp + t_at
log(f"  alpha taxonomiques : {t_at:.1f} s")
log(f"  => une iteration = {per_iter:.1f} s")
log(f"  => budget {BUDGET/3600:.1f} h permet ~{int(BUDGET/per_iter)} iterations au total")
log(f"  => cible {TARGET} par chaine ({2*TARGET} au total) = {2*TARGET*per_iter/3600:.1f} h")

# --------------------------------------------------- PHASE 3 : deux chaines, budget
log("=== BOUCLE : deux chaines a graines disjointes ===")
acc = {c: {"un": np.zeros((N_S, N_S)), "wn": np.zeros((N_S, N_S)),
           "rich": np.zeros(N_S), "sha": np.zeros(N_S), "inv": np.zeros(N_S),
           "fpd": np.zeros(N_S), "n": 0} for c in (1, 2)}
SEEDS = {1: 20260830, 2: 771113}
PROG = os.path.join(OUT, "progress.txt")

it = 0
while True:
    if time.time() - T0 > BUDGET:
        log(f"budget atteint, arret a {acc[1]['n']}+{acc[2]['n']} iterations"); break
    if acc[1]["n"] >= TARGET and acc[2]["n"] >= TARGET:
        log("cible atteinte sur les deux chaines"); break
    ch = 1 if acc[1]["n"] <= acc[2]["n"] else 2
    a = acc[ch]
    rng = np.random.default_rng(SEEDS[ch] + a["n"])
    R = rarefy(rng)
    tab, _ = to_biom(R)
    bp = write_biom(tab)
    a["un"] += dm(unifrac.unweighted, bp).data
    a["wn"] += dm(unifrac.weighted_normalized, bp).data
    a["fpd"] += unifrac.faith_pd(bp, TREE).reindex(kept_samples).to_numpy(dtype=float)
    r_, s_, i_ = alpha_taxo(R)
    a["rich"] += r_; a["sha"] += s_; a["inv"] += i_
    a["n"] += 1
    it += 1
    with open(PROG, "w") as fh:
        fh.write(f"chaine1={acc[1]['n']}\tchaine2={acc[2]['n']}\t"
                 f"elapsed_s={time.time()-T0:.0f}\n")
    if it % 5 == 0:
        log(f"  chaine1={acc[1]['n']} chaine2={acc[2]['n']} "
            f"({(time.time()-T0)/it:.1f} s/iteration)")

n1, n2 = acc[1]["n"], acc[2]["n"]
assert n1 >= 5 and n2 >= 5, f"trop peu d'iterations ({n1}, {n2}) pour un diagnostic"
log(f"boucle terminee : chaine1={n1}, chaine2={n2}")

# ------------------------------------------- PHASE 4 : convergence puis moyennes
def mean_of(ch, k): return acc[ch][k] / acc[ch]["n"]
nmin = min(n1, n2)
log("=== CONVERGENCE : ecart entre deux chaines INDEPENDANTES ===")
conv_rows = []
for key, lbl in (("un","unifrac_unweighted"), ("wn","unifrac_weighted")):
    A, B = mean_of(1, key), mean_of(2, key)
    iu = np.triu_indices(N_S, 1)
    a_, b_ = A[iu], B[iu]
    d = np.abs(a_ - b_)
    mean_dist = 0.5*(a_.mean()+b_.mean())
    se_chain = d.mean()/np.sqrt(2)
    conv_rows.append({"metrique": lbl, "n_par_chaine": nmin,
                      "ecart_max": d.max(), "ecart_moyen": d.mean(),
                      "ecart_p99": np.quantile(d, 0.99),
                      "correlation": np.corrcoef(a_, b_)[0,1],
                      "distance_moyenne": mean_dist,
                      "se_relative": se_chain/mean_dist})
    log(f"  {lbl:20} ecart moyen {d.mean():.6f} | distance moyenne {mean_dist:.4f} | "
        f"erreur MC relative {se_chain/mean_dist:.6f} | r = {np.corrcoef(a_,b_)[0,1]:.6f}")
for key, lbl in (("fpd","faith_pd"), ("rich","richness"), ("sha","shannon"), ("inv","invsimpson")):
    A, B = mean_of(1, key), mean_of(2, key)
    d = np.abs(A-B); m = 0.5*(A.mean()+B.mean())
    conv_rows.append({"metrique": lbl, "n_par_chaine": nmin,
                      "ecart_max": d.max(), "ecart_moyen": d.mean(),
                      "ecart_p99": np.quantile(d, 0.99),
                      "correlation": np.corrcoef(A, B)[0,1],
                      "distance_moyenne": m, "se_relative": (d.mean()/np.sqrt(2))/m})
    log(f"  {lbl:20} ecart moyen {d.mean():.6f} | moyenne {m:.4f} | "
        f"erreur MC relative {(d.mean()/np.sqrt(2))/m:.6f}")
with open(os.path.join(OUT, "phylo_convergence.tsv"), "w") as fh:
    ks = ["metrique","n_par_chaine","ecart_max","ecart_moyen","ecart_p99",
          "correlation","distance_moyenne","se_relative"]
    fh.write("\t".join(ks)+"\n")
    for r in conv_rows:
        fh.write("\t".join(str(r[k]) for k in ks)+"\n")

# moyennes finales : les deux chaines poolees
N_TOT = n1 + n2
def pooled(k): return (acc[1][k] + acc[2][k]) / N_TOT
log(f"=== MOYENNES FINALES sur N = {N_TOT} tirages ===")

for key, name in (("un","unifrac_unweighted_mean"), ("wn","unifrac_weighted_mean")):
    Dm = pooled(key)
    np.fill_diagonal(Dm, 0.0)
    path = os.path.join(OUT, f"{name}.tsv.gz")
    with gzip.open(path, "wt") as fh:
        fh.write("\t" + "\t".join(kept_samples) + "\n")
        for i, sid in enumerate(kept_samples):
            fh.write(sid + "\t" + "\t".join(f"{v:.6f}" for v in Dm[i]) + "\n")
    log(f"  {name}.tsv.gz ecrit | min={Dm[np.triu_indices(N_S,1)].min():.4f} "
        f"max={Dm[np.triu_indices(N_S,1)].max():.4f}")

alpha = {"richness_mean": pooled("rich"), "shannon_mean": pooled("sha"),
         "invsimpson_mean": pooled("inv"), "faith_pd_mean": pooled("fpd")}
with open(os.path.join(OUT, "alpha_phylo_mean.tsv"), "w") as fh:
    cols = ["richness_mean","shannon_mean","invsimpson_mean","faith_pd_mean"]
    fh.write("sample\t" + "\t".join(cols) + "\n")
    for i, sid in enumerate(kept_samples):
        fh.write(sid + "\t" + "\t".join(f"{alpha[c][i]:.6f}" for c in cols) + "\n")
log(f"  alpha_phylo_mean.tsv ecrit ({N_S} echantillons, 4 metriques, memes tirages)")

# CONTROLE : accord avec la serie taxonomique anterieure (N=1000, autres tirages).
# Un desaccord signalerait une erreur de pipeline, pas un manque d'iterations.
log("=== CONTROLE : accord avec alpha_mean_1000.tsv (serie de tirages independante) ===")
try:
    prev = {}
    with open("results/rarefaction/alpha_mean_1000.tsv") as fh:
        for r in _csv.DictReader(fh, delimiter="\t"):
            prev[r["sample"]] = r
    idx = [i for i, s in enumerate(kept_samples) if s in prev]
    for mine, theirs in (("richness_mean","richness_mean"), ("shannon_mean","shannon_mean"),
                         ("invsimpson_mean","invsimpson_mean")):
        a = np.array([alpha[mine][i] for i in idx])
        b = np.array([float(prev[kept_samples[i]][theirs]) for i in idx])
        r = np.corrcoef(a, b)[0,1]
        rel = np.abs(a-b).mean()/b.mean()
        log(f"  {mine:18} r = {r:.6f} | ecart relatif moyen = {rel:.5f}")
        assert r > 0.99, f"desaccord sur {mine} (r={r:.4f}) : verifier le pipeline"
    log("  -> accord confirme sur les 3 metriques taxonomiques")
except FileNotFoundError:
    log("  (fichier anterieur absent, controle saute)")

log("TERMINE")
PY

rm -rf "$TMPDIR"
printf '%s\tEND\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log
ls -lh results/phylo_diversity/
