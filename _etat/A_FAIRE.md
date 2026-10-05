# A_FAIRE — passations par type de session

État au **2026-10-05** (Table S10 / Figure S3 régénérées) ; avant cela, **2026-10-03, nuit**. Sections *Analyse* et *Rédaction* réécrites à la clôture de la session du 03/10 soir (4H, PERMDISP corrigé, article restructuré) ; *Bibliographie*, *Soumission de données* et *Autre* inchangées depuis le 03/10 soir.
Chaque section est réécrite par la session concernée à sa clôture (cf. `README.md` du dossier).

---

## Analyse

- **Fait le 03/10 (soir)** : HybridMicrobiomes 0.1.1 installé (`~/bin/envs/hm4h`, recette dans les notes meso) ; **indice 4H** pré-déclaré (`docs/plan_4H_2026-10-03.md`, `6372af6`) puis calculé et lu mécaniquement (scripts 37–38) → R33 : aucun axe transgressif robuste ; axe parental robuste en branchie (passe 2) ; rétention des taxons partagés partout.
- **Défaut de l'analyse antérieure, corrigé** : PERMDISP sans `bias.adjust` (R15/R25). Reprise pré-déclarée (`docs/plan_permdisp_biais_2026-10-03.md`) → R34 : « hybrides moins dispersés » ne tient qu'en station bloquée (passe 1 de justesse, 22/48) ; retiré en intra-station.
- **Signalé, non traité** : `metadata/analysis_metadata.csv` a 2 181 lignes contre 2 180 échantillons dans `ASV-CLEAN` (ligne en trop `15Bue1014Ch03A__durance3`, script 30) ; préexistant, à expliquer.
- **Attendu de JF** : D2 (inchangé) ; validation des choix techniques du 4H (1 000 lectures assignées au genre, N commun).
- **Ouvert** : abondance différentielle (reportée) ; mécanismes R22/R29/R30 `[À CONFIRMER]` ; R31 possiblement confondu avec l'ordre de traitement, non testé ; Table S10 et Figure S3 : fait le 2026-10-05 (script 41).

**Passation.** 4H et PERMDISP corrigé sont faits et lus ; Table S10 et Figure S3 régénérées (05/10, script 41). Rien de calculé en attente hors arbitrages de JF (D2, choix 4H). Lire d'abord `docs/recalcul/note_4H_2026-10-03.md`.

## Rédaction

- **Fait le 03/10 (soir)** : `Article.docx` restructuré pour Animal Microbiome (Abstract 306 mots, Background, Methods = méthodes seules, Results, Discussion, Conclusions, Abbreviations, Declarations, 51 références numérotées, légendes) ; cinq figures dans `docs/manuscrit/figures/` ; dispersion réécrite d'après R34 ; contrôle chiffré **59/59** (`scripts/40-verif_article_v2.py`), script 30 41/44 (2 attentes périmées du script 30, 1 écart de métadonnées préexistant).
- **Notes grises à lever** : autorisations Ain/Ardèche, euthanasie, température du tube (André) ; Competing interests, Authors' contributions, Acknowledgements ; DOI Zenodo ; FACIES ; Sinama 2013 (deux notices possibles) ; « not as a result of it » (paragraphe venu des Methods) ; mécanisme de l'effet de colonne (D2) ; code de sexe « X ».
- **Défauts connus** : ordre de première citation des tables S non croissant (S1, S2, S5, S3, S8, S10, S4, S7, S9) ; revues non abrégées (NLM) ; texte principal ≈ 12 500 mots, à resserrer.
- **Bloque** : D2 (JF) pour la phrase sur le mécanisme de l'effet de colonne.

**Passation.** L'article a sa structure complète. Prochaine étape : JF relit Results et Discussion ; puis ordre des tables S (S10 et S3 faits le 05/10). Fichier : `docs/manuscrit/Article.docx` (md5 `01461e48e5f395cd795801e2189d0690`), texte nouveau en bleu.

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

- **État** : PRJEB124417 vérifié (R28, 4 612/4 612), en ligne, non public.
- **Décidé par JF le 03/10** : soumettre **en une seule fois** les dates de Pertuis (`ENA-PERT`, 44) et le `host subject id` préfixé par la campagne (`ENA-SUBJ`, 727) ; **pas de restructuration** des 2 304 experiments pour l'instant ; ouverture publique **à la soumission de l'article**.
- **À faire, par un humain** (identifiants Webin au clavier) : la soumission, selon la ligne de commande testée de `ena_deposit/MEMO_corrections_restantes.md` ; puis ajouter les deux tables **en fin de liste** de `7_verifier_exhaustif.sh` et revérifier ; puis mettre à jour le §9 et la Note S2.
- **Recette à ne pas re-découvrir** : FTP Webin inutilisable, `webin-cli -ascp` en appelant le conteneur ; MODIFY par `curl` ; un reçu vide n'est pas un échec (`6_etat_du_depot.sh` avant toute relance).
- **Leçon du 30/09, toujours valable** : ne jamais écrire dans `docs/manuscrit/` depuis une session Soumission.

**Passation.** Rien à calculer : une soumission MODIFY à lancer par JF, déjà construite et testée. Lire `ena_deposit/MEMO_corrections_restantes.md`, puis `DECISIONS.md` du 03/10.

## Autre (données d'André, hygiène du dépôt)

- **Réponses d'André du 03/10** consignées mot pour mot dans `docs/reponses_andre_2026-10-03.md` : autorisations 2014-156-0001 et 2015-1426DDT605 (ONEMA, DDT 04, 05 et 84), même protocole de dissection pour les quatre tissus, tissu 01 = lobe de nageoire caudale, protocole de laboratoire identique à Guivier et al. 2017, témoins retrouvés dans les plaques, origine de la fuite de mock non récupérable, vivier et durées de dissection, contrat EDF-CNRS AGDI 428481.
- **Attendu d'André** (questions de suivi transmises par JF le 03/10) : couverture des stations de l'**Ain** et de l'**Ardèche** par une autorisation DDT ; euthanasie par dislocation cervicale juste avant chaque dissection ; température de conservation du tube en éthanol. Plus, en fin d'écriture, les remerciements.
- **Réponses de JF du 03/10** : `docs/reponses_JF_2026-10-03.md`.
- **Dépôt GitHub public** (JF) : le miroir s'arrêtait au 25/09 (`72666a3`) ; le manuscrit et les notes internes y deviennent publics à chaque synchronisation.
- **Hygiène, sans urgence** : `CLAUDE.md` périmé ; 33 fichiers en doublon à la racine ; 0,97 Go de tables ASV redondantes ; `results/fastqc_durance*` et `ena_deposit/webin_out_*` archivables. `metadata/index_hybride_andre.csv` est décrit « 0 = hotu → 1 = toxostome » dans `DONNEES.md`, alors que l'index de `analysis_metadata.csv` vaut 0,9999 pour les Cn : sens à vérifier avant toute intégration (`IDX-HYB`) `[À CONFIRMER]`.
- **Attention** : dépôt modifié en parallèle par d'autres sessions ; `git status` et relecture avant toute écriture dans `_etat/`.

