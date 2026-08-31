# docs/decision_permdisp.md — Dispersion par categorie genotypique (script 24)

## Pourquoi ce test n'est pas un simple controle

L'hypothese "transgressive" porte en partie sur la VARIABILITE du microbiote hybride, pas
seulement sur la position de son centroide. La PERMANOVA ne teste que la position ; c'est
betadisper qui teste la dispersion. Sans lui, une moitie de la question restait non posee.

## Deux dispositifs

- **global, station bloquee** : tous les echantillons d'une strate (tissu x run x metrique),
  permutations contraintes dans les blocs de station. 48 tests.
- **intra-station** : les trois stations a gradient complet, analysees separement. Une
  difference de dispersion n'y peut pas etre spatiale. 108 tests.

Mediane spatiale (type = "median"), 999 permutations, 4 metriques x 4 tissus x 3 runs.

## Resultat 1 — la prediction transgressive n'est PAS soutenue, et le sens est inverse

| | Hy le moins disperse | intermediaire | Hy le plus disperse |
|---|---|---|---|
| global (n=48) | **31 (65 %)** | 8 | 9 |
| intra-station (n=108) | **52 (48 %)** | 26 | 30 |

Attendu au hasard sans ordre : 33 %. Binomial unilateral p = 9.4e-6 (global) et 1.0e-3
(intra-station). **Un seul** test est a la fois significatif et dans le sens transgressif,
**aucun** en intra-station.

Ecart median Hy - moyenne parentale : -0.036 (Bray), -0.022 (UniFrac non pondere),
-0.010 (Jaccard), +0.002 (UniFrac pondere). L'effet est reel dans son sens mais petit.

La ou la dispersion differe significativement, c'est **P. toxostoma** le plus variable
(caudale et hindgut), ou C. nasus (midgut).

## Resultat 2 — le controle qui pouvait invalider la caudale, et qui ne l'a pas fait

La PERMANOVA est sensible a l'heterogeneite de dispersion. Dans la caudale :

| Metrique | Effet de position (PERMANOVA) | Heterogeneite de dispersion (PERMDISP) |
|---|---|---|
| Bray-Curtis | 2/3 | **3/3** |
| Jaccard | 0/3 | **3/3** |
| UniFrac non pondere | 2/3 | **3/3** |
| **UniFrac pondere** | **3/3** | **0/3** |

Les signaux de position en Bray, Jaccard et UniFrac non pondere ne sont pas separables
d'un effet de dispersion. Mais **la seule metrique ou le signal caudal est robuste est
aussi la seule sans heterogeneite de dispersion** — et cela tient aussi en intra-station
(0/3 a Buech-Meouge). Le resultat caudal en UniFrac pondere est donc une difference de
COMPOSITION, pas de variabilite. Le controle pouvait echouer.

## Reserve non levee

betadisper n'accepte pas de covariable : l'effet de position dans la plaque (scripts 17/18)
n'est PAS ajuste ici. Une categorie dont les echantillons sont plus etales en colonne
pourrait porter une dispersion gonflee. Ce point n'est pas separe par ces donnees.

## Non-metricite

Part de valeurs propres negatives des matrices moyennees : mediane 0.00 %, maximum 10.4 %.

## Fichiers
- `scripts/24-permdisp.sh`
- `results/permdisp/permdisp.tsv` (156 tests) et `.txt`
- `results/permdisp/fig_permdisp.png`
- redige dans l'Article section 8.9, Table S9 et Figure S3
