#!/usr/bin/env python3
"""33-alpha_categorie.py — test (c) de docs/plan_tests_2026-10-03.md (declare a priori, commit bd6ba3d).

Effet de la categorie genotypique sur la diversite alpha (H1 : intermediaire, dominant, transgressif),
quatre indices (richesse, Shannon, inverse Simpson, Faith PD), passes 1 et 2, par tissu.
Donnees : moyenne par individu x tissu sur les runs des valeurs > 0 (comme scripts/29), puis log.
Modeles MCO : principal log(x) ~ station + cat ; sensibilite log(x) ~ station + pos + cat.
Test F emboite pour cat ; contrastes Hy-Cn, Hy-Pt, Hy-(Cn+Pt)/2 avec IC 95 %.
Classement (precise avant calcul, cf. note du plan) : un seul critere satisfait -> classe ; plusieurs
ou aucun -> indetermine. A lancer depuis la racine du depot. Variable TESTS_OUTDIR.
Python systeme (/usr/bin/python3 : numpy, scipy, pandas).
"""
import os, sys
import numpy as np, pandas as pd
from scipy import stats

OUT = os.path.join(os.environ.get("TESTS_OUTDIR", "results/tests_20261003"), "alpha_categorie")
os.makedirs(OUT, exist_ok=True)
IDX = {"richness_mean": ("richesse observee", False), "shannon_mean": ("Shannon", True),
       "invsimpson_mean": ("inverse Simpson", True), "faith_pd_mean": ("Faith PD", False)}
md = pd.read_csv("metadata/analysis_metadata.csv")
for c in ("dada2_id", "individual_id", "tissue", "station", "categorie", "col_rank_station", "inclus_passe1"):
    assert c in md.columns, c
al = pd.read_csv("results/phylo_diversity/alpha_phylo_mean.tsv", sep="\t")
assert set(IDX) <= set(al.columns) and "sample" in al.columns
d = al.merge(md, left_on="sample", right_on="dada2_id", how="inner")
print("echantillons alpha joints :", len(d), "sur", len(al))

def ols(y, X):
    b, *_ = np.linalg.lstsq(X, y, rcond=None); r = y - X @ b
    df = len(y) - np.linalg.matrix_rank(X); s2 = float(r @ r) / df
    return b, s2, df, float(r @ r)

rows = []
for passe in ("1", "2"):
    dp = d if passe == "2" else d[d.inclus_passe1.astype(str).isin(["True", "TRUE"])]
    for col, (nice, pond) in IDX.items():
        v = dp[dp[col] > 0]
        g = v.groupby(["individual_id", "tissue"]).agg(x=(col, "mean"), station=("station", "first"),
                                                         cat=("categorie", "first"), pos=("col_rank_station", "first")).reset_index()
        for tis, s in g.groupby("tissue"):
            s = s.copy(); s["y"] = np.log(s.x)
            cats = sorted(s["cat"].unique())
            if set(cats) != {"Cn", "Hy", "Pt"}:
                continue
            St = pd.get_dummies(s.station, drop_first=True, dtype=float).values
            C = np.column_stack([(s["cat"] == "Hy").astype(float), (s["cat"] == "Pt").astype(float)])
            one = np.ones((len(s), 1)); P = s[["pos"]].astype(float).values
            for modele, base in (("principal_station_cat", np.hstack([one, St])),
                                 ("sensibilite_station_pos_cat", np.hstack([one, St, P]))):
                X0 = base; X1 = np.hstack([base, C])
                b1, s2, df1, rss1 = ols(s.y.values, X1); _, _, df0, rss0 = ols(s.y.values, X0)
                k = df0 - df1
                F = ((rss0 - rss1) / k) / (rss1 / df1) if k > 0 else np.nan
                pF = float(stats.f.sf(F, k, df1)) if k > 0 else np.nan
                XtXi = np.linalg.pinv(X1.T @ X1); jH, jP = X1.shape[1] - 2, X1.shape[1] - 1
                def con(cvec):
                    c = np.zeros(X1.shape[1]); [c.__setitem__(j, w) for j, w in cvec]
                    est = float(c @ b1); se = float(np.sqrt(s2 * c @ XtXi @ c)); q = stats.t.ppf(0.975, df1)
                    return est, est - q * se, est + q * se
                hc = con([(jH, 1)]); hp = con([(jH, 1), (jP, -1)]); hm = con([(jH, 1), (jP, -0.5)])
                bH, bP = b1[jH], b1[jP]; lo, hi = min(0.0, bP), max(0.0, bP)
                inc0 = lambda ci: ci[1] <= 0 <= ci[2]
                crit = []
                if lo <= bH <= hi and inc0(hm): crit.append("intermediaire")
                if inc0(hc) and not inc0(hp): crit.append("dominant Cn")
                if inc0(hp) and not inc0(hc): crit.append("dominant Pt")
                if bH > hi:
                    near = hc if hi == 0.0 else hp
                    if near[1] > 0: crit.append("transgressif")
                if bH < lo:
                    near = hc if lo == 0.0 else hp
                    if near[2] < 0: crit.append("transgressif")
                classe = crit[0] if len(crit) == 1 else "indetermine" + (" (" + "/".join(crit) + ")" if crit else "")
                rows.append(dict(passe=passe, tissu=tis, indice=nice, ponderee=pond, modele=modele, n=len(s),
                                 n_Cn=int((s["cat"] == "Cn").sum()), n_Hy=int((s["cat"] == "Hy").sum()), n_Pt=int((s["cat"] == "Pt").sum()),
                                 F_cat=F, p_cat=pF, Pt_moins_Cn=float(bP),
                                 Hy_moins_Cn=hc[0], Hy_moins_Cn_bas=hc[1], Hy_moins_Cn_haut=hc[2],
                                 Hy_moins_Pt=hp[0], Hy_moins_Pt_bas=hp[1], Hy_moins_Pt_haut=hp[2],
                                 Hy_moins_milieu=hm[0], Hy_moins_milieu_bas=hm[1], Hy_moins_milieu_haut=hm[2],
                                 criteres="/".join(crit), classe=classe))
res = pd.DataFrame(rows)
res.to_csv(os.path.join(OUT, "alpha_categorie.tsv"), sep="\t", index=False, float_format="%.6g")
print(res[res.modele == "principal_station_cat"][["passe", "tissu", "indice", "n", "p_cat", "classe"]].to_string(index=False))
print("ecrit :", os.path.join(OUT, "alpha_categorie.tsv"), len(res), "lignes")
