#!/usr/bin/env python3
"""36-lecture_tests.py — applique MECANIQUEMENT les regles de lecture de docs/plan_tests_2026-10-03.md
(declarees avant calcul, commit bd6ba3d) aux sorties des scripts 27 (mode 500), 31, 32, 33, 34, 35.
Ecrit avant d'avoir vu les resultats. Sortie : <TESTS_OUTDIR>/lecture_tests.{md,json}.
A lancer depuis la racine du depot avec /usr/bin/python3 (pandas)."""
import os, json
import pandas as pd

O = os.environ.get("TESTS_OUTDIR", "results/tests_20261003")
ALPHA = 0.05
POND = {"bray": True, "unifrac_weighted": True, "jaccard": False, "unifrac_unweighted": False}
TIS = ["caudale", "branchie", "midgut", "hindgut"]
out, md = {}, []
def nsig(ps): return int(sum(1 for p in ps if pd.notna(p) and p < ALPHA))
def robust(ps): return len(ps) == 3 and nsig(ps) == 3

# ------------------------------------------------------------------ (e) sejour en vivier
e = pd.read_csv(f"{O}/sejour_vivier/sejour_tests.tsv", sep="\t")
def etabli(mod, term):
    r = {}
    for t in TIS:
        rob = {m: robust(e[(e.modele == mod) & (e.metrique == m) & (e.tissu == t) & (e.terme == term)].p.tolist()) for m in POND}
        r[t] = dict(robuste=[m for m, v in rob.items() if v],
                    etabli=any(v and POND[m] for m, v in rob.items()) and any(v and not POND[m] for m, v in rob.items()))
    return r
E = {mod: {term: etabli(mod, term) for term in ("pos", "rang")} for mod in ("M1_4stations", "M2_Chavannes")}
m1 = E["M1_4stations"]
sej = [t for t in TIS if m1["rang"][t]["etabli"] and not m1["pos"][t]["etabli"]]
pos_any = [t for t in TIS if m1["pos"][t]["etabli"]]; rang_any = [t for t in TIS if m1["rang"][t]["etabli"]]
if sej: verdict_e = "sejour probable"
elif pos_any and not rang_any: verdict_e = "artefact de plaque probable"
elif not pos_any and not rang_any: verdict_e = "indetermine (non evaluable a cette puissance)"
else: verdict_e = "indetermine (pos et rang etablis dans un meme tissu)"
out["e"] = dict(verdict=verdict_e, detail=E)
md += ["## (e) Séjour en vivier", f"**Verdict (M1, règle déclarée) : {verdict_e}**", ""]
for mod in E:
    for term in ("pos", "rang"):
        md.append(f"- {mod} / {term} : " + "; ".join(f"{t} robuste={E[mod][term][t]['robuste'] or '—'} établi={E[mod][term][t]['etabli']}" for t in TIS))
md.append("")

# ------------------------------------------------------------------ (b) dilution
b2 = pd.read_csv(f"{O}/dilution/b2_direct.tsv", sep="\t")
def b2ps(cmp, mo="sanspos_grp_station_bloquee", met="unifrac_weighted", t="caudale"):
    return b2[(b2.comparaison == cmp) & (b2.modele == mo) & (b2.metrique == met) & (b2.tissu == t)].p.tolist()
pp, pi = b2ps("QPpt_vs_Ptpur"), b2ps("QPpt_vs_INT")
sim_pt = len(pp) == 3 and all(pd.notna(p) and p >= ALPHA for p in pp); dif_pt = robust(pp); dif_int = robust(pi)
b1 = pd.read_csv(f"{O}/dilution/b1_injection.tsv", sep="\t")
b1 = b1[(b1.metrique == "unifrac_weighted") & (b1.tissu == "caudale")]
def kept(rep):
    s = b1[b1.rep == rep]
    return robust(s[s.modele == "cat_apres_pos_station_bloquee"].p.tolist()) and robust(s[s.modele == "sanspos_cat_station_bloquee"].p.tolist())
ref0 = kept(0); nkept = sum(kept(r) for r in sorted(b1.rep.unique()) if r > 0); nrep = int((b1.rep.unique() > 0).sum())
if sim_pt and dif_int and nkept <= 5: verdict_b = "dilution soutenue"
elif dif_pt or nkept >= 15: verdict_b = "dilution refutee"
else: verdict_b = "dilution indeterminee"
out["b"] = dict(verdict=verdict_b, p_QPpt_vs_Pt=pp, p_QPpt_vs_INT=pi, reference_passe1_signal=ref0, tirages_signal_garde=nkept, n_tirages=nrep)
md += ["## (b) Dilution", f"**Verdict : {verdict_b}**",
       f"- b2 caudale UniFrac pondéré, sans position, station bloquée : QPpt vs Pt p = {pp} ; QPpt vs INT p = {pi}",
       f"- b1 : référence passe 1 (sans injection) signal présent = {ref0} (doit reproduire R22) ; signal gardé dans {nkept}/{nrep} injections", ""]

# ------------------------------------------------------------------ (a1) temoin d'effectif a 500
w = pd.read_csv(f"{O}/temoin_effectif_d500/witness.tsv", sep="\t")
w = w[(w.metrique == "unifrac_weighted") & (w.tissu == "caudale") & (w.modele == "ordre_MIN_pos_st_cat")]
nrep_w = w.rep.nunique(); nrepro = sum(robust(w[w.rep == r].p.tolist()) for r in w.rep.unique())
verdict_a1 = "effectif" if nrepro >= 10 else ("definition" if nrepro <= 2 else "indetermine")
out["a1"] = dict(verdict=verdict_a1, tirages_reproduisant=nrepro, n_tirages=nrep_w)
# ------------------------------------------------------------------ (a2) ensemble constant
a2 = pd.read_csv(f"{O}/ensemble_d500/ensemble.tsv", sep="\t")
def motif(v):
    s = a2[(a2.version == v) & (a2.tissu == "caudale")]
    return (nsig(s[s.modele == "cat_apres_pos_station_bloquee"].p.tolist()), nsig(s[s.modele == "sanspos_cat_station_bloquee"].p.tolist()))
mi, mii, miii = motif("i_3000"), motif("ii_500_ensemble_3000"), motif("iii_500_complet")
if mii == (3, 3): verdict_a2 = "ensemble d'echantillons"
elif mii == miii: verdict_a2 = "profondeur"
else: verdict_a2 = "indetermine"
out["a2"] = dict(verdict=verdict_a2, motif_i=mi, motif_ii=mii, motif_iii=miii)
md += ["## (a) Affaiblissement caudal à 500 lectures",
       f"**a1 (témoin d'effectif) : {verdict_a1}** — {nrepro}/{nrep_w} tirages reproduisent la passe 1 (ordre MIN, 3/3 runs)",
       f"**a2 (ensemble constant) : {verdict_a2}** — runs significatifs (pos+cat bloqué, cat bloqué sans pos) : (i) 3000 {mi} ; (ii) 500 sur l'ensemble 3000 {mii} ; (iii) 500 complet {miii}", ""]

# ------------------------------------------------------------------ (c) alpha x categorie
c = pd.read_csv(f"{O}/alpha_categorie/alpha_categorie.tsv", sep="\t")
c = c[c.modele == "principal_station_cat"]
cres = []
for (ps, t), s in c.groupby(["passe", "tissu"]):
    cls = {r.indice: (r.classe, bool(r.ponderee), r.p_cat) for r in s.itertuples()}
    fixed = [k for k, (cl, _, _) in cls.items() if not cl.startswith("indetermine")]
    etab = sorted({cl for cl, pnd, _ in cls.values() if not cl.startswith("indetermine")
                   and any(c2 == cl and p2 for c2, p2, _ in cls.values()) and any(c2 == cl and not p2 for c2, p2, _ in cls.values())})
    cres.append(dict(passe=str(ps), tissu=t, etabli=etab, par_indice={k: dict(classe=v[0], p_cat=v[2]) for k, v in cls.items()}))
out["c"] = cres
md += ["## (c) Catégorie × diversité alpha (modèle principal station + cat)"]
for r in cres:
    md.append(f"- passe {r['passe']} / {r['tissu']} : établi = {r['etabli'] or 'aucun'} ; " +
              "; ".join(f"{k}: {v['classe']} (p_cat={v['p_cat']:.3g})" for k, v in r["par_indice"].items()))
md.append("")
# ------------------------------------------------------------------ (d) partition alpha
dd = pd.read_csv(f"{O}/alpha_partition/alpha_partition.tsv", sep="\t")
out["d"] = dd.to_dict(orient="records")
md += ["## (d) Partition de la variance alpha (remplace R8)", dd.to_string(index=False), ""]
open(f"{O}/lecture_tests.md", "w", encoding="utf-8").write("# Lecture mécanique des tests du 2026-10-03\n\n" + "\n".join(md))
json.dump(out, open(f"{O}/lecture_tests.json", "w"), indent=1, default=str)
print("\n".join(md))
