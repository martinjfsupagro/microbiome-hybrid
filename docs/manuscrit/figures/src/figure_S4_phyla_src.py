"""figure_S4_phyla_src.py — figure supplémentaire : composition en phylums par tissu et catégorie génotypique, aux
trois stations qui portent les trois catégories (décision de JF du 2026-10-06 ; remplace la version à deux panneaux).
Panneau a (décision de JF du 2026-10-06, 2e version) : tous poissons réunis par tissu, chaque poisson pèse autant
(results/phyla_composition/tous_poissons.tsv, scripts/60, commit d67b3f0).
Panneau b : results/phyla_composition/trois_stations.tsv (scripts/59-phyla_trois_stations.py, commit 9aceb57) ;
barre = moyenne à poids égal, sur les stations retenues dans le tissu, du profil moyen de la catégorie ;
n = individus, nombre de stations retenues indiqué par tissu.
"""
import sys
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

SRC = sys.argv[1] if len(sys.argv) > 1 else "results/phyla_composition/"
OUT = sys.argv[2] if len(sys.argv) > 2 else "fig_S4_phyla"
T = pd.read_csv(SRC + "trois_stations.tsv", sep="\t")
A = pd.read_csv(SRC + "tous_poissons.tsv", sep="\t").set_index("tissu")
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

def stack(ax, x, r):
    bottom = 0.0
    for p in ORDER:
        ax.bar(x, r[p], bottom=bottom, width=0.8, color=COL[p], edgecolor="0.35" if p == "Unassigned" else "white", linewidth=0.3)
        bottom += r[p]
    ax.text(x, 1.012, f"{int(r.n)}", ha="center", va="bottom", fontsize=6, color="0.25")

assert np.allclose(A[PHY].sum(1), 1) and sorted(A.index) == sorted(t for t, _ in TIS)
fig = plt.figure(figsize=(7.2, 4.1))
gs = fig.add_gridspec(1, 3, width_ratios=[0.30, 1, 0.34], wspace=0.10)
axa = fig.add_subplot(gs[0, 0]); ax = fig.add_subplot(gs[0, 1], sharey=axa); axl = fig.add_subplot(gs[0, 2]); axl.axis("off")
for i, (tis, tname) in enumerate(TIS):
    stack(axa, i, A.loc[tis])
axa.set_xticks(range(4)); axa.set_xticklabels([t for _, t in TIS], fontsize=7, rotation=45, ha="right", rotation_mode="anchor")
axa.set_xlim(-0.7, 3.7)
axa.text(1.5, 1.075, "all fish\n(9 stations)", ha="center", va="bottom", fontsize=7)
x, xt, xl = 0.0, [], []
for tis, tname in TIS:
    x0 = x
    for k, lab in CAT:
        r = T[(T.tissu == tis) & (T.categorie == k)]
        assert len(r) == 1, (tis, k)
        stack(ax, x, r.iloc[0]); xt.append(x); xl.append(lab); x += 1.0
    ns = int(T[T.tissu == tis].n_stations.iloc[0])
    ax.text((x0 + x - 1.0) / 2, 1.075, f"{tname}\n({ns} stations)", ha="center", va="bottom", fontsize=7)
    x += 0.7
ax.set_xticks(xt); ax.set_xticklabels(xl, fontsize=7)
ax.set_xlim(-0.7, x - 1.0); axa.set_ylim(0, 1.0)
axa.set_yticks([0, 0.25, 0.5, 0.75, 1.0]); axa.set_yticklabels(["0", "25", "50", "75", "100"])
axa.set_ylabel("Mean relative abundance (%)")
ax.tick_params(axis="y", labelleft=False)
for a_ in (axa, ax):
    a_.spines[["top", "right"]].set_visible(False)
axa.set_title(r"$\bf{a}$", loc="left", fontsize=8, pad=44)
ax.set_title(r"$\bf{b}$   genotypic categories at the three stations where all three co-occur", loc="left", fontsize=8, pad=44)
fig.suptitle("Fusobacteriota and Bacillota are enriched in the gut, across all fish and in every genotypic group",
             x=0.08, ha="left", fontsize=8.5, y=1.10)
handles = [Patch(facecolor=COL[p], edgecolor="0.35" if p == "Unassigned" else "none", linewidth=0.4, label=p) for p in reversed(ORDER)]
axl.legend(handles=handles, loc="center left", frameon=False, fontsize=7, handlelength=1.1, handleheight=1.0,
           borderaxespad=0, title="Phylum (SILVA 138.2)", title_fontsize=7, alignment="left")
fig.savefig(OUT + ".png", dpi=300, bbox_inches="tight")
fig.savefig(OUT + ".pdf", bbox_inches="tight")
print("écrit :", OUT + ".png", OUT + ".pdf")
