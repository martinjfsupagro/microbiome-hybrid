# Deux précisions de l'utilisateur et leurs conséquences sur le plan d'analyse

Notes datées de la session du 23 août 2026, avant réception du génotypage complet.

## Précision 1 : les sites « allopatrie » sont des parapatries à barrière physique

Les trois sites codés `allopatrie` dans `index_hybride_andre.csv` — Ain 2014, Ain 2015 (Cab),
canal Durance (Caa) — ne sont pas des sites mono-spécifiques. Les deux espèces y sont présentes
mais ne peuvent pas se croiser, un élément physique faisant barrière.

**Réserve sur le confondant taille-espèce ci-dessous** : il est établi sur les seuls individus
actuellement génotypés. Le génotypage des « Ch » peut le lever — si des toxostomes de grande taille
ou des hotus de petite taille apparaissent, le chevauchement se rétablit et le contraste parental
redevient estimable. À ne pas traiter comme une limite définitive avant ce retour.

### Ce que ça change de bon

C'est le **même dispositif que Guivier et al. 2017** : deux stations séparées par 30 km et une
succession de barrages sur la rivière Suran, décrites comme limitant fortement le contact et le
potentiel d'hybridation. La continuité de design entre les deux articles est donc plus forte que je
ne l'avais écrit — et surtout, les sites à barrière fournissent un **contrôle négatif interne** :
des populations en contact géographique mais sans flux de gènes. C'est exactement le témoin qui
manque à la plupart des études de zones d'hybridation, et il est réplicable ici sur deux rivières
(Ain et Durance).

La conséquence sur le vocabulaire est immédiate : ne pas écrire « allopatrie » dans l'article. Le
terme juste est **parapatrie à isolement physique** ou **parapatrie sans hybridation**, et il faut
décrire la nature de la barrière pour chaque site — un barrage n'est pas un canal, et un lecteur de
*Molecular Ecology* fera la différence. Le champ `role_population` du fichier de métadonnées doit
être recodé en conséquence.

### Ce que ça change de moins bon : un facteur confondant que je n'avais pas isolé

À Ain 2014, seul site portant les deux parentaux en effectif exploitable, les deux espèces ne se
chevauchent pas en taille : les 10 toxostomes mesurent de 10,5 à 20,0 cm, les 4 hotus de 30,0 à
39,5 cm. La corrélation entre espèce et log-taille y est de -0,89. **Le contraste parental à Ain
est donc confondu avec la taille du poisson.**

Le modèle mixte le montre bien : l'effet espèce sur log-richesse ASV passe de 0,377 (p=0,014) sans
la taille à 0,815 (p=0,012) avec la taille, cette dernière absorbant une part du signal sans être
elle-même significative (p=0,130) — signature classique de colinéarité. Sur les 47 individus
parentaux poolés tous sites, taille et site contrôlés, le contraste parental n'est plus
significatif (coef 0,293, p=0,151).

À ce stade, **il n'existe pas de test propre du contraste parental** dans le jeu de données : à Ain
il est confondu avec la taille, à Avignon l'effectif toxostome est de 2. C'est une limite à écrire,
pas un résultat à sauver.

## Précision 2 : une part des « Ch » sont probablement des toxostomes

Si le génotypage reclasse une fraction des 132 « Ch » en parentaux, le problème central du jeu de
données — 12 toxostomes dont 10 sur un seul site-année — se résorbe. Effet sur le plafond du plan
équilibré exigé par l'indice 4H, en supposant que 60 % des reclassés soient des Pt :

| part des Ch reclassés en parentaux | peau | branchie | midgut | hindgut |
|---|---|---|---|---|
| 0 % (état actuel) | 12 | 11 | 10 | 11 |
| 15 % | 21 | 23 | 20 | 22 |
| 30 % | 30 | 34 | 29 | 33 |
| 50 % | 42 | 50 | 42 | 48 |

Et sur la puissance du contraste parental intra-site (log-richesse, sd résiduelle 0,55) :

| effectifs | ratio ×1,3 | ×1,5 | ×2,0 |
|---|---|---|---|
| 4 Cn / 10 Pt (Ain aujourd'hui) | 0,12 | 0,21 | 0,50 |
| 12 / 12 | 0,20 | 0,41 | 0,84 |
| 20 / 20 | 0,31 | 0,62 | 0,97 |
| 25 / 25 | 0,38 | 0,72 | 0,99 |

Le seuil utile est autour de 20 individus par espèce et par site : en dessous, seul un effet de
richesse doublée est détectable. Ce chiffre est le critère à appliquer au fichier de génotypage
dès sa réception, avant toute analyse.

### Une prédiction falsifiable à poser maintenant

À Ain 2014, la taille sépare parfaitement les deux espèces, avec un intervalle vide entre 20,0 et
30,0 cm (seuil naturel à 25 cm). Les 19 Ch de Ain 2015 (Cab), même rivière, même barrière, ont une
distribution de taille **franchement bimodale** : 9 individus entre 17,0 et 22,0 cm, puis un vide
de 7,5 cm entre 32,5 et 40,0 cm, puis 9 individus entre 40,0 et 50,0 cm.

Prédiction : sur un site où le croisement est physiquement impossible, ces deux modes correspondent
aux deux espèces parentales, et non à des hybrides. Le génotypage doit donc classer les 9 petits en
toxostomes et les 9 grands en hotus, avec index hybride à 0 ou 1 et non intermédiaire.

**Écrire cette prédiction avant de voir le fichier, et la vérifier après.** Si elle se réalise, le
génotypage est cohérent avec la biologie du site et le recodage est fiable. Si elle échoue — index
intermédiaires à un site sans croisement possible — alors soit la barrière est perméable, soit
l'index hybride a un problème de calibration. Dans les deux cas il faut le savoir avant d'analyser.

Le site canal (Caa) ne permet pas ce test : ses 20 Ch mesurent tous de 9,5 à 18,0 cm, sans
bimodalité, et le seuil de 25 cm est calibré sur l'Ain — sa transposition à la Durance n'est pas
validée. Ce sont probablement des juvéniles, cohérent avec le fait que ce site est aussi celui où
les sexes sont majoritairement indéterminés.

## Ce qui reste vrai malgré ces deux précisions

La régression sur index continu n'y gagne presque rien : elle a besoin d'individus **répartis sur
l'axe**, et reclasser des Ch en parentaux les envoie aux extrémités. Sa puissance intra-site reste
faible — 0,18 pour un effet ×1,5 à n=25 — et l'analyse principale doit rester un modèle global
multi-sites. Le gain porte sur le contraste parental et sur l'indice 4H, pas sur la pente.

Deux choses à demander à André avec le fichier de génotypage :

1. la **distribution** de l'index, globale et par site, et pas seulement les valeurs — c'est elle
   qui décide si une monotonie est testable sur tout l'axe ou seulement sur sa moitié basse ;
2. la **nature de la barrière** pour chacun des trois sites concernés (barrage, canal, distance),
   pour la décrire correctement en Methods et justifier leur statut de contrôle négatif.

## Réserve de métrique sur l'ensemble des chiffres de cette note

Tous les tests de cette note portent sur la richesse ASV observée. L'analyse de reproductibilité
technique menée en parallèle établit que cette métrique est peu reproductible sur les taxons rares
(48 % de recapture des ASV à 1-3 lectures) et que les analyses de diversité du manuscrit reposeront
sur des métriques pondérées par l'abondance. Les valeurs ci-dessus gardent leur statut de diagnostic
de faisabilité ; elles devront être recalculées en Shannon ou Bray-Curtis avant toute reprise dans
les Results, y compris les SD résiduelles qui fondent les calculs de puissance.
