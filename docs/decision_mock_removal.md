# docs/decision_mock_removal.md — Strategie de retrait des sequences mock (echantillons mock_contaminated)

## Decision (2026-07-27)
Pour les 20 echantillons `mock_contaminated` (vrais poissons a 4 tissus dont UN puits-
tissu est contamine par de l'ADN mock ; voir docs/decision_mock_samples.md), la
strategie retenue est **le retrait des ASV mock puis re-seuillage**, PAS l'exclusion
de l'echantillon. Distinct des 6 `probable_mock` (Cab1021/Cab1022), qui, eux, sont
exclus du biologique.

/!\ AUCUNE TABLE N'EST GENEREE A CE STADE. On fige la regle ; l'application attend le
mode de rarefaction (tirage unique vs repete, cf. docs/decision_rarefaction.md).

## Regle en trois temps
1. **Retirer les 10 ASV du mock Zymo de TOUS les echantillons**, au niveau ASV
   (sequences exogenes exactes : ASV0030, 0037, 0055, 0056, 0091, 0092, 0100, 0150,
   0262, 0508). Retrait au niveau ASV = ne touche que les sequences Zymo ; les vrais
   ASV poisson et leurs proportions relatives sont preserves apres renormalisation.
   Sans cout pour les tissus propres (les tissus digestifs des poissons concernes
   sont a ~0 % mock).
2. **Reappliquer le seuil de rarefaction (3 000 lectures) APRES retrait.** Sur les 20,
   13 conservent >= 3 000 lectures residuelles ; 7 tombent sous le seuil et sortent
   donc naturellement a la rarefaction (14Bue1005Cn01A caudale durance2/3 : 2 173-2 551 ;
   15Bue1011Ch03A durance2/3 ; 14Per2011Ch03A-bis ; 15Caa1018Ch01A ; 15Avi1001Cn02A).
3. **Conserver le flag de severite** pour la contamination forte (mock >= 50 % :
   14Man1022Ch05A branchie x3 ; 14Bue1005Cn01A caudale durance2/3). Ces echantillons
   sont gardes s'ils passent le seuil, mais SIGNALES : une fuite forte a pu apporter du
   bruit non retirable (voir justification).

## Justification
- La contamination est ADDITIVE : les lectures mock se sont ajoutees par-dessus les
  lectures poisson. Le retrait au niveau ASV est donc une soustraction propre.
- Le signal residuel est plausiblement piscicole : genres residuels dominants =
  Cetobacterium (genre intestinal classique de poisson d'eau douce), Flavobacterium,
  Cloacibacterium. Candidatus Branchiomonas (bacterie branchiale) figure dans le
  residu de 15Caa1018Ch01A (caudale).
- LIMITE — le mock est un traceur VISIBLE d'un evenement de contamination de puits.
  Rien ne garantit qu'une fuite d'ADN d'AUTRES poissons (invisible, indistinguable de
  vraies sequences) n'a pas accompagne la fuite mock. D'ou le flag de severite : plus
  la fraction mock est elevee, plus le residu est suspect meme apres nettoyage.
- Impact pratique limite : les puits touches sont quasi tous des CAUDALES (peau),
  plus une branchie (Man1022) ; AUCUN tissu intestinal n'est contamine. Le compartiment
  central de la question microbiome (gut) est donc epargne.

## Reproductibilite
Test de profondeur residuelle : calcule sur results/dada2_final/asv_table_filtered.tsv,
traceurs = 10 ASV mock confiants (results/mock_validation/mock_blast.tsv). Flags dans
metadata/sample_qc_flags.csv. Aucune donnee d'origine modifiee a ce stade.

## A confirmer par Andre / l'experimentateur
- Origine de la contamination des puits caudale (Bue*, Ain1043, Caa1018) : debordement
  de puits sur la plaque de librairies ?
