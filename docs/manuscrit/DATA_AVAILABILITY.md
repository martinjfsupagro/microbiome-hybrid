# Paragraphe *Data availability* — projet Durance 16S

Accession de l'étude : **PRJEB124417**
Dépôt effectué le 25 août 2026 · pas d'embargo, données publiques après validation ENA

---

## Version anglaise (pour le manuscrit)

> **Data availability**
>
> Raw sequence data have been deposited in the European Nucleotide Archive (ENA) at
> EMBL-EBI under accession number PRJEB124417. The submission comprises 768 samples
> and 2,304 sequencing runs (4,608 FASTQ files). Each sample was processed through two
> independent one-step dual-index PCR library preparations: the first library was
> sequenced once (run label durance1) and the second was sequenced twice on separate
> flow cells (durance2, durance3). Runs are named accordingly, so that the nested
> replication structure — sequencing replication nested within library preparation —
> can be recovered from the run titles. Sample metadata follow the GSC MIxS
> host-associated checklist (ERC000013) and include collection year, sampling site
> coordinates, host species and sampled tissue. Extraction blanks, no-template PCR
> controls and mock communities are included in the submission and are flagged as such
> in the sample titles.

## Version française

> **Disponibilité des données**
>
> Les données de séquençage brutes sont déposées dans l'European Nucleotide Archive
> (ENA, EMBL-EBI) sous le numéro d'accession PRJEB124417. Le dépôt comprend
> 768 échantillons et 2 304 runs de séquençage (4 608 fichiers FASTQ). Chaque
> échantillon a fait l'objet de deux préparations de librairie indépendantes par PCR
> dual-index en une étape : la première librairie a été séquencée une fois (run
> durance1), la seconde deux fois sur des flow cells distinctes (durance2, durance3).
> Les runs sont nommés en conséquence, de sorte que la structure de réplication
> emboîtée — réplication de séquençage nichée dans la préparation de librairie — soit
> reconstituable depuis les titres de runs. Les métadonnées suivent le checklist GSC
> MIxS host-associated (ERC000013) et renseignent l'année de collecte, les coordonnées
> du site, l'espèce hôte et le tissu prélevé. Blancs d'extraction, témoins de PCR sans
> matrice et communautés synthétiques sont inclus et identifiés dans les titres.

---

## Chiffres du dépôt

| Objet | Nombre |
|---|---|
| study | 1 (`PRJEB124417`) |
| samples | 768 |
| experiments | 2 304 |
| runs | 2 304 |
| fichiers fastq.gz | 4 608 (11,7 Go) |

Composition par librairie (chacune × 3 runs) :

| Catégorie | Librairies |
|---|---|
| Échantillons biologiques | 727 |
| Contrôles (blancs, témoins PCR, mocks) | 16 |
| Puits vides (mesure du crosstalk) | 25 |

Sites d'échantillonnage : 9 (Ain, Avi, Bau, Bue, Caa, Cab, Jus, Man, Per).

Note sur le compte de 727 : le décompte initial du projet était de 729 échantillons
biologiques. Deux d'entre eux (`15Cab1021Ch01A` et `15Cab1022Ch01A`) sont en réalité des
communautés synthétiques mal étiquetées, identifiées par les flags de QC d'André et
requalifiées en `mock` dans le dépôt — d'où 727 biologiques et 4 mocks.
Plage d'accessions de runs : `ERR17751455` à `ERR17753805`.

---

## Points à vérifier avant soumission de l'article

*Mis à jour le 25/08/2026 après lecture du Matériels et Méthodes (docs/materials_and_methods.docx).*

1. Les données ENA restent **privées** jusqu'à la validation par les curateurs
   (quelques jours) ; l'accession `PRJEB124417` est déjà citable dans un manuscrit soumis.
   Vérifié le 25/08/2026 : l'API publique de l'ENA ne renvoie encore aucun run pour cette
   accession et la fiche de synthèse répond en erreur — c'est le comportement attendu
   avant validation, non un problème de dépôt (le reçu de soumission, lui, confirme
   les 768 échantillons et les 2 304 runs).
2. Vérifiez l'affichage public sur
   <https://www.ebi.ac.uk/ena/browser/view/PRJEB124417> avant l'acceptation finale.
3. **Structure de réplication — résolue.** Le §8.7 du Matériels et Méthodes établit que
   les trois runs ne sont pas trois réplicats techniques d'une même librairie, mais
   **deux préparations de librairie indépendantes** : durance1 issu d'une première PCR
   dual-index, durance2 et durance3 issus d'une seconde PCR de ces mêmes échantillons,
   séquencée deux fois. Les données le confirment : i5 et i7 strictement identiques
   entre durance2 et durance3 (768/768), et l'analyse de similarité du §8.7 montre que
   les deux runs partageant une librairie sont bien plus proches (Bray-Curtis moyen
   0,118) que de celui de l'autre librairie (0,248). Les paragraphes ci-dessus ont été
   rédigés en conséquence.

4. **Une phrase du Matériels et Méthodes reste inexacte.** Le §sur la préparation des
   librairies affirme « Plate layout and i7 indices were identical throughout ». Les
   données le contredisent : entre durance1 et durance2, l'i7 change pour **384 des 768**
   librairies et l'i5 pour 576. En revanche, l'*ensemble* des 768 couples (i7, i5) est
   identique dans les trois runs — c'est donc la même réserve d'index, **réattribuée
   différemment aux puits** lors de la seconde PCR, et non un jeu d'index différent.
   Formulation suggérée : *« The same set of 768 index combinations was used for both
   library preparations, but index-to-well assignment differed between them. »*
   L'appariement échantillon-fichier a été vérifié empiriquement (plus proche voisin
   Bray-Curtis entre réplicats : aucun échec réciproque sur 136) et n'est pas affecté.

5. **Nuance sur le modèle ENA.** Le dépôt compte 2 304 experiments, un par run, là où il
   n'y a que 1 536 librairies réelles (768 × 2 préparations). Dans le modèle ENA, un
   EXPERIMENT décrit une librairie et un RUN son séquençage : durance2 et durance3
   partageant la même librairie, ils auraient pu être rattachés à un experiment unique.
   Les données déposées sont correctes et correctement reliées à leurs échantillons ;
   seul le décompte d'experiments suggère trois librairies par échantillon au lieu de
   deux. Un réutilisateur retrouve la structure réelle depuis les suffixes de run, et le
   paragraphe *Data availability* ci-dessus l'énonce explicitement. Si vous souhaitez une
   fidélité stricte du modèle, une mise à jour des métadonnées d'experiment est à
   discuter avec le support ENA — à mettre en balance avec le risque de manipuler un
   dépôt tout juste validé.
4. La table complète des accessions, avec les MD5 et les métadonnées par run, est dans
   `ENA_accessions_durance.tsv`.
