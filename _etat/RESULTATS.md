# RESULTATS

Règle : une entrée n'est admise que si elle pointe vers **un script** et vers **des données
référencées dans `DONNEES.md`**. Statuts : `préliminaire` / `validé` / `dans le manuscrit`.

> **D7 est tranchée** (2026-09-30, cf. `DECISIONS.md` et `docs/decision_D7_metrique.md`).
> Règle retenue : les quatre métriques sont rapportées partout ; **un résultat n'est énoncé
> comme établi que s'il est soutenu par au moins une métrique pondérée par l'abondance ET
> une métrique de présence**, sinon il est rapporté comme dépendant de la métrique, en
> nommant laquelle. Chiffres du texte courant : Shannon en alpha, Bray-Curtis en composition.
> Un résultat calculé sur la seule richesse ASV observée reste **préliminaire** tant qu'il
> n'a pas été refait.

---

## Pipeline et qualité des données

**R1 — La table finale compte 44 349 ASV × 2 295 échantillons, ramenés à 2 180 × 44 200 après retrait des contrôles.**
Script `scripts/05-merge_taxonomy.sh` puis `12-clean_table.py` · Entrées `RAW-D1/2/3` → `ASV-FILT` → `ASV-CLEAN` · **validé**, dans le manuscrit (§8.5)

**R2 — Le 12S mitochondrial de l'hôte représentait 14 à 67 % des lectures ; 1 144 ASV Mitochondria retirés.**
Script `scripts/02-remove_12S_worker.sh` · Entrées `RAW-D1/2/3` · **validé**, dans le manuscrit
*Correction 2026-10-05* : « 14 à 67 % » (ici) et « 15–67 % » (article, §5) n'étaient reproduits par aucun calcul. Recalcul (`scripts/45-resume_12S.py` → `PART-12S`) : lectures écartées comme 12S ou dimères = 14,1–15,1 % par run ; par échantillon biologique, médiane 12,2 %, étendue 0–99,4 %. Article corrigé (§5, Note S2).

**R3 — Le mock restitue 8/8 espèces attendues à 100 % ; fuite inter-puits (crosstalk) de 0,0002 %.**
Scripts `06-validate_mock.sh`, `10-crosstalk.sh` · Entrées `ASV-FILT`, `MOCK-REF` · **validé**, dans le manuscrit

**R4 — La décontamination retire 66 ASV et conserve 99,76 % des lectures.**
Script `07-decontam.sh` · Entrées `ASV-FILT`, `DECONT-SC` · **validé**, dans le manuscrit

**R5 — La raréfaction à 3 000 lectures conserve 81,8 % des échantillons.**
Script `09-qc_depth.sh` · Entrées `ASV-CLEAN` · **validé**, dans le manuscrit

**R6 — La moyenne sur 400 tirages est convergée : erreur de Monte-Carlo < 0,2 % entre deux chaînes indépendantes.**
Script `15-rarefaction_converge.sh` · Entrées `ASV-CLEAN` → `BETA-*` · **validé**, dans le manuscrit (§8.6)

**R7 — La structure de réplication est nichée : Bray-Curtis intra-librairie 0,118 vs inter-librairie 0,248 ; l'index i7 diffère pour 384 des 768 librairies et l'i5 pour 576 entre les deux préparations.**
Script `13-run_design.sh` · Entrées `META-SAMP`, `ASV-CLEAN` · **validé**, dans le manuscrit (Results « Technical variation », ex-§8.7)

**R8 — La variance de log(diversité alpha) se répartit, selon l'indice, en tissu 19–26 % (marginal), individu 17–21 %, site-année 10–14 % (séquentiel), technique ≤ 0,3 %, résiduel 38–45 %, avec le même ordre des facteurs sur les quatre indices.**
Script `scripts/34-alpha_partition.R` · Entrées `ALPHA`, `META-ANA` → `TESTS-1003` · **validé sous la règle D7** (quatre indices), **dans le manuscrit** (Results, Alpha diversity) · remplacé le 2026-10-03. *Correction* : l'ancien R8 (tissu 18,7 %, site-année 10,9 %, run 0,26 %, résiduel 69 %) était attribué à tort au script 14, qui est une PERMANOVA de composition ; il venait d'un diagnostic de conversation sans script (`docs/diagnostic_questions_recherche.md`). Les deux jeux de chiffres ne sont pas comparables (pas de terme individu dans l'ancien). Réf. `docs/recalcul/note_tests_2026-10-03.md` §(d).

## Profondeur et choix de métrique

**R9 — La géométrie bêta pondérée est invariante à la profondeur : UniFrac pondéré r = 0,9994 et Bray-Curtis r = 0,9985 entre 3 000 et 500 lectures, alors que l'UniFrac non pondéré tombe à r = 0,937 et la richesse perd 42 %.**
Scripts `22-depth_agreement.sh`, `23-bray_depth_agreement.sh` · Entrées `BETA-*`, `BETA-WUF-500` · **validé**, dans le manuscrit (§8.6)

**R10 — Aucune profondeur ne corrige le biais de sélection : sur la nageoire caudale il passe de +30,4 points à 3 000 lectures à +2,5 à 500, mais le signal de catégorie y est identique (3/3 dans les deux dispositifs).**
Script `20-variance_partition_category.sh` (mode d500) · Entrées `BETA-WUF`, `BETA-WUF-500`, `META-ANA` · **validé**
*Correction 2026-10-05* : les écarts de rétention de cette entrée (+30,4 → +2,5) viennent d'une trace antérieure à la reclassification de septembre et n'étaient produits par aucun script ; remplacés par R35. Le constat sur le signal de catégorie n'est pas touché.

## Structure de la variance : station, position, catégorie

**R11 — La station domine la composition : R² = 0,15–0,31 selon tissu et métrique, soit 10 à 20 × l'effet de la catégorie génotypique.**
Script `20-variance_partition_category.sh` · Entrées `BETA-*`, `META-ANA` · **validé sous la règle D7** (rapporté sur les quatre métriques), dans le manuscrit (Results, ex-§8.9)

**R12 — La catégorie génotypique explique 1,4 à 3,3 % de la variance selon la métrique et l'ordre d'entrée ; servie en premier elle atteint 3,3 % (UniFrac pondéré).**
Script `20-variance_partition_category.sh` · Entrées `BETA-*`, `META-ANA` · **périmé** (classification d'août) — **remplacé dans le manuscrit par R23** le 2026-09-25

**R13 — Aucun tissu n'est significatif de façon robuste dans les deux dispositifs pour les quatre métriques : branchie 2/4, midgut 2/4, hindgut 0/4. Conclure sur deux métriques seules serait une surinterprétation.**
Script `20-variance_partition_category.sh` · Entrées `BETA-*` · **validé sous la règle D7** (rapporté sur les quatre métriques) · Réf. `docs/decision_phylo_and_category.md`

**R14 — L'effet de position dans la plaque est réel : R² = 0,18–0,40, significatif dans 9 à 12 strates sur 12, et confondu avec la catégorie (V de Cramér 0,477 → 0,504 après génotypage, jusqu'à 0,559–0,694 aux trois stations à gradient).**
Scripts `17-position_effect.sh`, `18-position_control.sh` · Entrées `BETA-*`, `META-ANA` · **validé** ; sorti du modèle principal par D2, conservé en sensibilité · dans le manuscrit (Results « Plate position », ex-§8.8)
*Correction 2026-09-25* : les V 0,477 / 0,504 portaient sur le taxon morphologique puis sur la classe d'août (les scripts 17–18 lisaient `samples_all.csv`). Sur la classification à 25 chromosomes : **V = 0,527 (passe 1), 0,479 (passe 2)** — `docs/recalcul/note_recalcul_2passes.md` §1–2, entrées `RECAT`, `META-ANA`.
*Correction 2026-10-03* : la colonne de plaque suit l'ordre de traitement des poissons **dans chaque campagne** (ρ 0,55–0,93), et pas seulement à cinq stations : l'effet de position est inséparable de l'ordre de traitement et de la durée de séjour en vivier (R32).

**R15 — La prédiction transgressive en dispersion n'est pas soutenue et le sens est inversé : les hybrides sont les MOINS dispersés dans 31 tests sur 48 (p = 9,4 × 10⁻⁶), un seul test est significatif dans le sens transgressif, aucun en intra-station.**
Script `24-permdisp.sh` · Entrées `BETA-*`, `META-ANA` · **périmé** (classification d'août, sans correction de petit effectif) — voir R25 et R34
*Correction 2026-10-03* : calculé sans `bias.adjust`, ce qui biaise vers « hybrides moins dispersés » (R34).

## Génotypage et dispositif

**R16 — Le génotypage à 25 chromosomes donne 59 Cn / 42 Hy / 79 Pt ; 16 individus sur 180 changent de classe par rapport aux 12 chromosomes (13 Pt→Hy, 1 Cn→Hy, 1 Hy→Pt, 1 Hy→Cn), et 22 des 42 hybrides sont quasi-purs (introgressés sur 1 chromosome sur 25 dans 17 cas).**
Script `metadata/source/genome_hybride.Rmd` (produit par André), vérifié dans `docs/synthese_genotypage_25chr.md` · Entrées `GENO-SRC` → `GENO-SEPT` · **validé**

**R17 — Le seuil D = 0,12 sépare hybrides et parentaux sur un intervalle vide (0,1191–0,1301).**
Script `metadata/source/genome_hybride.Rmd` (produit par André) · Entrées `GENO-SRC` · **validé**

**R18 — Contrôle négatif interne : les deux stations du Suran, séparées de 25,4 km par une barrière de 2,5 m, portent des peuplements disjoints — Pont-d'Ain 12 Cn / 2 Hy / 0 Pt, Chavannes 0 / 0 / 19. Prédiction d'André confirmée.**
Script `16-station_metadata.py` · Entrées `STATIONS`, `GENO-SEPT` · **validé**, dans le manuscrit (§1)

**R19 — Le recalcul en deux passes est exécuté : 17 étapes en code 0 (position, contrôle, partition, partition d500, PERMDISP) sur les 4 jeux de catégories, plus un témoin d'effectif de 20 tirages de 22 individus parmi 158.**
Scripts `26-recalcul_categories.sh`, `27-recat_witness_effectif.sh` · Entrées `GENO-SEPT`, `BETA-*` → `RECAT` · **validé** (les scripts relancés en mode « août » reproduisent au bit près les sorties d'août ; PERMDISP au bruit Monte-Carlo près, 2 basculements sur 156 tests) · interprété dans `docs/recalcul/note_recalcul_2passes.md`, entrées `RECAT-DOC` · chiffres en R21–R25

## Recalcul en deux passes (classification à 25 chromosomes)

Passe 1 = 20 hybrides intermédiaires, quasi-purs exclus (n = 158) ; passe 2 = 42 hybrides (n = 180). Source unique des
chiffres ci-dessous : `docs/recalcul/note_recalcul_2passes.md` et `correspondance_ancien_nouveau.csv`.

**R21 — Seule détection robuste dans les six combinaisons (3 jeux de catégories × avec/sans position) : Jaccard dans le midgut, 3/3 runs en séquentiel et en station bloquée.**
Scripts `20-variance_partition_category.sh` via `26-recalcul_categories.sh` · Entrées `RECAT`, `BETA-JAC`, `META-ANA` · **validé sous la règle D7** (rapporté sur les quatre métriques), dans le manuscrit (Results, ex-§8.9)

**R22 — Le signal de la nageoire caudale en UniFrac pondéré est présent en passe 1 (3/3 runs, deux schémas, avec et sans position) et absent en passe 2 (p bloqué sans position 0,073–0,095). Aucun de 20 retraits aléatoires de 22 poissons non quasi-purs ne le restaure (0/20) : il dépend de la définition des hybrides, pas de l'effectif.**
Scripts `26-recalcul_categories.sh`, `27-recat_witness_effectif.sh` · Entrées `RECAT`, `BETA-WUF`, `META-ANA` · **dépendant de la métrique sous la règle D7** : le signal caudal n'existe que sur l'UniFrac pondéré et seulement en passe 1 (R27), dans le manuscrit (Results, ex-§8.9). Mécanisme (dilution du contraste Hy–Pt par les quasi-purs à fond Pt, 13 des 16 changements de classe) : `[À CONFIRMER]` — testé le 2026-10-03 (R30) : compatible, non établi.

**R23 — Parts de variance en deux passes : catégorie 1,3–3,7 %, station 14–29 % (médianes par métrique — agrégat différent de l'étendue par strate de R11, ne pas les comparer) ; aucun tissu détecté par les quatre métriques dans les deux schémas, dans aucune passe, avec ou sans position.**
Script `20-variance_partition_category.sh` via `26` · Entrées `RECAT`, `BETA-*`, `META-ANA` · **validé sous la règle D7** (rapporté sur les quatre métriques), dans le manuscrit (Results, ex-§8.9, Table S9)

**R24 — D2 change des conclusions : sur les 32 cellules de la Table S9, 14 diffèrent entre modèles avec et sans position, dont 8 changent de classe (robuste ↔ partiel ↔ aucun). Le résultat caudal R22 n'en dépend pas.**
Script `20-variance_partition_category.sh` (modèles `sanspos_*`) · Entrées `RECAT`, `RECAT-DOC` · **à arbitrer par JF** (D2, note §5), dans le manuscrit (Table S9, deux versions)

**R25 — PERMDISP en deux passes : hybrides les moins dispersés dans 34 (passe 2) et 32 (passe 1) tests sur 48 en station bloquée ; sur les 68 strates intra-station communes aux trois jeux, ils restent les moins dispersés partout. Les 5 tests transgressifs significatifs de la passe 2 portent tous sur la branchie de Saint-Just (3–4 Pt par strate).**
Script `24-permdisp.sh` via `26` · Entrées `RECAT`, `BETA-*`, `META-ANA` · **corrigé le 2026-10-03, remplacé par R34** : sans `bias.adjust`, les distances des hybrides (plus petite catégorie de chaque strate) étaient sous-estimées. Passe 1 : 32 → 22/48 en station bloquée, 45 → 25/68 intra-station ; passe 2 : 34 → 32/48. Retiré du manuscrit (Results, Dispersion réécrit d'après R34) ; Table S10 et Figure S3 régénérées sur R34 le 2026-10-05 (`scripts/41-supp_S10_S3.py`).

## Dépôt de données

**R20 — Le dépôt ENA PRJEB124417 est validé et corrigé : 727/727 alias et accessions ERS conformes, 3 472/3 472 valeurs corrigées sur 5 attributs, 0 changement hors champs cibles.**
Scripts `ena_deposit/4_corriger_metadonnees.sh`, `5_verifier_correction.sh` · Entrées `ENA-SAMP`, `ENA-RUNS`, `STATIONS` · **validé**, dans le manuscrit (Data availability)

**R26 — Correction de l'identité d'hôte du 2026-09-25 : 568 échantillons (1 199 champs), reçu de production success=true, 0 erreur, 568/568 alias et accessions identiques (MODIFY, aucune création). Application vérifiée sur le dépôt le 2026-09-25 à 18:38 : 727 échantillons interrogés, 1 199 champs vérifiés, 1 199 conformes, 0 non conforme, 0 introuvable (TITLE 568, host common name 568, host scientific name 63).**
Scripts `scripts/28-ena_hote_sept.py`, `ena_deposit/8_corriger_hote_sept.sh`, vérification `9_verifier_hote_sept.sh` (lancée au clavier par JF, 8 lots) · Entrées `ENA-HOTE`, `META-ANA` · **validé** · rapport `ena_deposit/verification_hote_sept_20260925_1838.txt` · conséquence : note grise ENA retirée du supplément (`MS-SUP`)

**R28 — Vérification cumulée du dépôt PRJEB124417 après les deux campagnes de correction : 727 échantillons interrogés, 4 612 champs conformes sur 4 612, 0 non conforme, 0 introuvable, 0 rupture de chaînage entre la table d'août et celle de septembre. Par champ : `collection date` 727, latitude 727, longitude 727, `region and locality` 727, `TITLE` 568, `host common name` 568, `host scientific name` 568**. Lancé au clavier par JF, 8 lots via l'API de rapport Webin. Rapport `ena_deposit/verification_cumulee_20260930_2019.txt`. Englobe et confirme R20 (5 attributs, 31/08) et R26 (identité d'hôte, 25/09) en une seule vérification.
Script `ena_deposit/7_verifier_exhaustif.sh` · Entrées `ENA-CORR`, `ENA-HOTE`, `ENA-VERIF` · **validé**


**R27 — La métrique décide de trois conclusions sur cinq. Indifférents au choix : le gradient externe/interne (significatif sur les quatre indices, p < 10⁻¹⁶, mais d'amplitude 1,51 en Shannon à 2,99 en inverse Simpson) et l'ampleur de l'effet de catégorie (R² médian 0,013–0,036 sur les quatre métriques en passe 2). Décidés par la métrique : le contraste midgut/hindgut, significatif sur les seuls indices non pondérés (0,83 p = 0,009 ; Faith PD 0,87 p = 0,003) et non significatif sur Shannon et l'inverse Simpson ; le compartiment du dimorphisme sexuel, interne sur les indices non pondérés mais externe sur Shannon ; et le compartiment portant l'effet de catégorie, la caudale n'existant que sur l'UniFrac pondéré en passe 1 tandis que le midgut est détecté par 4 métriques sur 4 et le hindgut par 3 sur 4 en passe 2. En composition le clivage n'est pas pondéré/non pondéré : Bray-Curtis, pourtant pondéré, se comporte comme Jaccard, et l'UniFrac pondéré est la métrique isolée.**
Script `29-d7_metriques.py` · Entrées `RECAT`, `BETA-*`, `ALPHA-PHYLO`, `META-ANA` · **validé** · recoupement 14/14 avec `docs/recalcul/d2_avec_vs_sans_position.csv` · Réf. `docs/decision_D7_metrique.md`, `docs/figures/fig_d7_metriques.png`

## Tests déclarés a priori du 2026-10-03

Plan `docs/plan_tests_2026-10-03.md` (commit `bd6ba3d`, avant calcul), verdicts appliqués mécaniquement par `scripts/36-lecture_tests.py` ; interprétation `docs/recalcul/note_tests_2026-10-03.md`.

**R29 — L'affaiblissement du signal caudal (UniFrac pondéré, passe 1) à 500 lectures ne tient ni à la profondeur ni à l'effectif : sur les mêmes échantillons, 500 et 3 000 lectures donnent le même résultat (3/3 runs, p 0,010–0,026 contre 0,009–0,023) ; il tient aux échantillons de caudale qui ne passent le seuil qu'à 500 lectures (n 147–151 contre 120–124). Aucun de 20 retraits aléatoires de 22 poissons ne reproduit le motif de la passe 1 (0/20).**
Scripts `scripts/35-temoin_ensemble_d500.sh`, `scripts/27-recat_witness_effectif.sh` (mode 500) · Entrées `BETA-WUF`, `BETA-WUF-500`, `META-ANA` → `TESTS-1003` · **dépendant de la métrique** (UniFrac pondéré seul existe à 500 lectures), dans le manuscrit (Results, Composition) · raison de la dilution par ces échantillons `[À CONFIRMER]`, non isolée

**R30 — Réétiqueter Hy 19 Pt et 3 Cn tirés dans les stations des quasi-purs supprime le signal caudal de la passe 1 dans 16 tirages sur 20 (référence sans injection : signal présent) ; mais les 19 quasi-purs à fond Pt ne se distinguent ni des Pt (p 0,28–0,60) ni des 20 intermédiaires (p 0,15–0,26, n 25–26). Dilution suffisante, non établie : verdict déclaré « indéterminée ».**
Script `scripts/32-dilution_quasipurs.sh` · Entrées `BETA-WUF`, `META-ANA` → `TESTS-1003` · **validé** (verdict indéterminé), **dans le manuscrit** (Results, Composition ; méthode §8.12) · non évaluable à cette puissance pour QPpt contre intermédiaires

**R31 — En diversité alpha, les hybrides ne sont transgressifs dans aucune combinaison (0/32). Le seul classement établi selon D7 est « dominant Cn » (Hy non distinct de Cn, distinct de Pt) : caudale en passe 1 (4 indices sur 4, p catégorie 0,012–0,128, stable avec position) et midgut en passe 2 (3 sur 4, p 0,040–0,111, **instable** avec position). Aucun classement établi ailleurs.**
Script `scripts/33-alpha_categorie.py` · Entrées `ALPHA`, `META-ANA` → `TESTS-1003` · **validé sous la règle D7**, **dans le manuscrit** (Results, Alpha diversity ; Figure 2) ; p non corrigées (5 tests sur 32 à p < 0,05) ; « dominant » = absence de différence avec Cn, pas égalité ; confusion possible avec l'ordre de traitement (hotus d'abord) `[À CONFIRMER]`, non testée

**R32 — Dans chaque campagne de pêche, la colonne de plaque suit l'ordre de traitement des poissons (ρ de Spearman 0,55–0,93) : l'effet de position (R14) est inséparable de l'ordre de traitement et de la durée de séjour en vivier dans ce dispositif. Le découplage apparent à quatre stations venait d'un calcul par station mélangeant 2014 et 2015. Le test colonne contre rang qui devait départager D2 est donc sans portée (verdict mécanique : indéterminé).**
Script `scripts/31-sejour_vivier.sh` (`spearman_rang_pos.tsv`, `sejour_tests.tsv`) · Entrées `BETA-*`, `META-ANA` → `TESTS-1003` · **validé**, dans le manuscrit (Results, Plate position ; ρ 0,548–0,950 sur 12 campagnes station × année, recalculé par `scripts/40-verif_article_v2.py`) · conséquence pour D2 à arbitrer par JF

## Indice 4H et reprise PERMDISP (2026-10-03, soir)

**R33 — Indice 4H (Jaccard, genre, ρ = 0,5, N commun) : axe transgressif dominant, porté par Loss, en caudale, midgut et hindgut des deux passes (G + L 0,584–0,688) ; axe parental, porté par Intersection, en branchie (0,409–0,462). Aucun axe transgressif robuste : la version Bray-Curtis met les huit tissu × passe sur l'axe parental (G + L 0,217–0,351), le rang famille aussi en caudale. Seul robuste : axe parental de la branchie en passe 2. Aucune paire de tissus distinguée (intervalles bootstrap jamais disjoints dans les 3 runs). Rétention préférentielle des taxons partagés partout (≥ 98,4 % des bootstraps). Hybride nul : G + L 0,405–0,566 (constat descriptif, hors règle).**
Scripts `scripts/37-indice_4H.R` (calcul `6372af6`, mise en forme `144bb98`), `scripts/38-lecture_4H.py` · Entrées `ASV-CLEAN`, `TAX`, `META-ANA` → `FOURH` · plan pré-déclaré `docs/plan_4H_2026-10-03.md` (commité avant calcul) · **validé**, dans le manuscrit (§8.11, Results « Four-dimensional index », Figure 5) · interprétation `docs/recalcul/note_4H_2026-10-03.md`. Couverture au genre 64,1 % des lectures ; profondeur 4H 1 000 lectures assignées au genre (1 749/1 784 échantillons). Pourquoi le core hybride est plus petit : `[À CONFIRMER]`, non testé.

**R34 — PERMDISP corrigé du biais de petit effectif (`bias.adjust = TRUE`) : la prédiction transgressive en dispersion n'est soutenue dans aucune passe ni aucun dispositif ; « hybrides moins dispersés » n'est maintenu qu'en station bloquée (passe 1 : 22/48, binomiale p = 0,048 ; passe 2 : 32/48, p = 2,4 × 10⁻⁶), et retiré en intra-station (25/68 ; 39/120). Porté surtout par Bray-Curtis en passe 2 (écart médian −0,068). Caudale : dispersion homogène sauf 1 run en UniFrac pondéré passe 1 (p = 0,048, Hy les plus dispersés).**
Scripts `scripts/24-permdisp.sh` (`PERMDISP_BIAS=1`, commit `ecef636`), `scripts/39-lecture_permdisp_biais.py` (`ec5e318`) · Entrées `BETA-*`, `META-ANA` → `PERMDISP-B` · plan `docs/plan_permdisp_biais_2026-10-03.md` (commité avant calcul ; les décomptes de direction avaient été calculés avant, déclaré) · **validé**, dans le manuscrit (Results « Dispersion », Discussion, Figure 4 ; supplément Table S10 et Figure S3 depuis le 2026-10-05) · **défaut de l'analyse antérieure de l'agent**, remplace R15/R25.


**R35 — Biais de sélection de la raréfaction, recalculé : à 3 000 lectures en caudale, P. toxostoma est retenu plus souvent que les hybrides de 36,4 points (passe 1) et 19,8 (passe 2) dans le run durance1, 29,0–36,4 et 14,7–19,8 sur les trois runs ; à 500 lectures, 3,8 et 5,7 (durance1 ; 2,6–3,8 et 3,4–5,7 sur les runs). En midgut à 500 lectures : 14,0 et 8,9 dans durance1, 5,7–14,0 et 7,8–8,9 sur les runs. À la station Confluence Buech-Meouge : 48,2 et 35,7 (durance1), 19,6–48,2 et 7,1–35,7 sur les runs.**
Script `scripts/43-retention_profondeur.py` · Entrées `ASV-CLEAN`, `META-ANA` → `RETENTION` · **validé** ; dans le manuscrit (§8.6, valeurs durance1, précisé le 2026-10-05 ; Figure S1 c–d). Le choix entre un run et l'étendue reste à trancher (A_FAIRE, Rédaction (b)).