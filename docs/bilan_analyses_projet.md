# Bilan des analyses du projet microbiome-hybride

État au 25 septembre 2026. Ce document recense ce qui a été analysé, par qui et avec quel
résultat, à travers les quatre conversations du projet. Les artefacts sont nommés pour pouvoir
être retrouvés ; les décisions ouvertes sont dans `decisions_a_prendre.md`.

Le projet compte 156 artefacts répartis en quatre volets : le dépôt de données (42), l'analyse
des données (74), la bibliographie et le design (28) et les fichiers sources fournis (12).

## 1. Le jeu de données

**180 individus**, deux espèces de cyprinidés et leurs hybrides, prélevés en 2014-2015 sur
**neuf stations** réparties sur six cours d'eau (Suran, Durance, canal du Largue, Büech, Ardèche,
Beaume). Quatre tissus par poisson — peau caudale, branchie, midgut, hindgut — soit **727
librairies**, chacune séquencée sur trois runs MiSeq, pour 2 174 échantillons rattachés.

L'effectif a été corrigé de 181 à 180 : une coquille de préfixe d'année sur `15Per2015Ch03A`
scindait un poisson en deux. Pertuis n'a été échantillonné qu'en 2014, en deux campagnes.

## 2. Contrôle qualité et caractérisation technique

**Structure des trois runs, tranchée.** `durance1` est une préparation de librairie distincte ;
`durance2` et `durance3` sont deux séquençages d'une même librairie (corrélation de profondeur
rho = 0,9987, Bray-Curtis intra-échantillon 0,118 contre 0,248 entre librairies). Ce ne sont donc
pas trois réplicats indépendants, et le Materials & Methods a été corrigé en conséquence.
Artefacts : `run_design_summary.txt`, `results_paragraph_technical.txt`.

**Conséquence majeure sur le choix de métrique.** Un re-séquençage de la même librairie ne
retrouve que 48 % des ASV présents à 1-3 lectures. La richesse observée est donc peu
reproductible sur les taxons rares, et les analyses de diversité du manuscrit reposent sur des
métriques pondérées par l'abondance. **Tous les résultats de diagnostic produits en richesse ASV
observée gardent une valeur de faisabilité mais ne peuvent pas entrer dans les Results tels
quels.**

**Décontamination, mocks, profondeur.** `decontam_scores.tsv`, `mock_validation_summary.txt`,
`mock_blast.tsv`, `mock_leakage.tsv`, `empty_totals.tsv`, `depth_thresholds.tsv`,
`rarefaction_curves.tsv`, `beta_convergence.tsv`. Seuil de raréfaction retenu : 3 000 lectures,
avec analyse de sensibilité. Figures : `fig_qc_depth.png`, `fig_depth_tradeoff.png`,
`fig_rarefaction_convergence.png`, `fig_technical_vs_biological.png`.

**Effet de position dans la plaque, quantifié et rédigé.** L'effet de la colonne de plaque sur la
composition est réel : R² de 0,18 à 0,40 selon la métrique et le sous-ensemble, significatif dans
9 à 12 strates sur 12, avec un effet par degré de liberté comparable à celui du taxon.
Artefacts : `position_tests.tsv`, `position_effect_synthesis.csv`, `position_summary.txt`,
`fig_position_effect.png`, `permdisp.tsv`, `fig_permdisp.png`.

## 3. Métadonnées spatiales : neuf stations, et une structure à deux stations

Les coordonnées et dates réelles ont été obtenues d'André le 30 août. Elles ont révélé que les
coordonnées antérieures du dépôt étaient des extrapolations : **six des neuf sites avaient une
coordonnée fausse de plus de 5 km et cinq une rivière fausse**, jusqu'à 41,4 km d'écart pour le
canal du Largue. Corrigé dans la Table S1 et dans le dépôt.

**Le Suran a deux stations séparées par une barrière.** Pont-d'Ain (aval, les hotus et hybrides) et
Chavannes-sur-Suran (amont, les toxostomes), 24 km d'écart, seuil de 2,5 m infranchissable vers
l'amont mais dévalaison possible — donc flux génique asymétrique. Une publication indépendante du
groupe confirme la coordonnée amont à 5 m près. Artefacts : `decision_stations.md`,
`station_reference.csv`, `station_mapping.csv`, `table_S1_stations.csv`.

**Validation croisée réussie.** L'assignation individu → station fournie par André prédisait que
les individus 1001-1010 de l'Ain 2015 seraient hotu ou hybride et les 1011-1019 toxostome. Le
génotypage sur 25 chromosomes, arrivé ensuite, confirme **19 individus sur 19**. Sur les deux
années du Suran, la séparation station × classe est parfaite (Pont-d'Ain : 12 Cn, 2 Hy, 0 Pt ;
Chavannes : 0, 0, 19). Le désaccord était possible : c'est une validation réelle de l'index
hybride par une source indépendante.

## 4. Dépôt des données

Projet ENA PRJEB124417, **727 échantillons** et les trois runs déposés. Les métadonnées ont été
corrigées après soumission par MODIFY le 31 août : 3 472 champs vérifiés un par un, zéro écart.
Artefacts : les scripts `1_` à `7_`, `GUIDE_depot_ENA.md`, `MEMO_correction_ENA.md`,
`ENA_accessions_durance.tsv`, `identity_check.tsv`, `DATA_AVAILABILITY.md`.

## 5. Génotypage : trois itérations

| étape | base | Cn / Hy / Pt |
|---|---|---|
| détermination morphologique | — | 37 / 0 / 131 « Ch » indéterminés |
| août 2026 | 12 chromosomes | 59 / 30 / 91 |
| septembre 2026 | 25 chromosomes | 59 / 42 / 79 |

**Huit déterminations morphologiques sont contredites par le génotype** sur les 49 individus
initialement déterminés à l'espèce (16 %), ce qui justifie le génotypage à lui seul.

Les calculs d'André ont été reproduits indépendamment depuis les Q-values par chromosome : D à
l'identique, médiane à 0,0095 près, règle de classification reproduite sans aucun désaccord,
clustering hiérarchique reproduit avec des tailles de clusters identiques. La polarité des
Q-values est harmonisée malgré l'alternance des préfixes Q1 et Q2.

**Le passage à 25 chromosomes a ajouté 12 hybrides nets**, tous de type « quasi-pur introgressé » :
médiane restée à l'extrême mais un chromosome divergent. La classe Hy réunit donc désormais
20 génomes intermédiaires et 22 quasi-purs, dont 17 introgressés sur un seul chromosome sur 25.
Artefacts : `synthese_genotypage_25chr.md`, `genotypes_verifies_sept_180.csv`,
`fig_genotypage_25chr.png`, `verification_genotypage_design.md`, `genotypes_verifies_180.csv`.

## 6. Analyse écologique : ce qui est fait

**Partition de variance encadrée.** Sur la composition (Bray-Curtis, Jaccard, UniFrac pondéré et
non pondéré), avec les trois termes station, position et catégorie. La station domine (R² de 0,18
à 0,35 selon le tissu), la catégorie apporte 0,013 à 0,035, la position 0,011 à 0,028. La
catégorie n'est que partiellement identifiée et l'encadrement par les deux ordres séquentiels est
rapporté. Artefacts : `category_partition.tsv`, `category_summary.txt`, `fig_category_effect.png`,
`d500_category_partition.tsv`.

**Métriques phylogénétiques calculées** : UniFrac pondéré et non pondéré, Faith PD, moyennés sur
1 000 tirages de raréfaction. `alpha_mean_1000.tsv`, `alpha_phylo_mean.tsv`, `phylo_summary.txt`,
`phylo_convergence.tsv`.

**Diagnostic de faisabilité et de puissance** (en richesse ASV observée, donc à recalculer) :
partition de variance à 18,7 % pour le tissu contre 10,9 % pour le site et 0,26 % pour le run ;
réplication des trois résultats de l'article de 2017 de l'équipe ; calculs de puissance par tissu
et par classe. Artefacts : `diagnostic_questions_recherche.md`, `fig_design_puissance.png`,
`note_guivier2017_implications.md`, `fig_replication_guivier2017.png`, `note_precisions_design.md`,
`fig_precisions_design.png`, `analyse_couts_benefices_sites.md`, `fig_couts_benefices_sites.png`.

## 7. Cadre conceptuel et bibliographie

**Un cadre publié existe pour les hypothèses du projet** : l'indice 4H de Camper et al. 2024
(*Methods in Ecology and Evolution* 15:511-529), avec le package R HybridMicrobiomes sur le CRAN.
Le texte intégral et son matériel supplémentaire ont été lus et analysés. Deux acquis
déterminants : l'indice se calcule sur **trois classes d'hôtes non chevauchantes** et non sur un
index continu ; et ses paramètres sont bien plus déterminants sur un système hybride naturel que
sur les lignées croisées des exemples publiés — amplitude de 0,52 sur le seuil de core et 0,65 sur
l'échelle taxonomique. Artefacts : `note_indice_4H.md`, `note_parametres_4H.md`,
`note_sensibilite_4H.md`, `fig_sensibilite_4H.png`.

**Bibliographie constituée.** 3 583 notices balayées sur Semantic Scholar et OpenAlex, criblage
assisté validé sur échantillon (89 % d'accord sur 36 décisions, exclusions comprises), boule de
neige sur les meilleures semences. **225 références** dans un fichier unique avec résumés,
mots-clés thématiques et traçabilité d'origine. Trois constats de cadrage en sont issus :
l'assimilation de « transgressif » à une dysbiose est contestée par un travail récent sur des
hybrides prospères ; un effet d'admixture apparent peut s'évanouir sous contrôle de
l'autocorrélation spatiale ; et le créneau de nouveauté du projet se nomme précisément.
Artefacts : `microbiome_hybrid_all_refs.bib`, `microbiome_hybrid_all_refs_inventaire.csv`,
`synthese_hybrides_microbiote.md`, `criblage_hybrid_microbiome.csv`, `hybrid_microbiome_refs.bib`.

**L'article précurseur de l'équipe a été retrouvé et lu** (Guivier et al. 2017, *Microbial
Ecology*) : même paire d'espèces, mêmes quatre compartiments tissulaires, en parapatrie stricte
sur le Suran avec un effectif réduit. Il se conclut en annonçant l'exploration du microbiote des
hybrides — le présent article est donc la suite annoncée. Conséquence : le quatrième compartiment
tissulaire n'est pas un argument de nouveauté.

## 8. Rédaction

`Article.docx`, `materials_and_methods.docx`, `Supplementary_Data.docx`,
`MS_hybrid and microbiota_draft1.docx`, plus les relectures `AM_introduction_review.docx` et
`AM_submission_readiness.docx`. Le Materials & Methods est à jour sur les stations, les runs et
les modèles statistiques ; quatre sections restent en attente d'informations de protocole
(capture et autorisations, extraction et librairies, contrôles mock, DOI Zenodo).

## 9. Le résultat structurant du bilan

**Aucun axe d'analyse n'est propre pour la question hybride.** Entre stations, la classe
génotypique est confondue avec la station, qui porte l'effet le plus fort mesuré sur la
composition. À station fixée, elle est confondue avec la position dans la plaque — et les trois
stations portant les trois classes sont précisément celles où cet enchevêtrement est maximal
(V de Cramér de 0,52 à 0,62 contre 0,18 à Rosières). Le sous-plan pleinement séparable compte
90 individus sur 180, mais seulement 32 dans une station gardant les trois classes.

**L'axe tissulaire, lui, est propre** : 109 individus ont les quatre tissus exploitables, 160 en
ont au moins trois, le contraste est apparié intra-individu et ne dépend d'aucune décision de
classification. C'est la seule ossature du jeu de données qui ne soit pas contrainte par un
confondant.