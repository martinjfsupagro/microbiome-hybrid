# DECISIONS — journal antichronologique

Index daté. Le raisonnement complet vit dans `docs/decision_*.md` et les messages de commit ;
ce fichier ne recopie pas, il pointe. Les entrées marquées **rétro** ont été reconstituées
depuis les scripts et le `git log` : la décision est certaine, sa date est approchée.

---

## 2026-09-25 — ENA : identité d'hôte alignée sur la classification à 25 chromosomes (titre, nom scientifique, nom commun)
- **Décision** : Aligner sur `categorie` de `analysis_metadata.csv` (septembre, 59 Cn / 42 Hy / 79 Pt) les champs TITLE, `host scientific name` et `host common name` de PRJEB124417. Les 22 quasi-purs sont déposés comme hybrides : le dépôt décrit le génotype, pas une passe d'analyse. Nom commun des hybrides **`nasus x toxostoma`** (décision JF Martin), parentaux `nase` / `toxostome`. Correction par patch du XML déposé, comme le 31/08.
- **Raison** : 63 échantillons (16 individus) portaient l'identité d'août ; la correction du 31/08 n'avait pas touché le titre ni le nom commun, restés morphologiques (531 « Chondrostoma sp. », 33 titres contredisant le nom scientifique).
- **Impact** : 568 échantillons modifiés (1 199 champs), soumis en production le 2026-09-25 à 18:08 : success=true, 568/568 accessions identiques. **Vérification exhaustive en attente.** État final attendu : 236 / 322 / 169 échantillons Cn / Pt / Hy.
- **Session** : Soumission de données. Réf. `ena_deposit/MEMO_correction_hote_sept.md`, `scripts/28-ena_hote_sept.py`, commits `c71a460`, `3e13880`, `01cd77d`.

## 2026-09-25 — Témoin de l'effet de position : sous-ensembles intra-catégorie au lieu des « stations mono-catégorie »
- **Décision** : Contrôler l'effet de colonne de plaque à l'intérieur d'une seule catégorie génotypique (sous-ensembles `intra_Cn`, `intra_Pt` de `18-position_control.sh`). L'ancien témoin est retiré de la Table S6 et du §8.8.
- **Raison** : Les scripts 17 et 18 lisaient le taxon morphologique : le témoin portait sur quatre codes de site ne comptant que des « Ch », c'est-à-dire des poissons non résolus. Génotypés, aucun code de site n'est mono-catégorie, sous aucune classification.
- **Impact** : Table S6, Figure S1 et §8.8 reconstruits en deux passes ; V catégorie × colonne 0,527 (passe 1) / 0,479 (passe 2).
- **Session** : Analyse + Rédaction. Réf. `docs/recalcul/note_recalcul_2passes.md` §1, commits `bb93a53`, `eed4ec3`, `691a155`.

## 2026-09-25 — D7 : métrique de diversité, **NON TRANCHÉE**
- **Décision** : aucune. La métrique portant le résultat principal reste ouverte.
- **Raison** : les analyses existantes reposaient sur la richesse ASV, mais 48 % seulement des
  ASV à 1–3 lectures sont retrouvés au reséquençage ; `docs/recommandations_consolidees.md`
  demande de refaire les résultats en métriques pondérées par l'abondance.
- **Impact** : **tous les R² de catégorie et de station sont en statut « préliminaire »**
  dans `RESULTATS.md` jusqu'à arbitrage. Les quatre matrices (Bray, Jaccard, UniFrac
  non pondéré, UniFrac pondéré) sont calculées et disponibles.
- **Session** : Analyse. Réf. `docs/recommandations_consolidees.md`, `docs/decisions_a_prendre.md`.

## 2026-09-25 — D1 : « hybride » = 42 individus, analyse en deux passes
- **Décision** : passe 1 = 20 hybrides intermédiaires, les 22 quasi-purs **exclus** (n = 158) ;
  passe 2 = les 42 hybrides (n = 180). Les quasi-purs ne sont pas reversés dans leur classe parentale.
- **Raison** : André tient que les 22 quasi-purs (parentaux sur presque tout le génome,
  introgressés sur un chromosome) sont des hybrides. Seuil D = 0,12 (intervalle vide 0,1191–0,1301).
- **Impact** : puissance du contraste Hy vs parentaux ×1,3 ; recalcul complet des analyses de
  catégorie ; la classification d'août (59/30/91) ne correspond à aucune des deux passes.
- **Session** : Analyse. Réf. `docs/synthese_genotypage_25chr.md`, `docs/prompt_conversation_analyse.md`.

## 2026-09-25 — D2 : station et catégorie non dissociées, position sortie du modèle principal
- **Décision** : rapporter les patterns sans chercher à séparer station et catégorie ;
  retirer la colonne de plaque du modèle principal, la **conserver en sensibilité supplémentaire**.
- **Raison** : André considère le lien station–catégorie comme biologiquement causal (température,
  sensibilité du hotu). L'effet de position est mesuré comme réel dans les 24 strates.
- **Impact** : §8.6 et §8.8 du manuscrit à réécrire (la position y est covariable de chaque modèle).
- **Session** : Analyse + Rédaction. Réf. `docs/decision_position_effect.md`.

## 2026-09-25 — D3 à D6 : périmètre et paramètres 4H
- **Décision** : D3 les 180 individus retenus (étude de terrain, pas d'expérimentation) ·
  D4 analyse 4H annoncée en deux passes · D5 ρ = 0,5 au rang **genre**, sensibilité
  ρ ∈ {0,3 ; 0,5 ; 0,7}, ϑ = ε = 0 · D6 les **4 tissus** conservés (caudale incluse malgré
  un plafond de 10 individus en passe 1).
- **Raison** : comparabilité aux 4 systèmes publiés ; le gradient tissulaire est l'axe non confondu.
- **Impact** : plan 4H 28/41/30/36 tissus en passe 2 ; classes annoncées abandonnées sous 10 individus.
- **Session** : Analyse. Réf. `docs/note_parametres_4H.md`, `docs/note_indice_4H.md`, `docs/point_etape_25sept.md`.

## 2026-09-25 — Bibliographie : reconstruction de `microbiome_hybrid_all_refs.bib`
- **Décision** : reconstruire les champs `author` de 218 des 223 notices.
- **Raison** : le séparateur BibTeX ` and ` avait été inséré entre chaque caractère, rendant les
  notices inexploitables par Zotero et BibTeX.
- **Impact** : validé contre Crossref sur 40 DOI tirés au hasard (premier auteur 40/40).
- **Session** : Bibliographie. Réf. commit `17abb8e`.

## 2026-09-25 — Rédaction : introduction intégrée à `Article.docx`
- **Décision** : 5 paragraphes (1 472 mots) insérés avant Materials and Methods ; les 76 paragraphes
  du M&M vérifiés inchangés avant/après.
- **Impact** : une note éditoriale grise liste les 4 points à trancher dans le document.
- **Session** : Rédaction. Réf. commits `de886e0`, `dd0f039`, `f8c0a28`.

## 2026-08-31 — PERMDISP : la prédiction transgressive en dispersion n'est pas soutenue
- **Décision** : rapporter le résultat en l'état, sens inversé compris.
- **Raison** : hybrides **les moins dispersés** dans 31 tests sur 48 (p = 9,4 × 10⁻⁶) ;
  un seul test significatif dans le sens transgressif, aucun en intra-station.
- **Impact** : réserve déclarée — `betadisper` n'accepte pas de covariable, l'effet de position
  n'y est pas ajusté. Le résultat caudal est compositionnel, non une différence de variabilité.
- **Session** : Analyse. Réf. `docs/decision_permdisp.md`, commits `766587a`, `64a786d`.

## 2026-08-31 — Profondeur : sensibilité à 500 restreinte aux métriques pondérées
- **Décision** : affirmations de présence/absence à 3 000 lectures avec biais déclaré ;
  sensibilité à 500 sur les métriques pondérées seules.
- **Raison** : la géométrie bêta pondérée est invariante à la profondeur (UniFrac pondéré
  r = 0,9994 ; Bray r = 0,9985) alors que les métriques de présence décrochent (non pondéré 0,937)
  et la richesse perd 42 %. Aucune profondeur ne corrige le biais de sélection.
- **Session** : Analyse. Réf. `docs/decision_depth_threshold.md`, commits `c985875`, `48d7799`.

## 2026-08-31 — ENA : correction par patch du XML déposé, pas par régénération
- **Décision** : patcher le XML du dépôt accepté (3 472 valeurs, 5 attributs, 727 échantillons).
- **Raison** : préserve octet pour octet tous les attributs absents du fichier de correction.
- **Impact** : vérifié 727/727 alias et accessions `ERS` conformes ; 0 changement hors des
  5 champs cibles. `Supplementary_Data.docx` et `DATA_AVAILABILITY.md` restent à régénérer
  depuis `station_reference.csv`.
- **Session** : Soumission de données. Réf. `ena_deposit/MEMO_correction_ENA.md`, `docs/GUIDE_correction_ENA.md`.

## 2026-08-31 — Manuscrit : retrait du Materials & Methods autonome
- **Décision** : `docs/materials_and_methods.docx` passe en **SUPERSEDED** ; les Methods se
  maintiennent dans `Article.docx` seul. Fichier conservé pour l'historique.
- **Raison** : 62 paragraphes communs, aucun des 7 propres au M&M ne portait d'information absente,
  et il conservait une affirmation fausse sur les index i7.
- **Session** : Rédaction. Réf. `docs/decision_manuscrit.md`, commit `46a7f34`.

## 2026-08-30 — Stations : `station_reference.csv` d'André fait foi
- **Décision** : le Suran porte deux stations (Pont-d'Ain / Chavannes, 25,4 km haversine) ;
  coordonnées et dates de pêche reprises du fichier d'André ; 181 → **180 individus**.
- **Raison** : les coordonnées déposées à l'ENA étaient des extrapolations sur noms de communes
  (6 sites sur 9 à plus de 5 km, 5 rivières fausses).
- **Impact** : Table S1 réécrite par station ; correction ENA déclenchée ; les deux stations du
  Suran forment un **contrôle négatif interne** (parapatrie).
- **Session** : Analyse + Soumission. Réf. `docs/decision_stations.md`, commits `f35bbcc`, `b63ca65`.

## 2026-08-25 — Plan de réplication : deux préparations de librairies, trois séquençages nichés
- **Décision** : ne pas modéliser `run` comme facteur à trois niveaux interchangeables.
- **Raison** : quatre faisceaux convergents ; l'index i7 diffère pour 384 des 768 librairies et
  l'i5 pour 576 entre `durance1` et la préparation n°2, or un pool indexé en une étape ne peut
  être réindexé.
- **Impact** : technique et biologique sont **croisés, non confondus** — aucune correction
  de batch de type méta-analyse n'est nécessaire (et aucune n'a été appliquée).
- **Session** : Analyse. Réf. `docs/decision_run_design.md`.

## 2026-08-23 — Raréfaction en tirages répétés, N = 400
- **Décision** : moyenne sur 400 tirages (2 chaînes × 200) à 3 000 lectures.
- **Raison** : erreur de Monte-Carlo mesurée < 0,2 % entre deux chaînes indépendantes.
- **Impact** : les matrices `beta_mean_*_N400.rds` sont l'entrée de **toutes** les analyses
  de catégorie ; les recalculer serait une décision à consigner.
- **Session** : Analyse. Réf. `docs/decision_rarefaction_mode.md`.

## 2026-08-22 — Table de travail : retrait des mocks et des puits vides
- **Décision** : `results/decontam/asv_table_clean.tsv` devient la table de travail
  (2 180 échantillons × 44 200 ASV). Deux échantillons (`15Cab1021Ch01A`, `15Cab1022Ch01A`)
  requalifiés en mocks, portant le total à 4 mocks.
- **Impact** : les autres tables de `results/decontam/` et les deux copies à la racine sont
  des **doublons archivables** (~0,97 Go).
- **Session** : Analyse. Réf. `docs/decision_mock_samples.md`, `docs/decision_mock_removal.md`.

## 2026-07-27 — Décontamination : seuil decontam p = 0,1
- **Décision** : retenir la sortie `p01` comme table d'analyse `[À CONFIRMER]` — inféré de
  l'identité de taille entre `asv_table_analysis.tsv` et `asv_table_decontam_p01.tsv`.
- **Raison / impact** : 66 ASV contaminants retirés, 99,76 % des lectures conservées.
- **Session** : Analyse. Réf. `docs/decision_decontam.md`.

## 2026-07-27 — Raréfaction à 3 000 lectures
- **Décision** : seuil de profondeur 3 000.
- **Raison** : 81,8 % des échantillons conservés ; suffisant pour l'indice 4H (testé 1 000–10 000).
- **Impact** : biais de sélection déclaré (caudale +30 points à 3 000, +2,5 à 500).
- **Session** : Analyse. Réf. `docs/decision_rarefaction.md`.

## 2026-07-25 — Pipeline DADA2 : par run, `truncLen = c(230, 190)`, SILVA v138.2
- **Décision** : apprentissage des erreurs par run, chimères sur la table fusionnée,
  taxonomie SILVA v138.2.
- **Raison** : profils qualité quasi identiques sur les trois runs ; insert V4 ~253 pb,
  lectures 2×251 → recouvrement ~167 pb.
- **Impact** : 44 349 ASV × 2 295 échantillons ; appariement 92,7–94,3 %.
- **Session** : Analyse. Réf. `scripts/04-dada2_worker.sh`, `scripts/05-merge_taxonomy.sh`.

## 2026-07-25 — `consolidated_dataset/` comme source fastq unique et réversible
- **Décision** : centraliser les R1/R2 des trois runs, un sous-dossier par run.
- **Raison** : durance1 et durance3 portent des noms de fichiers identiques ; DADA2 apprend
  les erreurs par run.
- **Impact** : réversible via `metadata/consolidate_manifest.csv`
  (`consolidate_fastq.py --revert`). Les index I1/I2 et `Undetermined` restent dans `data/`.
- **Session** : Analyse.

## rétro (2026-07) — Retrait du 12S co-amplifié
- **Décision** : retrait par la longueur (script `02`) puis filet taxonomique (1 144 ASV Mitochondria).
- **Raison** : les amorces 16S co-amplifient le 12S mitochondrial de l'hôte, 14–67 % des lectures.
- **Session** : Analyse. Réf. en-tête de `scripts/02-remove_12S_worker.sh`.

## rétro (2026-07-19) — `Ch` = chondrostome non identifié, **pas** le chevesne
- **Décision** : `Ch` désigne un *Chondrostoma* non tranché entre `Cn` et `Pt`.
- **Raison** : le commit `8a09794` « docs: Ch = chevesne » est **faux** ; le chevesne
  (*Squalius cephalus*, code `Sc`) est absent de ces trois runs.
- **Impact** : à ne pas redécouvrir. Réf. `CLAUDE.md`.
