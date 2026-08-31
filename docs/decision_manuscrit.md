

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
