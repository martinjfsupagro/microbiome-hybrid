# docs/decision_decontam.md — Choix du seuil de décontamination

## Décision
La table d'analyse de référence après décontamination est **le seuil decontam
0,1** (défaut). Fichier canonique :
`results/decontam/asv_table_analysis.tsv` (copie de `asv_table_decontam_p01.tsv`).

**Dimensions : 44 256 ASV × 2186 échantillons biologiques, 26 546 494 lectures.**

## Méthode
- Paquet : decontam 1.30.0 (Davis et al. 2018), méthode `prevalence`.
- Témoins négatifs : le manuscrit d'origine décrit le plan de contrôles PAR LOT —
  « four extraction negative controls and eight amplification negative controls »
  (soit 4 + 8 = 12 par lot). Dans les données Durance, ces contrôles correspondent
  aux 4 blancs d'extraction par tissu (`Blanc-*`) et aux 8 témoins PCR (`T-1..T-8`),
  chacun séquencé dans les 3 runs → **12 blancs d'extraction + 24 témoins PCR = 36
  échantillons-contrôles au total** (vérifié dans la table). C'est le manuscrit qui
  confirme la NATURE (extraction vs PCR) ; le total de 36 est propre à ce jeu (×3 runs).
- `batch` = run de séquençage (durance1/2/3).
- Mocks (témoins positifs) et puits vides `empty` (crosstalk) exclus de l'analyse.

## Comparaison des seuils
| Seuil | Contaminants retirés | ASV conservés | Lectures conservées |
|---|---|---|---|
| **0,1 (retenu)** | 66 (0,15 %) | 44 256 | 99,76 % |
| 0,5 (sensibilité) | 100 (0,23 %) | 44 222 | 97,87 % |

Les 66 contaminants du seuil 0,1 sont taxonomiquement cohérents avec des
contaminants de réactifs (Pseudomonadaceae, Moraxellaceae, Micrococcaceae,
Propionibacteriaceae, Streptococcaceae…).

## Pourquoi 0,1 et pas 0,5
Le seuil 0,5 retire 34 ASV de plus (2,12 % des lectures), dont des taxons
**biologiquement attendus**, ce qui traduit une perte de signal, pas un gain de
propreté. Cas décisif : **ASV0065 = Candidatus Branchiomonas** (bactérie
branchiale de poissons), dont la distribution prouve qu'il s'agit de signal réel :

| Compartiment | n | présents | lectures |
|---|---|---|---|
| Témoins négatifs (36) | 36 | 1 (2,8 %) | 2 |
| — dont témoins PCR (24) | 24 | 0 | 0 |
| Puits vides (67) | 67 | 0 | 0 |
| Biologiques (2186) | 2186 | 109 (5,0 %) | 60 835 |
| — branchie | 546 | 50 (9,2 %) | 4 463 |
| — caudale | 552 | 41 (7,4 %) | 4 909 |
| — midgut | 543 | 7 (1,3 %) | 1 862 |
| — hindgut | 545 | 11 (2,0 %) | 49 601 |

→ ~60 835 lectures côté biologique contre 2 côté négatifs (rapport ~30 000×),
prévalence maximale en branchie (tissu attendu). Un contaminant de réactif
montrerait le schéma inverse. 0,5 amputerait donc du signal biologique.

## Formulation pour l'article (Methods)
« Contaminant ASVs were identified with decontam (v1.30.0; Davis et al. 2018)
using the prevalence method, with the 36 sequenced negative controls
(12 extraction blanks, 24 no-template PCR controls) as the negative set and the
sequencing run as batch. The default threshold (0.1) removed 66 ASVs (0.15% of
ASVs; 0.24% of reads), taxonomically consistent with common reagent
contaminants. A stringent threshold (0.5) was evaluated for sensitivity but not
retained, as it additionally flagged host-associated taxa expected in this
system — notably Candidatus Branchiomonas, present in 9.2% of gill samples yet
virtually absent from negative controls — indicating loss of genuine biological
signal. »

## Reproductibilité
Script : `scripts/07-decontam.sh` (commits 4fad253 …). Table de sensibilité 0,5
conservée : `results/decontam/asv_table_decontam_p05.tsv`.
