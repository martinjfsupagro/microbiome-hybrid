# microbiome-hybrid

## Description
Comparative analysis of the 16S microbiota of several tissues in nase
(*Chondrostoma nasus*), South-west European nase (*Parachondrostoma toxostoma*)
and their hybrids, across several sites and two years (2014, 2015).

**Question**: is the hybrid microbiota intermediate between the two parental
species, or displaced outside their range?

### Sampling design
| Factor | Levels |
|---|---|
| Taxon  | nase (`Cn`) / toxostoma (`Pt`) / unresolved *Chondrostoma* (`Ch`) |
| Tissue | 4: caudal fin (`01`) / midgut (`02`) / hindgut (`03`) / gill (`05`) |
| Site   | Ain, Avi, Bau, Bue, Caa, Cab, Jus, Man, Per |
| Year   | 2014 / 2015 |

**Taxon codes.** `Ch` means a *Chondrostoma* **not yet identified** at this stage
(neither `Cn` nor `Pt` resolved) — it does **not** mean chub, as was first
assumed. Chub (*Squalius cephalus*, lab code `Sc`) is absent from these three
runs. Species-level identity (including hybrid status) is being genotyped and
will be delivered as a **hybrid index** per individual, from 0 (nase) to
1 (toxostoma); see `metadata/index_hybride_andre.csv`.

The design is strongly unbalanced: site and year are largely confounded (only Avi
and Bue span both years), as are taxon and site. See
[docs/donnees_durance1.md](docs/donnees_durance1.md).

### Data
| Batch | MiSeq run | Flow cell | n | Delivery | Status |
|---|---|---|---|---|---|
| `durance1` | 170710_M03930_0062 | BBHKV | 768 | run dir + SampleSheet | inventoried |
| `durance2` | M03930_0069 | BCFFD | 768 | renamed fastq + separate SampleSheet | inventoried |
| `durance3` | 171103_M03930_0072 | BFWT5 | 768 | run dir + SampleSheet | inventoried |

The three runs are **not** three sequencings of one library. The replication
structure is **nested**: the same 768 samples went through **two independent
one-step dual-index PCR library preparations**; the first was sequenced once
(`durance1`), the second twice on separate flow cells (`durance2`, `durance3`).
Establishing this took four converging lines of evidence — see
[docs/decision_run_design.md](docs/decision_run_design.md). Consequences:

- **Do not model `run` as a three-level factor with interchangeable levels.**
  Sequencing is nested within library preparation.
- Index assignment differs between preparations: relative to `durance1`, the i7
  index differs for 384 of the 768 libraries and the i5 index for 576, whereas
  `durance2` and `durance3` carry identical index pairs throughout. Because
  indices are incorporated during amplification in a one-step protocol, an
  existing amplicon pool cannot be re-indexed, so a different index assignment
  implies a distinct PCR.
- Every sample is present in all batches, so technical and biological factors
  are **crossed, not confounded**: batch-correction methods designed for
  confounded meta-analyses are unnecessary and were not applied.

Of the 768 samples, **727 are biological** and **41 are controls** (4 extraction
blanks, 8 no-template PCR controls, 4 mock aliquots, 25 empty wells), each
sequenced in all three runs.

`durance2` was delivered as demultiplexed fastq (uncompressed, controls in
`control/`) with no run dir. Its original SampleSheet, found separately
(`EG_16S_Durance_Run2.csv`, placed in the fastq folder), is auto-detected by
`build_metadata.py` and supplies plate, well and index — otherwise missing. Its
missing Sample_Name/Sample_Plate comma (name and plate number run together) is
fixed on read. All its rows keep the `nom_depuis_fichier` flag, names coming
from the files rather than from the sheet.

### Single fastq source: `consolidated_dataset/`
The **R1/R2 fastq of all three runs** were centralised into
`consolidated_dataset/<run>/` (4,608 files, all `.fastq.gz`) by
`scripts/consolidate_fastq.py`. This is the data source for the analysis; the
`fastq_r1`/`fastq_r2` columns of `samples_all.csv` point to it (paths relative
to the project root).

- **One subfolder per run**: durance1 and durance3 carry identical file names
  (same libraries) and would overwrite each other if flat. This also suits
  DADA2, which learns error rates per run.
- **durance2 compressed** to `.fastq.gz` in passing (delivered as `.fastq`).
- **R1/R2 only.** Index reads `I1/I2` (durance1/3) and `Undetermined` stay in
  `data/`, along with SampleSheets, InterOp, etc.
- **Reversible**: `metadata/consolidate_manifest.csv` (version-controlled);
  to undo: `python3 scripts/consolidate_fastq.py --revert metadata/consolidate_manifest.csv`
  (then regenerate the CSVs: build + merge).

### The `bis` suffix: re-extraction
`bis` denotes a **second DNA extraction from the same tissue**, not a second
sampling. Hence the `extraction` column (`initiale` / `bis`), which is part of
the replicate key: 9 tissues were extracted twice, i.e. 27 rows. Merging them
with their initial extraction would make an extraction effect look like a run
effect.

Two of these `bis` were mis-entered: `-bis` inside the durance2 file names
(Illumina conversion), and a missing suffix for `14Bue1006Cn05A` in well C07 of
the durance1 SampleSheet. The latter is fixed in `NOMS_CORRIGES`
(`build_metadata.py`), flag `nom_corrige` — the well is the same in all three
runs, so the identification is certain.

### Tissue code to tissue
Confirmed (colleague, 2026-07-25) and consistent with the plate layout:

| Code | Tissue |
|---|---|
| `01` | caudal fin |
| `02` | midgut |
| `03` | hindgut |
| `05` | gill |

### Taxon of individuals 1036-1043 (Ain 2014)
The species-code entry block was missing. Filled in from the field sheet
(`TAXON_MANUEL` in `build_metadata.py`, flag `taxon_saisi_manuellement`):
1036-1037 = nase (`Cn`), 1038-1043 = toxostoma (`Pt`). These individuals are
therefore not a separate group.

### Tissue code 04 to 05
`15Avi1002Cn04A` carried an `04` confirmed to be a typo for `05` (gill); the
individual recovers its 01/02/03/05 set. Fixed via `TISSU_CORRIGE`
(`build_metadata.py`), flag `tissu_corrige`.

### Length / weight / sex (HotuToxo_taillepoids.xlsx)
Columns `size_cm`, `weight_g` and `sex` are added to `samples_all.csv` by
`merge_metadata.py` (`--measurements` option), from
`metadata/HotuToxo_taillepoids.xlsx`. These are **per-individual** data: joined
on (year, site, individual) — **without** taxon, since the fish is the same
whatever its label — and propagated to all its tissues and all runs.

- length in cm, weight in g;
- `sex`: `M` / `F` / `X` (undetermined — the xlsx's `x` and `X` homogenised) /
  `NA` (juvenile);
- 2,070 rows filled, 36 corrected, 81 without measurement (sequenced individuals
  absent from the xlsx), 0 in conflict;
- **conflicts resolved**: 3 individuals (`15Jus1006/1007/1008`) had two divergent
  sets of measurements in the xlsx. Authoritative values supplied by the
  colleague (2026-07-25), entered in `MESURES_CORRIGEES` (`merge_metadata.py`),
  flag `mesures_corrigees`. The mechanism stays in place should further
  conflicts appear (an uncorrected divergent field would be left empty with a
  `mesures_conflit` flag);
- the xlsx also carries `Species` (Cn/Pt/Ch/**Hy** = hybrid), **not used**: the
  fine taxonomic status of the `Ch` is being characterised and will be
  integrated as a hybrid index when available.

### Renaming of raw fastq
The species (1036-1043) and tissue (04 to 05) corrections were also applied **to
the fastq file names and the SampleSheets** of all three runs, via
`scripts/rename_fastq.py` (320 files). The renaming is reversible:

- `metadata/rename_manifest.csv` (version-controlled): old to new mapping;
- a `SampleSheet.csv.orig` backup beside each modified sheet;
- to undo: `python3 scripts/rename_fastq.py --revert metadata/rename_manifest.csv --data-root data`.

fastq-to-SampleSheet matching uses the `_S{n}` number, so the renaming does not
depend on these corrections and remains reversible.

## Pipeline
```
01  QC          FastQC + MultiQC per run
02  12S removal cutadapt: co-amplified host 12S (15-67 % of reads) is removed
                by LENGTH (12S insert ~190 bp vs V4 ~253 bp); too-short kept
                (host signal). Per run.
04  DADA2       filterAndTrim truncLen c(230,190) + learnErrors PER RUN + dada +
                mergePairs -> seqtab_<run>.rds (raw). Per run.
05  merge+tax   mergeSequenceTables (samples suffixed __run -> 2,304 columns)
                + removeBimeraDenovo + assignTaxonomy SILVA + Mitochondria/
                Chloroplast/Eukaryota filter.
06  mock        blastn of mock ASVs against the ZymoBIOMICS 16S reference.
07  decontam    reagent contaminants from negative controls.
08  phylogeny   de-novo tree (MAFFT + FastTree2) for UniFrac / Faith PD.
09  depth QC    depth distribution and rarefaction curves.
10  crosstalk   index hopping quantified from the empty wells.
11  QC flags    annotation of mock-composition samples (join table).
12  clean table single canonical analysis table.
13  run design  characterisation of the nested replication structure.
14  variance    biological vs technical variance partition.
15  rarefaction repeated rarefaction: alpha and beta, convergence.
```
Launching (each launcher submits one job per run and requires a clean git tree):
```bash
cd ~/work/projects/microbiome-hybrid
bash scripts/01-quality_check_launcher.sh          # QC (optional, in parallel)
bash scripts/02-remove_12S_launcher.sh             # -> note the 3 job IDs
bash scripts/04-dada2_launcher.sh --after J1:J2:J3 # afterok, order = durance1/2/3
sbatch scripts/05-merge_taxonomy.sh                # after the 3 dada2 jobs
```
Key choices (measured on the data, see script headers): `-O 10`,
`--minimum-length 240` for the 12S; `learnErrors` per run because these are
distinct sequencings; chimeras on the merged table.

**MESO@LR pitfall**: the default QOS on `ondemand@biomics` is `ondemand-short`,
capped at **1 hour**. Any job with `--time` above that hangs PENDING with
`QOSMaxWallDurationPerJobLimit`. Add `#SBATCH --qos=cpu-ondemand-long`.

### Results (results/dada2_final/)
| Step | Figure |
|---|---|
| 12S removed | ~15 % of reads/run (up to 67 % per sample) |
| Pair merging (median) | 92.7-94.3 % depending on run |
| Raw ASVs per run | 26,128 / 27,605 / 29,197 |
| After merging the 3 runs | 2,295 samples x 48,819 ASVs |
| After chimeras | **46,320 ASVs** (98.0 % of reads kept) |
| ASV length | peak at 251 bp (V4; no 12S residue) |

2,295 samples rather than 2,304: 9 dropped as empty after filtering (8 `empty`
controls + `15Bue1014Ch03A` on durance3, present in the two other runs). Files:
`asv_table.tsv` (ASV x sample), `asv.fasta`, `seqtab_nochim.rds`,
`track_all.csv`.

**Joining table to metadata**: the columns of `asv_table.tsv` are named
`{sample}__{run}` (e.g. `14Ain1001Cn01A__durance1`). The `dada2_id` column of
`samples_all.csv` carries exactly this key — it is the join to the sampling
design (taxon, tissue, site, length/weight, etc.).

### Taxonomy (SILVA v138.2)
Reference in `$WORK/shared_softwares/silva/`, via `SILVA_TRAIN`/`SILVA_SPECIES`.
`assignTaxonomy` replicates the database per thread, hence a large memory peak:
**256G** required for step 05 (64G ran out of memory).

Assignment (on 46,320 ASVs): Kingdom 100 %, Phylum 98.6 %, Order 90.3 %,
Family 77.1 %, Genus 46.7 %, Species 2.1 % (typical of V4). Dominant phyla:
Pseudomonadota, Bacteroidota, Planctomycetota, Verrucomicrobiota.

**Off-target filter: 1,971 ASVs removed** — 1,144 Mitochondria, 784 Chloroplast,
22 Eukaryota, 21 unassigned. The 1,144 mitochondrial ASVs are residual host 12S
(passed at full length, not caught by the length filter in step 02): the
taxonomic net catches them, as intended.

-> **`asv_table_filtered.tsv`: 44,349 ASVs x 2,295 samples**, `taxonomy.tsv`,
`seqtab_nochim_filtered.rds`. Joined to the sampling design by `dada2_id`.

## Downstream analysis
Every decision below is recorded in `docs/decision_*.md`, with the criterion
used, what was measured, and what remains open.

| Step | Outcome | Note |
|---|---|---|
| Mock validation | 8/8 expected species at 100 % identity, no spurious ASV | see `results/mock_validation/` |
| Decontamination | conservative threshold; 66 contaminants, 99.76 % of reads kept | `decision_decontam.md` |
| Index hopping | 41 reads out of 26.8 M in the empty wells (0.0002 %) — negligible | `decision_crosstalk.md` |
| Mock artefacts | 2 samples reclassified as mislabelled mocks; 20 wells with mock reads, ASVs removed rather than samples excluded | `decision_mock_samples.md`, `decision_mock_removal.md` |
| Analysis table | **2,180 samples x 44,200 ASVs** | `results/decontam/asv_table_clean.tsv` |
| Phylogeny | de-novo MAFFT + FastTree2, one leaf per ASV | `results/phylogeny/tree.nwk` |
| Rarefaction | threshold 3,000 reads (81.8 % of samples kept), repeated rarefaction, metrics averaged | `decision_rarefaction.md`, `decision_rarefaction_mode.md` |
| Variance partition | technical 0.03 % vs tissue 9.2 % and fish identity 37.7 % | `results/var_partition/` |

**Still pending the hybrid index**: statistical models, hybrid-zone gradient
contrasts, and the final choice of retained populations.

## Structure
```
microbiome-hybrid/
├── scripts/
│   ├── 01-quality_check_{launcher,worker}.sh  <- FastQC/MultiQC per run
│   ├── 02-remove_12S_{launcher,worker}.sh     <- cutadapt 12S removal per run
│   ├── 04-dada2_{launcher,worker}.sh          <- DADA2 per run
│   ├── 05-merge_taxonomy.sh                   <- merge + chimeras + taxonomy
│   ├── 06-validate_mock.sh                    <- mock validation (blastn)
│   ├── 07-decontam.sh                         <- decontamination
│   ├── 08-phylogeny.sh                        <- de-novo tree
│   ├── 09-qc_depth.sh                         <- depth QC + rarefaction curves
│   ├── 10-crosstalk.sh                        <- index hopping
│   ├── 11-flag_mock_samples.py                <- QC flags (join table)
│   ├── 12-clean_table.py                      <- canonical analysis table
│   ├── 13-run_design.sh                       <- replication structure
│   ├── 14-variance_partition.sh               <- variance partition
│   ├── 15-rarefaction_converge.sh             <- repeated rarefaction
│   ├── lib_samples.sh      <- shared functions (R1/R2 pairing)
│   ├── job_template.sh     <- copy for each new job
│   ├── check_run.sh        <- check a run
│   ├── build_metadata.py   <- metadata for one run
│   ├── merge_metadata.py   <- merge + design diagnostics
│   └── rename_fastq.py     <- reversible renaming of corrected fastq
├── config/
│   └── project.env         <- shared variables
├── consolidated_dataset/   <- SINGLE fastq SOURCE for the analysis
│   └── durance{1,2,3}/     <- R1/R2 .fastq.gz, one subfolder per run
├── data/                   <- original run dirs (SampleSheet, InterOp, I1/I2…)
├── metadata/
│   ├── samples_durance{1,2,3}.csv
│   ├── samples_all.csv     <- combined file, 2,304 rows (+ size_cm/weight_g/sex)
│   ├── site_mapping.csv    <- site code -> ecological site (join, no renaming)
│   ├── sample_qc_flags.csv <- QC flags (join, no renaming)
│   ├── index_hybride_andre.csv <- hybrid index to be filled in (181 individuals)
│   ├── HotuToxo_taillepoids.xlsx  <- per-individual measurements (source)
│   ├── rename_manifest.csv <- old -> new fastq name
│   └── consolidate_manifest.csv <- data/ -> consolidated_dataset/ moves
├── ena_deposit/            <- ENA submission (scripts, XML, receipts)
├── results/                <- {jobname}_{jobid}/ per run (not versioned)
├── logs/                   <- SLURM .out / .err
├── docs/                   <- notes, decisions, manuscript
└── runs.log                <- register of every job
```

**Sample names are never changed.** Corrections and reclassifications go through
**join tables** (`site_mapping.csv`, `sample_qc_flags.csv`) joined on
`site_code` or `dada2_id`; `samples_all.csv` is left untouched.

### Regenerating the metadata
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
(`merge_metadata.py --measurements` requires `openpyxl`: `pip install openpyxl`.)

## Working procedure
```bash
cp scripts/job_template.sh scripts/my_job.sh
# edit my_job.sh ...
git add -A && git commit -m "feat: description"
sbatch scripts/my_job.sh
bash scripts/check_run.sh results/my_job_JOBID
```

## Data availability
Raw reads are deposited in the European Nucleotide Archive under accession
**PRJEB124417** (768 samples, 2,304 runs, 4,608 FASTQ files). Per-run accessions
and checksums: `docs/manuscrit/ENA_accessions_durance.tsv`.

## GitHub remote
The repository is mirrored at
**https://github.com/martinjfsupagro/microbiome-hybrid** (**private**, branch
`main`), with author identity preserved.

Until this mirror existed, the history lived in exactly one place: `.git` on
meso. Losing that filesystem would have taken the traceability of every analysis
decision with it.

### Pushing from meso
The `origin` remote is configured, but **no credential is stored on the
cluster** — deliberately: a GitHub token on a shared cluster is an avoidable
risk.

```bash
cd ~/work/projects/microbiome-hybrid
git push origin main      # prompts for username + token
```
GitHub no longer accepts passwords: at the "Password" prompt, paste a Personal
Access Token (Settings > Developer settings > Tokens, `repo` scope).

To avoid retyping it without writing it in clear text:
```bash
git config --global credential.helper 'cache --timeout=3600'
```
Note: `credential.helper` is currently set to `store`, which would write the
token in clear text to `~/.git-credentials`. Prefer `cache` on a shared machine.

Alternatively, the history can be transferred as a git bundle
(`git bundle create ... --all`) and pushed from elsewhere, so that no credential
ever reaches the cluster. That is how the first push was done.

### Visibility
The repository is **private** by explicit choice: the manuscript is not
submitted, and the decision notes contain points awaiting the collaborator's
input. Switching to public is one click away at submission time. The reverse is
not true — a repository made public cannot be un-published, since clones and
caches persist.

### Not version-controlled
`results/` (large, regenerable from the scripts), `consolidated_dataset/` (12 GB
of raw FASTQ, deposited at the ENA under PRJEB124417), the per-run webin
outputs, and stray job-output copies at the repository root.
