# Point d'étape après les réponses d'André du 25 septembre 2026

Les sept décisions sont tranchées, et les deux anomalies de données sont expliquées. Ce document
intègre les réponses, en tire les conséquences chiffrées, et signale les trois points qui
demandent encore une précision ou une vigilance.

## 1. Les deux anomalies sont expliquées

### Les blocs de numérotation : artefact de procédure, pas facteur spatial

**Explication d'André** : les numéros suivent l'ordre d'échantillonnage de terrain. Les hotus
étant plus fragiles que les toxostomes, ils sont prélevés en priorité — sauf une fois où cet
ordre n'a pas été respecté. Aucune relation n'est recherchée entre code individu et espèce.

Cela explique tout ce que j'avais observé, y compris le détail qui me gênait le plus : **le sens
s'inversait à St-Just**, où les petits numéros étaient les toxostomes. C'est la fois où l'ordre
n'a pas été respecté. La signature est donc une conséquence mécanique du protocole, et il n'y a
**aucun facteur de station supplémentaire à faire entrer au modèle** — c'était la réponse la plus
favorable des trois hypothèses.

**Mais cette explication en soulève une autre, et il faut la traiter.** Si l'ordre de prélèvement
est déterminé par l'espèce, alors le **délai entre capture et dissection est confondu avec la
classe, par construction du protocole**. Les hotus sont dissqués tôt, les toxostomes plus tard.
Ce n'est pas un problème de station : c'est un délai de manipulation.

Et ce délai n'est pas une hypothèse abstraite. J'ai testé la corrélation entre numéro d'individu
et colonne de plaque **à l'intérieur de chaque station** :

| station | n | rho de Spearman | p |
|---|---|---|---|
| Rosières | 25 | +0,950 | < 0,0001 |
| Saint-Just | 19 | +0,932 | < 0,0001 |
| Canal du Largue | 20 | +0,931 | < 0,0001 |
| Manosque | 15 | +0,908 | < 0,0001 |
| Pertuis | 9 | +0,866 | 0,0025 |
| Büech-Méouge | 35 | +0,387 | 0,022 |
| Avignon | 24 | +0,368 | 0,077 |
| Chavannes-sur-Suran | 19 | +0,008 | 0,97 |
| Pont-d'Ain | 14 | +0,168 | 0,57 |

**La plaque a été chargée dans l'ordre d'échantillonnage** à cinq stations sur neuf. La colonne de
plaque — ce que la conversation d'analyse appelle l'effet de position — est donc, à ces stations,
presque la même variable que l'ordre de prélèvement, lui-même déterminé par l'espèce.

**Un discriminateur existe.** Un délai de dissection affecte davantage les compartiments
digestifs que les surfaces externes : la communauté intestinale se modifie vite post-mortem,
celle de la peau et de la branchie beaucoup moins. La température de l'eau, elle, agit sur les
quatre compartiments. **Si un effet de classe apparaît en midgut et hindgut sans équivalent en
peau et branchie, le délai de manipulation est le candidat le plus simple ; s'il est présent
partout, l'explication environnementale tient.** C'est une prédiction à poser avant l'analyse,
pas à lire après, et elle est calculable sur les données existantes.

### Les cinq individus sans Q-values : c'est une question de tissu

**Explication d'André** : l'analyse par Q-scores est faite sur le **foie**. Elle est impossible
pour ces cinq individus faute de séquences de foie. Leur identification vient d'autres tissus,
sur lesquels la Q-value n'a pas été calculée.

Deux conséquences pour le manuscrit :

1. **le tissu de génotypage est le foie**, un cinquième tissu absent du jeu microbiote. À écrire
   explicitement dans les Methods — un lecteur supposera sinon que le génotype vient d'un des
   quatre tissus séquencés ;
2. **ces cinq individus ne sont pas génotypés par la même méthode que les 175 autres.** Ils sont
   classés, mais par une voie différente. Les compter parmi « 180 individus génotypés sur
   25 chromosomes » serait inexact. Formulation juste : 175 individus génotypés par Q-scores sur
   25 chromosomes à partir du foie, 5 identifiés à partir d'autres tissus.

**Ce qui reste à préciser, et c'est une vraie question.** Le tableau donne malgré tout à ces cinq
individus une médiane et un D — par exemple 0,9878 et 0,00 pour `2014_Bue_1001` (ligne 27 du
.xlsx). Si aucune Q-value n'a été calculée sur le foie pour eux, **d'où viennent ces deux
valeurs ?** Trois possibilités : elles proviennent d'une analyse antérieure sur un autre tissu ;
elles sont un report de l'analyse à 12 chromosomes ; ou ce sont des cellules de remplissage. La
réponse décide si ces colonnes doivent être vidées pour ces cinq lignes avant publication du
tableau en supplément. Détail dans `individus_sans_qvalues.csv`.

## 2. Les sept décisions et ce qu'elles impliquent

### D1 — hybride = les 42, analysés en deux passes

**Tranché** : les 22 quasi-purs sont des hybrides et ne peuvent pas être traités comme purs. Ce
sont des produits d'hybridation introgressive plutôt que des mosaïques ; une petite région
génomique conservée peut porter un signal qu'il serait dommage de perdre. Séquence retenue :
option 1 puis option 3.

**Une précision d'implémentation en découle.** Dans ma formulation d'origine, l'option 1 faisait
**rejoindre aux 22 quasi-purs leur classe parentale**. Cela contredit la position d'André. La
passe 1 doit donc les **exclure** et non les reverser. Bonne nouvelle : cela ne coûte rien sur le
plan équilibré, qui est fixé par la classe hybride dans les deux cas.

| | passe 1 : 20 hybrides, 22 exclus | passe 2 : 42 hybrides |
|---|---|---|
| individus exploitables | 158 | 180 |
| hotu / hybride / toxostome en branchie | 54 / 20 / 77 | 54 / 41 / 77 |
| plafond 4H, peau / branchie / midgut / hindgut | 10 / 20 / 12 / 16 | 28 / 41 / 30 / 36 |
| puissance Hy vs parentaux, ×1,3, peau | 0,30 | 0,61 |
| ... branchie | 0,51 | 0,76 |

À titre de comparaison, si les 22 avaient été reversés aux parentaux, le plafond serait identique
(10 / 20 / 12 / 16) mais les classes parentales gonfleraient à 50 Cn et 85 Pt en peau — ce qui
aurait mélangé des génomes introgressés dans les groupes de référence. L'exclusion est donc à la
fois plus fidèle à la biologie et sans coût statistique.

**Sa question mérite d'être reprise telle quelle dans la discussion** : jusqu'où un hybride très
introgressé — un chromosome sur 25 dans la plupart des cas — peut-il correspondre à une
adaptation liée au microbiote ? C'est la formulation d'une hypothèse, pas d'une limite.

### D2 — on ne dissocie pas station et classe ; l'effet position est abandonné

**Tranché** : le lien station-classe est biologiquement causal, la température de l'eau en
particulier, le hotu y étant sensible ainsi qu'au polio. On ne cherche pas à séparer les deux
effets, on se concentre sur les patterns observés, le contexte mécanistique viendra ensuite.

C'est une position défendable pour une étude de terrain, et elle simplifie beaucoup. Deux
conséquences à assumer par écrit :

1. **la formulation des résultats change**. Ce qui est rapporté n'est pas « un effet de la classe
   génotypique » mais « un pattern le long d'un gradient de stations qui co-varie avec la classe
   et avec la température ». La nuance n'est pas cosmétique : la littérature contient au moins un
   cas où un effet d'admixture apparent disparaît sous contrôle de l'autocorrélation spatiale, et
   c'est le reproche qu'un relecteur formulera. Le dire d'emblée le désarme ;
2. **l'abandon de l'effet position demande plus de précaution que l'abandon de la séparation
   station-classe.** Ce sont deux choses de nature différente : le lien station-classe est
   biologique et il est légitime de ne pas le disséquer ; la colonne de plaque est un facteur
   technique, mesuré comme réel par la conversation d'analyse (R² de 0,18 à 0,40 selon la
   métrique, significatif dans 9 à 12 strates sur 12). Et comme le montre la section 1, à cinq
   stations elle est quasiment confondue avec l'ordre de prélèvement.

**Version minimale défendable** : sortir la position du modèle principal comme demandé, mais
conserver en supplément une analyse de sensibilité montrant que les conclusions ne changent pas
quand on l'inclut. Cela coûte une table et retire l'argument à un relecteur. Si les conclusions
changent, il vaut mieux le savoir maintenant qu'en review.

### D3 — tout garder

**Tranché**, conforme à la recommandation : les échantillons correspondent à une étude de terrain
et à la réalité des faits, non à une expérimentation contrôlée. Les 180 individus sont retenus,
la campagne fantôme de Pertuis 2015 écartée, le rôle de population traité en covariable et non en
critère d'inclusion.

### D4 — 4H en deux passes, les plus mosaïques d'abord

**Tranché** : une première analyse 4H sur les 20 hybrides les plus mosaïques, puis une sur les 42
au sens large, puis comparaison des résultats.

**Le plan est faisable dans les deux passes.** Le plafond de la passe 1 descend à 10 individus par
classe en peau, mais le matériel supplémentaire de Camper et al. montre que l'indice est plat
au-delà de 8 hôtes par classe (axe parental à 0,472 pour N = 8, 0,475 pour N = 10, 0,489 pour
N = 12). Avec 10, on est dans la zone stable — de peu, mais dedans.

**Comparer les deux passes est informatif en soi** : si l'indice se déplace entre 20 et 42
hybrides, le déplacement mesure la contribution propre des introgressés, ce qui répond
directement à la question d'André sur le signal porté par ces petites régions génomiques.
À déclarer comme tel dans les Methods, avec les deux passes annoncées d'avance.

### D5 — paramètres du 4H : ρ = 0,5 au rang du genre

**Tranché**, conforme à la recommandation, avec ajustement si l'analyse de sensibilité l'indique.
Sensibilité à rapporter sur ρ ∈ {0,3 ; 0,5 ; 0,7} et sur les rangs famille et genre. Deux points
de vigilance déjà documentés : un ρ élevé favorise mécaniquement l'axe transgressif, qui est
l'hypothèse d'intérêt — d'où l'obligation de figer la valeur avant de regarder le résultat ; et la
dimension Intersection s'annule au seuil le plus haut testé comme à l'échelle la plus fine, ce qui
borne la gamme explorable. Préalable technique : vérifier le taux d'assignation des ASV au genre
sur nos données, et lancer `FourHpreanalysis` qui fournit un critère chiffré de subdivision de la
classe hybride calculable avant l'indice.

### D6 — les quatre tissus sont conservés

**Tranché**, conforme à la recommandation. Le déclencheur que j'avais posé — retirer la peau du
4H si son plafond tombe à 10 — se produit bien en passe 1, mais 10 reste au-dessus du plancher de
stabilité de 8. **La peau est donc conservée dans les deux passes**, en le déclarant : c'est le
tissu le plus contraint du plan, et un relecteur qui verra 10 individus par classe doit trouver la
justification déjà écrite.

### D7 — métrique de diversité : ouvert

Seule décision non tranchée. André demande d'aller plus loin dans la compréhension des
implications de ce choix, ce qui est juste : il ne s'agit pas d'un réglage mais du socle de tous
les chiffres. L'acquis à ce stade :

- la richesse observée est peu reproductible sur les taxons rares — 48 % seulement des ASV à
  1-3 lectures sont retrouvés lors d'un re-séquençage de la même librairie ;
- les analyses de diversité du manuscrit reposent donc sur des métriques pondérées par
  l'abondance ;
- **en conséquence, aucun des chiffres de puissance de ce document n'entre dans les Results tel
  quel**, y compris les tableaux de D1 : ils utilisent un écart-type résiduel estimé sur la
  richesse observée. Ils gardent leur valeur de diagnostic de faisabilité, et les seuils
  d'effectif se déplaceront après recalcul.

Ce travail revient à la conversation d'analyse. La question à instruire est de savoir quelles
conclusions dépendent du choix de métrique et lesquelles y sont indifférentes — le gradient
externe / interne, mesuré à un coefficient de 0,598 pour z = 8,7, survivra probablement, mais
cela doit être vérifié et non supposé.

## 3. Où nous en sommes

**Le cadrage de l'article n'est plus bloqué.** Six décisions sur sept sont prises, les deux
anomalies de données sont expliquées, les stations et leurs coordonnées sont acquises, le dépôt
ENA est corrigé et vérifié. L'introduction peut être écrite : ordre des hypothèses, annonce des
deux passes 4H, et phrase de nouveauté reposant sur la zone d'hybridation naturelle, l'effectif
et le génotypage sur 25 chromosomes — mais pas sur le nombre de compartiments tissulaires, déjà
au nombre de quatre dans l'article de 2017 de l'équipe.

**Ce qui reste, par ordre d'urgence :**

1. **D7, la métrique** — c'est le seul verrou restant, et il conditionne tous les chiffres
   rapportés. À instruire côté analyse ;
2. **la prédiction délai de dissection contre température** — à poser par écrit avant de lancer
   l'analyse par compartiment, sinon elle devient une explication post-hoc ;
3. **la provenance de la médiane et du D pour les cinq individus sans foie** — une question à
   André, qui décide si ces cellules doivent être vidées dans le tableau publié ;
4. **les trois sections de protocole** encore transposées du manuscrit de 2017 : capture,
   euthanasie et autorisations ; extraction et librairies ; contrôles mock et négatifs. Plus la
   vérification du financement FACIES ;
5. **l'assignation des individus de Pertuis aux deux dates de pêche**, pour affiner le dépôt ENA.

Les questions 3 à 5 sont les seules qui passent encore par André.