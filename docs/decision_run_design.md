# docs/decision_run_design.md — Structure reelle des 3 runs de sequencage

## Decision (2026-08-23)
Le design de replication est **emboite**, pas plat. Il ne doit PAS etre modelise
comme un facteur `run` a trois niveaux interchangeables.

```
PCR / librairie A (i5 = SC501) --> durance1   flow cell BBHKV, run Illumina #62, 10/07/2017
PCR / librairie B (i5 = SB501) -+-> durance2   flow cell BCFFD, run Illumina #69, 05/10/2017
                                +-> durance3   flow cell BFWT5, run Illumina #72, 03/11/2017
```

## Comment on l'a etabli
Le design initialement transmis etait different (durance2 = memes PCR que durance1
avec normalisation refaite ; durance3 = resequencage de durance2). Les donnees le
contredisent. Quatre temoins independants :

1. **Index i5** — i7 identique dans les 3 runs, mais i5 = SC501 pour durance1 et
   SB501 pour durance2/3 (sequences reellement differentes). Le protocole etant
   **1-step** (index incorpore pendant la PCR), une reindexation d'un pool existant
   est impossible : un i5 different implique necessairement une PCR distincte.
   Confirme par l'experimentateur : durance2 a fait l'objet d'une nouvelle PCR.
2. **Dissimilarite intra-echantillon** (548 echantillons a >=3000 lectures dans les
   3 runs, rarefies a profondeur egale) — script 13-run_design.sh :

   | paire | Bray-Curtis | Jaccard | recapture ASV rares |
   |---|---|---|---|
   | durance1 vs durance2 | 0.248 | 0.722 | 0.196 |
   | durance1 vs durance3 | 0.248 | 0.719 | 0.193 |
   | **durance2 vs durance3** | **0.118** | **0.445** | **0.484** |

   Les deux paires traversant les librairies sont indiscernables entre elles
   (Wilcoxon apparie sur Bray, p = 0.48) et toutes deux differentes de la paire
   intra-librairie (p < 1e-89).
3. **Recapture des ASV rares** (1-3 lectures) — 0.484 intra-librairie contre 0.19
   inter-librairies : les variants rares de durance3 se retrouvent dans durance2
   deux fois plus souvent que dans durance1, signature d'un pool partage.
4. **Correlation des profondeurs brutes** — Spearman 0.9987 entre d2 et d3, 0.79
   entre d1 et les autres.

## Controles negatifs du raisonnement
- d2 et d3 sont bien deux sequencages DISTINCTS : md5 differents, tailles
  differentes, deux flow cells (BCFFD / BFWT5), deux numeros de run Illumina
  (#69 / #72). La forte similarite n'est pas un artefact de fichiers dupliques.
- Le desaccord etait possible : si les trois runs avaient partage un pool unique,
  les trois paires seraient ressorties equivalentes.

## Ce que le test NE tranche PAS
La dissimilarite d1 vs {d2,d3} agrege tout ce qui differe entre les deux
preparations (PCR, normalisation, pooling). On ne peut pas attribuer la part de
chacune de ces etapes.

## Ce que le design fournit — deux niveaux emboites
- **d2 vs d3** = variabilite de **sequencage seul** (meme pool, 2 flow cells).
  Bray = 0.118. Plancher technique irreductible.
- **d1 vs {d2,d3}** = variabilite de **preparation de librairie + sequencage**.
  Bray = 0.248. Plafond technique.

La preparation double donc la dissimilarite technique. L'effet est
proportionnellement plus fort sur la presence/absence (Jaccard 0.72 vs 0.45) que
sur les abondances relatives : la preparation change surtout QUELS taxons rares
sont detectes.

## Consequences pour l'analyse
1. **Modelisation** : sequencage niche dans preparation de librairie, p. ex.
   `(1|library/run)` en effet aleatoire, ou un facteur `library` a 2 niveaux avec
   `run` niche. Ne pas utiliser `run` a 3 niveaux plats.
2. **Metriques sensibles aux ASV rares** (richesse observee, Jaccard, indices de
   diversite non ponderes) : peu reproductibles meme entre deux sequencages du meme
   pool (Jaccard 0.445). A eviter sans agregation entre runs, ou a accompagner d'une
   mesure de reproductibilite.
3. **decontam** a ete lance avec `batch = run` (3 niveaux). Ce choix reste
   defendable — il est conservateur, chaque sequencage ayant son propre profil de
   contamination — mais il ne reflete pas la structure emboitee. Non repris : la
   decontamination est figee et le seuil 0.1 retire 0.15 % des ASV seulement.

## Reste a confirmer
La "normalisation refaite" mentionnee dans le design initial s'appliquait-elle a
la librairie B par rapport a la librairie A, ou a l'interieur du couple d2/d3 ?
Sans consequence sur la modelisation (la structure emboitee est etablie), mais
utile pour la redaction.

## Fichiers
- `scripts/13-run_design.sh` — test reproductible
- `results/run_design/run_design_summary.txt` — synthese
- `results/run_design/pairwise_per_sample.tsv` — les 3 dissimilarites par echantillon
