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
| `GENO-TAB` | `docs/manuscrit/table_genotypes_individuels.csv` | table de génotypage par individu publiée en **Table S2** : 180 lignes, 17 colonnes, arbitrage JF du 30/09 appliqué (deux ajustements hors foie publiés, deux individus à NA) | `GENO-SEPT` + réponses d'André du 30/09 | 2026-09-30 | `699617724f814494e5003d866c542d75` | 17,3 ko | **dans le manuscrit** (Table S2) | `MS-SUP` |
| `CORR-IND` | `metadata/individual_corrections.csv` | corrections d'identifiants individuels (dont `15Per2015Ch03A`) | projet | 2026-08-30 | `fa0e042b8bc3091b4c8945852eb5d023` | 239 o | validé | `scripts/19` |
| `NOQ` | `metadata/individus_sans_qvalues.csv` | 5 individus sans foie : médiane et D d'origine inconnue | projet | 2026-09-25 | — | 548 o | **à trancher** | question ouverte André n°1 |

## Résultats dérivés récents

| id | chemin | description | date | statut | utilisé par |
|---|---|---|---|---|---|
| `RECAT` | `results/recat/{morpho,aout,1,2}` + `temoin_effectif` | recalcul complet position / partition / PERMDISP sur 4 jeux de catégories ; `status.tsv` md5 `a06da421ac21b99c71a94c20439e07fb` : 17 étapes, code 0 | 2026-09-25 | **validé** (reproduit août au bit près), interprété | §8.8–8.9, Tables S7–S10 (numérotation du 03/10), Figures S1, S3 |
| `RECAT-DOC` | `docs/recalcul/` : `note_recalcul_2passes.md` (`d04c19fdfc6865268a3bc450c33c6406`), `correspondance_ancien_nouveau.csv` (`a5949eb6e04cd9d5e10dd0b67efb7e20`), `d2_avec_vs_sans_position.csv` (`901275812ef8965fdaf257f53fe56b34`), `temoin_effectif_attribution.csv` (`d1fb334b6468510b36aa9f1ac0d2b763`), `faisabilite_permutations.csv` (`f028bf34dd081422724712ee62bce104`), `recat_elements_structurels.csv` (`562c4954b45d12f382126a5c449308df`) | interprétation de `RECAT`, correspondance valeur par valeur août → passes | 2026-09-25 | validé | manuscrit, `RESULTATS.md` R21–R25 |
| `FIG-S` | `docs/manuscrit/figures/fig_S1_position_effect.png` (`3cf5d2893f33a035b475b8051af89696`), `fig_S3_permdisp.png` (`2f6126c577ae9157780f8277188564a8`) | Figures S1 et S3 régénérées en deux passes | 2026-09-25 | dans le manuscrit | `Supplementary_Data.docx` |
| `VARPART` | `results/var_partition{,_cat,_cat_d500}` | partition technique/biologique et par catégorie (août) | 2026-08-23/30 | validé, **superseded par `RECAT`** | §8.9 (à réécrire) |
| `POS` | `results/position_effect`, `permdisp`, `depth_agreement`, `qc_depth`, `crosstalk`, `mock_validation` | témoins et QC | 2026-07→08 | validé | §8.6–8.8, Supplementary |
| `TESTS-1003` | `results/tests_20261003/` | cinq tests déclarés a priori le 03/10 : `sejour_vivier/sejour_tests.tsv` (`84f3599f60a454952591728f2906be7a`), `sejour_vivier/spearman_rang_pos.tsv` (`bd8ee6b9bc340fe94001a258e26fb697`), `dilution/b2_direct.tsv` (`a3478d21fe39315e5d801a0616a258ff`), `dilution/b1_injection.tsv` (`57937cdcadea89a108598a8f409c4d2a`), `dilution/b1_tirages.tsv` (`4097fb1b879dd9e61e79bbe948fd0a22`), `ensemble_d500/ensemble.tsv` (`0747ef76f35d00eec44191b8edb15662`), `temoin_effectif_d500/witness.tsv` (`16e5389b7f997f99286898d1b25e0475`), `alpha_categorie/alpha_categorie.tsv` (`fa293ec4f528f232af2047da5a5d1f92`), `alpha_partition/alpha_partition.tsv` (`d500516de1611daac2c141e04a099803`), `lecture_tests.json` (`2b45f56b0185ac38b0df34027cca8e64`) | 2026-10-03 | **validé** (7 étapes code 0, `HEAD` `8e4375d`) | R8, R29–R32 |
| `TESTS-DOC` | `docs/plan_tests_2026-10-03.md` (`26348c325bfc977cce2a876dd01aa120`, déclaration a priori), `docs/recalcul/note_tests_2026-10-03.md` (`dc4e5bf581f0dc7c12d1a38c498467c7`) | plan déclaré avant calcul et interprétation de `TESTS-1003` | 2026-10-03 | validé | `RESULTATS.md` R8, R29–R32 |

## Dépôt de séquences et manuscrit

| id | chemin | description | date | md5 | statut |
|---|---|---|---|---|---|
| `ENA-SAMP` | `ena_deposit/ena_samples.tsv` | 768 échantillons déposés | 2026-08-22 | `3336415ce31235bd9d9a4d35bf8cf34e` | **soumis** (PRJEB124417) |
| `ENA-RUNS` | `ena_deposit/ena_experiments_runs.tsv` | 2 304 experiments/runs | 2026-08-22 | `40768205c873545d1d04b3d73d29d12a` | **soumis** |
| `ENA-ACC` | `docs/manuscrit/ENA_accessions_durance.tsv` | accessions ERS/ERX/ERR consolidées | 2026-08-25 | `85d71bc6615e1945128599bf75df3ae8` | validé |
| `MS` | `docs/manuscrit/Article.docx` | manuscrit : titre provisoire, introduction, §1–§4 complétés par les réponses d'André du 03/10 (séjour en vivier, dissection, deux tubes), Funding (contrat EDF-CNRS AGDI 428481), lien GitHub au §9, renvois aux Tables S3–S10 ; règle D7 restaurée au §8.6, §8.8–8.9 alignés sur R29 et R32 | 2026-10-03 | `d6f368d30229afc1837d32ea26334507` | en rédaction |
| `MS-SUP` | `docs/manuscrit/Supplementary_Data.docx` | Tables S1–S10, Figures S1–S3 ; **Table S2 = génotypes individuels** (`GENO-TAB`, insérée le 03/10, section paysage), anciennes S2–S9 renumérotées S3–S10 ; Table S1 par station depuis `STATIONS` ; note *Host identity* corrigée (25 chromosomes, non microsatellites) | 2026-10-03 | `6518cd5a7dcf344944c290bda4f260b0` | en rédaction |
| `BIB` | `docs/biblio/microbiome_hybrid_all_refs.bib` | 223 notices, champs `author` reconstruits le 25/09 | 2026-09-25 | `0726d69ee154fec716f30def96197915` | **validé** |
| `ENA-HOTE` | `ena_deposit/ena_corrections_hote_sept.tsv` (`18e2ec93f8a1c406e3dcb461e404e693`), `ena_update_sept/sample.xml` (`9feb467c8d01326e666577f8ff7b200e`), `ena_etat_final_hote_sept.tsv` (`ceb3a6b26d86b0e9d196ce9fb09e4e44`), reçu `receipt_hote_sept_prod_20260925_180826.xml` (`a2cb65cdf8bec19c685368eebb312dc2`), rapport de vérification `verification_hote_sept_20260925_1838.txt` (`2d77d08daa440915d73bf835098e188b`) | correction de l'identité d'hôte : 568 échantillons, 1 199 champs | 2026-09-25 | voir colonne chemin | **soumis** (18:08) et **vérifié** (18:38 : 727 échantillons, 1 199 champs conformes, 0 écart) |
| `ENA-CORR` | `ena_deposit/ena_corrections.tsv` | table de correction du 31/08 : 3 472 lignes sur 5 attributs (coordonnées, localité, date, nom scientifique) pour 727 échantillons biologiques | session Soumission, d'après `STATIONS` et le génotypage d'août | 2026-08-31 | `98a2b065de322ee6059877ce6eec51dc` | 641 ko | **soumis** (31/08, vérifié) | R20, R28 |
| `ENA-VERIF` | `ena_deposit/verification_cumulee_20260930_2019.txt` | rapport de vérification cumulée : 727 échantillons, 4 612 champs, 0 écart — produit par `7_verifier_exhaustif.sh` (`95e5614c83206b989620e3e6f755b682`) | session Soumission | 2026-09-30 | `37661deec331a4c12a6d75585743901a` | 294 o | validé | R28 |
| `ENA-SUBJ` | `ena_deposit/ena_corrections_subject_id.tsv` | `host subject id` préfixé par la campagne — 727 lignes, 156 identifiants déposés → 180 sujets ; corrigée le 30/09 (la coquille `15Per2015Ch03A` scindait un poisson en deux, cf. `CORR-IND`) | session Soumission | 2026-09-30 | `95b065369063d05ee979f95c3f18443f` | 245 ko | **prête, non soumise** (décision JF) | MODIFY à venir |
| `ENA-PERT` | `ena_deposit/ena_corrections_pertuis_dates.tsv` | dates de Pertuis au jour près — 44 échantillons, séries 1011-1014 au 07/07/2014 et 2011-2015 au 20/08/2014 (réponse d'André du 30/09) | André via JF Martin | 2026-09-30 | `acacf5b8ff4cd0910858c1294d1ac0b4` | 11 ko | **prête, non soumise** | MODIFY à venir |
