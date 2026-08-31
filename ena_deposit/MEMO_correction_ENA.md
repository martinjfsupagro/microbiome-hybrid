# Correction des métadonnées ENA `PRJEB124417` — marche à suivre

Réponse à `GUIDE_correction_ENA.md`. Tout est prêt et vérifié sur meso dans
`~/work/projects/microbiome-hybrid/ena_deposit`.

---

## État du dépôt : le moment est favorable

Vérifié le 2026-08-31 : le portail public de l'ENA ne renvoie **rien** pour
`PRJEB124417` — ni runs, ni XML du projet, ni fiche d'échantillon (404). L'étude est
validée et enregistrée, mais **pas encore publique**.

C'est la meilleure configuration possible pour corriger : aucun tiers n'a pu moissonner
les coordonnées erronées, et la version corrigée sera la seule jamais exposée.

## Un écart avec le guide, assumé : patcher plutôt que régénérer

Le guide (§5.2, point 3) propose de régénérer `sample.xml` avec `build_ena_xml.py`
adapté. **Je n'ai pas fait cela**, pour une raison de sûreté.

L'action `MODIFY` **remplace l'objet entier** : tout attribut absent du XML soumis serait
effacé du dépôt. Régénérer depuis les sources fait dépendre 768 échantillons × ~15
attributs de la fidélité d'un script — dont le guide relève lui-même qu'il peut basculer
sur ERC000011 et écrire `not provided` si une coordonnée manque.

`build_ena_modify.py` part donc du **XML effectivement déposé et accepté par l'ENA**, et
n'y applique que les 3 472 différences de `ena_corrections.tsv`. Tout le reste est
préservé octet pour octet, par construction. Le script refuse de tourner si la table
contient un champ inattendu.

## Ce que la vérification a établi

La table de correction a d'abord été confrontée au dépôt réel :

| Contrôle | Résultat |
|---|---|
| Alias de la table présents dans le dépôt | 727 / 727 |
| Accessions `ERS` conformes au reçu de production | 727 / 727 |
| **Valeurs « déposée » conformes au XML réel** | **3 472 / 3 472, zéro discordance** |

Ce dernier point est le plus important : il prouve que la table décrit bien l'état réel
du dépôt, et non une hypothèse sur son contenu.

Puis le XML produit a été comparé au XML déposé, attribut par attribut :

| Contrôle | Résultat |
|---|---|
| Valeurs modifiées | 3 472, réparties sur exactement 5 champs |
| Changements **hors** de ces 5 champs | **0** (taxon, titre, jeu d'attributs intacts) |
| Contrôles (41) | inchangés, sans accession ajoutée |
| Accessions `ERS` posées sur les modifiés | 727 / 727 |

Enfin, les sept contrôles du §6 du guide passent tous, y compris les deux qui comptent
vraiment : les **deux stations du Suran ont des latitudes distinctes** (46.048 et
46.264389), et l'extrapolation `45.906458` a **totalement disparu**.

Les valeurs corrigées ont aussi été validées contre les **regex officiels d'ERC000013**
récupérés à l'instant : 727 latitudes, 727 longitudes et 727 dates, **zéro refus** —
l'intervalle `2014-07-07/2014-08-20` de Pertuis inclus, que le regex de date accepte.

## Les trois décisions du §4

### 4.1 Pertuis — l'intervalle est en place, mais c'est un choix par défaut

Les 44 échantillons portent `2014-07-07/2014-08-20`, format ISO 8601 accepté par l'ENA.
**Techniquement valide, mais c'est une perte d'information** : si André peut assigner les
individus à l'une des deux sorties, cela vaut mieux. La correction est alors une édition
de `ena_corrections.tsv` puis une régénération — pas de retour en arrière nécessaire.

Le script accepte `--drop-undecided` pour exclure ces 44 dates et corriger le reste
maintenant, si vous préférez ne pas figer un intervalle.

### 4.2 Nom d'hôte hybride — devrait passer

Vérifié dans la définition du checklist ERC000013 : `host_scientific_name` est
**optionnel, en texte libre**, sans regex ni vocabulaire contrôlé, et n'est pas un champ
taxonomique. L'option (a) du guide — `Chondrostoma nasus x Parachondrostoma toxostoma`,
122 échantillons — est donc légitime. Le serveur de test confirmera.

Une piste si vous voulez rendre le statut hybride exploitable par machine : ERC000013
définit aussi `host_genotype` et `host_subspecific_genetic_lineage`. Ajouter
`host genotype` = `Cn`/`Hy`/`Pt` en complément coûterait une colonne dans la table de
correction. À voir avec André — ce n'est pas nécessaire pour publier.

### 4.3 Alias avec coquille — d'accord avec le guide

`DURANCE16S_15Per2015Ch03A` garde son alias. Ses attributs sont corrigés, dont la date
qui passe de `2015` à la valeur 2014. Un alias est un identifiant, pas une donnée.

## La procédure

```bash
cd ~/work/projects/microbiome-hybrid/ena_deposit

# 1. Test — valide le format, les regex et le nom d'hôte hybride
bash 4_corriger_metadonnees.sh test

# 2. Production
bash 4_corriger_metadonnees.sh prod

# 3. Vérification, quelques heures plus tard
bash 5_verifier_correction.sh
```

### Ce que le serveur de test peut, et ne peut pas, valider

Deux tentatives ont été nécessaires pour l'établir, le 2026-08-31.

**Tentative 1 — `MODIFY` des accessions de production.** Rejet : 769 erreurs, toutes
`No new BioSample was created for sample with alias …`, pour les **768** échantillons, y
compris les 41 contrôles qui ne portent aucune accession. Refus uniforme, donc sans
rapport avec l'attribut `accession`.

**Tentative 2 — `ADD` des échantillons corrigés, sans accession.** Rejet : 768 erreurs
`The object being added already exists in the submission account with accession
"ERS31168048"` — et `ERS31168048` est l'accession de **production** de cet alias.

Ces deux échecs, mis côte à côte, disent la même chose : **wwwdev partage le registre
d'alias du compte soumettant avec la production, mais pas les enregistrements
BioSamples.** D'où l'impasse : un `ADD` bute sur l'alias déjà pris, un `MODIFY` bute sur
l'objet BioSamples absent. Aucune des deux voies ne valide quoi que ce soit sur les alias
réels.

**La solution retenue** : soumettre les échantillons corrigés sous des **alias suffixés**
(`_VAL<horodatage>`), qui n'entrent en collision avec rien. Les objets créés sont jetables
et détruits sous 24 h. Cela valide ce qui est validable — les **valeurs** contre le
checklist ERC000013, les regex des coordonnées et des dates, et l'acceptation du nom
d'hôte hybride sur les 122 échantillons concernés.

Ce que ce test ne couvre pas : la mécanique du `MODIFY` elle-même, non testable sur
wwwdev. En production, elle est couverte par le contrôle des accessions du reçu.

**Une leçon de méthode au passage.** Ma première version du script concluait « les VALEURS
sont refusées — c'est un vrai problème de données » sur une erreur `already exists`, qui ne
porte pas du tout sur les données. Un script qui interprète un échec doit distinguer les
erreurs de contenu des erreurs d'existence ; la version actuelle les sépare explicitement
et le dit dans sa sortie.

**Le garde-fou principal** est dans l'analyse du reçu : le script compare chaque accession
retournée à celle du reçu de production. Si une seule diffère, c'est qu'un `ADD` a eu lieu
au lieu d'un `MODIFY` — il s'arrête avec un code d'erreur et vous dit de ne pas relancer.

## Ce qui ne bouge pas

Les 4 608 fichiers FASTQ, les 2 304 objets EXPERIMENT et RUN, les accessions `ERR`/`ERX`,
les alias, les taxons d'échantillon (`fish metagenome` etc.) et les 41 contrôles. Aucun
retransfert : seule la partie SAMPLE est renvoyée.

## Après la correction

`Supplementary_Data.docx` (Table S1) et `DATA_AVAILABILITY.md` portent encore les
**anciennes coordonnées et les anciens noms de rivière**. Ils devront être régénérés
depuis `metadata/station_reference.csv`. La Table S1 du guide
(`docs/manuscrit/table_S1_stations.csv`) est déjà à jour et servira de source.

C'est le point à ne pas oublier : corriger l'ENA sans corriger le manuscrit laisserait
une incohérence entre l'article et le dépôt qu'il cite.
