# Les cinq individus sans Q-values sur le foie — réponse d'André et décision

Source : réponses d'André du **2026-09-30**, en retour de `pour_andre_questions_ouvertes.md`.
Les valeurs du tableau citées ci-dessous sont relues depuis
`metadata/genotypes_verifies_sept_180.csv`, pas depuis une note.

## Ce qu'il répond

Les Q-scores sont calculés sur le foie, indisponible pour ces cinq individus. Leur identification
vient donc d'ailleurs, et les deux voies sont différentes.

**Trois individus ont été ajustés sur les deux autres tissus, et les deux ajustements concordent.**
André fournit les valeurs par tissu :

| individu | midgut : médiane / D | caudale : médiane / D |
|---|---|---|
| `15Bue1014` | 0,0001 / 0,0431 | 0,0001 / 0,0117 |
| `15Cab1011` | 0,0001 / 0,0100 | 0,0001 / 0,0382 |
| `15Jus1008` | 0,0288 / 0,0577 | 0,0001 / 0,0104 |

**Deux individus n'ont aucune trace de Q-values.** `14Bue1001` et `14Bue1002` portent les valeurs
trouvées par Arnaud avec une autre méthode, assez proche ; ce sont bien des *C. nasus*, mais sans
trace exploitable. André tranche : **NA** pour la médiane et le D de ces deux individus, « pour que
tout soit propre ».

## Ce que la concordance établit, et ce qu'elle n'établit pas

**Elle établit la classe.** Sur les trois individus ajustés, les six valeurs de D vont de 0,0104 à
0,0577, toutes sous le seuil de 0,12 qui sépare un parental d'un hybride, et les médianes sont
toutes sous 0,05. Les deux tissus classent donc les trois individus en `Pt`, et le désaccord était
possible : un D au-dessus de 0,12 sur l'un des deux tissus les aurait fait basculer en `Hy`. Le D
le plus élevé atteint la moitié du seuil. La classification de ces trois individus est confirmée
par une source indépendante du foie.

**Elle n'explique pas les valeurs du tableau.** C'était la question posée, et elle reste ouverte.
Les valeurs actuellement portées par `genotypes_verifies_sept_180.csv` ne correspondent **ni** à
l'ajustement sur midgut, **ni** à celui sur caudale :

| individu | tableau (fichier vérifié) | midgut | caudale |
|---|---|---|---|
| `15Bue1014` | **0,001655 / 0,00** | 0,0001 / 0,0431 | 0,0001 / 0,0117 |
| `15Cab1011` | **0,000424 / 0,00** | 0,0001 / 0,0100 | 0,0001 / 0,0382 |
| `15Jus1008` | **0,045519 / 0,01** | 0,0288 / 0,0577 | 0,0001 / 0,0104 |

Les médianes diffèrent d'un facteur 10 à 450 pour les deux premiers, et le D du tableau vaut 0,00
alors que les deux ajustements donnent des valeurs strictement positives dans les six cas. Ce ne
sont donc pas des arrondis. La provenance des cellules du tableau pour ces trois individus n'est
pas établie.

## Décisions

1. **`14Bue1001` et `14Bue1002` : médiane et D à NA**, conformément à la réponse d'André. Ces deux
   individus restent classés `Cn` ; c'est la classe qui est documentée, pas l'index.
2. **`15Bue1014`, `15Cab1011`, `15Jus1008` : les valeurs du tableau ne doivent pas être publiées
   telles quelles**, leur provenance n'étant pas établie. **Tranché par JF le 2026-09-30** : publier les deux
   ajustements en nommant le tissu, plutôt que d'en choisir un — aucun des deux n'est le foie, et
   n'en montrer qu'un masquerait que le génotype de ces trois individus repose sur deux ajustements
   hors foie qui concordent.
3. **Le tissu de génotypage est le foie**, cinquième tissu absent du jeu microbiote. Écrit au §1 de
   `Article.docx`, désormais avec le détail des deux voies de secours.

## Portée analytique : nulle

`index_mediane_andre` et `delta_mediane_quart` sont écrits dans `analysis_metadata.csv` par
`19-analysis_metadata.py` mais **ne sont consommés par aucun script d'analyse** (vérifié par
recherche dans `scripts/` et `docs/recalcul/`). Les analyses portent sur `categorie`, qui ne change
pas. Le passage à NA est donc éditorial et ne déplace aucun résultat.

Aucune table du supplément ne publiait la médiane et le D par individu : les Tables S1 à S9 ne
contiennent pas de tableau de génotypage individuel. La décision portait donc sur une table à
produire, et cette table est maintenant produite —
`docs/manuscrit/table_genotypes_individuels.csv`, 180 lignes, l'arbitrage y étant appliqué
colonne par colonne : index et D du foie pour les 175, colonnes par tissu pour les trois ajustés
avec `median_index`/`D` laissés vides, tout vide pour les deux sans trace. Son numéro de table et
son insertion dans `Supplementary_Data.docx` reviennent à la session de rédaction.

**Défaut de ma première version de cette table, corrigé.** La colonne `river` avait été reprise
de `genotypes_verifies_sept_180.csv`, qui porte l'assignation de rivière antérieure aux réponses
d'André du 30 août : 113 des 180 individus recevaient une rivière fausse — le canal du Largue
donné en Durance (20 individus), les deux stations du Suran en Ain (33), le Büech en Durance (35)
et la Beaume en Ardèche (25) — et 19 de plus ne différaient que par l'accent de « Ardèche ». La
colonne est désormais sourcée depuis `metadata/station_reference.csv`, la seule référence qui
fasse foi, avec contrôle que les 180 lignes concordent après correction. Rien d'autre dans la
table n'était touché : catégories, types de génome et valeurs de génotypage étaient corrects.
