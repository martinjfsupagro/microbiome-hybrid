# Note de démarrage — Questions de recherche et introduction
## Projet microbiome-hybrid · document de passage de relais (2026-08-22)

Cette note synthétise les données disponibles et les questions abordées, pour servir de point
de départ à une conversation centrée sur la **définition des questions de recherche** et
l'**écriture de l'introduction** de l'article.

---

## 1. Le système biologique

Deux cyprinidés qui s'hybrident naturellement dans le bassin de la Durance et de l'Ardèche :

- **hotu** *Chondrostoma nasus* — code `Cn`
- **toxostome** *Parachondrostoma toxostoma* — code `Pt` (espèce d'intérêt patrimonial)
- **hybrides et parentaux non déterminés** — code `Ch` (*Chondrostoma* sp.)

Le toxostome est en régression et l'hybridation avec le hotu, plus généraliste, est un enjeu
de conservation. Le gradient d'hybridation est structuré géographiquement (voir §3).

## 2. Les données de microbiote disponibles

**16S rRNA, région V4 (251 pb), méthode dual-index Kozich (2013).**

| Élément | Valeur |
|---|---|
| Individus (poissons) | **181** |
| Tissus par individu | **4** : nageoire caudale (peau), branchie, midgut, hindgut |
| Individus complets (4 tissus) | 177 / 181 |
| Échantillons dans la table d'analyse | **2 180** |
| ASV | **44 200** |
| Lectures | 26,1 millions |
| Réplication technique | **3 runs MiSeq** des mêmes 768 librairies (2017) |
| Profondeur médiane | 10 129 lectures/échantillon |
| Arbre phylogénétique | de novo MAFFT + FastTree2, disponible (UniFrac, Faith PD) |
| Taxonomie | SILVA v138.2 (assignTaxonomy, DADA2) |

Le **gradient tissulaire** est une force du jeu : peau → branchie → midgut → hindgut couvre
un continuum d'exposition à l'eau et de fonction (interface externe → digestive).

## 3. Le plan d'échantillonnage : un gradient de zone hybride

Six populations organisées par rôle dans la zone d'hybridation :

| Rôle | Site | Rivière | n |
|---|---|---|---|
| Allopatrie (référence) | canal | Durance | 20 |
| Allopatrie (référence) | Ain | Ain | 33 |
| Sympatrie + hybridation | Büech | Durance | 35 |
| Sympatrie + hybridation | St-Just | Ardèche | 19 |
| Introgression asymétrique → toxostome | Baume | Ardèche | 25 |
| Introgression asymétrique → hotu | Avignon | Durance | 24 |

Deux sites supplémentaires en attente de statut : **Manosque** (15 individus, hors liste des 6)
et **Per** (10 individus, nom et rôle non renseignés). Leur sort dépendra de l'index hybride.

⚠️ **Point à clarifier pour l'introduction** : les libellés d'introgression asymétrique
(`asym. Toxo` à Baume, `asym. Hotu` à Avignon dans `metadata/site_mapping.csv`) sont ambigus —
ils peuvent désigner soit l'espèce **receveuse** des gènes, soit l'espèce **donneuse**. Le sens
exact conditionne l'interprétation du contraste entre ces deux sites (question secondaire 3) et
doit être confirmé auprès d'André avant de formuler l'hypothèse dans l'introduction.

## 4. Les covariables individuelles disponibles

- **taille (cm)** et **poids (g)** : 174/181 individus
- **sexe** : déterminé pour 108 individus (77 M, 31 F) ; 52 indéterminés, 21 manquants
- **année de capture** : 2014 ou 2015
- **site**, **rivière**, **rôle de population**

## 5. LA DONNÉE CENTRALE ATTENDUE : l'index hybride

Le génotypage est en cours (André). Il produira **un index hybride continu par individu**,
de **0 (hotu pur)** à **1 (toxostome pur)**. Fichier prêt à remplir :
`metadata/index_hybride_andre.csv` — 181 individus, dont **132 `Ch` à génotyper** (49 déjà
connus : Cn=0, Pt=1).

C'est une variable **continue**, ce qui ouvre des analyses plus riches qu'une simple
catégorie hybride/parental : on pourra tester des relations monotones, des seuils, ou une
non-linéarité le long de l'axe génomique.

---

## 6. LES QUESTIONS DE RECHERCHE ABORDÉES

### Question centrale (celle du projet)
**Le microbiote des hybrides est-il INTERMÉDIAIRE entre les parentaux, ou TRANSGRESSIF ?**

Trois hypothèses concurrentes, testables avec un index hybride continu :
- **intermédiaire / additif** : le microbiote varie de façon monotone avec l'index hybride —
  les hybrides ressemblent à la moyenne des parentaux ;
- **transgressif** : les hybrides sortent de la gamme parentale (diversité ou composition
  hors de l'enveloppe des deux espèces) — signature d'une rupture de la relation
  hôte-microbiote ;
- **dominance** : le microbiote des hybrides ressemble à un seul parent.

Cadre conceptuel : le microbiote comme trait de l'hôte partiellement héritable, et
l'hybridation comme perturbation potentielle du contrôle génétique de l'assemblage
microbien. Lien possible avec la notion de « dysbiose hybride » et avec la fitness des
hybrides.

### Questions secondaires identifiées

1. **Structuration par tissu** — le tissu est probablement le premier facteur de variation
   (gradient peau → branchie → intestin). Question : l'effet de l'hybridation est-il uniforme
   entre tissus, ou plus marqué dans un compartiment (p. ex. l'intestin, plus dépendant de
   l'hôte, vs la peau, plus déterminée par l'environnement) ?

2. **Effet du contexte écologique** — le gradient allopatrie → sympatrie → introgression
   permet de distinguer un effet **génomique** (index hybride) d'un effet **environnemental**
   (site/rivière). Question : le microbiote suit-il la génétique de l'hôte ou l'environnement
   local ?

3. **Asymétrie de l'introgression** — les deux sites d'introgression asymétrique (vers le
   toxostome à Baume, vers le hotu à Avignon) offrent un contraste : l'effet de l'hybridation
   sur le microbiote est-il symétrique selon le sens du flux de gènes ?

4. **Différence entre les deux espèces parentales** — préalable nécessaire : les parentaux
   diffèrent-ils dans leur microbiote ? Sans différence parentale, la question hybride perd
   son objet.

5. **Reproductibilité technique** — les 3 runs permettent de quantifier l'effet run et de
   montrer que les effets biologiques le dépassent (argument méthodologique, pas une question
   biologique).

### Questions écartées ou hors périmètre
- Fonction prédite du microbiote (PICRUSt) : présente dans le manuscrit d'origine, mais
  contestée dans la littérature récente ; à rediscuter avant de l'inclure.
- Effet du sexe : possible en covariable, mais le sexe n'est déterminé que pour 108/181
  individus — puissance limitée.

---

## 7. RESSOURCES BIBLIOGRAPHIQUES DÉJÀ CONSTITUÉES

| Fichier | Contenu |
|---|---|
| `fish_microbiome_key_refs.bib` | **99 références** clés du microbiome des poissons d'eau douce (top-cités, revues, récents influents), avec abstracts pour 68 |
| `fish_16S_sota_references.bib` | **19 références** méthodologiques de l'état de l'art 16S |
| `rarefaction_sota.bib` | **13 références** sur le débat raréfaction/normalisation |
| `references.bib` | **46 références** récupérées du manuscrit d'origine (Zotero reconstruit) |
| `fish_16S_state_of_the_art.docx` | protocole état de l'art 16S, avec citations inline |

Point de vigilance bibliographique : la sélection des 99 références a nécessité un filtrage
pour exclure l'ADN environnemental (eDNA de biodiversité) et le bactérioplancton libre, qui
polluaient les requêtes lexicales. La bibliographie est donc bien centrée sur le microbiote
**associé à l'hôte**.

---

## 8. ÉTAT DE L'ÉCRITURE

- **Materials & Methods** : rédigé de l'échantillonnage à la préparation des données
  (`docs/materials_and_methods.docx`, v7). Reste : §1 (dates/coordonnées de collecte),
  §8.6 (analyses statistiques, dépend de l'index hybride), §9 (accession ENA).
- **Introduction** : à écrire — objet de la prochaine conversation.
- **Manuscrit d'origine** : un draft antérieur existe (`MS_hybrid and microbiota_draft1.docx`),
  portant sur une **partie seulement** des données (branchie et midgut). Son introduction a
  déjà fait l'objet d'une revue critique (`AM_introduction_review.docx`) : problèmes relevés
  = affirmations causales trop fortes, dichotomie tissulaire trop tranchée, phrases longues.
  À réutiliser comme matière première, pas comme modèle.
- **Journal cible envisagé** : Animal Microbiome (BMC) — analyse de positionnement faite
  (`journal_shortlist.csv`, `AM_submission_readiness.docx`).

---

## 9. CE QUI CONDITIONNE LES QUESTIONS FORMULABLES

À garder en tête en rédigeant l'introduction :

1. **L'index hybride n'est pas encore disponible** — les questions doivent être formulées de
   façon à rester valides quelle que soit la distribution obtenue (p. ex. s'il y a peu
   d'hybrides intermédiaires, une analyse par classes sera impossible).
2. **Le plan est déséquilibré** : effectifs de 19 à 35 par site, et les sites à faible
   profondeur de séquençage (canal, Manosque) auront moins de puissance après raréfaction.
3. **Manosque et Per** ne sont pas encore rattachés au gradient — leur inclusion changerait le
   nombre de populations.
4. **La raréfaction à 3 000 lectures** retire environ 18 % des échantillons ; l'introduction
   n'a pas à en parler, mais le cadrage des questions doit rester réaliste sur la puissance.
