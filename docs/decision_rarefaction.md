# docs/decision_rarefaction.md — Seuil de raréfaction

## Décision (2026-07-27)
**Seuil de raréfaction retenu : 3 000 lectures.**

⚠️ SEULE LA VALEUR DE SEUIL EST FIGÉE. Aucune table raréfiée n'a été générée à ce
stade. Le MODE d'application reste à décider :
  - tirage unique (subsample une fois), ou
  - **raréfaction répétée** (Cameron et al. 2021 : répéter N fois et moyenner /
    agréger) — piste privilégiée mais non arrêtée.
Ne pas produire `asv_table_rarefied*` tant que ce choix n'est pas tranché.
Table d'entrée quand on le fera : results/decontam/asv_table_analysis.tsv
(décontaminée seuil 0.1 ; 44 256 ASV × 2186 échantillons).

## Justification du seuil (fondée sur les données + littérature)
Cadre : Schloss (2024, mSphere, doi:10.1128/msphere.00354-23) — la raréfaction est
actuellement la méthode la plus robuste pour contrôler l'effort de séquençage inégal
en diversité α/β ; le critère de choix décisif est de ne pas laisser la profondeur (ou
la perte d'échantillons) se confondre avec un facteur biologique/technique.

Aucune référence ne prescrit un seuil chiffré universel : le nombre se choisit sur les
données. Trois critères, tous vérifiés ici :

1. **Saturation de la richesse** : les courbes de raréfaction plafonnent avant 3 000
   lectures → 3 000 capture toute la richesse (fig_qc_depth.png).
2. **Conservation des échantillons** : 3 000 retient 1 793/2 186 (82,0 %) ;
   5 000 tombe à 73,2 %.
3. **Pas de biais de rétention sur le facteur batch (run)** : la perte d'échantillons
   est équilibrée entre les 3 runs (chi² p = 0,23 à 3 000 ; écart 3,4 points).

## Pourquoi 3 000 et pas 5 000
5 000 aggrave la perte déséquilibrée d'échantillons SANS gain de couverture
(richesse déjà saturée) :
| Facteur | écart rétention @3000 | @5000 |
|---|---|---|
| run     | 3,4 pts (p=0,23)      | 5,1 pts |
| tissu   | 12,0 pts              | 15,7 pts |
| taxon   | 14,0 pts              | 18,6 pts |
| site    | 37,0 pts              | 42,2 pts |

## Point de vigilance (à documenter, pas un défaut de la méthode)
La perte d'échantillons est déséquilibrée entre SITES (indépendamment du seuil) :
c'est une propriété du jeu (séquençage moins profond sur certains sites), pas un
artefact de la raréfaction. Site le plus touché = **canal (Caa, allopatrie)** :
58 % retenus à 3 000 (47 % à 5 000). Les sites à faible profondeur (canal, Manosque)
auront donc moins de puissance ; en tenir compte dans l'interprétation des contrastes.
Si protection accrue du canal souhaitée, 2 000 reste défendable (canal 66 % retenu,
richesse toujours saturée) — non retenu par défaut.

## Formulation pour l'article (Methods)
« Samples were rarefied to 3,000 sequences, a depth beyond which richness had
plateaued in rarefaction curves. This threshold retained 82% of samples
(1,793/2,186) and did not bias sample retention across sequencing runs
(chi-square p = 0.23), the main technical batch factor. A higher threshold (5,000)
was rejected as it increased uneven sample loss across sites and taxa without
improving coverage. Rarefaction was used to control for uneven sequencing effort
following Schloss (2024). »
[Compléter la phrase avec le mode retenu — tirage unique vs raréfaction répétée
(Cameron et al. 2021) — une fois décidé.]

## Reproductibilité
Test de confusion : calculé en local sur results/qc_depth/depth_per_sample.tsv
(Kruskal-Wallis sur profondeur ; chi² sur rétention par facteur). Références :
rarefaction_sota.bib (13 réf., DOI vérifiés).
