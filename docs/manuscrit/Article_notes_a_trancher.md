# Article.docx — notes éditoriales restantes

**7 notes** en gris italique 9 pt dans `Article.docx`, à trancher avant soumission.
Elles ne font pas partie du texte de l'article et doivent être supprimées une fois
résolues. Trois catégories, par ordre de gravité décroissante.

---

## À COMPLÉTER — 2 notes, contenu manquant

| § | Ce qui manque |
|---|---|
| **8.6** Normalization of sequencing effort | Modèles statistiques : structure des effets aléatoires (séquençage niché dans la préparation de librairie, cf. §8.7), PERMANOVA et PERMDISP, méthode d'abondance différentielle, contrôles |
| **9** Reproducibility and data availability | Lien vers le dépôt de code (git) et, le cas échéant, DOI Zenodo de la version utilisée |

Ces deux notes signalent du texte à **écrire**. Le §8.6 est le plus lourd : il décrit
les analyses statistiques, donc il dépend des analyses effectivement retenues.

## À CONFIRMER — 1 note, incohérence de données

| § | Point à vérifier |
|---|---|
| **1** Study system and sampling | Effectifs par site et par année : le tableau de génotypage fait état de **181 individus** contre **156** représentés dans les données déposées (cf. note sous Table S1) |

Écart attendu si le génotypage couvre des poissons non séquencés en 16S, mais non vérifié.
À trancher avec André.

## Transposé du manuscrit d'origine — 4 notes, à confirmer pour le lot Durance

Ces passages ont été repris d'un manuscrit antérieur de la même équipe sur le même
protocole. Ils sont probablement exacts, mais **aucun n'a été confirmé pour ce lot
d'échantillons** : ils décrivent des opérations de terrain et de laboratoire que seul
un participant peut valider.

| § | Contenu transposé |
|---|---|
| **1** Study system and sampling | Mode de capture (pêche électrique), euthanasie par dislocation cervicale, numéros d'autorisation |
| **2** Tissue sampling and preservation | Conservation en éthanol 95 % à −80 °C, dissection stérile — décrit pour 2 tissus dans le manuscrit d'origine, étendu ici aux 4 tissus |
| **3** DNA extraction, library preparation | Kit Qiagen Food Mericon, dual-index Kozich (2013), protocole Galan (2016), quantification Kapa, MiSeq v3 (2×300) |
| **4** Controls | Standard ZymoBIOMICS (8 taxons bactériens connus), inclusion de contrôles négatifs et mock |

### Le §3 mérite une attention particulière

Le texte affirme : *« loaded on an Illumina MiSeq flow cell with reagent kit v3
(2 × 300 cycles) »*. Or les lectures des trois runs mesurent **251 pb** — vérifié
directement sur les fichiers déposés — et le M&M lui-même s'appuie sur cette valeur en
plusieurs endroits (« 2×251 bp reads » au §5.3, « within a 251 bp read » au §5.2).

Une chimie 2×300 produit des lectures de 300 pb, pas de 251. Le protocole Kozich et al.
(2013) utilise le kit **v2 500 cycles** (2×250), ce qui correspond exactement aux données.
L'affirmation « v3 (2 × 300 cycles) » est vraisemblablement une transposition erronée du
manuscrit d'origine.

À vérifier sur les fiches de run (`RunParameters.xml` des dossiers de séquençage) et à
corriger dans le §3. Ce point n'affecte ni le dépôt ni les analyses, mais un relecteur
attentif le relèvera.

---

## Points résolus (aucune action)

- **Structure de réplication** : tranchée par le §8.7 du M&M — deux préparations de
  librairie, la seconde séquencée deux fois. Les paragraphes de disponibilité des
  données sont rédigés en conséquence.
- **Coordonnées des 9 sites** : fournies par André, vérifiées par géocodage, intégrées
  (Table S1).
- **Dépôt ENA** : `PRJEB124417`, 2 304 runs, zéro échec.

## Point d'inexactitude signalé, hors note

Le §3 affirme « Plate layout and i7 indices were identical throughout ». Les données le
contredisent : entre les deux préparations, l'i7 change pour **384 des 768** librairies
et l'i5 pour 576, l'ensemble des couples restant le même. Formulation suggérée :

> *The same set of 768 index combinations was used for both library preparations, but
> index-to-well assignment differed between them.*

Ce point n'est pas balisé par une note dans le document — il figure ici et dans
`Supplementary_Data.docx` (Table S4).
