# Plan — contrôle « campagne de pêche » (2026-10-06, décidé par JF : « teste le contrôle campagne »)

## Origine
Ordinations du script 65 (figure candidate, version b1) : à Confluence Buëch-Méouge, les échantillons de nageoire
caudale, branchie et midgut se séparent par campagne (2014 / 2015). Or, dans les stations pêchées deux fois, les
hybrides sont surtout de la seconde campagne (Buëch 2014 : 7 Cn / 2 Hy / 8 Pt, 2015 : 4 / 8 / 6 ; Avignon et
Pont-d'Ain : Hy en 2015 seulement). Les tests de l'article bloquent les permutations par station, pas par campagne :
un effet de campagne pourrait se lire comme un effet de catégorie. **Hypothèse, non établie.**

## Définition de la campagne (fixée avant calcul)
Campagne = station × année (colonne `annee`), sauf Pertuis, scindée selon André (2026-09-30) : série 1011–1014 le
2014-07-07, série 2011–2015 le 2014-08-20 (colonne `individual`). La colonne `date_collecte` porte encore
l'intervalle pour Pertuis et deux dates pour Avignon et Buëch : elle n'est pas utilisée. 14 blocs attendus
(Avignon 2, Largue 1, Chavannes 2, Buëch 2, Manosque 1, Pertuis 2, Pont-d'Ain 2, Rosières 1, Saint-Just 1).

## Tests (mêmes matrices, strates et échantillons que scripts/20 via results/recat)
Strates : 4 métriques (BETA-BRAY, BETA-JAC, BETA-UUF, BETA-WUF) × 3 runs × 4 tissus × 2 passes = 96.
- **T0, référence** : modèle principal de l'article, `adonis2(D ~ cat)`, permutations dans les blocs de station,
  999 permutations, même graine et même séquence d'appels que scripts/20 (aN1, aN2 puis aN3). **Témoin de
  montage** : p et R² identiques à `sanspos_cat_station_bloquee` de `results/recat/{1,2}/var_partition_cat/
  category_partition.tsv`. Si ce témoin échoue, aucun autre résultat n'est lu.
- **T1, contrôle** : même modèle, permutations dans les blocs station × campagne, même graine que T0.
- **T2, part de variance** : R² de la catégorie servie après les blocs station × campagne
  (`D ~ blk + cat`), comparé au R² servi après la station (`sanspos_MIN_st_cat`).
- **T3, témoin d'effet de campagne sans hybrides** : parentaux seuls (Cn, Pt), stations pêchées deux fois,
  `adonis2(D ~ campagne)`, permutations dans les blocs station × catégorie. Isole l'effet de la campagne de celui
  de la catégorie hybride. Par passe : sans objet (les parentaux sont les mêmes) → 48 strates.

## Lecture (fixée avant calcul)
1. Par métrique × tissu × passe : nombre de runs (sur 3) à p < 0,05 sous T0 et sous T1. Le résultat robuste de
   l'article (Jaccard midgut, 3/3 runs dans les deux passes, R21) et les détections de la Fig. 3a-b sont relus.
2. Si les détections persistent sous T1 : la campagne ne produit pas les effets de catégorie rapportés.
3. Si des détections disparaissent sous T1 : deux lectures possibles, **confondant** ou **perte de puissance**
   (les blocs à une seule catégorie ne contribuent plus, et les comparaisons entre campagnes sont retirées).
   T2 et T3 départagent sans trancher : chute du R² de la catégorie après station × campagne **et** effet de
   campagne chez les parentaux (T3) → confondant plausible ; R² stable → perte de puissance plus plausible.
   Aucune des deux lectures ne sera énoncée comme établie.
4. Les chiffres de l'article ne sont pas modifiés par ce contrôle tant que JF n'a pas décidé de son intégration
   (§8.12, contrôle déclaré après les résultats, comme le contrôle v).

## Sorties
`scripts/66-controle_campagne.R` → `results/controle_campagne/{campagne_tests.tsv, campagne_parentaux.tsv,
temoin_montage.tsv, blocs.tsv, resume.txt}`.
