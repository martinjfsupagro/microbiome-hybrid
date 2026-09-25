# PROJET — microbiome-hybrid

## Question de recherche
Le microbiote 16S des **hybrides hotu × toxostome** est-il **intermédiaire** entre les deux
espèces parentales, ou **déplacé hors de leur intervalle** (transgressif) ? Et cette
réorganisation dépend-elle du **compartiment tissulaire** ?

## Hypothèses testées
- H1 — Microbiote hybride intermédiaire (modèle additif) vs dominant vs transgressif
  (axe Gain–Loss de l'indice 4H, Camper et al. 2024, *Methods Ecol Evol* 15:511–529).
- H2 — L'effet de l'hybridation varie entre compartiments (gradient externe → interne :
  nageoire caudale, branchie, midgut, hindgut). **Seul axe non confondu** du dispositif
  (appariement intra-individu, 109 individus à 4 tissus).
- H3 — Génétique de l'hôte vs contexte local : la station explique 10 à 20× plus de variance
  que la catégorie génotypique (résultat acquis, cf. `RESULTATS.md`).
- H4 — Prédiction transgressive en dispersion (PERMDISP) : **non soutenue, sens inversé**.

## Périmètre
| Dimension | Valeurs |
|---|---|
| Taxons | `Cn` *Chondrostoma nasus* (hotu) · `Pt` *Parachondrostoma toxostoma* (toxostome) · `Ch` chondrostome **non identifié** (ni hybride, ni chevesne) · `Hy` hybride (après génotypage) |
| Catégories (25 chr, sept. 2026) | 59 Cn / 42 Hy / 79 Pt sur 180 individus |
| Tissus | 4 : `01` nageoire caudale, `02` midgut, `03` hindgut, `05` branchie — certaines notes récentes appellent `01` « peau » `[À CONFIRMER]` |
| Marqueur | 16S V4, amorces 515F/806R (Caporaso 2011), **déjà retirées des lectures** (protocole Schloss) |
| Sites / stations | 9 codes : Ain, Avi, Bau, Bue, Caa, Cab, Jus, Man, Per — le Suran porte **2 stations** (Pont-d'Ain aval / Chavannes-sur-Suran amont, 25,4 km, barrière de 2,5 m) |
| Période | Pêches 2014 et 2015 ; séquençage 2017 ; analyse 2026 |
| Effectifs | 180 individus · 727 librairies biologiques + 41 contrôles · ×3 runs MiSeq · 44 200 ASV |

## Conventions de nommage
- **Échantillon** : `<AA><Site><Individu><Taxon><Tissu><Réplicat>` — ex. `14Ain1001Cn01A`
  (2014, Ain, individu 1001, hotu, nageoire caudale). Deux identifiants malformés connus :
  `14Avi1036-Cn03A`, `14Avi1037-01A` (tiret → perte d'appariement).
- **Clé de jointure table ↔ métadonnées** : `dada2_id` = `<nom_ech>__<run>`
  (ex. `14Ain1001Cn01A__durance1`). **Jamais `sample_name`** (garde les variantes de saisie).
- **`bis`** = seconde extraction d'ADN du même tissu (colonne `extraction` : `initiale`/`bis`),
  9 tissus concernés, 27 lignes. Ne pas fusionner avec l'extraction initiale.
- **Runs** : `durance1` (préparation PCR n°1), `durance2` + `durance3` (préparation n°2,
  deux flow cells). Réplication **nichée** — ne pas modéliser `run` en facteur à 3 niveaux.
- **Commits** : en français, préfixes `feat:` / `fix:` / `docs:` / `chore:`. Un job n'est soumis
  qu'après commit ; toute exécution est tracée dans `runs.log`. Aucune donnée n'est « réparée »
  en silence : toute correction laisse un drapeau ou une trace.

## Chemins canoniques
| Rôle | Chemin (relatif à la racine) |
|---|---|
| Racine | `/home/martinj/work/projects/microbiome-hybrid` (= `~/work/…`, hors quota HOME) |
| Livraisons brutes de run | `data/durance{1,3}` (SampleSheets, I1/I2, InterOp) |
| **Source fastq unique** | `consolidated_dataset/durance{1,2,3}` (4 608 `.fastq.gz` R1/R2) |
| Table ASV filtrée | `results/dada2_final/asv_table_filtered.tsv` + `taxonomy.tsv` |
| **Table de travail validée** | `results/decontam/asv_table_clean.tsv` (2 180 × 44 200) |
| Arbre | `results/phylogeny/rooted_tree.qza` (44 256 feuilles) et `tree.nwk` |
| Matrices bêta moyennes | `results/rarefaction/beta_mean_*_N400.rds` (4 métriques) |
| Scripts | `scripts/` (`01`→`27`, lanceur + worker) ; variables : `config/project.env` |
| Sorties d'analyse | `results/<analyse>/` — **non versionnées** (`.gitignore`) |
| Figures | `docs/figures/` (versionnées) ; `results/*/fig_*.png` (non versionnées) |
| Manuscrit | `docs/manuscrit/` (`Article.docx`, `Supplementary_Data.docx`) |
| Bibliographie | `docs/biblio/` (`microbiome_hybrid_all_refs.bib` fait foi) |
| Dépôt de séquences | `ena_deposit/` — ENA **PRJEB124417** |
| Décisions détaillées | `docs/decision_*.md` (20 fichiers) |
| Scratch des jobs | `$SCRATCH_DIR` = `$SCRATCH/runs/microbiome-hybrid` ; chemin réel `/scratch/users/martinj/runs/microbiome-hybrid` `[À CONFIRMER]` |

## Outils et versions clés
- **DADA2** : env conda `~/bin/envs/dada2` (R 4.5.3, bioconductor-dada2, decontam 1.30.0,
  vegan 2.7.5). `truncLen = c(230, 190)`. `assignTaxonomy` : pic mémoire **256 Go**.
- **Référence taxonomique** : SILVA v138.2 format DADA2 (Zenodo 14169026).
- **Conteneurs** (`~/work/shared_softwares`) : cutadapt 5.0, FastQC, MultiQC,
  QIIME 2 (`qiime2_2024.10.sif`, `amplicon_2026.1.sif` — unifrac 1.3.0, biom 2.1.16).
- **SLURM meso** : `--account=ondemand@biomics --partition=cpu-ondemand` ;
  **tout job > 1 h exige `--qos=cpu-ondemand-long`** (sinon PENDING indéfini).
- **Indice 4H** : package R `HybridMicrobiomes` v0.1.1 (CRAN) — présence dans l'env dada2
  `[À CONFIRMER]`.
- Paramètres gelés : raréfaction **3 000 lectures**, N = **400** tirages, ρ = **0,5** au rang genre.
