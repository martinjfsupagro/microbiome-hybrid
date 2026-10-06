"""figure_S4_phyla_src.py — figure supplémentaire : composition en phylums par tissu (3e version, décision de JF
du 2026-10-06).
a : tous poissons réunis, tissu x station (results/phyla_composition/station_tous_poissons.tsv, scripts/61, commit
    c3bae96) ; chaque poisson de la station pèse autant ; ordre des stations de la Fig. 1a.
b : catégories Cn / Hy / Pt aux trois stations à trois catégories (results/phyla_composition/trois_stations.tsv,
    scripts/59, commit 9aceb57) ; barre = moyenne à poids égal des stations retenues dans le tissu.
n = individus au-dessus de chaque barre.
"""
import sys
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

SRC = sys.argv[1] if len(sys.argv) > 1 else "results/phyla_composition/"
OUT = sys.argv[2] if len(sys.argv) > 2 else "fig_S3_phyla"   # Figure S3 depuis scripts/62 (ex fig_S4_phyla)
T = pd.read_csv(SRC + "trois_stations.tsv", sep="\t")
A = pd.read_csv(SRC + "station_tous_poissons.tsv", sep="\t")
ST = [("Chavannes-sur-Suran", "Chavannes"), ("Pont-d'Ain", "Pont-d'Ain"), ("Rosieres", "Rosières"), ("Saint-Just-d'Ardeche", "Saint-Just"),
      ("Confluence Buech-Meouge", "Buëch–Méouge"), ("Manosque-Oraison", "Manosque"), ("Canal (usine du Largue)", "Largue canal"),
      ("Pertuis", "Pertuis"), ("Avignon", "Avignon")]                                    # ordre et libellés de la Fig. 1a
PHY = [c for c in T.columns if c not in ("tissu", "categorie", "n", "n_stations", "n_par_station") and "__" not in c]
ORDER = ["Pseudomonadota", "Fusobacteriota", "Bacteroidota", "Bacillota", "Verrucomicrobiota", "Thermodesulfobacteriota",
         "Deinococcota", "Chlamydiota", "Planctomycetota", "Actinomycetota", "Spirochaetota", "Cyanobacteriota",
         "Other phyla", "Unassigned"]                                           # ordre d'abondance (scripts/58, phyla.tsv)
assert sorted(PHY) == sorted(ORDER) and np.allclose(T[PHY].sum(1), 1)
assert set(A.station) == {k for k, _ in ST} and len(A) == 36 and np.allclose(A[PHY].sum(1), 1)
COL = {"Pseudomonadota": "#4C72B0", "Fusobacteriota": "#DD8452", "Bacteroidota": "#55A868", "Bacillota": "#E5C33C",
       "Verrucomicrobiota": "#8172B3", "Thermodesulfobacteriota": "#937860", "Deinococcota": "#DA8BC3",
       "Chlamydiota": "#64B5CD", "Planctomycetota": "#2F6B3B", "Actinomycetota": "#1F3A60", "Spirochaetota": "#A6D854",
       "Cyanobacteriota": "#17BECF", "Other phyla": "#CFCFCF", "Unassigned": "#FFFFFF"}
TIS = [("caudale", "caudal fin"), ("branchie", "gill"), ("hindgut", "hindgut"), ("midgut", "midgut")]   # ordre des Fig. 2-3
CAT = [("Cn", "Cn"), ("Hy", "Hy"), ("Pt", "Pt")]

def stacked(ax, blocks, key, labels, header, gap=0.8, rot=False):
    x, xt, xl = 0.0, [], []
    for tis, tname in TIS:
        x0 = x
        for k, lab in labels:
            r = blocks[(blocks.tissu == tis) & (blocks[key] == k)]
            assert len(r) == 1, (tis, k)
            r = r.iloc[0]; bottom = 0.0
            for p in ORDER:
                ax.bar(x, r[p], bottom=bottom, width=0.8, color=COL[p], edgecolor="0.35" if p == "Unassigned" else "white", linewidth=0.3)
                bottom += r[p]
            ax.text(x, 1.012, f"{int(r.n)}", ha="center", va="bottom", fontsize=5.5 if rot else 6, color="0.25", rotation=90 if rot else 0)
            xt.append(x); xl.append(lab); x += 1.0
        ax.text((x0 + x - 1.0) / 2, 1.085 if rot else 1.075, header(tis, tname), ha="center", va="bottom", fontsize=7)
        x += gap
    ax.set_xticks(xt)
    if rot:
        ax.set_xticklabels(xl, fontsize=6, rotation=55, ha="right", rotation_mode="anchor")
    else:
        ax.set_xticklabels(xl, fontsize=7)
    ax.set_xlim(-0.7, x - gap + 0.3); ax.set_ylim(0, 1.0)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0]); ax.set_yticklabels(["0", "25", "50", "75", "100"])
    ax.set_ylabel("Mean relative abundance (%)")
    ax.spines[["top", "right"]].set_visible(False)


fig = plt.figure(figsize=(7.2, 7.0))
gs = fig.add_gridspec(2, 2, width_ratios=[1, 0.27], height_ratios=[1.05, 1], hspace=0.75, wspace=0.04)
axa = fig.add_subplot(gs[0, 0]); ax = fig.add_subplot(gs[1, 0]); axl = fig.add_subplot(gs[0, 1]); axl.axis("off")
stacked(axa, A, "station", ST, lambda t, n: n, rot=True)
NST = T.groupby("tissu").n_stations.first()
stacked(ax, T, "categorie", CAT, lambda t, n: f"{n}\n({int(NST[t])} stations)", gap=0.7)
axa.set_title(r"All fish by station: $\it{Pseudomonadota}$ leads in 33 of 36 tissue × station profiles",
              loc="left", fontsize=8, pad=24)
ax.set_title(r"Three-category stations: $\it{Fusobacteriota}$ and $\it{Bacillota}$ are gut-enriched in every group",
             loc="left", fontsize=8, pad=34)
for a_, l, y in ((axa, "a", 1.20), (ax, "b", 1.255)):
    a_.text(-0.075, y, l, transform=a_.transAxes, fontsize=10, fontweight="bold", va="bottom")
handles = [Patch(facecolor=COL[p], edgecolor="0.35" if p == "Unassigned" else "none", linewidth=0.4, label=p) for p in reversed(ORDER)]
_lg = axl.legend(handles=handles, loc="center left", frameon=False, fontsize=7, handlelength=1.1, handleheight=1.1,
           borderaxespad=0, title="Phylum (SILVA 138.2)", title_fontsize=7, alignment="left")
for _t in _lg.get_texts():                      # noms de taxons en italique (consignes d'Animal Microbiome, 2026-10-06)
    if _t.get_text() not in ("Other phyla", "Unassigned"): _t.set_fontstyle("italic")
fig.savefig(OUT + ".png", dpi=300, bbox_inches="tight")
fig.savefig(OUT + ".pdf", bbox_inches="tight")
print("écrit :", OUT + ".png", OUT + ".pdf")
