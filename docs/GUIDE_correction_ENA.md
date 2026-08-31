# Guide — correction des métadonnées du dépôt ENA `PRJEB124417`

**Destinataire** : la session « ENA Submission Durance Replicates », qui a réalisé le dépôt initial.
**Auteur** : session « analyse microbiome » (projet `microbiome-hybrid` sur meso).
**Date** : 2026-08-31. **Dépôt de référence** : `github.com/martinjfsupagro/microbiome-hybrid` (privé).

---

## 1. Ce qui s'est passé, et pourquoi il faut corriger

Le dépôt initial a été soumis avec la checklist MIxS **ERC000013**, qui exige des coordonnées
géographiques. Celles-ci ont été prises dans `ena_deposit/ENA_sites_completes.csv`, dont le
guide de dépôt affirmait qu'elles venaient d'André.

**C'est inexact.** JF Martin a confirmé le 2026-08-30 que ces coordonnées étaient **ses propres
extrapolations**, déduites de noms de communes. André a depuis transmis les relevés de terrain.
L'écart est important :

| Code | Rivière déposée | Rivière réelle | Écart de position |
|---|---|---|---|
| `Caa` | Durance | **canal (usine du Largue)** | **41,4 km** |
| `Ain`, `Cab` | Ain | **Suran** | **17,2 km** |
| `Man` | Durance | Durance | **13,4 km** |
| `Bau` | Ardèche | **Beaume** | **7,6 km** |
| `Bue` | Durance | **Buech** | **5,2 km** |
| `Jus` | Ardèche | Ardèche | 1,1 km |
| `Per` | Durance | Durance | 0,34 km |
| `Avi` | Durance | Durance | 0,24 km |

Cinq noms de rivière sont faux et six positions décalées de plus de 5 km.

**Un point structurel s'ajoute** : les codes `Ain` et `Cab` recouvrent en réalité **deux stations
physiquement distinctes** sur le Suran — Pont-d'Ain et Chavannes-sur-Suran, distantes de 25,4 km
et séparées par un obstacle franchissable seulement vers l'aval. Elles portent des taxons
différents. La correction est donc **par échantillon**, pas par code de site : deux échantillons
du même code `Ain` peuvent avoir des coordonnées différentes.

Enfin, deux informations absentes au moment du dépôt sont maintenant disponibles : les **dates de
collecte exactes** (déposées à l'année seule) et l'**identité génotypique** des poissons
(531 échantillons déposés comme `Chondrostoma sp.`, désormais résolus).

---

## 2. Ce qui ne change PAS

À ne toucher sous aucun prétexte :

- **les accessions** `ERS…` — elles restent, c'est le point de la manœuvre ;
- **les alias** `DURANCE16S_*` — identifiants immuables (voir §4.3 pour le cas de la coquille) ;
- **`SAMPLE_NAME` / `TAXON_ID`** — `fish metagenome` (496924), `fish gut metagenome`,
  `gill metagenome`, `blank sample`, `synthetic metagenome` : ce sont les taxons de
  l'**échantillon** (métagénome), pas de l'hôte. Inchangés ;
- **les 41 contrôles** (25 `empty`, 8 `temoin`, 4 `blank`, 4 `mock`) — ils portent
  `missing: control sample` et n'ont aucune coordonnée à corriger ;
- **les objets EXPERIMENT et RUN**, les fichiers FASTQ, leurs sommes de contrôle : rien à
  retransférer.

Seuls **727 échantillons biologiques** sont concernés.

---

## 3. Les corrections à appliquer

Le fichier `ena_deposit/ena_corrections.tsv` (3 472 lignes) donne, pour chaque échantillon,
l'alias, l'accession `ERS`, l'attribut, la valeur déposée, la valeur corrigée et le motif.
Il est produit par `scripts/25-ena_corrections.py` et régénérable.

| Attribut ENA | Échantillons | Nature du changement |
|---|---|---|
| `geographic location (latitude)` | 727 | relevé de terrain au lieu de l'extrapolation ; **par station** |
| `geographic location (longitude)` | 727 | idem |
| `geographic location (region and locality)` | 727 | `Villieu-Loyes-Mollon` → `Pont-d'Ain, Suran` etc. |
| `collection date` | 727 | année → date exacte |
| `host scientific name` | 564 | identité résolue par génotypage |

Les coordonnées et dates de référence, par station :

| Station | Rivière | Codes | Latitude | Longitude | Date(s) |
|---|---|---|---|---|---|
| Avignon | Durance | Avi | 43.913000 | 4.820722 | 2014-07-17 ; 2015-07-10 |
| Canal (usine du Largue) | canal | Caa | 43.853389 | 5.858444 | 2015-09-08 |
| Chavannes-sur-Suran | Suran | Ain, Cab | 46.264389 | 5.429444 | 2014-08-12 ; 2015-08-26 |
| Confluence Buech-Méouge | Buech | Bue | 44.262000 | 5.828000 | 2014-07-03 ; 2015-07-17 |
| Manosque-Oraison | Durance | Man | 43.919667 | 5.896278 | 2014-07-23 |
| Pertuis | Durance | Per | 43.668139 | 5.493000 | 2014-07-07 ; 2014-08-20 |
| Pont-d'Ain | Suran | Ain, Cab | 46.048000 | 5.324000 | 2014-08-12 ; 2015-08-26 |
| Rosières | Beaume | Bau | 44.475000 | 4.264000 | 2015-07-22 |
| Saint-Just-d'Ardèche | Ardèche | Jus | 44.286000 | 4.597833 | 2015-07-21 |

Pour les stations à deux dates, l'année de chaque individu tranche — c'est déjà résolu dans
`ena_corrections.tsv`. **Sauf Pertuis** : voir §4.1.

Répartition des corrections d'identité de l'hôte :

| Valeur déposée | Valeur corrigée | Échantillons |
|---|---|---|
| `Chondrostoma sp.` | `Parachondrostoma toxostoma` | 322 |
| `Chondrostoma sp.` | `Chondrostoma nasus` | 112 |
| `Chondrostoma sp.` | hybride | 97 |
| `Chondrostoma nasus` | hybride | 17 |
| `Chondrostoma nasus` | `Parachondrostoma toxostoma` | 8 |
| `Parachondrostoma toxostoma` | hybride | 8 |

Les 33 dernières lignes correspondent à **8 individus dont l'identification morphologique était
fausse** — le génotypage les a reclassés. C'est une correction de fond, pas de forme.

---

## 4. Trois décisions à trancher AVANT de soumettre

### 4.1 Pertuis : deux dates la même année

La station Pertuis a été pêchée le **2014-07-07 et le 2014-08-20**, les deux en 2014. Rien dans
les métadonnées ne dit quel individu vient de quelle sortie. Les 44 échantillons concernés
portent la valeur `2014-07-07/2014-08-20` et le motif `A TRANCHER` dans le fichier de correction.

Options : demander l'assignation à André ; ou déposer l'intervalle au format ISO 8601
`2014-07-07/2014-08-20`, que la checklist ENA accepte pour une période. **Ne pas choisir une des
deux dates au hasard.**

### 4.2 Nom d'hôte pour les hybrides

**Vérifié** : il n'existe **aucun taxon NCBI** pour `Chondrostoma nasus x Parachondrostoma
toxostoma`. Une recherche naïve renvoie le taxid 77800, mais c'est *Parachondrostoma toxostoma*
lui-même, par appariement partiel du nom — ce n'est pas une confirmation.

Ce n'est pas bloquant : `host scientific name` est un attribut MIxS en **texte libre**, distinct
du `SCIENTIFIC_NAME`/`TAXON_ID` de `SAMPLE_NAME` (qui reste `fish metagenome`). Mais ENA peut
appliquer une validation. Deux options :

- **(a)** `Chondrostoma nasus x Parachondrostoma toxostoma` en texte libre — informatif, à valider
  sur le serveur de test ;
- **(b)** garder `Chondrostoma sp.` et ajouter un attribut libre, par exemple
  `host genotypic category` = `Cn` / `Hy` / `Pt` — plus sûr, moins lisible.

Le fichier de correction propose **(a)**. Si le serveur de test refuse, basculer sur (b) est une
substitution mécanique dans une colonne.

### 4.3 L'alias qui porte une coquille

L'échantillon `DURANCE16S_15Per2015Ch03A` (accession `ERS31168490`) a un préfixe d'année erroné :
le poisson a été collecté en **2014**, pas 2015. C'est une faute de frappe du nom de terrain, qui
avait scindé un même poisson en deux enregistrements dans nos tables — corrigée chez nous par une
table de jointure, sans jamais renommer l'échantillon.

**Recommandation : ne pas toucher à l'alias.** C'est un identifiant, pas une donnée ; le modifier
casserait la correspondance avec les fichiers FASTQ déjà déposés et avec nos manifestes. Corriger
en revanche ses **attributs** (`collection date` en 2014, `host_individual_id`), et mentionner la
divergence dans la description de l'étude.

---

## 5. Procédure technique

### 5.1 Le mécanisme

Le dépôt initial a utilisé un POST HTTPS vers la boîte de dépôt Webin avec
`submission.xml` + `sample.xml`, action `<ADD/>` (`ena_deposit/1_soumettre_metadonnees.sh`).
Une mise à jour emprunte **exactement la même voie** avec l'action `<MODIFY/>` :

```xml
<?xml version="1.0" encoding="UTF-8"?>
<SUBMISSION>
  <ACTIONS>
    <ACTION>
      <MODIFY/>
    </ACTION>
  </ACTIONS>
</SUBMISSION>
```

Le `sample.xml` doit contenir les échantillons **complets** — ENA remplace l'objet, il ne fusionne
pas les attributs. Il faut donc régénérer le XML entier avec les valeurs corrigées, pas un XML
partiel ne contenant que les champs modifiés. C'est le piège principal de cette opération.

### 5.2 Marche à suivre

1. **Vérifier le statut du dépôt.** Le portail public ENA ne renvoie rien pour `PRJEB124417` au
   2026-08-31, ce qui est cohérent avec une étude non encore publiée — à confirmer dans le portail
   Webin. Si l'étude est déjà publique, la modification de métadonnées reste possible, mais les
   enregistrements déjà moissonnés par des tiers ne seront pas rétroactifs.

2. **Mettre à jour la source des coordonnées.** `ena_deposit/ENA_sites_completes.csv` porte encore
   les extrapolations et est **indexé par code de site**, ce qui ne peut plus représenter les deux
   stations du Suran. Utiliser `metadata/station_reference.csv` (une ligne par couple code+station)
   ou directement `ena_deposit/ena_corrections.tsv`.

3. **Régénérer `sample.xml`** avec `build_ena_xml.py`, adapté pour lire les coordonnées **par
   échantillon** et non par site. Attention : ce script écrit `not provided` et bascule sur
   ERC000011 si une coordonnée manque — vérifier que la sortie annonce bien `ERC000013`.

4. **Passer par le serveur de test d'abord** : `bash 1_soumettre_metadonnees.sh test`
   (`https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit/`). C'est là qu'on voit si le nom d'hôte
   hybride passe la validation. Rien n'est publié.

5. **Soumettre en production** une fois le reçu de test propre.

6. **Contrôler le reçu** : il doit annoncer 727 `SAMPLE` avec `success="true"` et les **mêmes
   accessions ERS** qu'à l'origine. Une nouvelle accession signifierait qu'un `ADD` a eu lieu au
   lieu d'un `MODIFY` — dans ce cas, arrêter et ne pas relancer.

### 5.3 Identifiants

Les scripts existants demandent les identifiants Webin en interactif et ne les stockent pas ;
le `passwordFile` est hors du dossier versionné. **Conserver ce fonctionnement** — ne pas écrire
d'identifiant dans un fichier du dépôt.

---

## 6. Vérifications, avant et après

**Avant** : dans le XML régénéré, contrôler que
- aucune coordonnée ne vaut `45.906458` / `5.233251` (l'extrapolation de Villieu-Loyes-Mollon) ;
- les deux stations du Suran ont bien des coordonnées **différentes** — c'est le contrôle qui
  distingue une correction par station d'une correction par site ;
- aucune `collection date` biologique ne vaut `2014` ou `2015` nus ;
- la checklist annoncée est `ERC000013` ;
- il y a 727 échantillons biologiques et 41 contrôles inchangés.

**Après** : réinterroger l'API du portail ENA sur quelques accessions et vérifier que `lat`, `lon`
et `collection_date` reflètent les nouvelles valeurs.

---

## 7. Fichiers fournis

Tous dans `github.com/martinjfsupagro/microbiome-hybrid` :

| Fichier | Contenu |
|---|---|
| `ena_deposit/ena_corrections.tsv` | **la table de correction**, 3 472 lignes : alias, accession, attribut, avant, après, motif |
| `scripts/25-ena_corrections.py` | le script qui la produit, régénérable |
| `metadata/station_reference.csv` | les 9 stations : rivière, coordonnées WGS84, dates |
| `metadata/analysis_metadata.csv` | table par échantillon : station, catégorie génotypique, coordonnées, date |
| `docs/decision_stations.md` | la note qui établit les corrections et leur provenance |
| `docs/manuscrit/table_S1_stations.csv` | la Table S1 du manuscrit, cohérente avec ce qui précède |

---

## 8. Résumé en une ligne

727 échantillons biologiques, cinq attributs à corriger, par `MODIFY` sur la même voie HTTPS que
le dépôt initial, en passant d'abord par le serveur de test ; trois décisions à prendre avant
(dates de Pertuis, nom d'hôte hybride, alias avec coquille) ; les accessions, les alias et les
fichiers ne bougent pas.
