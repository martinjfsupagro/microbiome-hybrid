"""figure_S4_phyla_src.py — figure supplémentaire : composition en phylums par tissu et catégorie génotypique, aux
trois stations qui portent les trois catégories (décision de JF du 2026-10-06 ; remplace la version à deux panneaux).
Entrée : results/phyla_composition/trois_stations.tsv (scripts/59-phyla_trois_stations.py, commit 9aceb57).
Barre = moyenne à poids égal, sur les stations retenues dans le tissu, du profil moyen de la catégorie ;
n = individus, nombre de stations retenues indiqué par tissu.
"""
import sys
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

SRC = sys.argv[1] if len(sys.argv) > 1 else "results/phyla_composition/"
OUT = sys.argv[2] if len(sys.argv) > 2 else "fig_S4_phyla"
T = pd.read_csv(SRC + "trois_stations.tsv", sep="\t")
PHY = [c for c in T.columns if c not in ("tissu", "categorie", "n", "n_stations", "n_par_station") and "__" not in c]
ORDER = ["Pseudomonadota", "Fusobacteriota", "Bacteroidota", "Bacillota", "Verrucomicrobiota", "Thermodesulfobacteriota",
         "Deinococcota", "Chlamydiota", "Planctomycetota", "Actinomycetota", "Spirochaetota", "Cyanobacteriota",
         "Other phyla", "Unassigned"]                                           # ordre d'abondance (scripts/58, phyla.tsv)
assert sorted(PHY) == sorted(ORDER) and np.allclose(T[PHY].sum(1), 1)
COL = {"Pseudomonadota": "#4C72B0", "Fusobacteriota": "#DD8452", "Bacteroidota": "#55A868", "Bacillota": "#E5C33C",
       "Verrucomicrobiota": "#8172B3", "Thermodesulfobacteriota": "#937860", "Deinococcota": "#DA8BC3",
       "Chlamydiota": "#64B5CD", "Planctomycetota": "#2F6B3B", "Actinomycetota": "#1F3A60", "Spirochaetota": "#A6D854",
       "Cyanobacteriota": "#17BECF", "Other phyla": "#CFCFCF", "Unassigned": "#FFFFFF"}
TIS = [("caudale", "caudal fin"), ("branchie", "gill"), ("hindgut", "hindgut"), ("midgut", "midgut")]   # ordre des Fig. 2-3
CAT = [("Cn", "Cn"), ("Hy", "Hy"), ("Pt", "Pt")]

fig = plt.figure(figsize=(7.2, 3.9))
gs = fig.add_gridspec(1, 2, width_ratios=[1, 0.36], wspace=0.04)
ax = fig.add_subplot(gs[0, 0]); axl = fig.add_subplot(gs[0, 1]); axl.axis("off")
x, xt, xl = 0.0, [], []
for tis, tname in TIS:
    x0 = x
    for k, lab in CAT:
        r = T[(T.tissu == tis) & (T.categorie == k)]
        assert len(r) == 1, (tis, k)
        r = r.iloc[0]; bottom = 0.0
        for p in ORDER:
            ax.bar(x, r[p], bottom=bottom, width=0.8, color=COL[p], edgecolor="0.35" if p == "Unassigned" else "white", linewidth=0.3)
            bottom += r[p]
        ax.text(x, 1.012, f"{int(r.n)}", ha="center", va="bottom", fontsize=6, color="0.25")
        xt.append(x); xl.append(lab); x += 1.0
    ns = int(T[T.tissu == tis].n_stations.iloc[0])
    ax.text((x0 + x - 1.0) / 2, 1.075, f"{tname}\n({ns} stations)", ha="center", va="bottom", fontsize=7)
    x += 0.7
ax.set_xticks(xt); ax.set_xticklabels(xl, fontsize=7)
ax.set_xlim(-0.7, x - 1.0); ax.set_ylim(0, 1.0)
ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0]); ax.set_yticklabels(["0", "25", "50", "75", "100"])
ax.set_ylabel("Mean relative abundance (%)")
ax.spines[["top", "right"]].set_visible(False)
ax.set_title("At equal stations, Fusobacteriota and Bacillota are enriched in the gut of every genotypic group",
             loc="left", fontsize=8, pad=44)
handles = [Patch(facecolor=COL[p], edgecolor="0.35" if p == "Unassigned" else "none", linewidth=0.4, label=p) for p in reversed(ORDER)]
axl.legend(handles=handles, loc="center left", frameon=False, fontsize=7, handlelength=1.1, handleheight=1.0,
           borderaxespad=0, title="Phylum (SILVA 138.2)", title_fontsize=7, alignment="left")
fig.savefig(OUT + ".png", dpi=300, bbox_inches="tight")
fig.savefig(OUT + ".pdf", bbox_inches="tight")
print("écrit :", OUT + ".png", OUT + ".pdf")
