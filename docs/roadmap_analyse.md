# Étapes avant l'analyse de la variation du microbiote par catégorie de poisson

État au 2026-08-30. Audit du dépôt : 18 scripts, tous techniques ou QC — **aucun script
d'analyse écologique n'existe encore**. Index hybride : 131 des 180 individus restent à
génotyper.

---

## A. Ce qui peut être fait dès maintenant (indépendant de l'index hybride)

### A1. Calculer UniFrac et Faith PD — métriques manquantes
L'arbre phylogénétique (`results/phylogeny/rooted_tree.qza`, 44 256 feuilles, couvre
100 % des 44 200 ASV de la table propre) a été construit **pour** ces métriques, mais le
script 15 n'a calculé que Bray-Curtis et Jaccard.

Pourquoi ça compte pour la question posée : les métriques taxonomiques et phylogénétiques
ne répondent pas à la même question. Deux hybrides peuvent porter des ASV différents mais
phylogénétiquement proches — un cas que Bray-Curtis compte comme une divergence et
UniFrac comme une similarité. Pour trancher « intermédiaire ou transgressif », les deux
lectures sont nécessaires.

À produire : UniFrac pondéré et non pondéré (β), Faith PD (α), en rarefactions répétées
avec moyennage des métriques, sur le même jeu de 1 784 échantillons.
Coût : le calcul UniFrac est plus lourd que Bray-Curtis ; la convergence établie
(`decision_rarefaction_mode.md`) permet de réduire le nombre d'itérations.

### A2. Refaire la partition de variance avec un terme de position
Le script 14 attribuait 0,03 % de la variance au technique — mais **ne contenait aucun
terme de position dans la plaque**. Or l'effet de position est établi
(`decision_position_effect.md`) : ratio 1,77–1,89 sur l'attendu sous H₀, du même ordre par
degré de liberté que l'effet taxon (1,93). La partition actuelle sous-estime donc la
composante technique d'une quantité non mesurée.

Recommandation issue des résultats : utiliser le **rang de colonne au sein du site**
(1 seul degré de liberté) plutôt que la colonne en facteur (11 df). Il était significatif
dans 8 à 12 strates sur 12 selon le sous-ensemble, pour un coût en degrés de liberté
douze fois moindre — ce qui compte quand l'index hybride, le site et le tissu occupent
déjà le modèle.

### A3. Consolider les métadonnées d'analyse en une table unique
Les corrections passent actuellement par trois tables de jointure séparées :
`sample_qc_flags.csv`, `station_mapping.csv`, `individual_corrections.csv`. Un script
d'analyse qui en oublie une produira des résultats faux sans erreur visible.

À produire : une table `metadata/analysis_metadata.csv` au niveau échantillon, jointe sur
`dada2_id`, portant déjà appliquées : la requalification des mocks, la station, la
correction d'année de `15Per2015Ch03A`, le rang de colonne dans le site, et l'index
hybride quand il arrivera. Point d'entrée unique et vérifiable.

### A4. Corriger le dépôt ENA (n'affecte pas l'analyse, mais à ne pas oublier)
Six des neuf sites portent une coordonnée fausse de plus de 5 km et cinq une rivière
fausse ; les dates de collecte au jour près sont maintenant disponibles ; l'année de
collecte de `15Per2015Ch03A` est à corriger. Détails et champs :
`docs/decision_stations.md`, `ena_deposit/GUIDE_depot_ENA.md`.
À faire via l'interface Webin (identifiants côté JF Martin).

### A5. Compléter le §1 du Materials & Methods
Le placeholder « dates précises de collecte, effectifs par site/année, coordonnées des
9 sites » est **désormais entièrement résoluble** avec les réponses d'André. Le site table
doit aussi refléter les vraies coordonnées, la structure à deux stations du Suran, et le
comptage corrigé de 180 individus (au lieu de 181).

---

## B. Décisions à prendre avant d'écrire le script d'analyse

### B1. Station ou site pour le Suran ?
`Ain` et `Cab` couvrent chacun **deux stations physiques** (Pont-d'Ain et
Chavannes-sur-Suran, 24 km, séparées par un seuil infranchissable de 2,5 m vers l'amont,
dévalaison possible). Les traiter comme un site unique fusionne deux populations
allopatriques portant des taxons différents.

Recommandation : remplacer `site` par `station` dans tous les modèles spatiaux. La
barrière fournit en plus un contraste amont/aval à flux asymétrique, qui a un sens
écologique direct pour la question hybride.

### B2. Que faire de la nageoire caudale ?
Le signal taxon n'y survit **pas** à l'ajustement sur la position : 0/3 runs significatifs,
en Bray comme en Jaccard (p de 0,14 à 0,83). Dans les trois autres tissus il survit
(midgut 3/3 pour les deux métriques ; branchie 3/3 et 2/3 ; hindgut discordant entre
métriques). C'est aussi le tissu de plus faible biomasse, et celui qui concentrait les
échecs du contrôle d'assignation échantillon-fichier.

Trois options : la garder dans l'analyse principale en signalant la limite ; la déplacer
en supplémentaire ; l'analyser mais ne pas en tirer de conclusion sur le taxon.
Ce n'est pas une décision technique — elle dépend de ce que le manuscrit veut affirmer.

### B3. Confirmations de protocole attendues d'André
Trois passages du M&M (§2 mode de capture et autorisations, §4 conservation et
dissection, contrôles mock) sont transposés du manuscrit d'origine et marqués
« à confirmer pour le lot Durance ». Ils ne bloquent pas l'analyse mais bloquent la
soumission.

---

## C. Le verrou : l'index hybride

### C1. Les 131 individus à génotyper
Sans index hybride, **les catégories de poisson n'existent pas** : 131 des 180 individus
sont `Ch`, non résolus. C'est le seul vrai bloquant.

Répartition des 131 par station : Rosieres 25, Confluence Buech-Meouge 27, Canal 20,
Saint-Just 19, Manosque 12, Pont-d'Ain 10, Chavannes 9, Pertuis 9.

### C2. À VÉRIFIER dès l'arrivée de l'index : les parentaux sont-ils confondus avec la station ?
C'est le point qui décide si la question « intermédiaire ou transgressif » est répondable
telle qu'elle est posée.

Tester la transgression demande une **référence parentale** : l'intervalle occupé par
chaque espèce pure. Or l'état actuel des 49 individus déjà identifiés est déséquilibré :

| Parental | n | Répartition par station |
|---|---|---|
| Hotu (index 0) | 37 | Avignon 22, Buech 8, Pont-d'Ain 4, Manosque 3 |
| **Toxostome (index 1)** | **12** | **Chavannes 10, Avignon 2** |

**Une seule station contient les deux parentaux — Avignon — et seulement 2 toxostomes.**
La signature « toxostome pure » est donc actuellement quasi indissociable de la station
Chavannes. Et l'effet station est le plus fort mesuré sur la composition (ratio 3,07,
significatif dans les 12 strates) — plus fort que la position et que le taxon.

Conséquence : si l'index hybride ne fait qu'ajouter des Pt à Chavannes (ce que la règle
d'André prédit pour Cab 1011-1019, soit 9 individus de plus à Chavannes), le déséquilibre
persiste et l'intervalle parental toxostome ne pourra pas être séparé de l'effet station.

Vérification à faire, dans cet ordre :
1. compter les parentaux par station après application de l'index ;
2. vérifier qu'au moins deux stations contiennent les deux parentaux avec des effectifs
   exploitables ;
3. si ce n'est pas le cas : reformuler la question en contrastes **intra-station** aux
   stations où le gradient s'étend, plutôt qu'en comparaison à un intervalle parental
   global — qui mélangerait signature d'espèce et signature de station.

Ne pas sauter cette étape : une figure comparant des hybrides à un « intervalle parental »
construit sur une seule station serait trompeuse même si chaque valeur y est exacte.

---

## D. Puis l'analyse elle-même

Structure de modèle que les résultats techniques imposent :
- **stratifier par tissu** (la plaque est entièrement déterminée par le tissu ; les
  quatre tissus n'ont pas le même comportement) ;
- **station** et non site pour le Suran (B1) ;
- **rang de colonne dans le site** comme covariable de position (A2) ;
- effets aléatoires : séquençage **niché** dans la préparation de librairie, pas un
  facteur run à trois niveaux interchangeables (`decision_run_design.md`) ;
- **identité du poisson** comme effet aléatoire si les tissus sont analysés conjointement
  (elle porte 37,7 % de la variance, le plus fort effet biologique mesuré) ;
- métriques : taxonomiques (Bray-Curtis, Jaccard) **et** phylogénétiques (UniFrac, Faith
  PD) une fois A1 fait ;
- rarefactions répétées avec moyennage des **métriques** (jamais des tables de comptage) —
  `decision_rarefaction_mode.md`.

Effectif utile : 180 individus, dont **178 avec les quatre tissus**.

---

## Ordre recommandé

1. **A1** (UniFrac/Faith PD) et **A2** (partition avec position) — indépendants, peuvent
   tourner en parallèle sur le cluster.
2. **A3** (table de métadonnées unique) — prérequis de tout script d'analyse.
3. **B1** et **B2** — décisions, à trancher pendant que A1/A2 tournent.
4. **A5** et **A4** — rédaction et dépôt, en parallèle.
5. **C1** — attente d'André.
6. **C2** — dès l'index reçu, avant toute analyse.
7. **D** — l'analyse.

A1, A2 et A3 peuvent être lancés maintenant sans attendre André.
