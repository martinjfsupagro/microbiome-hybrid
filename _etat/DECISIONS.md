# DECISIONS — journal antichronologique

Index daté. Le raisonnement complet vit dans `docs/decision_*.md` et les messages de commit ;
ce fichier ne recopie pas, il pointe. Les entrées marquées **rétro** ont été reconstituées
depuis les scripts et le `git log` : la décision est certaine, sa date est approchée.

---

## 2026-10-05 — Texte principal resserré (≈ 8 000 mots), détails techniques en Note S2
- **Décision** (choix de JF) : cible ≈ 8 000 mots ; détails techniques déplacés dans le supplément ; livraison dans un fichier séparé, `Article.docx` restant la référence jusqu'à validation. Résultat : 10 677 → 7 904 mots (Background 1 449 → 1 053, Methods 5 261 → 3 298, Results 2 808 → 2 493, Discussion 1 047 → 948 ; Abstract, figures, légendes, références inchangés). 25 paragraphes de Methods déplacés **verbatim** dans une nouvelle Note S2 ; ancienne Note S2 → Note S3, désormais citée au §9 ; Note S1 citée dès le §3. Sous-titres 5.1–5.5 supprimés, numérotation 1–9 / 8.1–8.12 conservée.
- **Contrôles** : 64 chaînes du script 40 toutes présentes dans le texte principal ; aucun nombre à ≥ 2 chiffres des paragraphes modifiés absent à la fois de l'article et du supplément ; script 40 sur `Article_resserre.docx` 65/65 ; script 30 41/44 (inchangé, indépendant du docx).
- **Retraits à valider par JF** (liste complète dans `docs/manuscrit/journal_resserrement_2026-10-05.md`) : phrase « The choice of a differential-abundance method remains to be fixed. » (note grise) ; référence interne des deux stations du Suran (Background, non exploitée en Results) ; détails de littérature ; historique du témoin mono-catégorie ; ouverture « not as a result of it » (note grise levée).
- **Défauts préexistants corrigés dans le supplément** : renvois « §8.7 » (Note S1, Table S5) et « (§8.6, §8.8) » (Table S9) hérités de l'ancienne numérotation ; ancienne Note S2 jamais citée dans l'article.
- **Session** : Rédaction. Réf. `scripts/42-resserrement_article.py`, `scripts/40-verif_article_v2.py`, `docs/manuscrit/Article_resserre.docx` (`965b24f60fc9f4b1445f69e74cfeb759`), `Supplementary_Data_resserre.docx` (`4e38874db427458aa184608347c92723`).

## 2026-10-05 — Tables supplémentaires renumérotées dans l'ordre de citation ; deux paragraphes périmés retirés de l'article
- **Décision** : tables S renumérotées selon leur première citation dans l'article et déplacées en conséquence dans le supplément. Correspondance **ancien → nouveau** : S1→S1, S2→S2, **S5→S3** (runs et réplication), **S3→S4** (composition de la soumission ENA), **S6→S5** (convergence Monte-Carlo), **S8→S6** (concordance des métriques selon la profondeur), **S4→S7** (accessions des runs), **S7→S8** (effet de position), S9→S9, S10→S10. L'ancienne S6 n'était citée nulle part dans l'article : appel ajouté au §8.6 (« Convergence values are given in Supplementary Table S5 »). Les figures S ne sont **pas** renumérotées (S2 est citée avant S1) : non demandé, signalé.
- **Erreur de l'agent, corrigée** : les deux anciens paragraphes de dispersion (PERMDISP non corrigé : 32/48 et 34/48, 45/68 intra-station, dispersion hétérogène en caudale ; 492 mots) étaient restés dans les Methods après le §8.12 depuis la restructuration du 03/10 (commits `754f383` et `265a66e`). Le script de restructuration les recopiait en Results sans les retirer ; le script 40 ne contrôlait que la présence des bons chiffres. Paragraphes supprimés ; contrôles d'absence et d'ordre des tables ajoutés au script 40 (ils échouent sur la version précédente, passent sur la nouvelle).
- **Impact** : les notes et documents antérieurs au 05/10 (`docs/recalcul/*`, entrées de ce journal) gardent l'ancienne numérotation : se reporter à cette correspondance.
- **Session** : Rédaction. Réf. `docs/manuscrit/Article.docx` (`68caaeb7c55ec2716a7fa36010d898dd`), `Supplementary_Data.docx` (`3b6f95e4f6ac72b5dc773f53c061d483`), `scripts/40-verif_article_v2.py`.

## 2026-10-05 — Supplément : Table S10 et Figure S3 régénérées sur PERMDISP corrigé
- **Décision** : Table S10 (32 lignes) et Figure S3 recalculées depuis `results/recat/{1,2}/permdisp_bias/` ; libellés de la table traduits en anglais (« caudale », « UniFrac non pondéré » → termes du texte principal) ; Figure S3 recolorée avec la palette des figures principales (l'ancienne colorait les hybrides en orange, couleur de *P. toxostoma* dans l'article) ; titres de panneaux recalculés sur les données corrigées.
- **Raison** : R34 (2026-10-03) ; le supplément portait encore les valeurs non corrigées. Le code d'origine de la Table S10 n'avait pas été conservé : agrégation reconstruite et validée contre l'ancienne table (32/32 lignes reproduites à partir des sorties non corrigées).
- **Impact** : 12 cellules « station bloquée », 9 « intra-station », 6 « Hy most dispersed » changent (caudale passe 1 : Bray-Curtis, Jaccard et UniFrac non pondéré 3/3 → 0/3 ; UniFrac pondéré 0/3 → 1/3). Note de la table et légende S3 mises à jour ; note grise de l'article actualisée.
- **Session** : Rédaction. Réf. `scripts/41-supp_S10_S3.py`, `docs/plan_permdisp_biais_2026-10-03.md`.

## 2026-10-03 (soir) — Article restructuré pour Animal Microbiome ; références numérotées
- **Décision** : Abstract structuré (306 mots) et mots-clés ; Background / Methods (méthodes seules) / Results / Discussion / Conclusions / Abbreviations / Declarations / References / Figure legends ; résultats des anciens §8.7–8.9 déplacés en Results avec leur mise en forme ; nouveaux §8.7 (cadre statistique), §8.10 (alpha), §8.11 (4H), §8.12 (contrôles pré-déclarés) ; 51 références numérotées dans l'ordre de citation, dont 15 notices logicielles ou manquantes ajoutées depuis Crossref (DADA2, SILVA, cutadapt, QIIME 2, MAFFT, FastTree 2, UniFrac, Faith, PERMANOVA, PERMDISP, Stier et al. 2013, phyloseq, vegan, HybridMicrobiomes ; Kozich 2013, Small 2019 et Sevellec 2019 en version publiée) ; cinq figures principales.
- **Raison** : choix de JF du 03/10 (installer et calculer le 4H, Methods = méthodes seules, 4–5 figures). Contrat de la revue : section Declarations complète, références numérotées.
- **Impact** : contrôle chiffré `scripts/40-verif_article_v2.py` 59/59 ; `scripts/30-verif_article.py` 41/44 (2 attentes périmées du script 30, 1 écart de métadonnées préexistant, cf. A_FAIRE). Contraste femelles/mâles (R27) non rapporté tant que le code « X » n'est pas confirmé. Ordre de première citation des tables S toujours non croissant.
- **Session** : Rédaction. Réf. `docs/manuscrit/Article.docx` (md5 `5bbfdb78501626a507d4b63ca78660f9`).

## 2026-10-03 (soir) — PERMDISP : correction de petit effectif adoptée, R15/R25 remplacés
- **Décision** : `bias.adjust = TRUE` devient la version de référence de PERMDISP ; les sorties non corrigées sont conservées pour comparaison.
- **Raison** : sans correction, `betadisper` sous-estime la distance au centre des petits groupes, et les hybrides sont la plus petite catégorie de chaque strate. Le biais va dans le sens du résultat rapporté (« hybrides moins dispersés »). Défaut de l'analyse antérieure de l'agent, trouvé en rédigeant la Discussion.
- **Impact** : R34 remplace R15/R25 ; paragraphes Dispersion et Figure 4 réécrits ; Table S10 et Figure S3 du supplément à régénérer.
- **Session** : Analyse. Réf. `docs/plan_permdisp_biais_2026-10-03.md`, scripts 24 (`ecef636`) et 39 (`ec5e318`).

## 2026-10-03 (soir) — Indice 4H : profondeur, effectif et règles de lecture fixés avant calcul
- **Décision** (technique, prise par l'agent dans le cadre de D4–D6, **à valider par JF**) : raréfaction 4H à **1 000 lectures assignées au genre** (1 749/1 784 échantillons) ; N = plus petite classe de la passe 1 − 1, commun aux deux passes ; 500 bootstraps ; version Bray-Curtis, pré-analyse, plan nul et hybride nul ; règles de lecture 1–7 ; `FourHcompare` non utilisé (p dépendant du nombre de bootstraps).
- **Raison** : le package raréfie la table agrégée ; à 3 000 lectures assignées, trois tissus de la passe 1 tombaient sous 10 hybrides (abandon D6). Camper et al. : axe parental stable à ± 0,067 entre 1 000 et 10 000 lectures.
- **Impact** : R33. Couverture au genre 64,1 % des lectures, déclarée.
- **Session** : Analyse. Réf. `docs/plan_4H_2026-10-03.md` (`6372af6`), `docs/recalcul/note_4H_2026-10-03.md`.

## 2026-10-03 — Article : règle D7 restaurée, §8.8 et §8.9 alignés sur les tests du jour
- **Décision** :
  - restaurer **mot pour mot** au §8.6 les cinq phrases de la règle D7, depuis le commit `c2c1171` ;
  - corriger au §8.8 la phrase sur le chargement des plaques ;
  - préciser au §8.9 l'affaiblissement caudal à 500 lectures (R29).
  
  La reformulation du mécanisme de l'effet de colonne au §8.8 (« the delay between capture and dissection ») attend l'arbitrage D2 et reste signalée par une note grise.
- **Raison** : la règle D7, écrite le 30/09 à 17 h 24 (`c2c1171`), a disparu au commit suivant (`f2dd265`, 17 h 36), où le paragraphe « Statistical framework » a été repris d'une version antérieure. C'est la seule perte entre ces deux commits. Les registres affirmaient depuis que la règle figurait au §8.6. Les deux phrases du §8.8 et du §8.9 étaient contredites par R32 et R29.
- **Impact** : le §8.6 porte de nouveau la règle D7 (texte bleu). Le §8.8 indique que la plaque suit l'ordre de traitement dans **chaque** campagne (ρ 0,55–0,95). Le §8.9 attribue l'affaiblissement à 500 lectures à l'ensemble d'échantillons, non à la profondeur.
- **Session** : Rédaction. Réf. `RESULTATS.md` R29, R32 ; `docs/recalcul/note_tests_2026-10-03.md`.

## 2026-10-03 — D2 suspendue ; test du séjour en vivier déclaré a priori
- **Décision** : JF suspend D2 (option d de la question 2.1) jusqu'au résultat d'un test validé a priori (2.2). On compare, aux quatre stations où colonne de plaque et ordre de dissection se découplent, un modèle avec la colonne et un modèle avec le rang de dissection. La règle de lecture est écrite avant calcul.
- **Raison** : André, 2026-10-03 : poissons gardés vivants en vivier jusqu'à la dissection (4–6 min par poisson, ordre fixe). Le délai post-mortem est court et constant, alors que la durée de séjour (de quelques minutes à environ 2 h, hotus d'abord) est confondue avec la catégorie, et avec la colonne à cinq stations sur neuf (ρ 0,87–0,95). L'effet de position R14 pourrait donc être en partie un effet de séjour : hypothèse non testée.
- **Impact** : §8.8–8.9 non réécrits avant le résultat. Cinq tests lancés (2.3), dont (c) et (d) redéfinis sur deux défauts du registre : R8 sans script (diagnostic de conversation, attribué à tort au script 14), et Faith PD déjà exploité dans R27.
- **Session** : Analyse. Réf. `docs/plan_tests_2026-10-03.md`, `docs/reponses_JF_2026-10-03.md`, `docs/reponses_andre_2026-10-03.md`.

## 2026-10-03 — Manuscrit : cible Animal Microbiome, titre provisoire, Table S2, Funding
- **Décision** :
  - cible **Animal Microbiome**, à revérifier en fin d'écriture ; le manuscrit est construit pour cette revue ;
  - titre provisoire = sous-titre du supplément ;
  - table de génotypage individuel insérée en **Table S2**, les Tables S2–S9 devenant S3–S10 ;
  - Funding : contrat de thèse EDF-CNRS **AGDI 428481** (André) ;
  - lien vers le dépôt GitHub public au §9 ;
  - abondance différentielle reportée.
- **Raison** : réponses de JF aux questions 2.4 à 2.9 et 2.13.
- **Impact** : les registres et notes qui citent les Tables S8 et S9 (Table S8 de la D2, Table S9 du PERMDISP) renvoient désormais aux Tables **S9** et **S10**. Le rattachement de la thèse d'A. Ungaro au contrat FACIES reste sans confirmation explicite. Le miroir GitHub public s'arrêtait au 2026-09-25 ; il est à synchroniser.
- **Session** : Rédaction. Réf. `docs/reponses_JF_2026-10-03.md`.

## 2026-10-03 — ENA : une seule soumission pour Pertuis et host subject id ; pas de restructuration
- **Décision** : JF accepte de soumettre en une seule fois les dates de Pertuis (44) et le `host subject id` préfixé par la campagne (727 lignes). Le modèle à 2 304 experiments est conservé pour l'instant. Le dépôt sera ouvert à la soumission de l'article.
- **Impact** : la soumission reste à lancer par un humain (identifiants Webin au clavier). Après soumission, ajouter les deux tables en fin de liste de `7_verifier_exhaustif.sh`, puis mettre à jour le §9 et la Note S2.
- **Session** : Soumission de données. Réf. `ena_deposit/MEMO_corrections_restantes.md`.

## 2026-09-30 — Vérification du dépôt ENA : chaîner **toutes** les tables de correction soumises, pas la dernière
- **Décision** : `ena_deposit/7_verifier_exhaustif.sh` construit l'état attendu en appliquant successivement **toutes** les tables de correction déjà soumises, dans l'ordre chronologique (`ena_corrections.tsv` puis `ena_corrections_hote_sept.tsv`), et contrôle la cohérence du chaînage : si une table part d'un état que la précédente ne produit pas, il le signale au lieu de comparer. Règle inscrite en tête du script : **ne lister que les tables effectivement soumises** — y mettre une table préparée mais non soumise produirait de faux écarts. Le script couvre les sept champs corrigés, `TITLE` compris, qui n'est pas un attribut d'échantillon mais un élément du XML et échappait à la version d'août.
- **Raison** : La version d'août ne comparait le dépôt qu'à la table d'août. Relancée le 30/09 après la campagne du 25/09, elle a signalé **59 champs « non conformes » qui étaient corrects** : les valeurs de septembre, correctement appliquées. Le dépôt était juste, le vérificateur périmé. Les 59 sont exactement les recouvrements entre les deux tables — 63 noms scientifiques changés en septembre, dont 59 déjà corrigés en août ; les 4 autres partaient de la valeur d'origine du dépôt et n'étaient donc pas attendus par l'ancien script.
- **Impact** : R28 ajouté : **4 612 champs conformes sur 4 612**, 727 échantillons, 0 écart, 0 rupture de chaînage. R20 (5 attributs) et R26 (identité d'hôte) sont désormais couverts par une seule vérification. Contrôle négatif : en inversant l'ordre des tables, le script détecte 59 ruptures, exactement le nombre de recouvrements. Si les tables Pertuis et `host subject id` sont soumises, **il faudra les ajouter en fin de liste** de tables chaînées.
- **Session** : Soumission de données Réf. `ena_deposit/7_verifier_exhaustif.sh`, `ena_deposit/verification_cumulee_20260930_2019.txt`, `ena_deposit/verification_exhaustive_20260930_1811.txt (trace de la fausse alerte)`.

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

## 2026-09-30 — D7 : métrique de diversité, **TRANCHÉE**
- **Décision** : pas de métrique unique. Les quatre métriques sont rapportées partout ; un
  résultat n'est énoncé comme établi que s'il est soutenu par au moins une métrique pondérée par
  l'abondance **et** une métrique de présence, sinon il est rapporté comme dépendant de la
  métrique en nommant laquelle. Chiffres du texte courant : Shannon en alpha, Bray-Curtis en
  composition. Validée par JF le 2026-09-30.
- **Raison** : l'instruction chiffrée (R27) montre que le clivage pondéré/non pondéré n'est pas
  le même axe en alpha et en composition — Bray-Curtis, pourtant pondéré, se comporte comme
  Jaccard et l'UniFrac pondéré est isolé. Une règle « ne garder que les métriques pondérées »
  supprimerait le résultat digestif et ne conserverait que la métrique atypique.
- **Impact** : les statuts `préliminaire (D7)` de `RESULTATS.md` sont levés pour les résultats
  déjà calculés sur les quatre métriques ; R8 reste préliminaire (richesse seule, non refait) ;
  le contraste midgut/hindgut et l'inversion du dimorphisme sexuel sont retirés de
  `note_guivier2017_implications.md` ; la règle est écrite au §8.6 de `Article.docx` (commit `c2c1171`) — *perdue douze minutes plus tard au commit `f2dd265`, restaurée mot pour mot le 2026-10-03 (entrée du 2026-10-03)*.
- **Session** : Analyse + Rédaction. Réf. `docs/decision_D7_metrique.md`, `scripts/29-d7_metriques.py`.

## 2026-09-25 — D7 : métrique de diversité, **NON TRANCHÉE** *(remplacée par l'entrée du 2026-09-30)*
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
