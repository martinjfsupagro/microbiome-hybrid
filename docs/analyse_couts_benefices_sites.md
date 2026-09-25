# Garder les six populations ou tous les échantillons : analyse coûts-bénéfices

Le débat porte sur l'apport scientifique et la cohérence du plan telle qu'un lecteur la percevra,
pas sur des contraintes de calcul. Les six populations à rôle défini sont canal, Ain, Büech,
St-Just, Baume et Avignon — soit sept site-années puisque Ain, Büech et Avignon sont échantillonnés
sur deux années. Hors liste : Manosque (15 individus) et Pertuis (10).

## Ce que les deux sites apportent, mesuré

| | six populations | tous |
|---|---|---|
| individus | 156 | 181 |
| individus avec les 4 tissus | 90 | 109 |
| individus avec ≥ 3 tissus | 136 | 160 |
| hybrides (Ch) | 108 | 129 |
| hotu (Cn) | 31 | 34 |
| **toxostome (Pt)** | **12** | **12** |
| plafond du plan équilibré 4H | 10 | 10 |
| niveaux du facteur site | 7 | 9 |
| **individus à rôle de population défini** | **156** | **156** |

Trois lectures de ce tableau.

**Le gain est réel sur l'axe tissulaire** : +19 individus avec les quatre tissus, +24 avec au moins
trois. Sur un contraste apparié intra-individu, c'est un gain de puissance direct et sans
contrepartie — ces individus n'ont pas besoin d'un rôle de population pour contribuer à un test
« midgut contre hindgut ».

**Le gain est nul là où le jeu de données est le plus contraint.** Ni Manosque ni Pertuis ne porte
de toxostome. Le plafond du plan équilibré du 4H reste à 10-12 individus par classe et l'ancre
parentale reste à 12 poissons dans les deux scénarios. Les deux analyses les plus fragiles du projet
— contraste parental et indice 4H — sont donc rigoureusement indifférentes à cette décision.

**Le gain est nul, par construction, sur le gradient de rôles.** Le nombre d'individus rattachables
à un rôle de population est de 156 dans les deux cas. Les 25 individus supplémentaires ne peuvent
pas contribuer au test qui structure l'introduction — celui qui oppose allopatrie, sympatrie et
introgression asymétrique — puisqu'ils n'ont pas de rôle assigné. Ils entrent dans le modèle global
comme deux niveaux supplémentaires du facteur site, sans position sur le gradient.

## Le coût de cohérence : ce qu'un lecteur verra

Trois problèmes distincts, d'ampleur très inégale.

**Pertuis 2015 est un site-année à un seul poisson, et à un seul tissu.** L'individu `2015_Per_2015`
n'a que le hindgut séquencé. Une ligne « Pertuis 2015, n = 1 » dans le tableau 1 est un aimant à
commentaire de relecture, et comme niveau d'un facteur aléatoire elle n'estime rien. C'est le seul
élément du jeu de données que je recommande d'écarter sans hésitation, indépendamment de la décision
sur les sites : non pas parce qu'il déséquilibre le plan, mais parce qu'un niveau à une observation
n'est pas interprétable.

**Deux sites sans rôle dans un tableau organisé par rôle.** Si le tableau 1 est structuré par
rôle — c'est le cas dans la note de départ — deux lignes « à statuer » cassent la logique de
présentation. Mais ce coût dépend entièrement du retour d'André : si la discussion leur attribue un
rôle, il disparaît. C'est un coût conditionnel, pas acquis.

**Le déséquilibre de stade de développement, qui est le point important — et il traverse la liste
des six.** Fraction d'individus ≥ 20 cm par site-année, proxy du stade adulte :

| site-année | n | fraction ≥ 20 cm | sexe déterminé | dans les six |
|---|---|---|---|---|
| Ain 2015 (Cab) | 19 | 0,56 | 0,95 | oui |
| Büech 2015 | 18 | 0,56 | 0,89 | oui |
| Avignon 2014 | 11 | 0,55 | 0,55 | oui |
| Avignon 2015 | 13 | 0,54 | 0,54 | oui |
| Ain 2014 | 14 | 0,43 | 0,93 | oui |
| Baume 2015 | 25 | 0,35 | 0,88 | oui |
| Büech 2014 | 17 | 0,27 | 0,12 | oui |
| St-Just 2015 | 19 | 0,26 | 0,47 | oui |
| **canal 2015** | 20 | **0,00** | 0,25 | **oui** |
| Manosque 2014 | 15 | 0,00 | 0,27 | non |
| Pertuis 2014 | 9 | 0,00 | 0,67 | non |
| Pertuis 2015 | 1 | 0,00 | 0,00 | non |

Le canal — l'une des deux références de parapatrie, donc une pièce structurante de
l'argumentation — n'a **aucun individu de plus de 18 cm**, exactement comme les deux sites
contestés. Retirer Manosque et Pertuis au motif qu'ils sont juvéniles laisserait donc le même
problème à l'intérieur du plan, sur un site qu'on ne peut pas retirer sans perdre une référence.

Conséquence sur l'argument : **écarter ces deux sites n'achète pas la cohérence de stade qu'on
croit acheter.** La vraie réponse au problème est un contrôle statistique — la taille en covariable,
déjà prévue au modèle — et sa déclaration explicite en Methods, pas une sélection de sites.

## Recommandation

**Garder tous les échantillons, écarter le seul individu de Pertuis 2015, et traiter le rôle de
population comme une covariable à valeur manquante plutôt que comme un critère d'inclusion.**

Trois raisons.

1. Les 24 individus restants apportent un gain net et sans contrepartie sur l'axe tissulaire, qui
   est l'ossature de l'article. Aucun test prévu n'est dégradé par leur présence.
2. Le coût de cohérence redouté est en grande partie déjà dans le plan : le canal a le même profil
   juvénile. Le retrait ne règle pas le problème, il le cache en le laissant à l'intérieur.
3. Retirer des échantillons exploitables sans justification autre que la présentation est
   exactement ce qu'un relecteur demandera de justifier. Il est plus facile de défendre « nous
   avons analysé tous les individus disponibles, avec le rôle de population en covariable et la
   taille en contrôle » que « nous avons écarté 25 poissons séquencés parce qu'ils n'entraient pas
   dans notre typologie ».

### Comment le présenter sans incohérence apparente

- **tableau 1 organisé par rôle**, avec les sites sans rôle assigné en dernière section clairement
  étiquetée, et non intercalés ;
- **analyse principale sur les 181 individus**, index hybride en effet fixe, site-année et individu
  en effets aléatoires, taille et profondeur en covariables ;
- **analyse du gradient de rôles restreinte aux 156**, déclarée comme telle. C'est un
  sous-ensemble annoncé, pas une exclusion : les deux analyses répondent à deux questions
  différentes ;
- **une analyse de sensibilité « six populations seulement »** rapportée en supplément pour les
  résultats principaux. Elle coûte une table et retire l'argument à un relecteur.

### Le cas où je changerais d'avis

Si le génotypage révèle que Manosque ou Pertuis contient des index intermédiaires **incompatibles**
avec les sites voisins de la même rivière — par exemple des hybrides là où la barrière l'interdit —
alors ces sites posent un problème d'interprétation et non de présentation, et il faut les écarter.
C'est la seule information attendue qui puisse renverser la recommandation, et elle arrive avec le
retour d'André.

Réserve de métrique : les effectifs et couvertures tissulaires ci-dessus sont robustes, mais les
comparaisons de puissance de mes notes antérieures reposent sur la richesse ASV observée, métrique
écartée par l'analyse de reproductibilité technique. Elles seront à recalculer en métrique pondérée.