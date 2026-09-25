# Génotypage sur 25 chromosomes : intégration et points à trancher

Intégration des quatre fichiers du 7 septembre 2026 : `nouveau tableau_AG_Sept_2026.xlsx`,
`genome_hotox.csv` (Q-values par chromosome), `genome_hybride.Rmd` et son rendu HTML. Toutes les
valeurs ci-dessous sont recalculées depuis les fichiers, y compris par reproduction indépendante
des calculs du script R.

## 1. Vérifications : tout se reproduit

- **Le tableau de comptage du mail concorde exactement avec le fichier**, sur les onze
  site-années et les trois classes. Les deux écarts d'un individu signalés en août sont corrigés.
- **Les colonnes Q et R se recalculent depuis les Q-values** : D à l'identique (écart maximal
  0,000000), médiane à 0,0095 près (arrondi d'écriture).
- **La règle de classification du script reproduit exactement la colonne P** : 57 Bleu = Cn,
  76 Rouge = Pt, 42 Vert = Hy, sans aucun désaccord.
- **Le clustering se reproduit exactement** : tailles de clusters 88 / 67 / 9 / 4 / 3 / 3 / 1 à
  k = 7 et 88 / 52 / 15 / 9 / 4 / 3 / 3 / 1 à k = 8, identiques au rendu HTML.
- **La polarité des Q-values est harmonisée** malgré l'alternance des préfixes Q1 (9 colonnes) et
  Q2 (16 colonnes) : chez les hotus purs, les deux familles de colonnes donnent 0,9855 et 0,9857 ;
  chez les toxostomes purs, 0,0038 et 0,0039. Aucune colonne n'est inversée.
- **Convention d'orientation** : médiane proche de 1 = hotu, proche de 0 = toxostome. Inverse de
  l'ancien `index_hybride_andre.csv`, identique au tableau d'août.

## 2. Ce qui a changé depuis les 12 chromosomes

Seize individus changent de classe, pour un solde net de +12 hybrides — cohérent avec le mail :

| août (12 chr) → septembre (25 chr) | n |
|---|---|
| Pt → Hy | 13 |
| Cn → Hy | 1 |
| Hy → Pt | 1 |
| Hy → Cn | 1 |

Les effectifs passent de 59 / 30 / 91 à **59 Cn / 42 Hy / 79 Pt**. Aucun individu ne traverse
d'un parental à l'autre. Les 14 nouveaux hybrides ont tous une médiane restée à l'extrême
(0,0001 ou 0,9999) mais un D qui explose — par exemple `2014_Man_1010`, D de 0,0000 à 0,5419. Ce
sont bien des individus détectés comme introgressés sur un chromosome que les 12 premiers ne
couvraient pas.

## 3. Le point central : la classe Hy réunit deux réalités génomiques

La condition qui définit le groupe Vert dans le script est
`(médiane > 0,05 & médiane < 0,94) | (écart_max > 0,12)`. Le `|` est un OU, et le script d'André
le signale lui-même en commentaire. Conséquence : **tout individu dont D dépasse 0,12 devient
hybride, quelle que soit sa médiane**. Sans cette clause, ces individus ne seraient dans aucun
groupe — ils échouent aussi aux conditions Rouge et Bleu, qui exigent D < 0,12.

Ce n'est pas une erreur : c'est le choix, assumé, d'appeler « hybride » un individu introgressé.
Mais il produit une classe hétérogène :

| sous-type | n | médiane | D | chromosomes introgressés |
|---|---|---|---|---|
| génome intermédiaire (0,05 < médiane < 0,94) | 20 | 0,094 à 0,929 | 0,084 à 0,537 | non défini |
| quasi-pur, introgressé | 22 | 0,0001 ou 0,9999 | 0,151 à 0,600 | 1 à 6 (médiane 1) |

**Dix-sept des 22 quasi-purs sont introgressés sur exactement un chromosome sur 25.** C'est ce que
le mail appelle « très très très dilué ». Et parmi eux, 19 penchent vers le toxostome contre 3
vers le hotu : l'introgression détectée est fortement asymétrique.

### Trois éléments qui documentent la fragilité de la frontière

**Le clustering ne sépare pas ces 22 individus des purs.** À k = 8, le cluster qui contient les 76
toxostomes purs contient aussi 12 hybrides, et celui des 49 hotus purs en contient 3. Au total,
**22 des 42 hybrides tombent dans un cluster dont la majorité est parentale**. Les clusters
exclusivement hybrides (1, 2, 4, 7, 8) rassemblent 20 individus — exactement les génomes
intermédiaires. Le profil génomique complet retrouve donc la partition à deux sous-types, pas la
classe Hy à 42.

**Le décompte de chromosomes introgressés chevauche les classes.** Six individus classés purs en
ont au moins un (3 Cn à 1, 1 Cn à 2, 1 Cn à 3, 1 Pt à 1), alors que 17 hybrides n'en ont qu'un.
La cause est une incohérence entre les deux critères du script : le décompte utilise des seuils
absolus (Q > 0,12 ou Q < 0,88) tandis que D est relatif à la médiane de l'individu. Un hotu de
médiane 0,95 avec un chromosome à 0,87 compte un chromosome introgressé mais un D de seulement
0,08. Les deux critères peuvent donc se contredire.

**En revanche le seuil D = 0,12 est remarquablement stable.** Il tombe dans un intervalle vide de
la distribution : la plus haute valeur sous le seuil est 0,1191, la plus basse au-dessus 0,1301.
Tout seuil entre 0,12 et 0,15 donne exactement 42 hybrides ; à 0,11 on en aurait 49 et à 0,10,
54. Le choix se situe au début d'un plateau, ce qui est un bon argument de robustesse à publier.

## 4. Conséquences sur le plan d'analyse

Individus utilisables (≥ 3 000 lectures) par classe et tissu :

| classe | peau | branchie | midgut | hindgut |
|---|---|---|---|---|
| hotu (Cn) | 48 | 54 | 51 | 46 |
| hybride, les 42 | 28 | 41 | 30 | 36 |
| hybride, intermédiaires seuls | 10 | 20 | 12 | 16 |
| toxostome (Pt) | 69 | 77 | 70 | 75 |

Le plafond du plan équilibré 4H devient **28 / 41 / 30 / 36** avec les 42 hybrides (contre
17 / 30 / 20 / 25 en août), mais retombe à **10 / 20 / 12 / 16** si on restreint aux génomes
intermédiaires. Dans les deux cas on reste au-dessus du plancher de stabilité de 8 établi par les
analyses de sensibilité de Camper et al., mais la peau passe tout juste avec la définition
restrictive.

Puissance du contraste hybrides contre parentaux, effet ×1,3 :

| tissu | Hy = 42 | Hy = 20 |
|---|---|---|
| peau | 0,61 | 0,30 |
| branchie | 0,76 | 0,51 |
| midgut | 0,64 | 0,35 |
| hindgut | 0,70 | 0,43 |

Réserve inchangée : ces puissances utilisent une SD résiduelle de 0,55 estimée sur la richesse ASV
observée, métrique écartée par l'analyse de reproductibilité technique. À recalculer en métrique
pondérée par l'abondance.

Composition par site-année (individus utilisables) : les quatre sites à trois classes restent Ain,
Büech, St-Just et canal ; Avignon reste le seul site sans toxostome ; Baume, Manosque et Pertuis
restent sans hotu. La structure spatiale décrite en août est inchangée.

## 5. Ce qui reste à éclaircir

### Deux anomalies de données

**Cinq individus ont une classe et un index mais aucune Q-value dans `genome_hotox.csv`** :
`2014_Bue_1001`, `2014_Bue_1002` (Cn), `2015_Bue_1014`, `2015_Cab_1011`, `2015_Jus_1008` (Pt). Le
fichier contient 175 lignes pour 180 individus classés. Leurs valeurs de D sont de 0,00 ou 0,01 —
exactement zéro pour quatre d'entre eux, ce qui ne se produit pour aucun des 175 autres. Ces
valeurs semblent héritées de l'analyse à 12 chromosomes sans avoir été recalculées. Les cinq sont
classés parentaux, donc l'impact est faible, mais il faut savoir si leur génotypage a échoué ou
s'ils ont simplement été omis de l'export.

**Pertuis reste sans nom de site ni rivière** dans les métadonnées, et son individu 2015 est
absent du tableau — conforme à la décision de le retirer.

### La décision qui structure tout le reste

**Que veut dire « hybride » dans cet article ?** Trois options, dans l'ordre de ma préférence :

1. **Trois classes, hybride = les 20 génomes intermédiaires ; les 22 quasi-purs rejoignent leur
   parental d'origine.** Défendable biologiquement — un poisson introgressé sur 1 chromosome sur
   25 partage 96 % de son génome avec un parental —, cohérent avec le clustering, et cohérent avec
   la logique du 4H qui exige des classes non chevauchantes. Coût : la peau tombe à 10 individus
   hybrides et la puissance du contraste à 0,30 pour un effet ×1,3.
2. **Quatre classes : hotu, introgressé, hybride intermédiaire, toxostome.** Respecte la réalité
   génomique, et la variable « nombre de chromosomes introgressés » devient un gradient continu
   exploitable. Coût : le 4H n'admet que trois classes, donc il faudrait choisir lesquelles y
   entrent, et l'effectif introgressé penche à 19 contre 3 vers le toxostome, ce qui déséquilibre.
3. **Trois classes, hybride = les 42, comme aujourd'hui.** Maximise la puissance. Coût : la classe
   mélange un F1 putatif et un poisson quasi-pur, ce qu'un relecteur verra dès la figure
   médiane × D — et l'hypothèse « transgressif » perd son sens si 22 des 42 hybrides ont un génome
   parental.

Ma recommandation est l'option 1 pour l'analyse principale, avec l'option 3 en analyse de
sensibilité déclarée. La question à trancher avec André est biologique, pas statistique : un
individu introgressé sur un seul chromosome est-il, pour la question posée, un hybride ?

### Trois décisions dépendantes

- **le périmètre des sites** : la question Manosque / Pertuis est inchangée sur le fond, mais
  Manosque gagne 3 hybrides (de 2 à 5) et Baume 3 (de 4 à 7). Si l'option 1 est retenue, ces gains
  disparaissent puisque ces nouveaux hybrides sont tous des quasi-purs ;
- **la fenêtre d'index du 4H** : elle devient sans objet si les classes sont définies par la règle
  médiane/D plutôt que par un découpage de l'index continu. C'est une simplification à acter ;
- **la structure en stations**, toujours en attente. Les questions transmises à André restent
  ouvertes et conditionnent la possibilité de séparer un effet de classe d'un effet de lieu.

### Ce qui peut avancer sans rien attendre

L'axe tissulaire : 109 individus avec les quatre tissus, aucune classe génotypique requise. Le
test de composition midgut / hindgut et la réplication du gradient externe / interne sur
composition restent la partie du travail qui ne dépend d'aucune de ces décisions.