# Questions de recherche attaquables — diagnostic sur données réelles

Projet microbiome-hybrid · évaluation faite sur `depth_per_sample.tsv` (2 174 échantillons rattachés
aux 181 individus de `index_hybride_andre.csv`), `clean_table_summary.txt` et le plan d'échantillonnage.
Toutes les valeurs de puissance et de variance ci-dessous sont calculées, pas estimées à vue.

## Ce que dit le diagnostic quantitatif

| Constat | Valeur mesurée |
|---|---|
| Variance de log(richesse ASV) expliquée par le tissu | 18.7 % |
| ... par le site-année | 10.9 % |
| ... par le run MiSeq | 0.26 % |
| ... résiduelle (individu) | 69.0 % |
| Individus avec les 4 tissus exploitables après raréfaction | 109 / 181 |
| Individus avec ≥ 3 tissus exploitables | 160 / 181 |
| Individus toxostome (Pt) | 12, dont 10 au seul site-année Ain 2014 |
| Individus hotu (Cn) | 37, répartis sur 4 sites |
| Individus « Ch » en attente de génotypage | 132 |
| SD résiduelle de log(richesse) intra site×tissu | 0.44 (peau) → 0.76 (midgut) |

## Tableau de faisabilité

Voir `questions_recherche_faisabilite.csv` pour le détail par question.

### Q1 — Les deux parentaux diffèrent-ils dans leur microbiote ?

**Statut : Attaquable maintenant, mais fragile**

- Données mobilisables : Cn 37 ind. / Pt 12 ind. ; Cn+Pt cohabitent seulement à Ain 2014 (Cn4/Pt10) et Avignon (Cn22/Pt2)
- Puissance : Contraste intra-site : 0.21 (Ain) et 0.16 (Avignon) pour un effet x1.5 sur la richesse. En poolant : 0.57
- Limite structurelle : Le contraste parental est confondu avec le site-année ; Pt n'existe qu'à Ain 2014 en effectif utile
- Verdict : Préalable obligatoire mais à formuler comme un test à faible puissance, pas comme un résultat acquis

### Q2 — Le microbiote des hybrides est-il intermédiaire, transgressif ou dominant ?

**Statut : Bloquée jusqu'à l'index hybride**

- Données mobilisables : 132 Ch à génotyper ; 0 individu positionné entre 0 et 1 aujourd'hui
- Puissance : Régression intra-site n=25 : 80 % de puissance seulement à partir d'un rapport de richesse de ~2.4 (peau) à >3 (midgut)
- Limite structurelle : La forme de la distribution de l'index est inconnue ; si les Ch sont bimodaux, aucun test de monotonie n'est possible
- Verdict : Question centrale, mais l'analyse doit être un modèle global multi-sites (index en effet fixe, site en effet aléatoire), pas des tests par site

### Q3 — L'effet de l'hybridation est-il uniforme entre les quatre tissus ?

**Statut : Attaquable — le plus solide du jeu**

- Données mobilisables : 109 individus avec les 4 tissus utilisables, 51 avec 3 tissus ; appariement intra-individu
- Puissance : Le tissu explique 18.7 % de la variance de richesse contre 0.3 % pour le run ; contrastes appariés
- Limite structurelle : Le midgut est le tissu le plus bruité (SD résiduelle 0.76 vs 0.44 pour la peau) et le plus perdu à la raréfaction
- Verdict : À placer au cœur de l'article : c'est le seul axe où le plan est apparié et bien répliqué

### Q4 — Le microbiote suit-il la génétique de l'hôte ou l'environnement local ?

**Statut : Attaquable partiellement, dès maintenant pour la partie environnementale**

- Données mobilisables : 9 sites-années, 3 rivières (Durance, Ardèche, Ain), 2 années
- Puissance : Le site explique 10.9 % de la variance de richesse (p<1e-15) — effet environnemental établi
- Limite structurelle : Site, rivière, année et rôle de population sont largement confondus ; Ain est échantillonné en 2014 et 2015, c'est le seul levier de séparation année/site
- Verdict : La moitié environnementale est déjà démontrable ; la comparaison de poids génétique/environnement attend l'index

### Q5 — L'asymétrie du sens de l'introgression change-t-elle l'effet sur le microbiote ?

**Statut : Non attaquable en l'état**

- Données mobilisables : Baume (25 Ch, Ardèche) vs Avignon (22 Cn + 2 Pt, Durance)
- Puissance : Comparaison à 2 sites, sans réplication du niveau « sens de l'introgression »
- Limite structurelle : Les deux sites sont sur des rivières différentes ; le sens de l'introgression n'est pas répliqué et le libellé lui-même est ambigu (receveur ou donneur ?)
- Verdict : À reléguer en observation exploratoire ou à retirer ; ne peut pas porter une hypothèse de l'introduction

### Q6 — Les effets biologiques dépassent-ils le bruit technique ?

**Statut : Déjà répondu**

- Données mobilisables : 728 librairies re-séquencées sur 3 runs MiSeq
- Puissance : Run = 0.26 % de la variance de richesse ; corrélation inter-run de log-richesse r=0.81 (run1 vs 2/3) et 0.99 (run2 vs 3)
- Limite structurelle : Les runs 2 et 3 sont quasi proportionnels en profondeur (ratio médian 0.86, r=0.999) : ce sont probablement deux passages du même pool, pas trois réplicats indépendants
- Verdict : Argument méthodologique fort, à mettre en Methods/supplément — pas une question de recherche

### Q7 — La variation individuelle non expliquée est-elle structurée par un facteur mesuré (taille, sexe, année) ?

**Statut : Attaquable maintenant**

- Données mobilisables : taille et poids 174/181 ; sexe 108/181 informatif (77 M, 31 F) ; 69 % de la variance de richesse reste résiduelle
- Puissance : Suffisant pour la taille (covariable continue, n=174) ; limité pour le sexe
- Limite structurelle : Le sexe est indéterminé pour 52 individus, potentiellement les plus petits/juvéniles — manquant non aléatoire
- Verdict : À traiter en covariables du modèle, pas en question à part entière

## Trois points de vigilance découverts en inspectant les données

1. **Les 3 runs MiSeq ne sont pas 3 réplicats indépendants.** Les runs 2 et 3 ont des profondeurs
   quasi proportionnelles par librairie (rapport médian 0.86, corrélation de log-profondeur r = 0.999,
   corrélation de log-richesse r = 0.994), alors que le run 1 corrèle à r = 0.81 avec les deux autres.
   Cela ressemble à deux passages d'un même pool re-normalisé plutôt qu'à trois préparations
   indépendantes. Conséquence : ne pas annoncer « triple réplication technique » en Methods sans
   vérifier l'historique de préparation auprès d'André.

2. **Deux individus séquencés n'existent pas dans les métadonnées.** `15Cab1021Ch` et `15Cab1022Ch`
   sont présents dans la table de profondeur mais absents des 181 individus (ce sont les mock retirés
   à l'étape de nettoyage — cohérent). En revanche `14Avi1036-Cn03A` et `14Avi1037-01A` portent des
   identifiants mal formés (tiret à la place du code espèce) : à corriger avant tout appariement
   automatique génotype ↔ microbiote.

3. **Le site canal (Caa) est presque perdu sur deux tissus.** 3/20 individus exploitables en peau et
   9/20 en midgut après raréfaction, contre 20/20 en branchie. Ce site est une des deux références
   d'allopatrie : le déséquilibre est donc concentré exactement là où il coûte le plus cher.

## Recommandation de cadrage

Le jeu de données soutient un article dont l'ossature est **le gradient tissulaire**, avec
l'hybridation comme facteur testé à l'intérieur de cette ossature — et non l'inverse. Le tissu est
le seul facteur à la fois fortement structurant, apparié intra-individu et bien répliqué. La question
hybride reste la question d'intérêt, mais elle sera portée par un modèle global (index hybride en
effet fixe, site et individu en effets aléatoires) et non par des comparaisons site par site, qui
n'ont pas la puissance nécessaire.