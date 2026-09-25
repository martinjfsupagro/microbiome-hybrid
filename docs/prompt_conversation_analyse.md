# Recalcul des analyses par catégorie génotypique avec la classification à 25 chromosomes

## Contexte

Les analyses par catégorie génotypique (partition de variance, PERMDISP, effet de position, et les
§1, §8.8 et §8.9 du manuscrit qui en découlent) ont été faites avec la **classification d'août
2026, établie sur 12 chromosomes** : 59 Cn / 30 Hy / 91 Pt. André a livré en septembre une
classification sur **25 chromosomes**, vérifiée contre les Q-values par chromosome : 59 Cn / 42 Hy /
79 Pt. **16 individus sur 180 changent de classe.** Le fichier `metadata/analysis_metadata.csv`,
colonne `categorie`, porte encore la classification d'août pour les 180 individus.

Tout est versé dans le dépôt `~/work/projects/microbiome-hybrid` (commits `6437e15` et suivants).
Lis en premier `docs/recalcul_categories_8.8_8.9.md`, qui détaille le constat.

## Ce qui a été décidé et encadre le recalcul

**Deux définitions d'« hybride », deux passes (décision D1, tranchée par André le 25 septembre).**
La classe Hy de septembre réunit deux sous-types : 20 génomes intermédiaires et 22 quasi-purs,
parentaux sur presque tout le génome mais introgressés sur un chromosome dans la plupart des cas.
André tient que les 22 sont des hybrides et ne peuvent pas être traités comme purs. D'où :

- **passe 1** — 20 hybrides intermédiaires, les **22 quasi-purs exclus** de l'analyse, pas reversés
  dans leur classe parentale : n = 158 individus ;
- **passe 2** — les 42 hybrides : n = 180.

La classification d'août ne correspond à aucune des deux. Ses 30 Hy contiennent les 20
intermédiaires, 8 des 22 quasi-purs, et 2 individus que les 25 chromosomes classent purs
(`2015_Bue_1006`, devenu Pt ; `2015_Jus_1011`, devenu Cn). Les 14 autres quasi-purs étaient classés
parentaux en août. **Il faut donc recalculer deux fois, pas une.**

**Station et catégorie ne sont pas dissociées (D2).** André considère le lien comme biologiquement
causal (température de l'eau, sensibilité du hotu) et demande de rapporter les patterns observés
sans chercher à séparer les deux effets. **Il demande aussi d'abandonner l'effet de position.**
Or le manuscrit actuel (§8.6 et §8.8) fait entrer la colonne de plaque comme covariable dans chaque
modèle testant la catégorie. Recommandation retenue côté conception : sortir la position du modèle
principal comme demandé, mais **conserver en supplément une analyse de sensibilité qui l'inclut**,
puisqu'elle est mesurée comme réelle dans les 24 strates. Si les conclusions diffèrent entre les
deux versions, c'est un résultat à remonter, pas à trancher seul.

**Une information nouvelle sur l'effet de position.** André explique que les numéros suivent
l'ordre de prélèvement : les hotus, plus fragiles, sont prélevés en priorité, sauf une fois
(Saint-Just, d'où l'inversion du motif). La plaque a été chargée dans l'ordre de numérotation à cinq
stations sur neuf (rho de Spearman numéro × colonne : Rosières 0,950, Saint-Just 0,932, canal
0,931, Manosque 0,908, Pertuis 0,866). Le §8.8 dit le mécanisme « non identifié » : il a maintenant
une origine documentée pour l'association, même si l'on ne sait toujours pas si l'effet colonne
vient de l'extraction ou du délai entre capture et dissection.

**La métrique reste ouverte (D7).** Ne choisis pas de métrique principale : recalcule sur les
quatre métriques déjà utilisées, en conservant la structure actuelle des analyses.

## Ce que je te demande

1. **Régénérer les métadonnées d'analyse.** Dans `analysis_metadata.csv`, remplacer `categorie` par
   la classe de septembre et ajouter une colonne de passe (`intermediaire` / `quasi-pur` / `pur`),
   à partir de `metadata/genotypes_verifies_sept_180.csv` (colonnes `individual_id`,
   `classe_sept_25chr`, `type_genome`). Conserver l'ancienne classe dans une colonne distincte
   (`categorie_aout_12chr`), sans l'écraser : les deux doivent rester traçables. Vérifier après
   jointure : 180 individus, 59 / 42 / 79, et 20 / 22 / 138 pour `type_genome`.
2. **Relancer en deux passes** les analyses qui utilisent la catégorie : partition de variance par
   catégorie, PERMDISP, et les tests de position — soit, d'après leurs noms, les scripts 17, 18,
   20 et 24, et le script 19 pour les métadonnées. Vérifie dans `runs.log` s'il y en a d'autres ; les scripts qui
   ne touchent pas la catégorie n'ont pas à être relancés.
3. **Recompter les éléments structurels du plan dans chaque passe** :
   - stations portant les trois catégories — aujourd'hui 3 stations, 74 individus. Passe 2 : Büech
     11/10/14, canal 8/6/6, Saint-Just 9/6/4 = 74. Passe 1 : Büech 11/8/14, canal 8/4/6, Saint-Just
     9/1/4 = 65, **Saint-Just ne gardant qu'un hybride** ;
   - le sous-plan où catégorie et position sont séparables à station constante (aujourd'hui 32
     individus) ;
   - le témoin indépendant **Rosières** (V = 0,181 en août) : 0/4/21 en août, 0/7/18 en passe 2,
     **0/1/18 en passe 1** — en passe 1 il ne témoigne plus de rien ;
   - le V de Cramér catégorie × colonne de plaque. Attention : le 0,48 du §8.8 vient du **taxon
     morphologique d'avant génotypage** (0,477 dans `docs/roadmap_analyse.md`), pas de la
     classification d'août (0,504). Valeurs recalculées côté conception au niveau individu :
     0,505 (août), 0,479 (passe 2), 0,527 (passe 1). À confirmer au niveau où tu travailles.
4. **Dire ce qui change.** Pour chaque résultat des §8.8 et §8.9 et des Tables S6 et S8 : valeur
   d'août, valeur passe 1, valeur passe 2, et si la conclusion tient. En particulier : le signal de
   la nageoire caudale en UniFrac pondéré sur les trois runs et les deux schémas, et la faiblesse du
   hindgut.

## Livrables attendus

- `analysis_metadata.csv` régénéré, commité ;
- les sorties des scripts relancés dans `results/`, tracées dans `runs.log` comme d'habitude ;
- **une table de correspondance** ancien → nouveau, une ligne par valeur citée dans le manuscrit :
  emplacement (§1, §8.8, §8.9, Table S1, S6, S8, Note S2), valeur actuelle, valeur passe 1, valeur
  passe 2 ;
- une courte note de résultats : ce qui tient, ce qui tombe, ce qui apparaît. Distinguer ce qui
  change parce que les étiquettes ont changé de ce qui change parce que l'effectif a baissé en
  passe 1.

## Ce qui n'est pas à faire ici

- ne pas modifier `Article.docx` : une autre conversation rédige, elle reprendra ta table de
  correspondance ;
- ne pas choisir la métrique principale (D7 ouverte) ;
- ne pas chercher à séparer station et catégorie (D2) ;
- ne pas reverser les quasi-purs dans les classes parentales en passe 1 : ils sont **exclus**.

## Points de vigilance

- Les 5 individus sans Q-values (`2014_Bue_1001`, `2014_Bue_1002`, `2015_Bue_1014`, `2015_Cab_1011`,
  `2015_Jus_1008`) sont tous classés purs et génotypés à partir d'autres tissus que le foie. Ils
  restent dans l'analyse ; la formulation des Methods sera « 175 génotypés par Q-scores sur le foie,
  5 identifiés à partir d'autres tissus ».
- Au Büech, la composition est identique entre août et septembre (11/10/14) mais deux étiquettes
  s'échangent : les tests changent quand même.
- En passe 1, la classe Hy tombe à 20 individus et quatre stations n'en gardent qu'un (Saint-Just,
  Rosières, Manosque, Pertuis) : vérifie que les schémas de permutation contraints par station restent
  réalisables dans les strates à petit effectif, et signale ceux qui ne le sont pas.
