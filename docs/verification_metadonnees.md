# Métadonnées durance1/2/3 — points à vérifier

Note à l'intention de la personne qui a acquis les données.
Projet `microbiome-hybrid`, état au 19 juillet 2026, commit `6b9d996`.

Les métadonnées des trois runs MiSeq ont été reconstruites à partir des
SampleSheet et des noms de fichiers. Tout est décodé sans exception, mais
**41 librairies sur 768 reposent sur une interprétation** qu'il faut confirmer,
et une correspondance importante n'est établie que par déduction.

Le détail ligne à ligne est dans `a_verifier.csv`, avec une colonne `reponse`
laissée vide à remplir.

---

## Ce qui a été établi

Les trois lots sont **le reséquençage des mêmes 768 librairies** : mêmes noms,
même plan de plaque, mêmes index i7 ; seuls les i5 et la flowcell changent.

| Lot | Run | Flowcell |
|---|---|---|
| durance1 | M03930_0062 | BBHKV |
| durance2 | M03930_0069 | BCFFD |
| durance3 | M03930_0072 | BFWT5 |

Merci de confirmer que c'est bien voulu — trois passages de la même plaque, et
non trois jeux d'échantillons distincts. C'est une bonne nouvelle pour
l'analyse (l'effet run devient estimable et n'est confondu avec aucun facteur
biologique), mais ça change complètement la lecture du plan.

À noter : **durance2 a été livré sans SampleSheet**, seulement des fastq
renommés, décompressés, avec les témoins dans un sous-dossier `control/`. Ses
métadonnées sont donc reconstruites depuis les noms de fichiers, et ses
colonnes de plaque et d'index sont vides. Si la SampleSheet d'origine existe
quelque part, elle est la bienvenue.

---

## 1. Taxon jamais saisi — 8 individus, 31 échantillons

À Ain en 2014, les individus **1036 à 1043** portent une espace là où devraient
figurer les deux lettres du taxon :

```
14Ain1036 01A       au lieu de       14Ain1036Cn01A
```

Les 8 individus se suivent et les 4 tissus de chacun sont concernés : c'est un
bloc de saisie entier où le taxon manque, pas des oublis isolés.

Le taxon n'est pas récupérable depuis le reste du fichier :

- aucun des 4 tissus d'un même individu ne le porte, donc rien à propager ;
- Ain 2014 contient **les deux espèces** — hotu (individus 1001–1002) et
  toxostome (1011–1014) — donc le site ne le donne pas ;
- ces 8 individus forment une **troisième série de numéros** (1036–1043) qui
  n'apparaît nulle part ailleurs dans le jeu de données.

C'est ce dernier point qui rend la question importante plutôt que cosmétique :
une série de numéros distincte, sur le seul site où les deux parents
coexistent, ressemble beaucoup à un groupe à part. **S'agit-il des hybrides ?**

→ *Il faut la feuille de terrain. Ces 31 échantillons sont inutilisables tant
que leur statut n'est pas tranché, et ce sont peut-être les plus intéressants.*

---

## 2. Code tissu `04` — 1 échantillon

`15Avi1002Cn04A` est le seul échantillon en code tissu `04` ; tous les autres
utilisent `01`, `02`, `03` ou `05`. Il est présent à l'identique dans les trois
runs, ce n'est donc pas une erreur de transcription d'un seul lot.

Les positions sur plaque désignent une faute de frappe : l'échantillon est en
**plaque 4, puits B09**, encadré sans discontinuité par des tissus `05`.

```
  B05  15Jus1009Ch05A    05
  B06  15Jus1017Ch05A    05
  B07  15Caa1006Ch05A    05
  B08  15Caa1014Ch05A    05
  B09  15Avi1002Cn04A    04   ← ici
  B10  15Avi1010Cn05A    05
  B11  15BUe1005Ch05A    05
```

→ *`04` est-il bien une faute de frappe pour `05` ? Rien n'a été corrigé dans
les fichiers en attendant la réponse.*

---

## 3. Ré-extractions `bis` — 9 tissus

Neuf tissus portent le suffixe `bis`, compris comme une **seconde extraction
d'ADN du même tissu**. Ils sont traités comme des réplicats d'extraction et non
comme des réplicats de run, ce qui les distingue de leur extraction initiale
dans les analyses.

→ *Merci de confirmer qu'il s'agit bien à chaque fois du même tissu, et non
d'un second prélèvement sur le même poisson.* La liste est dans
`a_verifier.csv`.

Deux cas avaient un suffixe abîmé, déjà résolus mais signalés pour information :

- dans les fastq de durance2 le séparateur est `-bis` au lieu de `_bis`
  (conversion Illumina, sans conséquence) ;
- **`14Bue1006Cn05A` apparaît deux fois dans la SampleSheet de durance1**, en
  B07 et C07. durance2 et durance3 appellent celui de C07
  `14Bue1006Cn05Abis` : le suffixe a sauté à la saisie de durance1. Le puits
  étant le même dans les trois runs, le nom a été rétabli.

---

## 4. Correspondance code tissu ↔ tissu — déduite, non documentée

Aucun document du projet ne dit à quel tissu correspondent les codes `01`,
`02`, `03` et `05`. Le plan de plaque la donne pourtant : les librairies sont
rangées en quatre blocs de 192, un par tissu, et **chaque bloc contient un
blanc nommé explicitement**.

| Bloc (sample_id) | Code tissu | Blanc dans le bloc | Tissu déduit |
|---|---|---|---|
| 1–192 | `01` | `Blanc-Caudal` (id 71) | caudale |
| 193–384 | `05` | `Blanc-Branchie` (id 263) | branchie |
| 385–576 | `03` | `Blanc-Hindgut` (id 455) | hindgut |
| 577–768 | `02` | `Blanc-Midgut` (id 635) | midgut |

La correspondance est cohérente sur les quatre blocs sans exception. Elle
reste néanmoins une **déduction à partir du plan de plaque**, pas une donnée
documentée, et elle n'a donc pas été écrite dans les scripts.

→ *Est-ce bien : `01` = caudale, `02` = midgut, `03` = hindgut,
`05` = branchie ?* Une confirmation débloque l'ensemble des analyses par
tissu.

Accessoirement, cette lecture renforce le point 2 : l'échantillon `04` tombe
au milieu du bloc branchie.

---

## Récapitulatif des questions

1. Les trois runs sont-ils bien trois séquençages de la même plaque ?
2. La SampleSheet de durance2 existe-t-elle quelque part ?
3. Quelle espèce pour les individus 1036–1043 d'Ain 2014 — et forment-ils un
   groupe à part (hybrides) ?
4. Le code tissu `04` de `15Avi1002Cn04A` est-il une faute de frappe pour `05` ?
5. Les 9 `bis` sont-ils bien des ré-extractions du même tissu ?
6. `01` = caudale, `02` = midgut, `03` = hindgut, `05` = branchie ?
