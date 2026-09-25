# Correction de l'identité d'hôte — dépôt ENA `PRJEB124417` (classification à 25 chromosomes)

2026-09-25. Préparé et vérifié sur meso ; **la soumission demande les identifiants Webin et doit
être lancée par un humain**, dans un terminal (les scripts lisent l'identifiant et le mot de passe
sur `/dev/tty`, ils ne sont jamais écrits).

## Pourquoi

- La correction `MODIFY` du 2026-08-31 a posé `host scientific name` selon la classification
  d'**août** (12 chromosomes). Le génotypage de septembre (25 chromosomes) en change 16 individus,
  soit **63 échantillons** : 51 Pt → Hy, 4 Cn → Hy, 4 Hy → Pt, 4 Hy → Cn.
- Cette correction n'avait touché **ni le titre ni `host common name`**, restés à l'identification
  morphologique : 531 échantillons disaient « Chondrostoma sp. », et 33 avaient un titre
  contredisant leur nom scientifique (par ex. un hybride titré « Chondrostoma nasus »).

## Ce qui est soumis

`scripts/28-ena_hote_sept.py` part du XML **effectivement déposé** (`ena_update/sample.xml`, soumis
le 31/08 à 21:16) et n'y change que trois champs, sur **568 échantillons** :

| champ | échantillons modifiés |
|---|---|
| TITLE (préfixe hôte) | 568 |
| host common name | 568 |
| host scientific name | 63 |

État final attendu sur les 727 biologiques : 236 *C. nasus*, 322 *P. toxostoma*, 169 hybrides.
Ne sont **pas** soumis : les 41 contrôles et les 159 échantillons déjà corrects. Accessions, alias,
fichiers, EXPERIMENT et RUN sont inchangés.

`host common name` des hybrides = **`nasus x toxostoma`** (décision JF Martin, 2026-09-25 ; aucun
nom commun n'existait pour eux). Parentaux : `nase`, `toxostome`.

## Contrôles déjà passés (sans soumission)

- Témoin : les 727 noms scientifiques déposés sont **exactement** la classification d'août ;
  s'ils ne l'étaient pas, le script refuse d'écrire (l'état déposé serait inconnu).
- Toutes les accessions `ERS` concordent avec le reçu de production du 31/08.
- Relecture du XML produit : chaque échantillon ne diffère du dépôt **que** sur les champs de la
  table `ena_corrections_hote_sept.tsv` (1 199 lignes), valeurs conformes.
- Le vérificateur `9_verifier_hote_sept.sh`, simulé hors ligne : 0 écart sur un dépôt corrigé,
  exactement 1 199 écarts « valeur INITIALE » sur le dépôt actuel (contrôle négatif).
- 10 échantillons ont un `original sample name` avec espace ou `_` là où l'alias porte `-`
  (`14Per2011Ch01A_bis`, `14Avi1037 01A`…) : appariement par alias, vérifié explicitement.

## Procédure

```bash
cd ~/work/projects/microbiome-hybrid/ena_deposit

# 1. Test : valide les valeurs contre ERC000013 (objets jetables, alias suffixés)
bash 8_corriger_hote_sept.sh test

# 2. Production (demande de taper OUI)
bash 8_corriger_hote_sept.sh prod

# 3. Quelques heures plus tard : vérification exhaustive des 727
bash 9_verifier_hote_sept.sh
```

Le script de production s'arrête **sans relancer** si une seule accession du reçu diffère (ce
serait un ADD au lieu d'un MODIFY), et sur échec de transport il indique que l'état est
indéterminé : ne pas relancer à l'aveugle, lancer `bash 6_etat_du_depot.sh`.

## Points toujours ouverts, non traités ici

- Pertuis : dates déposées en intervalle `2014-07-07/2014-08-20`, assignation par individu inconnue.
- `host subject id` non unique entre campagnes (24 paires) : table
  `ena_corrections_subject_id.tsv` prête depuis le 31/08, jamais soumise, décision en attente.


---

## État au 2026-09-25 18:09 — soumis en production

| étape | résultat |
|---|---|
| test (wwwdev) 18:05–18:07 | **non concluant** : deux réponses vides, puis `success=false` avec 568 × « No new BioSample was created » et « Failed to submit samples to BioSamples ». Le test n'a rien validé. |
| production 18:08 | `success=true`, 0 erreur, 0 avertissement ; 568/568 alias et accessions identiques au XML soumis → MODIFY, aucune création |
| vérification exhaustive | **à faire** : `bash 9_verifier_hote_sept.sh`, quelques heures après |

Le test a échoué sur des alias neufs (suffixe `_VAL180214`), en ADD, avec le même mécanisme qui avait
fonctionné le 31/08 : l'hypothèse la plus simple est une indisponibilité du service BioSamples
de test, mais elle **n'est pas établie** (le message de commit `01cd77d` l'affirme à tort comme un
fait). Ce qui compte : la production valide elle aussi contre ERC000013 et n'a renvoyé aucune
erreur. L'application effective des valeurs reste à confirmer par la vérification.

Reçus : `receipt_hote_sept_prod_20260925_180826.xml` (+ `_accessions.tsv`),
`receipt_hote_sept_test_20260925_180605.xml`.
