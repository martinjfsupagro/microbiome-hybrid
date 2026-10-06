#!/usr/bin/env python3
"""60-phyla_tous_poissons.py — composition en phylums par tissu, tous poissons réunis (panneau a de la figure S4,
décision de JF du 2026-10-06 : « 4 tissus pour tous les poissons ensemble, la station est l'effet le plus fort » ;
panneau b = trois stations à trois catégories, scripts/59).

Règles (fixées avant calcul) :
  - entrée results/phyla_composition/profils_individus.tsv (scripts/58 : librairies >= 3 000 lectures, moyenne
    des librairies d'un individu x tissu) ; les 12 phylums affichés et « Other phyla » / « Unassigned » de scripts/58 ;
  - barre = moyenne des profils individu x tissu du tissu, toutes stations et catégories : chaque poisson pèse
    autant (même règle que scripts/58) ;
  - témoins écrits à côté : (i) moyenne à poids égal par station (sensibilité au déséquilibre d'échantillonnage
    entre stations), écart maximal rapporté ; (ii) la moyenne des 4 barres pondérée par n doit redonner
    abondance_moyenne de phyla.tsv (même ensemble de profils).
Sorties : results/phyla_composition/{tous_poissons.tsv, tous_poissons_resume.txt}
Python système (/usr/bin/python3). Lancer depuis la racine du dépôt.
"""
import numpy as np, pandas as pd

OUT = "results/phyla_composition/"
P = pd.read_csv(OUT + "profils_individus.tsv", sep="\t")
PHY = [c for c in P.columns if c not in ("individual_id", "tissue", "station", "groupe")]
assert len(PHY) == 14 and np.allclose(P[PHY].sum(1), 1), "profils non normalisés"
assert not P.duplicated(["individual_id", "tissue"]).any()
assert len(P) == 628 and P.individual_id.nunique() == 180, (len(P), P.individual_id.nunique())

rows, log = [], []
for tis, t in P.groupby("tissue"):
    ind = t[PHY].mean()                                          # chaque poisson pèse autant
    sta = t.groupby("station")[PHY].mean().mean()                # chaque station pèse autant
    r = dict(tissu=tis, n=len(t), n_stations=t.station.nunique(),
             n_par_categorie="; ".join(f"{k}={v}" for k, v in t.groupby("groupe").size().items()))
    r.update(ind.to_dict()); r.update({p + "__poids_station": sta[p] for p in PHY})
    rows.append(r)
    log.append(f"{tis} : n={len(t)}, stations={t.station.nunique()}, écart max individu vs station = "
               f"{(ind - sta).abs().max() * 100:.1f} points ({(ind - sta).abs().idxmax()})")
R = pd.DataFrame(rows)
glob = (R[PHY].mul(R.n, axis=0).sum() / R.n.sum())
ph = pd.read_csv(OUT + "phyla.tsv", sep="\t").set_index("phylum").abondance_moyenne
com = [p for p in PHY if p in ph.index]
ecart = (glob[com] - ph[com]).abs().max()
log.append(f"témoin (ii) : écart max moyenne pondérée vs phyla.tsv = {ecart:.2e} sur {len(com)} phylums")
assert ecart < 1e-5, ecart
R.to_csv(OUT + "tous_poissons.tsv", sep="\t", index=False, float_format="%.6g")
with open(OUT + "tous_poissons_resume.txt", "w") as f:
    f.write("\n".join(log) + "\n")
print(open(OUT + "tous_poissons_resume.txt").read())
