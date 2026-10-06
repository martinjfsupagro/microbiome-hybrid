#!/usr/bin/env python3
"""51-alpha_ordre.py — test R31 de docs/plan_R31_ordre_2026-10-06.md (déclaré a priori, commité avant calcul).

La dominance de C. nasus en diversité alpha (R31 : caudale passe 1, midgut passe 2) peut-elle être produite
par l'ordre de traitement des poissons ? Témoin intra-cellule (station x catégorie) de la pente du rang,
comparé à la pente requise pour produire l'écart Hy - Pt observé.

Données et modèle principal identiques à scripts/33-alpha_categorie.py ; contrôle de reproduction bloquant
contre results/tests_20261003/alpha_categorie/alpha_categorie.tsv. Lancer depuis la racine du dépôt.
Variable TESTS_OUTDIR (défaut results/tests_20261006). Python système (/usr/bin/python3).
"""
import os
import numpy as np, pandas as pd
from scipy import stats

OUT = os.path.join(os.environ.get("TESTS_OUTDIR", "results/tests_20261006"), "alpha_ordre")
os.makedirs(OUT, exist_ok=True)
REF = "results/tests_20261003/alpha_categorie/alpha_categorie.tsv"
IDX = {"richness_mean": ("richesse observee", False), "shannon_mean": ("Shannon", True),
       "invsimpson_mean": ("inverse Simpson", True), "faith_pd_mean": ("Faith PD", False)}

md = pd.read_csv("metadata/analysis_metadata.csv")
for c in ("dada2_id", "individual_id", "individual", "annee", "tissue", "station", "categorie", "inclus_passe1"):
    assert c in md.columns, c
al = pd.read_csv("results/phylo_diversity/alpha_phylo_mean.tsv", sep="\t")
assert set(IDX) <= set(al.columns) and "sample" in al.columns
d = al.merge(md, left_on="sample", right_on="dada2_id", how="inner")
print("echantillons alpha joints :", len(d), "sur", len(al))

# ── rang de traitement ───────────────────────────────────────────────────────────────────────
ind = md.drop_duplicates("individual_id")[["individual_id", "station", "annee", "individual"]].copy()
ind["individual"] = ind.individual.astype(int)
sa = ind.station + "_" + ind.annee.astype(str)
per14 = (ind.station == "Pertuis") & (ind.annee.astype(int) == 2014)
assert set(ind.loc[per14, "individual"] // 1000) == {1, 2}, "series de Pertuis 2014 inattendues"
ind["camp"] = np.where(per14, sa + "_serie" + (ind.individual // 1000).astype(str), sa)   # 1011-1014 : 07/07 ; 2011-2015 : 20/08
ind["camp_agr"] = sa                                                                         # comme scripts/31
ind["rang"] = ind.groupby("camp").individual.rank(method="first")
ind["rang_agr"] = ind.groupby("camp_agr").individual.rank(method="first")
assert ind.camp.nunique() == 14 and ind.camp_agr.nunique() == 13, (ind.camp.nunique(), ind.camp_agr.nunique())
RANG = ind.set_index("individual_id")[["rang", "rang_agr"]]


def ols(y, X):
    b, *_ = np.linalg.lstsq(X, y, rcond=None); r = y - X @ b
    df = len(y) - np.linalg.matrix_rank(X); s2 = float(r @ r) / df
    return b, s2, df, float(r @ r)


def classify(y, base, C):
    """Règle du test (c), copiée de scripts/33 : test F de cat, contrastes, classement."""
    X0 = base; X1 = np.hstack([base, C])
    b1, s2, df1, rss1 = ols(y, X1); _, _, df0, rss0 = ols(y, X0)
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
    return classe, pF, hp


def within_slope(y, cell, r):
    """Pente du rang identifiée par la seule variation intra-cellule (effets fixes de cellule)."""
    X = np.hstack([pd.get_dummies(cell, dtype=float).values, r.reshape(-1, 1)])
    b, s2, df, _ = ols(y, X)
    se = float(np.sqrt(s2 * np.linalg.pinv(X.T @ X)[-1, -1])); q = stats.t.ppf(0.975, df)
    t = b[-1] / se
    return float(b[-1]), float(b[-1] - q * se), float(b[-1] + q * se), float(2 * stats.t.sf(abs(t), df)), int(df)


def contrast_rank(r, St, C):
    X = np.hstack([np.ones((len(r), 1)), St, C]); b, *_ = ols(r, X)
    return float(b[-2] - b[-1])                       # Hy - Pt


def verdict(dr, breq, lo, hi):
    if abs(dr) < 1: return "sans prise"
    if (breq > 0 and hi < breq) or (breq < 0 and lo > breq): return "insuffisant"
    if lo <= breq <= hi and not (lo <= 0 <= hi): return "suffisant"
    return "indetermine"


rows = []
for passe in ("1", "2"):
    dp = d if passe == "2" else d[d.inclus_passe1.astype(str).isin(["True", "TRUE"])]
    for col, (nice, pond) in IDX.items():
        v = dp[dp[col] > 0]
        g = v.groupby(["individual_id", "tissue"]).agg(x=(col, "mean"), station=("station", "first"),
                                                         cat=("categorie", "first")).reset_index()
        g = g.join(RANG, on="individual_id"); assert not g.rang.isna().any()
        for tis, s in g.groupby("tissue"):
            s = s.copy(); s["y"] = np.log(s.x)
            if set(s["cat"].unique()) != {"Cn", "Hy", "Pt"}:
                continue
            y = s.y.values
            St = pd.get_dummies(s.station, drop_first=True, dtype=float).values
            C = np.column_stack([(s["cat"] == "Hy").astype(float), (s["cat"] == "Pt").astype(float)])
            one = np.ones((len(s), 1))
            classe, pF, hp = classify(y, np.hstack([one, St]), C)                 # = R31, modèle principal
            da = hp[0]
            cell = (s.station + "|" + s["cat"]).values
            row = dict(passe=passe, tissu=tis, indice=nice, ponderee=pond, n=len(s),
                       n_Cn=int((s["cat"] == "Cn").sum()), n_Hy=int((s["cat"] == "Hy").sum()), n_Pt=int((s["cat"] == "Pt").sum()),
                       classe_principal=classe, p_cat=pF, delta_a_Hy_moins_Pt=da)
            for tag, rc in (("", "rang"), ("_agr", "rang_agr")):
                r = s[rc].values.astype(float)
                dr = contrast_rank(r, St, C)
                bw, lo, hi, pw, dfw = within_slope(y, cell, r)
                breq = da / dr if abs(dr) >= 1 else np.nan
                ca, pFa, _ = classify(y, np.hstack([one, St, r.reshape(-1, 1)]), C)
                row.update({f"delta_r_Hy_moins_Pt{tag}": dr, f"beta_req{tag}": breq, f"beta_w{tag}": bw,
                            f"beta_w_bas{tag}": lo, f"beta_w_haut{tag}": hi, f"p_beta_w{tag}": pw, f"df_w{tag}": dfw,
                            f"verdict{tag}": verdict(dr, breq, lo, hi) if classe == "dominant Cn" else "non applicable",
                            f"classe_ajustee_rang{tag}": ca, f"p_cat_ajuste{tag}": pFa})
            rows.append(row)
res = pd.DataFrame(rows)

# ── contrôle de reproduction (bloquant) ──────────────────────────────────────────────────────
ref = pd.read_csv(REF, sep="\t", dtype={"passe": str})
ref = ref[ref.modele == "principal_station_cat"][["passe", "tissu", "indice", "n", "classe"]]
m = res.merge(ref, on=["passe", "tissu", "indice"], how="outer", indicator=True, suffixes=("", "_ref"))
assert (m._merge == "both").all() and len(m) == 32, ("combinaisons", len(m), m._merge.value_counts().to_dict())
bad = m[(m.classe_principal != m.classe) | (m.n != m.n_ref)]
assert bad.empty, ("reproduction de R31 en echec", bad[["passe", "tissu", "indice", "classe_principal", "classe"]].to_dict("records"))
print("reproduction de R31 : 32/32 classements et effectifs identiques")

# ── lecture mécanique ────────────────────────────────────────────────────────────────────────
def d7(sub, col, ok):
    return bool(((sub.ponderee) & sub[col].isin(ok)).any() and ((~sub.ponderee) & sub[col].isin(ok)).any())

est = []
for (ps, tis), sub in res.groupby(["passe", "tissu"]):
    if d7(sub, "classe_principal", ["dominant Cn"]):
        est.append((ps, tis))
assert sorted(est) == [("1", "caudale"), ("2", "midgut")], ("classements etablis inattendus", est)

V = []
for ps, tis in est:
    sub = res[(res.passe == ps) & (res.tissu == tis) & (res.classe_principal == "dominant Cn")]
    for tag in ("", "_agr"):
        non = d7(sub, f"verdict{tag}", ["insuffisant", "sans prise"])
        oui = d7(sub, f"verdict{tag}", ["suffisant"])
        lec = ("dominance non attribuable a l'ordre" if non and not oui else
               "dominance attribuable a l'ordre (possible)" if oui and not non else "indeterminee")
        V.append(dict(passe=ps, tissu=tis, version="Pertuis 2014 scinde (principal)" if not tag else "Pertuis 2014 agrege (sensibilite)",
                      indices_dominant_Cn=len(sub),
                      verdicts="; ".join(f"{i}: {x}" for i, x in zip(sub.indice, sub[f"verdict{tag}"])),
                      lecture=lec))
V = pd.DataFrame(V)

eff = []
for tis, sub in res.groupby("tissu"):
    hit = False
    for ps, s2 in sub.groupby("passe"):
        sig = s2[s2.p_beta_w < 0.05]
        for sgn in (1, -1):
            ss = sig[np.sign(sig.beta_w) == sgn]
            if ss.ponderee.any() and (~ss.ponderee).any(): hit = True
    eff.append(dict(tissu=tis, n_sig=int((sub.p_beta_w < 0.05).sum()), n_tests=len(sub),
                    effet_ordre_etabli=hit))
E = pd.DataFrame(eff)

res.to_csv(os.path.join(OUT, "alpha_ordre.tsv"), sep="\t", index=False, float_format="%.6g")
V.to_csv(os.path.join(OUT, "verdicts.tsv"), sep="\t", index=False)
E.to_csv(os.path.join(OUT, "effet_ordre_par_tissu.tsv"), sep="\t", index=False)

with open(os.path.join(OUT, "lecture.md"), "w") as fh:
    fh.write("# Lecture mecanique du test R31 (plan docs/plan_R31_ordre_2026-10-06.md)\n\n")
    fh.write("Reproduction de R31 : 32/32 classements identiques.\n\n## Verdicts par classement\n\n")
    fh.write(V.to_string(index=False))
    fh.write("\n\n## Effet de l'ordre sur l'alpha, par tissu (descriptif)\n\n")
    fh.write(E.to_string(index=False))
    fh.write(f"\n\nTests beta_w significatifs (p < 0,05, bruts) : {int((res.p_beta_w < 0.05).sum())} / {len(res)} "
             f"(attendu sous H0 : {0.05 * len(res):.1f}).\n\n## Detail des combinaisons dominant Cn\n\n")
    cols = ["passe", "tissu", "indice", "n", "delta_a_Hy_moins_Pt", "delta_r_Hy_moins_Pt", "beta_req", "beta_w",
            "beta_w_bas", "beta_w_haut", "p_beta_w", "verdict", "classe_ajustee_rang"]
    fh.write(res[res.classe_principal == "dominant Cn"][cols].to_string(index=False, float_format=lambda x: f"{x:.4g}"))
    fh.write("\n")
print(open(os.path.join(OUT, "lecture.md")).read())
