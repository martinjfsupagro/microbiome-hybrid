# Recommandations consolidées — projet microbiome hybride

Synthèse au 23 août 2026, après lecture du cadre conceptuel de Camper et al. 2024 et de son
matériel supplémentaire, du préprint Guivier et al. 2017, et diagnostic sur les données disponibles.
Les valeurs citées sont calculées sur les fichiers du projet ou extraites des articles, jamais
de mémoire.

## En une phrase

L'article devrait s'articuler sur le **gradient tissulaire** — le seul facteur fortement
structurant, apparié intra-individu et bien répliqué — avec l'hybridation testée à l'intérieur de
cette ossature par un modèle global multi-sites, et l'indice 4H comme analyse secondaire dont les
paramètres sont figés maintenant et la sensibilité publiée dans le corps de l'article.

## 1. Ce qui peut démarrer aujourd'hui, sans attendre André

L'axe tissulaire ne dépend d'aucun génotype : 109 individus ont les quatre tissus exploitables,
160 en ont au moins trois. Deux analyses sont prêtes :

- **le test de composition midgut / hindgut** (PERMANOVA sur distances UniFrac ou Bray-Curtis).
  C'est le seul test comparable terme à terme à l'absence de différenciation rapportée en 2017.
  Le contraste de richesse est déjà fait — ratio 0,83 sur 134 individus appariés — mais il porte
  sur la richesse observée, métrique écartée par l'analyse de reproductibilité technique ;
- **la réplication du gradient externe / interne sur composition**, et non seulement sur richesse.

Ces analyses relèvent du profil d'analyse de données, pas de la recherche bibliographique.

**Priorité absolue avant tout le reste : refaire en métrique pondérée par l'abondance.** Tous les
résultats que j'ai produits — contraste midgut/hindgut, gradient externe/interne, dimorphisme
sexuel, partition de variance, et l'intégralité des calculs de puissance — portent sur la richesse
ASV observée. L'analyse de reproductibilité technique menée en parallèle établit qu'un
re-séquençage de la même librairie ne retrouve que 48 % des ASV présents à 1-3 lectures : la
richesse observée est peu reproductible et le manuscrit fonde ses analyses de diversité sur des
métriques pondérées. Mes chiffres gardent leur valeur de diagnostic de faisabilité ; **aucun ne doit
entrer dans les Results tel quel**. En particulier les SD résiduelles (0,44 en peau à 0,76 en
midgut) qui fondent tous les seuils d'effectif annoncés ci-dessous : ils se déplaceront.

## 2. Paramètres du 4H à figer par écrit maintenant

La raison de les figer maintenant est que le matériel supplémentaire révèle un risque de
circularité. Chez le lézard *Aspidoscelis* — le système publié le plus proche du nôtre, hybride
naturel — l'axe transgressif passe de 0,467 à ρ = 0,1 à 0,911 à ρ = 0,8. « Transgressif » étant
l'hypothèse d'intérêt du projet, **un ρ élevé la favorise mécaniquement**. Choisir ρ après avoir vu
le résultat serait indéfendable ; l'invoquer au nom de la recommandation des auteurs le serait
aussi.

| paramètre | décision | justification |
|---|---|---|
| ρ principal | **0,5** | échelle des figures publiées, donc comparabilité externe ; c'est aussi le point où les deux axes s'équilibrent chez le lézard (0,500 / 0,500) |
| gamme de ρ rapportée | **0,1 à 0,7, dans le corps de l'article** | amplitude de 0,52 sur l'axe parental chez le lézard : reléguer cette gamme en annexe dissimulerait la fragilité du résultat |
| ρ ≥ 0,8 | **écarté d'emblée** | la dimension Intersection s'y annule exactement (0,000) : l'indice devient dégénéré |
| ϑ et ε | **0 (défauts du package)** | ne pas cumuler trois seuils arbitraires |
| échelle taxonomique | **genre**, famille en sensibilité | échelle des figures publiées ; à confirmer après mesure du taux d'assignation des ASV au genre |
| échelle ASV | **écartée** | axe parental à 0,117 et Intersection à 0,000 chez le lézard : aucun ASV n'est partagé par les cores des trois classes |
| classes d'index | parental si index < 0,1 ou > 0,9 | seuils symétriques a priori, indépendants des données |
| critère de subdivision de la classe hybride | **`FourHpreanalysis`** | la fonction avertit si le core des hybrides tombe sous 25 % de celui des parentaux et suggère de subdiviser : critère quantitatif calculable avant de voir l'indice |
| critère d'abandon du 4H | une classe sous 10 individus | ordre de grandeur des systèmes publiés (7 pour rat, lézard, cigale ; 10 pour maïs) |

Séquence à écrire en Methods, dans cet ordre : constituer les trois classes, lancer
`FourHpreanalysis`, rapporter les trois fractions de core, subdiviser si l'avertissement se
déclenche selon le degré de backcross, et seulement ensuite calculer l'indice.

## 3. Ce qui n'est plus une contrainte

Deux inquiétudes que j'avais formulées sont levées par le matériel supplémentaire :

**L'effectif ne bloque pas le 4H.** De 4 à 16 hôtes par classe, l'axe parental ne varie que de
0,114 chez le lézard, et la courbe est plate au-delà de 8 (0,472 à N = 8 ; 0,475 à N = 10 ; 0,489 à
N = 12). Notre plafond actuel — 12 en peau, 11 en branchie, 10 en midgut, 11 en hindgut — est dans
la zone stable. Le reclassement des « Ch » améliorera la précision des bootstraps sans déplacer
l'indice : l'analyse 4H attend le génotypage pour savoir qui est dans quelle classe, pas pour être
faisable.

**La profondeur de séquençage ne bloque rien.** De 1 000 à 10 000 lectures, l'axe parental varie de
0,067. La raréfaction à 3 000 est confortable pour le 4H — les sites pénalisés par la raréfaction
(canal en peau et midgut) le sont donc bien moins pour cette analyse que pour une analyse de
diversité.

## 4. Ce qui reste réellement bloqué, et pourquoi

Le cadrage de l'introduction : ordre des hypothèses, décision d'annoncer les deux analyses ou de
réserver le 4H à la discussion, formulation de la phrase de nouveauté. Tout cela dépend de deux
informations attendues d'André :

1. **la distribution de l'index**, globale et par site — pas seulement les valeurs. C'est elle qui
   décide si une monotonie est testable sur tout l'axe ou seulement sur sa moitié basse, et si les
   classes du 4H sont peuplées. Demander aussi la **précision** de l'index, qui fixe la largeur
   défendable de la fenêtre ;
2. **la nature de la barrière** pour chacun des trois sites concernés (barrage, canal, distance),
   pour justifier en Methods leur statut de contrôle négatif.

## 5. Positionnement de l'article — révisé

**À retirer** : le quatrième compartiment tissulaire comme élément de nouveauté. Guivier 2017
séparait déjà midgut et hindgut ; le résumé disait « gut », le texte dit autrement.

**À conserver** : l'index hybride continu, l'effectif (181 poissons sur 9 sites-années contre 16 sur
2 sites), et le fait que l'article répond à la question que 2017 posait explicitement en
conclusion. Le cadrage le plus économique est « la suite annoncée de 2017 ».

**À ajouter** : les sites à barrière physique sont un **contrôle négatif interne** — populations en
contact géographique sans flux de gènes, réplicable sur deux rivières. C'est un témoin qui manque à
la plupart des études de zones d'hybridation. Et ne plus écrire « allopatrie » : le terme juste est
parapatrie à isolement physique.

## 6. Trois précautions de rédaction

**Ne pas lier transgression et coût de fitness.** Un article de *Microbiome* 2025 attaque ce
consensus : les conclusions négatives reposent sur des hybrides de faible fitness, et étudier des
hybrides en cul-de-sac garantit de trouver que l'hybridation est délétère. Le toxostome étant
patrimonial et en régression, la tentation sera forte. L'axe Gain-Loss du 4H fournit une définition
opérationnelle de « transgressif » qui ne présuppose aucun coût.

**Contrôler l'autocorrélation spatiale d'emblée.** Chez la souris domestique, sur deux réplicats de
la même zone d'hybridation, l'effet d'admixture devient négligeable dès qu'on en tient compte
(*Molecular Ecology* 2023). Site, rivière, année et rôle sont confondus dans ce plan : à anticiper
dans le modèle, pas à découvrir en review.

**Reprendre la déclaration de portée des auteurs du 4H.** Ils écrivent que l'indice est une mesure
de motif et non de processus, à l'image de la diversité bêta, et qu'il ne devrait pas servir à
discriminer entre mécanismes de réassemblage. C'est la prudence que la revue critique de
l'introduction d'origine réclamait.

## 7. Deux points de nettoyage à ne pas oublier

- `14Avi1036-Cn03A` et `14Avi1037-01A` portent un tiret à la place du code espèce. Sans correction,
  ces deux poissons d'Avignon décrocheront silencieusement de l'appariement génotype ↔ microbiote —
  et Avignon est l'un des deux seuls sites à porter les deux parentaux.
- Le préprint 2017 mentionne un financement EDF via le projet FACIES et l'appui de la Fédération de
  l'Ain. Si l'échantillonnage 2014-2015 relève du même projet, cela doit figurer dans les
  remerciements.

## 8. À vérifier dès réception, dans cet ordre

1. la prédiction posée : les 19 « Ch » d'Ain 2015 devraient se classer en 9 toxostomes (17-22 cm) et
   9 hotus (40-50 cm), index à 0 ou 1, aucun intermédiaire. Si elle échoue, soit la barrière est
   perméable, soit l'index a un problème de calibration ;
2. le taux d'assignation des ASV au genre, qui valide ou invalide le choix d'échelle ;
3. le confondant taille-espèce : il vaut r = -0,89 à Ain sur les seuls individus génotypés
   aujourd'hui, et le reclassement des « Ch » peut le lever. À réévaluer, pas à traiter comme acquis ;
4. l'effectif parental par site : 20 individus par espèce est le seuil sous lequel le contraste
   intra-site ne détecte qu'un doublement de richesse (puissance 0,62 à n = 20 contre 0,21
   aujourd'hui, pour un effet ×1,5 — valeurs à recalculer en métrique pondérée).
## 9. Scénarios de retrait de sites — chiffré d'avance

En attente de la décision sur Pertuis et Manosque. Effet mesuré sur les données actuelles :

| scénario | individus | sites | 4 tissus | ≥ 3 tissus | Cn | Pt | Ch | plafond 4H (caudale/branchie/midgut/hindgut) |
|---|---|---|---|---|---|---|---|---|
| tous les sites | 181 | 9 | 109 | 160 | 34 | 12 | 129 | 12 / 11 / 10 / 11 |
| sans Pertuis | 171 | 8 | 101 | 151 | 34 | 12 | 120 | 12 / 11 / 10 / 11 |
| sans Manosque | 166 | 8 | 98 | 145 | 31 | 12 | 117 | 12 / 11 / 10 / 11 |
| sans les deux | 156 | 7 | 90 | 136 | 31 | 12 | 108 | 12 / 11 / 10 / 11 |

Deux conclusions.

**Le plafond du plan équilibré 4H est insensible au retrait.** Il est fixé par le toxostome, et ni
Pertuis ni Manosque n'en porte : 12 / 11 / 10 / 11 dans les quatre scénarios. Combiné à la zone de
stabilité de l'indice au-delà de 8 hôtes par classe, l'analyse 4H est indifférente à cette décision.

**L'axe tissulaire absorbe le retrait sans dommage.** Au pire — les deux sites écartés — il reste 90
individus avec les quatre tissus et 136 avec au moins trois. Le contraste apparié reste largement
mieux réplique que tout contraste inter-groupes du jeu de données.

La décision est donc à prendre sur des motifs de cohérence du plan (statut des populations,
comparabilité des sites), pas sur un argument de puissance : aucun des deux scénarios ne met en péril
une analyse prévue. Manosque coûte trois individus hotu, seul effet à surveiller puisque les
parentaux sont la ressource rare.

**Une case de métadonnées à remplir au passage.** Dans `index_hybride_andre.csv`, le site `Per` a
`site_nom` et `riviere` vides. Votre message le nomme Pertuis ; la rivière reste à faire confirmer
par André plutôt qu'à déduire. À renseigner avec le retour, quelle que soit la décision de conserver
le site ou non — un site écarté doit quand même être décrit dans le supplément.
