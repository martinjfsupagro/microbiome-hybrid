# Recalcul des analyses par catégorie — classification à 25 chromosomes, deux passes

**2026-09-25.** Conversation d'analyse, en réponse à `docs/recalcul_categories_8.8_8.9.md`.
Commits `bb93a53` (métadonnées, scripts 17/18/19/20/24/26) et `70205b7` (script 27).
Sorties dans `results/recat/{morpho,aout,2,1}/` et `results/recat/temoin_effectif/` ; les sorties
d'août (`results/position_effect`, `var_partition_cat`, `var_partition_cat_d500`, `permdisp`) ne
sont pas écrasées. Correspondance valeur par valeur : `docs/recalcul/correspondance_ancien_nouveau.csv`.
Aucune modification d'`Article.docx` ; pas de métrique principale choisie (D7) ; station et
catégorie non dissociées (D2) ; quasi-purs exclus, pas reversés, en passe 1.

Passe 1 = 20 hybrides intermédiaires, quasi-purs exclus, n = 158. Passe 2 = 42 hybrides, n = 180.

## 1. Ce qui garantit que les chiffres sont comparables

- **Métadonnées.** `analysis_metadata.csv` : `categorie` = septembre (59/42/79), `categorie_aout_12chr`
  conservée (59/30/91), `type_genome` (20/22/138), `inclus_passe1` (158). Témoin : la classe d'août
  portée par le fichier de septembre concorde avec la colonne P d'août pour les 180 individus. Diff
  avec l'ancienne table : seule `categorie` change (189 échantillons, 16 individus).
- **Reproduction.** Les scripts modifiés, relancés en mode « août », reproduisent **au bit près** les
  sorties d'août : 17, 18 et 20 (R² et p identiques, 768 + 192 + 216 + 144 lignes), ainsi que toutes les
  valeurs citées des §8.6, 8.8, 8.9 et des Tables S6, S8, S9. PERMDISP reproduit les distances
  exactement ; ses p-values diffèrent par bruit Monte-Carlo seulement (le script d'août n'avait pas de
  graine) : 2 basculements de significativité sur 156 tests. **Cet ordre de bruit vaut pour toute
  comparaison de comptes de strates significatives ci-dessous.**
- **Deux défauts du manuscrit mis au jour par cette reproduction** :
  1. La **Table S6 et le V = 0,48 du §8.8 n'ont jamais utilisé la classification génotypique** : les
     scripts 17 et 18 lisaient le taxon **morphologique** (Ch / Cn / Pt) de `samples_all.csv`. Le
     témoin « stations à une seule catégorie » (20/24, ratio 2,11) portait sur **quatre** codes de site
     (Bau, Caa, Jus, Per — le texte dit « five ») qui ne comptaient que des « Ch », c'est-à-dire des
     poissons **non résolus**. Génotypés, ces sites portent 2 ou 3 catégories, et **aucun code de site
     n'est mono-catégorie sous aucune classification** : ce témoin ne contrôlait pas la catégorie
     génotypique et n'existe plus. Je l'ai remplacé par des sous-ensembles intra-catégorie.
  2. Le §8.9 compare « 1,4 % à 2,7 % » pour la catégorie (**médiane** des 48 strates dans les deux
     ordres) à « 14 % à 36 % » pour la station (**minimum–maximum** des strates). Ce sont deux agrégats
     différents dans la même phrase.

## 2. Ce qui tient

- **Plan.** 3 stations à trois catégories (74 individus en passe 2, 65 en passe 1). Sous-plan
  séparable trop mince dans toutes les passes (32 / 31 individus dans ces stations). V catégorie ×
  colonne fort partout : 0,505 (août), 0,479 (passe 2), 0,527 (passe 1), au niveau individu comme au
  niveau échantillon.
- **Effet de colonne de plaque.** 24/24 strates dans les trois passes. En août comme en passe 2, les
  sorties sont identiques, car la colonne ne dépend pas des étiquettes ; en passe 1, seul l'effectif
  change (ratio 1,84 au lieu de 1,95, p max 0,033). Rangée 6–7/24, bord 0/24.
- **Parts de variance.** Catégorie 1,3–3,7 %, station 14–29 % (médianes par métrique), dans toutes les
  passes. Aucun tissu n'est détecté par les quatre métriques dans les deux schémas, dans aucune passe,
  avec ou sans position.
- **La forme « dispersion » de l'hypothèse transgressive reste non soutenue.** En schéma station
  bloquée, les hybrides sont les moins dispersés dans 31 (août), 34 (passe 2) et 32 (passe 1) tests
  sur 48. En UniFrac pondéré, la dispersion caudale reste homogène dans toutes les passes.
- **La sélection par la profondeur reste orientée** contre les hybrides dans la caudale : 30,4 points
  en août, 19,8 en passe 2, 36,4 en passe 1.
- **Seule détection robuste présente dans les six combinaisons** (3 passes × avec/sans position) :
  **Jaccard dans le midgut** (3/3 runs, séquentiel et station bloquée).

## 3. Ce qui tombe

- **Le signal de la nageoire caudale en UniFrac pondéré — le résultat central du §8.9 — ne tient pas
  en passe 2.** En août : 3/3 runs dans les deux schémas. En passe 2 : 0/0 avec position (p
  séquentiel 0,19–0,33, p bloqué 0,12–0,15) comme sans position (p bloqué 0,073–0,095). En passe 1, il
  revient à 3/3 dans les deux schémas, avec et sans position.
  **Cause établie par un témoin** : parmi 20 retraits aléatoires de 22 poissons non quasi-purs depuis
  la passe 2, **aucun** ne restaure le signal (0/20, dans les quatre modèles). Son retour en passe 1
  tient donc à l'**identité** des 22 poissons retirés — la définition des hybrides — et non à la baisse
  d'effectif. Autrement dit, le signal existe quand « hybride » désigne les génomes intermédiaires, et
  disparaît quand on y ajoute les quasi-purs.
  *Hypothèse, non testée isolément* : 13 des 16 changements de classe sont des Pt → Hy. Inclure des
  quasi-purs à fond Pt diluerait le contraste Hy–Pt.
- **« Inchangé à 500 lectures » ne tient plus.** *(Corrigé le 2026-09-25 : la première version de cette
  note ne rapportait que le modèle avec position.)* Dans le modèle **principal** (sans position), la
  caudale en UniFrac pondéré à 500 lectures est **partielle en passe 1** (séquentiel 3/3, p 0,022–0,049 ;
  station bloquée 1/3, p 0,034–0,073) et **absente en passe 2** (p 0,055–0,177). Avec position, elle est
  absente dans les deux passes (passe 1 : p 0,069–0,141). Le témoin d'effectif n'a pas été lancé à 500 :
  la cause de l'affaiblissement en passe 1 (effectif ou profondeur) n'est pas établie.
- **« Le hindgut est le plus faible » ne tient pas en passe 2.** Modèle principal : en schéma station
  bloquée, les quatre métriques le détectent dans les 3 runs (séquentiel : BC 2/3, UF pondéré 1/3, J et
  UF non pondéré 0/3). En passe 1, il redevient le plus faible (seul Jaccard, 1/3 en bloqué). *(Corrigé :
  la première version attribuait cette baisse « surtout à l'effectif », ce qui ne vaut que pour le
  modèle avec position.)* Dans le modèle principal, le témoin ne tranche pas : indéterminé pour BC, J et
  UF non pondéré (5 à 25 % des retraits aléatoires reproduisent la baisse), définition des hybrides pour
  UF pondéré.
- **Témoin Rosières en passe 1** : avec 1 hybride pour 18 Pt, la permutation libre n'offre que 17 à 19
  arrangements distincts, soit un p minimal de 0,053 à 0,059, et le midgut n'a aucun hybride. Les
  6/36 tests significatifs après position y sont portés par **un seul poisson** ; ils ne sont pas
  interprétables comme un effet de catégorie.

## 4. Ce qui apparaît

- **Le témoin propre Rosières détecte un effet en passe 2** : branchie, Jaccard et UniFrac non
  pondéré, 3/3 runs, avec et sans position (p 0,007–0,030). En août, il ne détectait rien (0/48).
  C'est la seule station où catégorie et position sont indépendantes.
- **PERMDISP en passe 2 : 5 tests intra-station significatifs dans le sens transgressif.** Tous
  portent sur la branchie de Saint-Just, avec 3 ou 4 Pt par strate ; Saint-Just n'est testable qu'en
  passe 2. Sur les 68 strates intra-station **communes aux trois passes**, les hybrides restent les
  moins dispersés partout (p = 1×10⁻⁴, 0,024, 3×10⁻⁸). Le Canal bascule en passe 2 (10/24 « plus
  dispersés »). Là où la dispersion diffère, la catégorie la plus variable passe de la caudale au
  midgut. L'écart médian en UniFrac pondéré change de signe en passe 2 (−0,005 contre +0,002).

## 5. Décision D2 : les conclusions diffèrent entre les modèles avec et sans position

C'est à remonter, pas à trancher ici. Sur les 32 cellules de la Table S8 (16 par passe), **14 diffèrent** (7 par passe), dont **8
changent de classe** (5 en passe 1, 3 en passe 2) (robuste 3/3 ↔ partiel ↔ aucun). Détail dans `d2_avec_vs_sans_position.csv`.
Exemples : en passe 2, Jaccard/hindgut et UniFrac non pondéré/midgut perdent leur robustesse sans
position ; en passe 1, Bray-Curtis/branchie devient robuste sans position. **Le résultat caudal en
UniFrac pondéré ne dépend pas de ce choix** : il est présent en passe 1 et absent en passe 2, avec
comme sans position.

## 6. Faisabilité des permutations en passe 1

Les schémas à station bloquée restent largement réalisables : au moins 10¹⁸ arrangements dans la
strate la plus petite (10²⁴ par blocs de site). Deux cas ne le sont pas :
- **Rosières**, voir ci-dessus ;
- **PERMDISP intra-station** : les 12 strates de Saint-Just sont sautées (1 hybride), 1 sur 12 à
  Büech. Le Canal est sauté en caudale et dans d'autres tissus dans toutes les passes (6/12 strates),
  faute d'échantillons après raréfaction.
`faisabilite_permutations.csv` donne le détail par strate.

## 7. Hors périmètre, mais à signaler

- **Dépôt ENA.** Les identités d'hôte de `PRJEB124417` ont été corrigées le 31 août avec la
  classification d'août. **63 échantillons déposés (16 individus) portent désormais une identité
  périmée** : 51 Pt → Hy, 4 Cn → Hy, 4 Hy → Pt, 4 Hy → Cn. Le paragraphe « Host identity » du
  supplément passe de 369/236/122 à 322/236/169.
- Le §1 doit ajouter « 175 génotypés par Q-scores sur le foie, 5 identifiés à partir d'autres
  tissus » ; les reclassements morphologiques passent de 8 sur 49 à 9 sur 49.
