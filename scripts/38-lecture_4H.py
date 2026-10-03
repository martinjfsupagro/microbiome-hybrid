#!/usr/bin/env python3
"""38-lecture_4H.py — applique mecaniquement les regles de lecture de docs/plan_4H_2026-10-03.md
(commite en 6372af6 avant calcul) aux sorties du script 37 (results/fourH/).

Regles (resume ; texte faisant foi : le plan) :
 1 axe dominant (J_genre_0.5, N commun) : G+L > 0.5 dans les 3 runs -> transgressif ; U+I > 0.5 dans
   les 3 runs -> parental ; sinon non tranche. Modele dominant rapporte s'il est le meme dans les 3 runs.
 2 robustesse : meme axe (regle 1) a rho 0.3, rho 0.7, rang famille et Bray-Curtis. Un axe
   transgressif qui n'apparait qu'a rho 0.7 n'est pas retenu.
 3 compartiment : intervalles bootstrap 2.5-97.5 % de G+L disjoints dans les 3 runs.
 4 plan nul : frac(I - I_nul > 0) > 0.95 dans les 3 runs -> retention preferentielle des taxons
   partages ; < 0.05 dans les 3 runs -> perte concentree sur les taxons partages.
 5 pre-analyse : fractions de core, critere de l'aide (core H < moitie de la moyenne parentale).
 6 passe 1 contre passe 2 : a N commun seulement.
Usage : python3 scripts/38-lecture_4H.py [DOSSIER]   (defaut results/fourH)
"""
import sys, json, itertools
import pandas as pd

D = sys.argv[1] if len(sys.argv) > 1 else "results/fourH"
C = pd.read_csv(f"{D}/centroides.tsv", sep="\t")
B = pd.read_csv(f"{D}/bootstraps.tsv", sep="\t")
NP = pd.read_csv(f"{D}/plan_nul.tsv", sep="\t")
PRE = pd.read_csv(f"{D}/preanalyse.tsv", sep="\t")
EFF = pd.read_csv(f"{D}/effectifs_strates.tsv", sep="\t")
for df, cols in [(C, ["intersection", "union", "gain", "loss"]),
                 (B, ["fraction_AND", "fraction_OR", "fraction_OUT", "fraction_MISS"])]:
    assert all(c in df.columns for c in cols), cols
C["UI"] = C.union + C.intersection
C["GL"] = C.gain + C.loss
assert ((C[["intersection", "union", "gain", "loss"]].sum(axis=1) - 1).abs() < 1e-6).all()
B["GL"] = B.fraction_OUT + B.fraction_MISS
TIS = ["caudale", "branchie", "midgut", "hindgut"]
RUNS = ["durance1", "durance2", "durance3"]
MOD = {"intersection": "Intersection", "union": "Union", "gain": "Gain", "loss": "Loss"}

def axe(sub):
    """sub : centroides d'un passe x tissu x reglage, un par run."""
    assert sorted(sub.run) == RUNS, (sub[["passe", "tissu", "reglage"]].drop_duplicates(), list(sub.run))
    if (sub.GL > 0.5).all(): a = "transgressif"
    elif (sub.UI > 0.5).all(): a = "parental"
    else: a = "non tranche"
    dom = sub[list(MOD)].idxmax(axis=1).map(MOD)
    return a, (dom.iloc[0] if dom.nunique() == 1 else "variable"), sub.GL.min(), sub.GL.max()

out = {"regle1_2": [], "regle3": [], "regle4": [], "regle5": [], "regle6": [], "sensib_Npropre": []}
ALT = ["J_genre_0.3", "J_genre_0.7", "J_famille_0.5", "BC_genre_0.5"]
for p in (1, 2):
    for t in TIS:
        c = C[(C.passe == p) & (C.tissu == t)]
        a0, dom0, gmin, gmax = axe(c[c.reglage == "J_genre_0.5"])
        alts = {r: axe(c[c.reglage == r])[0] for r in ALT}
        robuste = a0 != "non tranche" and all(v == a0 for v in alts.values())
        seul07 = (a0 != "transgressif" and alts["J_genre_0.7"] == "transgressif")
        out["regle1_2"].append(dict(passe=p, tissu=t, axe=a0, modele_dominant=dom0,
                                    GL_min=round(gmin, 3), GL_max=round(gmax, 3),
                                    **{f"axe_{r}": v for r, v in alts.items()},
                                    robuste=robuste, transgressif_seulement_rho07=seul07))
        if p == 2:
            s = c[c.reglage == "J_genre_0.5_Npropre"]
            if len(s): out["sensib_Npropre"].append(dict(passe=p, tissu=t, axe=axe(s)[0],
                                                       GL_min=round(s.GL.min(), 3), GL_max=round(s.GL.max(), 3)))
    # regle 3
    b = B[(B.passe == p) & (B.reglage == "J_genre_0.5")]
    for t1, t2 in itertools.combinations(TIS, 2):
        dis = []
        for r in RUNS:
            q1 = b[(b.tissu == t1) & (b.run == r)].GL.quantile([.025, .975]).values
            q2 = b[(b.tissu == t2) & (b.run == r)].GL.quantile([.025, .975]).values
            dis.append(bool(q1[1] < q2[0] or q2[1] < q1[0]))
        out["regle3"].append(dict(passe=p, tissus=f"{t1}-{t2}", disjoints_runs=sum(dis), compartiment_depend=all(dis)))
    # regle 4
    n = NP[(NP.passe == p) & (NP.reglage == "J_genre_0.5")]
    for t in TIS:
        s = n[n.tissu == t]; assert sorted(s.run) == RUNS
        v = ("retention des taxons partages" if (s.frac_diffI_pos > 0.95).all() else
             "perte concentree sur les partages" if (s.frac_diffI_pos < 0.05).all() else "non tranche")
        out["regle4"].append(dict(passe=p, tissu=t, verdict=v, frac_pos_min=round(s.frac_diffI_pos.min(), 3),
                                  moy_diffI_min=round(s.moy_diffI.min(), 3), moy_diffI_max=round(s.moy_diffI.max(), 3)))
    # regle 5
    for t in TIS:
        s = PRE[(PRE.passe == p) & (PRE.tissu == t)]
        out["regle5"].append(dict(passe=p, tissu=t, ratio_H_parents_min=round(s.ratio_H_parents.min(), 3),
                                  ratio_H_parents_max=round(s.ratio_H_parents.max(), 3),
                                  critere_aide_runs=int(s.avertissement_critere_aide.sum()),
                                  avertissement_package_runs=int((s.lignes_log > 0).sum())))
# regle 6 : passe 1 contre passe 2 a N commun
c = C[C.reglage == "J_genre_0.5"]
for t in TIS:
    m = c[c.tissu == t].pivot(index="run", columns="passe", values="GL")
    a1 = [x for x in out["regle1_2"] if x["passe"] == 1 and x["tissu"] == t][0]["axe"]
    a2 = [x for x in out["regle1_2"] if x["passe"] == 2 and x["tissu"] == t][0]["axe"]
    out["regle6"].append(dict(tissu=t, axe_passe1=a1, axe_passe2=a2, meme_axe=a1 == a2,
                              GL_p2_moins_p1_min=round((m[2] - m[1]).min(), 3), GL_p2_moins_p1_max=round((m[2] - m[1]).max(), 3)))
# modele nul : centroide moyen des bootstraps de l'hybride nul
nul = B[B.reglage == "nul1_genre_0.5"].groupby(["passe", "tissu", "run"])[["GL"]].mean().reset_index()
out["nul1_GL"] = nul.groupby(["passe", "tissu"]).GL.agg(["min", "max"]).round(3).reset_index().to_dict("records")
out["N"] = EFF[["passe", "tissu", "run", "n_Cn", "n_Hy", "n_Pt", "N_commun", "N_propre"]].to_dict("records")

with open(f"{D}/lecture_4H.json", "w") as f: json.dump(out, f, indent=1, ensure_ascii=False, default=str)
with open(f"{D}/lecture_4H.md", "w") as f:
    f.write("# Lecture mecanique de l'indice 4H (script 38, regles du plan 6372af6)\n\n")
    for k in ["regle1_2", "sensib_Npropre", "regle3", "regle4", "regle5", "regle6", "nul1_GL"]:
        f.write(f"## {k}\n\n" + "```\n" + pd.DataFrame(out[k]).to_string(index=False) + "\n```" + "\n\n")
print(open(f"{D}/lecture_4H.md").read())
