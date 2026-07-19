# microbiome-hybrid

## Description
Analyse comparative du microbiome (16S) de plusieurs tissus chez le hotu, le
toxostome et leurs hybrides, sur plusieurs sites et deux années (2014, 2015).
Le chevesne, cyprinidé sympatrique qui n'hybride pas avec ce couple, sert
d'espèce de référence.

**Question** : le microbiome des hybrides est-il intermédiaire entre les deux
espèces parentales, ou déplacé hors de leur intervalle ?

### Plan d'échantillonnage
| Facteur | Niveaux |
|---|---|
| Taxon    | hotu (`Cn`) / toxostome (`Pt`) / chevesne (`Ch`) — statut hybride hors nomenclature |
| Tissu    | 4 : caudale, branchie, midgut, hindgut (code ↔ tissu à confirmer) |
| Site     | Ain, Avi, Bau, Bue, Caa, Cab, Jus, Man, Per |
| Année    | 2014 / 2015 |

Plan très déséquilibré : site et année sont largement confondus (seuls Avi et
Bue couvrent les deux années), de même que taxon et site. Voir
[docs/donnees_durance1.md](docs/donnees_durance1.md).

### Données
| Lot | Run MiSeq | Flowcell | n | Livraison | État |
|---|---|---|---|---|---|
| `durance1` | 170710_M03930_0062 | BBHKV | 768 | run dir + SampleSheet | inventorié |
| `durance2` | M03930_0069 | BCFFD | 768 | fastq renommés, sans SampleSheet | inventorié |
| `durance3` | 171103_M03930_0072 | BFWT5 | 768 | run dir + SampleSheet | inventorié |

Les trois runs sont **le reséquençage des mêmes 768 librairies** (même plan de
plaque, mêmes i7 ; seuls les i5 changent d'un run à l'autre). Chaque échantillon
est donc présent en triple : 720 réplicats techniques inter-runs, plus les
39 contrôles × 3. L'effet run est estimable directement — il n'est confondu avec
aucun facteur biologique.

durance2 est livré sans SampleSheet : les métadonnées y sont reconstruites
depuis les noms de fichiers, et les colonnes de plaque et d'index restent vides
(elles ne sont pas reprises d'un autre run). D'où le flag `nom_depuis_fichier`
sur toutes ses lignes.

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

### Points en suspens sur les métadonnées
- **`15Avi1002Cn04A`** : seul échantillon en code tissu `04`, présent dans les
  trois runs (flag `tissu_inattendu`). Saisie ou 5ᵉ tissu ? → à voir avec le
  collègue qui a acquis les données.
- **Ain 2014, individus 1036 à 1043 : taxon non saisi.** Leurs noms portent une
  espace là où devraient figurer les deux lettres du taxon (`14Ain1036 01A` au
  lieu de `14Ain1036Cn01A`). Les 8 individus se suivent, c'est un bloc de saisie
  entier qui manque, soit 31 échantillons sur les 4 tissus. Le taxon n'est pas
  déductible : Ain 2014 contient à la fois du hotu (1001–1002) et du toxostome
  (1011–1014), et ces 8 individus forment une troisième série de numéros qui
  n'existe nulle part ailleurs. Il faut la feuille de terrain.
- Le code tissu (`01/02/03/05`) n'est toujours pas relié à un tissu nommé
  (`TISSUS` vide dans `build_metadata.py`).

## Structure
```
microbiome-hybrid/
├── scripts/
│   ├── job_template.sh     ← copier pour chaque nouveau job
│   ├── check_run.sh        ← vérifier un run
│   ├── build_metadata.py   ← métadonnées d'un run
│   └── merge_metadata.py   ← fusion + diagnostic du plan
├── config/
│   └── project.env         ← variables communes
├── data/                   ← un dossier par lot
├── metadata/
│   ├── samples_durance{1,2,3}.csv
│   └── samples_all.csv     ← fichier combiné, 2304 lignes
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
python3 scripts/merge_metadata.py metadata/samples_durance?.csv -o metadata/samples_all.csv
```

## Procédure
```bash
cp scripts/job_template.sh scripts/mon_job.sh
# éditer mon_job.sh ...
git add -A && git commit -m "feat: description"
sbatch scripts/mon_job.sh
bash scripts/check_run.sh results/mon_job_JOBID
```
