# microbiome-hybrid

## Description
Analyse comparative du microbiome (16S) de plusieurs tissus chez le hotu, le
toxostome et leurs hybrides, sur plusieurs sites et deux années (2014, 2015).

**Question** : le microbiome des hybrides est-il intermédiaire entre les deux
espèces parentales, ou déplacé hors de leur intervalle ?

### Plan d'échantillonnage
| Facteur | Niveaux |
|---|---|
| Taxon    | hotu (`Cn`) / toxostome (`Pt`) / chondrostome non résolu (`Ch`) |
| Tissu    | 4 : caudale (`01`) / midgut (`02`) / hindgut (`03`) / branchie (`05`) |
| Site     | Ain, Avi, Bau, Bue, Caa, Cab, Jus, Man, Per |
| Année    | 2014 / 2015 |

**Codes taxon.** `Ch` = chondrostome **non identifié** à ce stade (ni `Cn` ni
`Pt` tranché), et **non** le chevesne comme on l'a d'abord cru. Le chevesne
(*Squalius cephalus*, code labo `Sc`) n'est pas dans ces trois runs. L'espèce
fine (dont le statut hybride) se lit dans `HotuToxo_taillepoids.xlsx`, où les
individus séquencés `Ch` se répartissent en `Cn`/`Pt`/`Ch`/`Hy` — voir plus bas.

Plan très déséquilibré : site et année sont largement confondus (seuls Avi et
Bue couvrent les deux années), de même que taxon et site. Voir
[docs/donnees_durance1.md](docs/donnees_durance1.md).

### Données
| Lot | Run MiSeq | Flowcell | n | Livraison | État |
|---|---|---|---|---|---|
| `durance1` | 170710_M03930_0062 | BBHKV | 768 | run dir + SampleSheet | inventorié |
| `durance2` | M03930_0069 | BCFFD | 768 | fastq renommés + SampleSheet à part | inventorié |
| `durance3` | 171103_M03930_0072 | BFWT5 | 768 | run dir + SampleSheet | inventorié |

Les trois runs sont **le reséquençage des mêmes 768 librairies** (confirmé :
même plan de plaque, mêmes puits, mêmes i7 ; seuls les i5 changent — durance1 a
son propre jeu d'i5, durance2 et durance3 en partagent un autre). Chaque
échantillon est donc présent en triple : 729 réplicats techniques inter-runs,
plus les 39 contrôles × 3. L'effet run est estimable directement — il n'est
confondu avec aucun facteur biologique.

durance2 est livré en fastq démultiplexés (non compressés, témoins dans
`control/`) et sans run dir. Sa SampleSheet d'origine, retrouvée à part
(`EG_16S_Durance_Run2.csv`, déposée dans le dossier des fastq), est
autodétectée par `build_metadata.py` et fournit plaque, puits et index — sinon
absents. Sa virgule Sample_Name/Sample_Plate manquante (nom et n° de plaque
collés) est corrigée à la lecture. Toutes ses lignes gardent le flag
`nom_depuis_fichier`, les noms venant des fichiers et non de la feuille.

### Source unique des fastq : `consolidated_dataset/`
Les fastq **R1/R2 des trois runs** ont été centralisés dans
`consolidated_dataset/<run>/` (4608 fichiers, tout en `.fastq.gz`) par
`scripts/consolidate_fastq.py`. C'est la source de données pour l'analyse ; les
colonnes `fastq_r1`/`fastq_r2` de `samples_all.csv` pointent vers elle
(chemins relatifs à la racine du projet).

- **Sous-dossiers par run** : durance1 et durance3 portent les mêmes noms de
  fichiers (mêmes librairies) — à plat ils s'écraseraient. Ça convient aussi à
  DADA2, qui apprend les taux d'erreur par run.
- **durance2 compressé** en `.fastq.gz` au passage (livré en `.fastq`).
- **R1/R2 seulement.** Les index reads `I1/I2` (durance1/3) et les
  `Undetermined` restent dans `data/`, avec les SampleSheet, InterOp, etc.
- **Réversible** : `metadata/consolidate_manifest.csv` (versionné) ;
  annulation : `python3 scripts/consolidate_fastq.py --revert metadata/consolidate_manifest.csv`
  (puis régénérer les CSV : build + merge).

### Suffixe `bis` : ré-extraction
`bis` désigne une **seconde extraction d'ADN du même tissu**, pas un second
prélèvement. D'où la colonne `extraction` (`initiale` / `bis`), qui fait partie
de la clé de réplicat : 9 tissus ont été extraits deux fois, soit 27 lignes.
Les confondre avec leur extraction initiale ferait passer un effet extraction
pour un effet run.

Deux de ces `bis` étaient mal saisis : `-bis` dans les noms de fichiers de
durance2 (conversion Illumina), et suffixe absent pour `14Bue1006Cn05A` en C07
dans la SampleSheet de durance1. Ce dernier est corrigé dans `NOMS_CORRIGES`
(`build_metadata.py`), flag `nom_corrige` — le puits est le même dans les trois
runs, l'identification est certaine.

### Correspondance code tissu ↔ tissu
Confirmée (collègue, 2026-07-25) et cohérente avec le plan de plaque :

| Code | Tissu |
|---|---|
| `01` | caudale |
| `02` | midgut |
| `03` | hindgut |
| `05` | branchie |

### Taxon des individus 1036–1043 (Ain 2014)
Le bloc de saisie du code espèce manquait. Complété d'après la feuille de
terrain (`TAXON_MANUEL` dans `build_metadata.py`, flag
`taxon_saisi_manuellement`) : 1036–1037 = hotu (`Cn`), 1038–1043 = toxostome
(`Pt`). Ces individus ne sont donc pas un groupe à part.

### Code tissu 04 → 05
`15Avi1002Cn04A` portait un `04` confirmé faute de frappe pour `05` (branchie) ;
l'individu retrouve son jeu 01/02/03/05. Corrigé via `TISSU_CORRIGE`
(`build_metadata.py`), flag `tissu_corrige`.

### Taille / poids / sexe (HotuToxo_taillepoids.xlsx)
Colonnes `size_cm`, `weight_g` et `sex` ajoutées à `samples_all.csv` par
`merge_metadata.py` (option `--measurements`), depuis
`metadata/HotuToxo_taillepoids.xlsx`. Ce sont des données **par individu** :
jointes sur (année, site, individu) — **sans** le taxon, puisque le poisson est
le même quelle que soit son étiquette — et propagées à tous ses tissus et tous
les runs.

- taille en cm, poids en g ;
- `sex` : `M` / `F` / `X` (non défini — les `x` et `X` du xlsx homogénéisés) /
  `NA` (juvénile) ;
- 2070 lignes renseignées, 36 corrigées, 81 sans mesure (individus séquencés
  absents du xlsx), 0 en conflit ;
- **conflits résolus** : 3 individus (`15Jus1006/1007/1008`) avaient deux jeux
  de mesures divergents dans le xlsx. Valeurs faisant autorité fournies par le
  collègue (2026-07-25), saisies dans `MESURES_CORRIGEES` (`merge_metadata.py`),
  flag `mesures_corrigees`. Le mécanisme reste en place si d'autres conflits
  apparaissent (un champ divergent non corrigé serait laissé vide + flag
  `mesures_conflit`) ;
- le xlsx porte aussi `Species` (Cn/Pt/Ch/**Hy** = hybride), **non repris** : le
  statut taxonomique fin des `Ch` est en cours de caractérisation et sera intégré
  au fichier dès qu'il sera disponible.

### Renommage des fastq bruts
Les corrections d'espèce (1036–1043) et de tissu (04→05) ont aussi été
appliquées **aux noms de fichiers fastq et aux SampleSheet** des trois runs, via
`scripts/rename_fastq.py` (320 fichiers). Le renommage est réversible :

- `metadata/rename_manifest.csv` (versionné) : correspondance ancien → nouveau ;
- une sauvegarde `SampleSheet.csv.orig` à côté de chaque feuille modifiée ;
- annulation : `python3 scripts/rename_fastq.py --revert metadata/rename_manifest.csv --data-root data`.

L'appariement fastq ↔ SampleSheet se fait par le numéro `_S{n}`, donc le
renommage ne dépend pas de ces corrections et reste rejouable. Les flags de
provenance (`taxon_saisi_manuellement`, `tissu_corrige`) subsistent après
renommage : on garde trace de ce qui a été corrigé et pourquoi.

Seuls ces deux cas ont été renommés. Les casses de site (`15BUe`→`Bue`), les
séparateurs et le suffixe `bis` **ne sont pas** touchés dans les fichiers : ils
restent régularisés dans les seules métadonnées.

## Structure
```
microbiome-hybrid/
├── scripts/
│   ├── job_template.sh     ← copier pour chaque nouveau job
│   ├── check_run.sh        ← vérifier un run
│   ├── build_metadata.py   ← métadonnées d'un run
│   ├── merge_metadata.py   ← fusion + diagnostic du plan
│   └── rename_fastq.py     ← renommage réversible des fastq corrigés
├── config/
│   └── project.env         ← variables communes
├── consolidated_dataset/   ← SOURCE UNIQUE des fastq pour l'analyse
│   └── durance{1,2,3}/     ← R1/R2 .fastq.gz, un sous-dossier par run
├── data/                   ← run dirs d'origine (SampleSheet, InterOp, I1/I2…)
├── metadata/
│   ├── samples_durance{1,2,3}.csv
│   ├── samples_all.csv     ← fichier combiné, 2304 lignes (+ size_cm/weight_g/sex)
│   ├── HotuToxo_taillepoids.xlsx  ← mesures par individu (source)
│   ├── rename_manifest.csv ← ancien → nouveau nom de fastq
│   └── consolidate_manifest.csv ← déplacement data/ → consolidated_dataset/
├── results/                ← {jobname}_{jobid}/ par run
├── logs/                   ← .out / .err SLURM
├── docs/                   ← notes, protocoles
└── runs.log                ← registre de tous les jobs
```

### Régénérer les métadonnées
```bash
python3 scripts/build_metadata.py data/durance1/170710_M03930_0062_000000000-BBHKV \
        metadata/samples_durance1.csv --label durance1
python3 scripts/build_metadata.py data/durance2/16S-Dur2_renamed \
        metadata/samples_durance2.csv --label durance2
python3 scripts/build_metadata.py data/durance3/171103_M03930_0072_000000000-BFWT5 \
        metadata/samples_durance3.csv --label durance3
python3 scripts/merge_metadata.py metadata/samples_durance?.csv \
        -o metadata/samples_all.csv --measurements metadata/HotuToxo_taillepoids.xlsx
```
(`merge_metadata.py --measurements` requiert `openpyxl` : `pip install openpyxl`.)

## Procédure
```bash
cp scripts/job_template.sh scripts/mon_job.sh
# éditer mon_job.sh ...
git add -A && git commit -m "feat: description"
sbatch scripts/mon_job.sh
bash scripts/check_run.sh results/mon_job_JOBID
```
