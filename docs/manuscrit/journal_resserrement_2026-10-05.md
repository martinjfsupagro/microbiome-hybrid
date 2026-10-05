# Resserrement du texte principal — 2026-10-05

Demande de JF : « Resserrer le texte principal ». Choix de JF : cible ≈ 8 000 mots, détails techniques déplacés dans le supplément, livraison dans un fichier séparé (Article.docx reste la référence jusqu'à validation).

## Résultat
| Section | Avant | Après |
|---|---|---|
| Background | 1 449 | 1 053 |
| Methods | 5 261 | 3 298 |
| Results | 2 808 | 2 493 |
| Discussion | 1 047 | 948 |
| Conclusions | 112 | 112 |
| **Total** | **10 677** | **7 904** |

Hors notes grises et Abstract (326 mots, inchangé). Figures, légendes, références et Declarations inchangées.

## Fichiers
- `docs/manuscrit/Article_resserre.docx` — version resserrée (référence : Article.docx md5 68caaeb7, commit 23e3aad).
- `docs/manuscrit/Supplementary_Data_resserre.docx` — nouvelle **Note S2** (traitement des séquences, contrôles, raréfaction répétée, ENA) ; l'ancienne Note S2 (host subject id) devient **Note S3**.
- `docs/manuscrit/resserrement_2026-10-05_comparaison.docx` — chaque paragraphe modifié, avant/après, ce qui a été retiré et où.
- `docs/manuscrit/resserrement_2026-10-05_paragraphes.tsv` — même table sans le texte.
- `scripts/42-resserrement_article.py` — construction des deux fichiers (gardes md5 sur les références).

## Principes
1. Les 25 paragraphes de Methods retirés ou condensés figurent **verbatim** dans la Note S2 (seuls les renvois sont adaptés : « Supplementary Table S5 » → « Table S5 », « (Results) » → « (main text, Results) », etc.). Contrôle : début de chacun retrouvé dans le supplément, 25/25.
2. Aucun nombre des paragraphes modifiés n'a disparu à la fois du texte principal et du supplément (audit des valeurs numériques à deux chiffres et plus).
3. Les 64 chaînes contrôlées par le script 40 restent dans le texte principal ; tables citées S1→S10 ; notes citées S1→S3 (nouvel appel à la Note S1 au §3, à la Note S3 au §9).
4. Les sous-titres 5.1–5.5 sont supprimés ; la numérotation 1–9 et 8.1–8.12 est conservée, donc les renvois « §8.x » du texte et du supplément restent valables.

## Retraits de contenu (non déplacés verbatim) à valider
- §8.7 : « The choice of a differential-abundance method remains to be fixed. » — aucune analyse d'abondance différentielle n'est rapportée ; signalé en note grise.
- Background, dernier paragraphe : la phrase sur la référence interne des deux stations du Suran (14 et 19 individus) — n'est exploitée nulle part dans les Results.
- Background : détails de littérature (transect de 180 km chez les lémuriens, « on two replicates of the same hybrid zone » chez la souris, etc.).
- Results / Plate position : l'historique du témoin « station mono-catégorie » d'une analyse antérieure.
- Results / Composition : l'ouverture « A preliminary variance partition… not as a result of it » (la note grise qui demandait de la reformuler est mise à jour).
- Discussion, 1er paragraphe : la phrase récapitulative qui redisait l'Abstract.
Détail complet dans la table de comparaison.

## Défauts préexistants trouvés et corrigés au passage (supplément)
- Note S1 renvoyait à « §8.7 » pour la structure emboîtée → §3 et §8.8.
- Table S5 : « dissimilarity scales reported in §8.7 » → « in the main-text Results ».
- Table S9 : « (§8.6, §8.8) » pour la covariable de position → (§8.7, §8.9).
- L'ancienne Note S2 n'était citée nulle part dans le texte principal ; elle est maintenant appelée au §9 (comme Note S3).

## Script 40
Deuxième argument facultatif (fichier de sortie) pour vérifier une variante sans écraser `verif_article_v2.tsv` ; nouveau contrôle de l'ordre de citation des Notes S. Sur Article.docx (référence) ce contrôle est en ÉCART : la référence ne cite que la Note S1.
