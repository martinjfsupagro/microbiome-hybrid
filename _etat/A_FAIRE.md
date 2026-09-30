# A_FAIRE — passations par type de session

État au **2026-09-25, 18 h 45**. Sections *Analyse*, *Rédaction* et *Soumission de données* réécrites à la clôture
de la conversation du 25/09 qui a couvert ces trois types ; *Soumission de données* réécrite à nouveau le 25/09 à
18 h 45, après la vérification du dépôt ; *Bibliographie* et *Autre* inchangées.
Chaque section est réécrite par la session concernée à sa clôture (cf. `README.md` du dossier).

---

## Analyse

- **Fait le 25/09** : recalcul en deux passes **interprété** — `docs/recalcul/note_recalcul_2passes.md` et
  `correspondance_ancien_nouveau.csv` (chiffres en R21–R25). Reproduction d'août au bit près. `categorie`
  d'`analysis_metadata.csv` **est** la classification de septembre (vérifié : 59/42/79) — point levé.
- **D7 tranchée le 30/09** : règle du quatuor déclaré, un résultat n'est établi que s'il est
  soutenu par au moins une métrique pondérée et une métrique de présence (R27,
  `docs/decision_D7_metrique.md`). Les statuts `préliminaire (D7)` sont levés dans `RESULTATS.md`
  pour les résultats déjà calculés sur les quatre métriques.
- **Attendu de JF** : arbitrer D7 ; lire la note §5 — **D2 change des conclusions** (14 cellules sur 32 de la
  Table S8 diffèrent avec/sans position, 8 changent de classe) : décider ce que le texte en affirme.
- **Ouvert** : témoin d'effectif à 500 lectures non lancé (cause de l'affaiblissement caudal en passe 1 non
  établie) ; mécanisme de dilution Pt→Hy `[À CONFIRMER]` ; Faith PD calculé non exploité ; abondance
  différentielle (méthode à choisir).
- **Non commencé** : indice 4H (`HybridMicrobiomes` v0.1.1) — paramètres fixés (D5), dépend de D7 et de
  l'intégration d'`IDX-HYB`.

**Passation.** D7 est tranchée, le verrou est levé. **Le prochain calcul utile est l'indice 4H en deux
passes** (paramètres figés par D5). Reste à arbitrer côté JF : D2, ce que le texte affirme de l'effet de
position (note §5). Lire d'abord `docs/decision_D7_metrique.md`, puis `docs/recalcul/note_recalcul_2passes.md`.

## Rédaction

- **Fait le 25/09** : §1, §8.6, §8.8, §8.9 réécrits sur 25 chromosomes / deux passes / D2 ; Tables S1, S6–S9,
  *Host identity*, Note S2 ; Figures S1 et S3 régénérées (`docs/manuscrit/figures/`) ; introduction alignée
  (position selon D2, Suran : 2 hybrides à Pont-d'Ain, témoin par retraits aléatoires) ; styles Word corrigés
  (texte courant des §8.8, §8.9, Note S2 en Normal ; titres 8.8–8.9 en Titre 2). Le supplément n'est **plus** à
  régénérer pour les coordonnées : Table S1 comparée le 25/09 à `station_reference.csv`, 9/9 stations conformes
  (coordonnées, rivière, dates) ; `DATA_AVAILABILITY.md` ne porte aucune coordonnée ni rivière (grep, 25/09).
- **Erreurs à corriger dans la note grise de l'introduction** (écrites le 25/09 par cette session) :
  (iv) dit les paramètres 4H « pas encore fixés » — ils le sont (D5) ; ce qui manque est leur description au §8.6.
  (v) dit l'introgression « sur un seul chromosome » invérifiable — R16 l'établit pour 17 des 22 quasi-purs ;
  l'intro l'affirme pour tous → reformuler `[À CONFIRMER]` contre `docs/synthese_genotypage_25chr.md`.
- **Bloque** : D7 pour figer les chiffres ; André pour §2, §3, §4 (protocoles transposés de 2017).
- **Avant soumission** : retirer le **bleu** du texte ajouté ; titre d'article absent (note i) ; refs Wang 2015 et
  Sevellec (ii–iii) ; retirer la note grise ENA sous *Host identity* **après** vérification (Soumission).
- **Ouvert** : ordre de l'introduction ; cible éditoriale (`docs/manuscrit_animal_microbiome/`) `[À CONFIRMER]`.

**Passation.** Les Methods reflètent l'état des analyses au 25/09. Commencer par corriger les points (iv) et (v)
de la note grise de l'introduction, puis attendre D7. Fichier : `docs/manuscrit/Article.docx` (lire depuis le cluster).

## Bibliographie

- **Prêt à consommer** : `docs/biblio/microbiome_hybrid_all_refs.bib` — 223 notices, champs
  `author` reconstruits le 25/09 et validés contre Crossref sur 40 DOI. C'est le fichier qui
  fait foi ; les autres `.bib` du dossier sont thématiques (`hybrid_microbiome_refs`,
  `fish_microbiome_key_refs`, `batch_effect_sota`, `rarefaction_sota`).
- **Ouvert** : trois références sans DOI (dépôts institutionnels non résolus) ;
  texte intégral du cadre 4H (DOI `10.1111/2041-210x.14279`) non récupéré — nécessaire pour
  valider la formule de l'indice sur un index continu.
- **Attendu de la Rédaction** : rien en attente ; la biblio suit la rédaction.

## Soumission de données

- **État** : PRJEB124417 soumis (768 échantillons, 2 304 runs). Métadonnées corrigées le 31/08 (727/727 vérifiés),
  puis **identité d'hôte corrigée le 25/09 à 18:08** : 568 échantillons, 1 199 champs (titre, nom scientifique,
  nom commun ; hybrides `nasus x toxostoma`) — reçu success=true, 568/568 accessions identiques.
  Le test wwwdev a échoué (« No new BioSample was created ») ; cause probable une panne du service de test `[À CONFIRMER]`
  — sans conséquence pour le dépôt, la production ayant été vérifiée depuis.
- **Fait le 25/09 à 18:38** : vérification exhaustive du dépôt (`9_verifier_hote_sept.sh`, 8 lots) —
  **727 échantillons interrogés, 1 199 champs conformes, 0 non conforme, 0 introuvable** (TITLE 568,
  host common name 568, host scientific name 63). Rapport `ena_deposit/verification_hote_sept_20260925_1838.txt`.
  Conséquences appliquées : **R26 → `validé`** et **note grise ENA retirée** de `Supplementary_Data.docx` sous *Host identity*.
- **Reste** : affichage public du dépôt ; modèle ENA (2 304 experiments déclarés / 1 536 réels) ; dates de Pertuis
  (déposées en intervalle `2014-07-07/2014-08-20`) ; `host subject id` non unique entre campagnes (24 paires) —
  table `ena_corrections_subject_id.tsv` prête, non soumise, décision JF.
- **Recette à ne pas re-découvrir** : le FTP Webin est inutilisable, passer par `webin-cli -ascp` en appelant le
  conteneur directement (cf. notes du cluster et `ena_deposit/GUIDE_depot_ENA.md`). Les MODIFY passent par
  `curl` sur le drop-box, identifiants lus au clavier (jamais écrits) : un humain lance le script.

**Passation.** L'identité d'hôte est close : dépôt vérifié (727/727, 0 écart), R26 validé, note grise retirée du supplément.
Plus rien n'est en attente d'exécution côté soumission ; les quatre points de « Reste » attendent une décision, pas un calcul,
et le plus mûr est `host subject id` (24 paires, `ena_corrections_subject_id.tsv` prête, décision JF).
Lire d'abord `ena_deposit/MEMO_correction_hote_sept.md`, puis le rapport de vérification.
Le rappel `A_FAIRE_prochaine_session.md` de la racine est absorbé ici.

## Autre (données d'André, hygiène du dépôt)

- **Réponses d'André reçues le 30/09** — les trois points sont traités :
  (1) les 5 individus sans foie : trois ajustés sur midgut et caudale, concordants (`Pt` par les
  deux voies, D de 0,0104 à 0,0577 contre un seuil à 0,12) ; deux sans trace de Q-values, médiane
  et D passés à **NA** sur décision d'André. Les valeurs actuelles du tableau pour les trois
  premiers ne correspondent à aucun des deux ajustements et leur provenance reste inconnue ;
  **arbitrage rendu par JF le 30/09** : publier les deux ajustements en nommant le tissu, ne pas
  publier les valeurs du tableau. Appliqué dans `docs/manuscrit/table_genotypes_individuels.csv`
  (180 lignes) ; numérotation de la table et insertion dans le supplément à la charge de la
  Rédaction. Détail dans `docs/decision_individus_sans_qvalues.md`. Portée analytique nulle (`index_mediane_andre` n'est
  consommé par aucun script).
  (2) protocoles : **seul le financement est réglé** — même contrat qu'en 2017, EDF via FACIES avec
  l'appui de la Fédération de l'Ain ; section *Funding* ajoutée à `Article.docx`. Les §2, §3 et §4
  restent transposés et non confirmés.
  (3) dates de Pertuis : série 1011-1014 le 07/07/2014, série 2011-2015 le 20/08/2014 — confirme ce
  que `decision_stations.md` §5 portait déjà. Table `ena_deposit/ena_corrections_pertuis_dates.tsv`
  prête (44 échantillons), **non soumise**, MODIFY à lancer par un humain.
  **Attention** : la question 3 était double ; son « oui » ne couvre pas les séries 1036+ de l'Ain
  et d'Avignon, qui s'expliquent par des chevesnes intercalés dans la numérotation et gardent leur
  date unique.
- **Attendu d'André**, ce qui reste : les trois sections de protocole (§2, §3, §4), le délai entre
  capture et dissection avec l'ordre de prélèvement des tissus, et la référence exacte du contrat
  EDF avec le nom légal de la Fédération.
- **Hygiène à faire, sans urgence** :
  `CLAUDE.md` est périmé (état de juillet, annonce « analyse écologique pas commencée ») ;
  33 fichiers de sortie traînent à la racine du projet en doublon de `results/` ;
  0,97 Go de tables ASV redondantes à archiver (cf. `DONNEES.md`) ;
  `results/fastqc_durance{1,2,3}_*` (4 668 fichiers, 3,1 Go) et
  `ena_deposit/webin_out_{test,prod}` (46 076 fichiers) sont archivables.
- **Attention** : le dépôt est **modifié en parallèle par d'autres sessions** — le 25/09 à 17 h
  `runs.log` a été commité pendant cette session. Toujours `git pull`/vérifier
  `git status` avant d'écrire, et ne jamais réécrire un fichier de `_etat/` sans l'avoir relu.
