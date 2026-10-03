# Plan des cinq tests du 2026-10-03 — déclaration a priori

**Statut : déclaré avant tout calcul.** Ce fichier est commité avant la soumission du premier job.
Les définitions, les sous-ensembles et les règles de lecture ci-dessous ne sont pas modifiés après
avoir vu les résultats. Tout écart sera signalé comme tel dans `docs/recalcul/note_tests_2026-10-03.md`,
avec sa raison.

Validation : JF, 2026-10-03, questions 2.2 et 2.3 de `docs/questions_JF_2026-10-03_v2.docx`, puis
approbation du plan de session. Sorties : `results/tests_20261003/<test>/` (non versionnées).

Conventions communes, reprises des scripts 20 et 27 :

- matrices `results/rarefaction/beta_mean_*_N400.rds` (3 000 lectures, 400 tirages), quatre
  métriques ;
- strates run × tissu, chaque run analysé séparément (pas d'empilement) ;
- `pos` = `col_rank_station`, `st` = `station`, `cat` = `categorie` de `metadata/analysis_metadata.csv` ;
- `adonis2` avec 999 permutations, `by` explicite ; seuil **strict** p < 0,05 ;
- « robuste » = significatif dans les 3 runs sur 3 ;
- **règle D7** : un effet n'est **établi** que s'il est robuste pour au moins une métrique pondérée
  (Bray-Curtis, UniFrac pondéré ; en alpha, Shannon et inverse Simpson) **et** au moins une métrique de
  présence (Jaccard, UniFrac non pondéré ; en alpha, richesse et Faith PD) ; sinon il est rapporté
  comme dépendant de la métrique, en nommant laquelle ;
- un résultat nul sur un petit effectif est rapporté comme **non évaluable à cette puissance**, jamais
  comme une absence.

## 0. Deux défauts du registre qui redéfinissent les tests (c) et (d)

1. **R8 n'a pas de script.** `RESULTATS.md` attribue R8 (variance de la richesse : tissu 18,7 %,
   site-année 10,9 %, run 0,26 %, résiduel 69 %) à `scripts/14-variance_partition.sh`. Or ce script
   fait une PERMANOVA sur la composition (`D ~ library + run_label + tissue + fish`). Les chiffres de
   R8 viennent d'un diagnostic de conversation, consigné dans `docs/diagnostic_questions_recherche.md`,
   et aucun script versionné ne les produit. Le test (d) n'est donc pas une « refonte » de R8 : c'est
   un premier calcul scripté, dont la méthode n'est pas comparable au chiffre historique.
2. **Faith PD est déjà exploité.** Depuis le 2026-09-30, `scripts/29-d7_metriques.py` l'utilise dans
   les contrastes alpha de R27 (gradient externe/interne, midgut/hindgut, dimorphisme sexuel). La
   mention « Faith PD calculé non exploité » d'`A_FAIRE.md` est périmée. Ce qui n'a été fait pour
   **aucun** indice alpha, c'est le test de l'effet de la catégorie génotypique. Le test (c) porte donc
   sur ce point, qui est l'hypothèse H1 en diversité alpha.

## (e) Séjour en vivier : colonne de plaque contre rang de dissection

**Question.** L'effet de position (R14) est-il un artefact de plaque, ou un effet de la durée de séjour
en vivier avant dissection ?

**Fondement.** André, 2026-10-03 : les poissons restent vivants en vivier jusqu'à la dissection, qui
prend 4 à 6 min par poisson, et les numéros suivent l'ordre de traitement (2026-09-25). À cinq
stations sur neuf, la colonne suit l'ordre de traitement (ρ de 0,87 à 0,95,
`docs/point_etape_25sept.md`) : les deux variables y sont inséparables.

**Sous-ensemble.** Les quatre stations où la colonne et l'ordre se découplent : `Chavannes-sur-Suran`
(ρ = 0,008), `Pont-d'Ain` (0,17), `Avignon` (0,37), `Confluence Buech-Meouge` (0,39), soit 92 individus,
avec les catégories de la passe 2. Pertuis, où deux campagnes ont eu lieu la même année, n'en fait pas
partie.

**Variables.**

- `camp` = station × année (une campagne par station et par année dans ce sous-ensemble) ;
- `rang` = rang de `individual` (numéro) dans sa campagne, 1 pour le premier traité ; c'est
  l'approximation de la durée de séjour (environ 5 min par rang) ;
- `pos` comme ci-dessus.

Contrôle préalable rapporté : la corrélation de Spearman entre `rang` et `pos` par campagne et par
tissu.

**Modèles**, par métrique × run × tissu :

- **M1**, sur les quatre stations, avec au moins 20 échantillons :
  `adonis2(D ~ camp + cat + pos + rang, by = "margin")`, permutations dans les blocs `camp` ;
- **M2**, sur Chavannes seule (19 Pt, une seule catégorie), avec au moins 10 échantillons :
  `adonis2(D ~ camp + pos + rang, by = "margin")`, permutations dans les blocs `camp`. C'est le témoin :
  un effet de rang n'y peut pas être un effet de catégorie.

**Règle de lecture**, décidée sur M1 ; M2 est rapporté comme témoin et ne décide pas :

- **séjour probable** : `rang` établi (règle D7) dans au moins un tissu, et `pos` non établi dans ce
  même tissu ;
- **artefact de plaque probable** : `pos` établi dans au moins un tissu, et `rang` établi dans aucun ;
- **indéterminé** : les deux établis dans un même tissu, ou aucun des deux nulle part. Dans le second
  cas, la conclusion est « non évaluable à cette puissance ».

**Conséquence pour D2**, à arbitrer par JF :

- séjour probable : la covariable de position est requalifiée en ordre de traitement, et le §8.8 est
  réécrit en conséquence ;
- artefact de plaque probable : D2 se tranche avec la position comme artefact ;
- indéterminé : JF tranche D2 parmi les options (a) à (c) de la question 2.1.

## (b) Dilution du contraste Hy–Pt par les quasi-purs à fond Pt

**Hypothèse testée (R22).** Le signal caudal en UniFrac pondéré, présent en passe 1 et absent en
passe 2, disparaît parce que les 19 quasi-purs à fond Pt (`type_genome = quasi-pur`,
`index_mediane_andre < 0,5`), étiquetés Hy en passe 2, ont une composition de type Pt et diluent le
contraste.

**b2 — test direct.** Groupes : `QPpt` (19), `INT` (`type_genome = intermediaire`, 20), `Pt`
(`type_genome = pur` et `categorie = Pt`, 79). Les 3 quasi-purs à fond Cn sont exclus, trop peu nombreux.
Deux comparaisons, `QPpt` contre `Pt` et `QPpt` contre `INT`, par métrique × run × tissu, chacune avec
deux modèles :

- `adonis2(D ~ pos + grp, by = "terms")`, permutations dans les blocs `st` ;
- `adonis2(D ~ grp)`, permutations dans les blocs `st` (sans position).

On rapporte aussi le nombre de stations portant les deux groupes. Si aucune ne les porte, le test est
dégénéré et noté NA.

**b1 — injection témoin.** On part de la passe 1 (158 individus, 20 Hy) et l'on fait 20 tirages. À chaque
tirage, on ajoute à Hy 19 Pt et 3 Cn tirés **dans les mêmes stations** et en mêmes nombres que les
`QPpt` et `QPcn` (si une station en manque, on complète au hasard ailleurs, et on le rapporte). Les
modèles sont ceux du script 27 : `cat_apres_pos_station_bloquee` et `sanspos_cat_station_bloquee`. Un
tirage « garde le signal » si la caudale en UniFrac pondéré est significative en 3/3 runs **dans les
deux schémas**, définition de « présent » de R22. On calcule aussi la référence sans injection (passe 1)
avec le même code : elle doit reproduire R22.

**Limite déclarée.** Les poissons réétiquetés quittent leur classe parentale (Pt passe à 60). La
passe 2, elle, garde 79 Pt.

**Règle de lecture** (critère principal : caudale, UniFrac pondéré) :

- **dilution soutenue** : en b2, `QPpt` ne diffère pas de `Pt` (p ≥ 0,05 en 3/3 runs dans le schéma
  sans position) **et** diffère de `INT` (p < 0,05 en 3/3), **et** en b1 le signal est gardé dans au plus
  5 tirages sur 20 ;
- **dilution réfutée** : en b2, `QPpt` diffère de `Pt` (p < 0,05 en 3/3), **ou** en b1 le signal est
  gardé dans au moins 15 tirages sur 20 ;
- **indéterminée** dans les autres cas.

Les autres tissus et métriques sont rapportés à titre descriptif.

## (a) Témoin d'effectif à 500 lectures, et témoin à ensemble constant

**Question.** En passe 1, le signal caudal en UniFrac pondéré est robuste à 3 000 lectures mais
seulement partiel à 500 (séquentiel 3/3, p 0,022–0,049 ; station bloquée absent). Cet affaiblissement
tient-il à l'effectif, à la profondeur, ou au changement d'ensemble d'échantillons ? À 500 lectures,
davantage d'échantillons passent le seuil : l'ensemble n'est pas le même.

Seule la matrice UniFrac pondérée existe à 500 lectures (`results/rarefaction_d500/`) ; le test porte
donc sur cette métrique seule.

**a1 — témoin d'effectif, tel qu'annoncé.** Script 27 inchangé dans ses modèles, avec la nouvelle
variable `WITNESS_GLOB` pointée sur les matrices à 500 lectures et `WITNESS_OUTDIR` ; 20 tirages,
graine du script. Un tirage « reproduit la passe 1 » si la caudale est significative en 3/3 runs dans le
modèle `ordre_MIN_pos_st_cat`. Règle de lecture :

- au moins 10 tirages sur 20 : le motif de la passe 1 à 500 lectures tient à l'**effectif** ;
- au plus 2 sur 20 : il tient à la **définition** des hybrides ;
- entre les deux : indéterminé.

**a2 — témoin à ensemble constant**, ajouté parce que a1 ne sépare pas profondeur et sélection.
Passe 1, caudale, UniFrac pondéré, trois versions avec les quatre modèles du script 27 :

- (i) 3 000 lectures ;
- (ii) 500 lectures, **restreint aux échantillons présents à 3 000** ;
- (iii) 500 lectures, ensemble complet.

Règle de lecture :

- si (ii) retrouve le motif de (i), soit 3/3 runs dans les deux schémas station bloquée,
  l'affaiblissement tient à l'**ensemble d'échantillons** ;
- si (ii) reste au niveau de (iii), il tient à la **profondeur** ;
- sinon : indéterminé.

## (c) Effet de la catégorie sur la diversité alpha (H1)

**Données.** `results/phylo_diversity/alpha_phylo_mean.tsv`, quatre indices (richesse, Shannon, inverse
Simpson, Faith PD), joints par `dada2_id`. Pour chaque individu et chaque tissu, on prend la moyenne sur
les runs des valeurs strictement positives, comme le script 29, puis le log. Passes 1 et 2.

**Modèles** par tissu × indice, en moindres carrés ordinaires :

- principal (D2 sans position) : `log(x) ~ station + cat` ;
- sensibilité : `log(x) ~ station + pos + cat`.

L'effet de `cat` est testé par un test F emboîté (modèle sans `cat`). Contrastes sur les moyennes
ajustées par station, avec intervalles à 95 % : Hy − Cn, Hy − Pt, et Hy − (Cn + Pt)/2.

**Classement de Hy** par tissu × indice × passe (modèle principal) :

- **intermédiaire** : Hy est compris entre Cn et Pt, et l'intervalle de Hy − (Cn+Pt)/2 contient 0 ;
- **dominant Cn** ou **dominant Pt** : l'intervalle contient 0 pour ce parent et l'exclut pour l'autre ;
- **transgressif** : Hy est hors de [Cn ; Pt], et l'intervalle de l'écart au parent le plus proche
  exclut 0 du côté extérieur ;
- **indéterminé** dans les autres cas.

Un classement est **établi** (règle D7) s'il est le même pour au moins un indice pondéré et au moins un
indice de présence. Les p-valeurs sont brutes, sans correction de multiplicité (4 tissus × 4 indices ×
2 passes), et le texte le dira.

## (d) Partition de la variance alpha (remplace R8)

Pour chaque échantillon (tous les runs), modèle de `log(x)` sur quatre indices, en R de base (`lm`,
pas de modèle mixte faute de lme4 sur meso) :

`log(x) ~ tissue + site_annee + individu + library + run`

- `site_annee` = `site_code` × `annee` ;
- `library` = A pour durance1, B pour durance2 et durance3 ;
- `run` distingue durance2 de durance3 à l'intérieur de B.

On rapporte la part de somme des carrés de chaque terme, en ordre séquentiel (dans l'ordre ci-dessus)
et en marginal (`drop1`), plus la part résiduelle. R8 est remplacé par ce calcul. Le texte dira que la
méthode diffère du diagnostic historique, qui n'est pas reproductible faute de script.
