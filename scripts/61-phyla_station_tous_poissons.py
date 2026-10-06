#!/usr/bin/env python3
"""61-phyla_station_tous_poissons.py — composition en phylums par tissu x station, tous poissons réunis (panneau a
de la figure S4, décision de JF du 2026-10-06, 3e version : « en panneau a toutes les stations pour tous les tissus,
comme la première figure mais pour tous les poissons » ; panneau b = trois stations à trois catégories, scripts/59).

Règles (fixées avant calcul) :
  - entrée results/phyla_composition/profils_individus.tsv (scripts/58 : librairies >= 3 000 lectures, moyenne
    des librairies d'un individu x tissu) ;
  - barre = moyenne des profils individu x tissu de la station, toutes catégories réunies : chaque poisson de la
    station pèse autant ; effectifs par catégorie écrits à côté (la composition génotypique diffère entre stations,
    Fig. 1a : une barre de station mêle station et catégorie) ;
  - témoins : (i) pour chaque tissu, la moyenne des barres de station pondérée par n redonne la barre « tous
    poissons » de tous_poissons.tsv (scripts/60) ; (ii) leur moyenne non pondérée redonne la colonne __poids_station.
Sorties : results/phyla_composition/{station_tous_poissons.tsv, station_tous_poissons_resume.txt}
Python système (/usr/bin/python3). Lancer depuis la racine du dépôt.
"""
import numpy as np, pandas as pd

OUT = "results/phyla_composition/"
P = pd.read_csv(OUT + "profils_individus.tsv", sep="\t")
PHY = [c for c in P.columns if c not in ("individual_id", "tissue", "station", "groupe")]
assert len(PHY) == 14 and np.allclose(P[PHY].sum(1), 1)
assert len(P) == 628 and P.individual_id.nunique() == 180 and P.station.nunique() == 9

rows = []
for (tis, st), g in P.groupby(["tissue", "station"]):
    r = dict(tissu=tis, station=st, n=len(g),
             n_par_categorie="; ".join(f"{k}={v}" for k, v in g.groupby("groupe").size().items()))
    r.update(g[PHY].mean().to_dict()); rows.append(r)
R = pd.DataFrame(rows)

A = pd.read_csv(OUT + "tous_poissons.tsv", sep="\t").set_index("tissu")
log = []
for tis, t in R.groupby("tissu"):
    assert t.n.sum() == A.loc[tis, "n"], (tis, t.n.sum(), A.loc[tis, "n"])
    e1 = (t[PHY].mul(t.n, axis=0).sum() / t.n.sum() - A.loc[tis, PHY]).abs().max()
    e2 = (t[PHY].mean() - A.loc[tis, [p + "__poids_station" for p in PHY]].values).abs().max()
    assert e1 < 1e-5 and e2 < 1e-5, (tis, e1, e2)
    dom = t.set_index("station")[PHY].idxmax(axis=1)
    log.append(f"{tis} : {len(t)} stations, n={t.n.sum()}, témoins (i) {e1:.1e} (ii) {e2:.1e} ; "
               f"phylum premier : {dom.value_counts().to_dict()} ; n min {t.n.min()} ({t.loc[t.n.idxmin(), 'station']})")
R.to_csv(OUT + "station_tous_poissons.tsv", sep="\t", index=False, float_format="%.6g")
with open(OUT + "station_tous_poissons_resume.txt", "w") as f:
    f.write(f"{len(R)} profils tissu x station\n" + "\n".join(log) + "\n")
print(open(OUT + "station_tous_poissons_resume.txt").read())
