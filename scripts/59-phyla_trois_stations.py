#!/usr/bin/env python3
"""59-phyla_trois_stations.py — composition en phylums par tissu et catégorie génotypique, restreinte aux stations
qui portent les trois catégories (décision de JF du 2026-10-06 : figure supplémentaire à un seul panneau, groupes
comparés à stations égales). Remplace le panneau b « stations confondues » de la version provisoire.

Règles (fixées avant calcul) :
  - entrée : results/phyla_composition/profils_individus.tsv (scripts/58, commit 33257e3) : profils individu x tissu,
    librairies >= 3 000 lectures, mêmes 12 phylums + « Other phyla » + « Unassigned » ;
  - stations : celles où les trois catégories sont présentes parmi les 180 individus (attendu : 3 stations, 74
    individus) ; catégories Cn, Hy (les 42 hybrides, passe 2), Pt ;
  - dans chaque tissu, une station est retenue si chacune des trois catégories y a au moins 2 profils ;
  - barre = moyenne, sur les stations retenues, du profil moyen de la catégorie dans la station (poids égal par
    station, identique pour les trois catégories) ; la moyenne pondérée par individu est écrite pour comparaison.
Sorties : results/phyla_composition/{trois_stations.tsv, trois_stations_par_station.tsv, trois_stations_resume.txt}
Python système. Lancer depuis la racine du dépôt.
"""
import numpy as np, pandas as pd

OUT = "results/phyla_composition/"; MIN_N = 2
P = pd.read_csv(OUT + "profils_individus.tsv", sep="\t")
PHY = [c for c in P.columns if c not in ("individual_id", "tissue", "station", "groupe")]
assert len(PHY) == 14 and np.allclose(P[PHY].sum(1), 1)
P["cat"] = P.groupe.map({"Cn": "Cn", "Pt": "Pt", "Hy_int": "Hy", "Hy_nearp": "Hy"}); assert P.cat.notna().all()

md = pd.read_csv("metadata/analysis_metadata.csv").drop_duplicates("individual_id")
TRI = sorted(s for s, g in md.groupby("station") if set(g.categorie) == {"Cn", "Hy", "Pt"})
assert TRI == ["Canal (usine du Largue)", "Confluence Buech-Meouge", "Saint-Just-d'Ardeche"], TRI
assert md.station.isin(TRI).sum() == 74
S = P[P.station.isin(TRI)]

per = S.groupby(["tissue", "station", "cat"])
PS = per[PHY].mean().join(per.size().rename("n")).reset_index()
PS.to_csv(OUT + "trois_stations_par_station.tsv", sep="\t", index=False, float_format="%.6g")

rows, log = [], []
for tis, t in PS.groupby("tissue"):
    ok = [st for st, g in t.groupby("station") if set(g.cat) == {"Cn", "Hy", "Pt"} and (g.n >= MIN_N).all()]
    log.append(f"{tis} : stations retenues {len(ok)} / 3 : {', '.join(ok)}")
    for cat in ("Cn", "Hy", "Pt"):
        g = t[(t.station.isin(ok)) & (t.cat == cat)]
        assert len(g) == len(ok)
        bal = g[PHY].mean()                                                   # poids égal par station
        ind = S[(S.tissue == tis) & (S.station.isin(ok)) & (S.cat == cat)]
        rows.append(dict(tissu=tis, categorie=cat, n=int(g.n.sum()), n_stations=len(ok),
                         n_par_station="; ".join(f"{s}={int(v)}" for s, v in zip(g.station, g.n)),
                         **{p: bal[p] for p in PHY}, **{f"{p}__pondere_individu": ind[p].mean() for p in PHY}))
R = pd.DataFrame(rows)
assert np.allclose(R[PHY].sum(1), 1)
R.to_csv(OUT + "trois_stations.tsv", sep="\t", index=False, float_format="%.6g")
with open(OUT + "trois_stations_resume.txt", "w") as f:
    f.write(f"stations : {TRI} ; individus : 74 ; profils retenus : {len(S)}\n" + "\n".join(log) + "\n")
    f.write(R[["tissu", "categorie", "n", "n_stations", "n_par_station"]].to_string(index=False) + "\n")
    f.write("\nécart max (points) équilibré vs pondéré par individu : %.1f\n" %
            (100 * max(abs(R[p] - R[f"{p}__pondere_individu"]).max() for p in PHY)))
print(open(OUT + "trois_stations_resume.txt").read())
