# RESULTATS

Règle : une entrée n'est admise que si elle pointe vers **un script** et vers **des données
référencées dans `DONNEES.md`**. Statuts : `préliminaire` / `validé` / `dans le manuscrit`.

> **D7 est ouverte** (métrique de diversité, cf. `DECISIONS.md` du 2026-09-25). Tout résultat
> dont la valeur dépend du choix de métrique reste **préliminaire**, même s'il est déjà écrit
> dans le manuscrit. Ne pas le promouvoir sans décision consignée.

---

## Pipeline et qualité des données

**R1 — La table finale compte 44 349 ASV × 2 295 échantillons, ramenés à 2 180 × 44 200 après retrait des contrôles.**
Script `scripts/05-merge_taxonomy.sh` puis `12-clean_table.py` · Entrées `RAW-D1/2/3` → `ASV-FILT` → `ASV-CLEAN` · **validé**, dans le manuscrit (§8.5)

**R2 — Le 12S mitochondrial de l'hôte représentait 14 à 67 % des lectures ; 1 144 ASV Mitochondria retirés.**
Script `scripts/02-remove_12S_worker.sh` · Entrées `RAW-D1/2/3` · **validé**, dans le manuscrit

**R3 — Le mock restitue 8/8 espèces attendues à 100 % ; fuite inter-puits (crosstalk) de 0,0002 %.**
Scripts `06-validate_mock.sh`, `10-crosstalk.sh` · Entrées `ASV-FILT`, `MOCK-REF` · **validé**, dans le manuscrit

**R4 — La décontamination retire 66 ASV et conserve 99,76 % des lectures.**
Script `07-decontam.sh` · Entrées `ASV-FILT`, `DECONT-SC` · **validé**, dans le manuscrit

**R5 — La raréfaction à 3 000 lectures conserve 81,8 % des échantillons.**
Script `09-qc_depth.sh` · Entrées `ASV-CLEAN` · **validé**, dans le manuscrit

**R6 — La moyenne sur 400 tirages est convergée : erreur de Monte-Carlo < 0,2 % entre deux chaînes indépendantes.**
Script `15-rarefaction_converge.sh` · Entrées `ASV-CLEAN` → `BETA-*` · **validé**, dans le manuscrit (§8.6)

**R7 — La structure de réplication est nichée : Bray-Curtis intra-librairie 0,118 vs inter-librairie 0,248 ; l'index i7 diffère pour 384 des 768 librairies et l'i5 pour 576 entre les deux préparations.**
Script `13-run_design.sh` · Entrées `META-SAMP`, `ASV-CLEAN` · **validé**, dans le manuscrit (§8.7)

**R8 — La variance de la richesse ASV se répartit en tissu 18,7 %, site-année 10,9 %, run 0,26 %, résiduel 69 %.**
Script `14-variance_partition.sh` · Entrées `ASV-CLEAN`, `META-ANA` · **préliminaire** (richesse ASV, D7)

## Profondeur et choix de métrique

**R9 — La géométrie bêta pondérée est invariante à la profondeur : UniFrac pondéré r = 0,9994 et Bray-Curtis r = 0,9985 entre 3 000 et 500 lectures, alors que l'UniFrac non pondéré tombe à r = 0,937 et la richesse perd 42 %.**
Scripts `22-depth_agreement.sh`, `23-bray_depth_agreement.sh` · Entrées `BETA-*`, `BETA-WUF-500` · **validé**, dans le manuscrit (§8.6)

**R10 — Aucune profondeur ne corrige le biais de sélection : sur la nageoire caudale il passe de +30,4 points à 3 000 lectures à +2,5 à 500, mais le signal de catégorie y est identique (3/3 dans les deux dispositifs).**
Script `20-variance_partition_category.sh` (mode d500) · Entrées `BETA-WUF`, `BETA-WUF-500`, `META-ANA` · **validé**

## Structure de la variance : station, position, catégorie

**R11 — La station domine la composition : R² = 0,15–0,31 selon tissu et métrique, soit 10 à 20 × l'effet de la catégorie génotypique.**
Script `20-variance_partition_category.sh` · Entrées `BETA-*`, `META-ANA` · **préliminaire** (D7), dans le manuscrit (§8.9)

**R12 — La catégorie génotypique explique 1,4 à 3,3 % de la variance selon la métrique et l'ordre d'entrée ; servie en premier elle atteint 3,3 % (UniFrac pondéré).**
Script `20-variance_partition_category.sh` · Entrées `BETA-*`, `META-ANA` · **préliminaire** (D7 + classification d'août) — **remplacé dans le manuscrit par R23** le 2026-09-25

**R13 — Aucun tissu n'est significatif de façon robuste dans les deux dispositifs pour les quatre métriques : branchie 2/4, midgut 2/4, hindgut 0/4. Conclure sur deux métriques seules serait une surinterprétation.**
Script `20-variance_partition_category.sh` · Entrées `BETA-*` · **préliminaire** (D7) · Réf. `docs/decision_phylo_and_category.md`

**R14 — L'effet de position dans la plaque est réel : R² = 0,18–0,40, significatif dans 9 à 12 strates sur 12, et confondu avec la catégorie (V de Cramér 0,477 → 0,504 après génotypage, jusqu'à 0,559–0,694 aux trois stations à gradient).**
Scripts `17-position_effect.sh`, `18-position_control.sh` · Entrées `BETA-*`, `META-ANA` · **validé** ; sorti du modèle principal par D2, conservé en sensibilité · dans le manuscrit (§8.8)
*Correction 2026-09-25* : les V 0,477 / 0,504 portaient sur le taxon morphologique puis sur la classe d'août (les scripts 17–18 lisaient `samples_all.csv`). Sur la classification à 25 chromosomes : **V = 0,527 (passe 1), 0,479 (passe 2)** — `docs/recalcul/note_recalcul_2passes.md` §1–2, entrées `RECAT`, `META-ANA`.

**R15 — La prédiction transgressive en dispersion n'est pas soutenue et le sens est inversé : les hybrides sont les MOINS dispersés dans 31 tests sur 48 (p = 9,4 × 10⁻⁶), un seul test est significatif dans le sens transgressif, aucun en intra-station.**
Script `24-permdisp.sh` · Entrées `BETA-*`, `META-ANA` · **validé** ; réserve : `betadisper` n'accepte pas de covariable, la position n'y est pas ajustée · dans le manuscrit

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
Scripts `20-variance_partition_category.sh` via `26-recalcul_categories.sh` · Entrées `RECAT`, `BETA-JAC`, `META-ANA` · **préliminaire** (D7), dans le manuscrit (§8.9)

**R22 — Le signal de la nageoire caudale en UniFrac pondéré est présent en passe 1 (3/3 runs, deux schémas, avec et sans position) et absent en passe 2 (p bloqué sans position 0,073–0,095). Aucun de 20 retraits aléatoires de 22 poissons non quasi-purs ne le restaure (0/20) : il dépend de la définition des hybrides, pas de l'effectif.**
Scripts `26-recalcul_categories.sh`, `27-recat_witness_effectif.sh` · Entrées `RECAT`, `BETA-WUF`, `META-ANA` · **préliminaire** (D7), dans le manuscrit (§8.9). Mécanisme (dilution du contraste Hy–Pt par les quasi-purs à fond Pt, 13 des 16 changements de classe) : `[À CONFIRMER]`, non testé isolément.

**R23 — Parts de variance en deux passes : catégorie 1,3–3,7 %, station 14–29 % (médianes par métrique — agrégat différent de l'étendue par strate de R11, ne pas les comparer) ; aucun tissu détecté par les quatre métriques dans les deux schémas, dans aucune passe, avec ou sans position.**
Script `20-variance_partition_category.sh` via `26` · Entrées `RECAT`, `BETA-*`, `META-ANA` · **préliminaire** (D7), dans le manuscrit (§8.9, Table S8)

**R24 — D2 change des conclusions : sur les 32 cellules de la Table S8, 14 diffèrent entre modèles avec et sans position, dont 8 changent de classe (robuste ↔ partiel ↔ aucun). Le résultat caudal R22 n'en dépend pas.**
Script `20-variance_partition_category.sh` (modèles `sanspos_*`) · Entrées `RECAT`, `RECAT-DOC` · **préliminaire** (D7) — **à arbitrer par JF** (note §5), dans le manuscrit (Table S8, deux versions)

**R25 — PERMDISP en deux passes : hybrides les moins dispersés dans 34 (passe 2) et 32 (passe 1) tests sur 48 en station bloquée ; sur les 68 strates intra-station communes aux trois jeux, ils restent les moins dispersés partout. Les 5 tests transgressifs significatifs de la passe 2 portent tous sur la branchie de Saint-Just (3–4 Pt par strate).**
Script `24-permdisp.sh` via `26` · Entrées `RECAT`, `BETA-*`, `META-ANA` · **validé** (même réserve que R15), dans le manuscrit (§8.9, Table S9, Figure S3)

## Dépôt de données

**R20 — Le dépôt ENA PRJEB124417 est validé et corrigé : 727/727 alias et accessions ERS conformes, 3 472/3 472 valeurs corrigées sur 5 attributs, 0 changement hors champs cibles.**
Scripts `ena_deposit/4_corriger_metadonnees.sh`, `5_verifier_correction.sh` · Entrées `ENA-SAMP`, `ENA-RUNS`, `STATIONS` · **validé**, dans le manuscrit (Data availability)

**R26 — Correction de l'identité d'hôte du 2026-09-25 : 568 échantillons (1 199 champs), reçu de production success=true, 0 erreur, 568/568 alias et accessions identiques (MODIFY, aucune création). Application effective non vérifiée.**
Scripts `scripts/28-ena_hote_sept.py`, `ena_deposit/8_corriger_hote_sept.sh`, vérification `9_verifier_hote_sept.sh` · Entrées `ENA-HOTE`, `META-ANA` · **soumis, vérification en attente** — passe `validé` quand `9_verifier_hote_sept.sh` rend 727 conformes / 0
