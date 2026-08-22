# docs/decision_crosstalk.md — Quantification du crosstalk (saut d'index)

## Analyse (2026-07-27) — script 10-crosstalk.sh
Deux mesures indépendantes, deux conclusions à ne PAS confondre.

## 1) Crosstalk pur (saut d'index) = NÉGLIGEABLE
Puits vides (67 ; aucune librairie chargée → toute lecture = fuite pure) :
- **41 lectures parasites au total sur 26,8 M → 0,0002 %**
- médiane 0 lecture/puits, max 13.
→ Le saut d'index est très en-dessous du seuil de préoccupation usuel (~0,1–1 %).
  Aucun filtrage de bruit de fond nécessaire à ce titre. Chimie de séquençage propre.

## 2) Traceurs mock = RÉVÈLENT DEUX MOCKS MAL ÉTIQUETÉS (confirmé André ; ≠ crosstalk)
Les 10 ASV des 8 taxons Zymo (exogènes) apparaissent hors des puits mock :
68 % des lectures mock sont "hors mock", dans 942 échantillons biologiques.
MAIS ce n'est PAS du saut d'index diffus (qui serait à bas bruit, cf. §1) :
ce sont quelques échantillons à composition MASSIVEMENT mock, trahis par leur
puits/index partagés avec les mocks.

Échantillons les plus suspects (fraction mock élevée) :
| Échantillon           | puits | plaque | i7    | frac mock |
|-----------------------|-------|--------|-------|-----------|
| 15Cab1022Ch01A (x3 runs) | H11 | 1     | SA711 | ~99,4 %   |
| 15Cab1021Ch01A (x3 runs) | G11 | 1     | SA711 | 70–73 %   |
| 14Man1022Ch05A (x3 runs) | ?   | ?     | ?     | 52–57 %   |
(Mocks réels : puits G11, plaques 3 et 5, i7 SB711/SC711.)

INTERPRÉTATION : ces "Ch" annotés biologiques sont probablement des puits mock
mal étiquetés ou une contamination physique de puits (série d'index 711, puits
G11/H11, plaques adjacentes). Un saut d'index réel ne produit jamais un
échantillon à 99 % mock.

## ACTION REQUISE (à remonter à André)
- **15Cab1021*, 15Cab1022*** (Cab = Ain 2015) : CONFIRMÉ mocks par André (2026-07-27) — exclus du biologique, Ain 2015 = 19 poissons. Ancienne action de vérification :
  s'il s'agit de mocks mal annotés → à exclure des analyses biologiques ou à
  ré-identifier. Idem **14Man1022Ch05A*** (Manosque).
- Ces échantillons sont indépendants de la question hybride mais fausseraient
  tout contraste sur Ain 2015 / Manosque s'ils restent classés "biologiques".

## Fichiers
results/crosstalk/ : crosstalk_summary.txt, empty_totals.tsv, mock_leakage.tsv
