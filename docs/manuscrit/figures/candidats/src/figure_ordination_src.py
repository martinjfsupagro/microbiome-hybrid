"""figure_ordination_src.py — figure supplémentaire candidate : ordinations Jaccard (scripts/65, commit 25b87d4).
Deux versions du panneau b à comparer (JF et André, 2026-10-06) :
  v1 : b = PCoA par tissu aux trois stations à trois catégories (symbole = station) ;
  v2 : b = axes non contraints après retrait de la station (db-RDA conditionnée par la station, 9 stations).
Panneau a commun : PCoA de tous les échantillons du run durance1. Points = échantillons (y compris ré-extractions).
Usage : figure_ordination_src.py <dossier results/ordination/> <v1|v2> <sortie sans extension>
"""
import sys
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

SRC, VER, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
assert VER in ("v1", "v2")
CO = pd.read_csv(SRC + "coords.tsv", sep="\t"); AX = pd.read_csv(SRC + "axes.tsv", sep="\t")
AX = AX[AX.run == "durance1"].set_index(["panel", "tissu"])
TIS = [("caudale", "caudal fin"), ("branchie", "gill"), ("hindgut", "hindgut"), ("midgut", "midgut")]
TCOL = {"caudale": "#4D4D4D", "branchie": "#A8A8A8", "hindgut": "#1B7F79", "midgut": "#7FC8BF"}   # externes gris, digestifs sarcelle
CCOL = {"Cn": "#2166AC", "Hy": "#762A83", "Pt": "#E08214"}                                       # couleurs de la Fig. 1
CLAB = {"Cn": "C. nasus", "Hy": "hybrids", "Pt": "P. toxostoma"}
ST = {"Canal (usine du Largue)": ("o", "Largue canal"), "Confluence Buech-Meouge": ("s", "Buëch–Méouge"),
      "Saint-Just-d'Ardeche": ("^", "Saint-Just")}
PB = "b1" if VER == "v1" else "b2"

fig = plt.figure(figsize=(7.2, 4.3))
gs = fig.add_gridspec(2, 3, width_ratios=[1.25, 1, 1], wspace=0.32, hspace=0.42)
axa = fig.add_subplot(gs[:, 0])
a = CO[CO.panel == "a"]
for t, name in TIS:
    g = a[a.tissue == t]
    axa.scatter(g.ax1, g.ax2, s=7, c=TCOL[t], alpha=0.75, linewidths=0, label=f"{name} ({len(g)})")
pa = AX.loc[("a", "tous")]
axa.set_xlabel(f"PCoA 1 ({pa.pct1:.1f} %)"); axa.set_ylabel(f"PCoA 2 ({pa.pct2:.1f} %)")
pad_ = 0.03
axa.set_xlim(a.ax1.min() - pad_, a.ax1.max() + pad_); axa.set_ylim(a.ax2.min() - pad_, a.ax2.max() + pad_)
axa.set_aspect("equal", adjustable="box")
axa.legend(loc="upper left", bbox_to_anchor=(-0.02, -0.20), frameon=False, fontsize=6.5, ncol=2, handletextpad=0.2, markerscale=1.6, columnspacing=0.8)
axa.set_title("Gut and external tissues separate\nalong the first axis", loc="left", fontsize=8)
axa.text(-0.16, 1.07, "a", transform=axa.transAxes, fontsize=10, fontweight="bold")

axes_b = []
for k, (t, name) in enumerate(TIS):
    ax = fig.add_subplot(gs[k // 2, 1 + k % 2]); axes_b.append(ax)
    g = CO[(CO.panel == PB) & (CO.tissu_panneau == t)]
    for cat in ("Pt", "Cn", "Hy"):
        h = g[g.categorie == cat]
        if VER == "v1":
            for st, (mk, _) in ST.items():
                hh = h[h.station == st]
                ax.scatter(hh.ax1, hh.ax2, s=11, marker=mk, facecolors=CCOL[cat], edgecolors="white", linewidths=0.3, alpha=0.9)
        else:
            ax.scatter(h.ax1, h.ax2, s=9, c=CCOL[cat], edgecolors="white", linewidths=0.3, alpha=0.85)
    pb = AX.loc[(PB, t)]
    lab = "PCoA" if VER == "v1" else "residual axis"
    ax.set_xlabel(f"{lab} 1 ({pb.pct1:.1f} %)", fontsize=6.5, labelpad=1); ax.set_ylabel(f"{lab} 2 ({pb.pct2:.1f} %)", fontsize=6.5, labelpad=1)
    ax.tick_params(labelsize=5.5, length=2)
    ax.set_aspect("equal", adjustable="datalim")
    ax.set_title(f"{name} (n = {len(g)})", fontsize=7, pad=3)
btitle = ("At the three stations, samples group by station, not by category" if VER == "v1"
          else "With station removed, the three categories overlap in every tissue")
axes_b[0].text(-0.28, 1.30, "b", transform=axes_b[0].transAxes, fontsize=10, fontweight="bold")
axes_b[0].text(-0.12, 1.30, btitle, transform=axes_b[0].transAxes, fontsize=8, va="baseline")
hcat = [Line2D([], [], ls="", marker="o", ms=4.5, mfc=CCOL[c], mec="none", label=CLAB[c]) for c in ("Cn", "Hy", "Pt")]
if VER == "v1":
    hcat += [Line2D([], [], ls="", marker=mk, ms=4.5, mfc="0.55", mec="none", label=lab_) for mk, lab_ in ST.values()]
leg = axes_b[2].legend(handles=hcat, loc="upper left", bbox_to_anchor=(-0.25, -0.30), ncol=3 if VER == "v2" else 6, frameon=False,
                       fontsize=6.5, handletextpad=0.15, columnspacing=0.7)
for t_ in leg.get_texts()[:3]:
    if t_.get_text() != "hybrids": t_.set_fontstyle("italic")
fig.savefig(OUT + ".png", dpi=300, bbox_inches="tight")
fig.savefig(OUT + ".pdf", bbox_inches="tight")
print("écrit :", OUT)
