#!/usr/bin/env python3
"""40-verif_article_v2.py — vérification chiffrée de l'article restructuré (2026-10-03).
Pour chaque affirmation chiffrée nouvelle ou déplacée : recalcul depuis les fichiers de résultats du dépôt,
mise en forme comme dans le texte, et contrôle que la chaîne exacte figure dans docs/manuscrit/Article.docx.
Complète scripts/30-verif_article.py (qui reste valable pour les sections inchangées).
Sortie : results/verif_article/verif_article_v2.tsv. Lancer depuis la racine du dépôt (python3 système)."""
import re, sys, zipfile, json, csv, math
import numpy as np, pandas as pd
from scipy.stats import binomtest, spearmanr

DOCX = sys.argv[1] if len(sys.argv) > 1 else "docs/manuscrit/Article.docx"
OUT = sys.argv[2] if len(sys.argv) > 2 else "results/verif_article/verif_article_v2.tsv"  # ajout 2026-10-05 : vérifier une variante sans écraser la référence
xml = zipfile.ZipFile(DOCX).read("word/document.xml").decode("utf-8")
paras = [re.sub(r"<[^>]+>", "", p) for p in re.findall(r"<w:p[ >].*?</w:p>", xml, flags=re.S)]
TXT = "\n".join(paras).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
ROWS = []
def chk(section, claim, text, computed, ok):
    found = text in TXT
    ROWS.append(dict(section=section, affirmation=claim, texte=text, calcule=computed, valeur_ok=bool(ok), dans_docx=found,
                     statut="OK" if (ok and found) else "ECART"))
def f(x, d=2): return f"{x:.{d}f}"
def pct(x, d=1): return f"{100*x:.{d}f}"

# ------------------------------------------------------------ génotypes
G = pd.read_csv("docs/manuscrit/table_genotypes_individuels.csv")
cnt = G.genotypic_category.value_counts()
chk("Results/design", "59 Cn, 42 Hy, 79 Pt", "59 C. nasus, 42 hybrids and 79 P. toxostoma",
    f"{cnt['Cn']}/{cnt['Hy']}/{cnt['Pt']}", (cnt["Cn"], cnt["Hy"], cnt["Pt"]) == (59, 42, 79))
qp = G[G.genome_type.str.contains("near", case=False, na=False) | G.genome_type.str.contains("quasi", case=False, na=False)]
par_ = G[G.genome_type == "parental"]
chk("Results/design", "D quasi-purs 0.15–0.60", "discordance D of 0.15–0.60", f"{qp.D.min():.4f}–{qp.D.max():.4f}",
    f(qp.D.min()) == "0.15" and f(qp.D.max()) == "0.60")
chk("Results/design", "D parentaux <= 0.12", "at most 0.12 in parental individuals", f"{par_.D.max():.4f}", par_.D.max() <= 0.12)
bgPt = int((qp.median_index < 0.5).sum()); bgCn = int((qp.median_index >= 0.5).sum())
chk("Results/design", "fond 19 Pt / 3 Cn", "19 have a P. toxostoma background and 3 a C. nasus background", f"{len(qp)} : {bgPt}/{bgCn}",
    (len(qp), bgPt, bgCn) == (22, 19, 3))

# ------------------------------------------------------------ alpha
A = pd.read_csv("results/d7_metriques/alpha_par_indice.tsv", sep="\t").set_index(["indice", "contraste"])
ext = {"Shannon": ("1.51", "1.40–1.64"), "inverse Simpson": ("3.00", "2.48–3.63"),
       "richesse observee": ("1.93", "1.71–2.18"), "Faith PD": ("1.62", "1.50–1.76")}
for ind, (r_, ci) in ext.items():
    a = A.loc[(ind, "externe / interne")]
    ok = f(a.ratio) == r_ and f"{f(a.ic_bas)}–{f(a.ic_haut)}" == ci and a.n == 174
    chk("Results/alpha", f"externe/interne {ind}", ci, f"{a.ratio:.3f} [{a.ic_bas}–{a.ic_haut}] n={a.n}", ok)
pmax = max(A.loc[(i, "externe / interne")].p_wilcoxon for i in ext)
chk("Results/alpha", "Wilcoxon p <= 4.6e-17", "Wilcoxon p ≤ 4.6 × 10⁻¹⁷", f"{pmax:.3g}", f"{pmax:.2g}" == "4.6e-17")
mh = {"richesse observee": ("0.83", "p = 0.009"), "Faith PD": ("0.87", "p = 0.003"), "Shannon": ("0.94", "p = 0.18"), "inverse Simpson": ("0.87", "p = 0.25")}
for ind, (r_, ptxt) in mh.items():
    a = A.loc[(ind, "midgut / hindgut")]
    pv = ptxt.split("= ")[1]; d = len(pv.split(".")[1])
    chk("Results/alpha", f"midgut/hindgut {ind}", f"{r_}" , f"{a.ratio:.3f} p={a.p_wilcoxon:.4g} n={a.n}",
        f(a.ratio) == r_ and f"{a.p_wilcoxon:.{d}f}" == pv and a.n == 136)
AP = pd.read_csv("results/tests_20261003/alpha_partition/alpha_partition.tsv", sep="\t")
def rng(term, col):
    v = AP[AP.terme == term][col].dropna(); return f"{100*v.min():.0f}–{100*v.max():.0f}", v
for term, col, txt in (("tissue", "part_marginale", "19–26 %"), ("individu", "part_marginale", "17–21 %"),
                       ("site_annee", "part_sequentielle", "10–14 %"), ("residuel", "part_sequentielle", "38–45 %")):
    r_, v = rng(term, col); chk("Results/alpha", f"partition {term}", txt, f"{v.min():.4f}–{v.max():.4f}", r_ + " %" == txt)
tech = AP[AP.terme == "technique_library_plus_run"].part_marginale.max()
chk("Results/alpha", "technique <= 0.3 %", "at most 0.3 %", f"{tech:.5f}", tech <= 0.003)
AC = pd.read_csv("results/tests_20261003/alpha_categorie/alpha_categorie.tsv", sep="\t")
pr = AC[AC.modele == "principal_station_cat"]; se = AC[AC.modele != "principal_station_cat"]
chk("Results/alpha", "0/32 transgressif", "transgressive in none of the 32", f"{int(pr.classe.str.contains('transgressif').sum())}/{len(pr)}",
    len(pr) == 32 and not pr.classe.str.contains("transgressif").any())
c1 = pr[(pr.passe == 1) & (pr.tissu == "caudale")]; m2 = pr[(pr.passe == 2) & (pr.tissu == "midgut")]
chk("Results/alpha", "caudale p1 dominant Cn 4/4, p 0.012–0.128", "p for category 0.012–0.128",
    f"{(c1.classe=='dominant Cn').sum()}/4 {c1.p_cat.min():.3f}–{c1.p_cat.max():.3f}", (c1.classe == "dominant Cn").sum() == 4 and f"{c1.p_cat.min():.3f}–{c1.p_cat.max():.3f}" == "0.012–0.128")
d2 = m2[m2.classe == "dominant Cn"]
chk("Results/alpha", "midgut p2 dominant Cn 3/4, p 0.040–0.111", "p = 0.040–0.111", f"{len(d2)}/4 {d2.p_cat.min():.3f}–{d2.p_cat.max():.3f}",
    len(d2) == 3 and f"{d2.p_cat.min():.3f}–{d2.p_cat.max():.3f}" == "0.040–0.111")
s1 = se[(se.passe == 1) & (se.tissu == "caudale")]; s2 = se[(se.passe == 2) & (se.tissu == "midgut")]
chk("Results/alpha", "caudale p1 stable avec position", "The first was unchanged", f"{(s1.classe=='dominant Cn').sum()}/4", (s1.classe == "dominant Cn").sum() == 4)
nint = int((s2.classe == "intermediaire").sum()); nind = int(s2.classe.str.startswith("indetermine").sum())
chk("Results/alpha", "midgut p2 avec position : 2 intermédiaires, 2 indéterminés", "two indices becoming intermediate and two undetermined",
    f"{nint} interm / {nind} indet", (nint, nind) == (2, 2))
chk("Results/alpha", "5/32 p < 0.05", "Five of the 32 principal tests", f"{int((pr.p_cat < 0.05).sum())}", (pr.p_cat < 0.05).sum() == 5)

# ------------------------------------------------------------ composition (partition)
for p, st1, c1_, c2_ in (("1", "20.9", "2.8", "1.7"), ("2", "20.1", "3.0", "1.4")):
    x = pd.read_csv(f"results/recat/{p}/var_partition_cat/category_partition.tsv", sep="\t"); x = x[x.sous_ensemble == "complet"]
    st_first = x[(x.modele == "sanspos_MIN_st_cat") & (x.terme == "st")].R2.median()
    st_after = x[(x.modele == "sanspos_MAX_cat_st") & (x.terme == "st")].R2.median()
    cf = x[(x.modele == "sanspos_MAX_cat_st") & (x.terme == "cat")].R2.median()
    cl = x[(x.modele == "sanspos_MIN_st_cat") & (x.terme == "cat")].R2.median()
    chk("Results/composition", f"passe {p} station servie en premier", f"{st1} %", f"{100*st_first:.2f}", pct(st_first) == st1)
    chk("Results/composition", f"passe {p} catégorie en premier / en dernier", f"{c1_} %", f"{100*cf:.2f} / {100*cl:.2f}",
        pct(cf) == c1_ and abs(100 * cl - float(c2_)) < 0.051)
    chk("Results/composition", f"passe {p} station après catégorie (19/18 %)", ["19 %", "18 %"][int(p) - 1], f"{100*st_after:.2f}",
        f"{100*st_after:.0f}" == ["19", "18"][int(p) - 1])
B1 = pd.read_csv("results/tests_20261003/dilution/b1_injection.tsv", sep="\t")
B2 = pd.read_csv("results/tests_20261003/dilution/b2_direct.tsv", sep="\t")
lect = json.load(open("results/tests_20261003/lecture_tests.json"))
lb = lect["b"]
chk("Results/composition", "dilution : signal gardé 4/20 -> supprimé 16/20", "in 16 of 20 draws",
    f"garde {lb['tirages_signal_garde']}/{lb['n_tirages']}", lb["n_tirages"] - lb["tirages_signal_garde"] == 16 and lb["n_tirages"] == 20)
for key, txt in (("p_QPpt_vs_Pt", "p = 0.28–0.60"), ("p_QPpt_vs_INT", "p = 0.15–0.26")):
    v = lb[key]; chk("Results/composition", f"dilution directe {key}", txt, f"{min(v):.3f}–{max(v):.3f}", f"p = {min(v):.2f}–{max(v):.2f}" == txt)
zi = B2[(B2.comparaison == "QPpt_vs_INT") & (B2.metrique == "unifrac_weighted") & (B2.tissu == "caudale") & (B2.p.round(3).isin([round(x, 3) for x in lb["p_QPpt_vs_INT"]]))]
chk("Results/composition", "dilution directe n = 25–26", "n = 25–26", f"{zi.n.min()}–{zi.n.max()} ({len(zi)} lignes)", len(zi) == 3 and (zi.n.min(), zi.n.max()) == (25, 26))

# ------------------------------------------------------------ dispersion corrigée
L = pd.read_csv("results/recat/lecture_permdisp_biais.tsv", sep="\t")
def lv(p, disp, col): return L[(L.passe == int(p)) & (L.version == "corrige") & (L.dispositif == disp)][col].iloc[0]
chk("Results/dispersion", "22/48 et 32/48", "22 of 48 tests in pass 1 and 32 of 48 in pass 2",
    f"{lv(1,'global_station_bloquee','hy_moins_disperse')}/{lv(2,'global_station_bloquee','hy_moins_disperse')}",
    (lv(1, 'global_station_bloquee', 'hy_moins_disperse'), lv(2, 'global_station_bloquee', 'hy_moins_disperse')) == (22, 32))
pa, pb_ = lv(1, 'global_station_bloquee', 'p_binom_moins'), lv(2, 'global_station_bloquee', 'p_binom_moins')
chk("Results/dispersion", "binomiale 0.048 / 2.4e-6", "p = 0.048 and 2.4 × 10⁻⁶", f"{pa:.3g} / {pb_:.3g}", f"{pa:.3f}" == "0.048" and f"{pb_:.2g}" == "2.4e-06")
chk("Results/dispersion", "plus dispersés 18 / 10, p 0.32 / 0.98", "most dispersed in 18 and 10 (p = 0.32 and 0.98)",
    f"{lv(1,'global_station_bloquee','hy_plus_disperse')}/{lv(2,'global_station_bloquee','hy_plus_disperse')} {lv(1,'global_station_bloquee','p_binom_plus'):.3f}/{lv(2,'global_station_bloquee','p_binom_plus'):.3f}",
    (lv(1, 'global_station_bloquee', 'hy_plus_disperse'), lv(2, 'global_station_bloquee', 'hy_plus_disperse')) == (18, 10)
    and f"{lv(1,'global_station_bloquee','p_binom_plus'):.2f}" == "0.32" and f"{lv(2,'global_station_bloquee','p_binom_plus'):.2f}" == "0.98")
chk("Results/dispersion", "intra 25/68, 39/120 ; plus 17, 45", "25 of 68 tests in pass 1 and 39 of 120 in pass 2",
    f"{lv(1,'intra_station','hy_moins_disperse')}/{lv(1,'intra_station','tests')} {lv(2,'intra_station','hy_moins_disperse')}/{lv(2,'intra_station','tests')} plus {lv(1,'intra_station','hy_plus_disperse')},{lv(2,'intra_station','hy_plus_disperse')}",
    (lv(1,'intra_station','hy_moins_disperse'), lv(1,'intra_station','tests'), lv(2,'intra_station','hy_moins_disperse'), lv(2,'intra_station','tests'),
     lv(1,'intra_station','hy_plus_disperse'), lv(2,'intra_station','hy_plus_disperse')) == (25, 68, 39, 120, 17, 45))
chk("Results/dispersion", "sig transgressifs 3 / 0 ; intra 0 / 5", "numbered 3 in pass 1",
    f"{lv(1,'global_station_bloquee','sig_plus')}/{lv(2,'global_station_bloquee','sig_plus')} intra {lv(1,'intra_station','sig_plus')}/{lv(2,'intra_station','sig_plus')}",
    (lv(1,'global_station_bloquee','sig_plus'), lv(2,'global_station_bloquee','sig_plus'), lv(1,'intra_station','sig_plus'), lv(2,'intra_station','sig_plus')) == (3, 0, 0, 5))
CC = pd.read_csv("results/recat/lecture_permdisp_biais_cellules.tsv", sep="\t"); CC = CC[CC.version == "corrige"]
bray = CC[CC.metrique == "bray"].groupby("passe").ecart_median.median()
oth = CC[CC.metrique != "bray"].groupby(["passe", "metrique"]).ecart_median.median().abs().max()
chk("Results/dispersion", "Bray médiane −0.068 / −0.008 ; autres < 0.013", "−0.068 in pass 2 and −0.008 in pass 1",
    f"{bray.get(2):.4f} / {bray.get(1):.4f} ; autres max {oth:.4f}", f"{bray.get(2):.3f}" == "-0.068" and f"{bray.get(1):.3f}" == "-0.008" and oth < 0.013)
def runs(p, m, t): return int(CC[(CC.passe == p) & (CC.metrique == m) & (CC.tissu == t)].runs_p_inf_005.iloc[0])
cau = {p: {m: runs(p, m, "caudale") for m in ("bray", "jaccard", "unifrac_unweighted", "unifrac_weighted")} for p in (1, 2)}
chk("Results/dispersion", "caudale homogène p2, 1 test p1 (WUF)", "homogeneous on all four metrics in pass 2", json.dumps(cau),
    sum(cau[2].values()) == 0 and cau[1] == {"bray": 0, "jaccard": 0, "unifrac_unweighted": 0, "unifrac_weighted": 1})
chk("Results/dispersion", "midgut Jaccard : 0 run p1, 1 run p2", "homogeneous dispersion in pass 1 and in two runs of three in pass 2",
    f"{runs(1,'jaccard','midgut')}/{runs(2,'jaccard','midgut')}", (runs(1, 'jaccard', 'midgut'), runs(2, 'jaccard', 'midgut')) == (0, 1))
chk("Results/dispersion", "hétérogène 3/3 : midgut UUF p1+p2, Bray midgut+hindgut p2", "midgut on unweighted UniFrac in both passes",
    f"{runs(1,'unifrac_unweighted','midgut')},{runs(2,'unifrac_unweighted','midgut')},{runs(2,'bray','midgut')},{runs(2,'bray','hindgut')}",
    (runs(1, 'unifrac_unweighted', 'midgut'), runs(2, 'unifrac_unweighted', 'midgut'), runs(2, 'bray', 'midgut'), runs(2, 'bray', 'hindgut')) == (3, 3, 3, 3))

# ------------------------------------------------------------ 4H
Cn4 = pd.read_csv("results/fourH/centroides.tsv", sep="\t"); Cn4["GL"] = Cn4.gain + Cn4.loss
cov = pd.read_csv("results/fourH/couverture_taxonomique.tsv", sep="\t").set_index("rang")
chk("Methods/4H", "genre 48.6 % ASV / 64.1 % lectures", "48.6 % of ASVs, carrying 64.1 % of reads",
    f"{cov.loc['genus','pct_asv']:.2f}/{cov.loc['genus','pct_lectures']:.2f}", f"{cov.loc['genus','pct_asv']:.1f}" == "48.6" and f"{cov.loc['genus','pct_lectures']:.1f}" == "64.1")
chk("Methods/4H", "famille 77.9 / 90.6", "family: 77.9 % and 90.6 %", f"{cov.loc['family','pct_asv']:.2f}/{cov.loc['family','pct_lectures']:.2f}",
    f"{cov.loc['family','pct_asv']:.1f}" == "77.9" and f"{cov.loc['family','pct_lectures']:.1f}" == "90.6")
E = pd.read_csv("results/fourH/effectifs_strates.tsv", sep="\t")
nC = E[E.tissu == "caudale"].N_commun.unique(); nO = E[E.tissu != "caudale"].N_commun
chk("Methods/4H", "N 9 caudale, 10–19 ailleurs", "9 in the caudal fin, 10–19", f"{list(nC)} / {nO.min()}–{nO.max()}", list(nC) == [9] and (nO.min(), nO.max()) == (10, 19))
nP = E[E.passe == 2].N_propre
chk("Results/4H", "N propre 26–40", "26–40 hosts per class", f"{nP.min()}–{nP.max()}", (nP.min(), nP.max()) == (26, 40))
lg = open("results/fourH/../../results/fourH/lecture_4H.md").read() if False else None
pr4 = Cn4[Cn4.reglage == "J_genre_0.5"]
tr = pr4[pr4.tissu != "branchie"].GL; gi = pr4[pr4.tissu == "branchie"].GL
chk("Results/4H", "G+L transgressif 0.58–0.69", "Gain + Loss = 0.58–0.69", f"{tr.min():.3f}–{tr.max():.3f}", f"{tr.min():.2f}–{tr.max():.2f}" == "0.58–0.69")
chk("Results/4H", "G+L branchie 0.41–0.46", "Gain + Loss = 0.41–0.46", f"{gi.min():.3f}–{gi.max():.3f}", f"{gi.min():.2f}–{gi.max():.2f}" == "0.41–0.46")
bc = Cn4[Cn4.reglage == "BC_genre_0.5"].GL
chk("Discussion/4H", "Bray-Curtis G+L 0.22–0.35", "Gain + Loss = 0.22–0.35", f"{bc.min():.3f}–{bc.max():.3f}", f"{bc.min():.2f}–{bc.max():.2f}" == "0.22–0.35")
NPl = pd.read_csv("results/fourH/plan_nul.tsv", sep="\t"); NPl = NPl[NPl.reglage == "J_genre_0.5"]
chk("Results/4H", ">= 98.4 % des bootstraps côté Intersection", "at least 98.4 % of bootstraps", f"{NPl.frac_diffI_pos.min():.4f}", f"{100*NPl.frac_diffI_pos.min():.1f}" == "98.4")
PRE = pd.read_csv("results/fourH/preanalyse.tsv", sep="\t")
mp1 = PRE[(PRE.passe == 1) & (PRE.tissu == "midgut")]; oth4 = PRE[~((PRE.passe == 1) & (PRE.tissu == "midgut"))]
chk("Results/4H", "pré-analyse midgut p1 2/3, 0.45–0.64 ; ailleurs 0.51–1.07", "ratio 0.45–0.64) and 0.51–1.07",
    f"{int(mp1.avertissement_critere_aide.sum())}/3 {mp1.ratio_H_parents.min():.3f}–{mp1.ratio_H_parents.max():.3f} ; {oth4.ratio_H_parents.min():.3f}–{oth4.ratio_H_parents.max():.3f} (crit ailleurs {int(oth4.avertissement_critere_aide.sum())})",
    int(mp1.avertissement_critere_aide.sum()) == 2 and f"{mp1.ratio_H_parents.min():.2f}–{mp1.ratio_H_parents.max():.2f}" == "0.45–0.64"
    and f"{oth4.ratio_H_parents.min():.2f}–{oth4.ratio_H_parents.max():.2f}" == "0.51–1.07" and oth4.avertissement_critere_aide.sum() == 0)
Bt = pd.read_csv("results/fourH/bootstraps.tsv", sep="\t", usecols=["passe", "tissu", "run", "reglage", "fraction_OUT", "fraction_MISS"])
nul = Bt[Bt.reglage == "nul1_genre_0.5"].assign(GL=lambda d: d.fraction_OUT + d.fraction_MISS).groupby(["passe", "tissu", "run"]).GL.mean().reset_index()
chk("Results/4H", "hybride nul 0.40–0.57", "transgressive share of 0.40–0.57", f"{nul.GL.min():.3f}–{nul.GL.max():.3f}", f"{nul.GL.min():.2f}–{nul.GL.max():.2f}" == "0.40–0.57")
gap = pr4[["passe", "tissu", "run", "GL"]].merge(nul, on=["passe", "tissu", "run"], suffixes=("", "_n")); gap["d"] = gap.GL - gap.GL_n
gtxt = {"caudale": "0.08–0.15", "midgut": "0.09–0.22", "hindgut": "0.03–0.13"}
for t, txt in gtxt.items():
    z = gap[gap.tissu == t].d; chk("Results/4H", f"écart au nul {t}", f"{txt} in the", f"{z.min():.3f}–{z.max():.3f}", f"{z.min():.2f}–{z.max():.2f}" == txt)
zb = gap[gap.tissu == "branchie"].d
chk("Results/4H", "écart au nul branchie −0.04 à +0.06", "−0.04 to +0.06 in the gill", f"{zb.min():.3f}–{zb.max():.3f}", f"{zb.min():.2f}" == "-0.04" and f"{zb.max():.2f}" == "0.06")
cp = Cn4[(Cn4.reglage == "J_genre_0.5_Npropre") & (Cn4.tissu == "caudale")].GL
chk("Results/4H", "caudale N propre 0.42–0.47", "Gain + Loss = 0.42–0.47", f"{cp.min():.4f}–{cp.max():.4f}", 0.42 <= cp.min() < 0.43 and 0.47 <= cp.max() < 0.48)

# ------------------------------------------------------------ Spearman numéro × colonne, toutes campagnes (méthode du script 31)
MD = pd.read_csv("metadata/analysis_metadata.csv")
MD["camp"] = MD.station + "_" + MD.annee.astype(str)
ind = MD[["individual_id", "camp", "individual"]].drop_duplicates()
assert not ind.individual_id.duplicated().any()
ind["rang"] = ind.groupby("camp").individual.rank(method="first")
MD = MD.merge(ind[["individual_id", "rang"]], on="individual_id")
sp = []
for (camp, tis), s in MD[MD.run_label == "durance1"].groupby(["camp", "tissue"]):
    if len(s) >= 4 and s.col_rank_station.std() > 0: sp.append((camp, tis, len(s), spearmanr(s.rang, s.col_rank_station).correlation))
SP = pd.DataFrame(sp, columns=["camp", "tissu", "n", "rho"])
SP.to_csv("results/verif_article/spearman_toutes_campagnes.tsv", sep="\t", index=False)
chk("Results/plate", "ρ 0.55–0.95 dans toutes les campagnes", "0.55–0.95", f"{SP.rho.min():.3f}–{SP.rho.max():.3f} ({SP.camp.nunique()} campagnes)",
    f"{SP.rho.min():.2f}–{SP.rho.max():.2f}" == "0.55–0.95")

# ------------------------------------------------------------ chiffres périmés qui doivent être ABSENTS (ajout 2026-10-05)
# Les deux anciens paragraphes de dispersion (PERMDISP non corrigé) étaient restés dans les Methods après la
# restructuration du 03/10 ; un contrôle de présence seul ne pouvait pas le voir.
GREY_FREE = TXT  # les notes grises peuvent citer les anciens chiffres ; on contrôle des formulations du texte d'origine
for s_old in ["hybrids are the least dispersed of the three categories in 32 (pass 1) and 34 (pass 2)",
              "Within stations the pattern holds in pass 1 (45 of 68",
              "In the caudal fin, dispersion is heterogeneous on Jaccard in all three runs",
              "binomial p = 2.4 × 10-6 and 1.2 × 10-7"]:
    ROWS.append(dict(section="absence", affirmation="formulation périmée absente", texte=s_old, calcule="",
                     valeur_ok=True, dans_docx=s_old in TXT, statut="OK" if s_old not in TXT else "ECART"))
# ------------------------------------------------------------ tables supplémentaires : ordre de première citation
order = []
for m in re.finditer(r"Tables?\s+S(\d+)", TXT):
    n = int(m.group(1))
    if n not in order: order.append(n)
chk("Tables S", "ordre de première citation = S1…S10, toutes citées", "Supplementary Table S10", str(order), order == list(range(1, 11)))
# ------------------------------------------------------------ §8.6 : rétention selon la profondeur (ajout 2026-10-05, script 43)
RT = pd.read_csv("results/depth_agreement/retention_par_categorie.tsv", sep="\t")
RE = pd.read_csv("results/depth_agreement/retention_effectifs.tsv", sep="\t")
def rt(ps, tis, d, col, run="durance1"):
    x = RT[(RT.passe == ps) & (RT.tissu == tis) & (RT.profondeur == d) & (RT.run == run)]
    assert len(x) == 1, (ps, tis, d, run); return float(x[col].iloc[0])
h1, p1_ = rt(1, "caudale", 3000, "retention_Hy"), rt(1, "caudale", 3000, "retention_Pt")
h2 = rt(2, "caudale", 3000, "retention_Hy")
g1, g2 = rt(1, "caudale", 3000, "ecart_Pt_moins_Hy"), rt(2, "caudale", 3000, "ecart_Pt_moins_Hy")
chk("Methods/8.6", "rétention caudale à 3 000 (durance1) : Hy p1, Pt, Hy p2",
    f"in sequencing run durance1, {h1:.0f} % of intermediate hybrids passed the threshold against {p1_:.0f} % of P. toxostoma (pass 1), and {h2:.0f} % of all 42 hybrids (pass 2)",
    f"{h1:.2f} / {p1_:.2f} / {h2:.2f}", (f"{h1:.0f}", f"{p1_:.0f}", f"{h2:.0f}") == ("50", "86", "67"))
chk("Methods/8.6", "écart caudal à 3 000 (durance1)", f"a gap of {g1:.0f} and {g2:.0f} points", f"{g1:.2f} / {g2:.2f}",
    (f"{g1:.0f}", f"{g2:.0f}") == ("36", "20"))
c1, c2 = rt(1, "caudale", 500, "ecart_Pt_moins_Hy"), rt(2, "caudale", 500, "ecart_Pt_moins_Hy")
chk("Methods/8.6", "écart caudal à 500 (durance1)", f"falls to {c1:.1f} points (pass 1) and {c2:.1f} points (pass 2)",
    f"{c1:.2f} / {c2:.2f}", (f"{c1:.1f}", f"{c2:.1f}") == ("3.8", "5.7"))
m1, m2 = rt(1, "midgut", 500, "ecart_Pt_moins_Hy"), rt(2, "midgut", 500, "ecart_Pt_moins_Hy")
chk("Methods/8.6", "écart midgut à 500 (durance1)", f"({m1:.1f} and {m2:.1f} points)", f"{m1:.2f} / {m2:.2f}",
    (f"{m1:.1f}", f"{m2:.1f}") == ("14.0", "8.9"))
n2 = int(RE[(RE.passe == 2) & (RE.profondeur == 500)].n_retenus.iloc[0]); n1 = int(RE[(RE.passe == 1) & (RE.profondeur == 500)].n_retenus.iloc[0])
chk("Methods/8.6", "échantillons retenus à 500 (tous runs)", f"{n2:,} samples are retained ({n1:,} in pass 1)", f"{n2} / {n1}", (n2, n1) == (2067, 1825))
# ------------------------------------------------------------ figures supplémentaires : ordre de première citation (ajout 2026-10-05)
forder = []
for m in re.finditer(r"Figures?\s+S(\d+)", TXT):
    n = int(m.group(1))
    if n not in forder: forder.append(n)
chk("Figures S", "ordre de première citation des figures = S1…S3", "Figure S3", str(forder), forder == [1, 2, 3])
# ------------------------------------------------------------ références : noms de revues abrégés (NLM), ajout 2026-10-05
NLMA = json.load(open("docs/biblio/nlm_abreviations.json"))
reste = [o for o, n in NLMA.values() if o != n and f". {o}. " in TXT]
ROWS.append(dict(section="absence", affirmation="noms de revues non abrégés absents (31 attendus abrégés)", texte="; ".join(reste),
                 calcule=str(len(reste)), valeur_ok=True, dans_docx=bool(reste), statut="OK" if not reste else "ECART"))
# ------------------------------------------------------------ notes supplémentaires : ordre de première citation (ajout 2026-10-05)
norder = []
for m in re.finditer(r"Notes?\s+S(\d+)", TXT):
    n = int(m.group(1))
    if n not in norder: norder.append(n)
chk("Notes S", "ordre de première citation des notes = S1…S3, toutes citées", "Supplementary Note S3", str(norder), norder == [1, 2, 3])
out = pd.DataFrame(ROWS); out.to_csv(OUT, sep="\t", index=False)
print(out[["section", "affirmation", "calcule", "valeur_ok", "dans_docx", "statut"]].to_string(index=False))
print(f"\n{(out.statut=='OK').sum()} OK / {len(out)} ; écarts : {(out.statut!='OK').sum()}")
