"""Figure 4 (dispersion) — code exécuté dans le bac à sable le 2026-10-05. Entrées : permdisp_bias_{1,2}.tsv
(sorties de scripts/24-permdisp.sh avec PERMDISP_BIAS=1, results/recat/{1,2}/permdisp_bias/), chemins locaux ci-dessous."""
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# skill:figure-style kernel.py (auto-injected on skill load)
META_GREY = "#888888"


def apply_figure_style(*, frame="open", font=None, sizes=(8, 7, 6), grid=False):
    import matplotlib as mpl
    if frame not in ("open", "boxed", "none"):
        raise ValueError(f"frame must be 'open'|'boxed'|'none', got {frame!r}")

    try:
        import os, sys, glob, matplotlib.font_manager as fm
        fdir = os.path.join(os.environ.get("CONDA_PREFIX") or sys.prefix, "fonts")
        if os.path.isdir(fdir):
            known = {f.fname for f in fm.fontManager.ttflist}
            for f in glob.glob(os.path.join(fdir, "*.ttf")):
                if f not in known:
                    fm.fontManager.addfont(f)
    except Exception:
        pass
    base, secondary, tick = sizes
    boxed = (frame == "boxed")
    rc = {
        "font.family": "sans-serif",
        "font.size": base,
        "axes.labelsize": base,
        "axes.titlesize": base,
        "legend.fontsize": secondary,
        "xtick.labelsize": tick,
        "ytick.labelsize": tick,
        "axes.linewidth": 0.6,
        "xtick.direction": "out", "ytick.direction": "out",
        "xtick.major.size": 3, "ytick.major.size": 3,
        "xtick.major.width": 0.6, "ytick.major.width": 0.6,
        "axes.spines.top": boxed, "axes.spines.right": boxed,
        "axes.spines.left": frame != "none", "axes.spines.bottom": frame != "none",
        "axes.grid": bool(grid),
        "legend.frameon": False,
        "figure.dpi": 200,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "axes.titleweight": "normal",
        "axes.titlelocation": "left",
        "axes.labelweight": "normal",
        "lines.linewidth": 1.2,
        "patch.linewidth": 0.6,
        "pdf.fonttype": 42, "ps.fonttype": 42,
    }
    if font:
        rc["font.sans-serif"] = [font, "DejaVu Sans"]
    mpl.rcParams.update(rc)


def panel_letter(ax, letter, dx=-0.18, dy=1.02, case="lower", fontsize=None):
    import matplotlib.pyplot as plt
    if fontsize is None:
        fontsize = plt.rcParams.get("font.size", 8) + 1
    s = letter.lower() if case == "lower" else letter.upper()
    ax.text(dx, dy, s, transform=ax.transAxes,
            fontweight="bold", fontsize=fontsize, va="bottom", ha="left")


apply_figure_style(sizes=(8, 7, 6))

pb = {
    '1': pd.read_csv("/home/martinjf/.claude-science/orgs/3ee7bf4c-c79b-4c8d-be07-b1e4b9255247/artifacts/proj_5fdcb680abee/80acf1cd-daed-4d89-9a78-cb9cf0797526/va64bc899_permdisp_bias_1.tsv", sep='\t'),
    '2': pd.read_csv("/home/martinjf/.claude-science/orgs/3ee7bf4c-c79b-4c8d-be07-b1e4b9255247/artifacts/proj_5fdcb680abee/120ac7ff-c35e-4c85-9f0a-8daa524f0c23/vdbf561ba_permdisp_bias_2.tsv", sep='\t'),
}

TIS = [('caudale', 'caudal fin'), ('branchie', 'gill'), ('hindgut', 'hindgut'), ('midgut', 'midgut')]
MET = [('bray', 'Bray–Curtis'), ('unifrac_weighted', 'weighted UniFrac'), ('jaccard', 'Jaccard'), ('unifrac_unweighted', 'unweighted UniFrac')]
mk = {'caudale': 'o', 'branchie': 's', 'hindgut': '^', 'midgut': 'D'}
TM = {t: i for i, (t, _) in enumerate(TIS)}

rng = np.random.default_rng(1)

fig4, ax4 = plt.subplots(1, 2, figsize=(7.2, 2.8), sharey=True)
fig4.subplots_adjust(wspace=0.22)

cnt = {}; below0 = {}
for k, ps in enumerate(('1', '2')):
    x = pb[ps]
    x = x[x.dispositif == 'global_station_bloquee'].copy()
    x['ec'] = x.dist_Hy - (x.dist_Cn + x.dist_Pt) / 2
    least = (x.dist_Hy < x[['dist_Cn', 'dist_Pt']].min(axis=1)).sum()
    cnt[ps] = (int(least), len(x)); below0[ps] = int((x.ec < 0).sum())
    ax = ax4[k]
    for i, (m, ml) in enumerate(MET):
        s = x[x.metrique == m]
        for t, tlab in TIS:
            ss = s[s.tissu == t]
            xs = i + (TM[t] - 1.5) * 0.15 + rng.uniform(-0.03, 0.03, len(ss))
            sig = (ss.p < 0.05).values
            ax.scatter(xs[~sig], ss.ec[~sig], marker=mk[t], s=14, facecolor='white', edgecolor='#4d4d4d', lw=0.7, zorder=3)
            ax.scatter(xs[sig], ss.ec[sig], marker=mk[t], s=14, color='#4d4d4d', zorder=3)
    ax.axhline(0, color=META_GREY, lw=0.7, ls='--', zorder=1)
    ax.set_xticks(range(4))
    ax.set_xticklabels([ml for _, ml in MET], fontsize=6)
    ax.margins(x=0.05, y=0.08)

ax4[0].set_title(f'Pass 1: below both parents in {cnt["1"][0]}/{cnt["1"][1]} tests', loc='left')
ax4[1].set_title(f'Pass 2: below both parents in {cnt["2"][0]}/{cnt["2"][1]} tests', loc='left')
ax4[0].set_ylabel('Hybrid minus mean parental\ndistance to median')

h4 = [Line2D([], [], marker=mk[t], ls='', mfc='white', mec='#4d4d4d', label=tl) for t, tl in TIS] + \
     [Line2D([], [], marker='o', ls='', color='#4d4d4d', label='PERMDISP p < 0.05')]
ax4[1].legend(handles=h4, frameon=False, fontsize=6, loc='lower right')

ax4[0].text(0.02, 0.04, 'below 0: hybrids below the parental mean\n(a weaker condition than below both parents)',
            transform=ax4[0].transAxes, fontsize=6, color=META_GREY, va='bottom')

fig4.text(0.5, 1.02, 'Corrected for group size, hybrids are the most dispersed category no more often than by chance',
          ha='center', fontsize=8)

panel_letter(ax4[0], 'a')
panel_letter(ax4[1], 'b')

fig4.savefig('Figure4_dispersion.png', dpi=300, bbox_inches='tight')