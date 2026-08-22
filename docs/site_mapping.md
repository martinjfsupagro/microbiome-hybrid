# metadata/site_mapping.csv — table de correspondance code-site → site écologique

## Objet
Joindre les codes-sites des échantillons séquencés (colonne `site` de
`samples_all.csv`, telle qu'écrite dans les noms d'échantillons) aux noms de
sites écologiques et à leur rôle dans la zone hybride (tableau d'André).

**Aucun nom d'échantillon n'est modifié.** Cette table est une simple clé de
jointure : on relie par `site_code`. Les noms d'échantillons et la colonne
`site` d'origine restent intacts.

## Jointure
```python
import csv
samples = list(csv.DictReader(open('metadata/samples_all.csv')))
smap = {r['site_code']: r for r in csv.DictReader(open('metadata/site_mapping.csv'))}
for s in samples:
    m = smap.get(s['site'])          # jointure par le code-site, sans renommage
    s['site_nom']  = m['site_nom']  if m else ''
    s['role']      = m['role_propose'] if m else ''
```

## Colonnes
- `site_code`     : code tel qu'il apparaît dans les noms d'échantillons (Caa, Ain, Cab, …)
- `site_nom`      : nom écologique du site (canal, Ain, Büech, …)
- `riviere`       : Durance / Ardèche / Ain
- `role_propose`  : rôle dans la zone hybride (allopatrie / sympatrie+hyb / asym. Toxo / asym. Hotu)
- `annees_sequencees` : année(s) présente(s) dans les données pour ce code
- `statut`        : source/état de la correspondance (confirmé André, en attente, à statuer)

## Faits à retenir (mis à jour 2026-07-27, réunion André)
- **Ain = deux codes** : `Ain` (2014, 14 poissons) + `Cab` (2015, 19 poissons après
  exclusion des 2 mocks). Réunis, **33 poissons**.
- **Cab1021 et Cab1022 = MOCKS confirmés par André** (mal étiquetés, plaque 1, série
  d'index 711) : à interpréter comme mocks, PAS comme poissons. Ain 2015 : 21 → **19**.
  Total individus biologiques : 183 → **181**. Voir docs/decision_mock_samples.md.
- **Caa = canal** (Durance, allopatrie), 20 poissons — confirmé André.
- **Man = Manosque** (Durance), 15 poissons — confirmé André, mais ABSENT du
  tableau des 6 populations : rôle à définir (7ᵉ population ou exclusion).
- **Per** : 10 poissons, nom et rôle NON renseignés — en attente André.
- **Büech (Bue)** : **35 poissons** (effectif définitif, confirmé André). Le chiffre
  « 53 » évoqué précédemment provenait d'une lecture erronée du tableau et est retiré.
- Rappel : les Chondrostoma sp. (`Ch`) ne sont pas encore résolus en
  hotu/toxostome/hybride.

## Résolution des taxons et des populations retenues (en attente André)
Le génotypage des poissons n'est pas terminé (André). Il produira **un index hybride
par individu**. Cet index servira à :
  - classer chaque `Ch` en hotu / toxostome / hybride (point 4a) ;
  - décider **quelles populations sont conservées** dans l'analyse finale (point 4b :
    sort de Manosque et Per, structure du gradient).
Ces décisions sont donc suspendues à la réception de l'index hybride.
