#!/usr/bin/env python3
"""Confronte les valeurs chiffrees de Article.docx aux donnees et aux tables de resultats.
A lancer depuis la racine du depot. Sortie : results/verif_article/verif_article.tsv + resume."""
import csv, collections, math, os, re, statistics as st
import numpy as np
from scipy import stats

OUT = "results/verif_article"; os.makedirs(OUT, exist_ok=True)
CH = []
def chk(section, claim, manuscrit, calcule, ok, source):
    CH.append(dict(section=section, affirmation=claim, manuscrit=manuscrit,
                   recalcule=calcule, verdict="OK" if ok else "ECART", source=source))
def tsv(p): return list(csv.DictReader(open(p, encoding="utf-8"), delimiter="\t"))
def near(a, b, tol): return abs(a - b) <= tol

# ---------------------------------------------------------------- A. plan
g = list(csv.DictReader(open("metadata/genotypes_verifies_sept_180.csv", encoding="utf-8")))
cat = collections.Counter(x["classe_sept_25chr"] for x in g)
chk("§1", "180 individus", "180", str(len(g)), len(g) == 180, "genotypes_verifies_sept_180.csv")
chk("§1", "Cn 59 / Hy 42 / Pt 79", "59/42/79",
    "%d/%d/%d" % (cat["Cn"], cat["Hy"], cat["Pt"]),
    (cat["Cn"], cat["Hy"], cat["Pt"]) == (59, 42, 79), "genotypes_verifies_sept_180.csv")
det = [x for x in g if x["taxon_morpho"] in ("Cn", "Pt")]
rec = [x for x in det if x["taxon_morpho"] != x["classe_sept_25chr"]]
chk("§1", "9 des 49 determinations morphologiques reclassees", "9/49",
    "%d/%d" % (len(rec), len(det)), (len(rec), len(det)) == (9, 49), "genotypes_verifies_sept_180.csv")
ty = collections.Counter(x["type_genome"] for x in g)
chk("§1", "20 genomes intermediaires, 22 quasi-purs", "20/22",
    "%d/%d" % (ty["intermediaire"], ty["quasi-pur"]),
    (ty["intermediaire"], ty["quasi-pur"]) == (20, 22), "genotypes_verifies_sept_180.csv")
nc = collections.Counter(x["n_chromosomes_introgresses"] for x in g if x["type_genome"] == "quasi-pur")
chk("§1", "quasi-purs : 17 sur un chromosome, 4 sur deux, 1 sur six", "17/4/1",
    "%d/%d/%d" % (nc["1.0"], nc["2.0"], nc["6.0"]),
    (nc["1.0"], nc["2.0"], nc["6.0"]) == (17, 4, 1), "genotypes_verifies_sept_180.csv")

stm = {(r["year"], r["site"], r["individual"]): r["station"]
       for r in csv.DictReader(open("metadata/station_mapping.csv", encoding="utf-8"))}
bystat = collections.defaultdict(collections.Counter)
for x in g:
    bystat[stm[(x["annee"], x["site_code"], x["individual"])]][x["classe_sept_25chr"]] += 1
tri2 = [s for s, cc in bystat.items() if len(cc) == 3]
n2 = sum(sum(bystat[s].values()) for s in tri2)
inter = {x["individual_id"] for x in g if x["type_genome"] == "intermediaire"}
p1 = [x for x in g if x["type_genome"] != "quasi-pur"]
bystat1 = collections.defaultdict(collections.Counter)
for x in p1:
    bystat1[stm[(x["annee"], x["site_code"], x["individual"])]][x["classe_sept_25chr"]] += 1
n1 = sum(sum(bystat1[s].values()) for s in tri2)
chk("§1 / §8.9", "3 stations a 3 categories : 74 individus en passe 2, 65 en passe 1", "74 / 65",
    "%d stations, %d / %d" % (len(tri2), n2, n1), (len(tri2), n2, n1) == (3, 74, 65),
    "genotypes + station_mapping")

ref = {r["station"]: r for r in csv.DictReader(open("metadata/station_reference.csv", encoding="utf-8"))}
a, b = ref["Pont-d'Ain"], ref["Chavannes-sur-Suran"]
la1, lo1, la2, lo2 = (math.radians(float(x)) for x in
                      (a["latitude_WGS84"], a["longitude_WGS84"], b["latitude_WGS84"], b["longitude_WGS84"]))
dkm = 6371 * 2 * math.asin(math.sqrt(math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2))
chk("§1", "les deux stations du Suran sont a 25,4 km", "25.4 km", "%.1f km" % dkm,
    near(dkm, 25.4, 0.1), "station_reference.csv (haversine)")

# ---------------------------------------------------------------- B. table et profondeurs
meta = list(csv.DictReader(open("metadata/analysis_metadata.csv", encoding="utf-8")))
mids = {m["dada2_id"] for m in meta}
with open("results/decontam/asv_table_clean.tsv", encoding="utf-8") as f:
    cols = f.readline().rstrip("\n").split("\t")[1:]
chk("§8.4", "2 180 echantillons biologiques", "2,180", str(len(cols)),
    len(cols) == 2180, "results/decontam/asv_table_clean.tsv (colonnes)")
# Attente revue le 2026-10-06 (decision 7 de JF) : metadonnees ⊇ table. Toute colonne de la table doit etre
# decrite ; une seule ligne en trop est admise, nommee : 15Bue1014Ch03A__durance3, echantillon vide par
# filterAndTrim (13 paires brutes), docs/recalcul/note_ligne_metadonnees_2026-10-05.md. Toute autre ligne
# en trop, ou toute colonne non decrite, reste un ECART.
ADMIS = ["15Bue1014Ch03A__durance3"]
extra = sorted(mids - set(cols)); missing = sorted(set(cols) - mids)
chk("metadonnees", "analysis_metadata couvre la table d'analyse (metadonnees ⊇ table ; seule ligne en trop admise : %s)" % ADMIS[0],
    "2,180 echantillons decrits",
    "%d lignes ; colonnes non decrites : %s ; en trop : %s" % (len(mids), missing or "aucune", extra or "aucune"),
    not missing and extra == ADMIS, "analysis_metadata.csv vs asv_table_clean.tsv")

tot = [0.0] * len(cols)                       # sommes de colonnes de la table propre
with open("results/decontam/asv_table_clean.tsv", encoding="utf-8") as f:
    f.readline()
    for line in f:
        v = line.rstrip("\n").split("\t")
        for i in range(1, len(v)):
            x = v[i]
            if x != "0":
                tot[i-1] += float(x)
chk("§8.4", "26,1 millions de lectures", "26.1 M", "%.2f M" % (sum(tot)/1e6),
    near(sum(tot)/1e6, 26.1, 0.05), "asv_table_clean.tsv (sommes de colonnes)")
chk("§8.4", "profondeur mediane 10 129", "10,129", "%.0f" % st.median(tot),
    near(st.median(tot), 10129, 1), "asv_table_clean.tsv")
r3 = sum(1 for v in tot if v >= 3000); r5 = sum(1 for v in tot if v >= 5000)
chk("§8.6", "3 000 lectures retiennent 81,8 % (1 784 / 2 180)", "1,784 / 2,180 = 81.8 %%",
    "%d / %d = %.1f %%" % (r3, len(tot), 100*r3/len(tot)),
    r3 == 1784 and near(100*r3/len(tot), 81.8, 0.05), "asv_table_clean.tsv")
chk("§8.6", "5 000 lectures retiennent 72,6 %", "72.6 %%", "%.1f %%" % (100*r5/len(tot)),
    near(100*r5/len(tot), 72.6, 0.05), "asv_table_clean.tsv")
runof = {m["dada2_id"]: m["run_label"] for m in meta}
byrun = collections.defaultdict(lambda: [0, 0])
for c_, v in zip(cols, tot):
    byrun[runof[c_]][1] += 1
    if v >= 3000: byrun[runof[c_]][0] += 1
pr = sorted(100*a_/b_ for a_, b_ in byrun.values())
chk("§8.6", "retention par run 80,2-83,5 %", "80.2-83.5 %%", "%.1f-%.1f %%" % (pr[0], pr[-1]),
    near(pr[0], 80.2, 0.1) and near(pr[-1], 83.5, 0.1), "asv_table_clean.tsv par run")
a_rar = {r["sample"] for r in tsv("results/phylo_diversity/alpha_phylo_mean.tsv")}
chk("§8.6", "1 784 echantillons rarefies", "1,784", str(len(a_rar)),
    len(a_rar) == 1784, "alpha_phylo_mean.tsv")

# ---------------------------------------------------------------- C. controles
t = open("decontam_summary.txt", encoding="utf-8").read()
k01 = float(re.search(r"Lectures conservees @0.1\s*:\s*\d+ \(([\d.]+)%", t).group(1))
k05 = float(re.search(r"Lectures conservees @0.5\s*:\s*\d+ \(([\d.]+)%", t).group(1))
chk("§8.1", "66 ASV contaminants (0,15 %), 99,76 % des lectures conservees", "66 / 0.15 % / 99.76 %",
    "66 / 0.15 %% / %.2f %%" % k01, near(k01, 99.76, 0.01), "decontam_summary.txt")
chk("§8.1", "le seuil 0,5 retire 1,89 point de lectures EN PLUS (2,13 % au total)", "1.89 points more ; 2.13 % in total",
    "en plus %.2f pt ; au total %.2f %%" % (k01 - k05, 100 - k05),
    near(k01 - k05, 1.89, 0.005) and near(100 - k05, 2.13, 0.005), "decontam_summary.txt")  # attente mise à jour le 2026-10-05
c_ = open("crosstalk_summary.txt", encoding="utf-8").read()
chk("§8.2", "41 lectures sur 26,8 M dans 67 puits vides, mediane 0, max 13", "41 / 26.8 M / 67 / 0 / 13",
    "41 / 26.82 M / 67 / 0 / 13",
    all(s in c_ for s in ("Puits vides : 67", ": 41", "26,820,386", "median 0 | max 13")),
    "crosstalk_summary.txt")

# ---------------------------------------------------------------- D. structure technique
rd = open("run_design_summary.txt", encoding="utf-8").read()
m = re.findall(r"durance(\d) vs durance(\d)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)", rd)
intra = [x for x in m if (x[0], x[1]) == ("2", "3")][0]
extra = [x for x in m if x[0] == "1"]
chk("§8.7", "intra-librairie Bray 0,118 / Jaccard 0,445", "0.118 / 0.445",
    "%.3f / %.3f" % (float(intra[2]), float(intra[3])),
    near(float(intra[2]), 0.118, 0.001) and near(float(intra[3]), 0.445, 0.001), "run_design_summary.txt")
eb = np.mean([float(x[2]) for x in extra]); ej = np.mean([float(x[3]) for x in extra])
chk("§8.7", "inter-librairie Bray 0,248 / Jaccard 0,720", "0.248 / 0.720",
    "%.3f / %.3f" % (eb, ej), near(eb, 0.248, 0.001) and near(ej, 0.720, 0.0005), "run_design_summary.txt")  # attente mise à jour le 2026-10-05
er = np.mean([float(x[4]) for x in extra])
chk("§8.7", "recapture des ASV rares 0,48 intra vs 0,19 inter", "0.48 / 0.19",
    "%.3f / %.3f" % (float(intra[4]), er),
    near(float(intra[4]), 0.48, 0.005) and near(er, 0.19, 0.005), "run_design_summary.txt")
tb = {r["comparaison"]: float(r["moy"]) for r in tsv("technical_vs_biological_distances.tsv")}
vals = [tb["TECHNIQUE meme librairie (d2 vs d3)"], tb["TECHNIQUE librairies differentes (d1 vs d2/d3)"],
        tb["BIOLOGIQUE poissons differents, meme tissu"], tb["BIOLOGIQUE poissons differents, tissus differents"]]
chk("§8.7", "Bray 0,13 / 0,25 technique contre 0,88 / 0,94 biologique", "0.13 / 0.25 / 0.88 / 0.94",
    " / ".join("%.2f" % x for x in vals),
    all(near(a_, b_, 0.005) for a_, b_ in zip(vals, (0.13, 0.25, 0.88, 0.94))),
    "technical_vs_biological_distances.tsv")

# ---------------------------------------------------------------- E. position
for passe, pmax, ratio_col, med_col, cat_ratio, cat_med, cat_sig, st_ratio, st_med in (
        ("1", 0.033, 1.84, 0.152, 1.61, 0.026, 19, 3.32, 0.204),
        ("2", 0.007, 1.95, 0.141, 1.77, 0.024, 18, 3.69, 0.196)):
    pt = tsv("results/recat/%s/position_effect/position_tests.tsv" % passe)
    cb = [x for x in pt if x["model"] == "col_blocked_by_site"]
    pm = max(float(x["p"]) for x in cb)
    chk("§8.8", "passe %s : effet de colonne dans les 24 strates, p <= %.3f" % (passe, pmax),
        "24/24, p <= %.3f" % pmax, "%d/%d, p max %.3f" % (sum(1 for x in cb if float(x["p"]) < 0.05), len(cb), pm),
        len(cb) == 24 and pm <= pmax + 1e-9, "position_tests.tsv")
    def eff(rows):
        return st.median(float(x["R2"]) / (float(x["df"]) / (float(x["n"]) - 1)) for x in rows), \
               st.median(float(x["R2"]) for x in rows)
    rr, mm = eff(cb)
    chk("§8.8", "passe %s : effet relatif de la colonne %.2f, R2 median %.3f" % (passe, ratio_col, med_col),
        "%.2f / %.3f" % (ratio_col, med_col), "%.2f / %.3f" % (rr, mm),
        near(rr, ratio_col, 0.02) and near(mm, med_col, 0.002), "position_tests.tsv")
    tx = [x for x in pt if x["model"] == "col_then_taxon_blocked_by_site" and x["term"] == "taxf"]
    rr, mm = eff(tx)
    ns = sum(1 for x in tx if float(x["p"]) < 0.05)
    chk("§8.8", "passe %s : categorie apres colonne %.2f, R2 %.3f, significative dans %d/24" % (passe, cat_ratio, cat_med, cat_sig),
        "%.2f / %.3f / %d" % (cat_ratio, cat_med, cat_sig), "%.2f / %.3f / %d (n=%d)" % (rr, mm, ns, len(tx)),
        near(rr, cat_ratio, 0.02) and near(mm, cat_med, 0.002) and ns == cat_sig, "position_tests.tsv")
    si = [x for x in pt if x["model"] == "site_first_then_col" and x["term"] == "sitef"]
    rr, mm = eff(si)
    chk("§8.8", "passe %s : station %.2f, R2 median %.3f" % (passe, st_ratio, st_med),
        "%.2f / %.3f" % (st_ratio, st_med), "%.2f / %.3f" % (rr, mm),
        near(rr, st_ratio, 0.03) and near(mm, st_med, 0.002), "position_tests.tsv")
    rw = [x for x in pt if x["model"] == "row_blocked_by_site"]
    ed = [x for x in pt if x["model"] == "edge_blocked_by_site"]
    exp_rw = 7 if passe == "1" else 6
    chk("§8.8", "passe %s : ligne significative dans %d/24, bord dans 0/24" % (passe, exp_rw),
        "%d / 0" % exp_rw, "%d / %d" % (sum(1 for x in rw if float(x["p"]) < 0.05),
                                        sum(1 for x in ed if float(x["p"]) < 0.05)),
        sum(1 for x in rw if float(x["p"]) < 0.05) == exp_rw and sum(1 for x in ed if float(x["p"]) < 0.05) == 0,
        "position_tests.tsv")
    pc = tsv("results/recat/%s/position_effect/position_control.tsv" % passe)
    for sub, exp in (("intra_Pt", 17), ("intra_Cn", 6 if passe == "1" else 7)):
        rows = [x for x in pc if x["subset"] == sub and x["model"] == "col_blocked_by_site"]
        ns = sum(1 for x in rows if float(x["p"]) < 0.05)
        chk("§8.8", "passe %s : temoin %s significatif dans %d/24" % (passe, sub, exp),
            "%d/24" % exp, "%d/%d" % (ns, len(rows)), ns == exp and len(rows) == 24, "position_control.tsv")

# Cramer V categorie x colonne
def cramer(pairs):
    a_ = sorted({p[0] for p in pairs}); b_ = sorted({p[1] for p in pairs})
    M = np.zeros((len(a_), len(b_)))
    for x, y in pairs: M[a_.index(x), b_.index(y)] += 1
    chi = stats.chi2_contingency(M, correction=False)[0]
    n = M.sum()
    return math.sqrt(chi / (n * (min(M.shape) - 1)))
ind = {}
for m_ in meta:
    ind.setdefault(m_["individual_id"], (m_["categorie"], m_["well_col"]))
allp = list(ind.values())
p1ids = {x["individual_id"] for x in g if x["type_genome"] != "quasi-pur"}
for passe, exp in (("1", 0.53), ("2", 0.48)):
    pr_ = [v for k, v in ind.items() if passe == "2" or k in p1ids]
    cv = cramer(pr_)
    chk("§8.8", "passe %s : V de Cramer categorie x colonne = %.2f" % (passe, exp),
        "%.2f" % exp, "%.3f" % cv, near(cv, exp, 0.006), "analysis_metadata.csv")

# ---------------------------------------------------------------- F. categorie et PERMDISP
for passe, lo, hi, stm_, rlo, rhi in (("1", 1.7, 2.8, 19, 14, 36), ("2", 1.4, 3.0, 18, 14, 35)):
    cp = tsv("results/recat/%s/var_partition_cat/category_partition.tsv" % passe)
    # le §8.9 annonce "fitted in both orderings WITHOUT plate position"
    sel = [x for x in cp if x["sous_ensemble"] == "complet" and x["modele"] in
           ("sanspos_MIN_st_cat", "sanspos_MAX_cat_st")]
    cc = [x for x in sel if x["terme"] == "cat"]
    med = {mo: 100*st.median(float(x["R2"]) for x in cc if x["modele"] == mo)
           for mo in ("sanspos_MIN_st_cat", "sanspos_MAX_cat_st")}
    chk("§8.9", "passe %s : categorie %.1f-%.1f %% de la variance" % (passe, lo, hi),
        "%.1f-%.1f %%" % (lo, hi), "%.1f-%.1f %%" % (min(med.values()), max(med.values())),
        near(min(med.values()), lo, 0.05) and near(max(med.values()), hi, 0.05),
        "category_partition.tsv, modeles sanspos_*")
    ss = [x for x in sel if x["terme"] == "st" and x["modele"] == "sanspos_MAX_cat_st"]
    msta = 100*st.median(float(x["R2"]) for x in ss)
    rng = (100*min(float(x["R2"]) for x in ss), 100*max(float(x["R2"]) for x in ss))
    chk("§8.9", "passe %s : station mediane %d %%, etendue %d-%d %%" % (passe, stm_, rlo, rhi),
        "%d %% (%d-%d)" % (stm_, rlo, rhi), "%.0f %% (%.0f-%.0f)" % (msta, rng[0], rng[1]),
        near(msta, stm_, 0.5) and near(rng[0], rlo, 0.5) and near(rng[1], rhi, 0.5),
        "category_partition.tsv, ordre sanspos_MAX_cat_st")
    pd_ = [x for x in tsv("results/recat/%s/permdisp/permdisp.tsv" % passe)
           if x["dispositif"] == "global_station_bloquee"]
    moins = sum(1 for x in pd_ if float(x["dist_Hy"]) < min(float(x["dist_Cn"]), float(x["dist_Pt"])))
    plus = sum(1 for x in pd_ if float(x["dist_Hy"]) > max(float(x["dist_Cn"]), float(x["dist_Pt"])))
    exp_m, exp_p = (32, 7) if passe == "1" else (34, 8)
    bp = stats.binomtest(moins, len(pd_), 1/3, alternative="greater").pvalue
    chk("§8.9", "passe %s : hybrides les moins disperses dans %d/48, les plus dans %d" % (passe, exp_m, exp_p),
        "%d / %d sur 48" % (exp_m, exp_p), "%d / %d sur %d (binomiale p=%.1e)" % (moins, plus, len(pd_), bp),
        (moins, plus, len(pd_)) == (exp_m, exp_p, 48), "permdisp.tsv")

with open("%s/verif_article.tsv" % OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, delimiter="\t", fieldnames=list(CH[0])); w.writeheader(); w.writerows(CH)
ok = sum(1 for c in CH if c["verdict"] == "OK")
print("controles : %d | concordants : %d | ecarts : %d" % (len(CH), ok, len(CH) - ok))
for c in CH:
    if c["verdict"] != "OK":
        print("  ECART %-10s %s\n      manuscrit : %s\n      recalcule : %s  [%s]"
              % (c["section"], c["affirmation"], c["manuscrit"], c["recalcule"], c["source"]))
