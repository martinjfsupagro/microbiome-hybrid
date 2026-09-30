#!/usr/bin/env python3
"""D7 — de quelles conclusions le choix de metrique decide-t-il ?
Volet composition : synthese des tables deja calculees (results/recat/{1,2}), aucun recalcul.
Volet alpha : recalcul des contrastes sur les quatre indices (richesse, Shannon, inverse Simpson,
Faith PD), les diagnostics anterieurs ne portant que sur la richesse ASV observee.
A lancer depuis la racine du depot."""
import csv, collections, math, os, sys
import numpy as np
from scipy import stats

ALPHA = 0.05   # seuil STRICT (p < ALPHA), convention du depot : la cellule passe 2 /
               # UniFrac non pondere / hindgut a un p exactement egal a 0,05 sur durance2,
               # comptee non significative par docs/recalcul/note_recalcul_2passes.md
OUT = "results/d7_metriques"
os.makedirs(OUT, exist_ok=True)
NICE = {"bray":"Bray-Curtis","jaccard":"Jaccard",
        "unifrac_unweighted":"UniFrac non pondere","unifrac_weighted":"UniFrac pondere"}
PONDEREE = {"bray":True,"jaccard":False,"unifrac_unweighted":False,"unifrac_weighted":True}

def tsv(p):
    with open(p, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))

# ===================================================================== A. composition
cat_rows, disp_rows = [], []
for passe in ("1","2"):
    r = tsv("results/recat/%s/var_partition_cat/category_partition.tsv" % passe)
    sel = [x for x in r if x["sous_ensemble"]=="complet"
           and x["modele"]=="cat_apres_pos_station_bloquee" and x["terme"]=="cat"]
    g = collections.defaultdict(list)
    for x in sel: g[(x["metrique"], x["tissu"])].append(x)
    brack = collections.defaultdict(list)
    for x in r:
        if x["sous_ensemble"]=="complet" and x["terme"]=="cat" and x["modele"] in (
                "ordre_MIN_pos_st_cat","ordre_MAX_cat_st_pos"):
            brack[(x["metrique"], x["tissu"], x["modele"])].append(float(x["R2"]))
    for (m,t), xs in sorted(g.items()):
        ps = sorted(float(x["p"]) for x in xs)
        nsig = sum(1 for p in ps if p < ALPHA)
        klass = "robuste 3/3" if nsig==len(ps) and len(ps)==3 else ("aucun" if nsig==0 else "partiel")
        lo = brack.get((m,t,"ordre_MIN_pos_st_cat"), [float("nan")])
        hi = brack.get((m,t,"ordre_MAX_cat_st_pos"), [float("nan")])
        cat_rows.append({"passe":passe,"metrique":NICE[m],"ponderee_abondance":PONDEREE[m],
                         "tissu":t,"n_runs":len(ps),"n_significatifs":nsig,"classe":klass,
                         "p_par_run":";".join("%.3f"%p for p in ps),
                         "R2_min_ordre":round(float(np.nanmedian(lo)),4),
                         "R2_max_ordre":round(float(np.nanmedian(hi)),4)})

    d = tsv("results/recat/%s/permdisp/permdisp.tsv" % passe)
    for x in [y for y in d if y["dispositif"]=="global_station_bloquee"]:
        dd = {k: float(x["dist_"+k]) for k in ("Cn","Hy","Pt")}
        par = (dd["Cn"]+dd["Pt"])/2
        disp_rows.append({"passe":passe,"metrique":NICE[x["metrique"]],
                          "ponderee_abondance":PONDEREE[x["metrique"]],
                          "tissu":x["tissu"],"run":x["run"],"p":float(x["p"]),
                          "hy_moins_disperse": dd["Hy"] < min(dd["Cn"],dd["Pt"]),
                          "hy_plus_disperse":  dd["Hy"] > max(dd["Cn"],dd["Pt"]),
                          "ecart_Hy_moins_parentaux": round(dd["Hy"]-par,4)})

for name, rows in (("composition_categorie",cat_rows),("composition_permdisp",disp_rows)):
    with open("%s/%s.tsv"%(OUT,name),"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,delimiter="\t",fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

# ===================================================================== B. alpha
meta = {r["dada2_id"]: r for r in csv.DictReader(open("metadata/analysis_metadata.csv", encoding="utf-8"))}
sexe = {r["individual_id"]: r["sexe"]
        for r in csv.DictReader(open("metadata/genotypes_verifies_sept_180.csv", encoding="utf-8"))}
alpha = tsv("results/phylo_diversity/alpha_phylo_mean.tsv")
IDX = {"richness_mean":"richesse observee","shannon_mean":"Shannon",
       "invsimpson_mean":"inverse Simpson","faith_pd_mean":"Faith PD"}
PONDEREE_A = {"richesse observee":False,"Shannon":True,"inverse Simpson":True,"Faith PD":False}

tis = collections.Counter(meta[a["sample"]]["tissue"] for a in alpha if a["sample"] in meta)
EXT = {t for t in tis if t.lower() in ("caudale","branchie","caudal fin","gill","peau")}
INT = {t for t in tis if t.lower() in ("midgut","hindgut")}
assert EXT and INT and EXT|INT == set(tis), (tis, EXT, INT)

# moyenne sur les runs, par (individu, tissu)
val = collections.defaultdict(lambda: collections.defaultdict(list))
for a in alpha:
    m = meta.get(a["sample"])
    if m is None: continue
    for col in IDX:
        v = float(a[col])
        if v > 0: val[(m["individual_id"], m["tissue"])][col].append(v)
mean = {k: {c: float(np.mean(v)) for c, v in d.items()} for k, d in val.items()}
indiv = sorted({k[0] for k in mean})

def paired(col, pick_a, pick_b):
    xa, xb = [], []
    for i in indiv:
        a = [mean[(i,t)][col] for t in pick_a if (i,t) in mean and col in mean[(i,t)]]
        b = [mean[(i,t)][col] for t in pick_b if (i,t) in mean and col in mean[(i,t)]]
        if a and b: xa.append(np.mean(a)); xb.append(np.mean(b))
    la, lb = np.log(xa), np.log(xb)
    t, p = stats.ttest_rel(la, lb)
    w, pw = stats.wilcoxon(la, lb)
    return dict(n=len(xa), ratio=round(float(np.exp(np.mean(la-lb))),3),
                ic_bas=round(float(np.exp(np.mean(la-lb)-1.96*np.std(la-lb,ddof=1)/math.sqrt(len(xa)))),3),
                ic_haut=round(float(np.exp(np.mean(la-lb)+1.96*np.std(la-lb,ddof=1)/math.sqrt(len(xa)))),3),
                p_apparie=float(p), p_wilcoxon=float(pw))

alpha_rows = []
for col, nice in IDX.items():
    for lab, a, b in (("externe / interne", EXT, INT),
                      ("midgut / hindgut", {"midgut"}, {"hindgut"})):
        r = paired(col, a, b)
        r.update(indice=nice, ponderee_abondance=PONDEREE_A[nice], contraste=lab)
        alpha_rows.append(r)
    # dimorphisme sexuel, par compartiment, non apparie
    for lab, grp in (("externe", EXT), ("interne", INT)):
        F = [np.mean([mean[(i,t)][col] for t in grp if (i,t) in mean])
             for i in indiv if sexe.get(i)=="F" and any((i,t) in mean for t in grp)]
        M = [np.mean([mean[(i,t)][col] for t in grp if (i,t) in mean])
             for i in indiv if sexe.get(i)=="M" and any((i,t) in mean for t in grp)]
        u, p = stats.mannwhitneyu(F, M)
        alpha_rows.append(dict(indice=nice, ponderee_abondance=PONDEREE_A[nice],
                               contraste="femelles / males, %s" % lab,
                               n=len(F)+len(M), ratio=round(float(np.mean(F)/np.mean(M)),3),
                               ic_bas=float("nan"), ic_haut=float("nan"),
                               p_apparie=float("nan"), p_wilcoxon=float(p)))

with open("%s/alpha_par_indice.tsv"%OUT,"w",newline="",encoding="utf-8") as f:
    cols=["indice","ponderee_abondance","contraste","n","ratio","ic_bas","ic_haut","p_apparie","p_wilcoxon"]
    w=csv.DictWriter(f,delimiter="\t",fieldnames=cols); w.writeheader()
    for r in alpha_rows: w.writerow({k:r.get(k,"") for k in cols})

# ===================================================================== C. resume
with open("%s/resume.txt"%OUT,"w",encoding="utf-8") as f:
    def say(*a): print(*a); print(*a, file=f)
    say("individus avec au moins un tissu exploitable :", len(indiv))
    say("compartiments externes :", sorted(EXT), "| internes :", sorted(INT))
    say()
    say("--- ALPHA : contrastes par indice ---")
    for r in alpha_rows:
        say("%-18s %-26s n=%4d  ratio=%6.3f  p=%.2e%s" %
            (r["indice"], r["contraste"], r["n"], r["ratio"],
             r["p_wilcoxon"], "  [pondere]" if r["ponderee_abondance"] else ""))
    say()
    say("--- COMPOSITION : classe du terme categorie, test conservateur ---")
    for passe in ("1","2"):
        for m in ("Bray-Curtis","Jaccard","UniFrac non pondere","UniFrac pondere"):
            xs=[x for x in cat_rows if x["passe"]==passe and x["metrique"]==m]
            say("passe %s  %-20s %s" % (passe, m,
                "  ".join("%s:%s(%d/%d)"%(x["tissu"],x["classe"].split()[0],
                                          x["n_significatifs"],x["n_runs"]) for x in xs)))
    say()
    say("--- PERMDISP : sens de la dispersion hybride, dispositif station bloquee ---")
    for m in ("Bray-Curtis","Jaccard","UniFrac non pondere","UniFrac pondere"):
        xs=[x for x in disp_rows if x["metrique"]==m]
        moins=sum(1 for x in xs if x["hy_moins_disperse"]); plus=sum(1 for x in xs if x["hy_plus_disperse"])
        sig=sum(1 for x in xs if x["p"]<ALPHA)
        say("%-20s Hy le moins disperse %2d/%2d, le plus %2d/%2d, ecart median %+0.4f, tests significatifs %d"
            % (m, moins, len(xs), plus, len(xs),
               float(np.median([x["ecart_Hy_moins_parentaux"] for x in xs])), sig))
print("\necrit dans", OUT)
