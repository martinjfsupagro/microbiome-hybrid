# Réponses d'André du 2026-10-03 — questions en suspens, section 1

Source : réponses d'André transmises par JF le 2026-10-03, en retour de
`docs/questions_en_suspens_2026-10-03.docx` (commit `fe8df21`). Les réponses sont recopiées
**mot pour mot** ci-dessous, puis confrontées aux fichiers du projet. Aucune modification
d'`Article.docx` n'est faite à ce stade.

Fichiers relus pour les contrôles : `metadata/station_reference.csv`,
`metadata/analysis_metadata.csv`, `metadata/samples_all.csv`, `docs/manuscrit/Article.docx`
(identique à `HEAD`), Guivier et al. (2017), *Microbial Ecology*, doi:10.1007/s00248-017-1077-9
(version HAL hal-02270253).

## Synthèse

| Q | Objet | Statut | Reste à obtenir |
|---|---|---|---|
| 1.1 | Autorisations | **Partiellement clos** | DDT de l'Ain et de l'Ardèche ; euthanasie |
| 1.2 | Dissection, tissu 01, conservation | **Clos**, une précision | Température des tubes éthanol |
| 1.3 | Extraction, librairies | **Clos** | — |
| 1.4 | Témoins ; fuite de mock | **Clos** (témoins) ; **non récupérable** (fuite) | — |
| 1.5 | Délai, ordre de prélèvement | **Clos** | — (conséquences analytiques, voir plus bas) |
| 1.6 | Financement | **Clos** sur l'organisme ; référence du contrat absente | Décision JF : citer sans numéro ? |
| 1.7 | Remerciements | **Reporté** (« on verra à la fin ») | — |

## 1.1 — Autorisations

> « oui l'autorisation est valable pour l'ensemble des site et des années 2014 et 2015 L'ensemble
> de l' échantillonnage ainsi que les méthodes expérimentales ont été approuvées par les agences
> locales de régulation et de contrôle l'ONEMA (Office national de l'eau et des milieux aquatiques),
> la DDT (Direction départementale des Territoires) des Alpes-de-Haute-Provence, Hautes-Alpes et
> Vaucluse, avec les numéros d'autorisations 2014-156-0001 and 2015-1426DDT605. »

**Concordance.** Les deux numéros sont ceux que le §1 d'`Article.docx` porte déjà. Ce n'est
qu'une confirmation partielle : le texte transposé et la réponse peuvent provenir de la même
source.

**Écart à lever.** D'après `station_reference.csv`, quatre des neuf stations sont hors des trois
départements cités. Pont-d'Ain et Chavannes-sur-Suran (Suran, 2014 et 2015, 33 individus) sont dans
l'**Ain** ; Saint-Just-d'Ardèche et Rosières (2015, 44 individus) sont en **Ardèche**. Ces
départements sont déduits des noms de commune ; ils n'ont pas été vérifiés par géocodage. Avignon
et Pertuis sont sur la Durance, qui sépare le Vaucluse des Bouches-du-Rhône : si la pêche a eu lieu
en rive gauche, le département serait différent.
Soit une autorisation des DDT de l'Ain et de l'Ardèche existe, soit la phrase « valable pour
l'ensemble des sites » repose sur un cadre que la réponse ne nomme pas. Le texte actuel parle
de *national protocol authorisations*, ce qui ne correspond pas non plus à des arrêtés départementaux.

**Non couvert par la réponse.** Le mode d'euthanasie (dislocation cervicale, dans le texte
transposé) n'est ni confirmé ni infirmé.

## 1.2 — Dissection, tissu 01, conservation

> « Oui j'ai suivi le même protocole pour la dissection le tissu 01 c'est un lobe de la nageoire
> caudale il y a aussi la branchie et le mid et hindgut, apres dissection tous les tissus sont coupes
> en deux et places dans deux eppendorf 1,5 ml conservation en éthanol 95 % pour le microbiome et
> aussi −80 °C pour des analyse de transciptome et de genotypage transcriptomique. »

**Clos : le tissu 01 est un lobe de la nageoire caudale.** Le drapeau `[À CONFIRMER]` de
`PROJET.md` (« peau ») est levé. `Article.docx` n'emploie pas « skin » (0 occurrence) ; seules des
notes internes (`decision_mock_removal.md`, `decisions_a_prendre.md`, `point_etape_25sept.md`)
écrivent « peau ».

**Information nouvelle.** Chaque tissu est coupé en deux tubes : une moitié en éthanol 95 % pour le
microbiote, l'autre à −80 °C pour le transcriptome et le génotypage.

**Précision à demander.** Le texte actuel, repris mot pour mot de Guivier et al. (2017), dit
*stored in 95% ethanol at −80 °C*. La réponse ne dit pas si le tube en éthanol est lui-même stocké à
−80 °C, ou si seule la seconde moitié l'est.

## 1.3 — Extraction et librairies

> « c'est le meme protocole que dans l'article de guivier pas de modification. »

**Clos.** Le §3 d'`Article.docx` est conforme à Guivier et al. (2017) sur le kit (Qiagen Food
Mericon modifié), l'indexation (Kozich 2013 selon Galan 2016) et la quantification (Kapa). La chimie
reste celle des fiches de run (v3 600 cycles en 2 × 251), et non le « 2 × 300 cycles » de Guivier.

**Défaut éditorial relevé en passant.** `Article.docx` cite « Guivier et al. (2017) » trois fois et
« Guivier et al. (2018) » une fois (§3). La bibliographie porte 2017 (en ligne 2017, volume 2018).
Il faut harmoniser l'année selon le style de la revue.

## 1.4 — Témoins et fuite de mock

> « on a utilise des blancs d'extraction , blancs de PCR, puits vides on doit les retouver dans les
> plaque normalement. »
> « Je ne sais pas je n'ai pas fait les manips complique de le dire et ca ne se voit pas sur le
> cahier de manip. »

**Clos, vérifié dans les plaques** (`samples_all.csv`, colonne `sample_type`) :

- 4 `blank` nommés par tissu (`Blanc-Caudal`, `Blanc-Branchie`, `Blanc-Midgut`, `Blanc-Hindgut`) ;
- 8 `temoin` (`T-1` à `T-8`, un par plaque) ;
- 25 `empty` ;
- 2 `mock`.

Chaque contrôle est séquencé dans les trois runs, ce qui donne 12, 24, 75 et 6 lignes. Le §4
d'`Article.docx` décrit déjà exactement cette composition. On y lit les `Blanc-*` comme des blancs
d'extraction et les `T-*` comme des blancs de PCR ; cette lecture vient des noms et de la position
dans les plaques, et elle est cohérente avec la réponse. La note grise du §4 peut être retirée.

**Fuite de mock : origine non récupérable.** L'information n'existe pas dans le cahier de
manipulation. Le texte s'en tiendra à ce qui est mesuré : 20 échantillons concernés, retrait des
ASV du mock, drapeau de sévérité (`decision_mock_removal.md`). Aucune cause ne sera avancée.

## 1.5 — Délai et ordre de prélèvement

> « les poissons sont garde dans un grand vivier dans l'eau de la riviere pour ne pas perturbé.la
> dissection d'un poisson dure 4 à 6 minutes je commence par caudale puis branchie et enfin le hind
> et midgut donc pour tous les poissons ca dure deux heures. (la peche electrique ca va de 30 minute
> à 1 heure). »

**Contrôle de cohérence.** Les effectifs retenus par jour de pêche vont de 4 à 25 poissons. Le
maximum est à Rosières, avec 25 poissons le 22/07/2015 ; le Buëch et Avignon se répartissent sur
deux années (17/18 et 11/13). À 4–6 min par poisson, une session de 25 poissons dure de 1 h 40 à
2 h 30, ce qui est cohérent avec « deux heures ». Le désaccord était possible : 35 poissons du Buëch
en une seule session auraient demandé jusqu'à 3 h 30. Réserve : seuls les poissons retenus sont
comptés. Les chevesnes intercalés à l'Ain et à Avignon en 2014 ont pu allonger les sessions.

**Contradiction avec le texte actuel.** Le §1 écrit *euthanised by cervical dislocation, and
immediately dissected*. Selon André, les poissons sont gardés vivants en vivier jusqu'à leur
dissection, soit jusqu'à environ 2 h 30 après la fin de la pêche pour le dernier. La séquence
réelle est : pêche (30–60 min), vivier, puis euthanasie et dissection poisson par poisson.

**Conséquences analytiques — hypothèses, non testées.**

1. *L'intervalle post-mortem est court et constant.* Chaque poisson est disséqué en 4–6 min dans le
   même ordre (caudale, branchie, hindgut, midgut). Le délai post-mortem ne dépend donc pas de la
   catégorie. La lecture « dégradation post-mortem des communautés digestives », sur laquelle
   reposait la prédiction de `point_etape_25sept.md`, est écartée **par construction du protocole**
   et non par un test.
2. *Ce qui reste confondu avec la catégorie, c'est la durée de séjour en vivier* : de quelques
   minutes à environ 2 h 30, les hotus étant disséqués en premier. On ne sait pas sur quel
   compartiment un tel séjour (stress, jeûne, eau du vivier) agirait en premier. La prédiction
   « digestif contre externe » ne discrimine donc plus proprement délai et température.
3. *L'effet de position pourrait en partie être un effet de séjour.* À cinq stations sur neuf, la
   colonne de plaque suit l'ordre de prélèvement (ρ de Spearman de 0,87 à 0,95,
   `point_etape_25sept.md`). L'effet de position (R14, R² 0,18–0,40) ne s'y distingue pas d'un
   effet de durée en vivier. **Témoin possible** : les quatre stations où colonne et ordre se
   découplent (Chavannes ρ = 0,008, Pont-d'Ain 0,17, Avignon 0,37, Buëch 0,39). On y comparerait un
   modèle avec la colonne et un modèle avec le rang de dissection. Tant que ce test n'est pas fait,
   c'est une hypothèse.

## 1.6 — Financement

> « Electricité de France financement de la these Arnaud UNGARO, Fédération de l'Ain pour la pêche
> et la protection des milieux aquatiques. »

**Clos sur l'organisme.** EDF finance la thèse d'Arnaud Ungaro. L'intitulé de la Fédération est
celui de Guivier et al. (2017). Le texte actuel (*EDF via le projet FACIES*) est à reformuler. Les
deux formulations ne se contredisent pas : Guivier écrit *within the project FACIES*.
**Aucune référence de contrat n'est fournie** : à JF de décider si l'on cite sans numéro.

## 1.7 — Remerciements

> « on verra à la fin »

Reporté à la finalisation du manuscrit.

## Questions de suivi pour André (trois, courtes)

1. Les stations du Suran (Pont-d'Ain, Chavannes-sur-Suran, département de l'Ain) et de l'Ardèche
   (Saint-Just-d'Ardèche, Rosières) étaient-elles couvertes par une autorisation des DDT de l'Ain et
   de l'Ardèche ? Si oui, sous quels numéros ? Sinon, quel cadre les couvrait ?
2. L'euthanasie se faisait-elle par dislocation cervicale, juste avant la dissection de chaque poisson ?
3. Le tube en éthanol 95 % destiné au microbiote était-il conservé à −80 °C (comme dans Guivier et al.
   2017), ou à une autre température ?

## Ce que ces réponses permettent de modifier dans `Article.docx` (non fait)

- §1 : décrire la séquence pêche → vivier → euthanasie → dissection, avec les durées. Remplacer
  *national protocol authorisations* par l'ONEMA et les DDT (une fois la question de suivi 1 réglée).
- §2 : lobe de nageoire caudale ; ordre de dissection ; tissu coupé en deux tubes ; retirer la note grise.
- §3 et §4 : retirer les notes grises (confirmés par André).
- §8 ou la discussion : la durée de séjour en vivier devient le confondant à nommer, à la place du
  délai post-mortem.
- *Funding* : EDF, financement de thèse d'A. Ungaro ; Fédération de l'Ain pour la pêche et la
  protection des milieux aquatiques.
- Harmoniser l'année de Guivier et al.
