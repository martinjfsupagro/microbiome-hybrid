# Retour du génotypage : vérification de cohérence et lecture du design spatial

Fichier `nouveau tableau_AG_Aout_2026.xlsx` (181 lignes, 18 colonnes), confronté à
`index_hybride_andre.csv` et à `depth_per_sample.tsv`. Toutes les valeurs ci-dessous sont
recalculées sur les fichiers.

## 1. Vérifications de cohérence

### Ce qui concorde exactement

- **Appariement aux données de séquençage : 180 / 180.** Chaque individu du tableau est retrouvé
  dans les données séquencées, et tous les individus séquencés sauf un sont dans le tableau.
- **Le seul manquant est Pertuis 2015** (`2015_Per_2015`), sans classe, sans index, sans taille, et
  avec un seul tissu séquencé (hindgut). Cohérent avec votre indication : erreur non traçable, à
  retirer. Le jeu de travail passe donc à **180 individus**.
- **Les trois groupes de sites annoncés dans votre message se vérifient tous les trois** :
  4 réplicats à trois classes (Ain, canal, St-Just, Büech), 1 population Cn+Hy (Avignon, 20 Cn +
  4 Hy), 3 populations Pt+Hy (Pertuis 1 Hy + 8 Pt, Manosque 2 Hy + 13 Pt, Baume 4 Hy + 21 Pt).
- **Les règles de classification d'André sont appliquées de façon cohérente** : en reconstruisant
  les seuils qu'il décrit (médiane < 0,05 ou > 0,95 = espèce pure, D < 0,12 ; sinon hybride), on
  retrouve 57 des 59 Cn et 91 des 91 Pt. Les 30 Hy se décomposent en 18 à D faible (profil F1),
  3 à D élevé (profil F2 ou recombinant), 8 à médiane extrême mais D élevé (fortement introgressés).

### Trois écarts à signaler

**Écart 1 — deux différences d'un individu entre le tableau de comptage du message et le fichier.**

| site-année | message | fichier | différence |
|---|---|---|---|
| Ain 2014 | 4 Cn, 0 Hy, 11 Pt = 15 | 4 Cn, 0 Hy, 10 Pt = 14 | **1 Pt de moins** dans le fichier |
| Manosque 2014 | 0 Cn, 2 Hy, 12 Pt = 14 | 0 Cn, 2 Hy, 13 Pt = 15 | **1 Pt de plus** dans le fichier |

Les neuf autres lignes concordent exactement. Comme les deux écarts vont en sens opposés et
portent tous deux sur la classe Pt, l'hypothèse la plus économique est un décalage d'une ligne
lors du comptage manuel. Sans conséquence analytique, mais le tableau 1 de l'article doit être
généré depuis le fichier, pas recopié depuis le message.

**Écart 2 — la polarité de l'index est inversée par rapport à l'ancien fichier.** Dans
`index_hybride_andre.csv`, la convention documentée était Cn = 0 et Pt = 1. Dans le nouveau
tableau, les Cn ont une médiane de 0,9469 à 0,9999 et les Pt de 0,0001 à 0,0455 : **Cn ≈ 1,
Pt ≈ 0**. Ce n'est pas un problème puisque les scores ne seront pas utilisés, mais toute
réutilisation ultérieure de la colonne Q doit expliciter le sens, sous peine d'inverser une
conclusion.

**Écart 3 — deux individus classés Cn ont une médiane sous le seuil de 0,95.** `2015_Caa_1001`
(médiane 0,9471, D 0,0528) et `2015_Jus_1014` (0,9469, D 0,0530) sont à quelques millièmes sous
le seuil que décrit le message. Les classer Cn est défendable — le D est faible et la médiane
quasiment à 0,95 — mais c'est un arbitrage à mentionner si un relecteur demande la règle exacte.
À faire confirmer par André plutôt qu'à trancher nous-mêmes.

## 2. Le reclassement est massif

Croisement de l'ancienne détermination et de la nouvelle classe génotypique :

| ancien \ nouveau | Cn | Hy | Pt | total |
|---|---|---|---|---|
| Ch (indéterminé) | 28 | 24 | 79 | 131 |
| Cn | 31 | 4 | 2 | 37 |
| Pt | 0 | 2 | 10 | 12 |
| **total** | **59** | **30** | **91** | **180** |

**La ressource rare a changé de camp.** Le toxostome passe de 12 à 91 individus et devient la
classe la plus nombreuse ; le hotu passe de 37 à 59 ; les hybrides, de 0 identifié à 30. Huit
individus déterminés morphologiquement sont contredits par le génotype (4 Cn → Hy, 2 Cn → Pt,
2 Pt → Hy), ce qui est attendu dans un complexe hybridant et vaut d'être mentionné en une phrase
comme justification du génotypage.

## 3. Le design spatial tel que je le comprends

Individus utilisables (≥ 3 000 lectures), par site-année :

| rivière | site | année | Cn | Hy | Pt | total | classes |
|---|---|---|---|---|---|---|---|
| Ain | Ain | 2014 | 4 | 0 | 10 | 14 | 2 |
| Ain | Ain | 2015 | 8 | 2 | 9 | 19 | 3 |
| Ardèche | Baume | 2015 | 0 | 4 | 21 | 25 | 2 |
| Ardèche | St-Just | 2015 | 8 | 3 | 8 | 19 | 3 |
| Durance | Avignon | 2014 | 11 | 0 | 0 | 11 | 1 |
| Durance | Avignon | 2015 | 9 | 4 | 0 | 13 | 2 |
| Durance | Büech | 2014 | 7 | 1 | 9 | 17 | 3 |
| Durance | Büech | 2015 | 4 | 9 | 5 | 18 | 3 |
| Durance | Manosque | 2014 | 0 | 2 | 13 | 15 | 2 |
| Durance | Pertuis | 2014 | 0 | 1 | 8 | 9 | 2 |
| Durance | canal | 2015 | 8 | 4 | 8 | 20 | 3 |

### Ce que ce plan est, en une phrase

Un plan à **trois niveaux emboîtés** : trois rivières (Ain, Ardèche, Durance) ; huit sites dont
six sur la Durance ou l'Ain et deux sur l'Ardèche ; et à l'intérieur de plusieurs sites, **deux
stations amont/aval** dont la séparation est le mécanisme même du contact entre espèces. La
réplication utile n'est ni au niveau de la rivière (3 niveaux, dont un à un seul site) ni au
niveau de l'individu, mais au niveau du **site** : quatre sites portent les trois classes, ce qui
est la structure qui permet de tester un effet de classe génotypique répliqué.

### La découverte que je n'attendais pas : la numérotation encode les stations

Votre avertissement sur l'Ain — Cn et Hy en aval, Pt 20 km en amont, donc pas en sympatrie — se
lit directement dans les numéros d'individu. À l'Ain, les numéros 1001-1010 sont 10 Cn et 2 Hy,
les numéros supérieurs à 1010 sont 19 Pt et 2 Cn (test exact de Fisher, p < 0,001).

**Et ce motif n'est pas propre à l'Ain.** La même association apparaît à trois autres sites :

| site | numéros 1001-1010 | numéros > 1010 | p |
|---|---|---|---|
| Ain | 10 Cn, 2 Hy, 0 Pt | 2 Cn, 0 Hy, 19 Pt | < 0,001 |
| canal | 8 Cn, 2 Hy, 0 Pt | 0 Cn, 2 Hy, 8 Pt | 0,0003 |
| St-Just | 1 Cn, 1 Hy, 8 Pt | 7 Cn, 2 Hy, 0 Pt | 0,0017 |
| Büech | 10 Cn, 6 Hy, 2 Pt | 1 Cn, 4 Hy, 12 Pt | 0,0006 |
| Avignon | 16 Cn, 2 Hy | 4 Cn, 2 Hy | 0,25 (n.s.) |
| Baume | 2 Hy, 8 Pt | 2 Hy, 13 Pt | 1,0 (n.s.) |
| Manosque | 1 Hy, 2 Pt | 1 Hy, 11 Pt | 0,37 (n.s.) |

Noter que le sens s'inverse à St-Just : les petits numéros y sont les Pt. La numérotation encode
donc un bloc d'échantillonnage, pas une direction hydrologique fixe.

**C'est la question la plus importante que je dois vous poser.** Si les blocs de numérotation
correspondent à des stations distinctes sur les quatre sites — et non seulement à l'Ain — alors
le facteur « station » existe dans les données sans être documenté dans les métadonnées, et il est
presque parfaitement confondu avec la classe génotypique. Un effet de classe pourrait être un
effet de lieu de capture : eau, substrat, ressource trophique différents à 20 km d'écart.

C'est exactement le risque documenté chez la souris domestique, où l'effet d'admixture s'évanouit
dès qu'on contrôle l'autocorrélation spatiale (*Molecular Ecology* 2023, doi 10.1111/mec.17192).
Il faut donc demander à André, pour chaque site, si les blocs de numéros correspondent à des
points de capture distincts, et si oui leurs coordonnées. Sans cette information, le facteur
station ne peut pas entrer au modèle et la confusion reste non traitée.

### Ce qui a changé dans les rôles de population

Le codage `role_population` de l'ancien fichier est périmé sur trois points :

- **plus aucune population pure** : les trois classes coexistent sur quatre sites, deux sur les
  quatre autres. Le mot « allopatrie » n'a plus d'objet, et « parapatrie » doit être requalifié
  par la présence d'hybrides ;
- **le canal, ancienne référence d'allopatrie, porte les trois classes** (8 Cn, 4 Hy, 8 Pt) ;
- **Avignon est le seul site sans toxostome** (20 Cn, 4 Hy, 0 Pt) : c'est lui, et non plus Baume,
  qui constitue le cas asymétrique le plus net du jeu de données.

Le gradient de rôles qui structurait l'introduction n'existe donc plus sous cette forme. Ce qui le
remplace naturellement est un contraste de **composition de population** : sites à trois classes
contre sites à deux, et parmi ces derniers, sens de l'asymétrie (Cn+Hy à Avignon contre Pt+Hy à
Baume, Manosque, Pertuis).

## 4. Conséquences chiffrées sur la puissance

Individus utilisables par classe et tissu :

| classe | peau | branchie | midgut | hindgut |
|---|---|---|---|---|
| hotu (Cn) | 48 | 54 | 51 | 46 |
| hybride (Hy) | 17 | 30 | 20 | 25 |
| toxostome (Pt) | 80 | 88 | 80 | 86 |

**Le plafond du plan équilibré 4H passe de 10-12 à 17-30 individus par classe** (17 en peau, 20 en
midgut, 25 en hindgut, 30 en branchie) — au-dessus de tous les systèmes publiés dans Camper et al.
(7 pour le rat, le lézard et la cigale ; 10 pour le maïs), et bien au-delà de la zone de stabilité
de l'indice qui commence à 8.

**Le contraste parental devient réellement testable** : puissance de 0,98 pour un effet ×1,5 en
peau (48 Cn contre 80 Pt), contre 0,21 dans l'ancien plan. Un effet ×1,3 est détecté à 0,74.

**Le contraste hybride contre parentaux est correct mais inégal selon le tissu** : 0,81 en peau
(17 Hy), 0,95 en branchie (30 Hy), pour un effet ×1,5. L'hybride est désormais la classe rare, et
la peau le tissu le plus pénalisé — inversion complète par rapport au diagnostic initial.

Réserve : ces puissances utilisent une SD résiduelle de 0,55 estimée sur la richesse ASV observée,
métrique écartée par l'analyse de reproductibilité technique. Les ordres de grandeur tiennent, les
valeurs exactes devront être recalculées en métrique pondérée par l'abondance.

## 5. Trois questions à poser à André

1. **Structure en stations de chaque site-année.** Confirmé pour l'Ain par l'utilisateur : deux
   stations à quelques kilomètres, toxostomes en amont, hotus et hybrides en aval, séparées par un
   seuil infranchissable de l'aval vers l'amont. Ce type de dispositif se retrouve ailleurs dans
   l'échantillonnage, y compris en configuration symétrique. Questions détaillées dans
   `questions_andre_stations.md`.
2. **Les deux écarts d'un individu** (Ain 2014, Manosque 2014) : *tranché — le fichier fait foi,
   pas le comptage du corps du message. Le plan de travail est donc 10 Pt à Ain 2014 et 13 Pt à
   Manosque 2014.*
3. **Les deux Cn à médiane 0,947** (`2015_Caa_1001`, `2015_Jus_1014`) : *tranché — décision
   arbitrée assumée, à mentionner comme telle en Methods.*