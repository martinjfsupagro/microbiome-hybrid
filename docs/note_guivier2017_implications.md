# Ce que le texte intégral de Guivier et al. 2017 change

Préprint fourni par l'utilisateur (version Microbial Ecology, doi 10.1007/s00248-017-1077-9).
Je n'avais lu que le résumé, récupéré via HAL. Le texte contient plusieurs éléments absents du
résumé et directement structurants pour l'article en cours.

## Correction : ce n'était pas « le gut », c'étaient déjà midgut et hindgut séparés

Le résumé annonce « skin, gills and gut ». Le texte précise que le tube digestif a été séparé en
**midgut et hindgut** — soit exactement les quatre compartiments du jeu de données actuel
(nageoire caudale, branchie, midgut, hindgut). La nouveauté du présent article n'est donc **pas**
le quatrième compartiment : il faut retirer cet argument du positionnement.

La nouveauté défendable se réduit à deux éléments, mais ils restent solides :
l'**index hybride continu** sur des individus de zone d'hybridation, et l'**effectif** — 181 poissons
sur 9 sites-années contre 16 poissons sur 2 sites, en allopatrie stricte.

## Le plan de 2017 était minuscule et volontairement sans hybrides

Seize poissons : 8 P. toxostoma en amont (Chavasnes-sur-Suran) et 8 C. nasus en aval (Pont d'Ain),
séparés par 30 km et une succession de barrages limitant fortement le contact et donc
l'hybridation, échantillonnés en août 2015 sur la rivière **Suran** — pas la Durance ni l'Ardèche.
Plan équilibré en sexe (4 mâles, 4 femelles par espèce). Les auteurs concluent en annonçant
explicitement que la suite consistera à explorer le réarrangement du microbiote chez les hybrides.
**L'article en cours est la suite annoncée de 2017** : c'est le cadrage le plus économique pour
l'introduction.

## Continuité méthodologique forte, avec deux différences à déclarer

Identique : fragment de 251 pb de la région V4 du 16S, méthode dual-index de Kozich adaptée
d'après Galan ; MiSeq ; mock ZymoBIOMICS ; contrôles négatifs d'extraction et d'amplification ;
duplication de l'amplification par échantillon.

Différent, et à assumer en Methods :

| | Guivier 2017 | article en cours |
|---|---|---|
| Unités | OTU 97 % (Mothur, 11 332 OTU) | ASV (DADA2, 44 200) |
| Référence taxonomique | Silva v123 | Silva v138.2 |
| Raréfaction | 34 000 lectures, 1 000 tirages | 3 000 lectures |
| Profondeur moyenne | 65 415 lectures/échantillon | médiane 10 129 |

L'écart de profondeur est d'un ordre de grandeur. Le passage OTU→ASV et Silva v123→v138.2 est
une amélioration défendable, mais il empêche toute comparaison directe des décomptes de taxons
entre les deux articles : à dire une fois, explicitement.

Un détail de méthode à reprendre : ils raréfient **1 000 fois** et prennent la moyenne des indices
sur les 1 000 tables, plutôt qu'un tirage unique. C'est plus robuste que ce que le plan actuel
prévoit et coûte peu.

## Trois résultats de 2017 testables sur les données actuelles — et deux se comportent différemment

### 1. Midgut et hindgut ne se distinguaient pas. Ici, ils se distinguent.

En 2017 : « nous n'avons détecté aucune différenciation entre les microbiotes associés aux deux
parties de l'intestin, quelle que soit l'espèce », ni en composition (PERMANOVA p>0,05), ni en
abondance de phyla. Les auteurs en concluaient une composition constante sur la longueur du tube.

Test apparié sur les 134 individus ayant les deux compartiments exploitables (richesse ASV, moyenne
sur les runs) : le midgut porte **0,83 fois** la richesse du hindgut (IC95 0,73–0,95 ; t=-2,83,
p=0,005). L'écart est modeste mais significatif. À titre de comparaison, les autres contrastes
appariés vont de 1,44 à 2,46 avec des p entre 1e-6 et 2e-19 : midgut/hindgut reste de loin le
contraste le plus faible des six, ce qui est cohérent avec l'absence de détection sur 16 poissons.

Lecture : ce n'est pas une contradiction mais un gain de puissance — 134 individus appariés contre
16. La conclusion à écrire est que les deux compartiments intestinaux sont proches mais non
interchangeables, et qu'il ne faut donc pas les fusionner en un « gut » comme le permettait 2017.
**Réserve de métrique** : 2017 teste Shannon, PD et la composition ; ce test porte sur la richesse
ASV observée. Le test sur composition (PERMANOVA sur UniFrac) reste à faire pour une comparaison
terme à terme — c'est lui qui trancherait vraiment.

### 2. Le gradient externe/interne se réplique, et fortement.

En 2017, la différenciation externe (caudale, branchie) / interne (midgut, hindgut) était le
résultat principal, avec le tissu comme premier facteur explicatif (R² de 0,11 à 0,22 selon la
métrique). Ici, les tissus externes portent 1,8 fois la richesse des internes (coefficient 0,598
sur log-richesse, z=8,7) et le tissu explique 18,7 % de la variance. Réplication franche, sur des
rivières, des années et une pipeline différentes. C'est l'argument le plus solide de l'article.

### 3. Le dimorphisme sexuel s'inverse — et c'est peut-être un artefact.

En 2017 : le dimorphisme sexuel était **plus marqué sur les tissus externes**, plus diverses chez
les femelles, tandis que le microbiote intestinal était similaire entre sexes. Les auteurs
l'interprétaient par le statut hormonal.

Ici, le motif est inversé : l'interaction tissu×sexe est significative (z=3,21, p=0,001) mais le
dimorphisme est plus fort en **interne** (ratio femelles/mâles 1,52) qu'en externe (1,17). Par
tissu : hindgut 1,55 (p=0,006), midgut 1,66 (p=0,030), branchie 1,27 (p=0,048), caudale 1,17
(p=0,283). L'effet survit à l'ajout de la taille en covariable (sexe z=-3,58 ; taille p=0,031).

**Ne pas rapporter ce résultat sans son biais.** Le sexe n'est déterminé que pour 108 individus sur
181, et les 73 indéterminés sont nettement plus petits (taille moyenne 14,2 cm contre 22,6 pour les
mâles et 23,9 pour les femelles). Ce sont probablement des juvéniles : le manquant n'est pas
aléatoire et l'analyse porte sur les adultes seuls. Avec 31 femelles contre 77 mâles, et une
métrique différente de 2017, une inversion de motif n'est pas interprétable en l'état. À traiter en
covariable de contrôle, pas en résultat.

## Un résultat de 2017 qui donne une hypothèse dirigée

Les proportions d'OTU spécifiques par tissu étaient asymétriques entre espèces : C. nasus portait
beaucoup d'OTU spécifiques sur les tissus externes (59 % en caudale, 46 % en branchie), tandis que
P. toxostoma en portait beaucoup dans l'intestin (56 % en midgut, 58 % en hindgut). La part d'OTU
communs aux deux espèces était stable, 23 à 27 % selon le tissu.

Et les microbiotes core par tissu étaient de tailles très inégales : chez P. toxostoma, 11 phyla en
caudale contre 17 en hindgut ; chez C. nasus, 14 en caudale contre 6 en midgut. Les auteurs en
tirent explicitement l'hypothèse d'un « impact différent de l'hybridation introgressive sur le
microbiote selon le tissu considéré ».

C'est une hypothèse dirigée et citable pour la question secondaire 1 du projet : l'effet de
l'hybridation devrait être plus marqué là où les parentaux divergent le plus, donc dans l'intestin
plutôt que sur la peau. Cela contredit l'intuition inverse (peau plus déterminée par
l'environnement) que la note de démarrage formulait comme alternative — les deux directions sont
désormais argumentables, ce qui est préférable à une seule.

## Conséquence sur le positionnement

À retirer : le quatrième compartiment tissulaire comme élément de nouveauté.

À conserver et renforcer : l'index hybride continu, l'effectif (181 vs 16), la couverture de la zone
d'hybridation (9 sites-années contre 2 sites allopatriques), et le fait que l'article répond à la
question que 2017 posait en conclusion sans pouvoir y répondre.

Un point à vérifier auprès d'André avant de rédiger : le préprint mentionne un financement EDF via
le projet FACIES et l'appui de la Fédération de l'Ain. Si l'échantillonnage 2014-2015 du présent
jeu relève du même projet, cela doit apparaître dans les remerciements et la déclaration de
financement.