# Décisions à prendre — projet microbiome-hybride

> **TRANCHÉ le 25 septembre 2026 — document d'archive.** Six des sept décisions ci-dessous ont
> reçu leur réponse d'André, et les deux anomalies de données sont expliquées. Seule D7 (métrique
> de diversité) reste ouverte. L'état à jour, les conséquences chiffrées de chaque arbitrage et ce
> qui reste à faire sont dans `point_etape_25sept.md`. Ce document est conservé parce qu'il porte
> les options écartées et leur coût, utiles pour justifier les choix en Methods et en review.
>
> Une correction d'implémentation à retenir : l'option 1 de D1, telle que formulée ici, faisait
> rejoindre aux 22 quasi-purs leur classe parentale. André tranche qu'ils sont des hybrides et ne
> peuvent pas être traités comme purs — la passe 1 doit donc les **exclure**, non les reverser.

État au 25 septembre 2026. Chaque décision est posée avec les données qui l'éclairent, les
options et leur coût chiffré, et une recommandation. Les valeurs sont recalculées sur les
fichiers du projet. Figure d'appui : `fig_aide_decision.png`.

## Vue d'ensemble

| # | décision | qui tranche | bloque quoi |
|---|---|---|---|
| D1 | que veut dire « hybride » : 42 ou 20 individus ? | André + JF | tout le reste |
| D2 | comment rapporter la classe confondue avec position et station | JF | les Results |
| D3 | périmètre : garder Manosque et Pertuis ? | JF | la présentation |
| D4 | annoncer l'analyse 4H ou la réserver à la discussion | JF | l'introduction |
| D5 | paramètres a priori du 4H : ρ et échelle taxonomique | JF | les Methods |
| D6 | que faire de la peau caudale | JF | le périmètre tissulaire |
| D7 | métrique de diversité retenue pour les Results | analyse | tous les chiffres |

Deux questions restent ouvertes côté André (section finale) et quatre sections de protocole
restent en attente pour le Materials & Methods.

---

## D1. Que veut dire « hybride » dans cet article ?

**C'est la décision qui commande toutes les autres.** La classe Hy à 42 individus réunit deux
réalités génomiques : 20 génomes intermédiaires (médiane entre 0,05 et 0,94) et 22 quasi-purs,
dont 17 introgressés sur un seul chromosome sur 25.

### Les données qui éclairent

Figure `fig_genotypage_25chr.png`, panneau a : le plan médiane × D sépare visuellement les deux
sous-types. Et trois éléments quantitatifs :

- **le clustering hiérarchique retrouve la partition en deux sous-types, pas la classe à 42** :
  22 des 42 hybrides tombent dans un cluster dont la majorité est parentale, et les clusters
  exclusivement hybrides rassemblent exactement les 20 génomes intermédiaires ;
- **le décompte de chromosomes ne sépare pas les classes** : six individus classés purs ont au
  moins un chromosome introgressé (un Cn en a trois) alors que 17 hybrides n'en ont qu'un ;
- **mais le seuil D = 0,12 est stable** : il tombe dans un intervalle vide de la distribution
  (0,1191 / 0,1301), et tout seuil de 0,12 à 0,15 donne exactement 42 hybrides.

### Le coût chiffré

| | Hy = 42 (règle actuelle) | Hy = 20 (intermédiaires) |
|---|---|---|
| plafond 4H, peau / branchie / midgut / hindgut | 28 / 41 / 30 / 36 | 10 / 20 / 12 / 16 |
| puissance Hy vs parentaux, effet ×1,3, peau | 0,61 | 0,30 |
| ... branchie | 0,76 | 0,51 |
| stations avec ≥ 3 individus dans les 3 classes | 3 | 2 |
| stations avec ≥ 3 individus dans ≥ 2 classes | 6 | 3 |
| V de Cramér classe × position (confondant) | 0,479 | 0,531 |

**Un effet secondaire à connaître** : sous l'option restrictive, les 22 quasi-purs rejoignent leur
parental, et Avignon — seul site sans toxostome aujourd'hui — en gagne un. La composition des
stations change sensiblement (Rosières passe de 18 Pt / 7 Hy à 24 Pt / 1 Hy, Manosque de 10 / 5 à
14 / 1).

### Les trois options

1. **Hybride = les 20 génomes intermédiaires ; les 22 quasi-purs rejoignent leur parental.**
   Défendable biologiquement — 96 % du génome partagé avec un parental —, cohérent avec le
   clustering, et cohérent avec l'exigence de classes non chevauchantes du 4H. Coût : la peau
   tombe à 10 hybrides, la puissance à 0,30, la réplication entre stations de 6 à 3, et le
   confondant position augmente légèrement.
2. **Quatre classes : hotu, introgressé, hybride intermédiaire, toxostome.** Respecte la réalité
   génomique, et le nombre de chromosomes introgressés devient un gradient exploitable. Coût : le
   4H n'admet que trois classes, et la classe introgressée penche à 19 contre 3 vers le
   toxostome.
3. **Hybride = les 42, comme aujourd'hui.** Maximise la puissance et la réplication. Coût : la
   classe mélange un F1 putatif et un poisson quasi-pur, visible dès le panneau a — et
   l'hypothèse « transgressif » perd son sens si la moitié des hybrides a un génome parental.

**Recommandation** : option 1 pour l'analyse principale, option 3 en analyse de sensibilité
déclarée d'avance. La question à trancher avec André est biologique, pas statistique : un poisson
introgressé sur un seul chromosome sur 25 est-il, pour la question posée, un hybride ?

---

## D2. Comment rapporter un effet de classe triplement confondu

**Le constat le plus contraignant du projet.** Entre stations, la classe est confondue avec la
station, qui porte l'effet le plus fort sur la composition. À station fixée, elle est confondue
avec la position dans la plaque — et les trois stations portant les trois classes sont exactement
celles où l'enchevêtrement est maximal (figure `fig_aide_decision.png`, panneau b) :

| station | n | classes | V de Cramér classe × colonne |
|---|---|---|---|
| Pertuis | 9 | 2 | 0,000 |
| Rosières | 25 | 2 | 0,181 |
| Pont-d'Ain | 14 | 2 | 0,354 |
| Manosque | 15 | 2 | 0,487 |
| Saint-Just | 19 | **3** | **0,523** |
| Canal du Largue | 20 | **3** | **0,540** |
| Avignon | 24 | 2 | 0,564 |
| Büech-Méouge | 35 | **3** | **0,620** |

Le sous-plan pleinement séparable compte 90 individus sur 180, mais seulement 32 dans une station
gardant les trois classes. Rosières est le seul témoin propre, et il est petit.

**Options** : rapporter l'encadrement par les deux ordres séquentiels — position d'abord puis
classe (variance minimale attribuable à la classe), classe d'abord puis position (maximale) — et
l'intervalle comme degré d'incertitude ; ou restreindre le test principal au sous-plan séparable ;
ou présenter Rosières comme témoin et le reste comme exploratoire.

**Recommandation** : l'encadrement, déjà calculé et rédigé par la conversation d'analyse. Rapporter
un seul des deux ordres serait choisir la réponse. C'est un choix à annoncer dans les Methods, pas
à justifier après coup — c'est exactement le reproche que la littérature adresse aux études
d'admixture dont l'effet s'évanouit sous contrôle spatial.

---

## D3. Périmètre : garder Manosque et Pertuis ?

Analyse déjà chiffrée dans `analyse_couts_benefices_sites.md` et `fig_couts_benefices_sites.png`.
Le résultat décisif reste valable : **le déséquilibre de stade de développement que leur retrait
était censé régler traverse aussi la liste restreinte** — le canal du Largue, site structurant,
a le même profil juvénile que les deux sites contestés. Les retirer déplace le problème à
l'intérieur du plan.

Mise à jour de septembre : Manosque gagne 3 hybrides (de 2 à 5) et Rosières 3 (de 4 à 7) — mais
**tous quasi-purs**, donc ces gains disparaissent si l'option 1 de D1 est retenue. La décision D3
est donc subordonnée à D1.

**Recommandation inchangée** : tout garder, écarter le seul individu de la campagne fantôme de
Pertuis 2015, traiter le rôle de population en covariable et non en critère d'inclusion, et
ajouter une sensibilité « liste restreinte » en supplément.

---

## D4. Annoncer l'analyse 4H ou la réserver à la discussion

Le cadre existe et le package est sur le CRAN, mais l'indice se calcule sur trois classes
non chevauchantes et non sur un index continu — donc il exige exactement la décision D1. Ses
quatre modèles portent sur l'appartenance taxonomique, pas sur la position sur un gradient : le
pont vers le vocabulaire du projet passe par les deux axes du diagramme quaternaire, dont l'axe
transgressif fournit une définition opérationnelle sans présupposer de coût de fitness.

Le plafond du plan équilibré reste au-dessus du plancher de stabilité de 8 dans les deux options
de D1 (panneau a), donc l'analyse est faisable dans les deux cas.

**Recommandation** : annoncer les deux analyses dans l'introduction — le modèle global sur la
classe, et le 4H comme caractérisation complémentaire — mais seulement après avoir tranché D1.
Détail dans `note_indice_4H.md`.

---

## D5. Paramètres a priori du 4H

**À figer par écrit avant de calculer quoi que ce soit**, car le matériel supplémentaire de Camper
et al. montre que l'amplitude des biais est bien plus grande sur un système hybride naturel que
sur les lignées croisées de leurs exemples (`note_sensibilite_4H.md`, `fig_sensibilite_4H.png`) :

| levier | lézard (hybride naturel) | maïs (lignées) |
|---|---|---|
| seuil de core ρ, de 0,1 à 0,8 | **0,520** | 0,058 |
| échelle taxonomique, phylum → ASV | **0,648** | 0,280 |
| hôtes par classe, 4 → 16 | 0,114 | 0,129 |
| profondeur, 1 000 → 10 000 | 0,067 | 0,013 |

**Le risque de circularité est réel** : un ρ élevé favorise mécaniquement l'axe transgressif, qui
est l'hypothèse d'intérêt. Invoquer la recommandation des auteurs pour choisir un ρ élevé puis
conclure à la transgression serait indéfendable. Deux arguments durs en revanche : la dimension
Intersection s'annule au seuil le plus haut testé, et aussi à l'échelle taxonomique la plus fine.
Bonne nouvelle : l'effectif par classe et la profondeur comptent peu.

**Recommandation** : ρ = 0,5 au rang du genre, comme les figures publiées, avec sensibilité
rapportée sur ρ ∈ {0,3 ; 0,5 ; 0,7} et sur le rang famille et genre. Vérifier au préalable le taux
d'assignation des ASV au genre sur nos données. Et lancer `FourHpreanalysis`, qui fournit un
critère chiffré de subdivision de la classe hybride calculable avant de regarder l'indice.

---

## D6. Que faire de la peau caudale

C'est le tissu le plus pénalisé : plafond de 28 (ou 10) contre 41 (ou 20) en branchie, et la
décision B2 de la feuille de route d'analyse reste ouverte. Le gradient externe / interne est
solidement répliqué et la peau en est un pôle, donc la retirer coûterait un résultat.

**Recommandation** : garder les quatre tissus pour l'axe tissulaire, qui est bien répliqué
(109 individus aux quatre tissus), et n'exclure la peau que de l'analyse 4H si le plafond tombe à
10 sous l'option 1 de D1 — en le déclarant.

---

## D7. Métrique retenue pour les Results

**Tous les diagnostics de faisabilité que j'ai produits portent sur la richesse ASV observée** :
contrastes tissulaires, réplication de 2017, dimorphisme sexuel, partition de variance, et
l'intégralité des calculs de puissance de ce document. L'analyse de reproductibilité technique a
établi que cette métrique est peu reproductible sur les taxons rares (48 % de recapture des ASV
à 1-3 lectures) et que le manuscrit fonde ses analyses sur des métriques pondérées.

**Conséquence à acter** : aucun de ces chiffres n'entre dans les Results tel quel, et les
écarts-types résiduels qui fondent les seuils d'effectif annoncés ici se déplaceront. Les
comparaisons de puissance sont à recalculer en Shannon ou Bray-Curtis avant toute reprise.
Le gradient externe / interne, lui, est assez massif (coefficient 0,598, z = 8,7) pour
probablement survivre au changement de métrique — mais il faut le vérifier, pas le supposer.

---

## Ce qui reste ouvert côté André

> Ces trois points, plus la question biologique de D1, sont regroupés et détaillés dans
> `pour_andre_questions_ouvertes.md` — c'est ce document qu'il faut lui envoyer, pas celui-ci.
> Le résumé ci-dessous est conservé pour que la liste des décisions soit lisible seule.

**1. Les cinq individus sans Q-values.** `2014_Bue_1001`, `2014_Bue_1002` (Cn), `2015_Bue_1014`,
`2015_Cab_1011`, `2015_Jus_1008` (Pt) ont une classe et un index dans le tableau mais aucune ligne
dans `genome_hotox.csv` (175 lignes pour 180 classés). Leur D vaut exactement 0,00 pour quatre
d'entre eux, ce qui n'arrive à aucun des 175 autres : ces valeurs semblent héritées de l'analyse
à 12 chromosomes. Tous parentaux, donc impact faible — mais génotypage échoué ou simple omission
d'export ?

**2. Les blocs de numérotation hors Suran, toujours inexpliqués.** La structure à deux stations du
Suran explique parfaitement le motif à Pont-d'Ain / Chavannes. Mais **les autres sites n'ont qu'une
station**, et pourtant la composition se rompt nettement à la frontière 1010 / 1011 au canal du
Largue, à Saint-Just et au Büech 2014 (tests exacts de Fisher p = 0,0003, 0,0016 et 0,0002), avec
un sens inversé à Saint-Just. Une station unique ne peut pas produire cela par hasard. Trois
hypothèses à départager : deux passages de pêche successifs à des micro-habitats différents ;
un tri des poissons par morphotype avant numérotation ; ou deux points de capture non consignés à
l'intérieur de la station. Ce n'est pas une curiosité de numérotation : si la numérotation encode
un micro-habitat, c'est un facteur de plus, confondu avec la classe, à faire entrer au modèle.
Chiffres à jour et hypothèses à départager dans `pour_andre_questions_ouvertes.md`,
section 3. Le document `questions_andre_stations.md` est caduc : il précède les réponses du
30 août.

**3. Quatre sections de protocole** pour le Materials & Methods : capture, euthanasie et
autorisations ; extraction et préparation des librairies ; contrôles mock et négatifs ; DOI Zenodo.

---

## Ce qui n'attend aucune décision

L'axe tissulaire (figure `fig_aide_decision.png`, panneau d) : **109 individus avec les quatre
tissus, 160 avec au moins trois, six contrastes appariés intra-individu, aucune classe génotypique
requise**. Deux analyses sont prêtes à tourner — le test de composition midgut / hindgut, seul
test permettant la comparaison terme à terme avec l'article de 2017, et la réplication du gradient
externe / interne sur composition. C'est la seule ossature du jeu de données qui ne soit contrainte
ni par un confondant ni par une décision de classification.