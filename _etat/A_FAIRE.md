# A_FAIRE — passations par type de session

État au **2026-10-05** (Table S10 / Figure S3 régénérées ; tables S renumérotées ; texte principal resserré dans `Article_resserre.docx` ; corrections mécaniques sur les deux versions ; liste « sans décision » exécutée le soir) ; avant cela, **2026-10-03, nuit**. Sections *Analyse* et *Rédaction* réécrites à la clôture de la session du 03/10 soir (4H, PERMDISP corrigé, article restructuré) ; *Bibliographie*, *Soumission de données* et *Autre* inchangées depuis le 03/10 soir.
Chaque section est réécrite par la session concernée à sa clôture (cf. `README.md` du dossier).

---

## Analyse

- **Fait le 03/10 (soir)** : HybridMicrobiomes 0.1.1 installé (`~/bin/envs/hm4h`, recette dans les notes meso) ; **indice 4H** pré-déclaré (`docs/plan_4H_2026-10-03.md`, `6372af6`) puis calculé et lu mécaniquement (scripts 37–38) → R33 : aucun axe transgressif robuste ; axe parental robuste en branchie (passe 2) ; rétention des taxons partagés partout.
- **Défaut de l'analyse antérieure, corrigé** : PERMDISP sans `bias.adjust` (R15/R25). Reprise pré-déclarée (`docs/plan_permdisp_biais_2026-10-03.md`) → R34 : « hybrides moins dispersés » ne tient qu'en station bloquée (passe 1 de justesse, 22/48) ; retiré en intra-station.
- **Expliqué le 05/10** : la ligne en trop de `analysis_metadata.csv` (`15Bue1014Ch03A__durance3`) est le réplicat durance3 dont `filterAndTrim` a retiré toutes les lectures (13 paires brutes) ; le script 19 part de l'inventaire et ne filtre pas sur la table ASV. Aucun effet sur les résultats (`docs/recalcul/note_ligne_metadonnees_2026-10-05.md`). **Attendu de JF** : accord pour corriger l'attente du script 30 (métadonnées ⊇ table, différence = échantillons vidés par DADA2) — c'est désormais son seul écart (43/44 le 05/10).
- **Attendu de JF** : D2 (inchangé) ; validation des choix techniques du 4H (1 000 lectures assignées au genre, N commun).
- **Ouvert** : abondance différentielle (reportée) ; mécanismes R22/R29/R30 `[À CONFIRMER]` ; R31 possiblement confondu avec l'ordre de traitement, non testé ; Table S10 et Figure S3 : fait le 2026-10-05 (script 41).

**Passation.** 4H et PERMDISP corrigé sont faits et lus ; Table S10 et Figure S3 régénérées (05/10, script 41). Rien de calculé en attente hors arbitrages de JF (D2, choix 4H). Lire d'abord `docs/recalcul/note_4H_2026-10-03.md`.

## Rédaction

- **Fait le 05/10** : texte principal resserré (7 904 mots) dans `Article_resserre.docx` + Note S2 du supplément resserré ; puis, **dans les deux versions** (script 44) : titres des Tables S6/S8/S9/S10, **figures S dans l'ordre de citation** (S1 = compromis profondeur, régénérée en anglais ; S2 = position), **références abrégées NLM** (31), Figure 4 titres/légende alignés, note ENA périmée remplacée, Discussion « one of the two forms » (Camper et al.). Contrôle chiffré : script 40 étendu (voir `VERIF-V2`).
- **Attendu de JF** : (a) valider la version resserrée (`docs/manuscrit/resserrement_2026-10-05_comparaison.docx`) ; (b) **§8.6 : écarts de rétention d'un seul run (durance1) ou étendue sur les trois runs** (note grise ; le midgut passe 1 varie de 5,7 à 14,0 points) ; (c) phrase retirée sur l'abondance différentielle (note grise §8.7) ; (d) correction de l'attente du script 30.
- **Notes grises à lever** : autorisations Ain/Ardèche, euthanasie, température du tube (André) ; Competing interests, Authors' contributions, Acknowledgements ; DOI Zenodo ; FACIES ; Sinama 2013 (deux notices possibles) ; mécanisme de l'effet de colonne (D2) ; code de sexe « X ».
- **Fait le 05/10 (soir), liste « sans décision »** : part du 12S recalculée et corrigée (§5, Note S2, R2 ; script 45) ; images du supplément ramenées à 15,24 cm ; note de la Figure S1 corrigée (« ex-Figure S2 ») ; note grise d'introduction réduite à (i) titre et (ii) Wang 2015 / Sevellec 2014 ; `.bib` : Small 2019 et Sevellec 2019 propagés (script 46) ; script 30 : deux attentes périmées mises à jour (43/44). Scripts 46–47.
- **Réglé le 05/10 (soir)** : Supporting Information de Camper et al. fournies par JF (`CAMPER-SI`) ; exclusion de ρ ≥ 0,8 confirmée (Intersection = 0, Tables S.2.1–S.2.2) ; « 0.067 » corrigé en **0.066** au §8.11 des deux versions (Table S.4.1 : 0,0664 ; script 48), contrôlé par le script 40.
- **Bloque** : D2 (JF) pour la phrase sur le mécanisme de l'effet de colonne.

**Passation.** Deux versions coexistent et portent les mêmes corrections du 05/10 : `Article.docx` (référence) et `Article_resserre.docx` (en relecture). Lire d'abord `DECISIONS.md` (deux entrées du 05/10), puis `docs/manuscrit/journal_resserrement_2026-10-05.md`. Ensuite : arbitrages (a)–(d) de JF.

## Bibliographie

- **Prêt à consommer** : `docs/biblio/microbiome_hybrid_all_refs.bib` — 223 notices, champs
  `author` reconstruits le 25/09 et validés contre Crossref sur 40 DOI. C'est le fichier qui
  fait foi ; les autres `.bib` du dossier sont thématiques (`hybrid_microbiome_refs`,
  `fish_microbiome_key_refs`, `batch_effect_sota`, `rarefaction_sota`).
- **Réglé le 05/10** : les trois références sans DOI (thèses de Kiel et de Washington University, notice MPDL de Wang & Baines 2014) n'ont pas de version publiée dans Crossref ; aucune n'est citée dans l'article. Small 2019 et Sevellec 2019 propagés dans la `.bib` (script 46).
- **Ouvert** : texte intégral du cadre 4H (DOI `10.1111/2041-210x.14279`) **relu le 05/10** (artefact du projet, PDF non déposé sur le dépôt public) : valeurs de la Discussion conformes à leur Table 3 ; leurs **tables supplémentaires** (`CAMPER-SI`, fournies par JF le 05/10) confirment l'exclusion de ρ ≥ 0,8 et donnent 0,066 (et non 0,067) pour la variation de l'axe parental entre 1 000 et 10 000 lectures ; `docs/note_sensibilite_4H.md` attribuait au lézard un « 0,013 » qui est la valeur du maïs (Table S.4.1).
- **Attendu de la Rédaction** : rien en attente ; la biblio suit la rédaction.

## Soumission de données

- **État** : PRJEB124417 vérifié (R28, 4 612/4 612), en ligne, non public.
- **Décidé par JF le 03/10** : soumettre **en une seule fois** les dates de Pertuis (`ENA-PERT`, 44) et le `host subject id` préfixé par la campagne (`ENA-SUBJ`, 727) ; **pas de restructuration** des 2 304 experiments pour l'instant ; ouverture publique **à la soumission de l'article**.
- **À faire, par un humain** (identifiants Webin au clavier) : la soumission, selon la ligne de commande testée de `ena_deposit/MEMO_corrections_restantes.md` ; puis ajouter les deux tables **en fin de liste** de `7_verifier_exhaustif.sh` et revérifier ; puis mettre à jour le §9 et la note sur le host subject id (Note S2 de `Supplementary_Data.docx`, Note S3 de la version resserrée).
- **Recette à ne pas re-découvrir** : FTP Webin inutilisable, `webin-cli -ascp` en appelant le conteneur ; MODIFY par `curl` ; un reçu vide n'est pas un échec (`6_etat_du_depot.sh` avant toute relance).
- **Leçon du 30/09, toujours valable** : ne jamais écrire dans `docs/manuscrit/` depuis une session Soumission.

**Passation.** Rien à calculer : une soumission MODIFY à lancer par JF, déjà construite et testée. Lire `ena_deposit/MEMO_corrections_restantes.md`, puis `DECISIONS.md` du 03/10.

## Autre (données d'André, hygiène du dépôt)

- **Réponses d'André du 03/10** consignées mot pour mot dans `docs/reponses_andre_2026-10-03.md` : autorisations 2014-156-0001 et 2015-1426DDT605 (ONEMA, DDT 04, 05 et 84), même protocole de dissection pour les quatre tissus, tissu 01 = lobe de nageoire caudale, protocole de laboratoire identique à Guivier et al. 2017, témoins retrouvés dans les plaques, origine de la fuite de mock non récupérable, vivier et durées de dissection, contrat EDF-CNRS AGDI 428481.
- **Attendu d'André** (questions de suivi transmises par JF le 03/10) : couverture des stations de l'**Ain** et de l'**Ardèche** par une autorisation DDT ; euthanasie par dislocation cervicale juste avant chaque dissection ; température de conservation du tube en éthanol. Plus, en fin d'écriture, les remerciements.
- **Réponses de JF du 03/10** : `docs/reponses_JF_2026-10-03.md`.
- **Dépôt GitHub public** (JF) : le miroir s'arrêtait au 25/09 (`72666a3`) ; le manuscrit et les notes internes y deviennent publics à chaque synchronisation.
- **Hygiène, sans urgence** : `CLAUDE.md` périmé ; 33 fichiers en doublon à la racine ; 0,97 Go de tables ASV redondantes ; `results/fastqc_durance*` et `ena_deposit/webin_out_*` archivables. `metadata/index_hybride_andre.csv` (`IDX-HYB`) : sens **vérifié le 05/10** (0 = hotu, 1 = toxostome ; convention inverse de la colonne Q d'`analysis_metadata.csv`) ; formulaire rempli pour 49/180 individus seulement, non utilisé par les analyses.
- **Attention** : dépôt modifié en parallèle par d'autres sessions ; `git status` et relecture avant toute écriture dans `_etat/`.

