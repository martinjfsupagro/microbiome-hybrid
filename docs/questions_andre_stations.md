# Questions à transmettre à André — structure spatiale de l'échantillonnage

> **CADUC pour l'essentiel — ne pas envoyer tel quel.** Ce document a été rédigé le 29 août, la
> veille des réponses d'André du 30 août, qui ont fourni les neuf stations, leurs coordonnées
> WGS84, les dates de pêche, les rivières et la structure à deux stations du Suran
> (`station_reference.csv`, `decision_stations.md`). Les sections 1, 3, 4 et 5 sont donc
> répondues : seul le Suran a deux stations, tous les autres sites en ont une, et les coordonnées
> sont acquises. La seule question qui survit est le résidu de la section 2 — pourquoi la
> numérotation sépare-t-elle les classes sur des sites à station unique ? Elle est reformulée,
> avec les chiffres à jour, en section 3 de `pour_andre_questions_ouvertes.md`, qui est le
> document à envoyer. Celui-ci est conservé pour la trace de l'observation initiale.

Contexte : l'analyse du microbiote doit distinguer un effet de la classe génotypique (hotu,
hybride, toxostome) d'un effet du lieu de capture. Dans l'état actuel des métadonnées, les deux
sont largement confondus, et nous ne disposons d'aucune variable pour les séparer.

## L'observation qui motive ces questions

Les numéros d'individu attribués au terrain ne sont pas répartis au hasard entre les classes
génotypiques. À l'Ain 2015, les numéros 1001 à 1010 sont 8 hotus et 2 hybrides, les numéros 1011 à
1019 sont 9 toxostomes — séparation parfaite (test exact de Fisher, p = 0,0001). Ce que Jean-François
nous a expliqué explique cette régularité : deux stations séparées de quelques kilomètres, les
toxostomes en amont, les hotus et les hybrides en aval, avec un seuil infranchissable de l'aval
vers l'amont.

**La même signature apparaît sur quatre autres site-années**, ce qui suggère que le même codage
implicite a été utilisé ailleurs :

| site-année | numéros 1001-1010 | numéros 1011+ | p |
|---|---|---|---|
| Ain 2015 | 8 Cn, 2 Hy | 9 Pt | 0,0001 |
| Ain 2014 | 2 Cn | 4 Pt (+ série 1036-1043 : 2 Cn, 6 Pt) | 0,067 |
| Büech 2014 | 7 Cn, 1 Hy | 9 Pt | 0,0002 |
| canal 2015 | 8 Cn, 2 Hy | 8 Pt, 2 Hy | 0,0003 |
| St-Just 2015 | 8 Pt, 1 Cn, 1 Hy | 7 Cn, 2 Hy | 0,0016 |

Et **elle est absente** de Büech 2015, Avignon 2015, Baume 2015 et Manosque 2014, où les classes
sont mélangées sur toute la plage de numéros (p de 0,20 à 1,00). Cette absence est informative :
elle suggère que ces site-années ont été échantillonnés en une seule station, ou que le codage n'y
a pas été appliqué.

Deux détails supplémentaires : le sens s'inverse à St-Just (les petits numéros y sont les
toxostomes, l'inverse des autres sites), et trois site-années ont des séries de numéros
entièrement distinctes — Ain 2014 et Avignon 2014 avec une série 1036+, Pertuis 2014 avec une série 2011-2015.

## Les questions, par ordre d'importance

### 1. Pour chaque site-année, combien de stations distinctes, et lesquelles ?

C'est la question centrale. Pour chacun des onze site-années, nous avons besoin de savoir :

- **combien de points de capture distincts** ont été échantillonnés ;
- **quels individus proviennent de quel point** — et si la réponse est « les numéros 1001-1010
  d'un côté, 1011 et suivants de l'autre », c'est exactement ce qu'il nous faut, mais il faut le
  confirmer site par site, y compris là où nous ne voyons pas la signature ;
- **les coordonnées** de chaque station, ou à défaut le lieu-dit et la distance approximative
  entre stations d'un même site.

Sans cette variable, un effet de classe génotypique restera indistinguable d'un effet de lieu de
capture. Avec elle, la station entre au modèle comme effet aléatoire et l'effet de classe devient
estimable à l'intérieur des stations.

### 2. Que signifient les séries de numéros séparées ?

Trois cas :

- **Ain 2014**, série 1036-1043 (2 Cn, 6 Pt) en plus de la série 1001-1014 ;
- **Avignon 2014**, série 1036-1038 (3 Cn) en plus de la série 1001-1008 ;
- **Pertuis 2014**, série 2011-2015 (4 Pt, 1 Hy) en plus de la série 1011-1014 (4 Pt).

S'agit-il d'une autre station, d'une autre date de capture, d'un autre opérateur, ou d'une
renumérotation administrative ? Le cas de Pertuis est le plus marqué puisque les deux séries n'ont
aucun chevauchement de plage.

### 3. Nature et direction du filtre pour chaque site

Jean-François indique que le dispositif de l'Ain — barrière franchissable dans un seul sens — se
retrouve ailleurs, y compris dans des configurations symétriques. Pour chaque site à plusieurs
stations, nous avons besoin de :

- la **nature de l'obstacle** entre stations : seuil, barrage, canal, simple distance ;
- son **caractère directionnel** : infranchissable dans un sens, dans les deux, ou franchissable ;
- la **position relative** des stations (amont / aval).

Cette information n'est pas seulement méthodologique. Elle produit une prédiction testable :
**si les hybrides ne peuvent apparaître que du côté vers lequel le franchissement est possible,
alors leur position observée doit suivre la direction du filtre à chaque site.** Nous observons
déjà que les hybrides sont d'un seul côté à l'Ain 2015 et au Büech 2014, mais des deux côtés au
canal 2015 et à St-Just 2015. Si les filtres diffèrent entre ces sites, c'est cohérent et cela
devient un résultat. Si les filtres sont identiques, il y a quelque chose à comprendre.

### 4. Y a-t-il des stations où aucun individu n'a été retenu ?

Si certaines stations ont été prospectées sans capture, ou avec des captures écartées avant
séquençage, il faut le savoir : cela change l'interprétation d'une absence de classe à un site
(absence réelle contre absence d'échantillonnage).

### 5. Deux points de forme, déjà tranchés mais à consigner

- le site **Pertuis** n'a ni nom de site ni rivière renseignés dans les métadonnées : à compléter,
  y compris si le site est finalement écarté de l'analyse, puisqu'il doit être décrit dans le
  supplément ;
- **coordonnées WGS84 de chaque station** pour le dépôt ENA, qui les demande au niveau de
  l'échantillon et non du site.

## Format de réponse le plus utile

Un tableau à une ligne par station, avec : site, année, identifiant de station, plage de numéros
d'individu correspondante, latitude, longitude, position relative (amont / aval), nature de
l'obstacle vers la station voisine, direction de franchissement possible. Même partiel, ce tableau
permet de faire entrer la station au modèle ; s'il manque, nous devrons déclarer la confusion
comme une limite non traitée.