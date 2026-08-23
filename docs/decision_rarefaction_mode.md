# docs/decision_rarefaction_mode.md — Mode d'application de la rarefaction

## Decision (2026-08-23)
**Rarefactions repetees, moyenne des METRIQUES** (jamais des tables).
- **alpha : N = 1000** tirages (decision utilisateur, executee).
- **beta : N = 100 suffisant** ; les matrices livrees en portent 400.

Complete `decision_rarefaction.md` (seuil = 3000 lectures), qui laissait le MODE ouvert.

## Pourquoi on moyenne les metriques et pas les tables
Moyenner les 1000 tables rarefiees produirait une table dont les cellules non nulles
sont l'UNION des detections sur 1000 tirages. La richesse observee y serait gonflee et
ne correspondrait plus a une profondeur de 3000 — exactement le biais que la
rarefaction doit supprimer. On moyenne donc les indices alpha et les matrices de
distances, pas les comptages.

## Resultat alpha (N = 1000)
1784 echantillons. Ecart-type de Monte-Carlo median :

| indice | moyenne mediane | sd_MC | erreur relative |
|---|---|---|---|
| Shannon | 3.01 | 0.023 | 0.83 % |
| richesse observee | 111.6 | 2.368 | 1.95 % |
| inverse Simpson | 8.43 | 0.209 | 2.47 % |

Hierarchie coherente avec la sensibilite aux taxons rares : Shannon (pondere par
l'abondance) est le plus stable, la richesse (chaque ASV rare compte pour 1) le moins.
Argument supplementaire pour privilegier les metriques ponderees.

## Resultat beta — convergence
### Comment elle a ete mesuree
Comparer une moyenne cumulee a N contre celle a 2N serait TROMPEUR : les deux partagent
les N premiers tirages, sont autocorrelees, et l'ecart sous-estime l'erreur. On a donc
lance **deux chaines independantes** (graines disjointes) et compare leurs moyennes au
meme N. L'erreur d'une chaine s'en deduit : se = sd(chaine1 - chaine2)/sqrt(2).

### Mesures
| N / chaine | metrique | se | distance moyenne | erreur relative |
|---|---|---|---|---|
| 25 | Bray | 0.00076 | 0.9233 | 0.082 % |
| 50 | Bray | 0.00054 | 0.9233 | 0.058 % |
| 100 | Bray | 0.00038 | 0.9233 | 0.041 % |
| 200 | Bray | 0.00027 | 0.9233 | 0.029 % |
| 25 | Jaccard | 0.00087 | 0.9572 | 0.091 % |
| 200 | Jaccard | 0.00030 | 0.9572 | 0.031 % |

### Controle de validite
La decroissance suit la loi theorique de Monte-Carlo : pente log-log mesuree
**-0.494 (Bray)** et **-0.509 (Jaccard)**, contre -0.5 attendu. Le comportement est
donc bien celui d'une moyenne d'echantillons independants — si la pente avait devie,
cela aurait signale un defaut (tirages correles, accumulateur errone).

### Conclusion
L'erreur de Monte-Carlo est **deja sous 0.1 % a N = 25** et sous 0.05 % a N = 100.
Elle est de **trois ordres de grandeur inferieure** aux echelles qui comptent :
- erreur MC a N=100 : 0.0004
- variabilite technique de sequencage : 0.118
- variabilite technique de preparation de librairie : 0.248
- distance biologique entre poissons : 0.880

N = 100 est donc largement suffisant pour le beta ; pousser a 1000 diviserait l'erreur
par 3 sur une quantite deja negligeable, pour 10x le temps de calcul.

## Livrables
- `results/rarefaction/alpha_mean_1000.tsv` — alpha moyenne + sd, 1784 echantillons
- `results/rarefaction/beta_mean_bray_N400.rds` — matrice Bray moyennee, 400 tirages
- `results/rarefaction/beta_mean_jaccard_N400.rds` — matrice Jaccard moyennee, 400 tirages
- `results/rarefaction/beta_convergence.tsv` — le tableau de convergence
- `results/rarefaction/fig_rarefaction_convergence.png` — figure (supplementaire)
- `scripts/15-rarefaction_converge.sh` — script versionne

Les matrices livrees portent 400 tirages (200 par chaine, fusionnees) : au-dela du
necessaire, conservees telles quelles puisque deja calculees.

## Cout mesure — pour dimensionner les prochains jobs
Sur 1784 x 44200 : `rrarefy` 4.7 s, indices alpha 8.8 s, mais `vegdist` bray **414 s**
et jaccard **313 s** par tirage (mesures en serie). Le beta coute ~55x l'alpha.
Sur 32 coeurs l'acceleration est loin d'etre lineaire — `vegdist` sature la bande
passante memoire plutot que le CPU : le job complet a pris ~6 h de walltime.
**Ne pas surdimensionner en coeurs pour ce type de calcul.**

## Formulation Methods (pret a inserer)
"Sequencing effort was normalized by repeated rarefaction to 3,000 reads. Alpha
diversity indices were averaged over 1,000 independent rarefactions; Bray-Curtis and
Jaccard dissimilarity matrices were averaged over 400. Metrics were averaged rather
than count tables, since averaging tables would inflate observed richness by taking
the union of detections across draws. Monte-Carlo error was quantified by comparing
two independent chains at matched iteration counts and was below 0.05% of the mean
distance at 100 iterations, three orders of magnitude below both the technical and the
biological dissimilarity scales. Note that an averaged dissimilarity matrix is not
guaranteed to satisfy the triangle inequality; this does not affect PERMANOVA or
principal coordinates analysis, which accept semi-metrics."

## Reserve technique
Une matrice de distances moyennee n'est plus garantie metrique (inegalite
triangulaire). Sans consequence pour PERMANOVA ni PCoA, qui tolerent les
semi-metriques, mais a ne pas utiliser dans une methode qui exige une vraie metrique.
