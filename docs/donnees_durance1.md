# Jeu de données `durance1`

Run MiSeq `170710_M03930_0062_000000000-BBHKV`, extrait de
`data/durance1/170710_M03930_0062_000000000-BBHKV.tar` (5,0 Go → 4,8 Go).

## Run
| | |
|---|---|
| Experiment | EG_16S_Durance_070717 |
| Date | 2017-07-10 |
| Investigator | JFMartin |
| Assay | **Schloss** (dual-index V4, 515F/806R) |
| Reads | 2 × 251 pb |
| Workflow | GenerateFASTQ (déjà démultiplexé, pas de bcl) |

3076 fastq.gz = 769 × (R1, R2, I1, I2) — 768 échantillons + Undetermined.

> Les dossiers du tar sont en mode 666 (archive créée sous Windows depuis le
> MiSeq) : non traversables sous Linux. Après extraction :
> `chmod -R u+rwX,go+rX,go-w <rundir>`

## Nomenclature
`{année}{Site}{individu}{Taxon}{tissu}{réplicat}` — ex. `14Ain1001Cn01A`

| Champ | Position | Valeurs |
|---|---|---|
| Année   | 1-2   | 14 (270), 15 (459) |
| Site    | 3-5   | Ain, Avi, Bau, Bue, Caa, Cab, Jus, Man, Per |
| Individu| 6-9   | 1001… / 2011… |
| Taxon   | 10-11 | **Ch** = chevesne (531), **Cn** = hotu (140), **Pt** = toxostome (24) |
| Tissu   | 12-13 | 01 (182), 02 (141), 03 (180), 05 (179) |
| Réplicat| 14    | A |

Les 4 blancs sont nommés par tissu — `Blanc-Caudal`, `Blanc-Branchie`,
`Blanc-Midgut`, `Blanc-Hindgut` — soit 4 tissus, cohérent avec les 4 codes
numériques. La correspondance code ↔ tissu reste **à confirmer**.

### Site × année (plan très déséquilibré)
| Site | 2014 | 2015 |
|---|---|---|
| Ain | 55 | – |
| Avi | 44 | 52 |
| Bue | 68 | 72 |
| Man | 60 | – |
| Per | 43 | 1 |
| Bau | – | 100 |
| Caa | – | 80 |
| Cab | – | 78 |
| Jus | – | 76 |

**Seuls Avi et Bue sont échantillonnés les deux années.** Site et année sont
donc largement confondus : un effet « année » ne sera estimable que sur ces
deux sites.

### Taxon × site (également confondu)
Le chevesne (`Ch`) est présent partout et domine (531/695). Le hotu (`Cn`) est
concentré sur Avi (87 sur 140) ; le toxostome (`Pt`) n'existe qu'à Ain (16) et
Avi (8), soit 24 échantillons seulement. Une comparaison taxon brute mélangera
donc de l'effet site. **Avi est le seul site où les trois taxons coexistent.**

### ⚠ Aucun code « hybride » dans ce run
Les trois codes correspondent à trois espèces distinctes — le chevesne
(*Squalius cephalus*) n'hybride pas avec le couple *Chondrostoma* et sert
vraisemblablement d'espèce de référence sympatrique. **Le statut hybride
hotu × toxostome n'est donc pas encodé dans les noms d'échantillons.**

Trois hypothèses à trancher avant de construire les métadonnées :
1. les hybrides sont dans un autre run (le dossier s'appelle `durance1`) ;
2. `Cn`/`Pt` sont des déterminations de terrain (morphologiques), et le statut
   hybride est assigné a posteriori par génotypage, dans un fichier externe ;
3. les hybrides ne sont pas encore séquencés.

L'hypothèse 2 est la plus probable : dans la zone d'hybridation de la Durance
les hybrides sont morphologiquement intermédiaires et régulièrement confondus
avec l'une des deux espèces parentales sur le terrain. Si c'est le cas, une
partie des 164 `Cn`/`Pt` sont en réalité des hybrides mal étiquetés, et le
fichier de génotypage est indispensable — sans lui il n'y a pas de variable
réponse.

## Contrôles disponibles
| Type | n | Usage |
|---|---|---|
| `empty_1..25` | 25 | puits vides — bruit d'index hopping |
| `Blanc-*` | 4 | blancs d'extraction, un par tissu |
| `Mock-1`, `Mock-2` | 2 | communauté mock — calibration du pipeline |
| `T-1..T-8` | 8 | témoins (nature à préciser) |

Jeu de contrôles complet et exploitable — à passer dans DADA2 avec les
échantillons, pas à écarter en amont.

## Anomalies de nomenclature (à corriger au parsing)
- Espaces internes : `14Ain1038 01A`, `14Ain 1043 01A` (~31 échantillons Ain)
- Tirets internes : `14Ain-1039-02A`
- **Code taxon absent** sur les ~31 échantillons Ain 2014 et `14Avi1037`
- Casse du site incohérente : `BUe` (17) vs `Bue`, `per` (4) vs `Per`
- Suffixe `_bis` : `14Per2011Ch01A_bis`, `14Per2012Ch01A_bis` (4 ×, tissus 01 et 05)
- Un seul `04A` (`Cn`) — code tissu inattendu, à vérifier

Ne pas parser les noms par position sans normalisation préalable.

## Point de vigilance : 12S d'hôte
Protocole Schloss V4 confirmé → les primers 515F/806R co-amplifient le 12S
mitochondrial de poisson. Sur un projet antérieur (apron), 15–47 % des lectures
étaient du 12S d'hôte. À retirer avec cutadapt **avant** DADA2, en logguant le
taux retiré par échantillon (il variera selon le tissu : branchie et nageoire
caudale sont bien plus riches en cellules hôtes que le contenu intestinal, ce
qui biaiserait toute comparaison de diversité entre tissus).

Ces lectures 12S sont à **conserver dans un fichier séparé**, d'autant plus que
le statut hybride n'est pas dans les noms d'échantillons. Elles permettent :
- de séparer sans ambiguïté chevesne et *Chondrostoma* (genres très distants au
  12S) → contrôle des inversions d'étiquettes entre taxons ;
- de donner la lignée **maternelle** au sein du couple hotu / toxostome.

Limite : l'ADN mitochondrial étant transmis par la mère seule, un hybride F1 de
mère hotu est indistinguable d'un hotu pur. Le 12S ne remplace donc pas un
génotypage nucléaire — c'est un contrôle qualité et un indicateur du sens du
croisement, pas un test d'hybridation.
