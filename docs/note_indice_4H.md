# L'indice 4H : ce que le cadre Camper et al. 2024 permet et ne permet pas ici

Lecture du texte intégral (Methods in Ecology and Evolution 15:511-529, doi 10.1111/2041-210X.14279),
fourni par l'utilisateur. Package R **HybridMicrobiomes** v0.1.1, publié le 2023-12-05 sur le CRAN,
licence GPL-2, DOI 10.32614/CRAN.package.HybridMicrobiomes. Il existe et il est installable.

## Réponse à la question posée : l'indice 4H ne se calcule pas sur un index hybride continu

L'indice est défini sur exactement **trois classes d'hôtes** — premier parent, second parent,
hybride — et sur des ensembles de taxons microbiens *core* propres à chaque classe. La formulation
est ensembliste : P1, P2 et H sont les ensembles de taxons core des trois classes, et les quatre
dimensions se calculent à partir de cardinalités d'intersections et d'unions. Les auteurs précisent
que l'indice est « défini uniquement à partir des distributions de présence-absence ou d'abondance
microbienne sur des ensembles d'hôtes **non chevauchants** ». Un index continu ne fournit pas de
partition en trois classes non chevauchantes : il faudrait la créer par seuillage, ce que le texte
n'aborde pas. Le mot « continu » n'apparaît nulle part dans l'article ; « hybrid index » non plus.

Conclusion opérationnelle : **l'indice 4H et la régression sur index continu sont deux analyses
distinctes, pas deux variantes d'une même analyse.** La seconde reste l'analyse principale ; la
première ne peut être qu'une analyse secondaire, sur une discrétisation assumée de l'index.

## Les quatre modèles ne sont pas ceux de la note de démarrage

Correction importante : le cadre publié ne décline pas intermédiaire / transgressif / dominance.
Ses quatre modèles portent sur l'**appartenance taxonomique**, pas sur la position sur un gradient :

- **Union** — l'hybride héberge les taxons présents sur au moins un parent. Le génome de l'hôte agit
  comme un « ticket » d'acquisition ; l'hybride en a deux, donc deux microbiotes. Diversité
  attendue supérieure aux deux parents.
- **Intersection** — l'hybride n'héberge que les taxons présents sur les deux parents. Chaque génome
  agit comme une « barrière » ; deux barrières filtrent plus. Diversité attendue inférieure.
- **Gain** — l'hybride héberge des taxons présents sur aucun parent. Les auteurs l'assimilent
  explicitement à l'évolution saltationnelle de Bateson et aux « hopeful monsters » de Goldschmidt,
  et le qualifient de scénario « à haut risque, haute récompense » : les nouveaux microbes peuvent
  aussi bien augmenter que réduire la valeur adaptative de l'hôte.
- **Loss** — l'hybride a perdu des taxons présents sur un ou les deux parents.

Ces quatre modèles sont des **cas limites idéalisés**, jamais observés purs : tout système réel est
une combinaison, et l'indice 4H mesure la part de chacun (les quatre dimensions sommant à 1, soit
trois dimensions indépendantes).

Le lien avec le vocabulaire du projet passe par les deux axes du diagramme quaternaire :
**axe parental** = Union + Intersection, **axe transgressif** = Gain + Loss. C'est cet axe
transgressif qui correspond à l'hypothèse « transgressif » de la note. Le contraste entre les
systèmes publiés est net : chez le rat Neotoma, l'axe transgressif ne pèse que 0,124 (Intersection
dominant à 0,775), alors que chez le lézard Aspidoscelis il atteint 0,712 et chez la cigale Kikihia
0,641 (indice inspiré de Bray-Curtis, Table 3).

## Ce que le cadre apporte que la formulation actuelle du projet n'a pas

**Les « plans nuls ».** L'indice seul confond deux types de perte : perdre un taxon présent sur un
seul parent (attendu par simple intersection) et perdre un taxon présent sur les deux (perte
saltationnelle, biologiquement bien plus intéressante). Les auteurs construisent un plan nul sous
l'hypothèse que tous les taxons parentaux ont la même probabilité d'être perdus. Un indice situé
du côté Intersection par rapport à ce plan signifie que l'hybride retient préférentiellement les
taxons partagés ; du côté Union, que la perte est concentrée sur les taxons partagés — donc
saltationnelle. C'est le test qui distingue une perte banale d'une perte informative, et il n'a pas
d'équivalent dans le plan d'analyse actuel du projet.

**Une déclaration explicite de portée.** Les auteurs écrivent que l'indice est une mesure de
*motif* et non de *processus*, à l'image de la diversité bêta, et qu'il « ne devrait pas servir à
discriminer entre mécanismes de réassemblage ». Ils le présentent comme un outil exploratoire de
formulation d'hypothèses, pas comme un test de causalité. À reprendre telle quelle : c'est
précisément la prudence que la revue critique de l'introduction d'origine réclamait.

## Trois contraintes techniques qui touchent directement ce jeu de données

**1. Plan équilibré exigé, et il coûte cher ici.** L'indice suppose le même nombre d'hôtes N dans
chaque classe ; le package rééchantillonne pour y parvenir. Sur nos données après raréfaction :

| tissu | hotu (Cn) | toxostome (Pt) | Ch | N équilibré possible |
|---|---|---|---|---|
| peau (caudale) | 32 | 12 | 101 | **12** |
| branchie | 32 | 11 | 129 | **11** |
| midgut | 34 | 10 | 107 | **10** |
| hindgut | 25 | 11 | 122 | **11** |

Le toxostome plafonne le plan à 10-12 individus par classe et par tissu. C'est du même ordre que
les systèmes publiés (7 individus par classe pour la cigale, le rat et le lézard ; 10 pour le maïs),
donc ce n'est pas disqualifiant — mais l'analyse 4H n'exploitera qu'une petite fraction des 132
hybrides, et le reste de la puissance ne peut venir que de la régression sur index continu.

**2. La profondeur de séquençage n'est presque pas un problème pour cet indice.** Les auteurs
rapportent un effet quasi nul de la profondeur au-delà de ~1 000 lectures, parce que l'indice
porte sur les microbiotes *core* : les taxons rares, ceux que perd une faible profondeur, ne sont
de toute façon pas dans le core. Ils jugent la standardisation de profondeur « largement inutile ».
C'est une bonne nouvelle ciblée : les sites que la raréfaction à 3 000 lectures pénalise le plus
(canal en peau et midgut) sont moins pénalisés pour une analyse 4H que pour une analyse de richesse.

**3. Trois seuils de core, pas un, et une échelle taxonomique à fixer.** Le package expose ρ
(fraction d'hôtes portant le taxon), ϑ (abondance relative moyenne minimale) et ε (abondance
minimale sur au moins un hôte), avec ϑ = ε = 0 par défaut. Les figures publiées utilisent ρ = 0,5
au niveau du **genre** — correction : le mot « phylum » n'apparaît pas dans l'article, contrairement
à ce que j'avais écrit ici. Les auteurs montrent qu'un ρ bas et une échelle taxonomique élevée
favorisent tous deux Intersection, et exigent des valeurs identiques pour toute comparaison entre
systèmes. Arguments détaillés et recommandations dans `note_parametres_4H.md`.

## Effet sur le plan d'analyse

L'article ne change pas l'analyse principale : la régression du microbiote sur l'index hybride
continu, avec site et individu en effets aléatoires, reste le cœur. Il ajoute une analyse secondaire
bien cadrée et un vocabulaire publié, et il déplace un point du plan : l'axe Gain-Loss donne une
définition opérationnelle de « transgressif » qui ne présuppose aucun coût de fitness — cohérent
avec la position de Microbiome 2025 sur les hybrides prospères, et avec la correction déjà apportée
à la synthèse.

Point à trancher pour l'introduction : faut-il annoncer les deux analyses, ou ne garder le 4H qu'en
discussion ? Annoncer les deux oblige à justifier une discrétisation de l'index alors que le projet
vient de décider d'en faire une variable continue unique. Le compromis le plus défendable est de
réserver le 4H aux trois classes déjà génotypées avec certitude (Cn=0, Pt=1, et les Ch dont l'index
tombera dans une fenêtre intermédiaire à définir *avant* de voir la distribution).