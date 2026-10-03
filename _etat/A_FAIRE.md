# A_FAIRE — passations par type de session

État au **2026-10-03, soir**. Sections *Analyse*, *Rédaction*, *Soumission de données* et *Autre* réécrites à la clôture de la session du 03/10 (réponses d'André et de JF, cinq tests déclarés a priori, manuscrit) ; *Bibliographie* inchangée.
Chaque section est réécrite par la session concernée à sa clôture (cf. `README.md` du dossier).

---

## Analyse

- **Fait le 03/10** : cinq tests **déclarés a priori** (`docs/plan_tests_2026-10-03.md`, commité avant calcul) et lancés (scripts 31–36, `results/tests_20261003/`) ; interprétation dans `docs/recalcul/note_tests_2026-10-03.md`, chiffres en R8 (refait) et R29–R32.
- **Défauts du registre corrigés** : R8 n'avait pas de script (diagnostic de conversation attribué à tort au script 14) ; « Faith PD non exploité » était périmé (utilisé dans R27).
- **Erreur de cette session, consignée** : le test du séjour en vivier reposait sur quatre stations « découplées » ; le découplage venait d'un ρ calculé par station en mélangeant 2014 et 2015. Dans chaque campagne, colonne et ordre de traitement sont corrélés (ρ 0,55–0,93) : le test ne pouvait pas trancher (R32).
- **Attendu de JF** : **D2**, qu'il avait suspendue à ce test. Le test ne départage rien : la position est confondue avec l'ordre de traitement par construction du plan. Options (a) à (c) de la question 2.1, plus une formulation « colonne de plaque confondue avec l'ordre de traitement ».
- **Ouvert** : indice 4H en deux passes (paramètres D5) ; abondance différentielle reportée par JF ; mécanismes de R22 (dilution, R30) et de R29 `[À CONFIRMER]` ; proximité Hy–Cn en alpha (R31) possiblement confondue avec l'ordre de traitement, non testée.

**Passation.** Les cinq tests sont faits et lus. Le prochain calcul utile reste **l'indice 4H en deux passes** ; D2 attend JF, qui dispose désormais de R32. Lire d'abord `docs/recalcul/note_tests_2026-10-03.md`, puis `docs/plan_tests_2026-10-03.md`.

## Rédaction

- **Fait le 03/10** : réponses d'André intégrées à `Article.docx` (§1 séquence pêche → vivier → dissection, §2 lobe caudal, ordre de dissection, deux tubes ; notes grises §3–§4 retirées) ; titre provisoire = sous-titre du supplément ; Funding avec le contrat EDF-CNRS **AGDI 428481** ; lien GitHub public au §9 ; **Table S2 = génotypes individuels** insérée, anciennes S2–S9 renumérotées S3–S10 (8 renvois dans l'article, 12 dans le supplément) ; note *Host identity* corrigée (elle disait « microsatellite ») ; légende de la Table S2 corrigée après relecture (D minimal 0,0100 ; D ne sépare pas les intermédiaires).
- **Notes grises restantes** : autorisations des stations de l'Ain et de l'Ardèche, euthanasie, température du tube en éthanol (questions de suivi à André, envoyées le 03/10) ; DOI Zenodo ; rattachement de la thèse d'A. Ungaro au contrat FACIES non confirmé ; code de sexe « X » (52 individus) non documenté ; Acknowledgements en fin d'écriture.
- **Signalé, non corrigé** : l'ordre des premières citations des tables n'est pas croissant (1, 2, 5, 3, 8, 7, 9, 10, 4), alors que le supplément annonce le contraire — le défaut préexistait (1, 4, 2, 7, 6, 8, 9, 3).
- **Cible Animal Microbiome** (JF) : structure Background / Methods / Results / Discussion / Conclusions et section Declarations à mettre en place ; titre définitif en fin d'écriture ; références Wang 2015 et Sevellec 2014 : JF cherche les textes intégraux.
- **Bloque** : D2 pour les §8.8–8.9 (le §8.8 cite encore « the delay between capture and dissection » parmi les mécanismes possibles ; à reformuler avec R32) ; Results et Discussion pas commencés.

**Passation.** Les Methods reflètent les réponses d'André du 03/10 et la numérotation S1–S10. Commencer par reformuler le §8.8 avec R32 **après** l'arbitrage D2 de JF. Fichier : `docs/manuscrit/Article.docx` (lire depuis le cluster, texte ajouté en bleu).

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

