# Corrections ENA restantes — état et mode d'emploi

État au 2026-09-30. PRJEB124417 est soumis et à jour sur les coordonnées, les rivières, les dates
(hors Pertuis) et l'identité d'hôte. Deux corrections de métadonnées sont **prêtes et non
soumises**, une troisième question est structurelle et ne se traite pas par un MODIFY.

## Ce qui est prêt

| table | champ ENA | lignes | état |
|---|---|---|---|
| `ena_corrections_pertuis_dates.tsv` | `collection date` | 44 | décidé (André, 2026-09-30) |
| `ena_corrections_subject_id.tsv` | `host subject id` | 727 | prêt, **décision JF** sur l'opportunité |

Les deux tables portent le même format à huit colonnes et **ne se recouvrent pas** : elles touchent
44 alias communs mais sur deux champs différents, et `build_ena_modify.py` refuse explicitement de
corriger deux fois le même champ pour un même alias. Elles peuvent donc partir **dans une seule
soumission** — l'option `--corrections` est répétable.

## Un défaut corrigé le 2026-09-30, avant toute soumission

La table `host subject id` était construite mécaniquement depuis les identifiants déposés. Elle
préfixait chaque sujet par sa campagne, ce qui donnait pour le poisson Pertuis n° 2015 :

| échantillon | puits | sujet déposé | sujet corrigé, version d'origine |
|---|---|---|---|
| `14Per2015Ch01A` | E11 | `Per2015` | `14Per2015` |
| `14Per2015Ch02A` | D11 | `Per2015` | `14Per2015` |
| `14Per2015Ch05A` | E11 | `Per2015` | `14Per2015` |
| `15Per2015Ch03A` | E11 | `Per2015` | **`15Per2015`** |

Ces quatre échantillons sont les quatre tissus **d'un seul poisson** : le préfixe `15` est une
coquille de saisie, documentée dans `metadata/individual_corrections.csv` et à l'origine de la
correction de 181 à 180 individus. Soumise telle quelle, la table aurait scindé cet animal en
**deux sujets d'hôte distincts** dans une archive publique — une erreur structurelle bien plus
difficile à repérer après coup qu'une valeur fausse.

Corrigé : `15Per2015Ch03A` reçoit `14Per2015` comme ses trois autres tissus. Le motif de la table
annonçait « 25 identifiants réutilisés » ; le nombre réel de réutilisations entre campagnes est de
**24**, le vingt-cinquième étant cette coquille. Contrôle après correction : aucun identifiant
n'est plus ambigu, et les quatre tissus du poisson portent le même sujet.

## Comment soumettre

Les identifiants Webin sont saisis au clavier et ne sont jamais écrits : **un humain lance le
script**. Depuis `ena_deposit/` :

```bash
# 1. construire le MODIFY (les deux corrections, ou une seule en retirant sa ligne)
python3 build_ena_modify.py \
    --deposited ena_submission/sample.xml \
    --corrections ena_corrections_pertuis_dates.tsv \
    --corrections ena_corrections_subject_id.tsv \
    --receipt "$(ls -t receipt_prod_*.xml | head -1)" \
    --outdir ena_update

# 2. valider les valeurs sur le serveur de test, puis soumettre en production
bash 4_corriger_metadonnees.sh test
bash 4_corriger_metadonnees.sh prod

# 3. verifier quelques heures plus tard
bash 5_verifier_correction.sh
```

Rappel de recette, à ne pas redécouvrir : le FTP Webin est inutilisable, les MODIFY passent par
`curl` sur le drop-box. Le script s'arrête si une seule accession du reçu diffère.

Après soumission, deux textes sont à mettre à jour : le §9 de `Article.docx`, où la note grise sur
Pertuis doit céder la place aux deux dates, et la note grise du `Supplementary_Data.docx` sous
*Host subject identifiers*.

## Ce qui ne se traite pas par un MODIFY

**Le modèle du dépôt : 2 304 EXPERIMENT déclarés.** Dans le modèle de données de l'ENA, un
EXPERIMENT est une **librairie** et un RUN un séquençage de cette librairie. Or `durance2` et
`durance3` sont deux séquençages d'une **même** préparation : ils devraient partager un
EXPERIMENT et ne différer que par le RUN. Le compte cohérent est donc **1 536** experiments
(768 échantillons × 2 préparations) pour 2 304 runs, au lieu de 2 304 experiments.

Ce n'est pas une valeur à corriger mais une restructuration : fusionner des objets et repointer
des runs. C'est aussi, ironiquement, exactement la structure nichée que le §8.7 de l'article
décrit et dont il fait un argument. À traiter délibérément, avec l'assistance ENA si nécessaire,
et **pas** en même temps qu'une correction d'attributs.

**L'ouverture publique du dépôt** se décide à la soumission de l'article, pas maintenant.
