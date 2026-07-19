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
| Lot | Run | n | État |
|---|---|---|---|
| `durance1` | 170710_M03930_0062 | 768 | extrait, inventorié |

## Structure
```
microbiome-hybrid/
├── scripts/
│   ├── job_template.sh   ← copier pour chaque nouveau job
│   └── check_run.sh      ← vérifier un run
├── config/
│   └── project.env       ← variables communes
├── results/              ← {jobname}_{jobid}/ par run
├── logs/                 ← .out / .err SLURM
├── docs/                 ← notes, protocoles
└── runs.log              ← registre de tous les jobs
```

## Procédure
```bash
cp scripts/job_template.sh scripts/mon_job.sh
# éditer mon_job.sh ...
git add -A && git commit -m "feat: description"
sbatch scripts/mon_job.sh
bash scripts/check_run.sh results/mon_job_JOBID
```
