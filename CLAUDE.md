# CLAUDE.md — microbiome-hybrid

Orientation pour un agent reprenant ce projet. Le détail vit dans le dépôt
(`README.md`, en-têtes des `scripts/`, `git log`, `runs.log`, `docs/`) ; ce
fichier donne l'état et les pièges non évidents.

## Le projet
Microbiome 16S V4 comparé chez le **hotu** (`Cn`), le **toxostome** (`Pt`), le
**chondrostome non résolu** (`Ch`) et leurs hybrides, 4 tissus, 9 sites Durance,
2014–2015. **Question** : le microbiome des hybrides est-il intermédiaire entre
les parentaux, ou déplacé hors de leur intervalle ? Données fournies par André
(écologue). Cluster SLURM + Singularity ; env R/DADA2 (`~/bin/envs/dada2`).

## État (juillet 2026)
Pipeline exécuté de bout en bout. Livrable : `results/dada2_final/` —
**`asv_table_filtered.tsv` : 44 349 ASV × 2295 échantillons** + `taxonomy.tsv`
(SILVA v138.2). Détail des résultats : `docs/rapport_analyse_16S.md`.
**Prochaine étape : l'analyse écologique** (décontam, diversité α/β, test de la
question hybride) — pas encore commencée.

## Faits non évidents — À NE PAS redécouvrir
- **`Ch` = chondrostome non identifié** (ni `Cn` ni `Pt` tranché), **PAS le
  chevesne**. Le commit `8a09794 "docs: Ch = chevesne"` est FAUX (corrigé
  ensuite). Le chevesne (`Sc`) n'est pas dans ces runs.
- **3 runs = reséquençage des mêmes 768 librairies** (durance1/2/3). Gardés
  distincts (échantillons suffixés `__duranceN`) pour estimer l'effet run — il
  n'est confondu avec aucun facteur biologique. À exploiter en analyse.
- **Co-contamination 12S** : les amorces 16S co-amplifient le 12S mito de l'hôte
  (14–67 % des lectures). Retiré par la longueur (script `02`) puis filet
  taxonomique (1144 ASV Mitochondria retirés). Voir en-tête de `02-remove_12S_worker.sh`.
- **Amorces déjà retirées** des lectures (protocole Schloss) : pas de retrait 5'
  ni d'adaptateur Nextera.
- **Jointure table↔métadonnées par `dada2_id`** (`{nom_ech}__{run}`, ex.
  `14Ain1001Cn01A__durance1`), colonne de `metadata/samples_all.csv` — **PAS**
  `sample_name` (qui garde les variantes de saisie).
- **`assignTaxonomy` = pic mémoire** : 256 Go requis (OOM à 64 G). Nœuds
  cpu-ondemand = 1,4 To. SLURM : `--account=ondemand@biomics --qos=cpu-ondemand-long`.

## Données
- `consolidated_dataset/durance{1,2,3}/` : **source unique** des fastq.gz R1/R2
  (16S V4, 12S non retiré ici). `data/` = run dirs d'origine (SampleSheet, I1/I2…).
- `metadata/samples_all.csv` : 2304 lignes, plan + taille/poids/sexe (colonnes
  `size_cm`/`weight_g`/`sex`) + `dada2_id`. Corrections tracées par drapeaux.
- **En attente d'André** : identification fine des `Ch` et statut hybride (code
  `Hy` dans `metadata/HotuToxo_taillepoids.xlsx`, colonne `Species`) — non encore
  intégré, verrou de la question hybride.

## Workflow
Scripts numérotés `01`→`05` (lanceur + worker par run), soumis depuis la racine,
arbre git propre exigé, tout tracé dans `runs.log`. Régénérer les métadonnées :
`build_metadata.py` (par run) → `merge_metadata.py` (+`--measurements`).
Réexécuter la taxonomie : `sbatch scripts/05-merge_taxonomy.sh` (SILVA dans
`config/project.env`). Commandes détaillées : `README.md`.

## Convention
Commits en français, préfixe `feat:`/`fix:`/`docs:`. Rien n'est « réparé » en
silence : toute correction de données laisse un drapeau/trace. Soumettre les
jobs seulement après commit.
