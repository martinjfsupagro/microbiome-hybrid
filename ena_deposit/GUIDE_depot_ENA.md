# Dépôt des données brutes Durance sur l'ENA — guide pas à pas

Projet *microbiome-hybrid* — 16S V4, trois runs de séquençage (durance1, durance2, durance3).
Document rédigé pour un premier dépôt : chaque étape est explicitée.

---

## 1. Ce qui va être déposé

| Objet ENA | Nombre | Correspondance dans le projet |
|---|---|---|
| **study** (BioProject) | 1 | le jeu de données Durance dans son ensemble |
| **sample** | 768 | les 768 librairies (une par tissu × individu, plus les contrôles) |
| **experiment** | 2 304 | une librairie × un run de séquençage |
| **run** | 2 304 | la paire de fichiers R1/R2 correspondante |
| fichiers fastq.gz | 4 608 | 11,7 Go au total |

**Pourquoi 768 samples et non 2 304 ?** Un *sample* ENA désigne la matière biologique.
Vos trois runs sont des réplicats **techniques** : c'est le même ADN, la même librairie,
repassé trois fois sur le séquenceur. Le matériel est donc unique, et c'est ce que dit
le modèle ENA — un sample, trois experiments, trois runs. C'est exactement la structure
qui permettra à un lecteur de retrouver vos triplicats et d'estimer l'effet run.

Détail des 768 samples : 727 échantillons biologiques, 4 blancs d'extraction, 8 témoins PCR
sans matrice, 4 mocks ZymoBIOMICS et 25 puits vides (témoins d'index hopping).

---

## 2. Créer le compte Webin (à faire en premier)

Webin est le portail de soumission de l'EBI. Le compte est gratuit.

1. Ouvrir <https://www.ebi.ac.uk/ena/submit/webin/> puis « Register ».
2. Renseigner le laboratoire et l'adresse institutionnelle. Le champ *center name*
   deviendra le nom du centre soumettant affiché publiquement : mettez le nom
   de l'unité, pas votre nom personnel.
3. L'identifiant reçu a la forme `Webin-XXXXX`. C'est lui qui sera demandé par les scripts.

**Conseil pratique :** demandez d'abord à vos collègues si l'unité dispose déjà d'un
compte Webin partagé. Un compte d'unité évite que les données deviennent inaccessibles
au départ d'une personne — l'EBI ne transfère pas facilement la propriété d'une soumission.

---

## 3. Métadonnées de sites — RÉSOLU

Les coordonnées des 9 sites ont été fournies par André et intégrées
(`ENA_sites_completes.csv`). La soumission est en **checklist ERC000013
(GSC MIxS host associated)**, le standard de la communauté microbiome.

| Site | Commune | Latitude | Longitude | Rivière | Années |
|---|---|---|---|---|---|
| Ain | Villieu-Loyes-Mollon | 45.906458 | 5.233251 | Ain | 2014 |
| Cab | Villieu-Loyes-Mollon | 45.906458 | 5.233251 | Ain | 2015 |
| Avi | Avignon | 43.912848 | 4.817756 | Durance | 2014, 2015 |
| Bau | Sanilhac | 44.523904 | 4.196789 | Ardèche | 2015 |
| Bue | Laragne-Montéglin | 44.308322 | 5.823657 | Durance | 2014, 2015 |
| Caa | Le Puy-Sainte-Réparade | 43.660840 | 5.417827 | Durance | 2015 |
| Jus | Saint-Just-d'Ardèche | 44.286334 | 4.611151 | Ardèche | 2015 |
| Man | Manosque | 43.809710 | 5.828565 | Durance | 2014 |
| Per | **Pertuis** | 43.667517 | 5.497149 | Durance | 2014, 2015 |

Contexte environnemental appliqué à tous les échantillons biologiques :
*freshwater river biome* [ENVO:01000253] / *river* [ENVO:00000022] /
*river water* [ENVO:01000599]. Les 41 contrôles portent `missing: control sample`
sur les champs géographiques, conformément au vocabulaire INSDC.

### Quatre corrections apportées aux données transmises

**Précision des coordonnées.** Le checklist ENA n'accepte que 8 décimales au maximum
sur latitude et longitude ; certaines valeurs en comptaient 9. Sans correction,
587 valeurs auraient été rejetées à la soumission. Les coordonnées sont tronquées
à 6 décimales, soit une précision d'environ 10 cm — bien au-delà de ce que justifie
une station de pêche.

**Commune d'Ain et Cab.** Les coordonnées tombent sur Villieu-Loyes-Mollon (01800),
à 18 km en aval de Pont-d'Ain initialement indiqué, sur la même rivière Ain.
Commune confirmée par l'utilisateur et corrigée.

**Identité du site Cab.** `site_mapping.csv` porte la ligne
`Cab,Ain,Ain,allopatrie,2015` : Cab désigne bien la station Ain échantillonnée en 2015
(la ligne était initialement passée inaperçue : elle contient une virgule non protégée
dans son dernier champ — « mocks confirmés André, exclus » — ce qui lui donne 7 champs
au lieu de 6, et un parseur CSV strict l'écarte silencieusement). Les coordonnées identiques à Ain fournies par
André sont donc cohérentes avec cette source, et confirmées par l'utilisateur
(Villieu-Loyes-Mollon). Cab et Ain sont deux années de collecte sur la même station,
et restent deux codes distincts dans le dépôt car ils portent des échantillons différents.

**Orthographe du site Bau.** « Sanihac » est une coquille pour **Sanilhac**
(Ardèche, 07110) ; le géocodage inverse des coordonnées fournies tombe exactement
dans cette commune.

**Dates de collecte.** Les dates transmises portaient toutes le 1er juillet, avec
deux coquilles de frappe (« 20215 » pour 2015). Cette date uniforme est manifestement
une valeur générique et non la date réelle de chaque pêche. La soumission ne retient
donc que **l'année**, format que l'ENA accepte pleinement, plutôt que de publier une
fausse précision au jour près. Les années par site concordent exactement avec les
années réellement séquencées. Si les dates de pêche réelles sont retrouvées plus tard,
elles pourront être ajoutées depuis l'interface Webin.

Une vérification indépendante a été menée par géocodage. Confrontées aux communes
telles qu'initialement déclarées, **six** des neuf coordonnées tombaient à moins de 4 km
du centre de la commune (Avi, Bue, Caa, Jus, Man, Per) et **trois** montraient un écart
supérieur à 15 km (Ain, Cab et Bau), ce qui a conduit aux corrections ci-dessus.
Après correction, les neuf sites sont cohérents : Bau se situe à 2,4 km du centre de
Sanilhac, et les coordonnées d'Ain et Cab tombent dans Villieu-Loyes-Mollon même
(commune confirmée par l'utilisateur, géocodage inverse concordant).

## 4. Vérifications déjà effectuées

Trois contrôles ont été menés sur les données avant de préparer le dépôt.

**Intégrité des fichiers.** Les 4 608 fichiers ont été inventoriés et leurs MD5 calculés :
tous distincts, et correspondance exacte avec les 2 304 lignes de `samples_all.csv`.

**Écart de taille sur durance2.** Les métadonnées annonçaient 8,31 Go pour durance2 contre
1,16 Go sur le disque. Explication : ces fichiers étaient stockés non compressés et ont été
gzippés lors de la consolidation ; la colonne de taille du CSV date d'avant compression.
Aucune donnée perdue — le contenu est intact (29 252 lectures sur le fichier témoin,
flow cell BCFFD bien distincte des deux autres runs).

**Permutation d'index i7 (point important).** Les métadonnées montrent que les plaques
branchie et hindgut portent des jeux d'index i7 **différents** entre durance1 et durance2/3
(plaque 3 : SC en durance1, SB ensuite ; plaque 4 : SA puis SC ; etc.), alors que les M&M
annoncent des i7 identiques. Une librairie déjà indexée ne pouvant pas changer d'index,
il fallait écarter l'hypothèse d'une table de correspondance erronée, qui aurait attribué
de mauvais tissus à des fichiers.

Test réalisé : pour chaque librairie, recherche de son plus proche voisin en composition
bactérienne (Bray-Curtis) parmi les réplicats de l'autre run. Si l'étiquetage est juste,
chaque échantillon doit se retrouver lui-même.

- Plaques permutées (3, 4, 5, 6) : **96,5 %** d'auto-appariement.
- Plaques non permutées (1, 2, 7, 8) : **90,1 %**.
- Échecs réciproques (signature d'une véritable inversion) : **0 sur 136**.

Les plaques suspectes s'apparient donc *mieux* que les autres, et aucune paire d'échantillons
ne s'échange mutuellement. L'étiquetage est correct. Les 136 échecs sont des échantillons
peu reproductibles (Bray-Curtis médian 0,53 contre 0,13 pour les réussites), concentrés sur
la nageoire caudale — un tissu à faible biomasse bactérienne, où la variabilité technique
domine. Ce n'est pas un problème de dépôt.

Reste une question pour André, sans effet sur le dépôt mais utile pour les M&M : les PCR
d'indexation ont-elles été refaites pour les runs 2 et 3 ? C'est l'explication la plus
simple des jeux d'index différents. La phrase « identical plate layout and i7 indices »
des M&M devra être corrigée.

---

## 5. Transférer les fichiers

Le transfert se fait **directement de meso vers l'EBI** : les données ne transitent nulle part ailleurs.

```bash
ssh martinj@io-login.meso.umontpellier.fr
cd <répertoire contenant les scripts>

tmux new -s ena          # indispensable : 11,7 Go prennent 1 à 3 h
bash upload_ena_ftp.sh
```

Le script demande l'identifiant et le mot de passe Webin de façon interactive — rien
n'est écrit sur disque. Pour se détacher de tmux : `Ctrl-b` puis `d` ; pour revenir :
`tmux attach -t ena`.

**Point critique — les sous-répertoires par run.** Les noms de fichiers sont *identiques*
d'un run à l'autre (`14Ain1001Cn01A_S1_L001_R1_001.fastq.gz` existe dans les trois runs,
avec trois contenus différents). Un dépôt à plat écraserait les deux tiers des données.
Le script crée donc `durance1/`, `durance2/` et `durance3/` sur le dropbox, et les XML
référencent les fichiers par leur chemin complet.

Le script est relançable : en cas de coupure, relancez la même commande, seuls les fichiers
manquants seront envoyés. Il affiche en fin d'exécution le décompte côté serveur
(attendu : 1 536 par run, 4 608 au total).

---

## 6. Soumettre les métadonnées

Une fois les 4 608 fichiers en place :

```bash
bash submit_ena.sh test     # validation seule — rien n'est publié
```

Le serveur de test rejoue l'intégralité des contrôles ENA sans rien enregistrer.
Lisez le récapitulatif : il doit afficher `success = true`. En cas d'erreur, chaque
message `[ERROR]` désigne l'objet en cause ; corrigez, régénérez les XML
(`python3 build_ena_xml.py --sites ...`) et relancez le test.

Quand le test passe :

```bash
bash submit_ena.sh prod     # soumission réelle, avec confirmation
```

Le reçu XML est conservé horodaté dans `ena_submission/`. **Gardez-le** : il contient
les accessions, et c'est la seule preuve de ce qui a été soumis.

L'ordre project → samples → experiments → runs est géré en une seule requête : l'ENA
résout les références internes (`refname`) automatiquement.

### Embargo

Par défaut les données deviennent publiques immédiatement. Pour les garder confidentielles
jusqu'à la publication de l'article :

```bash
python3 build_ena_xml.py --sites ENA_sites_completes.csv --hold-date 2027-06-30
```

La date est modifiable à tout moment depuis l'interface Webin, y compris pour lever
l'embargo plus tôt le jour de l'acceptation.

---

## 7. Après la soumission

Vous recevrez quatre familles d'accessions :

| Préfixe | Objet | Usage |
|---|---|---|
| `PRJEB######` | study | **c'est celle à citer dans l'article** |
| `ERS######` | samples | 768 |
| `ERX######` | experiments | 2 304 |
| `ERR######` | runs | 2 304 |

Paragraphe *Data availability* proposé, à compléter avec l'accession réelle :

> Raw sequence data have been deposited in the European Nucleotide Archive (ENA) at EMBL-EBI
> under study accession PRJEB###### (https://www.ebi.ac.uk/ena/browser/view/PRJEB######).
> The dataset comprises 768 16S rRNA V4 amplicon libraries, each sequenced three times on
> independent Illumina MiSeq runs (2,304 runs in total), together with extraction blanks,
> no-template PCR controls, ZymoBIOMICS mock community standards and empty-well index-hopping
> controls.

Les métadonnées restent modifiables après dépôt via l'interface Webin : c'est ainsi que
vous passerez de ERC000011 à ERC000013 si vous déposez avant d'avoir les coordonnées.

---

## 8. Fichiers fournis

| Fichier | Rôle |
|---|---|
| `ENA_sites_completes.csv` | coordonnées des 9 sites, validées et corrigées (fourni) |
| `build_ena_xml.py` | génère les 5 XML ; `--sites` bascule vers MIxS, `--hold-date` pose l'embargo |
| `ena_samples.tsv` | table des 768 samples |
| `ena_experiments_runs.tsv` | table des 2 304 experiments/runs avec MD5 |
| `ena_submission/*.xml` | **XML prêts, checklist MIxS ERC000013 — validés, rien à régénérer** |
| `upload_ena_ftp.sh` | transfert des 4 608 fichiers depuis meso |
| `submit_ena.sh` | soumission des métadonnées (`test` puis `prod`) |
| `fastq_manifest.tsv` | inventaire des 4 608 fichiers avec MD5 et tailles |
| `identity_check.tsv` | résultat détaillé de la vérification d'identité |

---

## 9. Ordre des opérations

1. **Créer le compte Webin** — seule étape préalable restante (section 2).
2. Transférer : `bash upload_ena_ftp.sh` (dans tmux, 1 à 3 h).
3. Valider : `bash submit_ena.sh test` → jusqu'à `success = true`.
4. Soumettre : `bash submit_ena.sh prod`.
5. Archiver le reçu et noter l'accession `PRJEB`.

Les métadonnées sont complètes et validées : les XML du dossier `ena_submission/`
sont prêts à l'emploi. Il n'y a plus rien à régénérer, sauf si vous souhaitez poser
un embargo :

```bash
python3 build_ena_xml.py --sites ENA_sites_completes.csv --hold-date 2027-06-30
```


---

## CORRECTION IMPORTANTE (2026-08-30) — provenance des coordonnees

La section 3 ci-dessus affirme que *"les coordonnees des 9 sites ont ete fournies par
Andre"*. **C'est inexact.** JF Martin a confirme le 2026-08-30 que ces coordonnees
etaient **ses propres extrapolations**, deduites de noms de communes, et non des
releves de terrain.

Andre a transmis les coordonnees reelles le 2026-08-30. Confrontees au depot :

| Code | Riviere deposee | Riviere reelle | Ecart de position |
|---|---|---|---|
| Caa | Durance | Canal (usine du Largue) | **41,4 km** |
| Ain / Cab | Ain | **Suran** | **17,2 km** |
| Man | Durance | Durance | **13,4 km** |
| Bau | Ardeche | **Beaume** | **7,6 km** |
| Bue | Durance | **Buech** | **5,2 km** |
| Jus | Ardeche | Ardeche | 1,1 km |
| Per | Durance | Durance | 0,34 km |
| Avi | Durance | Durance | 0,24 km |

**Six des neuf sites** portent une coordonnee fausse de plus de 5 km dans le depot, et
**cinq** une riviere fausse. De plus, `Ain` et `Cab` correspondent chacun a **DEUX
stations physiques** sur le Suran (Pont-d'Ain et Chavannes-sur-Suran, 24 km d'ecart,
separees par un seuil infranchissable de 2,5 m), et non a une station unique.

En consequence, les raisonnements de la section 3 batis sur ces coordonnees sont
caducs :
- la "commune confirmee par l'utilisateur" (Villieu-Loyes-Mollon) confirmait une
  extrapolation, pas un releve ;
- le geocodage inverse concordait avec la commune extrapolee, ce qui ne validait donc
  rien : la concordance etait garantie par construction ;
- la correction d'orthographe Sanihac -> Sanilhac portait sur une commune deduite ;
  la station reelle est **Rosieres**, sur la **Beaume**.

**A FAIRE** : corriger les metadonnees d'echantillon du depot PRJEB124417 via
l'interface Webin (les champs geographiques et la date de collecte sont modifiables
apres soumission) :
1. latitude / longitude des 9 sites -> `metadata/station_reference.csv` ;
2. distinguer les deux stations du Suran (les echantillons Ain/Cab n'ont pas tous la
   meme coordonnee) -> `metadata/station_mapping.csv` ;
3. renseigner la **date de collecte au jour pres**, maintenant disponible (le depot ne
   porte que l'annee, faute de dates fiables a l'epoque) ;
4. corriger l'annee de collecte de `15Per2015Ch03A` : coquille de saisie, l'individu
   a ete peche en 2014 (Pertuis n'a pas ete echantillonne en 2015).

Details et temoins : `docs/decision_stations.md`.
