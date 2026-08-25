# Microbiome 16S — hotu / toxostome / chondrostome et hybrides
## Rapport d'analyse : des lectures brutes à la table d'ASV

*Projet `microbiome-hybrid`. Traitement bioinformatique, juillet 2026.*
*Destiné à André (données de terrain et identification des poissons).*

---

## 1. Objet

Caractériser le microbiome (16S V4) de plusieurs tissus chez le hotu (`Cn`), le
toxostome (`Pt`), le chondrostome non résolu (`Ch`) et — via les mesures de
terrain — leurs hybrides, sur 9 sites de la Durance et deux années (2014, 2015).
**Question de fond** : le microbiome des hybrides est-il intermédiaire entre les
parentaux, ou déplacé hors de leur intervalle ?

Ce rapport couvre le **traitement des données** (nettoyage, inférence des
variants de séquence, taxonomie). L'analyse écologique proprement dite
(diversité, comparaisons entre groupes) reste à faire ; les données sont prêtes
pour cela. Les points nécessitant ton avis sont en **§7**.

---

## 2. Jeu de données

Trois runs MiSeq (`M03930` n° 62, 69, 72) qui se sont révélés être **le
reséquençage des mêmes 768 échantillons** — même plan de plaque, mais DEUX
préparations de librairie distinctes (cf. docs/decision_run_design.md) : par rapport
à durance1, l'i7 diffère pour 384/768 librairies et l'i5 pour 576/768 ; durance2 et
durance3 partagent des index identiques sur les 768. [CORRIGE 2026-08-25 : la version
antérieure disait "mêmes index i7, seuls les i5 changent", généralisation erronée
depuis la plaque 1.] Chaque échantillon est donc présent **en
triple**. C'est une bonne nouvelle : l'effet « run de séquençage » peut être
estimé directement et n'est confondu avec aucun facteur biologique (voir §7).

**Plan réalisé au séquençage** (183 échantillons "poisson" séquencés ; 181 vrais poissons après exclusion de Cab1021/Cab1022 = mocks confirmés André 2026-07-27) :

| Facteur | Détail |
|---|---|
| Taxon (poissons) | chondrostome `Ch` : 134 · hotu `Cn` : 37 · toxostome `Pt` : 12 |
| Tissus | caudale, branchie, midgut, hindgut (≈ 4 par poisson) |
| Sites | Ain, Avi, Bau, Bue, Caa, Cab, Jus, Man, Per |
| Années | 2014, 2015 |
| Contrôles | 4 blancs, 2 mock, témoins et puits vides (× 3 runs) |

Plan déséquilibré (site et année largement confondus, taxon et site aussi) —
à garder en tête pour les modèles statistiques.

---

## 3. Consolidation des métadonnées (tes réponses intégrées)

Avant toute analyse, les métadonnées des trois runs ont été reconstruites,
vérifiées et fusionnées en un fichier unique (`samples_all.csv`, 2304 lignes).
Les points que tu avais tranchés ont été appliqués et **tracés** (chaque
correction laisse un drapeau dans le fichier, rien n'est réparé en silence) :

| Point | Décision appliquée |
|---|---|
| Codes tissus | `01`=caudale, `02`=midgut, `03`=hindgut, `05`=branchie |
| Code `Ch` | = **chondrostome non identifié** (ni `Cn` ni `Pt` tranché) — **pas** le chevesne ; le chevesne (`Sc`) n'est pas dans ces runs |
| Taxons manquants (Ain 2014, individus 1036–1043) | complétés depuis la feuille de terrain (1036–1037 `Cn`, 1038–1043 `Pt`) |
| Suffixe `bis` | = ré-extraction du même tissu (colonne `extraction`) |
| `15Avi1002Cn04A` | code tissu `04` corrigé en `05` (branchie) |
| Taille / poids / sexe | joints depuis `HotuToxo_taillepoids.xlsx`, par individu (2070 lignes renseignées ; 3 individus en conflit corrigés avec tes valeurs) |

**Reste ouvert** : l'identification fine des `Ch` (et le statut hybride, code
`Hy` du fichier taille/poids) est en cours de ton côté ; elle n'est pas encore
intégrée à la table. C'est le point clé pour la question hybride (§7).

---

## 4. Traitement bioinformatique

Marqueur 16S V4 (amorces Caporaso 515F/806R), déjà retirées des lectures
(protocole Schloss). Les trois runs sont traités **séparément** puis fusionnés.

### 4.1 Retrait du 12S de l'hôte (co-amplification)

Les amorces 16S V4 co-amplifient le **12S mitochondrial du poisson hôte** : entre
**14 et 16 % des lectures par run**, et jusqu'à **67 % pour certains
échantillons** (souvent les tissus riches en tissu hôte). Ce n'est pas du bruit
technique — c'est de l'ADN hôte — mais il fausserait l'analyse bactérienne.

Il est retiré en amont, par la **longueur** : l'amplicon 12S (~190 pb) est plus
court que le V4 bactérien (~253 pb), ce qui permet de les séparer proprement.
Les lectures 12S sont **conservées à part** (elles restent un signal hôte
exploitable si besoin).

| Run | Lectures | dont 12S/dimères retirés |
|---|---|---|
| durance1 | 12,5 M | 1,90 M (15,2 %) |
| durance2 | 14,8 M | 2,19 M (14,8 %) |
| durance3 | 14,0 M | 1,99 M (14,2 %) |

### 4.2 Inférence des ASV (DADA2)

Filtrage qualité puis inférence des **variants de séquence d'amplicon (ASV)** —
résolution à la base près, sans clustering en OTU. Modèle d'erreur appris
**séparément pour chaque run**. Fusion R1/R2 excellente : **93–94 %** des
lectures filtrées (médiane), signe d'un recouvrement franc et d'un nettoyage
correct.

Bilan de rétention (lectures 16S entrant dans DADA2 → conservées) : **78–87 %
selon le run**. Longueur des ASV : pic net à **251 pb** (V4 attendu, aucun
résidu 12S).

### 4.3 Fusion des runs, chimères, taxonomie

Les trois tables sont fusionnées en **gardant les runs distincts** (chaque
échantillon suffixé par son run), puis les chimères sont retirées (98 % des
lectures conservées). Taxonomie assignée contre **SILVA v138.2**.

---

## 5. Résultats

**Table d'analyse : 44 349 ASV × 2295 échantillons** (26,8 M de lectures cibles).

Sur les 2304 lignes attendues, 9 sont absentes de la table (vides après
filtrage) : 8 puits/contrôles `empty` et un seul biologique
(`15Bue1014Ch03A`, uniquement sur durance3 — présent dans les deux autres runs).

### Assignation taxonomique (% d'ASV assignés)

| Rang | % | | Rang | % |
|---|---|---|---|---|
| Domaine | 100 % | | Famille | 77 % |
| Phylum | 98,6 % | | Genre | 47 % |
| Classe | 96,6 % | | Espèce | 2 % |
| Ordre | 90,3 % | | | |

(Le faible taux à l'espèce est normal pour le V4 avec SILVA — la résolution
s'arrête souvent au genre.)

### Composition (par abondance de lectures)

**Phyla** : Pseudomonadota 49 % · Fusobacteriota 13,5 % · Bacillota 10 % ·
Bacteroidota 7,6 % · Verrucomicrobiota et Thermodesulfobacteriota ~3,5 % chacun.

**Genres dominants** — plusieurs sont des taxons bien connus chez les poissons,
sur lesquels ton regard d'écologue sera précieux :

| Genre | % lectures | Note |
|---|---|---|
| *Cetobacterium* | 13,4 % | symbionte intestinal typique des poissons d'eau douce |
| *Aeromonas* | 6,0 % | commensal/pathogène opportuniste fréquent |
| *Flavobacterium* | 3,0 % | inclut des pathogènes de branchies/peau |
| *Deinococcus* | 2,9 % | |
| Ca. *Branchiomonas* | 1,8 % | associé aux branchies (épithéliocystis) |
| Ca. *Piscichlamydia* | 1,4 % | agent d'épithéliocystis branchiale |

La cohérence de ces taxons avec l'écologie des cyprinidés est un bon indice que
le nettoyage (12S, chimères) a bien fonctionné.

### Signal hôte résiduel

Au-delà du retrait par la longueur (§4.1), un **filtre taxonomique** a retiré
**1971 ASV hors-cible** : 1144 Mitochondria (12S hôte passé en pleine longueur),
784 Chloroplast (algues/plantes de l'environnement), 22 Eukaryota, 21 non
assignés. Ce double garde-fou (longueur + taxonomie) est ce qui garantit une
table réellement bactérienne.

---

## 6. Contrôles

Blancs, mocks (communautés artificielles) et puits vides sont conservés dans la
table pour l'évaluation de la contamination : les vides tombent bien à zéro
(écartés du fait de l'absence de lectures), et les mocks fourniront le contrôle
positif de l'inférence. Une analyse de décontamination (p. ex. *decontam*)
pourra s'appuyer dessus si tu le juges utile.

---

## 7. Ce qui est prêt, et ce sur quoi j'ai besoin de toi

**Prêt** : table d'ASV filtrée + taxonomie + métadonnées complètes (taxon,
tissu, site, année, taille, poids, sexe), reliées échantillon par échantillon.
On peut enchaîner sur diversité α/β, décontamination, et le test de la question
hybride.

**Questions pour toi :**

1. **Identification fine des `Ch` et statut hybride.** C'est le verrou de la
   question centrale. Le fichier taille/poids contient un code `Species`
   (Cn/Pt/Ch/**Hy**) qui distingue les hybrides — non encore intégré. Dès que
   ton identification est stabilisée, je l'ajoute et on pourra positionner les
   hybrides vis-à-vis des parentaux.
2. **Réplicats de run.** Les 3 séquençages des mêmes librairies : veux-tu qu'on
   s'en serve pour **quantifier/contrôler l'effet run** (recommandé), puis qu'on
   agrège ? ou qu'on somme d'emblée ?
3. **Plan déséquilibré.** Site × année × taxon sont partiellement confondus ;
   il faudra choisir ensemble les contrastes défendables (p. ex. comparer les
   taxons à site et tissu fixés là où c'est possible).
4. **Tissus et co-contamination hôte.** Le taux de 12S varie beaucoup selon le
   tissu ; est-ce attendu (branchie/caudale plus « hôte » que le tube digestif) ?
   Cela peut orienter des analyses par tissu.

---

## 8. Fichiers

Dans `results/dada2_final/` :

| Fichier | Contenu |
|---|---|
| `asv_table_filtered.tsv` | table d'analyse : 44 349 ASV × 2295 échantillons |
| `taxonomy.tsv` | assignation SILVA (Domaine → Espèce) par ASV |
| `asv.fasta` | séquences des ASV |
| `seqtab_nochim_filtered.rds` | même table, format R/DADA2 |
| `track_all.csv` | suivi des lectures à chaque étape |

Métadonnées : `metadata/samples_all.csv`. La **jointure** table ↔ métadonnées se
fait par la colonne `dada2_id` (ex. `14Ain1001Cn01A__durance1`).

*Toutes les étapes sont scriptées, versionnées (git) et reproductibles ; les
choix de paramètres sont justifiés en tête de chaque script.*
