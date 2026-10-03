# PERMDISP : correction de petit effectif — plan de reprise (2026-10-03)

## Défaut
`scripts/24-permdisp.sh` appelait `betadisper(D, g, type = "median")` sans `bias.adjust = TRUE`.
Sans correction, la distance au centre d'un groupe de taille n est sous-estimée d'un facteur
≈ √((n−1)/n). Les hybrides sont la plus petite catégorie dans **toutes** les strates (p. ex.
caudale passe 1 : 10 Hy contre 44 Cn et 70 Pt ; en intra-station, parfois 3–4 individus par
catégorie). Le test est donc biaisé vers « hybrides moins dispersés » — le sens rapporté par R15
et R25 et écrit dans l'article (§8.9). Défaut de l'analyse antérieure de l'agent, non signalé
jusqu'ici.

## Ce qui a déjà été vu (déclaré)
`bias.adjust` multiplie toutes les distances d'un groupe par √(n/(n−1)) ; les médianes publiées par
le script se corrigent donc exactement à partir de `results/recat/{1,2}/permdisp/permdisp.tsv`.
Ce calcul a été fait **avant** ce plan, sur les sorties existantes :

| passe | dispositif | tests | Hy les moins dispersés, non corrigé → corrigé | Hy les plus dispersés, corrigé |
|---|---|---|---|---|
| 1 | station bloquée | 48 | 32 → 22 (binomiale unilatérale contre 1/3 : p = 0,048) | 18 |
| 1 | intra-station | 68 | 45 → 25 (p = 0,31) | 17 |
| 2 | station bloquée | 48 | 34 → 32 (p = 2,4 × 10⁻⁶) | 10 |
| 2 | intra-station | 120 | 41 → 39 (p = 0,61) | 45 |

Ce que la reprise ajoute et qui n'a **pas** été vu : les valeurs p des tests (permutest sur les
distances corrigées) et le nombre de tests significatifs dans chaque sens.

## Reprise
`PERMDISP_BIAS=1` (nouvelle option, défaut 0 = comportement d'origine) ; mêmes graine, matrices,
dispositifs et permutations ; passes 1 et 2 → `results/recat/{1,2}/permdisp_bias/`. Les sorties
non corrigées sont conservées.

## Règles de lecture
1. « Hybrides moins dispersés » est maintenu pour une passe × dispositif si, après correction, le
   nombre de tests où Hy est le moins dispersé dépasse le hasard (binomiale unilatérale contre 1/3,
   p < 0,05) ; sinon il est retiré pour cette passe × dispositif.
2. La prédiction transgressive en dispersion (Hy plus dispersés que les deux parents) est dite
   soutenue si le nombre de tests où Hy est le plus dispersé dépasse le hasard de la même façon.
3. Les tests significatifs (p < 0,05) sont rapportés dans chaque sens, par passe et dispositif.
4. Le paragraphe dispersion de l'article et la figure 4 sont réécrits à partir des sorties
   corrigées ; R15 et R25 sont corrigés dans le registre avec le chiffrage ancien → nouveau.
