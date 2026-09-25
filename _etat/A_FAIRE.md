# A_FAIRE — passations par type de session

État au **2026-09-25, 18 h 30**. Sections *Analyse*, *Rédaction* et *Soumission de données* réécrites à la clôture
de la conversation du 25/09 qui a couvert ces trois types ; *Bibliographie* et *Autre* inchangées.
Chaque section est réécrite par la session concernée à sa clôture (cf. `README.md` du dossier).

---

## Analyse

- **Fait le 25/09** : recalcul en deux passes **interprété** — `docs/recalcul/note_recalcul_2passes.md` et
  `correspondance_ancien_nouveau.csv` (chiffres en R21–R25). Reproduction d'août au bit près. `categorie`
  d'`analysis_metadata.csv` **est** la classification de septembre (vérifié : 59/42/79) — point levé.
- **Bloque** : **D7** (métrique de diversité) — tout R² de catégorie reste `préliminaire`.
- **Attendu de JF** : arbitrer D7 ; lire la note §5 — **D2 change des conclusions** (14 cellules sur 32 de la
  Table S8 diffèrent avec/sans position, 8 changent de classe) : décider ce que le texte en affirme.
- **Ouvert** : témoin d'effectif à 500 lectures non lancé (cause de l'affaiblissement caudal en passe 1 non
  établie) ; mécanisme de dilution Pt→Hy `[À CONFIRMER]` ; Faith PD calculé non exploité ; abondance
  différentielle (méthode à choisir).
- **Non commencé** : indice 4H (`HybridMicrobiomes` v0.1.1) — paramètres fixés (D5), dépend de D7 et de
  l'intégration d'`IDX-HYB`.

**Passation.** Le recalcul est fait et rédigé ; rien n'avance sans D7. Lire d'abord `docs/recalcul/note_recalcul_2passes.md`
(§3 ce qui tombe, §5 D2). Prochain calcul utile une fois D7 tranchée : 4H en deux passes.

## Rédaction

- **Fait le 25/09** : §1, §8.6, §8.8, §8.9 réécrits sur 25 chromosomes / deux passes / D2 ; Tables S1, S6–S9,
  *Host identity*, Note S2 ; Figures S1 et S3 régénérées (`docs/manuscrit/figures/`) ; introduction alignée
  (position selon D2, Suran : 2 hybrides à Pont-d'Ain, témoin par retraits aléatoires) ; styles Word corrigés
  (texte courant des §8.8, §8.9, Note S2 en Normal ; titres 8.8–8.9 en Titre 2). Le supplément n'est **plus** à
  régénérer pour les coordonnées ; `DATA_AVAILABILITY.md` n'en porte aucune (vérifié).
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
  Le test wwwdev a échoué (« No new BioSample was created ») ; cause probable une panne du service de test `[À CONFIRMER]`.
- **À faire EN PREMIER** : `cd ena_deposit && bash 9_verifier_hote_sept.sh` — attendu
  `conformes 727 | non conformes 0`. Si oui : R26 → `validé`, retirer la note grise ENA du supplément.
  Si non : ne rien resoumettre, lire `verification_hote_sept_*.txt`.
- **Reste** : affichage public du dépôt ; modèle ENA (2 304 experiments déclarés / 1 536 réels) ; dates de Pertuis
  (déposées en intervalle `2014-07-07/2014-08-20`) ; `host subject id` non unique entre campagnes (24 paires) —
  table `ena_corrections_subject_id.tsv` prête, non soumise, décision JF.
- **Recette à ne pas re-découvrir** : le FTP Webin est inutilisable, passer par `webin-cli -ascp` en appelant le
  conteneur directement (cf. notes du cluster et `ena_deposit/GUIDE_depot_ENA.md`). Les MODIFY passent par
  `curl` sur le drop-box, identifiants lus au clavier (jamais écrits) : un humain lance le script.

**Passation.** Une seule action en attente : lancer `9_verifier_hote_sept.sh`. Lire d'abord
`ena_deposit/MEMO_correction_hote_sept.md`. Le rappel `A_FAIRE_prochaine_session.md` de la racine est absorbé ici.

## Autre (données d'André, hygiène du dépôt)

- **Attendu d'André**, trois points (détail dans `docs/pour_andre_questions_ouvertes.md`) :
  (1) provenance de la médiane et du D des 5 individus sans foie — cellules à vider ou à
  documenter avant publication du supplément ; (2) les trois sections de protocole ci-dessus ;
  (3) les dates de pêche de Pertuis.
- **Hygiène à faire, sans urgence** :
  `CLAUDE.md` est périmé (état de juillet, annonce « analyse écologique pas commencée ») ;
  33 fichiers de sortie traînent à la racine du projet en doublon de `results/` ;
  0,97 Go de tables ASV redondantes à archiver (cf. `DONNEES.md`) ;
  `results/fastqc_durance{1,2,3}_*` (4 668 fichiers, 3,1 Go) et
  `ena_deposit/webin_out_{test,prod}` (46 076 fichiers) sont archivables.
- **Attention** : le dépôt est **modifié en parallèle par d'autres sessions** — le 25/09 à 17 h
  `runs.log` a été commité pendant cette session. Toujours `git pull`/vérifier
  `git status` avant d'écrire, et ne jamais réécrire un fichier de `_etat/` sans l'avoir relu.
