# Ce qui reste à obtenir d'André

État au **2026-09-30**. Les trois points ouverts ont reçu une réponse ; **deux sont clos**, un
reste partiellement ouvert. Le détail du point 1 est dans `docs/decision_individus_sans_qvalues.md`.

## 1. Les cinq individus sans foie — CLOS, avec une réserve

**Réponse.** Trois individus (`15Bue1014`, `15Cab1011`, `15Jus1008`) ont été ajustés sur le midgut
et sur la caudale, et les deux ajustements concordent : toutes les valeurs de D vont de 0,0104 à
0,0577, sous le seuil de 0,12, donc les trois sont `Pt` par les deux voies. Deux individus
(`14Bue1001`, `14Bue1002`) portent des valeurs obtenues par Arnaud avec une autre méthode et
n'ont aucune trace de Q-values : André tranche **NA** pour leur médiane et leur D.

**Réserve.** Les valeurs actuellement dans le tableau pour les trois premiers ne correspondent ni à
l'ajustement sur midgut ni à celui sur caudale — les médianes diffèrent d'un facteur 10 à 450 et le
D du tableau vaut 0,00 là où les deux ajustements donnent des valeurs positives. Leur provenance
reste inconnue. Décision à prendre par JF avant de publier une table de génotypage individuelle :
publier les deux ajustements en nommant le tissu, ou ne rien publier.

## 2. Les sections de protocole — PARTIELLEMENT OUVERT

**Ce qui est réglé : le financement.** André confirme que le contrat est le même que celui de 2017,
soit EDF via le projet FACIES avec l'appui de la Fédération de l'Ain. Une section *Funding* est
ajoutée à `Article.docx`. Restent à compléter la référence exacte du contrat et le nom légal complet
de la Fédération, à reprendre des remerciements de Guivier et al. (2017).

**Ce qui reste ouvert : les trois sections elles-mêmes.** La réponse ne porte que sur le
financement ; les protocoles transposés du manuscrit de 2017 ne sont toujours pas confirmés pour le
lot Durance 2014-2015 :

| section | à confirmer |
|---|---|
| §2 capture, euthanasie, autorisations | protocole et numéros d'autorisation pour 2014-2015 |
| §3 extraction et librairies | kit, version, protocole d'indexation réellement utilisés — et la chimie MiSeq, le texte annonçant v3 2×300 alors que les lectures font 251 pb |
| §4 contrôles mock et négatifs | composition du mock et nature des témoins pour ce lot |

**Et une précision toujours attendue** : le délai entre capture et dissection, et l'ordre de
prélèvement des tissus sur un même poisson. Elle conditionne l'interprétation d'un effet propre aux
compartiments digestifs.

## 3. Pertuis : quel individu vient de quelle pêche — CLOS

**Réponse.** André confirme : la série **1011-1014 correspond à la pêche du 7 juillet 2014** et la
série **2011-2015 à celle du 20 août 2014**.

C'est une confirmation réelle et non une simple complétude : `decision_stations.md` §5 portait déjà
cette assignation depuis le 30 août, et l'inverse était parfaitement possible. Table de correction
ENA prête : `ena_deposit/ena_corrections_pertuis_dates.tsv`, 44 échantillons, à soumettre par un
humain selon la procédure MODIFY habituelle.

**Ce que sa réponse ne couvre pas.** La question était double et portait aussi sur les séries 1036+
de l'Ain 2014 et d'Avignon 2014. Son « oui » ne peut pas être étendu à ces deux séries :
`decision_stations.md` §5 établit qu'elles s'expliquent par des **chevesnes intercalés dans la
numérotation**, et non par des dates de pêche distinctes. Ces deux sites gardent donc leur date
unique.

## Ce qui ne passe plus par André

D7, le choix de la métrique de diversité, relève de la conversation d'analyse. Le DOI Zenodo, le
préfixage des identifiants de sujet dans le dépôt et le titre de l'article sont des décisions
internes.
