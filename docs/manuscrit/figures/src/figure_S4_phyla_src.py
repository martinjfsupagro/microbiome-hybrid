"""figure_S4_phyla_src.py — figure supplémentaire : composition en phylums par tissu (analogue de Guivier et al.
2017, Fig. 5). Entrée : results/phyla_composition/moyennes.tsv (scripts/58-phyla_composition.py, commit 33257e3).
a : P. toxostoma, tissu x station ; b : quatre groupes génotypiques, stations confondues. Barres = moyenne entre
individus des profils individu x tissu ; n = individus au-dessus de chaque barre.
"""
import sys
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

SRC = sys.argv[1] if len(sys.argv) > 1 else "results/phyla_composition/"
OUT = sys.argv[2] if len(sys.argv) > 2 else "fig_S4_phyla"
Mo = pd.read_csv(SRC + "moyennes.tsv", sep="\t")
ph = pd.read_csv(SRC + "phyla.tsv", sep="\t")
PHY = list(ph[ph.affiche].phylum) + ["Other phyla", "Unassigned"]
assert len(PHY) == 14 and np.allclose(Mo[PHY].sum(1), 1)

COL = {"Pseudomonadota": "#4C72B0", "Fusobacteriota": "#DD8452", "Bacteroidota": "#55A868", "Bacillota": "#E5C33C",
       "Verrucomicrobiota": "#8172B3", "Thermodesulfobacteriota": "#937860", "Deinococcota": "#DA8BC3",
       "Chlamydiota": "#64B5CD", "Planctomycetota": "#2F6B3B", "Actinomycetota": "#1F3A60", "Spirochaetota": "#A6D854",
       "Cyanobacteriota": "#17BECF", "Other phyla": "#CFCFCF", "Unassigned": "#FFFFFF"}
assert set(COL) == set(PHY), set(PHY) ^ set(COL)
TIS = [("caudale", "caudal fin"), ("branchie", "gill"), ("hindgut", "hindgut"), ("midgut", "midgut")]   # ordre des Fig. 2-3
ST = [("Chavannes-sur-Suran", "Chavannes"), ("Rosieres", "Rosières"), ("Saint-Just-d'Ardeche", "Saint-Just"),
      ("Confluence Buech-Meouge", "Buëch–Méouge"), ("Manosque-Oraison", "Manosque"), ("Canal (usine du Largue)", "Largue canal"),
      ("Pertuis", "Pertuis")]                                                                            # ordre de la Fig. 1
GR = [("Cn", "Cn"), ("Hy_int", "Hy int."), ("Hy_nearp", "Hy near-p."), ("Pt", "Pt")]                  # libellés de la Fig. 2

A = Mo[Mo.panneau == "a"]; B = Mo[Mo.panneau == "b"]
assert set(A.station) == {s for s, _ in ST} and set(B.groupe) == {g for g, _ in GR}


def stacked(ax, blocks, key, labels):
    x, xt, xl, centres = 0.0, [], [], []
    for tis, tname in TIS:
        x0 = x
        for k, lab in labels:
            r = blocks[(blocks.tissu == tis) & (blocks[key] == k)]
            if len(r) == 0:
                ax.text(x, 0.02, "n.d.", ha="center", va="bottom", fontsize=6, color="0.4")
            else:
                r = r.iloc[0]; bottom = 0.0
                for p in PHY:
                    ax.bar(x, r[p], bottom=bottom, width=0.82, color=COL[p], edgecolor="0.35" if p == "Unassigned" else "white",
                           linewidth=0.3)
                    bottom += r[p]
                ax.text(x, 1.012, f"{int(r.n)}", ha="center", va="bottom", fontsize=6, color="0.25")
            xt.append(x); xl.append(lab); x += 1.0
        centres.append(((x0 + x - 1.0) / 2, tname)); x += 0.8
    ax.set_xticks(xt); ax.set_xticklabels(xl)
    ax.set_xlim(-0.7, x - 1.1); ax.set_ylim(0, 1.0)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0]); ax.set_yticklabels(["0", "25", "50", "75", "100"])
    ax.set_ylabel("Mean relative abundance (%)")
    for cx, tname in centres:
        ax.text(cx, 1.075, tname, ha="center", va="bottom", fontsize=8, transform=ax.transData)
    ax.spines[["top", "right"]].set_visible(False)


fig = plt.figure(figsize=(7.2, 6.9))
gs = fig.add_gridspec(2, 2, width_ratios=[1, 0.27], height_ratios=[1.05, 1], hspace=0.95, wspace=0.04)
axa = fig.add_subplot(gs[0, 0]); axb = fig.add_subplot(gs[1, 0]); axl = fig.add_subplot(gs[:, 1]); axl.axis("off")
stacked(axa, A, "station", ST)
plt.setp(axa.get_xticklabels(), rotation=55, ha="right", rotation_mode="anchor", fontsize=6)
stacked(axb, B, "groupe", GR)
plt.setp(axb.get_xticklabels(), rotation=55, ha="right", rotation_mode="anchor", fontsize=6)
axa.set_title("Pseudomonadota is the most abundant phylum in 23 of 28 tissue × station profiles of $\\it{P.\\ toxostoma}$",
              loc="left", fontsize=8, pad=26)
axb.set_title("Fusobacteriota and Bacillota are more abundant in the gut in all four genotypic groups",
              loc="left", fontsize=8, pad=26)
for ax, l in ((axa, "a"), (axb, "b")):
    ax.text(-0.075, 1.27, l, transform=ax.transAxes, fontsize=10, fontweight="bold", va="bottom")
handles = [Patch(facecolor=COL[p], edgecolor="0.35" if p == "Unassigned" else "none", linewidth=0.4, label=p) for p in reversed(PHY)]
axl.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.0, 0.97), frameon=False, fontsize=7, handlelength=1.1, handleheight=1.1,
           borderaxespad=0, title="Phylum (SILVA 138.2)", title_fontsize=7, alignment="left")
fig.savefig(OUT + ".png", dpi=300, bbox_inches="tight")
fig.savefig(OUT + ".pdf", bbox_inches="tight")
print("écrit :", OUT + ".png", OUT + ".pdf")
