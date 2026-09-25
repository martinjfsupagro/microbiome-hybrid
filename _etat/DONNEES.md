# DONNEES — manifeste des jeux de données

Chemins relatifs à `/home/martinj/work/projects/microbiome-hybrid`.
md5 calculés le **2026-09-25** pour les fichiers canoniques ; les doublons et les répertoires
de fastq portent leur taille seule (décision du 2026-09-25).
`résultats/` n'est pas versionné : ces fichiers ne sont récupérables que par réexécution
du script indiqué.

## Données brutes

| id | chemin | description | provenance | version / date | md5 | taille | statut | utilisé par |
|---|---|---|---|---|---|---|---|---|
| `RAW-D1` | `consolidated_dataset/durance1` | 1 536 fastq.gz R1/R2, préparation PCR n°1 | plateforme MiSeq, run `170710_M03930_0062` (BBHKV) | 2017-07-12 | — | 4,06 Go | **brut validé** | `scripts/01`,`02`,`04` ; ENA PRJEB124417 |
| `RAW-D2` | `consolidated_dataset/durance2` | 1 536 fastq.gz, préparation n°2, flow cell BCFFD | livré démultiplexé non compressé, compressé en place | 2026-07-25 | — | 3,39 Go | **brut validé** | idem |
| `RAW-D3` | `consolidated_dataset/durance3` | 1 536 fastq.gz, préparation n°2, run `171103_M03930_0072` (BFWT5) | plateforme MiSeq | 2017-11-05 | — | 4,94 Go | **brut validé** | idem |
| `RAW-DIR` | `data/durance{1,3}` | livraisons d'origine : SampleSheets, I1/I2, `Undetermined`, InterOp | plateforme | 2026-07-25 | — | 13,1 Go (3 412 f.) | brut, archive | `build_metadata.py` |
| `MOCK-REF` | `refs/zymo_mock` | mock de référence (26 fichiers) | Zymo | 2026-07-26 | — | 111 Mo | brut de référence | `scripts/06-validate_mock.sh` |

## Tables ASV et arbre

| id | chemin | description | version / date | md5 | taille | statut | utilisé par |
|---|---|---|---|---|---|---|---|
| `ASV-RAW` | `results/dada2_final/asv_table.tsv` | table DADA2 avant filtrage hors-cible | 2026-07-25 | `c427b230e1e3ac2e5ee8400a4c39781e` | 213,3 Mo | filtré (intermédiaire) | `scripts/05` |
| `ASV-FILT` | `results/dada2_final/asv_table_filtered.tsv` | 44 349 ASV × 2 295 échantillons, hors-cible retiré | 2026-07-25 | `63f828d0c17b4f07a39475ccbd4058ff` | 204,2 Mo | filtré | `scripts/07`,`11`,`12` |
| `TAX` | `results/dada2_final/taxonomy.tsv` | assignation SILVA v138.2 | 2026-07-25 | `7b712455ffe7910e833407cf92060f86` | 4,0 Mo | validé | toutes analyses taxonomiques |
| `SEQS` | `results/dada2_final/asv.fasta` | séquences des ASV | 2026-07-25 | `e8290e062c9b0f020b75fe26b2b8ab57` | 12,1 Mo | validé | `scripts/08-phylogeny.sh`, mock BLAST |
| `SEQTAB` | `results/dada2_final/seqtab_nochim_filtered.rds` | objet DADA2 filtré | 2026-07-25 | `610260aef53ce27d284080b597a57c00` | 3,4 Mo | validé | R |
| `TRACK` | `results/dada2_final/track_all.csv` | suivi des lectures par étape | 2026-07-25 | `100a86111ef55d6cb484139a45dc0d0f` | 137,8 ko | validé | `docs/rapport_analyse_16S.md` |
| **`ASV-CLEAN`** | `results/decontam/asv_table_clean.tsv` | **table de travail validée** : 2 180 × 44 200, mocks et puits vides retirés | 2026-08-22 | `85f344572e669cf9338b0b00b5e8a8d0` | 193,4 Mo | **validé** | `scripts/13`→`27`, toutes les analyses écologiques |
| `DECONT-SC` | `results/decontam/decontam_scores.tsv` | scores decontam par ASV | 2026-07-27 | `224f72f1f95d05818ce35adc14d687e6` | 1,3 Mo | validé | `docs/decision_decontam.md` |
| `TREE` | `results/phylogeny/rooted_tree.qza` (+ `tree.nwk` à la racine) | arbre raciné, 44 256 feuilles | 2026-07-27 | `1e500f9e80b9e359098d158d9309a86e` / `a12089a8b6dc669aaf68e30a315ee38b` | 0,6 Mo / 1,6 Mo | validé | `scripts/21-unifrac_faith.sh` |

**Doublons archivables (~0,97 Go, aucune analyse ne les lit)** — statut confirmé le 2026-09-25 :
`results/decontam/asv_table_analysis.tsv`, `asv_table_decontam_p01.tsv`, `asv_table_decontam_p05.tsv`,
et les deux copies à la racine `asv_table_decontam_p01.tsv`, `asv_table_decontam_p05.tsv`.
`analysis` et `p01` ont une taille identique au bit près (194 163 588 o) : `p01` est bien la sortie
retenue `[À CONFIRMER]`.

## Matrices de distance et diversité

| id | chemin | description | date | md5 | taille | statut | utilisé par |
|---|---|---|---|---|---|---|---|
| `BETA-BRAY` | `results/rarefaction/beta_mean_bray_N400.rds` | Bray-Curtis moyen, 400 tirages à 3 000 lectures | 2026-08-23 | `6b7501d1b031b7ef43c3decb6b7844ff` | 9,5 Mo | validé | `scripts/20`,`23`,`24` |
| `BETA-JAC` | `results/rarefaction/beta_mean_jaccard_N400.rds` | Jaccard moyen | 2026-08-23 | `aadf68c76d8392f1d4e321288cb94c31` | 11,4 Mo | validé | idem |
| `BETA-UUF` | `results/rarefaction/beta_mean_unifrac_unweighted_N400.rds` | UniFrac non pondéré | 2026-08-30 | `19d29bc76bd5fdc2433d5e787ad62680` | 9,7 Mo | validé | idem |
| `BETA-WUF` | `results/rarefaction/beta_mean_unifrac_weighted_N400.rds` | UniFrac pondéré | 2026-08-30 | `8ed89c59fefab9e9d6067ab1074442e5` | 9,1 Mo | validé | idem |
| `BETA-WUF-500` | `results/rarefaction_d500/beta_mean_unifrac_weighted_N400.rds` | sensibilité à 500 lectures | 2026-08-31 | `5c36bac3737ab35fe27aee9d42c3634f` | 12,3 Mo | validé | `scripts/20`,`22` (mode d500) |
| `PHYLO-W` | `results/phylo_diversity/unifrac_weighted_mean.tsv.gz` | UniFrac pondéré, format long | 2026-08-30 | `132731533fa90e63af057495b3eb2ffe` | 9,5 Mo | validé | `scripts/21b-unifrac_to_rds.R` |
| `PHYLO-U` | `results/phylo_diversity/unifrac_unweighted_mean.tsv.gz` | UniFrac non pondéré, format long | 2026-08-30 | `76c45ec7660b8bf7e62cd55b70a4fbca` | 10,4 Mo | validé | idem |
| `ALPHA` | `results/phylo_diversity/alpha_phylo_mean.tsv` (+ `_d500`) | Faith PD, richness, shannon, invsimpson | 2026-08-30 | — | 114 ko | validé | analyses alpha |

## Métadonnées et génotypage

| id | chemin | description | provenance | date | md5 | taille | statut | utilisé par |
|---|---|---|---|---|---|---|---|---|
| `META-SAMP` | `metadata/samples_all.csv` | 2 304 lignes : plan, `dada2_id`, taille/poids/sexe, drapeaux de correction | `build_metadata.py` + `merge_metadata.py` | 2026-07-25 | `5c44d9dd92d634ff16edc61cab8b3aa9` | 881,5 ko | validé | tout le pipeline |
| `META-ANA` | `metadata/analysis_metadata.csv` | 2 181 lignes, métadonnées unifiées, tous confondants. `categorie` = **septembre, 25 chr (59/42/79)**, `categorie_aout_12chr` (59/30/91), `type_genome`, `inclus_passe1` (158) — vérifié le 2026-09-25 sur les 180 individus, md5 inchangé (la mention « encore en classification d'août » était fausse) | `scripts/19-analysis_metadata.py` | 2026-09-25 | `14d75b54629b11dada0d275e792a0185` | 418,6 ko | **validé** | `scripts/17`,`18`,`20`,`24`,`26`,`27`,`28` |
| `GENO-SEPT` | `metadata/genotypes_verifies_sept_180.csv` | **génotypage de référence** : 25 chromosomes, 59 Cn / 42 Hy / 79 Pt, seuil D = 0,12 | André, vérifié contre les Q-values | 2026-09-25 | `aab2f05c9ac0433bc8210739697e5298` | 20,1 ko | **validé** | `scripts/26`,`27` ; `results/recat/{1,2}` |
| `GENO-AOUT` | `metadata/genotypes_andre_aout2026.csv` | génotypage à 12 chromosomes, 59/30/91 — **périmé**, conservé pour comparaison | André | 2026-08-30 | `b0b9f53c0899fdf979758a5004d75207` | 28,7 ko | périmé | `results/recat/aout` |
| `GENO-SRC` | `metadata/source/nouveau_tableau_AG_Sept_2026.xlsx`, `genome_hotox.csv`, `genome_hybride.Rmd`/`.html` | sources brutes du génotypage (Q-scores par chromosome) | André | 2026-09-25 | `0cbb12ffb7420398ff618513a2126990` / `c38214e43958e933aae0742855019ba1` | 29,1 / 35,4 ko | brut fourni | `docs/synthese_genotypage_25chr.md` |
| `IDX-HYB` | `metadata/index_hybride_andre.csv` | index hybride continu par individu (0 = hotu → 1 = toxostome) | André | 2026-08-30 | `1f06cb108a36c93d6c9141ca3e25914b` | 30,3 ko | fourni, **non intégré** | indice 4H (à venir) |
| `STATIONS` | `metadata/station_reference.csv` | 9 stations, coordonnées WGS84 et dates de pêche — **fait foi** | André via JF Martin | 2026-08-30 | `0c46a39521db7af53911179ab367dc70` | 1,1 ko | validé | `scripts/16`,`19` ; Table S1 ; corrections ENA |
| `CORR-IND` | `metadata/individual_corrections.csv` | corrections d'identifiants individuels (dont `15Per2015Ch03A`) | projet | 2026-08-30 | `fa0e042b8bc3091b4c8945852eb5d023` | 239 o | validé | `scripts/19` |
| `NOQ` | `metadata/individus_sans_qvalues.csv` | 5 individus sans foie : médiane et D d'origine inconnue | projet | 2026-09-25 | — | 548 o | **à trancher** | question ouverte André n°1 |

## Résultats dérivés récents

| id | chemin | description | date | statut | utilisé par |
|---|---|---|---|---|---|
| `RECAT` | `results/recat/{morpho,aout,1,2}` + `temoin_effectif` | recalcul complet position / partition / PERMDISP sur 4 jeux de catégories ; `status.tsv` md5 `a06da421ac21b99c71a94c20439e07fb` : 17 étapes, code 0 | 2026-09-25 | **validé** (reproduit août au bit près), interprété | §8.8–8.9, Tables S6–S9, Figures S1, S3 |
| `RECAT-DOC` | `docs/recalcul/` : `note_recalcul_2passes.md` (`d04c19fdfc6865268a3bc450c33c6406`), `correspondance_ancien_nouveau.csv` (`a5949eb6e04cd9d5e10dd0b67efb7e20`), `d2_avec_vs_sans_position.csv` (`901275812ef8965fdaf257f53fe56b34`), `temoin_effectif_attribution.csv` (`d1fb334b6468510b36aa9f1ac0d2b763`), `faisabilite_permutations.csv` (`f028bf34dd081422724712ee62bce104`), `recat_elements_structurels.csv` (`562c4954b45d12f382126a5c449308df`) | interprétation de `RECAT`, correspondance valeur par valeur août → passes | 2026-09-25 | validé | manuscrit, `RESULTATS.md` R21–R25 |
| `FIG-S` | `docs/manuscrit/figures/fig_S1_position_effect.png` (`3cf5d2893f33a035b475b8051af89696`), `fig_S3_permdisp.png` (`2f6126c577ae9157780f8277188564a8`) | Figures S1 et S3 régénérées en deux passes | 2026-09-25 | dans le manuscrit | `Supplementary_Data.docx` |
| `VARPART` | `results/var_partition{,_cat,_cat_d500}` | partition technique/biologique et par catégorie (août) | 2026-08-23/30 | validé, **superseded par `RECAT`** | §8.9 (à réécrire) |
| `POS` | `results/position_effect`, `permdisp`, `depth_agreement`, `qc_depth`, `crosstalk`, `mock_validation` | témoins et QC | 2026-07→08 | validé | §8.6–8.8, Supplementary |

## Dépôt de séquences et manuscrit

| id | chemin | description | date | md5 | statut |
|---|---|---|---|---|---|
| `ENA-SAMP` | `ena_deposit/ena_samples.tsv` | 768 échantillons déposés | 2026-08-22 | `3336415ce31235bd9d9a4d35bf8cf34e` | **soumis** (PRJEB124417) |
| `ENA-RUNS` | `ena_deposit/ena_experiments_runs.tsv` | 2 304 experiments/runs | 2026-08-22 | `40768205c873545d1d04b3d73d29d12a` | **soumis** |
| `ENA-ACC` | `docs/manuscrit/ENA_accessions_durance.tsv` | accessions ERS/ERX/ERR consolidées | 2026-08-25 | `85d71bc6615e1945128599bf75df3ae8` | validé |
| `MS` | `docs/manuscrit/Article.docx` | manuscrit : introduction (25/09), §1, 8.6, 8.8, 8.9 sur 25 chr / deux passes / D2, styles de titres corrigés | 2026-09-25 | `b82994af0fbb052f31aee287e6c03acc` | en rédaction |
| `MS-SUP` | `docs/manuscrit/Supplementary_Data.docx` | Tables S1–S9, Figures S1–S3 ; Table S1 par station depuis `STATIONS` (31/08), S6–S9 et Figures S1, S3 en deux passes (25/09) | 2026-09-25 | `2f7eb75cf7ed837cd8698796964c61f5` | en rédaction ; note grise ENA sous *Host identity* à retirer après R26 |
| `BIB` | `docs/biblio/microbiome_hybrid_all_refs.bib` | 223 notices, champs `author` reconstruits le 25/09 | 2026-09-25 | `0726d69ee154fec716f30def96197915` | **validé** |
| `ENA-HOTE` | `ena_deposit/ena_corrections_hote_sept.tsv` (`18e2ec93f8a1c406e3dcb461e404e693`), `ena_update_sept/sample.xml` (`9feb467c8d01326e666577f8ff7b200e`), `ena_etat_final_hote_sept.tsv` (`ceb3a6b26d86b0e9d196ce9fb09e4e44`), reçu `receipt_hote_sept_prod_20260925_180826.xml` (`a2cb65cdf8bec19c685368eebb312dc2`) | correction de l'identité d'hôte : 568 échantillons, 1 199 champs | 2026-09-25 | voir colonne chemin | **soumis** (18:08), vérification en attente |
