# microbiome-hybrid

## Description
Analyse comparative du microbiome (16S) de plusieurs tissus chez le hotu, le
toxostome et leurs hybrides, sur plusieurs sites et deux années (2014, 2015).

**Question** : le microbiome des hybrides est-il intermédiaire entre les deux
espèces parentales, ou déplacé hors de leur intervalle ?

### Plan d'échantillonnage
| Facteur | Niveaux |
|---|---|
| Taxon    | hotu / toxostome / hybride |
| Tissu    | *(à compléter)* |
| Site     | *(à compléter)* |
| Année    | 2014 / 2015 |

Facteurs croisés → prévoir les effets site et année comme covariables, et
vérifier l'équilibre du plan (taxon × tissu × site × année) avant tout test.

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
