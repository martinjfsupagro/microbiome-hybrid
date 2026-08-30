# docs/decision_position_effect.md — Effet de la position dans la plaque sur la composition

## Question
Andre (2026-08-30) : la numerotation des individus au terrain suit le taxon (les hotu
d'abord, plus fragiles). Le taxon predit donc la position sur la plaque
(chi2 = 330, V de Cramer = 0.477 ; le toxostome n'occupe que les colonnes 1, 2 et 10).
Un effet de position pourrait-il se faire passer pour un effet taxon ?

Le test sur la PROFONDEUR etait insuffisant : la rarefaction egalise la profondeur.
Il fallait tester la COMPOSITION. Scripts 17 et 18.

## Reponse : OUI, l'effet de position est reel et du meme ordre que l'effet taxon

Chiffres medians, metrique Jaccard (quasi-metrique, voir reserve ci-dessous), R²
rapporte a l'attendu sous H0 (df/(n-1)) — indispensable car les df diffferent :

| Effet | df | R² | attendu H0 | ratio | strates significatives |
|---|---|---|---|---|---|
| Site (en premier) | 8 | 0.163 | 0.053 | **3.07** | 12/12 |
| **Colonne de plaque** (site fixe) | 11 | 0.128 | 0.075 | **1.77** | **12/12** |
| **Colonne, sites mono-taxon** | 9 | 0.267 | 0.133 | **1.89** | **11/12** |
| Taxon (apres colonne) | 2 | 0.027 | 0.014 | **1.93** | 8/12 |
| Rangee de plaque | 7 | — | — | **0.89** | 3/12 |
| Bord de plaque | 1 | — | — | **1.11** | **0/12** |

## Les temoins, et ce que chacun exclut

### 1. Ce n'est pas un effet TISSU
La plaque est ENTIEREMENT determinee par le tissu (1-2 caudale, 3-4 branchie,
5-6 hindgut, 7-8 midgut). L'analyse est stratifiee PAR TISSU : le tissu ne peut pas
contribuer.

### 2. Ce n'est pas un effet SITE
Les permutations sont contraintes DANS les blocs de site (`how(blocks = site)`) : le
site est fixe par construction du test. L'effet colonne reste significatif dans les
**24 strates** (12 strates x 2 metriques), p <= 0.007.

Precondition verifiee avant de conclure : site et colonne sont fortement associes
(V = 0.593) mais **pas confondus** — chaque colonne contient au moins 2 sites, dans
chaque tissu. Le test etait donc interpretable.

### 3. Ce n'est pas un effet TAXON — le temoin decisif
Le blocage par site ne fixe PAS le taxon, et dans les 4 sites ou le taxon varie, la
colonne et le taxon sont fortement confondus :
`Ain V=0.502 | Avi V=0.588 | Bue V=0.826 | Man V=0.951`.

**Temoin** : quatre sites n'ont qu'UN SEUL taxon sequence et une seule station
(Bau, Caa, Jus, Per). Le taxon y est constant par construction — un effet colonne y
est necessairement positionnel. Resultat : ratio **1.89** (vs 1.77 toutes strates),
significatif dans **11/12** strates. **L'effet ne faiblit pas quand le taxon ne peut
plus varier.**

`Cab` est ECARTE de ce temoin : il couvre deux stations du Suran, donc la colonne y
encoderait la station (cf decision_stations.md §2).

**Contre-temoin** (sites multi-taxons) : ratio 1.40, significatif 12/12 — pas plus
fort. Le taxon n'ajoute rien a l'effet colonne.

**Test symetrique** (taxon EN PREMIER, ordre defavorable a la colonne) : la colonne
conserve R² = 0.167 (12/12 significatif en Jaccard), contre R² = 0.049 pour le taxon
servi d'abord. La colonne porte de l'information que le taxon n'explique pas.

### 4. Ce n'est pas un artefact de bord — controle negatif qui aurait pu echouer
Les artefacts de plaque classiques (evaporation, effets de bord) sont **absents** :
- **bord** : ratio 1.11, significatif dans **0/12** strates ;
- **rangee** : ratio 0.89, significatif dans 3/12 seulement.

L'effet est **specifique a la colonne**. C'est un controle negatif informatif : un
artefact de manipulation generique aurait touche le bord et la rangee.

### 5. L'effet se replique dans les trois runs
La position est identique dans les 3 runs (memes librairies), donc les empiler serait
de la pseudo-replication. Chaque run est analyse separement : l'effet colonne est
significatif dans **les 3 runs, pour les 4 tissus, pour les 2 metriques**. Un artefact
de bruit ne se repliquerait pas ainsi.

### 6. L'effet est monotone dans le rang de colonne au sein du site
Le rang de colonne DANS le site (1 seul df) est significatif dans 8-12/12 strates
selon le sous-ensemble, ratio 1.74 a 3.36. L'effet a donc une composante graduelle,
compatible avec un gradient d'ORDRE DE TRAITEMENT — ce que la reponse d'Andre predit
(les poissons sont traites dans l'ordre, les puits remplis dans l'ordre).

## Statut du mecanisme : HYPOTHESE, pas resultat
Les temoins ci-dessus etablissent que l'effet **existe** et qu'il n'est ni le tissu,
ni le site, ni le taxon, ni un effet de bord. Ils **n'identifient pas sa cause**.
Hypotheses compatibles, non departagees :
- delai entre capture et dissection (evolution post-mortem de la communaute
  intestinale), correle a l'ordre de traitement ;
- derive de manipulation le long du remplissage de la plaque ;
- structure spatiale fine non mesuree, correlee a l'ordre de peche.
Aucun temoin ne les separe. Tant que c'est le cas, **la cause reste une hypothese**.

## Consequence pour l'analyse — contraignante
1. **La colonne de plaque doit entrer comme covariable** dans tout modele testant le
   taxon ou l'index hybride. Son effet par degre de liberte (1.77-1.89) est du meme
   ordre que celui du taxon (1.93) : l'ignorer expose a attribuer a la biologie un
   signal positionnel.
2. **La nageoire caudale demande une prudence particuliere.** Le signal taxon n'y
   survit PAS a l'ajustement sur la colonne : 0/3 runs significatifs, en Bray comme en
   Jaccard (p de 0.14 a 0.83). Dans ce tissu, le signal taxon apparent pourrait etre
   entierement positionnel. C'est aussi le tissu de plus faible biomasse.
3. **Branchie et midgut resistent** : le taxon y reste significatif apres ajustement
   (3/3 runs en Bray et en Jaccard pour le midgut ; 3/3 et 2/3 pour la branchie).
   Hindgut est discordant entre metriques (0/3 Bray, 3/3 Jaccard).
4. La partition de variance du script 14 (technique = 0.03 %) **ne contenait aucun
   terme de position**. Cette composante n'y avait jamais ete estimee ; elle n'est pas
   negligeable. La partition devra etre refaite avec un terme de position.

## Reserve methodologique : non-metricite des matrices moyennees
Les matrices sont des MOYENNES sur 400 rarefactions. Une moyenne de matrices de
Bray-Curtis n'est pas garantie de respecter l'inegalite triangulaire. Diagnostic
(cmdscale standard) :

| Metrique | vp negatives | part de la somme des \|vp\| | \|vp min\| / vp max |
|---|---|---|---|
| Bray-Curtis | 808 / 1784 | 7.04 % | 0.028 |
| Jaccard | 34 / 1784 | **0.02 %** | 0.0006 |

Jaccard est essentiellement metrique. Les conclusions sont identiques pour les deux
metriques, ce qui **borne la portee de cette reserve** : elles ne dependent pas de la
non-metricite. Les chiffres cites ci-dessus sont ceux de Jaccard.

**Defaut corrige dans mon propre travail.** Le script 17 calculait cette part avec un
double-centrage ecrit a la main, qui ajoutait la moyenne generale alors que le
centrage sequentiel l'inclut deja. Il annoncait "exactement 50.000 %" pour LES DEUX
metriques — la valeur identique etait le signe de l'erreur. Recalcule avec cmdscale.

**Second defaut du script 17.** La table `position_tests.tsv` n'a **pas de colonne
metrique** : bray et jaccard y sont ecrites a la suite sans etiquette. Elles ne sont
separables que par l'ordre des lignes (bray d'abord, ecriture incrementale dans
l'ordre de la boucle). Le script 18 corrige cela (colonne `metric`). Quiconque relit
`position_tests.tsv` doit en tenir compte.

## A faire
- Refaire la partition de variance (script 14) avec un terme de position.
- Reprendre le test taxon quand l'index hybride sera disponible : le taxon actuel
  (Cn/Pt/Ch avec Ch non resolu) est un predicteur faible et partiellement confondu
  avec le site.
- Decider du traitement de la nageoire caudale dans le manuscrit.

## Fichiers
- `results/position_effect/position_tests.tsv` (script 17, sans colonne metrique)
- `results/position_effect/position_control.tsv` (script 18, avec colonne metrique)
- `results/position_effect/position_summary.txt`, `position_control.txt`
- `results/position_effect/fig_position_effect.png`
- `results/position_effect/negative_eigenvalues.txt`
