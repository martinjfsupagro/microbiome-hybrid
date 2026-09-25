# Arguments pour fixer ρ, l'échelle taxonomique et la fenêtre d'index

> **Note révisée après lecture du matériel supplémentaire.** Les tables S.1.1 à S.4.2 quantifient
> l'ampleur des biais et corrigent deux recommandations ci-dessous : ρ et l'échelle sont bien plus
> déterminants sur un système hybride naturel que sur les lignées croisées (amplitude 0,52 et 0,65
> contre 0,06 et 0,28), et la section S2 fournit un critère quantitatif pour décider de subdiviser
> la classe hybride, que je disais absent. Voir `note_sensibilite_4H.md`, qui prévaut sur les
> recommandations de cette note.

Réponse tirée du texte de Camper et al. 2024, avec les passages à l'appui. Une correction
préalable : j'avais écrit que les figures publiées utilisaient l'échelle du **phylum**. C'est faux.
Le mot « phylum » n'apparaît pas une fois dans l'article ; les figures 2 et 3 travaillent au
**genre** (« 500 bootstrapped genus-level microbial samples »). Les phyla que je citais venaient de
Guivier 2017, pas de Camper.

Autre point à savoir avant de lire : ρ n'est pas seul. Le package expose **trois** seuils de core.

| seuil | ce qu'il contrôle | défaut du package |
|---|---|---|
| ρ | fraction des hôtes d'une classe portant le taxon | à choisir |
| ϑ | abondance relative moyenne minimale, sur tous les hôtes de la classe | 0 |
| ε | abondance relative minimale atteinte sur au moins un hôte | 0 |

ρ, ϑ et ε sont communs aux trois classes d'hôtes, mais le core est calculé **séparément** pour
chaque classe. Les défauts ϑ = ε = 0 donnent un core d'incidence pure.

## 1. Le seuil de core ρ

### Ce que l'article argumente

ρ va de 1 (taxon retenu seulement s'il est présent sur *tous* les hôtes de la classe) à 0 (microbiote
complet, tous les taxons retenus). Les auteurs recommandent des valeurs **élevées**, sur un argument
explicite : un taxon microbien ayant des conséquences fortes pour l'écologie ou l'évolution de
l'hôte devrait être détectable chez la majorité des hôtes de la population. C'est une hypothèse
biologique, pas une commodité statistique — et elle est réfutable : si vous pensez que l'effet
intéressant passe par des taxons rares, l'argument tombe et un ρ plus bas se justifie.

Les auteurs ajoutent deux échappatoires : utiliser un ρ plus bas si l'on a raison de penser
autrement, ou **comparer l'indice sur une gamme de valeurs de ρ**. Cette seconde option est la plus
défendable ici (voir ci-dessous).

Le sens du biais est documenté : définir le core sur une fraction plus **basse** d'hôtes favorise la
dimension **Intersection**, pour une raison mécanique — au moins quelques hybrides et quelques
individus de chaque parent porteront un taxon donné, même s'il ne s'agit que d'une acquisition
transitoire depuis l'environnement. Un ρ bas fait donc entrer du bruit environnemental dans les
trois cores simultanément, ce qui gonfle leur intersection.

### L'argument spécifique à ce jeu de données

ρ n'agit pas sur une fraction continue mais sur un **nombre entier d'hôtes**, ⌈ρN⌉, et N est petit
ici. Avec le plafond de plan équilibré actuel :

| N par classe | ρ = 0,5 | ρ = 0,7 | ρ = 0,9 |
|---|---|---|---|
| 10 (midgut aujourd'hui) | 5 hôtes | 7 | 9 |
| 12 (peau aujourd'hui) | 6 | 9 | 11 |
| 20 (après reclassement des Ch) | 10 | 14 | 18 |
| 25 | 13 | 18 | 23 |

À N = 10, un hôte de plus ou de moins déplace la prévalence de 10 points : la granularité de ρ est
grossière et un ρ « précis » serait une illusion de précision. À N = 20-25, ρ = 0,5 correspond à
10-13 hôtes et le seuil devient réellement discriminant.

**Recommandation.** Fixer ρ = 0,5 comme valeur principale — c'est celle des figures publiées, ce qui
rend l'indice directement comparable aux quatre systèmes de l'article (rat, lézard, cigale, maïs) —
et déclarer *avant analyse* que l'indice sera aussi rapporté pour ρ ∈ {0,4 ; 0,6 ; 0,7} en matériel
supplémentaire. Garder ϑ = ε = 0 (défauts), pour ne pas cumuler trois seuils arbitraires.

L'engagement à publier la gamme est ce qui protège réellement : il rend impossible de choisir ρ
après avoir vu le résultat, puisque tous les résultats seront montrés.

## 2. L'échelle taxonomique

### Ce que l'article argumente

L'indice s'applique à n'importe quelle échelle taxonomique, mais une échelle **plus élevée** prédit
une importance plus grande de la dimension **Intersection** — même sens de biais que pour un ρ bas,
et pour une raison analogue : plus on agrège, plus les trois classes partagent forcément leurs
taxons. Les auteurs sont catégoriques sur la conséquence : les systèmes doivent toujours être
comparés à la **même** échelle taxonomique, et l'interprétation de l'indice doit toujours se faire
dans le contexte de l'échelle choisie.

### L'argument spécifique

Le genre est l'échelle des figures publiées, donc celle qui permet la comparaison externe. Mais
attention à un point qui vous concerne : vos données sont en **ASV**, et l'affectation taxonomique
au genre depuis un fragment V4 de 251 pb est incomplète — une fraction des ASV restera non assignée
au genre et sera perdue par l'agrégation. Il faut mesurer cette fraction avant de trancher, parce
qu'elle décide si le genre est praticable ou s'il faut remonter à la famille.

**Recommandation.** Genre comme échelle principale, sous réserve de vérifier le taux
d'assignation ; famille en analyse de sensibilité. Déclarer explicitement le pourcentage d'ASV
agrégés et perdus. Ne pas travailler à l'ASV : chaque ASV serait présent chez trop peu d'hôtes pour
qu'un core au sens de ρ ait un sens à N = 10-25.

## 3. La fenêtre d'index « intermédiaire »

### Ce que l'article dit : rien

Point important à savoir avant lecture : **cette question n'est pas traitée dans Camper et al.**
L'indice y est défini sur trois classes d'hôtes déjà données — les mots « continu » et « hybrid
index » sont absents de l'article. Tous leurs systèmes ont des classes non ambiguës : hybrides de
laboratoire, lignées de maïs, espèces parthénogénétiques. Le problème de découper un gradient
continu en trois classes est le **notre**, pas le leur, et aucun argument d'autorité ne le couvre.

### Ce sur quoi s'appuyer à la place

La seule contrainte issue de l'article est structurelle : les trois classes doivent être **non
chevauchantes**, et le plan doit être équilibré, N identique dans les trois classes — le package
sous-échantillonne pour y parvenir. Cela suffit à écarter les découpages fantaisistes mais ne
désigne aucun seuil.

Trois options défendables, à choisir avant de voir la distribution :

1. **Seuils symétriques a priori** : parental si index < 0,1 ou > 0,9, hybride entre 0,1 et 0,9. Le
   plus simple à défendre parce qu'indépendant des données. Mais il peut vider une classe si les
   index se concentrent aux extrémités.
2. **Seuils fondés sur la génétique** : classes définies par l'attendu théorique des générations
   (F1 autour de 0,5, backcross autour de 0,25 et 0,75), avec une tolérance liée à la précision de
   l'index. Demande de connaître cette précision — à demander à André avec le fichier.
3. **Renoncer à discrétiser et ne pas faire de 4H.** Option à garder ouverte : si la distribution
   est unimodale et étalée, tout découpage sera arbitraire et l'indice n'ajoutera rien à la
   régression continue.

**Recommandation.** Écrire maintenant que l'option 1 sera appliquée, avec le repli explicite sur
l'option 3 si une classe descend sous N = 10 individus — l'ordre de grandeur des systèmes publiés
(7 hôtes par classe pour le rat, le lézard et la cigale ; 10 pour le maïs). Décider maintenant le
critère d'abandon est ce qui distingue une analyse planifiée d'une analyse opportuniste.

## Ce qui reste à vérifier avant de figer

- le taux d'assignation des ASV au genre, sur vos données (décide le point 2) ;
- la précision de l'index hybride annoncée par André (décide entre les options 1 et 2 du point 3) ;
- les figures et tables supplémentaires S1.1-S1.4 et S2.1-S2.4 de Camper et al., qui contiennent
  les analyses de sensibilité à l'échelle taxonomique et à ρ. Le PDF que vous m'avez fourni est
  l'article principal ; ces annexes en sont absentes. Si vous pouvez les récupérer, elles
  quantifieraient l'ampleur des deux biais au lieu de nous en laisser seulement le sens.