# Décisions à verrouiller avant réception du fichier de génotypage

Liste établie le 23 août 2026, en attente du retour d'André (index hybrides, paramètres des sites
et nature des barrières). Chaque élément ci-dessous est une décision qui **perd sa valeur si elle
est prise après avoir vu les données** : consignée maintenant, elle est un choix a priori ;
consignée après, elle devient un choix post-hoc que la relecture sanctionnera.

## 1. Paramètres d'analyse à fixer par écrit maintenant

| paramètre | valeur proposée | pourquoi maintenant |
|---|---|---|
| seuil de core ρ pour l'indice 4H | 50 % des hôtes | Camper et al. montrent qu'un ρ bas favorise systématiquement la dimension Intersection : choisir ρ après avoir vu l'indice serait indéfendable |
| échelle taxonomique pour le 4H | à fixer (phylum dans les figures publiées) | même raison ; une échelle élevée favorise aussi Intersection |
| fenêtre d'index « intermédiaire » pour la discrétisation 4H | à fixer en amont | l'indice exige trois classes non chevauchantes ; définir la fenêtre après avoir vu la distribution revient à choisir le résultat |
| profondeur de raréfaction | 3 000 lectures | déjà appliquée ; à justifier explicitement contre les 34 000 de Guivier 2017 |
| nombre de tirages de raréfaction | 1 000, indices moyennés | méthode de Guivier 2017, plus robuste qu'un tirage unique et peu coûteuse |
| structure du modèle principal | index en effet fixe, site et individu en effets aléatoires, profondeur et taille en covariables | la taille est confondue avec l'espèce à Ain (r = -0,89) : sa présence au modèle doit être décidée avant, pas selon qu'elle rend l'effet significatif |

## 2. Prédiction falsifiable déjà posée

Les 19 « Ch » d'Ain 2015 ont une distribution de taille bimodale (9 individus de 17 à 22 cm, vide
de 7,5 cm, 9 individus de 40 à 50 cm) et le site est à croisement impossible. Prédiction : le
génotypage classe les 9 petits en toxostomes et les 9 grands en hotus, index à 0 ou 1, aucun
intermédiaire. Détail et calibration dans `note_precisions_design.md`.

Critère de recevabilité du fichier, posé avant de le voir : **20 individus par espèce et par site**
est le seuil en dessous duquel le contraste parental intra-site ne détecte qu'un doublement de
richesse.

## 3. Ce qui n'attend pas André du tout

**L'axe tissulaire est entièrement indépendant du génotypage.** 109 individus ont les quatre tissus
exploitables et 160 en ont au moins trois, sans qu'aucun index soit nécessaire. Or c'est cet axe que
le diagnostic désignait comme ossature de l'article : tissu à 18,7 % de la variance de log-richesse
contre 10,9 % pour le site et 0,26 % pour le run. Deux analyses sont prêtes à tourner :

- le test de composition (PERMANOVA sur distances UniFrac) entre midgut et hindgut, seul test
  permettant une comparaison terme à terme avec l'absence de différenciation rapportée en 2017 —
  le contraste de richesse, lui, est déjà fait (ratio 0,83, p = 0,005) ;
- la réplication du gradient externe/interne sur composition et non seulement sur richesse.

Ces analyses relèvent du profil principal, pas de la recherche bibliographique.

## 4. Deux points de nettoyage à traiter avant tout appariement automatique

**Identifiants mal formés : deux individus, pas quatre** (correction de ce que j'avais écrit).
`14Avi1036-Cn03A` et `14Avi1037-01A` portent un tiret à la place du code espèce, sur les trois runs
chacun. Sans correction, ces deux poissons d'Avignon décrocheront silencieusement de l'appariement
génotype ↔ microbiote — et Avignon est l'un des deux seuls sites à porter les deux parentaux.

**Structure des runs : question close.** Tranchée dans la conversation d'analyse des données, et le
Materials and Methods est à jour. La structure caractérisée est : durance1 = préparation de
librairie distincte ; durance2 et durance3 = deux séquençages d'une même librairie (rho de
profondeur 0,9987, Bray-Curtis 0,118 contre 0,248 entre librairies). La conclusion établie est que
préparation de librairie et run expliquent 0,03 % et 0,005 % de la variance contre 9,2 % pour le
tissu et 37,7 % pour l'identité du poisson, que technique et biologique sont croisés et non
confondus, et qu'aucune correction de batch n'est nécessaire. Ma formulation « probablement deux
passages du même pool » allait dans le bon sens mais n'a plus à être vérifiée : elle est documentée.

## 4bis. Conséquence de cette analyse sur mes propres résultats

La même analyse établit que **la richesse observée est la mauvaise métrique** : un re-séquençage de
la même librairie ne retrouve que 48 % des ASV présents à 1-3 lectures, et la dissimilarité de
Jaccard entre deux séquençages d'une librairie atteint 0,45 contre 0,12 pour Bray-Curtis. D'où la
décision, actée dans le manuscrit, de fonder les analyses de diversité sur des métriques pondérées
par l'abondance plutôt que sur la richesse observée ou des indices non pondérés.

Or **tous les tests que j'ai produits dans cette conversation portent sur la richesse ASV
observée** : le contraste apparié midgut/hindgut (ratio 0,83, p = 0,005), le gradient
externe/interne, le dimorphisme sexuel, la partition de variance (tissu 18,7 %), et l'ensemble des
calculs de puissance. Ils restent valables comme diagnostic de faisabilité — c'est leur usage — mais
**aucun ne doit être repris tel quel dans les Results.** À refaire en Shannon ou Bray-Curtis avant
toute rédaction, en particulier :

- le contraste midgut/hindgut, dont l'écart est le plus faible des six (0,83) et donc le plus
  susceptible d'être un artefact de taxons rares — c'est précisément le résultat que je présentais
  comme une non-réplication de Guivier 2017 ;
- les SD résiduelles servant de base aux calculs de puissance (0,44 en peau à 0,76 en midgut), qui
  changeront sur une métrique pondérée et donc déplaceront tous les seuils d'effectif annoncés.

Le gradient externe/interne, lui, est assez massif (coefficient 0,598, z = 8,7) pour survivre à un
changement de métrique — mais il faut le vérifier, pas le supposer.

## 5. Ce qui est effectivement bloqué

Le cadrage de l'introduction : ordre des hypothèses, choix entre annoncer les deux analyses (index
continu et 4H) ou réserver le 4H à la discussion, et formulation de la phrase de nouveauté — qui a
perdu l'argument du quatrième compartiment depuis la lecture de Guivier 2017 et repose désormais
sur l'index continu et l'effectif. Tout cela dépend de la distribution de l'index et du statut
exact des sites à barrière. Rien à gagner à l'écrire avant.