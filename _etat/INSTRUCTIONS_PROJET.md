# INSTRUCTIONS_PROJET — microbiome-hybrid

À copier dans les instructions du projet. Le bloc est autoportant : il ne suppose aucune
connaissance venue d'une conversation antérieure.

---

## Le projet en une phrase
Microbiote 16S V4 de quatre tissus chez le hotu (`Cn`), le toxostome (`Pt`) et leurs hybrides,
9 stations, 2014–2015, sur le cluster meso :
racine **`/home/martinj/work/projects/microbiome-hybrid`**, mémoire partagée dans **`_etat/`**.

## En début de session
1. Lire `_etat/PROJET.md`, puis `_etat/A_FAIRE.md`, puis les fichiers utiles à la tâche
   (`DONNEES.md` pour toucher aux données, `RESULTATS.md` pour citer un chiffre,
   `DECISIONS.md` pour savoir ce qui est déjà tranché).
2. Vérifier l'état du dépôt (`git status`, `git log -3`) : **plusieurs sessions écrivent
   en parallèle**, le dépôt a pu bouger depuis la dernière note de passation.
3. Annoncer en **trois lignes** : ce qu'on sait, ce qu'on va faire, ce qui bloque.
4. **Ne jamais retraiter une donnée marquée « validé » dans `DONNEES.md`** sans une décision
   explicite consignée d'abord dans `DECISIONS.md`. Cela vaut en particulier pour
   `results/decontam/asv_table_clean.tsv` et les matrices `beta_mean_*_N400.rds`.

## En fin de session, ou quand je dis « clôture »
1. Mettre à jour les fichiers concernés — et seulement eux :
   `DECISIONS.md` (nouvelle entrée en tête : `## AAAA-MM-JJ — titre`, puis
   **Décision / Raison / Impact / Session concernée**), `DONNEES.md` (tout fichier créé,
   déplacé, ou dont le statut change), `RESULTATS.md` (tout résultat nouveau ou promu).
2. **Réécrire la section d'`A_FAIRE.md`** correspondant au type de session : ce qui est attendu
   de qui, ce qui bloque, ce qui est prêt à consommer.
3. Écrire une **note de passation de cinq lignes maximum** à la fin de cette section,
   destinée à la prochaine session : où on en est, quoi faire ensuite, quel fichier lire d'abord.
4. Commiter dans les conventions du dépôt (français, `feat:` / `fix:` / `docs:` / `chore:`),
   après avoir vérifié que rien d'autre n'est emporté dans le commit.

## Règles
- Un résultat n'entre dans `RESULTATS.md` que s'il **pointe vers un script** et vers des
  **données référencées dans `DONNEES.md`**. Sinon il reste dans la prose de la session.
- **Toute modification d'un fichier de `_etat/` est signalée explicitement dans la réponse**
  (quel fichier, quelle entrée), pas seulement dans le commit.
- Les hypothèses non vérifiées restent marquées **`[À CONFIRMER]`** dans le texte — on ne les
  efface qu'en les confirmant, jamais en les reformulant.
- Rien n'est « réparé » en silence : toute correction de données laisse un drapeau ou une trace,
  et une entrée dans `DECISIONS.md` si elle change un statut.
- **D7 (métrique de diversité) est ouverte** : tout R² de catégorie ou de station reste
  `préliminaire`, y compris ceux déjà écrits dans le manuscrit.

## Contraintes du cluster à connaître
- SLURM : `--account=ondemand@biomics --partition=cpu-ondemand` ;
  **tout job de plus d'une heure exige `--qos=cpu-ondemand-long`**, sinon il reste PENDING
  indéfiniment (`QOSMaxWallDurationPerJobLimit`).
- Un job est soumis **après** commit ; chaque exécution est tracée dans `runs.log`.
- Les sorties de jobs vont dans `results/` ou sur le scratch, **jamais** dans le HOME ;
  `results/` n'est pas versionné, un résultat n'est donc reproductible que par son script.
- `assignTaxonomy` (DADA2) demande 256 Go de mémoire.
