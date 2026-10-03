# Résultats des cinq tests du 2026-10-03

Tests déclarés a priori dans `docs/plan_tests_2026-10-03.md` (commit `bd6ba3d`, précisions de mise en
œuvre ajoutées avant calcul), puis exécutés par le job Slurm du 2026-10-03 sur `HEAD` `8e4375d`. Les sept
étapes se sont terminées en code 0. Les verdicts ci-dessous sont ceux que produit
`scripts/36-lecture_tests.py`, écrit avant calcul, et ne sont pas réinterprétés. Sorties :
`results/tests_20261003/` (md5 dans `_etat/DONNEES.md`, entrée `TESTS-1003`).

## Écarts au plan, déclarés

1. **(e) La prémisse du test était fausse, et l'erreur est mienne.** Le plan définissait quatre
   stations « découplées » d'après les ρ de `point_etape_25sept.md` (Chavannes 0,008, Pont-d'Ain 0,17,
   Avignon 0,37, Buëch 0,39). Ces ρ étaient calculés **par station, 2014 et 2015 mélangés**, alors que la
   numérotation repart chaque année. Le contrôle préalable déclaré montre qu'**à l'intérieur de chaque
   campagne**, rang de dissection et colonne restent fortement corrélés (ρ de 0,55 à 0,93 ;
   `spearman_rang_pos.tsv`). Les permutations se faisant dans les campagnes, le test ne peut pas séparer
   les deux variables. Il a été lancé tel que déclaré, mais son verdict est sans portée (voir (e)).
2. **(a2) et le script 35** ont été ajoutés au plan avant tout calcul (précisions du plan).
3. **(b1)** : sur 20 tirages, 20 Pt au total ont dû être tirés hors de la station du quasi-pur qu'ils
   remplaçaient (environ un par tirage) ; aucun Cn.

## (a) Affaiblissement du signal caudal à 500 lectures — UniFrac pondéré, passe 1

- **a1 (témoin d'effectif) : définition.** Aucun des 20 retraits aléatoires de 22 poissons non quasi-purs
  ne reproduit le motif de la passe 1 à 500 lectures (0/20, modèle `ordre_MIN`, 3/3 runs). C'est le même
  résultat qu'à 3 000 lectures (R22).
- **a2 (ensemble constant) : ensemble d'échantillons.** Sur les **mêmes** échantillons, passer de 3 000
  à 500 lectures ne change pas le résultat : significatif en 3/3 runs dans les deux schémas station
  bloquée, p = 0,009–0,023 à 3 000 et 0,010–0,026 à 500. L'ensemble complet à 500 lectures (n = 147–151
  contre 120–124) ne l'est plus (0/3 et 1/3).

**Conclusion.** L'affaiblissement à 500 lectures ne tient pas à la profondeur. Il tient aux échantillons
de caudale qui ne passent le seuil qu'à 500 lectures, ce qui est cohérent avec l'invariance de l'UniFrac
pondéré à la profondeur (R9). *Pourquoi* ces échantillons diluent le signal (bruit des échantillons peu
profonds, ou composition réellement différente) n'est pas isolé : c'est une hypothèse.

## (b) Dilution du contraste Hy–Pt par les quasi-purs à fond Pt — verdict : indéterminée

- **b2** (caudale, UniFrac pondéré, sans position, station bloquée) :
  - QPpt ne diffère pas de Pt (p = 0,60 ; 0,32 ; 0,28 ; R² 0,011–0,018 ; n = 79–86 ; 4 stations portant
    les deux groupes) ;
  - QPpt ne diffère pas non plus des 20 intermédiaires (p = 0,15 ; 0,26 ; 0,24 ; R² 0,050–0,051 ;
    n = 25–26 ; 5 stations).
  
  La règle exigeait les deux conditions : la seconde manque.
- **b1** : la référence sans injection reproduit R22 (p = 0,011–0,027 dans les deux schémas). Réétiqueter
  Hy 19 Pt et 3 Cn tirés dans les mêmes stations ne garde le signal que dans **4 tirages sur 20**.

**Lecture.** Ajouter à la classe Hy des poissons de type Pt suffit, dans 16 tirages sur 20, à faire
disparaître le signal. Cela rend la dilution **suffisante**. En revanche, il n'est pas établi que les
quasi-purs à fond Pt *soient* de type Pt : ils ne se distinguent ni des Pt ni des intermédiaires. Le R²
QPpt–INT est trois à quatre fois plus grand que le R² QPpt–Pt, mais sur environ trois fois moins
d'échantillons, donc non évaluable à cette puissance. Le mécanisme de R22 reste une hypothèse, désormais
compatible avec un témoin d'injection.

## (c) Effet de la catégorie sur la diversité alpha (H1)

Modèle principal `log(x) ~ station + cat`, par tissu, indice et passe ; règle D7 sur les classements.

| passe | tissu | classement établi | indices | p de la catégorie |
|---|---|---|---|---|
| 1 | caudale | **dominant Cn** | 4 sur 4 | 0,012–0,128 |
| 2 | midgut | **dominant Cn** | richesse, Shannon, Faith PD | 0,040–0,111 |
| autres combinaisons (6) | | aucun | | |

« Dominant Cn » signifie que Hy ne se distingue pas de Cn et se distingue de Pt. En caudale (passe 1),
par exemple, l'écart Hy − Pt vaut −0,21 en Shannon (log ; IC −0,36 à −0,05), et l'écart Hy − Cn −0,09
(IC −0,24 à 0,07). C'est une **absence de différence** avec Cn, pas une égalité démontrée.

- **Aucun classement transgressif**, dans aucune combinaison (0 sur 32), ce qui concorde avec PERMDISP
  (R15, R25).
- **Sensibilité à la position.** Le classement de la caudale en passe 1 tient avec position. Celui du
  midgut en passe 2 **ne tient pas** : il devient « intermédiaire » ou indéterminé. Il dépend donc de D2.
- **Multiplicité.** 5 tests de la catégorie sur 32 ont p < 0,05 (environ 1,6 attendu sous H0) ; les
  p-valeurs sont brutes, sans correction.
- **À ne pas négliger.** Les hotus sont traités en premier. La proximité de Hy et de Cn pourrait donc
  être confondue avec l'ordre de traitement, au même titre que l'effet de position (voir (e)). Ce point
  n'est pas testé.

## (d) Partition de la variance alpha — remplace R8

Modèle `lm(log(x) ~ tissue + site_annee + individu + library + run)`, 1 784 échantillons, parts de
somme des carrés :

| indice | tissu (séq. / marg.) | site-année (séq.) | individu (séq. / marg.) | technique (marg.) | résiduel |
|---|---|---|---|---|---|
| richesse | 21,6 % / 19,0 % | 13,5 % | 19,5 % / 19,5 % | 0,25 % | 45,1 % |
| Shannon | 24,9 % / 21,2 % | 9,5 % | 21,3 % / 21,2 % | 0,10 % | 44,2 % |
| inverse Simpson | 29,8 % / 25,6 % | 13,0 % | 18,7 % / 18,6 % | 0,04 % | 38,5 % |
| Faith PD | 23,6 % / 21,0 % | 14,1 % | 16,7 % / 16,7 % | 0,29 % | 45,3 % |

Le classement des facteurs est le même sur les quatre indices : tissu > individu > site-année
≫ technique (au plus 0,3 %). Ces chiffres **ne sont pas comparables** à l'ancien R8 (tissu 18,7 %,
site-année 10,9 %, run 0,26 %, résiduel 69 %). Celui-ci venait d'un diagnostic de conversation sans
script et sans terme individu ; le terme individu absorbe ici une partie de son résiduel.

## (e) Séjour en vivier contre colonne de plaque — sans portée (voir écart 1)

Le verdict mécanique est « indéterminé ». Dans le modèle M1 (n médian 78), `pos` et `rang` ne sont
robustes que pour Bray-Curtis en branchie, **tous les deux dans les mêmes strates**, avec des R² médians
de 0,011 et 0,012. Aucun n'est établi selon D7. M2 (Chavannes seule, n = 17) : rien de robuste.

**Ce que l'on apprend tout de même, et qui vaut pour D2.** Dans **chaque** campagne de pêche, la plaque
a été chargée dans l'ordre de traitement des poissons. L'« effet de position » (R14) et un éventuel effet
de la durée de séjour en vivier ou de l'ordre de manipulation sont donc **inséparables dans ce
dispositif**, à toutes les stations et pas seulement à cinq. Ce n'est pas une limite de puissance : c'est
une propriété du plan d'échantillonnage, que ce test ne pouvait pas lever. La covariable de position
devrait être décrite comme « colonne de plaque, confondue avec l'ordre de traitement ».
