# docs/decision_mock_samples.md — Échantillons à composition mock (annotation QC)

## Décision (2026-07-27)
Certains échantillons annotés "biological" contiennent des lectures du mock Zymo.
L'examen PAR TISSU sépare deux cas de nature différente. **samples_all.csv n'est PAS
modifié** ; une table de jointure `metadata/sample_qc_flags.csv` (clé = dada2_id)
porte l'annotation, sur le même principe que site_mapping.csv.

## Cas 1 — probable_mock : 6 échantillons → NE PAS compter comme biologiques
Hypothèse retenue : ce sont des puits mock mal étiquetés, pas des poissons.
Preuve : ces "individus" n'ont **qu'un seul échantillon (caudale)** — aucun tissu
digestif ni branchial (un vrai poisson du design = 4 tissus) — et sont à 70-99 %
lectures mock, en puits G11/H11 index série 711 (co-localisés avec les vrais mocks).
- 15Cab1022Ch01A (durance1/2/3) : 99,4-99,5 % mock, 1 tissu
- 15Cab1021Ch01A (durance1/2/3) : 70-73 % mock, 1 tissu
(Cab = Ain 2015 dans site_mapping.csv.)
→ À exclure des analyses biologiques (traiter comme mock/contrôle).

## Cas 2 — mock_contaminated : 20 échantillons → GARDER le poisson, signaler le puits
Ce sont de VRAIS poissons (4 tissus, tissus intestinaux à ~0 % mock) dont UN puits-
tissu (surtout la caudale) est contaminé à 20-65 % mock. Ex. 14Man1022 : branchie
52-57 % mock mais caudale/midgut/hindgut à 0 %. Individus concernés : Bue1005, Bue1001,
Bue1004, Bue1011, Man1022, Ain1043, Per2011, Caa1018, Avi1001.
→ NE PAS requalifier en mock. Le puits-tissu contaminé est à écarter ou à traiter avec
prudence dans les analyses par tissu ; le reste du poisson est exploitable.

## Seuils
probable_mock    : frac_mock >= 0,70 (les 6 tombent tous à tissu unique — cohérent)
mock_contaminated: 0,20 <= frac_mock < 0,70 sur un puits d'un individu à 4 tissus
Le trou net entre 0 % (tissus digestifs des vrais poissons) et 70-99 % (puits Cab
isolés) rend la coupure robuste ; la zone 20-65 % correspond sans exception à des
poissons complets par ailleurs propres.

## À confirmer par André / l'expérimentateur
- Cab1021/Cab1022 : étaient-ce des puits mock sur la plaque 1 (série index 711) ?
- Origine de la contamination des puits caudale (Bue*, Ain1043) : débordement de puits ?

## Reproductibilité
Script : scripts/11-flag_mock_samples.py (déterministe, relit la table filtrée).
Table : metadata/sample_qc_flags.csv (26 lignes). Traceurs mock = 10 ASV Zymo
confiants (mock_blast.tsv). Aucune donnée d'origine modifiée.
