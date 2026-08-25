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

1. **Assignation des index** (CORRIGE 2026-08-25 — voir note ci-dessous) — le meme
   jeu de 768 combinaisons i7 x i5 sert aux deux preparations, mais l'assignation des
   paires aux puits differe. Sur les 768 librairies, par rapport a durance1 :
   **l'i7 differe pour 384** et **l'i5 pour 576** ; durance2 et durance3 portent des
   paires **identiques sur les 768**. Le protocole etant **1-step** (index incorpore
   pendant la PCR), une reindexation d'un pool existant est impossible : une
   assignation d'index differente implique necessairement une PCR distincte.
   Confirme par l'experimentateur : durance2 a fait l'objet d'une nouvelle PCR.

   NOTE DE CORRECTION. Une version anterieure de ce document affirmait que l'i7 etait
   *identique dans les 3 runs* et que seul l'i5 changeait. C'etait FAUX : cette
   affirmation venait de l'inspection de la seule plaque 1 (SC501 vs SB501) et avait
   ete generalisee a tort aux 768 librairies. Verification sur l'ensemble des
   librairies : i7 differe 384/768, i5 differe 576/768 entre durance1 et durance2/3 ;
   d2-d3 : 0/768 pour les deux. **La conclusion est inchangee et meme renforcee** —
   durance2/durance3 partagent une preparation, durance1 en est une autre — mais la
   caracterisation etait inexacte.
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

## Controle d'assignation echantillon-fichier (ajout 2026-08-25)

**Question.** L'assignation des index differant entre les deux preparations de librairie
(i7 : 384/768, i5 : 576/768), un echange d'etiquettes entre echantillons etait concevable.

**Test.** Pour chaque librairie, recherche de son plus proche voisin en composition
bacterienne (Bray-Curtis) parmi les replicats des autres runs. Un etiquetage correct
predit que le plus proche voisin d'une librairie est son propre replicat.
Fichier de resultat : `results/run_design/identity_check.tsv` (2027 comparaisons).
Test realise dans la session de depot ENA (frame 90e7af1c), verifie ici sur le fichier.

**Resultats.**
| mesure | valeur |
|---|---|
| auto-appariements | 1891/2027 = 93.3 % |
| entre runs partageant une preparation (d2 vs d3) | 99.7 % |
| entre preparations (d1 vs d2, d1 vs d3) | 89.8 % / 90.1 % |
| plaques dont l'assignation d'index a change (3,4,5,6) | **96.5 %** (n=1019) |
| plaques inchangees (1,2,7,8) | **90.1 %** (n=1008) |
| echecs reciproques (signature d'un vrai echange) | **0 / 136** |
| dissimilarite self, mediane : echecs vs succes | 0.532 vs 0.133 |

**Conclusion.** Deux temoins independants excluent l'erreur d'etiquetage :
1. les plaques dont l'assignation d'index a change s'auto-apparient MIEUX que les
   plaques inchangees (96.5 % vs 90.1 %) — l'inverse de ce qu'un brouillage produirait ;
2. aucun des 136 echecs n'est reciproque, alors qu'un echange A<->B laisse par
   construction une paire pointant mutuellement.
Les echecs sont des echantillons peu reproductibles (dissimilarite self mediane 0.53
contre 0.13), concentres sur la nageoire caudale — le tissu de plus faible biomasse.

**ATTENTION a la formulation.** Une version du supplementaire ecrivait
"no reciprocal mismatch was observed (0 of 136 discordant pairs), excluding a labelling
error", ce qui laissait entendre 136 comparaisons dont 0 en echec. En realite il y a
**136 echecs** sur 2027 comparaisons, dont 0 reciproque. Le taux d'auto-appariement
global est de 93.3 %, pas de 100 %. Corrige dans Supplementary_Data.docx (v2).
