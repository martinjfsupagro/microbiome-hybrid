# Corrections ENA restantes — état et mode d'emploi

État au 2026-10-06. **La procédure de soumission du 30/09 était fausse** (section « Incident du 2026-10-06 ») ;
elle est remplacée par `scripts/53` et `10_corriger_pertuis_sujet.sh`. Au 30/09, PRJEB124417 est
soumis et à jour sur les coordonnées, les rivières, les dates (hors Pertuis) et l'identité d'hôte. Deux corrections de métadonnées sont **prêtes et non
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

## Incident du 2026-10-06 — la commande du 30/09 aurait annulé les corrections publiées

La version précédente de ce mémo faisait construire le MODIFY par
`build_ena_modify.py --deposited ena_submission/sample.xml`, c'est-à-dire à partir du XML
**d'origine du 22/08**, en n'y appliquant que les deux tables ci-dessus. Or :

- `build_ena_modify.py` écrase les champs listés et recopie tout le reste du XML de départ ; il ne
  compare jamais la colonne `valeur_deposee` à ce XML ;
- l'action MODIFY de l'ENA **remplace l'objet entier** ;
- la table `host subject id` touche les 727 échantillons biologiques.

Mesuré sur meso le 2026-10-06, sans soumission : la commande aurait ramené à leur valeur du 22/08
**4 612 champs sur 727 échantillons** — coordonnées, localité et date corrigées le 31/08 (727 ×
4), nom scientifique, nom commun et titre corrigés le 25/09 (568 × 3) — soit exactement l'état que
R28 avait vérifié le 30/09. Le « contrôle ponctuel » de la construction ne portait que sur les
deux champs modifiés et ne pouvait pas le voir. Deux défauts annexes : `--outdir ena_update`
écrasait le XML effectivement soumis le 31/08 ; et le mode `test` de `4_corriger_metadonnees.sh`
reconstruit **toujours** la table d'août, il ne validait donc pas les nouvelles valeurs.

**Règle** : ne plus utiliser `build_ena_modify.py` ni `4_corriger_metadonnees.sh` pour une
correction postérieure au 31/08. Toute nouvelle campagne part de l'**état déposé** et vérifie le
chaînage avant d'écrire, comme `scripts/28` (25/09) et `scripts/53` (06/10).

## Comment soumettre (procédure du 2026-10-06)

Les XML sont **déjà construits et vérifiés** par `scripts/53-ena_pertuis_sujet.py` (commit
`c650006`, sorties `6039d49`) :

| contrôle (bloquant) | résultat |
|---|---|
| base = XML du 25/09 (568 objets), sinon du 31/08 (159) ; accessions = reçus de production | 727 objets |
| base conforme au chaînage des tables soumises (l'état vérifié en direct par R28) | 4 612 / 4 612 |
| champs de la base différant de l'origine hors des tables soumises | aucun |
| `valeur_deposee` == base, pour chaque ligne des deux tables du jour | 771 / 771 |
| relecture : chaque objet écrit ne diffère de la base que sur les champs des tables | 727 / 727 |

Soumission de 727 échantillons (44 `collection date`, 727 `host subject id`) ; les 41 contrôles ne
sont pas envoyés. `ena_update_oct/sample.xml` md5 `e6488a371118e42d5fd704e1b45927cf` (MODIFY),
`ena_update_oct_test/sample.xml` md5 `d379e3218e98b94796e99db3df00b122` (ADD, alias suffixés
`_VAL101943`, sans accession).

Les identifiants Webin sont saisis au clavier et ne sont jamais écrits : **un humain lance le
script**, en session interactive sur la frontale (le script lit `/dev/tty`), depuis `ena_deposit/` :

```bash
cd ~/work/projects/microbiome-hybrid/ena_deposit

# 1. serveur de test : valide les VALEURS (checklist ERC000013), objets jetables
bash 10_corriger_pertuis_sujet.sh test

# 2. production, seulement si le test affiche « VALEURS VALIDEES » (taper OUI, puis identifiants)
bash 10_corriger_pertuis_sujet.sh prod

# 3. quelques heures plus tard : vérification exhaustive, les QUATRE tables dans cet ordre
bash 7_verifier_exhaustif.sh ena_corrections.tsv ena_corrections_hote_sept.tsv \
     ena_corrections_pertuis_dates.tsv ena_corrections_subject_id.tsv
# attendu : « LES 5339 VALEURS ATTENDUES SONT EN PLACE » (4 612 + 727 host subject id)
```

Un second test exige de reconstruire les XML (alias de test figés) : déplacer
`ena_update_oct{,_test}/` puis relancer `scripts/53`. En cas d'échec en production (transport ou
`success=false`), **ne pas relancer** : établir d'abord l'état du dépôt avec
`bash 7_verifier_exhaustif.sh` (sans argument : les deux tables soumises ; attendu si rien n'a changé :
« LES 4612 VALEURS ATTENDUES SONT EN PLACE »). **Ne pas utiliser `6_etat_du_depot.sh`** : il compare
le dépôt à la seule table d'août et, s'il conclut « non appliqué », propose de relancer
`4_corriger_metadonnees.sh prod`, qui renverrait le XML du 31/08 et annulerait les corrections du
25/09 sur 568 échantillons (constaté le 2026-10-06).

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
