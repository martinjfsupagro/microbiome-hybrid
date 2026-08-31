# docs/decision_phylo_and_category.md — Etapes A1 et A2

## A1 — metriques phylogenetiques (script 21 + 21b)

**Produit.** UniFrac non pondere, UniFrac pondere normalise, Faith PD, plus les trois
metriques alpha taxonomiques RECALCULEES sur les memes tirages. 1 784 echantillons,
profondeur 3 000, **N = 400 tirages** (deux chaines de 200 a graines disjointes), aligne
sur les matrices taxonomiques deja produites afin que les quatre metriques beta soient
constituees de la meme facon.

**Outils.** Image QIIME2 `amplicon_2026.1.sif` : unifrac 1.3.0 (implementation C++),
biom 2.1.16, skbio 0.6.2. **Aucune installation.** picante, GUniFrac, phyloseq et ape
sont absents du R du projet ; l'image les rend inutiles.

**Convergence, MESUREE et non supposee.** L'ecart entre deux chaines independantes, a
comptes appariés (200 chacune) :

| Metrique | erreur MC relative | correlation entre chaines |
|---|---|---|
| UniFrac non pondere | 0.00082 | 0.999867 |
| UniFrac pondere | 0.00052 | 0.999993 |
| Faith PD | 0.00134 | — |
| richness | 0.00107 | — |
| shannon | 0.00043 | — |
| invsimpson | 0.00184 | — |

Toutes sous 0.2 %. La convergence etablie sur Bray-Curtis et Jaccard n'etait PAS
supposee transferable a UniFrac : elle est mesuree ici. Deux chaines independantes sont
necessaires — comparer une moyenne cumulee a N contre une a 2N serait autocorrele
(tirages partages).

**Controle du pipeline, qui pouvait echouer.** Les trois metriques alpha taxonomiques
recalculees ici (N=400, mes tirages) contre celles de `alpha_mean_1000.tsv` (N=1000,
tirages independants, autre implementation) :

| Metrique | r | ecart relatif moyen |
|---|---|---|
| richness | 0.999999 | 0.00090 |
| shannon | 0.999999 | 0.00037 |
| invsimpson | 0.999997 | 0.00145 |

Un defaut dans ma lecture de la table, ma rarefaction ou mon indexage serait apparu ici.
L'accord valide toute la chaine.

**Etendues.** UniFrac non pondere 0.0024 a 0.9646 (moyenne 0.7312) ; pondere normalise
0.0008 a 0.1798 (moyenne 0.1006). L'ecart d'echelle entre les deux est attendu : le non
pondere est domine par la presence de taxons rares, le pondere par les taxons abondants,
largement partages.

**Piege rencontre, a retenir.** `unifrac.weighted_normalized` annonce
`table: Union[str, biom.table.Table]` mais n'accepte PAS un `biom.Table` en memoire : il
fait `str(table)` puis valide un chemin (`ValueError: Table does not appear to be a
BIOM-Format v2.1`). `unifrac.unweighted` l'accepte. La signature ne decrit donc pas
l'implementation. Les trois appels passent desormais par un fichier BIOM — requis de
toute facon par `faith_pd`, qui est file-only. Detecte par une repetition a faible N
avant l'engagement long : le job long aurait echoue apres la lecture.

**Cout.** 6.4 s par iteration, 400 iterations en ~42 min sur 32 CPU.

---

## A2 — part de variance de la categorie, ENCADREE (script 20)

**Pourquoi un encadrement.** Categorie, station et position dans la plaque sont
enchevetrees (categorie x colonne : V de Cramer = 0.504 ; 0.56 a 0.69 dans les trois
stations a gradient complet). En PERMANOVA sequentielle l'ordre change la valeur, donc
les deux ordres sont rapportes. Rapporter un seul ordre serait choisir la reponse.

**Pourquoi stratifie par tissu.** 168 des 180 poissons occupent la MEME colonne dans les
quatre tissus. Dans un modele groupe portant l'identite du poisson, la position est
entierement absorbee et n'est pas estimable. Ce n'est pas un oubli du script 14 : c'est
une contrainte du plan.

### Resultat : la categorie explique 1.4 a 3.3 % de la composition

| Metrique | apres station et position | servie en premier | facteur |
|---|---|---|---|
| Bray-Curtis | 0.0142 | 0.0327 | 2.30 |
| Jaccard | 0.0136 | 0.0208 | 1.52 |
| UniFrac non pondere | 0.0158 | 0.0243 | 1.54 |
| UniFrac pondere | 0.0165 | 0.0319 | 1.93 |

Pour situer : la STATION explique 0.15 a 0.31 selon la metrique, soit **dix a vingt fois
plus** que la categorie. La position (1 seul df) explique 0.014 a 0.020, soit **autant
que la categorie qui en consomme deux**.

### Le resultat le plus important : aucun tissu n'est detecte par les quatre metriques

Nombre de runs sur 3 avec p < 0.05, dans les deux dispositifs (sequentiel : categorie
apres station et position ; bloque : station fixee par les blocs de permutation,
position ajustee) :

| Metrique | caudale | branchie | midgut | hindgut |
|---|---|---|---|---|
| Bray-Curtis | 2/3 ; 2/3 | **3/3 ; 3/3** | 0/3 ; 0/3 | 0/3 ; 0/3 |
| Jaccard | 0/3 ; 1/3 | **3/3 ; 3/3** | **3/3 ; 3/3** | 2/3 ; 1/3 |
| UniFrac non pondere | 2/3 ; 3/3 | **0/3 ; 0/3** | **3/3 ; 3/3** | 0/3 ; 0/3 |
| UniFrac pondere | 3/3 ; 3/3 | 3/3 ; 0/3 | 0/3 ; 3/3 | 0/3 ; 0/3 |

Robuste (3/3 dans LES DEUX dispositifs) : branchie pour 2 metriques sur 4, midgut pour
2 sur 4, caudale pour 1, hindgut pour 0. **Aucun tissu n'atteint 4/4.**

**CE QUE CELA CHANGE PAR RAPPORT A MA CONCLUSION SUR DEUX METRIQUES.** Avec Bray-Curtis
et Jaccard seuls, j'aurais conclu "seule la branchie porte un effet robuste". C'est
faux : UniFrac non pondere donne **0/3 pour la branchie dans les deux dispositifs**, et
UniFrac pondere bascule entre dispositifs pour la branchie comme pour le midgut. Ajouter
les metriques phylogenetiques a AFFAIBLI le dossier, pas renforce. Une conclusion tiree
des deux seules metriques taxonomiques aurait ete une surinterpretation.

**Statut du mecanisme de la discordance : HYPOTHESE.** La discordance ne se range pas
selon l'axe pondere/non pondere (branchie : significative en Bray, Jaccard et UniFrac
pondere, pas en non pondere ; midgut : l'inverse). Une explication possible est que la
difference entre categories porte dans la branchie sur des taxons phylogenetiquement
proches et dans le midgut sur des taxons rares mais distants. **Aucun temoin ne teste
cela** : c'est une hypothese.

### Deux defauts de mes propres comparaisons, corriges

1. **Ratio applique a des tests a permutation contrainte.** J'avais divise le R² des
   tests a permutations bloquees par `df/(n-1)`, qui est l'attendu sous permutation
   LIBRE. Le null contraint n'a pas cette esperance ; ces ratios etaient sans valeur.
   Seuls les p de ces tests sont interpretables.
2. **Ratio applique a un terme servi en dernier.** `df/(n-1)` est l'esperance sous le
   null GLOBAL (aucun terme n'a d'effet). Pour un terme servi apres un facteur fort
   (station, 8 df, R² 0.15-0.31), l'attendu n'est plus celui-la : seul le p de
   permutation repond. Les ratios ne sont rapportes que pour les termes servis en
   premier (categorie en ordre MAX : 1.45 a 2.48 ; position en ordre MIN : 2.09 a 2.21 —
   ce dernier replique l'effet de position etabli aux scripts 17-18, avec un codage
   different (rang, 1 df) et la station au lieu du site).

### Temoins

- **Sous-plan separable** (echantillons en colonnes occupees par toutes les categories
  de leur station ; n median 67 contre 147) : **0/12 strates significatives** pour
  Bray-Curtis et Jaccard. Mais n est divise par ~2 et les modeles sequentiels n'y ont
  PAS ete lances : ce n'est ni une confirmation ni une refutation, et aucune comparaison
  de R² a l'identique n'est disponible.
- **Rosieres**, seule station ou categorie et position sont statistiquement
  independantes (V = 0.181, p = 0.35) : **0/12 significatif**, sur 4 hybrides contre
  21 Pt. Sous-dimensionne, donc non concluant.

## Consequence pour l'analyse ecologique

1. **Aucune affirmation globale du type "les hybrides different" n'est soutenable.** Le
   manuscrit devra dire quelle metrique soutient quelle affirmation, et dans quel tissu.
2. L'effet de categorie est **du meme ordre par degre de liberte que l'effet de
   position**, et dix a vingt fois plus petit que l'effet de station.
3. Le hindgut est le tissu le plus faible : aucune metrique ne le detecte dans les 3 runs, quel que soit le dispositif. Seul Jaccard atteint la significativite, dans 2 runs sur 3 en sequentiel (p = 0.036, 0.041, 0.063) et 1 sur 3 a station bloquee (p = 0.042, 0.052, 0.123). Les trois autres metriques ne detectent rien dans aucun run. CORRECTION 2026-08-31 : la redaction anterieure disait « ne montre rien avec aucune metrique », ce qui contredisait la grille de detectabilite de ce meme document.
4. L'analyse "intermediaire vs transgressif" devra se faire la ou le gradient existe
   intra-station (3 stations, 74 individus) en sachant que c'est aussi la que le
   confondant de position est le plus fort.

## Fichiers
- `results/phylo_diversity/` : alpha_phylo_mean.tsv (4 metriques, memes tirages),
  unifrac_{unweighted,weighted}_mean.tsv.gz, phylo_convergence.tsv, phylo_summary.txt
- `results/rarefaction/beta_mean_unifrac_{unweighted,weighted}_N400.rds` (script 21b)
- `results/var_partition_cat/` : category_partition.tsv (avec colonne `metrique`),
  category_summary.txt
- `results/var_partition_cat/fig_category_effect.png`
