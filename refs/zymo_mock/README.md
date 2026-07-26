# refs/zymo_mock — reference ZymoBIOMICS pour la validation des mocks

Source : Zymo Research (telecharge le 2026-07-26 sur le cluster).

- ZymoBIOMICS.STD.genomes.ZR160406.zip  : ANCIEN jeu de souches (lots ~2016,
  D6300 / ZRC183430-187326). C'est la reference a utiliser pour ce projet
  (sequencage 2014-2015, avant le changement de 5 souches au lot ZRC190633).
- ZymoBIOMICS.STD.refseq.v2.zip          : NOUVEAU jeu de souches (2023),
  conserve par precaution si le lot du flacon est >= ZRC190633.
- zymo_mock_8bact_16S_ZR160406.fasta     : les 8 sequences 16S bacteriennes de
  l'ancien lot, concatenees (reference de travail). NB : 10 entrees pour 8
  especes car E. coli et S. enterica ont 2 copies 16S divergentes.

8 especes bacteriennes attendues (standard equimolaire) :
Bacillus subtilis, Enterococcus faecalis, Escherichia coli, Lactobacillus
fermentum, Listeria monocytogenes, Pseudomonas aeruginosa, Salmonella enterica,
Staphylococcus aureus. (Les 2 levures du standard ne sont pas pertinentes en 16S.)

A CONFIRMER par l'experimentateur : numero de lot exact du flacon Zymo utilise
en 2014-2015, pour verrouiller le choix ancien vs nouveau jeu de souches.

Reversibilite : les .zip et le dossier decompresse OLD_ZR160406/ sont ignores
par git (volumineux, retelechargeables) ; seuls ce README et le fasta 16S de
travail (16 Ko) sont versionnes.
