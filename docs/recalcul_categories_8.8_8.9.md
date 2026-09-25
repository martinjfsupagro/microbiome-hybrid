# Recalcul des §8.8 et §8.9 : ce qui est périmé et ce qu'il faut recalculer

Vérification du 25 septembre 2026 du constat remonté par la conversation de rédaction. Destinée à la
conversation d'analyse, qui porte les scripts 17 à 24 et les matrices de distance.

## 1. Le constat est exact

- `metadata/analysis_metadata.csv`, colonne `categorie` : **180 individus sur 180 portent la
  classification d'août (12 chromosomes)**, 59 Cn / 30 Hy / 91 Pt. 164 seulement concordent avec
  septembre ; 16 changent de classe.
- Le §1 de `Article.docx` annonce « Cn (59 individuals), Hy (30) and Pt (91) ».
- Deux autres endroits portent les mêmes effectifs, non signalés : **la Table S1**
  (`table_S1_stations.csv` et `Supplementary_Data.docx`), colonne Cn / Hy / Pt par station et ligne
  Total « 59 / 30 / 91 » ; et **la Note S2** du supplément (« 91 *Parachondrostoma toxostoma*, 59
  *Chondrostoma nasus* and 30 hybrids »).

## 2. Composition par station : août, puis les deux passes décidées

| station | août (12 chr) | passe 2 : 42 Hy | passe 1 : 20 Hy | exclus en passe 1 | individus qui changent |
|---|---|---|---|---|---|
| Saint-Just-d'Ardeche | 8/3/8 | 9/6/4 | 9/1/4 | 5 | 5 |
| Rosieres | 0/4/21 | 0/7/18 | 0/1/18 | 6 | 3 |
| Manosque-Oraison | 0/2/13 | 0/5/10 | 0/1/10 | 4 | 3 |
| Confluence Buech-Meouge | 11/10/14 | 11/10/14 | 11/8/14 | 2 | 2 |
| Canal (usine du Largue) | 8/4/8 | 8/6/6 | 8/4/6 | 2 | 2 |
| Avignon | 20/4/0 | 19/5/0 | 19/2/0 | 3 | 1 |
| Chavannes-sur-Suran | 0/0/19 | 0/0/19 | 0/0/19 | 0 | 0 |
| Pont-d'Ain | 12/2/0 | 12/2/0 | 12/2/0 | 0 | 0 |
| Pertuis | 0/1/8 | 0/1/8 | 0/1/8 | 0 | 0 |

Lecture, en nuançant le constat d'origine :

- **Saint-Just est fortement modifié** : 8 / 3 / 8 devient 9 / 6 / 4, les toxostomes sont divisés par
  deux. En passe 1 il ne garde qu'**un seul hybride** et cesse d'être exploitable comme station à
  trois catégories.
- **Le canal du Largue l'est modérément** : 8 / 4 / 8 devient 8 / 6 / 6.
- **Rosières et Manosque changent davantage que le canal** (3 individus chacun, 4 → 7 et 2 → 5
  hybrides), mais ce sont des stations à deux catégories. Rosières compte : c'est le « témoin propre »
  du §8.9, la seule station où catégorie et position sont indépendantes.
- **Büech-Méouge a deux individus qui changent mais une composition identique** (11 / 10 / 14) : un
  hybride devient toxostome et un toxostome devient hybride. Les étiquettes individuelles changent,
  donc les tests aussi, même si les effectifs non.
- Suran (deux stations) et Pertuis sont inchangés.

## 3. La cible du recalcul n'est pas « les 42 », c'est les deux passes

La décision D1 du 25 septembre retient deux passes : 20 hybrides à génome intermédiaire avec les 22
quasi-purs **exclus** (n = 158), puis les 42 (n = 180). **La classification d'août ne correspond à
aucune des deux** : ses 30 hybrides contiennent les 20 intermédiaires plus 10 quasi-purs, ceux que les
12 premiers chromosomes détectaient déjà. Les résultats actuels portent donc sur une classe
intermédiaire entre les deux définitions retenues, et il faut recalculer deux fois — pas une.

Conséquence sur la phrase du §8.9 « three carry all three categories (74 individuals) » : elle reste
vraie en passe 2 (Büech 35 + canal 20 + Saint-Just 19 = 74), mais en passe 1 les trois stations ne
totalisent plus que 65 individus et Saint-Just n'y contribue qu'un hybride. Le sous-plan séparable
de 32 individus est aussi à recompter dans les deux passes.

## 4. Deux points du §8.8 que la rédaction doit connaître

**Le texte contredit la décision D2.** Le §8.8 et le §8.6 font entrer la colonne de plaque comme
covariable dans chaque modèle testant la catégorie. André a tranché le 25 septembre d'abandonner
l'effet position. Soit le texte est réécrit, soit la décision est rediscutée — ma recommandation
reste de sortir la position du modèle principal mais de garder en supplément une sensibilité qui
l'inclut, parce qu'elle est mesurée comme réelle dans les 24 strates.

**Le mécanisme que le §8.8 dit « non identifié » a maintenant une origine documentée.** Le texte
constate que la numérotation n'est pas aléatoire vis-à-vis du génotype. André l'explique : les hotus,
plus fragiles, sont prélevés en priorité, sauf une fois (Saint-Just). Et la plaque a été chargée
dans l'ordre de numérotation à cinq stations sur neuf (rho de Spearman de 0,87 à 0,95). Cela ne dit
pas si l'effet colonne vient de l'extraction ou du délai de dissection, mais cela explique pourquoi
colonne et catégorie sont associées.

**Le V de Cramér de 0,48 est à recalculer avec le reste.** Recalculé ici entre catégorie et colonne
de plaque : 0,505 avec les classes d'août au niveau individu (0,504 au niveau échantillon), 0,479
avec les 42 hybrides et 0,527 en passe 1. Je ne retrouve pas le 0,48 du texte avec les classes
d'août, qui sont celles des fichiers d'analyse : il a donc été calculé sur une autre unité ou un
autre sous-ensemble, que la conversation d'analyse connaît. La valeur proche obtenue avec les 42 est
une coïncidence, pas une confirmation. L'association reste forte dans les trois cas.

## 5. Liste de recalcul

1. régénérer `analysis_metadata.csv` avec la classe de septembre et une colonne de passe
   (`intermediaire` / `quasi-pur` / parental), à partir de `metadata/genotypes_verifies_sept_180.csv` ;
2. relancer les scripts de partition par catégorie, de PERMDISP et de position (20, 24, 17-18) **en
   deux passes** ;
3. recompter les stations à trois catégories, le sous-plan séparable et le témoin Rosières ;
4. mettre à jour le §1, les §8.8 et §8.9, la Table S1, la Table S8 et la Note S2 ;
5. rappel de D7 : tous ces chiffres dépendent encore du choix de métrique, qui reste ouvert.