# D7 — de quelles conclusions le choix de métrique décide-t-il ?

Instruction du 2026-09-30, préalable à l'arbitrage. Volet composition : synthèse des tables
déjà calculées dans `results/recat/{1,2}`, aucun recalcul. Volet alpha : recalculé sur les quatre
indices, les diagnostics antérieurs ne portant que sur la richesse ASV observée.
Script `scripts/29-d7_metriques.py`, sorties dans `results/d7_metriques/`.

Seuil `p < 0,05` strict, convention du dépôt. Contrôle de cohérence : les 14 cellules que
`docs/recalcul/d2_avec_vs_sans_position.csv` documente sont reproduites **14 sur 14**. Le
désaccord était possible — ma première passe en `p ≤ 0,05` en donnait 13 sur 14, l'écart tenant à
une cellule dont le `p` vaut exactement 0,050 sur `durance2`.

---

## 1. Ce qui ne dépend pas de la métrique

**Le gradient externe / interne.** Significatif sur les quatre indices, tous à p < 10⁻¹⁶, sur
174 individus appariés. C'est le résultat le plus solide du jeu et aucun choix de métrique ne le
menace.

**Mais son amplitude, elle, dépend fortement de l'indice** — et c'est la valeur que le texte cite :

| indice | rapport externe / interne | IC 95 % |
|---|---|---|
| richesse observée | 1,93 | 1,71 – 2,18 |
| Shannon | **1,51** | 1,40 – 1,64 |
| inverse Simpson | 2,99 | 2,48 – 3,63 |
| Faith PD | 1,62 | 1,50 – 1,76 |

Le « 1,8 fois » des notes de diagnostic est une valeur de richesse observée. Sur Shannon le rapport
tombe à 1,51, sur l'inverse Simpson il double à 3,00. Le chiffre doit être donné avec son indice,
jamais seul.

**L'effet de la catégorie génotypique est petit sur les quatre métriques.** R² médian encadré par
les deux ordres séquentiels, passe 2 : 0,013–0,036 (Bray-Curtis), 0,013–0,022 (Jaccard),
0,014–0,026 (UniFrac non pondéré), 0,014–0,036 (UniFrac pondéré). Les métriques ne désaccordent
pas sur l'ampleur, seulement sur la significativité.

## 2. Ce que la métrique décide

### Le contraste midgut / hindgut — et donc la comparaison avec 2017

| indice | rapport midgut / hindgut | p |
|---|---|---|
| richesse observée | 0,829 | **0,009** |
| Faith PD | 0,874 | **0,003** |
| Shannon | 0,942 | 0,18 |
| inverse Simpson | 0,871 | 0,25 |

Les deux indices qui soutiennent le contraste sont **les deux indices non pondérés** — précisément
ceux que l'analyse de reproductibilité technique disqualifie, puisque 48 % seulement des ASV à
1–3 lectures sont retrouvés au reséquençage. Sur les deux indices pondérés par l'abondance, le
contraste n'est pas significatif.

**Conséquence directe : l'affirmation « midgut et hindgut sont proches mais non
interchangeables », posée contre le résultat négatif de Guivier et al. (2017), n'est pas
soutenue par les métriques reproductibles.** Le résultat de 2017 tient sur celles-là. Cette
affirmation doit être retirée ou requalifiée en « détectable sur les indices non pondérés
seulement ».

### Le dimorphisme sexuel — et l'inversion supposée par rapport à 2017

| indice | externe (F/M, p) | interne (F/M, p) |
|---|---|---|
| richesse observée | 1,23 (0,15) | **1,43 (0,007)** |
| Faith PD | 1,13 (0,12) | **1,29 (0,007)** |
| Shannon | **1,12 (0,032)** | 1,17 (0,092) |
| inverse Simpson | 1,44 (0,083) | 1,48 (0,26) |

Le compartiment où le dimorphisme est significatif **change avec l'indice** : interne sur les deux
indices non pondérés, externe sur Shannon, nulle part sur l'inverse Simpson. Or 2017 rapportait un
dimorphisme plus marqué sur les tissus externes.

**`note_guivier2017_implications.md` conclut que le motif s'inverse par rapport à 2017. Ce n'est
pas établi : sur Shannon, il ne s'inverse pas.** L'inversion était un effet du choix de la
richesse observée. À cela s'ajoute le biais déjà documenté — le sexe n'est déterminé que pour 108
individus sur 180 et les indéterminés sont nettement plus petits, donc probablement juvéniles.
Verdict inchangé sur le fond, mais pour une raison de plus : le sexe reste une covariable de
contrôle, pas un résultat.

### La composition : quel compartiment porte l'effet de catégorie

Nombre de runs significatifs sur 3, test conservateur (catégorie après position, permutations
bloquées dans la station) :

| passe | métrique | caudale | branchie | midgut | hindgut |
|---|---|---|---|---|---|
| 1 | Bray-Curtis | 0 | 1 | 0 | 0 |
| 1 | Jaccard | 0 | 3 | 3 | 3 |
| 1 | UniFrac non pondéré | 1 | 0 | 3 | 2 |
| 1 | UniFrac pondéré | **3** | 0 | 0 | 0 |
| 2 | Bray-Curtis | 0 | 3 | 3 | 3 |
| 2 | Jaccard | 0 | 3 | 3 | 3 |
| 2 | UniFrac non pondéré | 1 | 0 | 3 | 2 |
| 2 | UniFrac pondéré | 0 | 0 | 3 | 3 |

Deux lectures s'imposent.

**Le résultat caudal est une cellule unique.** Il n'existe que sur l'UniFrac pondéré et seulement
en passe 1. Les trois autres métriques donnent 0 ou 1 run sur 3 dans les deux passes, et l'UniFrac
pondéré lui-même tombe à 0 en passe 2. C'est le résultat que le §8.9 met aujourd'hui en avant.

**Les compartiments digestifs sont le résultat robuste.** En passe 2, le midgut est détecté par les
quatre métriques et le hindgut par trois sur quatre. C'est le seul endroit du plan où les métriques
concordent — et c'est exactement la prédiction dirigée héritée de Guivier et al. (2017), qui
observaient la divergence parentale la plus forte dans l'intestin.

### La dispersion (PERMDISP)

| métrique | Hy le moins dispersé | Hy le plus dispersé | écart médian | tests significatifs |
|---|---|---|---|---|
| Bray-Curtis | 18 / 24 | 6 / 24 | −0,033 | 10 |
| Jaccard | 19 / 24 | 0 / 24 | −0,012 | 11 |
| UniFrac non pondéré | 18 / 24 | 1 / 24 | −0,019 | 14 |
| UniFrac pondéré | 11 / 24 | 8 / 24 | **+0,000** | 4 |

Le motif « hybrides les moins dispersés » est porté par trois métriques et absent de la quatrième.
Le manuscrit le déclare déjà ainsi ; la classification de septembre et les deux passes ne le
changent pas.

## 3. Un point qui invalide une règle simple

**L'axe pertinent n'est pas le même en alpha et en composition.** En alpha, le clivage est bien
pondéré contre non pondéré : richesse et Faith PD d'un côté, Shannon et inverse Simpson de l'autre.
En composition, non : **Bray-Curtis est pondéré par l'abondance et se comporte comme Jaccard**, en
passe 2 cellule pour cellule, tandis que l'UniFrac pondéré est la métrique isolée — sur la
catégorie comme sur la dispersion. Le clivage y est {Bray, Jaccard, UniFrac non pondéré} contre
{UniFrac pondéré}, ce qui n'est pas une question de pondération mais de pondération *par les
longueurs de branches*.

Une règle du type « ne garder que les métriques pondérées » serait donc fausse ici : elle
supprimerait le résultat digestif porté par Bray-Curtis et Jaccard pour ne conserver que la
métrique dont le comportement est atypique.

## 4. Recommandation

**Ne pas désigner une métrique unique, mais un quatuor déclaré et une règle d'assertion.**

1. **Rapporter les quatre métriques partout**, comme le manuscrit le fait déjà, avec Shannon en
   indice alpha de référence et Bray-Curtis en distance de référence pour les chiffres cités dans
   le texte courant — les deux sont pondérés par l'abondance, donc reproductibles, et Bray-Curtis
   n'est pas la métrique isolée du jeu.
2. **Règle d'assertion** : une conclusion n'est énoncée comme établie que si elle est soutenue par
   au moins une métrique pondérée par l'abondance **et** une métrique de présence. Sinon elle est
   rapportée comme dépendante de la métrique, en nommant laquelle. Cette règle est à écrire au
   §8.6 et à appliquer mécaniquement.
3. **Conséquence sur le texte, à appliquer** : le §8.9 déplace son accent de la caudale vers les
   compartiments digestifs ; l'affirmation midgut ≠ hindgut est requalifiée ; l'inversion du
   dimorphisme sexuel est retirée ; et tout rapport externe / interne cité porte le nom de son
   indice.

Cette règle a un coût qu'il faut accepter d'avance : elle retire au manuscrit son résultat caudal,
qui était le plus spectaculaire, et le remplace par un résultat digestif moins frappant mais
soutenu par quatre métriques et par une prédiction posée avant l'analyse.

## 5. Ce que cette note ne fait pas

Elle ne teste pas la partition de variance tissu / site / run sur les quatre indices — elle n'a
porté que sur les contrastes appariés. Elle ne traite pas non plus l'abondance différentielle,
dont la méthode reste à choisir et dont la sensibilité à la métrique est un problème distinct.
Les contrastes alpha sont appariés par individu, moyennés sur les runs, et testés par Wilcoxon
signé ; le dimorphisme sexuel est testé non apparié, sans ajustement sur la taille — les
diagnostics antérieurs ajustaient sur la taille, donc les p ne sont pas comparables terme à terme
avec eux.
