# Figure S1 (ex-S2). Exécution : build_figS1(DA, DL, BR, RC) avec DA/DL/BR = results/depth_agreement/{depth_agreement,
# depth_agreement_low,bray_depth_agreement}.tsv et RC = results/depth_agreement/retention_par_categorie.tsv (script 43).
"""Figure S1 (ex-S2) : compromis profondeur de raréfaction / fidélité des métriques / biais de sélection.
Panneaux a et b : results/depth_agreement/{depth_agreement,depth_agreement_low,bray_depth_agreement}.tsv (inchangés).
Panneau c : results/depth_agreement/retention_par_categorie.tsv (script 43), recalculé le 2026-10-05 sur la
classification de septembre ; l'ancienne figure portait des valeurs recopiées d'une trace antérieure."""
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from matplotlib.lines import Line2D

def build_figS1(DA, DL, BR, RC, out="fig_S1_depth_tradeoff.png", style=None):
    if style: style()
    AG = pd.concat([DA, DL, BR], ignore_index=True)
    DEP = [500, 750, 1000, 1500, 2000, 3000]
    COL = {"unifrac_weighted": "#2166AC", "bray": "#5AA0D6", "jaccard": "#4D9221", "unifrac_unweighted": "#D6604D"}
    NAME = {"unifrac_weighted": "weighted UniFrac", "bray": "Bray–Curtis", "jaccard": "Jaccard", "unifrac_unweighted": "unweighted UniFrac"}
    fig, axs = plt.subplots(2, 2, figsize=(7.2, 5.0)); ax = axs.ravel()
    fig.subplots_adjust(wspace=0.32, hspace=0.62)
    TICKS = [500, 1000, 2000, 3000]
    # a — fidélité des matrices
    for m in ["unifrac_weighted", "bray", "jaccard", "unifrac_unweighted"]:
        s = AG[AG.metrique == m].sort_values("profondeur")
        x = [d for d in s.profondeur if d in DEP and d < 3000] + [3000]
        y = [s[s.profondeur == d].r_pearson.iloc[0] for d in x[:-1]] + [1.0]
        ax[0].plot(x, y, "-o", color=COL[m], ms=3, lw=1.2, label=NAME[m])
    ax[0].axhline(0.99, color="#888888", lw=0.6, ls=":")
    ax[0].set_ylabel("Pearson r with the\n3,000-read matrix")
    ax[0].set_title("Metric fidelity on a fixed set of 1,784 samples", loc="left")
    ax[0].legend(frameon=False, fontsize=6, loc="lower right")
    # b — perte de richesse observée
    s = AG[AG.metrique == "richness"].sort_values("profondeur")
    x = [d for d in s.profondeur if d < 3000] + [3000]
    y = [-100 * s[s.profondeur == d].biais_moyen.iloc[0] / s[s.profondeur == d].distance_moyenne_ref.iloc[0] for d in x[:-1]] + [0]
    ax[1].plot(x, y, "-^", color="#4575B4", ms=3, lw=1.2)
    ax[1].set_ylabel("Loss of observed\nrichness (%)")
    ax[1].set_title("Observed richness, same sample set", loc="left")
    # c, d — biais de sélection : écart de rétention P. toxostoma − hybrides
    PC = {1: ("#1b2a49", "-", "o", "pass 1 (20 intermediate hybrids)"), 2: ("#6fa8dc", "--", "s", "pass 2 (all 42 hybrids)")}
    for k, (tis, lab) in enumerate([("caudale", "caudal fin"), ("midgut", "midgut")]):
        a = ax[2 + k]
        for ps, (col, ls, mk, plab) in PC.items():
            r = RC[(RC.tissu == tis) & (RC.passe == ps)]
            d1 = r[r.run == "durance1"].set_index("profondeur").ecart_Pt_moins_Hy.reindex(DEP)
            runs = r[r.run.isin(["durance1", "durance2", "durance3"])].pivot(index="profondeur", columns="run", values="ecart_Pt_moins_Hy").reindex(DEP)
            a.fill_between(DEP, runs.min(axis=1), runs.max(axis=1), color=col, alpha=0.18, lw=0)
            a.plot(DEP, d1.values, ls, marker=mk, color=col, ms=3, lw=1.2, label=plab)
        a.axhline(0, color="#888888", lw=0.6, ls=":")
        a.set_ylim(-3, 40)
        a.set_ylabel("Retention gap\n(percentage points)")
        a.set_title(f"Selection bias, {lab}", loc="left")
    ax[2].legend(frameon=False, fontsize=6, loc="upper left")
    for a in ax:
        a.set_xscale("log"); a.set_xticks(TICKS); a.set_xticklabels([f"{d:,}" for d in TICKS]); a.minorticks_off()
        a.set_xlabel("Rarefaction depth (reads)")
    for a, l in zip(ax, "abcd"):
        a.text(-0.22, 1.04, l, transform=a.transAxes, fontweight="bold", fontsize=9, va="bottom")
    fig.savefig(out, dpi=300, bbox_inches="tight")
    return fig
