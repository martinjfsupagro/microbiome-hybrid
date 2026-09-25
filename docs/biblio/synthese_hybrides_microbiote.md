# Le microbiote des hybrides : état de la littérature mobilisable

Veille exploratoire, projet microbiome-hybrid. 52 références retenues, dont 4 préprints signalés
comme tels. Bilan de recherche : 3 583 notices balayées (Semantic Scholar en masse + OpenAlex),
820 candidates après préfiltre lexical, couverture des résumés 97,6 %, puis boule de neige sur
6 semences (775 notices, 69 nouvelles candidates). Criblage assisté validé sur un échantillon de
36 décisions, exclusions comprises : 89 % d'accord (32/36), les 4 désaccords portant tous sur des
cas limites et aucun sur une référence structurante. Couverture DOI 49/52 (94 %).

## Les quatre modèles concurrents ont un nom et un cadre publié

Un cadre conceptuel dédié existe, avec un package R publié sur le CRAN — HybridMicrobiomes
v0.1.1, GPL-2 (Methods in Ecology and Evolution 15:511-529, 2024, doi 10.1111/2041-210x.14279).
Le texte intégral a été lu ; deux corrections en découlent par rapport à une lecture du seul
résumé.

D'abord, ses quatre modèles ne sont pas ceux du projet. Ils portent sur l'appartenance
taxonomique, pas sur la position sur un gradient : **Union** (l'hybride héberge les taxons de au
moins un parent — le génome comme « ticket » d'acquisition), **Intersection** (seulement les
taxons communs aux deux parents — chaque génome comme « barrière »), **Gain** (des taxons
présents sur aucun parent) et **Loss** (perte de taxons parentaux). Ce sont des cas limites
idéalisés, jamais purs : l'indice mesure la part de chacun, les quatre dimensions sommant à 1.
Le pont vers le vocabulaire du projet passe par les deux axes du diagramme quaternaire — axe
parental (Union + Intersection) et **axe transgressif (Gain + Loss)**. C'est cet axe qui donne une
définition opérationnelle de « transgressif », et elle ne présuppose aucun coût de fitness.

Ensuite, et c'est déterminant pour le plan d'analyse : **l'indice ne se calcule pas sur un index
hybride continu**. Il est défini sur trois classes d'hôtes non chevauchantes et sur des ensembles
de taxons core, par cardinalités d'unions et d'intersections. Les mots « continu » et « hybrid
index » sont absents de l'article. Régression sur index continu et indice 4H sont donc deux
analyses distinctes, la seconde exigeant une discrétisation assumée. Détail complet et contraintes
d'effectif dans `note_indice_4H.md`.

## La thèse « transgressif = dysbiose » est contestée, et c'est une ouverture

L'article le plus utile au cadrage est aussi le plus récent : il attaque frontalement le
consensus selon lequel l'hybridation détruit la symbiose hôte-microbiote. Son argument est
méthodologique et vise le biais d'échantillonnage de la littérature : les conclusions négatives
reposent sur des hybrides de faible valeur adaptative, et étudier des hybrides « en cul-de-sac »
garantit de trouver que l'hybridation est délétère. Sur un lézard hybride écologiquement
prospère, les auteurs trouvent au contraire une ségrégation transgressive généralisée, corrélée
à une restructuration de niche, et proposent que l'hybridation génère des phénotypes holobiontes
nouveaux et potentiellement bénéfiques (Microbiome, 2025, doi 10.1186/s40168-024-01994-8).

Conséquence directe pour l'introduction : « transgressif » ne doit pas être présenté comme
synonyme de rupture ou de dysbiose. Le toxostome étant une espèce patrimoniale en régression,
la tentation de lier transgression et coût de fitness sera forte — la littérature 2025 ne
l'autorise plus sans argument. C'est aussi exactement le reproche que la revue critique de
l'introduction du manuscrit d'origine formulait déjà : affirmations causales trop fortes.

## Génétique de l'hôte contre environnement : le champ ne tranche pas, et les réplicats se contredisent

C'est le point le plus important pour la question secondaire 2 du projet, et le plus
inconfortable : sur des zones d'hybridation naturelles, les études récentes concluent en sens
opposé, y compris entre systèmes proches.

Du côté « l'ascendance de l'hôte domine » : chez des rats du désert (Neotoma), l'habitat
détermine le régime alimentaire mais le génotype de l'hôte détermine le microbiote intestinal,
avec une composition intermédiaire chez les hybrides de première génération — le motif additif
observé directement (Ecology Letters, 2022, doi 10.1111/ele.14135). Chez des lémuriens bruns
hybrides, l'ascendance de l'hôte l'emporte sur l'écologie le long d'un transect de 180 km
(préprint, doi 10.64898/2025.12.10.693535).

Du côté inverse : chez des babouins couvrant une zone d'hybridation, ni l'ascendance génétique,
ni l'apparentement, ni la distance génétique entre populations ne prédisent fortement le
microbiote — ce sont les propriétés du sol du site qui l'expliquent (Proceedings B, 2019,
doi 10.1098/rspb.2019.0431). Chez la souris domestique, un effet d'admixture qui devient
négligeable dès qu'on tient compte de l'autocorrélation spatiale, sur deux réplicats de la même
zone d'hybridation (Molecular Ecology, 2023, doi 10.1111/mec.17192).

Ce dernier résultat est celui à lire en priorité côté méthode. Il montre qu'un effet
génomique apparent peut n'être qu'une structure spatiale mal contrôlée — le risque exact du plan
de ce projet, où site, rivière, année et rôle de population sont largement confondus.

Un résultat récent suggère de découper la question autrement, mais il faut le citer avec sa
propre réserve. Chez des mésanges hybrides transférées d'un milieu naturel vers un environnement
commun contrôlé, le changement d'environnement affecte significativement la richesse du
microbiote intestinal, alors qu'il n'affecte pas la composition de la communauté (diversité
bêta). Les auteurs ajoutent qu'un effet de l'ascendance sur la composition, supérieur à celui de
l'environnement, est possible — mais ils précisent explicitement qu'il **n'est pas
statistiquement significatif** (Ecosphere, 2026, doi 10.1002/ecs2.70611).

Ce qui est établi dans cette étude est donc le découplage entre métriques du côté de
l'environnement (effet sur la richesse, pas sur la composition), pas la contrepartie génomique.
À utiliser comme raison de rapporter systématiquement diversité alpha et diversité bêta
séparément, et non comme prédiction d'un effet d'ascendance sur la composition : ce serait
transformer un résultat non significatif en hypothèse dirigée.

## L'héritabilité du microbiote est réelle mais faible — ce qui fixe la barre de puissance

Le chiffre à retenir vient d'un suivi longitudinal de 16 234 profils sur 585 babouins sauvages
pendant 14 ans : 97 % des phénotypes de microbiote sont significativement héritables, mais
l'héritabilité est typiquement faible, de moyenne 0,068, et dépend du contexte — plus forte en
saison sèche et chez les hôtes âgés. Les auteurs concluent explicitement que des profils
longitudinaux et de grands effectifs sont indispensables pour quantifier cette héritabilité
(Science, 2021, doi 10.1126/science.aba5483).

C'est la référence qui légitime le cadrage de puissance du diagnostic précédent. Avec une
héritabilité de cet ordre, chercher un effet génomique sur 25 individus par site est hors
d'atteinte, et le modèle global multi-sites n'est pas un raffinement statistique mais la seule
analyse recevable.

Une étude sur épinoche complète l'argument par le versant technique : elle quantifie les
composantes de variance biologique et technique avant de conclure sur l'influence génétique de
l'hôte, en insistant sur la nécessité de cette décomposition préalable (mSystems, 2018,
doi 10.1128/msystems.00331-19). C'est le précédent qui justifie de présenter la partition de
variance tissu/site/run comme un préalable et non comme un supplément.

## Chez les poissons, la littérature existe mais elle est presque entièrement expérimentale

C'est le vrai créneau de l'article, et il faut le nommer précisément.

Ce qui existe porte sur des croisements contrôlés : hybrides réciproques de brème et de culter
aux régimes alimentaires opposés, avec corrélation forte entre génotype et caractéristiques
intestinales (Frontiers in Microbiology, 2018, doi 10.3389/fmicb.2018.02972) ; hybrides F1 de
Takifugu où l'hybridation de l'hôte domine sur la cohabitation (mSystems, 2023,
doi 10.1128/msystems.01181-22) ; hybrides réciproques de carpe koï et de poisson rouge, dont le
microbiote ressemble davantage au koï — un cas de dominance parentale (Journal of Applied
Microbiology, 2022, doi 10.1111/jam.15616). Le corégone est le système le plus proche d'une
question évolutive, avec des paires d'espèces sympatriques et leurs hybrides réciproques comparés
en milieu naturel et en conditions contrôlées (préprint, doi 10.1101/312231).

Une synthèse dédiée au microbiote intestinal des poissons hybrides existe (Microorganisms, 2022,
doi 10.3390/microorganisms10050891) : à lire pour ne pas réinventer son plan.

Ce qui manque, et que ce projet peut fournir : une zone d'hybridation **naturelle** de poissons,
avec un index d'ascendance **continu** plutôt que des classes de croisement, et **quatre
compartiments tissulaires** par individu. Aucune des références retenues ne réunit ces trois
éléments. C'est la phrase de nouveauté de l'introduction, et elle est défendable.

## Les zones d'hybridation permettent la cartographie d'association — une piste pour plus tard

Un travail sur la fauvette à croupion jaune exploite le fait que la recombinaison génétique
brasse les allèles divergents chez les individus rétrocroisés, ce qui permet d'identifier des
associations entre régions génomiques et traits, appliqué ici à la composition du microbiote
(Molecular Ecology, 2026, doi 10.1111/mec.70498). Hors de portée avec un index hybride scalaire,
mais à citer si vous voulez ouvrir la discussion sur ce que permettrait un génotypage plus dense.

## Ce qu'il reste à faire côté bibliographie

Trois références retenues n'ont pas de DOI (dépôts institutionnels de Kiel, Washington University
et Max Planck) : elles sont dans le .bib mais Zotero ne pourra pas résoudre leur PDF
automatiquement. Aucune rétractation détectée sur les 49 DOI vérifiés.

Le texte intégral du cadre conceptuel 4H (doi 10.1111/2041-210x.14279) est resté verrouillé :
Unpaywall le donne en accès doré mais aucune source atteignable d'ici ne sert le PDF, et le
package R annoncé dans le résumé n'est trouvable ni sur GitHub ni via les registres accessibles.
Ce texte est le seul de la sélection dont la lecture complète changerait le plan d'analyse —
il définit les quatre modèles et la formule de l'indice. À récupérer via votre accès
institutionnel et à déposer ici : je pourrai alors dire si l'indice 4H est calculable sur un
index hybride continu ou s'il suppose des classes discrètes.