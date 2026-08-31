# docs/decision_depth_threshold.md — Seuil de rarefaction : mesure du compromis

## Le probleme

Le seuil de rarefaction fait DEUX choses a la fois :
1. il egalise la profondeur entre echantillons (but de la rarefaction) ;
2. il decide quels echantillons entrent dans l'analyse (filtre de selection).

Le filtre est **oriente sur la variable d'interet**. A 3000 lectures, dans la caudale,
57 % des hybrides passent contre 87 % des Pt (+30 points), et l'ecart atteint
**+53 points a Buech-Meouge**, l'une des trois stations a gradient complet. Le midgut
porte +23 points. La branchie est propre (-1 point).

L'ecart n'est PAS du a la station Canal (usine du Largue) : sans elle il reste a
+29,9 points. Canal est une perte totale de station (0/20 echantillons caudaux, profondeur
mediane 240 lectures), pas une perte orientee — sur place l'ecart Hy/Pt est nul.

## La mesure (script 22)

Sur un jeu d'echantillons **FIXE** — les 1 784 retenus a 3000 — on rarefie a 500, 750,
1000, 1500 et 2000 et on compare aux matrices de reference a 3000. Le jeu etant identique,
l'ecart mesure l'effet de la PROFONDEUR seule, sans melange avec la selection.

**Temoin d'appariement, qui pouvait echouer.** UniFrac recalcule ici a 3000 (N=20) contre
les references N=400 lues et reordonnees : r = 0.999336 (non pondere) et 0.999962
(pondere). Un mauvais ordre des identifiants aurait fait s'effondrer ces correlations.

### Resultat : la geometrie beta resiste, la richesse non

| Seuil | Jaccard | UniFrac non pond. | UniFrac pondere | richesse | biais caudale | biais midgut | n retenus |
|---|---|---|---|---|---|---|---|
| 500 | 0.9617 | **0.9373** | **0.9994** | **-42 %** | **+2,5** | +15,0 | 679 |
| 750 | 0.9789 | 0.9612 | 0.9997 | -31 % | +8,1 | +18,2 | 661 |
| 1000 | 0.9876 | 0.9755 | 0.9998 | -23 % | +21,4 | +19,2 | 646 |
| 1500 | 0.9952 | 0.9900 | 0.9999 | -13 % | +23,7 | +17,0 | 630 |
| 2000 | 0.9981 | 0.9961 | 0.9999 | -7 % | +28,2 | +20,2 | 612 |
| 3000 | (ref) | (ref) | (ref) | (ref) | +30,4 | +23,3 | 583 |

**Le temoin de contraste fonctionne.** UniFrac PONDERE reste a r = 0.9994 meme a 500,
alors que le NON PONDERE tombe a 0.9373 : la degradation vient bien de la perte des
taxons rares, et non d'un artefact general de faible profondeur. L'inquietude
« a 500 on ne voit plus que le core microbiota » est donc **exacte pour les metriques de
presence et pour la richesse (-42 %), et fausse pour les metriques ponderees**, dont la
geometrie est essentiellement inchangee.

**Aucune profondeur ne fait les deux.** Le biais caudal ne tombe qu'a 500 (+2,5), la ou
42 % de la richesse est perdue. A 1000 il reste a +21,4 : un controle a 1000 ne
controlerait pas. Les deux courbes ne se croisent pas.

## Decision qui en decoule

**Analyse principale : 3000, quatre metriques.** Inchangee.

**Sensibilite a 500, restreinte aux metriques PONDEREES.** Le signal de categorie de la
caudale — le tissu au biais de selection maximal — est porte par UniFrac pondere
(3/3 runs dans les deux dispositifs, cf. decision_phylo_and_category.md), qui est
precisement la metrique invariante a la profondeur. Cette affirmation-la peut donc etre
testee a 500, ou le biais caudal disparait (+2,5 points).

**Les affirmations fondees sur les metriques de PRESENCE restent a 3000, biais declare.**
Elles ne peuvent pas etre testees a 500 (r = 0.94 pour UniFrac non pondere) — et de toute
facon le biais du midgut reste a +15 points a 500, donc baisser le seuil ne le corrigerait
pas. C'est une limite a declarer, pas a corriger.

**Les metriques ALPHA restent a 3000.** La richesse perd 42 % a 500 : des valeurs alpha
issues de deux seuils ne sont pas comparables.

**Canal caudale est perdue a tout seuil defendable** (mediane 240 lectures) : a declarer
dans les limites.

## Non teste

**Bray-Curtis n'a pas ete mesure** a faible profondeur : vegdist n'est pas dans l'image
QIIME2 et le calcul en Python sur 1.59 M paires n'est pas praticable sans compilation.
C'est une metrique ponderee, donc son comportement est vraisemblablement proche de celui
d'UniFrac pondere — **mais ce n'est pas verifie**. Si Bray-Curtis doit entrer dans
l'analyse de sensibilite a 500, il faut le mesurer d'abord (job R avec vegan, ~15 min).

## Fichiers
- `scripts/22-depth_agreement.sh` (profondeurs pilotees par AGREE_DEPTHS)
- `results/depth_agreement/depth_agreement{,_low}.{tsv,txt}`
- `results/depth_agreement/fig_depth_tradeoff.png`
- `results/depth_agreement/retention_par_station_tissu.csv`


---

# COMPLEMENT 2026-08-31 — Bray-Curtis mesure, et sensibilite a 500 executee

## 1. Bray-Curtis : le point non verifie est leve (script 23)

Meme protocole que le script 22, jeu fixe de 1 784 echantillons, reference =
`beta_mean_bray_N400.rds` (le script 15 l'a produite avec exactement le meme appel
`rrarefy` + `vegdist(R,"bray")`). Temoin de recalcul a 3000 (3 tirages) contre cette
reference : **r = 0.999830**, ecart absolu moyen 0.00144 — lecture de table et
appariement des identifiants confirmes.

| Profondeur | r avec la matrice a 3000 | ecart relatif |
|---|---|---|
| 500 | **0.9985** | 0.5 % |
| 1000 | 0.9996 | 0.2 % |
| 2000 | 0.9999 | 0.1 % |

**Bray-Curtis est invariant a la profondeur**, comme UniFrac pondere. La classification
est donc complete et entierement mesuree :

| Famille | Metrique | r a 500 |
|---|---|---|
| **Ponderee — invariante** | UniFrac pondere | 0.9994 |
| | Bray-Curtis | 0.9985 |
| **Presence — degrade** | Jaccard | 0.9617 |
| | UniFrac non pondere | 0.9373 |
| alpha | richesse observee | 0.9623 (-42 % de valeur) |

**Defaut de ma premiere version du script 23, corrige.** Elle etait serielle : 7 min par
tirage, N=20 par profondeur plus une reference recalculee, soit ~10 h pour un walltime de
6 h — et elle n'ecrivait qu'a la fin, donc un depassement n'aurait rien rendu. Corrige :
tirages repartis par `mclapply` (avec controle explicite des objets d'erreur, que
`mclapply` rend sans lever), reference prise sur la matrice existante, N=10, ecriture
incrementale apres chaque profondeur.

## 2. Sensibilite a 500 : le signal caudal survit

Executee avec **le meme code** que l'analyse principale (scripts 21 et 20 parametres par
`PHYLO_DEPTH` / `CATPART_GLOB`), sur UniFrac pondere, N=400, deux chaines. Jeu elargi :
**2 067 echantillons** contre 1 784 a 3000 (+16 %). Convergence a 500 : erreur MC
relative 0.00135, r entre chaines 0.999946.

| Tissu | n (3000) | n (500) | sequentiel 3000 | sequentiel 500 | bloque 3000 | bloque 500 |
|---|---|---|---|---|---|---|
| **caudale** | 141 | 168 | **3/3** | **3/3** | **3/3** | **3/3** |
| branchie | 161 | 179 | 3/3 | 3/3 | 0/3 | 0/3 |
| midgut | 147 | 172 | 0/3 | 3/3 | 3/3 | 3/3 |
| hindgut | 154 | 173 | 0/3 | 0/3 | 0/3 | 1/3 |

Encadrement du R² de la categorie : 0.0165–0.0319 a 3000, **0.0161–0.0283 a 500**.

**Le controle pouvait echouer et n'a pas echoue.** Le biais de selection dans la caudale
passe de +30.4 a +2.5 points entre les deux seuils ; si le signal de categorie y avait
ete produit par la selection, il aurait du disparaitre a 500. Il est identique : 3/3 dans
les deux dispositifs, aux deux seuils. **Le signal caudal n'est pas un artefact du filtre
de profondeur.**

Le midgut passe de 0/3 a 3/3 en sequentiel — mais son biais reste a +15 points a 500,
donc ce n'est pas une lecture affranchie de la selection.

Le hindgut ne montre rien aux deux seuils, ce qui est coherent avec les quatre metriques
a 3000.

## 3. Ce qui reste ouvert

**Bray-Curtis a 500 n'a PAS ete calcule.** Il est maintenant valide comme utilisable a
cette profondeur, mais la matrice a 500 (2 067 echantillons, N=400) demanderait ~4 h
(vegdist ~9 min par tirage, reparti sur 16 coeurs). Elle apporterait une seconde metrique
ponderee au controle — utile puisque Bray-Curtis donnait 2/3 pour la caudale a 3000,
contre 3/3 pour UniFrac pondere.

## Fichiers ajoutes
- `scripts/23-bray_depth_agreement.sh`
- `results/depth_agreement/bray_depth_agreement.{tsv,txt}`
- `results/phylo_diversity_d500/`, `results/rarefaction_d500/`,
  `results/var_partition_cat_d500/`
