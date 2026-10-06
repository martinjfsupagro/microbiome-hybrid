# A_FAIRE — passations par type de session

État au **2026-10-06, clôture du soir** (HEAD avant clôture `9a966af`). Sections *Analyse*, *Rédaction*, *Soumission de données* et *Autre* réécrites à cette clôture ; *Bibliographie* inchangée depuis le 05/10.
Chaque section est réécrite par la session concernée à sa clôture (cf. `README.md` du dossier).

---

## Analyse

- **Fait le 06/10** : test R31 (contrôle v, R36 : dominance de *C. nasus* non attribuable à l'ordre ; ordre effectif sur l'alpha du hindgut) ; contrôle (vi) campagne de pêche (R39 : détections maintenues, 46 → 52 runs) ; composition en phylums (R37) ; ordination (R38) ; nageoire caudale du Largue (R40) ; taille par catégorie (R42). D2 tranchée (séjour en vivier, hypothèse non testable ici, R32). Abondance différentielle **abandonnée** (décision de JF).
- **Attendu de JF** : validation des choix techniques du 4H pris par l'agent le 03/10 (1 000 lectures au genre, N commun, 500 bootstraps) ; l'entrée correspondante de `DECISIONS.md` est précisée (Jaccard principal, Bray-Curtis en sensibilité, conforme au plan).
- **Ouvert, facultatif** : identité de l'ASV0185 (phylum non assigné, 80 % du midgut de 2015_Caa_1003 ; BLAST non fait) ; part des Mycoplasmatales (comptées dans *Bacillota* par SILVA 138.2) ; mécanisme de l'excès de 12S en plaque 2, colonnes 06–08 `[À CONFIRMER]` ; mécanismes R22/R29/R30 `[À CONFIRMER]`.

**Passation.** Aucun calcul en attente : tout ce que l'article cite est calculé, contrôlé (script 40 95/95, script 30 44/44) et consigné (R36–R42). Les points ouverts sont facultatifs et ne bloquent pas la soumission. Lire d'abord R36–R42 dans `RESULTATS.md`.

## Rédaction

- **Fait le 06/10** : version resserrée devenue la référence unique (`MS`, `MS-SUP`) ; D2, décisions 5 et 7, contrôles (v) et (vi), réponses d'André, contraste de sexe non rapporté, Figures S3 (phylums), S4 (ordination), S5 (PERMDISP), taille et Largue dans les limites ; **paquet de soumission Animal Microbiome** (`SOUMIS-AM`, `docs/soumission/`, commit `9a966af`) : manuscrit sans notes, Fig1–5, 18 Additional files, contrôle des consignes 112/113.
- **Attendu de JF** : (1) remplir les 8 marqueurs [TO COMPLETE] (auteurs, affiliations, courriels, auteur correspondant, DOI Zenodo, rôle des financeurs, contributions, remerciements) ; (2) titre définitif ; (3) références : année du volume imprimé, notice Sinama 2013, pertinence de Wang 2015 [11] et Sevellec 2014 [6], maintien de l'appel à la Table S5 (Additional file 7) au §8.6 ; (4) « Eukaryota » et « Mitochondria » laissés en romain (libellés SILVA) : confirmer ; (5) lettre d'accompagnement, relecteurs suggérés, résumé graphique (facultatif).
- **Attendu d'André** : rôle de Benjamin Hérodet dans les remerciements ; sa part des contributions.
- **Règle** : toute correction se fait dans `MS` / `MS-SUP` (version de travail annotée), puis le paquet est **régénéré** par les scripts 72–75 (commandes dans `docs/soumission/LISEZMOI.md`, exécution locale) — jamais d'édition à la main de `docs/soumission/`.

**Passation.** Le texte est prêt à soumettre, moins les 8 marqueurs. Une fois remplis par JF dans `MS`, régénérer le paquet (72, 73, 75) et relancer les scripts 40 et 30. Lire d'abord `docs/soumission/LISEZMOI.md`, puis les entrées du 06/10 de `DECISIONS.md`.

## Bibliographie

- **Prêt à consommer** : `docs/biblio/microbiome_hybrid_all_refs.bib` — 223 notices, champs
  `author` reconstruits le 25/09 et validés contre Crossref sur 40 DOI. C'est le fichier qui
  fait foi ; les autres `.bib` du dossier sont thématiques (`hybrid_microbiome_refs`,
  `fish_microbiome_key_refs`, `batch_effect_sota`, `rarefaction_sota`).
- **Réglé le 05/10** : les trois références sans DOI (thèses de Kiel et de Washington University, notice MPDL de Wang & Baines 2014) n'ont pas de version publiée dans Crossref ; aucune n'est citée dans l'article. Small 2019 et Sevellec 2019 propagés dans la `.bib` (script 46).
- **Ouvert** : texte intégral du cadre 4H (DOI `10.1111/2041-210x.14279`) **relu le 05/10** (artefact du projet, PDF non déposé sur le dépôt public) : valeurs de la Discussion conformes à leur Table 3 ; leurs **tables supplémentaires** (`CAMPER-SI`, fournies par JF le 05/10) confirment l'exclusion de ρ ≥ 0,8 et donnent 0,066 (et non 0,067) pour la variation de l'axe parental entre 1 000 et 10 000 lectures ; `docs/note_sensibilite_4H.md` attribuait au lézard un « 0,013 » qui est la valeur du maïs (Table S.4.1).
- **Attendu de la Rédaction** : rien en attente ; la biblio suit la rédaction.

## Soumission de données

- **État** : PRJEB124417 corrigé le 06/10 (44 dates de Pertuis, 727 `host subject id` préfixés) et vérifié par JF à 15:02 : 5 339/5 339 (R41) ; en ligne, **non public**.
- **Défaut résiduel** (trouvé le 06/10 au soir) : TITLE de ERS31168490 (`15Per2015Ch03A`, pêché le 2014-08-20) = « … Per 2015, individual 2015 », attendu « … Per 2014, individual 2015 ». La vérification l'a déclaré conforme parce que sa valeur de référence portait la même erreur.
- **À faire, par un humain** (identifiants Webin au clavier) : (1) MODIFY de ce seul TITLE, construit **depuis l'état déposé** (méthode de `scripts/53`, jamais depuis le XML d'août), test puis production ; corriger aussi la valeur de référence avant de revérifier par `7_verifier_exhaustif.sh` ; (2) ouverture publique **à la soumission de l'article** (décision du 03/10).
- **Recettes à ne pas re-découvrir** : `build_ena_modify.py` depuis le XML d'origine ramène les 4 612 champs corrigés à leur valeur d'août (incident du 06/10) ; `6_etat_du_depot.sh` est périmé (garde `FORCER_ETAT_AOUT=1`) ; un reçu vide ou `success=false` sans accession n'altère pas l'état : vérifier avant toute relance ; FTP Webin inutilisable, `webin-cli -ascp` via le conteneur.
- **Leçon du 30/09, toujours valable** : ne jamais écrire dans `docs/manuscrit/` depuis une session Soumission.

**Passation.** Un seul champ à corriger (TITLE de ERS31168490), puis l'ouverture publique au moment de la soumission. Lire `ena_deposit/MEMO_corrections_restantes.md` (procédure du 06/10) et R41.

## Autre (données d'André, hygiène du dépôt)

- **André** : réponses du 06/10 consignées (`ANDRE-1006`) et portées au manuscrit ; restent le rôle de B. Hérodet et sa part des contributions (voir Rédaction).
- **Dépôt GitHub public** (JF) : miroir arrêté au 25/09 (`72666a3`) ; à synchroniser avant soumission (référence [51] de l'article). **Attention** : la synchronisation rend publics la version annotée (`MS`, notes grises) et les notes internes (`_etat/`, `docs/`) — décider avant ce qui est exclu. Archive Zenodo et DOI ensuite (marqueur de la section Availability).
- **Hygiène, sans urgence** : `CLAUDE.md` périmé ; 33 fichiers en doublon à la racine ; 0,97 Go de tables ASV redondantes ; `results/fastqc_durance*` et `ena_deposit/webin_out_*` archivables ; `scripts/41` écrit encore `fig_S3_permdisp.png` (nom historique de la Figure S5) ; `metadata/analysis_metadata.csv` porte des dates de collecte par station (listes du type « 2014-07-17;2015-07-10 »), l'ENA par échantillon (alignement facultatif) ; `IDX-HYB` non utilisé.
- **Attention** : dépôt modifié en parallèle par d'autres sessions ; `git status` et relecture avant toute écriture dans `_etat/`.

**Passation.** Rien d'urgent hors la décision sur le contenu du miroir GitHub, à prendre avant la soumission. Lire cette section puis `docs/soumission/LISEZMOI.md`.

