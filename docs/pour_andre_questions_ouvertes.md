# Ce qui reste à obtenir d'André

État au 25 septembre 2026, après ses réponses. Les sept décisions sont tranchées (voir
`point_etape_25sept.md`) et les deux anomalies de données sont expliquées : les blocs de
numérotation suivent l'ordre de prélèvement, les hotus étant prélevés en priorité car plus
fragiles ; et les Q-scores sont calculés sur le foie, indisponible pour cinq individus.

Trois points seulement restent à sa main.

## 1. D'où viennent la médiane et le D des cinq individus sans foie ?

Les Q-scores étant calculés sur le foie, ces cinq individus n'ont pas pu être analysés par cette
voie — leur identification vient d'autres tissus. Mais le tableau leur attribue malgré tout une
médiane et un D :

| individu | ligne du .xlsx | classe | médiane | D |
|---|---|---|---|---|
| `14Bue1001` | 27 | Cn | 0,9878 | 0,00 |
| `14Bue1002` | 28 | Cn | 0,9897 | 0,00 |
| `15Bue1014` | 119 | Pt | 0,0017 | 0,00 |
| `15Cab1011` | 154 | Pt | 0,0004 | 0,00 |
| `15Jus1008` | 170 | Pt | 0,0455 | 0,01 |

**Question : ces deux valeurs proviennent-elles d'une analyse sur un autre tissu, d'un report de
l'analyse à 12 chromosomes, ou sont-ce des cellules de remplissage ?**

L'enjeu est éditorial et non analytique : le tableau sera publié en supplément, et des colonnes
`médiane` et `D` renseignées pour des individus sans analyse Q feraient croire à un génotypage qui
n'a pas eu lieu. Selon la réponse, ces cellules sont à vider ou à documenter. Références
ligne par ligne dans `individus_sans_qvalues.csv`.

Pour le manuscrit, la formulation juste sera : 175 individus génotypés par Q-scores sur
25 chromosomes à partir du foie, 5 identifiés à partir d'autres tissus. Le fait que le tissu de
génotypage soit le foie — un cinquième tissu, absent du jeu microbiote — est à écrire
explicitement dans les Methods.

## 2. Trois sections de protocole encore transposées du manuscrit de 2017

Elles décrivent pour l'instant le lot de 2017 et doivent être confirmées ou corrigées pour le lot
Durance de 2014-2015 :

| section | état actuel | ce qu'il faut confirmer |
|---|---|---|
| §2 capture, euthanasie, autorisations | transposé | protocole et numéros d'autorisation pour 2014-2015 |
| §3 extraction et librairies | transposé (Qiagen Food Mericon, Kozich 2013, Galan 2016) | kit, version, protocole d'indexation réellement utilisés |
| §4 contrôles mock et négatifs | transposé | composition du mock et nature des témoins pour ce lot |

**Un point de financement au passage** : le préprint de 2017 mentionne un financement EDF via le
projet FACIES et l'appui de la Fédération de l'Ain. Si l'échantillonnage 2014-2015 relève du même
projet, cela doit figurer dans les remerciements et la déclaration de financement.

**Et une précision à ajouter à ces sections** : le délai entre capture et dissection, et l'ordre
dans lequel les tissus ont été prélevés sur un même poisson. Sa réponse sur la priorité donnée aux
hotus rend cette information nécessaire — voir section 1 de `point_etape_25sept.md`, où elle
conditionne l'interprétation d'un éventuel effet propre aux compartiments digestifs.

## 3. Pertuis : quel individu vient de quelle pêche

Pertuis 2014 a été pêché le 7 juillet et le 20 août, et les deux séries de numéros du fichier
(1011-1014 et 2011-2015) correspondent vraisemblablement aux deux dates. Le dépôt ENA porte pour
l'instant un intervalle, licite mais qui n'assigne pas les individus.

**Question : la série 1xxx correspond-elle à la pêche du 7 juillet et la série 2xxx à celle du
20 août, ou l'inverse ?** Même question pour les séries 1036+ de l'Ain 2014 et d'Avignon 2014, si
elles correspondent à des dates ou des passages distincts. Avec sa réponse, un second MODIFY
affine le dépôt.

## Ce qui ne passe plus par André

D1 à D6 sont tranchées. D7, le choix de la métrique de diversité, relève de la conversation
d'analyse et non de lui. Le DOI Zenodo et le préfixage des identifiants de sujet dans le dépôt
sont des décisions internes.
