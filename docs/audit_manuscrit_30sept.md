# L'Article est-il à jour des décisions et des résultats ?

Audit du 2026-09-30 sur `docs/manuscrit/Article.docx` **lu depuis le cluster**
(commit `c2c1171`, md5 `c78d9ea3d2194319dc3d346f612d57ac`, 86 paragraphes, 51 656 caractères),
confronté à `_etat/DECISIONS.md`, `_etat/RESULTATS.md` et aux données.

**Verdict : à jour sur les sept décisions de design et sur les résultats de composition. Six
écarts subsistent, dont deux sont des affirmations fausses portées par le document lui-même.**

---

## Ce qui est à jour

| élément | où | contrôle |
|---|---|---|
| D1 — hybride = 42, deux passes (158 / 180) | §1, §8.6 | passes définies au §1 et invoquées au §8.6 |
| D2 — position hors modèle principal, en sensibilité | §8.6, §8.8, §8.9 | les deux versions rapportées, 7 cellules sur 16 diffèrent |
| D3 — 180 individus, tous les sites | §1 | 180 / 156 expliqués |
| D5 / D6 — quatre tissus conservés | §2 | caudale, midgut, hindgut, branchie |
| D7 — règle d'assertion | §8.6 | écrite le 30/09 |
| Génotypage 25 chromosomes, 59 / 42 / 79 | §1 | conforme à `genotypes_verifies_sept_180.csv` |
| Les cinq individus sans foie, deux voies distinctes | §1 | conforme à la réponse d'André du 30/09 |
| Stations d'André, Suran à deux stations, 25,4 km | §1 | conforme à `station_reference.csv` |
| Structure de réplication nichée | §3, §8.7 | conforme à R7 |
| Raréfaction 3 000, sensibilité 500, biais de sélection en deux passes | §8.6 | conforme à R9 et au registre |
| Effet de position et ses trois témoins, en deux passes | §8.8 | conforme au recalcul du 25/09 |
| Partition de variance et PERMDISP, deux passes × quatre métriques | §8.9 | conforme à R23 et R27 |
| Financement EDF / FACIES | Funding | ajouté le 30/09 |

**Deux contrôles qui auraient pu échouer et n'échouent pas.** « Nine of the 49 individuals
previously identified on morphology were reclassified » : recalculé sur les données,
**9 sur 49** exactement (6 Cn→Hy, 2 Pt→Hy, 1 Cn→Pt). Et le chiffre de 18,7 % de variance
tissulaire, calculé sur la richesse observée et resté `préliminaire` (R8), **n'apparaît nulle
part dans le manuscrit** — le texte cite les 9,2 % issus de la PERMANOVA Bray-Curtis du §8.7.
La métrique écartée n'a pas fui dans le texte.

---

## Les six écarts

### 1. Deux notes éditoriales du document affirment des choses fausses

C'est le plus grave, parce qu'une note fausse oriente la prochaine session.

**Note (iv)** : « Les paramètres a priori du 4H (seuil de core, rang taxonomique) ne sont pas
encore fixés ». **Ils le sont** — D5, le 25 septembre : ρ = 0,5 au rang du genre, sensibilité sur
ρ ∈ {0,3 ; 0,5 ; 0,7}, ϑ = ε = 0. Ce qui manque n'est pas la décision mais sa description au §8.6.

**Note (v)** : « "near-parental genome introgressed on a single chromosome" n'est pas vérifiable
sur `genotypes_verifies_sept_180.csv`, qui ne porte pas les assignations par chromosome ».
**Le fichier porte une colonne `n_chromosomes_introgresses`**, et elle donne, sur les 22
quasi-purs : **17 introgressés sur un chromosome, 4 sur deux, 1 sur six**. L'affirmation est donc
vérifiable, et la note doit être remplacée par le chiffre.

### 2. L'introduction généralise ce que les données donnent pour 17 des 22

Le §5 de l'introduction écrit « a near-parental genome introgressed on a single chromosome »
comme si c'était le cas de tous les quasi-purs. C'est vrai de 17 sur 22. Formulation à corriger,
par exemple « introgressed on one or a few chromosomes — a single one in 17 of the 22 ».

### 3. Le §9 ignore la correction ENA du 25 septembre

Il ne mentionne que celle du 31 août et conclut « PRJEB124417 is up to date ». Manquent la
correction d'identité d'hôte du 25/09 — 568 échantillons, 1 199 champs, alignée sur la
classification à 25 chromosomes, hybrides en `nasus x toxostoma` — et sa vérification exhaustive
du même jour : 727 échantillons interrogés, 1 199 champs conformes, 0 non conforme. R26 est
`validé` au registre ; le manuscrit l'ignore.

### 4. Le §9 se contredit sur la résolution des dates

Le paragraphe 80 dit que la correction du 31 août portait sur les « exact collection dates » ; le
paragraphe 81 dit « Collection dates are given at year resolution ». Les deux ne peuvent pas être
vrais. Les dates sont au jour près depuis le 31 août, à l'exception de Pertuis, déposé en
intervalle — et dont l'assignation est désormais décidée (série 1011-1014 au 07/07/2014, série
2011-2015 au 20/08/2014) mais **pas encore soumise**.

### 5. « 25 empty wells » au §9 contre « 75 empty wells » aux §4 et §8.2

Le dépôt porte **25 puits vides**, chacun séquencé dans les trois runs, soit 75 échantillons —
et 67 d'entre eux ont retenu au moins une lecture, ce que le §8.2 rapporte correctement. Le §4
applique pourtant à ces puits la convention inverse de celle qu'il applique aux blancs, où il
distingue explicitement 4 puits et 12 échantillons. À harmoniser : 25 puits, 75 échantillons.

### 6. Le §3 porte toujours une chimie incompatible avec les lectures, sans note

« reagent kit v3 (2 × 300 cycles) » alors que les §5.2 et §5.3 reposent sur des lectures de
251 pb et que le protocole de Kozich et al. utilise le kit v2 500 cycles. Le point est consigné
dans `Article_notes_a_trancher.md`, mais **aucune note grise ne le signale dans le document**,
alors que les quatre autres transpositions de 2017 en portent une.

---

## Ce qui n'est pas un écart mais une attente déclarée

- **Le 4H n'a pas de section Methods.** L'introduction l'annonce comme analyse complémentaire,
  le §8.6 ne le décrit pas. Ce n'est pas une incohérence tant que l'analyse n'est pas lancée —
  elle est le prochain calcul de la passation — mais l'introduction promet une méthode que les
  Methods ne décrivent pas encore. À écrire en même temps que le calcul.
- **§2, §3, §4 restent transposés du manuscrit de 2017**, chacun sous sa note grise, en attente
  d'André. C'est déclaré, donc conforme.
- **D2 dans sa part ouverte** : le manuscrit rapporte les deux versions et compte les cellules
  qui diffèrent. C'est un état intérimaire défendable, pas une décision. Il reste à arbitrer ce
  que le texte affirme.
- **Titre de l'article absent**, note (i). Cible éditoriale non confirmée.
