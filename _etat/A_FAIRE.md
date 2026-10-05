# A_FAIRE — passations par type de session

État au **2026-10-05, clôture du soir** (commit `cfe939b`). Sections *Analyse* et *Rédaction* réécrites à cette clôture ; *Bibliographie* mise à jour en cours de session (05/10) ; *Soumission de données* inchangée depuis le 03/10 soir ; *Autre* : point `IDX-HYB` réglé le 05/10.
Chaque section est réécrite par la session concernée à sa clôture (cf. `README.md` du dossier).

---

## Analyse

- **Fait le 05/10** : ligne en trop de `analysis_metadata.csv` expliquée (`15Bue1014Ch03A__durance3`, vidé par `filterAndTrim` ; aucun effet ; `docs/recalcul/note_ligne_metadonnees_2026-10-05.md`) ; rétention selon la profondeur recalculée par catégorie, tissu, passe et run (`scripts/43`, `RETENTION`, R35) — les chiffres du §8.6 sont ceux du run durance1 ; part du 12S recalculée (`scripts/45`, `PART-12S`, R2 annoté) ; index hybride d'André : sens vérifié (0 = hotu), non utilisé.
- **Rappel 03/10** : 4H pré-déclaré, calculé et lu (R33) ; PERMDISP corrigé du biais de petit effectif (R34).
- **Attendu de JF** : D2 (mécanisme de l'effet de colonne) ; choix techniques du 4H (1 000 lectures au genre, N commun) ; accord pour l'attente « métadonnées ⊇ table » du script 30 (son seul écart, 43/44) ; tester ou non R31 (dominance de *C. nasus* et ordre de traitement), avec un plan pré-déclaré.
- **Ouvert** : abondance différentielle (reportée, cf. Rédaction (c)) ; mécanismes R22/R29/R30 `[À CONFIRMER]`.

**Passation.** Rien de calculé en attente : tout ce qui pouvait l'être sans arbitrage l'est (scripts 43 et 45 du 05/10). Prochaine analyse possible : test R31 si JF le valide. Lire d'abord `RESULTATS.md` (R35, R2) puis `docs/recalcul/note_4H_2026-10-03.md`.

## Rédaction

- **Fait le 05/10** : (1) texte principal resserré (10 677 → 7 904 mots) dans `Article_resserre.docx`, détails techniques déplacés verbatim en Note S2 du supplément resserré (ancienne Note S2 → S3) ; (2) **dans les deux versions** : figures S dans l'ordre de citation (S1 = compromis profondeur, régénérée en anglais avec des valeurs recalculées ; S2 = position), titres des Tables S6/S8/S9/S10, 31 revues abrégées NLM, Figure 4 titres et légende alignés, §8.6 « run durance1 » précisé, §5 part du 12S corrigée (14–15 % par run), §8.11 0,067 → 0,066 (Camper et al., SI), Discussion « one of the two forms », notes grises périmées remplacées, images du supplément à 15,24 cm. Scripts 42, 44, 47, 48.
- **Contrôles en fin de session** : script 40 **75/75** sur `Article_resserre.docx`, 74/75 sur `Article.docx` (seul écart : ordre des notes, la référence ne citant que la Note S1) ; script 30 **43/44**.
- **Attendu de JF** : (a) valider ou non la version resserrée (comparaison : `docs/manuscrit/resserrement_2026-10-05_comparaison.docx`) ; (b) §8.6 : un run (durance1) ou l'étendue sur les trois runs (midgut passe 1 : 5,7–14,0 points) ; (c) phrase retirée sur l'abondance différentielle (note grise §8.7) ; (d) D2, phrase sur le mécanisme de l'effet de colonne (séjour en vivier) ; (e) références : année du volume imprimé, notice Sinama 2013, pertinence de Wang 2015 [11] et Sevellec 2014 [6], appel à la Table S5 ; (f) titre définitif ; (g) Declarations : auteurs et contributions, conflits d'intérêts, DOI Zenodo ; (h) notes grises historiques à retirer avant soumission.
- **Attendu d'André** : autorisations couvrant l'Ain et l'Ardèche ; euthanasie ; température du tube en éthanol ; rattachement du contrat AGDI 428481 à FACIES ; code de sexe « X » ; remerciements ; sa part des contributions.
- **Bloque** : D2 (JF) pour la phrase sur le mécanisme ; (a) pour savoir quelle version porte la suite du travail.

**Passation.** Deux versions coexistent et portent les mêmes corrections : `Article.docx` (référence, `c3884a23…`) et `Article_resserre.docx` (en relecture, `1baaab97…`). Toute nouvelle correction s'applique aux deux tant que (a) n'est pas tranché. Plus rien à faire sans décision de JF ou réponse d'André. Lire d'abord les entrées du 05/10 de `DECISIONS.md`, puis la liste (a)–(h) ci-dessus.

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

