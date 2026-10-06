#!/usr/bin/env python3
"""70-largue_caudale.py — nageoire caudale du canal du Largue : 0 échantillon sur 20 à >= 3 000 lectures dans durance1,
3 sur 20 dans durance2 et durance3 (constat du 2026-10-06 sur la Figure S4). Décision de JF : (A) chiffrer la part du
Largue dans la sélection des hybrides par la raréfaction en nageoire caudale ; (B) chercher où se perdent les lectures.

A. Même définition que scripts/43 (unité : échantillon individu × tissu × run ; profondeur = somme de colonne de
   results/decontam/asv_table_clean.tsv ; retenu si >= d ; passe 1 sans quasi-purs ; écart = 100 × (rétention Pt −
   rétention Hy)). Calcul avec toutes les stations — témoin : doit redonner results/depth_agreement/
   retention_par_categorie.tsv à l'identique — puis sans le canal du Largue. Rien d'autre ne change entre les deux.
B. Par échantillon : lectures brutes et lectures retirées comme 12S de l'hôte (rapports cutadapt
   results/rm12S_<run>_*/<échantillon>.12s.json, champs read_counts.input / filtered.too_short / output), parcours
   DADA2 (results/dada2_final/track_all.csv : input, filtered, merged, nonchim), total après décontamination. Médianes
   par groupe : caudale Largue, caudale des 8 autres stations, autres tissus du Largue. Plaque et colonne relevées.
   Descriptif : aucun mécanisme n'est conclu de ces seules étapes.
Sorties : results/largue_caudale/{retention_avec_sans_largue.tsv, etapes_par_echantillon.tsv, etapes_resume.tsv,
resume.txt}. Python système. Lancer depuis la racine du dépôt.
"""
import csv, glob, json, os, collections
import pandas as pd, numpy as np

OUT = "results/largue_caudale/"; os.makedirs(OUT, exist_ok=True)
LAR = "Canal (usine du Largue)"
with open("results/decontam/asv_table_clean.tsv") as fh:
    hdr = fh.readline().rstrip("\n").split("\t")[1:]
    tot = [0] * len(hdr)
    for line in fh:
        v = line.rstrip("\n").split("\t")[1:]
        for i, x in enumerate(v):
            if x and x != "0": tot[i] += int(float(x))
depth = dict(zip(hdr, tot)); assert len(depth) == 2180
md = {r["dada2_id"]: r for r in csv.DictReader(open("metadata/analysis_metadata.csv", encoding="utf-8"))}
S = [dict(md[s], depth=depth[s]) for s in depth]

# ---------------------------------------------------------------- A
def retention(samples):
    rows = []
    for ps in ("1", "2"):
        sub = [r for r in samples if ps == "2" or r["inclus_passe1"] in ("True", "TRUE")]
        for run in ("tous", "durance1", "durance2", "durance3"):
            for tis in sorted({r["tissue"] for r in sub}):
                st = [r for r in sub if r["tissue"] == tis and run in ("tous", r["run_label"])]
                for d in (500, 3000):
                    ret = {c: (sum(r["depth"] >= d for r in st if r["categorie"] == c), sum(r["categorie"] == c for r in st)) for c in ("Cn", "Hy", "Pt")}
                    rows.append(dict(passe=ps, run=run, tissu=tis, profondeur=d,
                                     **{f"retenus_{c}": ret[c][0] for c in ret}, **{f"n_{c}": ret[c][1] for c in ret},
                                     **{f"retention_{c}": round(100 * ret[c][0] / ret[c][1], 2) for c in ret},
                                     ecart_Pt_moins_Hy=round(100 * (ret["Pt"][0] / ret["Pt"][1] - ret["Hy"][0] / ret["Hy"][1]), 2)))
    return pd.DataFrame(rows)
avec = retention(S); sans = retention([r for r in S if r["station"] != LAR])
ref = pd.read_csv("results/depth_agreement/retention_par_categorie.tsv", sep="\t", dtype={"passe": str})
ref = ref[ref.profondeur.isin([500, 3000])]
k = ["passe", "run", "tissu", "profondeur"]
m = avec.merge(ref, on=k, suffixes=("", "_ref"))
assert len(m) == len(avec), (len(m), len(avec))
cols = [c for c in avec.columns if c not in k]
ecarts = {c: float((m[c] - m[c + "_ref"]).abs().max()) for c in cols}
assert max(ecarts.values()) < 1e-9, ecarts
R = avec.merge(sans, on=k, suffixes=("_avec", "_sans"))
R.to_csv(OUT + "retention_avec_sans_largue.tsv", sep="\t", index=False)

# ---------------------------------------------------------------- B
js = {}
for f in glob.glob("results/rm12S_durance*_*/*.12s.json"):
    run = f.split("/")[1].split("_")[1]
    d = json.load(open(f))["read_counts"]
    js[(os.path.basename(f)[:-len(".12s.json")], run)] = (d["input"], d["filtered"]["too_short"], d["output"])
tr = pd.read_csv("results/dada2_final/track_all.csv")
tr = {(r.sample, r.run): r for r in tr.itertuples()}
E = []
for s, r in md.items():
    if s not in depth: continue
    stem, run = s.split("__")
    key = (stem, run) if (stem, run) in js else (stem.replace("-", ""), run)
    j = js.get(key); t = tr.get(key) or tr.get((stem, run))
    E.append(dict(dada2_id=s, station=r["station"], tissue=r["tissue"], run=run, categorie=r["categorie"],
                  plate=r["plate"], well=r["well"], well_col=r["well_col"],
                  brut=j[0] if j else np.nan, retire_12S=j[1] if j else np.nan, apres_12S=j[2] if j else np.nan,
                  dada2_input=t.input if t is not None else np.nan, dada2_filtered=t.filtered if t is not None else np.nan,
                  dada2_merged=t.merged if t is not None else np.nan, dada2_nonchim=t.nonchim if t is not None else np.nan,
                  final=depth[s]))
E = pd.DataFrame(E)
manq = int(E.brut.isna().sum() + E.dada2_input.isna().sum())
E["part_12S"] = E.retire_12S / E.brut
E["rendement_dada2"] = E.dada2_nonchim / E.dada2_input
E["rendement_decontam"] = E.final / E.dada2_nonchim
E.to_csv(OUT + "etapes_par_echantillon.tsv", sep="\t", index=False)
E["groupe"] = np.where(E.station == LAR, np.where(E.tissue == "caudale", "Largue caudale", "Largue autres tissus"),
                       np.where(E.tissue == "caudale", "caudale autres stations", "autres tissus autres stations"))
G = E.groupby(["groupe", "run"]).agg(n=("final", "size"), brut=("brut", "median"), part_12S=("part_12S", "median"),
                                     apres_12S=("apres_12S", "median"), rendement_dada2=("rendement_dada2", "median"),
                                     rendement_decontam=("rendement_decontam", "median"), final=("final", "median"))
G.round(3).to_csv(OUT + "etapes_resume.tsv", sep="\t")
LC = E[(E.station == LAR) & (E.tissue == "caudale")]
with open(OUT + "resume.txt", "w") as fh:
    fh.write(f"A. témoin : écarts max avec retention_par_categorie.tsv = {max(ecarts.values())} sur {len(m)} lignes\n")
    q = R[(R.tissu == "caudale") & (R.run != "tous")]
    fh.write(q[["passe", "run", "profondeur", "n_Hy_avec", "retention_Hy_avec", "retention_Pt_avec", "ecart_Pt_moins_Hy_avec",
                "n_Hy_sans", "retention_Hy_sans", "retention_Pt_sans", "ecart_Pt_moins_Hy_sans"]].to_string(index=False) + "\n\n")
    lh = [r for r in S if r["station"] == LAR and r["tissue"] == "caudale"]
    fh.write("Largue caudale, échantillons par catégorie (3 runs) : " + str(collections.Counter(r["categorie"] for r in lh)) + "\n\n")
    fh.write(f"B. clés manquantes (JSON ou suivi DADA2) : {manq}\n" + G.round(3).to_string() + "\n\n")
    fh.write("Largue caudale : plaques " + str(LC.plate.value_counts().to_dict()) + " ; colonnes " + str(LC.well_col.value_counts().sort_index().to_dict()) + "\n")
    oth = E[(E.station != LAR) & (E.tissue == "caudale")]
    fh.write("caudale autres stations : plaques " + str(oth.plate.value_counts().to_dict()) + "\n")
print(open(OUT + "resume.txt").read())
