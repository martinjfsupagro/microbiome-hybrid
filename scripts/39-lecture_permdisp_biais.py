#!/usr/bin/env python3
"""39-lecture_permdisp_biais.py — regles de docs/plan_permdisp_biais_2026-10-03.md (commit ecef636).
Compare results/recat/{1,2}/permdisp (non corrige) et permdisp_bias (bias.adjust = TRUE).
Sortie : results/recat/lecture_permdisp_biais.md / .tsv. Lancer depuis la racine du depot."""
import pandas as pd
from scipy.stats import binomtest
rows, cell = [], []
for p in ("1", "2"):
    for ver, d in (("non_corrige", "permdisp"), ("corrige", "permdisp_bias")):
        t = pd.read_csv(f"results/recat/{p}/{d}/permdisp.tsv", sep="\t")
        for c in ("dispositif", "metrique", "tissu", "run", "p", "dist_Cn", "dist_Hy", "dist_Pt"): assert c in t.columns, c
        t["least"] = t.dist_Hy < t[["dist_Cn", "dist_Pt"]].min(axis=1)
        t["most"] = t.dist_Hy > t[["dist_Cn", "dist_Pt"]].max(axis=1)
        t["ecart"] = t.dist_Hy - (t.dist_Cn + t.dist_Pt) / 2
        for disp, s in t.groupby("dispositif"):
            n = len(s); nl, nm = int(s.least.sum()), int(s.most.sum())
            pl = binomtest(nl, n, 1/3, alternative="greater").pvalue
            pm = binomtest(nm, n, 1/3, alternative="greater").pvalue
            rows.append(dict(passe=p, version=ver, dispositif=disp, tests=n, hy_moins_disperse=nl, p_binom_moins=pl,
                             hy_plus_disperse=nm, p_binom_plus=pm,
                             sig_moins=int((s.least & (s.p < 0.05)).sum()), sig_plus=int((s.most & (s.p < 0.05)).sum()),
                             sig_total=int((s.p < 0.05).sum()),
                             regle1_moins_maintenu=(pl < 0.05) if ver == "corrige" else None,
                             regle2_transgressif_soutenu=(pm < 0.05) if ver == "corrige" else None))
            if disp == "global_station_bloquee":
                for (m, ti), z in s.groupby(["metrique", "tissu"]):
                    cell.append(dict(passe=p, version=ver, metrique=m, tissu=ti, runs_p_inf_005=int((z.p < 0.05).sum()),
                                     ecart_median=round(z.ecart.median(), 4),
                                     p_min=round(z.p.min(), 4), p_max=round(z.p.max(), 4),
                                     categorie_plus_dispersee=";".join(sorted(set(
                                         z[z.p < 0.05][["dist_Cn", "dist_Hy", "dist_Pt"]].idxmax(axis=1).str[5:])))))
R = pd.DataFrame(rows); Cc = pd.DataFrame(cell)
med = Cc.groupby(["passe", "version", "metrique"]).ecart_median.median().unstack("version").round(4)
R.to_csv("results/recat/lecture_permdisp_biais.tsv", sep="\t", index=False)
Cc.to_csv("results/recat/lecture_permdisp_biais_cellules.tsv", sep="\t", index=False)
with open("results/recat/lecture_permdisp_biais.md", "w") as f:
    f.write("# PERMDISP non corrige / corrige (bias.adjust) — script 39\n\n```\n" + R.to_string(index=False) + "\n```\n\n")
    f.write("## ecart median Hy - moyenne parentale (station bloquee), par metrique\n\n```\n" + med.to_string() + "\n```\n\n")
    f.write("## cellules station bloquee, version corrigee\n\n```\n" + Cc[Cc.version == "corrige"].to_string(index=False) + "\n```\n")
print(open("results/recat/lecture_permdisp_biais.md").read())
