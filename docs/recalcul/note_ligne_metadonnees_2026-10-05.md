# La ligne en trop de `analysis_metadata.csv` : `15Bue1014Ch03A__durance3` (2026-10-05)

Écart signalé par `scripts/30-verif_article.py` (contrôle « analysis_metadata ne décrit que la table d'analyse ») :
`metadata/analysis_metadata.csv` a 2 181 lignes, `results/decontam/asv_table_clean.tsv` 2 180 échantillons.

## Ce qu'est l'échantillon
Hindgut (tissu 03) de l'individu `2015_Bue_1014` (Confluence Buech-Meouge, 2015 ; *P. toxostoma* au génotypage,
noté « Ch » sur morphologie), plaque 6, puits C12, réplicat **durance3** (préparation de librairie B, second run).

## Trace, de la donnée brute à la table (job meso 4306017a)
| étape | durance1 | durance2 | durance3 |
|---|---|---|---|
| paires de lectures brutes (`consolidated_dataset/<run>/…R1…`) | 10 883 | 21 | **13** |
| après retrait 12S (`logs/rm12S_durance3_8736610.out`) | — | — | 12 V4, 1 12S/dimère |
| `track_all.csv` : input → nonchim | 1 893 → 1 726 | 19 → 1 | **absent** |
| `asv_table.tsv` (2 295 colonnes) | présent | présent | **absent** |
| `asv_table_clean.tsv` (2 180), somme des lectures | 908 | 0 | **absent** |

`logs/dada2_durance3_8736613.err`, ligne 1 : « The filter removed all reads: …/15Bue1014Ch03A_R1_filt.fastq.gz and …R2_filt.fastq.gz not written. »
`filterAndTrim` a éliminé les 12 paires restantes ; DADA2 n'a pas produit de colonne pour cet échantillon.
C'est **l'échantillon biologique « vide après filtrage, présent dans les deux autres runs »** du §6 de l'article
(neuf échantillons vides : huit témoins et celui-ci).

## Pourquoi il reste dans les métadonnées
`scripts/19-analysis_metadata.py` construit les lignes depuis l'inventaire `metadata/samples_all.csv`
(2 187 échantillons biologiques = 729 × 3 runs), en écartant les non-biologiques et les 6 puits requalifiés
en mock (`mock_confirme`, 2 échantillons × 3 runs) : 2 187 − 6 = **2 181**. Il ne filtre pas sur la présence
dans la table ASV. Son contrôle de couverture ne va que dans un sens (« chaque échantillon de la table propre
a une ligne de métadonnées », lignes 261-269) ; l'inverse n'est pas exigé. Table propre par run :
727 (durance1), 727 (durance2), **726** (durance3).

Ce n'est donc ni un doublon ni une erreur de jointure : les deux fichiers n'ont pas la même définition
(métadonnées = échantillons biologiques séquencés et génotypés ; table = échantillons ayant produit au moins
une lecture après DADA2). C'est l'attente du script 30 (égalité stricte) qui ne correspond pas à la
construction du script 19.

## Effet sur les résultats : aucun, avec ce témoin
- Les scripts consommateurs (17, 18, 20, 24, 27, 29, 31-35, 37) partent des étiquettes des matrices ou des
  tables alpha et vont chercher les métadonnées (`lab %in% MD$dada2_id`, `MD[ids, ]`, `merge(..., how="inner")`,
  `intersect(...)`) ; aucun n'itère sur les lignes de métadonnées pour constituer un échantillon.
- L'échantillon n'a aucune lecture et ne peut entrer dans aucune matrice raréfiée (seuils 3 000, 1 000 pour le
  4H, 500 en sensibilité).
- Les grandeurs calculées directement sur les métadonnées le sont par individu (V de Cramér) ou sur durance1
  seul (ρ de Spearman, script 40) ; l'individu `2015_Bue_1014` y figure par ses autres lignes.

## Observation annexe
Le réplicat durance2 du même tissu est présent dans la table propre mais avec 0 lecture (1 lecture après
chimères dans `track_all.csv`, retirée ensuite) : la table d'analyse contient donc une colonne vide.
Sans effet (jamais raréfiée).

## Proposition (non appliquée)
Remplacer l'attente du script 30 par : métadonnées ⊇ table, et différence = échantillons dont
`filterAndTrim` a retiré toutes les lectures (ici exactement `15Bue1014Ch03A__durance3`). Le contrôle
échouerait alors pour tout autre écart.
