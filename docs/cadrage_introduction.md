# Cadrage de l'article : objectifs, research gaps, contribution

Note de synthèse au 25 septembre 2026, préalable à la rédaction de l'introduction.
Reprend `point_etape_25sept.md`, `decisions_a_prendre.md`, `diagnostic_questions_recherche.md`,
`recommandations_consolidees.md`, `synthese_hybrides_microbiote.md`, `note_guivier2017_implications.md`,
`synthese_genotypage_25chr.md`, `decision_stations.md` et les sections Methods de `docs/manuscrit/Article.docx`.
Les chiffres sont recalculés sur les fichiers du dépôt, jamais repris de mémoire.

---

## 0. Un défaut à traiter avant les Results (et qui touche l'introduction)

**Tous les résultats de catégorie génotypique actuellement rédigés dans les Methods reposent sur
la classification à 12 chromosomes, périmée.**

Chaîne vérifiée dans le dépôt : `19-analysis_metadata.py` lit
`metadata/genotypes_andre_aout2026.csv` (12 chromosomes) et produit `analysis_metadata.csv` ;
`20-variance_partition_category.sh` et `24-permdisp.sh` consomment ce fichier. Le génotypage sur
25 chromosomes (`genotypes_verifies_sept_180.csv`, 7 septembre) n'y est pas entré.

Ce qui change entre les deux classifications :

| | août, 12 chr | septembre, 25 chr |
|---|---|---|
| Cn / Hy / Pt | 59 / 30 / 91 | **59 / 42 / 79** |
| individus reclassés | — | **16 sur 180** (13 Pt→Hy, 1 Cn→Hy, 1 Hy→Pt, 1 Hy→Cn) |
| Saint-Just (Cn/Hy/Pt) | 8 / 3 / 8 | **9 / 6 / 4** |
| Canal du Largue | 8 / 4 / 8 | **8 / 6 / 6** |
| Baume–Rosières | 21 Pt / 4 Hy | **18 Pt / 7 Hy** |
| Manosque | 13 Pt / 2 Hy | **10 Pt / 5 Hy** |

Ce que ça chiffre, concrètement :

- l'effectif hybride augmente de 40 % et l'effectif toxostome baisse de 13 % ;
- **Saint-Just et le canal du Largue sont deux des trois stations portant les trois catégories** :
  leur composition interne change fortement, or c'est exactement le sous-plan sur lequel le test
  de catégorie à station fixée est calculé ;
- ce qui ne bouge pas : les trois stations à trois catégories restent les mêmes et le total de
  74 individus tient ; les bornes de variance (1,4 à 2,7 % pour la catégorie contre 14 à 36 % pour
  la station) sont d'un ordre de grandeur tel qu'elles ne s'inverseront pas.

Deux conséquences. **Les §8.8 et 8.9 de l'Article doivent être recalculés** sur la classification
de septembre avant d'entrer dans les Results — y compris le résultat caudale/UniFrac pondéré et
l'ensemble des 48 tests PERMDISP, dont les étiquettes ont changé pour 16 poissons. Et **le §1
annonce encore « Cn (59), Hy (30), Pt (91) »** : ce décompte est à corriger en 59 / 42 / 79.

Sur l'introduction, l'effet est indirect mais réel : elle ne peut pas annoncer comme acquis un
motif dont le test sera refait. Elle annonce des questions et un dispositif, pas des résultats.
C'est de toute façon la forme correcte.

---

## 1. Où nous en sommes

**Acquis.** 180 individus, 9 stations sur 6 cours d'eau, 4 tissus par poisson, 727 librairies,
44 200 ASV sur 2 180 échantillons. Génotypage sur 25 chromosomes livré et reproduit
indépendamment (D à l'identique, règle de classification sans désaccord, clustering reproduit).
Dépôt ENA PRJEB124417 corrigé et vérifié. Structure de réplication technique établie : deux
préparations de librairie, la seconde séquencée deux fois — pas trois réplicats interchangeables.
Methods §1 et §5 à §9 rédigés.

**Six des sept décisions de design sont tranchées** (D1 à D6, réponses du 25 septembre) :
hybride = les 42, analysés en deux passes (passe 1 : les 20 génomes intermédiaires, les 22
quasi-purs exclus ; passe 2 : les 42) ; on ne dissocie pas station et classe ; tous les sites sont
gardés ; 4H en deux passes avec ρ = 0,5 au rang du genre ; les quatre tissus sont conservés.

**Reste ouvert** : D7, la métrique de diversité retenue pour les Results — seul verrou, et il
conditionne tous les chiffres, puisque tous les diagnostics produits jusqu'ici portent sur la
richesse ASV observée, métrique écartée par l'analyse de reproductibilité technique (48 % de
recapture des ASV à 1–3 lectures). Plus trois points chez André (provenance de la médiane et du D
des cinq individus sans foie ; trois sections de protocole ; assignation des individus de Pertuis
aux deux dates de pêche).

---

## 2. Les objectifs de l'article

L'article a une question principale et trois questions subordonnées. L'ordre ci-dessous est celui
que le plan d'échantillonnage soutient, du mieux répliqué au plus contraint.

**O1 — Le microbiote se réorganise-t-il chez les hybrides, et selon lequel des quatre modèles ?**
C'est la question du projet, et c'est la question que Guivier et al. 2017 posaient explicitement en
conclusion sans pouvoir y répondre. Elle se décline en trois hypothèses concurrentes — additif
(monotone entre parentaux), dominant (ressemblance à un seul parent), transgressif (hors de
l'enveloppe parentale) — auxquelles le cadre 4H de Camper et al. 2024 ajoute une lecture
taxonomique en quatre dimensions (Union, Intersection, Gain, Loss) dont l'axe Gain–Loss fournit une
définition opérationnelle de « transgressif » sans présupposer de coût de fitness.

**O2 — Cette réorganisation est-elle uniforme entre compartiments tissulaires ?**
C'est l'axe le mieux répliqué du jeu : 109 individus aux quatre tissus, 160 à au moins trois,
contraste apparié intra-individu, indépendant de toute décision de classification. Et 2017 fournit
une hypothèse dirigée et citable : les parentaux divergent le plus dans l'intestin (56–58 % d'OTU
spécifiques au toxostome en midgut et hindgut, contre 46–59 % au hotu sur les tissus externes),
donc l'effet de l'hybridation devrait être plus marqué là où les parentaux divergent le plus.

**O3 — Le motif suit-il la génétique de l'hôte ou le contexte local ?**
La moitié environnementale est démontrable : la station est de très loin le premier facteur de
composition (R² de 0,18 à 0,35 selon le tissu, contre 0,013 à 0,035 pour la catégorie). La moitié
génomique, elle, est structurellement contrainte — voir §4.

**O4 — Préalable : les deux parentaux diffèrent-ils ?**
Sans divergence parentale, la question hybride perd son objet. Test à faible puissance et à
déclarer comme tel : le contraste parental est largement confondu avec la station, et le toxostome
n'existe en effectif utile qu'à une station en 2014.

Deux questions du démarrage sont écartées et il vaut mieux l'écrire : **l'asymétrie du sens de
l'introgression** (non répliquée, deux sites sur deux rivières différentes, libellé ambigu) et la
**fonction prédite du microbiote** (PICRUSt, contestée dans la littérature récente).

---

## 3. Les research gaps que l'article met en lumière

Quatre lacunes, chacune adossée à une référence précise, et formulées de façon à ce que le
dispositif de l'article y réponde.

**G1 — Chez les poissons, la littérature sur le microbiote des hybrides est presque entièrement
expérimentale.** Ce qui existe porte sur des croisements contrôlés : hybrides réciproques de brème
et de culter, F1 de *Takifugu*, koï × poisson rouge, corégone. Aucune des références retenues ne
réunit une zone d'hybridation **naturelle**, une ascendance **quantifiée par génotypage** plutôt
que par classes de croisement, et **plusieurs compartiments tissulaires** par individu. C'est la
lacune que l'article comble, et c'est la phrase de nouveauté.

**G2 — Le champ ne tranche pas entre ascendance de l'hôte et environnement local, et les
réplicats se contredisent.** Le génotype de l'hôte domine chez *Neotoma* et chez les lémuriens
bruns ; le sol du site domine chez les babouins ; et chez la souris domestique l'effet d'admixture
devient négligeable dès qu'on tient compte de l'autocorrélation spatiale, sur deux réplicats de la
même zone d'hybridation. Ce désaccord est un gap, pas un bruit de fond : il dit que la question ne
se règle pas sans un dispositif qui sépare explicitement les deux axes.

**G3 — L'héritabilité du microbiote est réelle mais faible, ce qui fixe une barre de puissance que
la plupart des études ne franchissent pas.** Le suivi de 585 babouins sur 14 ans donne 97 % de
phénotypes significativement héritables pour une héritabilité moyenne de 0,068, et ses auteurs
concluent explicitement à la nécessité de grands effectifs. Avec un effet de cet ordre, un
contraste sur 25 individus par site est hors d'atteinte : le modèle global multi-stations n'est pas
un raffinement, c'est la seule analyse recevable.

**G4 — « Transgressif » est assimilé à une dysbiose sur la base d'un biais d'échantillonnage.**
Un travail de 2025 sur un lézard hybride écologiquement prospère montre une ségrégation
transgressive généralisée corrélée à une restructuration de niche, et argumente que les conclusions
négatives de la littérature reposent sur des hybrides de faible valeur adaptative. Étudier des
hybrides en cul-de-sac garantit de trouver que l'hybridation est délétère. Le toxostome étant
patrimonial et en régression, la tentation de lier transgression et coût de fitness sera forte :
la littérature de 2025 ne l'autorise plus sans argument.

---

## 4. Ce que le plan permet et ce qu'il ne permet pas

À poser dans l'introduction, pas à découvrir en review.

**Un seul axe est propre.** L'axe tissulaire : apparié intra-individu, 109 individus complets,
indépendant du génotypage.

**L'axe hybride est triplement contraint.** Entre stations, la catégorie est confondue avec la
station. À station fixée, elle est confondue avec la colonne de plaque, parce que la numérotation
de terrain suivait le taxon (les hotus, plus fragiles, prélevés en priorité) et que la plaque a été
chargée dans cet ordre à cinq stations sur neuf (ρ de Spearman de +0,87 à +0,95). Et les trois
stations portant les trois catégories sont précisément celles où cet enchevêtrement est maximal
(V de Cramér de 0,52 à 0,62, contre 0,18 à Rosières, seul témoin propre et petit).

**Ce que l'article fait de cette contrainte est une partie de sa contribution**, à condition de
l'annoncer : encadrement par les deux ordres séquentiels plutôt qu'une décomposition unique ;
covariable de position dans tout modèle de catégorie ; témoins qui isolent l'effet de position
(stations monoclasses, ordre symétrique, ligne et bord de plaque) ; et une prédiction posée
d'avance pour départager le délai de dissection de la température — un effet limité aux
compartiments digestifs signerait le délai, un effet présent dans les quatre signerait
l'environnement.

**Deux stations parapatriques à barrière physique constituent un contrôle négatif interne** :
Pont-d'Ain et Chavannes-sur-Suran, 25,4 km, seuil de 2,5 m infranchissable vers l'amont, hotus en
aval et toxostomes en amont, avec dévalaison possible donc flux génique asymétrique. Témoin qui
manque à la plupart des études de zones d'hybridation. Et ne plus écrire « allopatrie » : le terme
juste est parapatrie à isolement physique.

---

## 5. La contribution, énoncée précisément

**Ce qui est retiré du positionnement.** Le quatrième compartiment tissulaire. Guivier et al. 2017
séparait déjà midgut et hindgut — le résumé dit « gut », le texte dit autrement. Les quatre
compartiments de cet article sont exactement les quatre de 2017.

**Ce qui tient.**

1. **Une zone d'hybridation naturelle de poissons avec ascendance génotypée**, là où la littérature
   poisson est expérimentale (G1) ;
2. **L'effectif et la couverture spatiale** : 180 poissons sur 9 stations et 6 cours d'eau, contre
   16 poissons sur 2 stations parapatriques en 2017 — le saut d'effectif est ce qui rend O1
   posable, au vu de G3 ;
3. **Le génotypage sur 25 chromosomes**, qui distingue un génome intermédiaire d'un génome
   quasi-pur introgressé sur un seul chromosome, et permet de traiter la définition d'« hybride »
   comme une variable d'analyse — les deux passes — plutôt que comme une convention ;
4. **Un contrôle négatif interne** : deux stations parapatriques à barrière physique, réplicable
   sur deux cours d'eau (§4) ;
5. **Une caractérisation technique et spatiale rarement publiée à ce niveau** : structure de
   réplication nichée établie sur les données, effet de position dans la plaque quantifié et
   contrôlé, sélection d'échantillons induite par la raréfaction mesurée et assortie d'une analyse
   de sensibilité. Le précédent qui légitime de le présenter en préalable et non en annexe est
   l'étude épinoche de 2018, qui décompose variance biologique et technique avant de conclure sur
   l'influence génétique de l'hôte ;
6. **Une réponse à la question que 2017 posait en conclusion.** C'est le cadrage le plus économique
   de l'introduction : la suite annoncée.

---

## 6. Ce que l'introduction doit et ne doit pas faire

**Doit** : annoncer les deux analyses de la question hybride — le modèle global sur la catégorie,
et le 4H comme caractérisation complémentaire — et les deux passes de définition de l'hybride,
d'avance ; définir « transgressif » à sa première occurrence, par l'axe Gain–Loss ; reprendre la
déclaration de portée des auteurs du 4H, qui écrivent que l'indice mesure un motif et non un
processus ; et poser d'emblée le risque d'autocorrélation spatiale plutôt que de le laisser à un
relecteur.

**Ne doit pas** : lier transgression et coût de fitness (G4) ; présenter le quatrième compartiment
comme une nouveauté ; faire porter à l'axe hybride une affirmation causale que le plan ne soutient
pas — la formulation juste, conforme à la décision D2, est « un motif le long d'un gradient de
stations qui co-varie avec la catégorie et avec la température », pas « un effet de la catégorie » ;
et trancher la dichotomie branchie = immunité / intestin = régime, reproche déjà adressé à
l'introduction du manuscrit d'origine, avec les affirmations causales trop fortes et les phrases
trop longues.

---

## 7. Ce qui reste à arbitrer avant d'écrire

1. **L'ordre des hypothèses** : question hybride en tête avec le tissu comme axe de test, ou
   ossature tissulaire avec l'hybridation testée à l'intérieur. Les documents de diagnostic
   recommandent deux fois la seconde ; le positionnement « suite annoncée de 2017 » tire vers la
   première. C'est une décision d'auteur, pas une décision de données.
2. **D7, la métrique** — n'empêche pas d'écrire l'introduction, mais empêche d'y chiffrer quoi que
   ce soit.
3. **Le recalcul des §8.8 et 8.9 sur la classification de septembre** (§0), à faire avant les
   Results.
