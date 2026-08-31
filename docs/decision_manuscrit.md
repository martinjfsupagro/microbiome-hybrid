

## Retrait du Materials & Methods autonome (2026-08-31)

`docs/materials_and_methods.docx` est **supersede** par les sections Methods de
`docs/manuscrit/Article.docx`. Verification faite paragraphe par paragraphe :

| | Article | M&M |
|---|---|---|
| paragraphes | 73 | 69 |
| communs a l'identique | 62 | 62 |
| propres au document | 11 | 7 |

Aucun des 7 paragraphes propres au M&M ne porte d'information absente de l'Article :
quatre sont des variantes ou l'Article est **plus riche** (renvois vers les Tables S2/S4
et la Note S1, correction de l'assignation des index), un est un en-tete de projet, un
est un placeholder que l'Article a deja resolu, et un est le renvoi Table S1 que
l'Article formule mieux.

Le M&M portait en revanche **une affirmation etablie fausse** : « Plate layout and i7
indices were identical throughout, whereas the i5 index set differs between the two
libraries ». C'est la generalisation abusive depuis la plaque 1, corrigee dans l'Article
(i7 pour 384 des 768 librairies, i5 pour 576) mais restee ici. Un document perime qui
porte une erreur connue est pire qu'un document absent.

**Traitement retenu** : bandeau SUPERSEDED en tete, phrase fausse neutralisee sur place
avec renvoi vers l'Article, fichier conserve (l'historique git garde ses etats). Il ne
doit plus etre edite ni cite. Toute mise a jour des Methods se fait desormais dans
`docs/manuscrit/Article.docx` seul.


---

## Divergence de lignee du manuscrit, 2026-08-31 (resolue)

La session ENA a edite `docs/manuscrit/Article.docx` et `Supplementary_Data.docx` a partir
d'une lignee d'artefact ANTERIEURE et a ecrase les fichiers de l'arbre de travail :

| | version commitee (HEAD) | version deposee par la session ENA |
|---|---|---|
| Article.docx | 50 319 o, 75 paragraphes | 46 455 o, 63 paragraphes |
| Supplementary_Data.docx | 475 466 o, 9 tables, 3 figures | 41 282 o, 4 tables, 0 figure |

Aucune perte : l'ecrasement etait **non commite**, `git checkout` a restaure HEAD. La version
de la session ENA est conservee dans `docs/manuscrit/version_session_ena/` pour tracabilite.

**Fusion effectuee** — porte depuis leur version vers la version commitee :
- note sur la precision des coordonnees et les termes ENVO (Table S1) ;
- paragraphe « Host identity » (369 Pt / 236 Cn / 122 hybrides sur 727 echantillons — verifie
  contre `analysis_metadata.csv`, concordance exacte) ;
- **Note S2** sur la reutilisation des identifiants de poisson entre campagnes ;
- phrase de §9 sur la correction ENA du 2026-08-31.

**NON porte, parce que faux** : leur decompte de **181 individus** (et « 25 identifiants
reutilises », « 92 P. toxostoma »). Reproduit exactement : la cle (prefixe d'annee du nom
depose, site, numero) donne 181, la cle corrigee 180, et la cle en trop est le fantome cree
par la coquille `15Per2015Ch03A` — dont trois tissus sont nommes `14Per2015*` et le quatrieme
`15Per2015*`. Leur mecanisme (collision d'identifiants entre campagnes) est JUSTE ; c'est
l'arithmetique qui porte la coquille. Chiffres corrects : **180 individus, 24 identifiants
reutilises, 91 P. toxostoma / 59 C. nasus / 30 hybrides**.

Leur message concluait que 181 « correspond exactement au compte du tableau de genotypage ».
C'etait une concordance avec un chiffre perime : le tableau d'Andre portait 181 lignes AVANT
la correction de la coquille. L'accord ne testait rien.

**Regle pour la suite** : `docs/manuscrit/` n'a qu'une lignee canonique, celle du depot git.
Une session qui edite ces fichiers doit partir du fichier du cluster, pas d'un artefact de sa
propre conversation.
