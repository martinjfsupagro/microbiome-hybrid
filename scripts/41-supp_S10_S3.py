#!/usr/bin/env python3
"""41-supp_S10_S3.py — Table S10 et Figure S3 du supplément, PERMDISP corrigé (bias.adjust = TRUE).

Entrées (md5 vérifiés le 2026-10-05) :
  results/recat/{1,2}/permdisp_bias/permdisp.tsv   eae71c0e77214fcdce1aaec0c4fce3c1 / 1845ed4b1ee7536c86f49757e461ab72
  results/recat/{1,2}/permdisp/permdisp.tsv        a538187a3c5de87539cf8481ed338139 / 217572a3bd14ae6aea8294dc35947b34 (contrôle)
  results/recat/{1,2}/var_partition_cat/category_partition.tsv  2ef02204f0012f6ffbc049a6caad0f04 / 49155eda83539442342d3d29c1af28a3
Contrôle qui pouvait échouer : appliquée aux sorties NON corrigées, l'agrégation reproduit l'ancienne Table S10
(32 lignes sur 32, valeurs à 0,0006 près) — le code d'origine de la table n'avait pas été conservé.
Agrégation par passe × métrique × tissu : runs significatifs (p < 0,05) en station bloquée (x/3) ; tests
intra-station significatifs (x/k) ; médiane sur les 3 runs de la distance médiane de chaque catégorie à la
médiane spatiale de son groupe ; runs où Hy est la catégorie la plus dispersée.
Figure S3 : reprise du code du 2026-09-25 (artefact fig_S3_permdisp.png), données corrigées, titres recalculés,
palette des figures principales (Cn #2166ac, Hy #762a83, Pt #e08214).
Exécuté dans le bac à sable sur des copies des fichiers ci-dessus ; sorties déposées dans
docs/manuscrit/figures/fig_S3_permdisp.png et dans Supplementary_Data.docx (Table S10).
Usage : python3 41-supp_S10_S3.py DOSSIER_ENTREES   (fichiers pd_raw_{1,2}.tsv, pd_bias_{1,2}.tsv, cp_{1,2}.tsv)
"""
import sys
import numpy as np, pandas as pd

H = sys.argv[1] if len(sys.argv) > 1 else "."
MET = ["bray", "jaccard", "unifrac_unweighted", "unifrac_weighted"]
TIS = ["caudale", "branchie", "midgut", "hindgut"]
ML = {"bray": "Bray–Curtis", "jaccard": "Jaccard", "unifrac_unweighted": "unweighted UniFrac", "unifrac_weighted": "weighted UniFrac"}
TL = {"caudale": "caudal fin", "branchie": "gill", "midgut": "midgut", "hindgut": "hindgut"}
COLS = ["Pass", "Metric", "Tissue", "Significant, station-blocked", "Significant, within-station",
        "Median distance Cn", "Median distance Hy", "Median distance Pt", "Hy most dispersed"]

def table_s10(PD, english=True):
    out = []
    for p in "12":
        t = PD[p]; G = t[t.dispositif == "global_station_bloquee"]; I = t[t.dispositif == "intra_station"]
        for m in MET:
            for ti in TIS:
                g = G[(G.metrique == m) & (G.tissu == ti)]; i = I[(I.metrique == m) & (I.tissu == ti)]
                most = ((g.dist_Hy > g.dist_Cn) & (g.dist_Hy > g.dist_Pt)).sum()
                out.append([p, ML[m] if english else m, TL[ti] if english else ti,
                            f"{(g.p < 0.05).sum()}/{len(g)}", f"{(i.p < 0.05).sum()}/{len(i)}",
                            round(g.dist_Cn.median(), 3), round(g.dist_Hy.median(), 3), round(g.dist_Pt.median(), 3),
                            f"{most}/{len(g)}"])
    return pd.DataFrame(out, columns=COLS)


def fig_s3(PDB, CP, out="fig_S3_permdisp.png"):
    import matplotlib as mpl; mpl.use("Agg"); import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from scipy.stats import binomtest
    mpl.rcParams.update({"font.size": 8, "axes.titlesize": 8, "axes.labelsize": 7, "xtick.labelsize": 6,
                         "ytick.labelsize": 6, "legend.fontsize": 6, "axes.spines.top": False, "axes.spines.right": False})
    GREY = "#888888"; CAT = {"Cn": "#2166ac", "Hy": "#762a83", "Pt": "#e08214"}; PASSC = {"1": "#4d4d4d", "2": "#bdbdbd"}
    def prep(P):
        G = P[P.dispositif == "global_station_bloquee"].dropna(subset=["dist_Cn", "dist_Hy", "dist_Pt"]).copy()
        I = P[P.dispositif == "intra_station"].dropna(subset=["dist_Cn", "dist_Hy", "dist_Pt"]).copy()
        for D_ in (G, I):
            D_["hy_sup"] = (D_.dist_Hy > D_.dist_Cn) & (D_.dist_Hy > D_.dist_Pt)
            D_["hy_inf"] = (D_.dist_Hy < D_.dist_Cn) & (D_.dist_Hy < D_.dist_Pt)
        return G, I
    GI = {p: prep(PDB[p]) for p in "12"}
    fig = plt.figure(figsize=(7.2, 5.4)); gs = fig.add_gridspec(2, 2, width_ratios=[1.45, 1.0], hspace=0.75, wspace=0.35)
    rng = np.random.default_rng(3); axs = []
    TT = {"1": "Pass 1 (20 intermediate hybrids): hybrid median lowest in\nthree tissues, highest in the gill; all medians within ±0.01",
          "2": "Pass 2 (all 42 hybrids): same ordering; largest\ngap in the midgut (hybrids −0.018)"}
    for row, p in enumerate("12"):
        ax = fig.add_subplot(gs[row, 0], sharey=axs[0] if axs else None); axs.append(ax); G = GI[p][0]
        for i, t in enumerate(TIS):
            s = G[G.tissu == t]; mm = s[["dist_Cn", "dist_Hy", "dist_Pt"]].mean(axis=1)
            for j, cc in enumerate(["Cn", "Hy", "Pt"]):
                vals = (s["dist_" + cc] - mm).values; x = i + (j - 1) * 0.26 + (rng.random(len(vals)) - 0.5) * 0.10
                ax.scatter(x, vals, s=10, color=CAT[cc], alpha=0.85, edgecolor="none",
                           label=({"Cn": "C. nasus", "Hy": "hybrids", "Pt": "P. toxostoma"}[cc] if i == 0 else None))
                ax.plot([i + (j - 1) * 0.26 - 0.09, i + (j - 1) * 0.26 + 0.09], [np.median(vals)] * 2, color="black", lw=1.2, zorder=5)
        ax.axhline(0, color=GREY, lw=0.7, ls=":"); ax.set_xticks(range(4)); ax.set_xticklabels([TL[t] for t in TIS])
        ax.set_ylabel("Distance to group median,\ndeviation from 3-category mean", fontsize=7); ax.set_title(TT[p], loc="left")
        ax.margins(x=0.04, y=0.06)
    leg = axs[0].legend(frameon=False, fontsize=6, loc="upper right", ncol=3, columnspacing=0.8)
    for t_ in leg.get_texts():
        if t_.get_text() != "hybrids": t_.set_fontstyle("italic")
    axC = fig.add_subplot(gs[0, 1]); x = np.arange(3); w = 0.2; pv = []
    for k, (p, dv) in enumerate([("1", "global"), ("1", "intra"), ("2", "global"), ("2", "intra")]):
        D_ = GI[p][0] if dv == "global" else GI[p][1]
        v = np.array([D_.hy_inf.sum(), len(D_) - D_.hy_inf.sum() - D_.hy_sup.sum(), D_.hy_sup.sum()])
        pv.append(binomtest(int(D_.hy_sup.sum()), len(D_), 1 / 3, alternative="greater").pvalue)
        axC.bar(x + (k - 1.5) * w, 100 * v / len(D_), w, color=PASSC[p], hatch=("" if dv == "global" else "////"), edgecolor="white", lw=0.3,
                label=f"pass {p}, {'station-blocked' if dv == 'global' else 'within station'} (n = {len(D_)})")
    axC.axhline(100 / 3, ls="--", color=GREY, lw=0.8)
    axC.set_xticks(x); axC.set_xticklabels(["hybrids least\ndispersed", "hybrids\nintermediate", "hybrids most\ndispersed"], fontsize=6)
    axC.set_ylabel("% of tests"); axC.set_ylim(0, 112)
    h, l = axC.get_legend_handles_labels(); h.append(Line2D([], [], ls="--", color=GREY, lw=0.8)); l.append("expected by chance (1/3)")
    axC.legend(h, l, frameon=False, fontsize=6, loc="upper left", ncol=2, columnspacing=0.8, handlelength=1.6)
    axC.set_title(f"Hybrids are the most dispersed category no\nmore often than chance (binomial p ≥ {min(pv):.2f})", loc="left")
    axD = fig.add_subplot(gs[1, 1]); mm_ = []
    for m in MET:
        r_ = []
        for p in "12":
            C_ = CP[p]; loc = C_[(C_.sous_ensemble == "complet") & (C_.modele == "sanspos_cat_station_bloquee") & (C_.terme == "cat")
                                 & (C_.metrique == m) & (C_.tissu == "caudale")]
            dis = PDB[p][(PDB[p].dispositif == "global_station_bloquee") & (PDB[p].metrique == m) & (PDB[p].tissu == "caudale")]
            r_ += [int((loc.p < 0.05).sum()), int((dis.p < 0.05).sum())]
        mm_.append(r_)
    mm_ = np.array(mm_); axD.imshow(mm_, cmap="Blues", vmin=0, vmax=3, aspect="auto")
    for i in range(4):
        for j in range(4): axD.text(j, i, str(mm_[i, j]), ha="center", va="center", fontsize=7, color="white" if mm_[i, j] >= 2 else "black")
    axD.axvline(1.5, color="white", lw=4); axD.set_xticks(range(4)); axD.set_xticklabels(["location", "dispersion"] * 2, fontsize=6)
    for xx, p in [(0.5, "1"), (2.5, "2")]: axD.text(xx, -0.85, f"pass {p}", ha="center", fontsize=6)
    axD.set_yticks(range(4)); axD.set_yticklabels([ML[m] for m in MET], fontsize=6); axD.set_ylim(3.5, -1.2)
    axD.set_title("Caudal fin: only weighted UniFrac shows a consistent\nlocation effect (pass 1); dispersion differs in 1 run of 3", loc="left")
    for s_ in axD.spines.values(): s_.set_visible(False)
    axD.tick_params(length=0)
    for ax, L in [(axs[0], "a"), (axs[1], "b"), (axC, "c"), (axD, "d")]:
        ax.text(-0.30 if ax in axs else -0.22, 1.30, L, transform=ax.transAxes, fontsize=9, fontweight="bold", va="top")
    fig.savefig(out, dpi=300, bbox_inches="tight")
    return mm_, pv

if __name__ == "__main__":
    PDB = {p: pd.read_csv(f"{H}/pd_bias_{p}.tsv", sep="\t") for p in "12"}
    T = table_s10(PDB)
    T.to_csv("table_S10_permdisp_corrige.tsv", sep="\t", index=False)
    print(T.to_string(index=False))
    CP = {p: pd.read_csv(f"{H}/cp_{p}.tsv", sep="\t") for p in "12"}
    PDR = {p: pd.read_csv(f"{H}/pd_raw_{p}.tsv", sep="\t") for p in "12"}
    print("controle (non corrige, libelles d'origine) :", table_s10(PDR, english=False).shape)
    print(fig_s3(PDB, CP))
