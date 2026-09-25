# Analyses de sensibilité de l'indice 4H (matériel supplémentaire Camper et al. 2024)

Valeurs extraites des tables S.1.1 à S.4.2 du fichier `mee314279-sup-0001-Supinfo1.docx`.
Ces tables changent deux de mes trois recommandations précédentes.

## Le constat qui change tout : la sensibilité dépend du type de système

Amplitude de l'axe parental (U + I) sur la gamme testée, indice inspiré de Jaccard :

| levier | lézard *Aspidoscelis* (hybride naturel) | maïs B73 × Mo17 (lignées croisées) |
|---|---|---|
| ρ, de 0,1 à 0,8 | **0,520** | 0,058 |
| échelle, phylum → ASV | **0,648** | 0,280 |
| hôtes par classe, 4 → 16 | 0,114 | 0,129 |
| profondeur de lecture | 0,067 (1 000 → 10 000) | 0,013 (1 000 → 5 000) |

Sur les lignées de maïs, ρ est presque sans effet — l'indice varie de 0,058 sur toute la gamme
(0,004 seulement pour la version Bray-Curtis). Sur le système hybride **naturel**, il varie de
0,520 : plus de la moitié de l'échelle de l'indice. L'article, dans son texte principal, donne le
sens du biais mais pas cet ordre de grandeur.

Notre système est un hybride naturel en zone d'introgression, avec variation génétique et
environnementale — donc du côté du lézard, pas du maïs. **Il faut traiter ρ et l'échelle comme des
paramètres qui peuvent renverser la conclusion, pas comme des réglages de second ordre.**

## ρ : ma recommandation était trop confiante, et le sens du biais mérite précision

Détail chez le lézard (Jaccard) :

| ρ | Union | Intersection | axe parental U+I | axe transgressif G+L |
|---|---|---|---|---|
| 0,1 | 0,183 | 0,350 | 0,533 | 0,467 |
| 0,2 | 0,221 | 0,388 | 0,609 | 0,391 |
| 0,5 | 0,326 | 0,173 | 0,500 | 0,500 |
| 0,7 | 0,266 | 0,015 | 0,281 | 0,719 |
| 0,8 | 0,089 | **0,000** | 0,089 | 0,911 |

Deux choses à retenir. D'abord la dimension Intersection **s'annule** à ρ = 0,8 : au-delà d'un
certain seuil, aucun taxon n'est présent chez 80 % des hôtes des trois classes à la fois, et
l'indice devient dégénéré. Ensuite l'axe transgressif double entre ρ = 0,1 et ρ = 0,8 (0,467 →
0,911). Comme « transgressif » est précisément l'hypothèse d'intérêt du projet, **un ρ élevé la
favorise mécaniquement**. Choisir ρ élevé en invoquant la recommandation des auteurs, puis
conclure à la transgression, serait circulaire.

Le maximum de l'axe parental est atteint à ρ = 0,2 et non aux extrêmes : la relation n'est pas
monotone. Annoncer « ρ élevé » sans plus de précision ne suffit donc pas.

**Recommandation révisée.** ρ = 0,5 reste le bon choix principal — c'est celui des figures
publiées, il est au milieu de la gamme, et c'est là que les deux axes s'équilibrent chez le lézard
(0,500 / 0,500). Mais la gamme complète ρ ∈ [0,1 ; 0,8] doit être rapportée **dans le corps de
l'article et non en supplément**, avec les deux axes. Vu l'amplitude de 0,52, la reléguer en annexe
serait dissimuler la fragilité du résultat.

Écarter ρ ≥ 0,8 d'emblée, justification à l'appui : la dimension Intersection s'y annule sur le
système le plus proche du nôtre.

## Échelle taxonomique : le levier le plus fort, et l'ASV est à écarter

Chez le lézard (Jaccard), l'axe parental passe de 0,765 au phylum à 0,498 au genre et **0,117 à
l'ASV**, où Intersection tombe à 0,000 exactement. À l'échelle de l'ASV l'indice n'a plus de sens :
aucun ASV n'est partagé par les cores des trois classes. C'est un argument dur contre l'ASV, plus
solide que mon argument d'effectif de la note précédente.

Le genre reste le bon choix — échelle des figures publiées, donc comparabilité — mais la
dépendance à l'échelle est telle (0,648) que la famille doit être rapportée en sensibilité, pas
seulement mentionnée. Et la réserve sur le taux d'assignation des ASV au genre depuis un fragment
V4 de 251 pb reste entière : à mesurer sur nos données avant de trancher.

## Effectif et profondeur : les deux bonnes nouvelles

**Effectif.** De 4 à 16 hôtes par classe, l'axe parental ne bouge que de 0,114 chez le lézard, et
de façon monotone et plate au-delà de 8 (0,472 à N=8 ; 0,475 à N=10 ; 0,489 à N=12). Notre plafond
actuel de 10-12 individus par classe est donc **dans la zone stable**. Le reclassement des « Ch »
améliorera la précision des bootstraps mais ne déplacera pas l'indice : contrairement à ce que je
laissais entendre, l'analyse 4H n'est pas en attente du génotypage pour être faisable — elle l'est
seulement pour savoir qui est dans quelle classe.

**Profondeur.** L'axe parental varie de 0,067 chez le lézard sur 1 000 à 10 000 lectures et de 0,013
chez le maïs sur 1 000 à 5 000 lectures — la gamme testée diffère entre les deux systèmes,
le maïs n'ayant pas été évalué au-delà de 5 000. Notre raréfaction à 3 000 lectures est
confortable dans les deux cas. Cela confirme ce que j'avais
écrit, avec les chiffres à l'appui.

## La fenêtre d'index : l'article a un outil que je disais absent

Correction de ma note précédente. J'ai écrit que la question de découper un gradient continu
n'était « pas traitée » par Camper et al. C'est vrai du texte principal, mais la section S2
(« System Pre-analysis ») l'aborde directement, et prévoit même notre cas de figure :

Les auteurs notent que les hybrides peuvent présenter une variation génétique et environnementale
dépassant largement celle des espèces parentales, « ce qui sera particulièrement vrai pour des
hybrides en **zone d'introgression**, où il peut y avoir du backcross substantiel sur toute leur
aire ». Dans ce cas, le core de l'hybride peut ne représenter qu'une petite fraction de son
microbiote total.

Le package fournit `FourHpreanalysis`, qui calcule pour chaque classe la fraction de la richesse
microbienne totale appartenant au core. **Si le core des hybrides représente moins de 25 % de ce
qu'il représente chez les parentaux, la fonction émet un avertissement et suggère de subdiviser la
classe hybride** — par degré de backcross, position géographique ou spécificité d'habitat.

C'est une réponse partielle mais réelle à la question de la fenêtre : la décision de subdiviser
n'est pas laissée à l'arbitraire, elle est déclenchée par un critère quantitatif calculable **avant**
de regarder l'indice. Procédure à adopter :

1. constituer les trois classes avec les seuils symétriques a priori (parental si index < 0,1 ou
   > 0,9) ;
2. lancer `FourHpreanalysis` et rapporter les trois fractions de core ;
3. si l'avertissement se déclenche, subdiviser la classe hybride selon un critère déclaré d'avance —
   le degré de backcross est le plus naturel ici puisque l'index le mesure ;
4. seulement ensuite calculer l'indice.

Cette séquence est défendable en Methods parce que le critère de subdivision est extérieur au
résultat.

## Ce qui reste à vérifier

- le taux d'assignation des ASV au genre sur nos données ;
- la précision de l'index annoncée par André, qui décidera de la largeur de la fenêtre ;
- les figures S1.1 à S2.4 : le document contient 12 images que je n'ai pas examinées, seules les
  tables ont été extraites. Si un point reste ambigu, elles sont là.