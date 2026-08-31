# docs/decision_stations.md — Stations reelles, coordonnees et dates de collecte

## Source
Reponses d'Andre du **2026-08-30** (message transmis par JF Martin), qui apportent
pour la premiere fois : les coordonnees WGS84 par station, les dates de peche, les
noms de rivieres, et la **structure a deux stations du Suran**.

**Statut des coordonnees anterieures.** Le fichier `ena_deposit/ENA_sites_completes.csv`
et le `GUIDE_depot_ENA.md` attribuaient les coordonnees a Andre. C'est **inexact** :
JF Martin a confirme le 2026-08-30 qu'il s'agissait de ses propres extrapolations
(a partir de noms de communes). Les coordonnees d'Andre du 2026-08-30 sont les seules
qui font foi. Le guide est corrige en consequence.

## 1. Les neuf stations (source : Andre, DMS converti en decimal)

| Code | Station | Riviere | Latitude | Longitude | Date(s) |
|---|---|---|---|---|---|
| Ain | Pont-d'Ain + Chavannes-sur-Suran | **Suran** | 46.048000 / 46.264389 | 5.324000 / 5.429444 | 2014-08-12 |
| Cab | Pont-d'Ain + Chavannes-sur-Suran | **Suran** | idem | idem | 2015-08-26 |
| Avi | Avignon | Durance | 43.913000 | 4.820722 | 2014-07-17 ; 2015-07-10 |
| Per | Pertuis | Durance | 43.668139 | 5.493000 | 2014-07-07 ; 2014-08-20 |
| Caa | Canal (usine du Largue) | **Canal** | 43.853389 | 5.858444 | 2015-09-08 |
| Man | Manosque-Oraison | Durance | 43.919667 | 5.896278 | 2014-07-23 |
| Bue | Confluence Buech-Meouge | **Buech** | 44.262000 | 5.828000 | 2014-07-03 ; 2015-07-17 |
| Jus | Saint-Just-d'Ardeche | Ardeche | 44.286000 | 4.597833 | 2015-07-21 |
| Bau | Rosieres | **Beaume** | 44.475000 | 4.264000 | 2015-07-22 |

Fichier : `metadata/station_reference.csv`.

### Ecarts par rapport au depot ENA (PRJEB124417 deja soumis)
Distances entre la coordonnee deposee et la coordonnee reelle :

| Code | Riviere deposee | Riviere reelle | Ecart |
|---|---|---|---|
| Caa | Durance | Canal | **41,4 km** |
| Ain / Cab | Ain | Suran | **17,2 km** |
| Man | Durance | Durance | **13,4 km** |
| Bau | Ardeche | Beaume | **7,6 km** |
| Bue | Durance | Buech | **5,2 km** |
| Jus | Ardeche | Ardeche | 1,1 km |
| Per | Durance | Durance | 0,34 km |
| Avi | Durance | Durance | 0,24 km |

**Six des neuf sites** ont une coordonnee fausse de plus de 5 km, et **cinq** ont une
riviere fausse. Le depot ENA doit etre corrige via l'interface Webin (les metadonnees
d'echantillon sont modifiables apres soumission). Les dates de collecte, absentes du
depot (seule l'annee avait ete declaree, faute de dates fiables), peuvent maintenant
etre renseignees au jour pres.

### Confirmation independante
Une publication du groupe donne la station amont du Suran a
`latitude 46.264383, longitude 5.429392` (Chavannes-sur-Suran), soit **~5 m** de la
coordonnee d'Andre. Le desaccord etait possible : c'est une confirmation reelle.

## 2. Le Suran a DEUX stations, separees par une barriere

Andre : *"Uniquement le Suran barriere infranchissable (seuil de 2,5 metres) 2014-2015
entre les deux stations pour aller vers l'amont mais devalaisons sont toujours possible."*

- **Pont-d'Ain** (aval, 46.048) : les **Cn et Hy**
- **Chavannes-sur-Suran** (amont, 46.264) : les **Pt**
- 24 km separent les deux stations ; seuil de 2,5 m infranchissable **vers l'amont**,
  la devalaison reste possible -> **flux genique asymetrique**.

Assignation individu -> station (Andre) :

| Code | Pont-d'Ain (aval) | Chavannes (amont) |
|---|---|---|
| Ain 2014 | 1001, 1002, 1036, 1037 | 1011-1014, 1038-1043 |
| Cab 2015 | 1001-1010 | 1011-1019 |

Fichier : `metadata/station_mapping.csv` (cle : annee, site, individual — 180 lignes,
couverture 100 %).

### Controle : les donnees confirment l'assignation
Sur Ain 2014, ou le taxon est deja resolu :

| Station | n individus | Taxons observes |
|---|---|---|
| Pont-d'Ain | 4 | **hotu uniquement** (48 echantillons) |
| Chavannes-sur-Suran | 10 | **toxostome uniquement** (117 echantillons) |

Concordance parfaite avec le temoignage d'Andre, et **le desaccord etait possible** :
les donnees pouvaient montrer des taxons melanges a chaque station. C'est donc une
confirmation, pas une simple completude.

### Prediction testable pour Cab 2015
Cab 2015 est integralement `Ch` (non resolu). La regle d'Andre predit :
- 1001-1010 (Pont-d'Ain) -> **Cn ou Hy**
- 1011-1019 (Chavannes) -> **Pt**

C'est une **validation externe de l'index hybride** quand il arrivera : si le
genotypage contredit cette prediction, l'une des deux sources est fausse et il faudra
trancher avant d'analyser.

### Consequence pour l'analyse
`Ain` et `Cab` **ne sont pas des populations uniques**. Les traiter comme un seul site
fusionne deux populations allopatriques separees par une barriere, avec des taxons
differents. Le niveau `station` doit remplacer `site` pour le Suran dans tout modele
spatial, et la barriere fournit un contraste (amont/aval, flux asymetrique) qui a un
sens ecologique pour la question hybride.

## 3. Coquille d'annee sur 15Per2015Ch03A

Andre : Pertuis a ete echantillonne **uniquement en 2014**, en deux campagnes
(07/07/2014 pour 1011-1014 ; 20/08/2014 pour 2011-2015). Aucune campagne en 2015.

Or `15Per2015Ch03A` porte le prefixe d'annee `15`. Les trois autres tissus du meme
individu (numero 2015, **meme puits E11**) portent `14`. Le prefixe `15` est une
coquille de saisie.

**Temoin qui isole la coquille** : apres correction, l'individu Per 2015 a ses
**4 tissus complets** (branchie, caudale, hindgut, midgut) — c'est exactement ce
qu'on attend d'un seul poisson, alors qu'avant correction il apparaissait comme deux
individus a 3 et 1 tissus. Les mesures taille/poids n'existent que sur la ligne 2014,
ce qui confirme une entree unique dans le fichier de mesures.

**Traitement** : conformement a la regle du projet (les noms d'echantillons ne sont
jamais modifies), la correction passe par une table de jointure
`metadata/individual_corrections.csv`. Le `dada2_id` reste la cle vers la table ASV.

**A confirmer par Andre** avant correction du depot ENA : le depot declare
`15Per2015Ch03A` avec l'annee de collecte 2015.

### Ce que ca change dans les chiffres
| | Avant | Apres |
|---|---|---|
| Individus (par site-annee) | 181 | **180** |
| A genotyper par Andre | 132 | **131** |
| Individus Per | 10 | **9** |
| Ecart site-annee vs fusionne | 25 | **24** |

**Defaut dans mon propre travail, signale explicitement.** J'avais ecrit dans l'Article
et le supplementaire que l'ecart 181/156 = 25 etait du a deux sites, Avi (+8) et
Bue (+16). Or 8 + 16 = 24, pas 25 : je donnais un total et une decomposition
incoherents sans verifier l'arithmetique. Le 25e individu etait le fantome cree par
cette coquille. Apres correction, l'ecart est de 24 et se decompose exactement en
Avi (+8) et Bue (+16). Les documents sont corriges.

Le CSV `metadata/index_hybride_andre.csv` transmis precedemment contenait donc une
ligne fantome (`2015_Per_2015`). **Version corrigee a retransmettre a Andre.**

## 4. Numerotation non aleatoire vis-a-vis du genotype

Andre : *"on commence souvent par les hotu car ils sont plus fragiles que les
toxostome ou les hybrides. A Saint-Just on a commence par les toxo facilement
identifiables visuellement, en revanche on voyait des hotu bizarres donc on les a
fait en second."*

Le numero d'individu n'est donc **pas un identifiant neutre** : il encode l'ordre de
traitement au terrain, lui-meme correle au taxon (et, au Suran, a la station).

### Confondant mesure
Sur durance1 (727 echantillons biologiques), association taxon x colonne de plaque :
**chi2 = 330,2 ; ddl = 22 ; p = 8,7e-57 ; V de Cramer = 0,477** — association forte.
Le toxostome n'occupe que les colonnes 1, 2 et 10 ; il est **absent des colonnes 3 a 9**.

### La position a-t-elle une consequence mesurable ?
Test sur la profondeur de sequencage. La plaque etant **entierement determinee par le
tissu** (1-2 caudale, 3-4 branchie, 5-6 hindgut, 7-8 midgut), un effet "plaque" brut
serait un effet tissu deja connu. Le test doit donc etre fait **a tissu constant** :

| Tissu | Effet de la colonne sur la profondeur (Kruskal-Wallis) |
|---|---|
| caudale  | H = 51,5 ; p < 0,001 |
| branchie | H = 21,5 ; p = 0,028 |
| midgut   | H = 27,0 ; p = 0,005 |
| hindgut  | H = 25,2 ; p = 0,008 |

L'effet de position sur la profondeur **persiste dans les quatre tissus** une fois le
tissu tenu constant. Il n'est donc pas un artefact du plan de plaque par tissu.

### Statut : hypothese, pas resultat
La profondeur n'est **pas** la variable d'interet : apres rarefaction a 3 000 lectures
elle est egalisee par construction. La question qui compte est de savoir si la position
sur plaque affecte la **composition**. Ce test n'a pas ete fait : il demande une
PERMANOVA sur les donnees rarefiees avec la colonne comme terme, a tissu constant.
**Tant qu'il n'est pas fait, on ne peut pas affirmer que le confondant est sans
consequence — ni qu'il en a une.**

Rappel de contexte qui rend le risque plausible mais borne : la partition de variance
attribuait 0,03 % de la variance aux termes techniques (contre 9,2 % au tissu et 37,7 %
a l'identite du poisson). Mais elle ne contenait **pas** de terme de position dans la
plaque : cette composante n'a jamais ete estimee.

### A faire avant de conclure sur le taxon
1. PERMANOVA composition ~ colonne, a tissu constant, sur les donnees rarefiees.
2. Si effet non nul : la colonne entre comme covariable dans les modeles taxon/index
   hybride, ou les contrastes de taxon sont testes en strates de colonne.
3. Ne pas conclure sur un effet taxon sans avoir tranche ce point : taxon et colonne
   sont fortement associes (V = 0,477).

## 5. Series de numeros separees — resolu
Andre confirme les trois cas :
- **Ain 2014**, serie 1036-1043 : des **chevesnes (Sc)** avaient ete numerotes entre
  les deux series ;
- **Avignon 2014**, serie 1036-1038 : idem, chevesnes intercales ;
- **Pertuis 2014**, serie 2011-2015 : **deuxieme campagne**, le 20/08/2014, alors que
  1011-1014 datent du 07/07/2014.

Les series separees ne sont donc ni des erreurs ni des individus manquants.

## 6. Points clos
- **Aucune station prospectee sans individu retenu** (Andre, question 4).
- **Un seul obstacle** dans le jeu : le seuil de 2,5 m du Suran (question 3). Les autres
  sites n'ont pas de barriere documentee entre stations — il n'y a d'ailleurs qu'une
  station par site ailleurs.

## 7. Reste ouvert
- **Index hybride** (Andre) : debloque la question scientifique et testera la
  prediction Cab/station ci-dessus.
- **Correction du depot ENA** : coordonnees des 9 sites, rivieres, dates au jour pres,
  annee de `15Per2015Ch03A`. A faire via Webin.
- **Test de position sur la composition** (point 4).
- **Role des populations** : `Man` et `Per` restent "a statuer" dans `site_mapping.csv`.


## Distance entre les deux stations du Suran (ajout 2026-08-31)

Pont-d'Ain (46.048000 N, 5.324000 E) et Chavannes-sur-Suran (46.264389 N, 5.429444 E) sont
distantes de **25,4 km** (haversine sur les coordonnees d'Andre).

**Correction.** Une premiere redaction de la note de la Table S1 et du paragraphe 1 de
l'Article annoncait « 17,2 km apart ». C'etait faux : 17,2 km est l'ecart entre la
coordonnee ENA extrapolee (Villieu-Loyes-Mollon) et la station reelle de Pont-d'Ain,
c'est-a-dire une valeur du tableau ci-dessus, reutilisee par erreur pour une affirmation
geographique differente sans etre recalculee. La distance entre les deux stations n'avait
jamais ete calculee. Corrige dans Supplementary_Data.docx, Article.docx et
materials_and_methods.docx. Le 17,2 km du tableau des ecarts, lui, reste exact.
