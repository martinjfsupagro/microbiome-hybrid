#!/usr/bin/env python3
"""58-phyla_composition.py — abondance relative moyenne des phylums par tissu, pour une figure supplémentaire
analogue à la Figure 5 de Guivier et al. 2017 (demande de JF et André, 2026-10-06).

Règles (fixées avant calcul, reprises dans la légende) :
  - table results/decontam/asv_table_clean.tsv (2 180 librairies) ; taxonomie results/dada2_final/taxonomy.tsv
    (SILVA 138.2, noms de phylums actuels) ; métadonnées metadata/analysis_metadata.csv (clé dada2_id) ;
  - librairies d'au moins 3 000 lectures (1 784, l'ensemble des analyses de composition) ;
  - abondance relative par librairie, cumulée par phylum ; ASV sans phylum -> « Unassigned » ;
  - moyenne des librairies d'un même individu x tissu (runs et ré-extractions « bis »), puis moyenne entre
    individus : chaque poisson pèse autant ;
  - panneau a : P. toxostoma, tissu x station ; panneau b : Cn, Hy intermédiaires, Hy quasi-purs, Pt, tissu,
    stations confondues ;
  - phylums affichés : les 12 de plus forte abondance moyenne sur l'ensemble des profils individu x tissu ;
    les autres -> « Other phyla ».
Sorties : results/phyla_composition/{profils_individus.tsv, moyennes.tsv, phyla.tsv, resume.txt}
Python système (/usr/bin/python3). Lancer depuis la racine du dépôt.
"""
import csv, os, collections
import numpy as np, pandas as pd

OUT = "results/phyla_composition"; os.makedirs(OUT, exist_ok=True)
MIN_DEPTH, N_TOP = 3000, 12

tax = pd.read_csv("results/dada2_final/taxonomy.tsv", sep="\t", dtype=str)
assert {"ASV", "Phylum"} <= set(tax.columns)
phy_of = dict(zip(tax.ASV, tax.Phylum.fillna("Unassigned").replace({"NA": "Unassigned"})))

with open("results/decontam/asv_table_clean.tsv") as fh:
    hdr = fh.readline().rstrip("\n").split("\t")[1:]
    assert len(hdr) == 2180, len(hdr)
    acc = collections.defaultdict(lambda: np.zeros(len(hdr)))
    n_asv = 0
    for line in fh:
        v = line.rstrip("\n").split("\t")
        assert v[0] in phy_of, f"ASV sans taxonomie : {v[0]}"
        acc[phy_of[v[0]]] += np.array([float(x) if x else 0.0 for x in v[1:]])
        n_asv += 1
P = pd.DataFrame(acc, index=hdr)                      # librairies x phylums, lectures
depth = P.sum(axis=1)
keep = depth[depth >= MIN_DEPTH].index
assert len(keep) == 1784, len(keep)
R = P.loc[keep].div(depth[keep], axis=0)              # abondances relatives
assert np.allclose(R.sum(axis=1), 1)

md = pd.read_csv("metadata/analysis_metadata.csv").set_index("dada2_id")
assert set(keep) <= set(md.index)
M = md.loc[keep, ["individual_id", "tissue", "station", "categorie", "type_genome"]]
grp = np.where(M.categorie == "Hy", np.where(M.type_genome == "intermediaire", "Hy_int", "Hy_nearp"), M.categorie)
assert set(M.type_genome[M.categorie == "Hy"]) == {"intermediaire", "quasi-pur"}
M = M.assign(groupe=grp)

# profils individu x tissu (moyenne des librairies)
ind = R.join(M).groupby(["individual_id", "tissue"])
prof = ind[list(R.columns)].mean()
meta = ind[["station", "groupe"]].first()
assert (ind.station.nunique() == 1).all() and (ind.groupe.nunique() == 1).all()
prof = prof.join(meta)

ab = prof[list(R.columns)].mean().drop("Unassigned", errors="ignore").sort_values(ascending=False)
top = list(ab.index[:N_TOP])


def collapse(df):
    cols = list(R.columns)
    o = df[top].copy()
    o["Other phyla"] = df[[c for c in cols if c not in top and c != "Unassigned"]].sum(axis=1)
    o["Unassigned"] = df["Unassigned"] if "Unassigned" in df else 0.0
    return o


C = collapse(prof).join(prof[["station", "groupe"]])
C.reset_index().to_csv(f"{OUT}/profils_individus.tsv", sep="\t", index=False, float_format="%.6g")
show = top + ["Other phyla", "Unassigned"]
rows = []
for (tis, st), s in C[C.groupe == "Pt"].groupby(["tissue", "station"]):
    rows.append(dict(panneau="a", tissu=tis, groupe="Pt", station=st, n=len(s), **s[show].mean().to_dict()))
for (tis, g), s in C.groupby(["tissue", "groupe"]):
    rows.append(dict(panneau="b", tissu=tis, groupe=g, station="toutes", n=len(s), **s[show].mean().to_dict()))
Mo = pd.DataFrame(rows)
assert np.allclose(Mo[show].sum(axis=1), 1)
Mo.to_csv(f"{OUT}/moyennes.tsv", sep="\t", index=False, float_format="%.6g")
pd.DataFrame({"phylum": ab.index, "abondance_moyenne": ab.values, "affiche": [p in top for p in ab.index]}).to_csv(
    f"{OUT}/phyla.tsv", sep="\t", index=False, float_format="%.6g")

with open(f"{OUT}/resume.txt", "w") as f:
    f.write(f"ASV lus : {n_asv} ; librairies : {len(hdr)} ; retenues (>= {MIN_DEPTH}) : {len(keep)}\n")
    f.write(f"profils individu x tissu : {len(prof)} ; individus : {prof.index.get_level_values(0).nunique()}\n")
    f.write(f"part moyenne non assignée au phylum : {prof['Unassigned'].mean():.4f}\n")
    f.write("phylums affichés : " + ", ".join(f"{p} ({ab[p]:.3f})" for p in top) + "\n")
    f.write(f"part moyenne des autres phylums : {C['Other phyla'].mean():.4f}\n")
    f.write("effectifs panneau a (Pt, tissu x station) :\n" + Mo[Mo.panneau == "a"].pivot(index="station", columns="tissu", values="n").to_string() + "\n")
    f.write("effectifs panneau b (groupe x tissu) :\n" + Mo[Mo.panneau == "b"].pivot(index="groupe", columns="tissu", values="n").to_string() + "\n")
print(open(f"{OUT}/resume.txt").read())
