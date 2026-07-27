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

## Faits à retenir (2026-07)
- **Ain = deux codes** : `Ain` (2014) + `Cab` (2015). Réunis, 35 poissons —
  concorde avec le tableau d'André (14 + 21).
- **Caa = canal** (Durance, allopatrie), 20 poissons — confirmé André.
- **Man = Manosque** (Durance), 15 poissons — confirmé André, mais ABSENT du
  tableau des 6 populations : rôle à définir (7ᵉ population ou exclusion).
- **Per** : 10 poissons, nom et rôle NON renseignés — en attente André.
- **Büech (Bue)** : nom confirmé, mais l'effectif séquencé (35) ne concorde pas
  encore avec le tableau (53) — réconciliation en attente André.
- Rappel : les Chondrostoma sp. (`Ch`) ne sont pas encore résolus en
  hotu/toxostome/hybride ; c'est indépendant de cette table de sites.
