"""56-note_sexe.py — décision de JF du 2026-10-06 : le contraste femelles/mâles (R27) n'est pas rapporté.
Seule la note grise du paragraphe Results « Alpha diversity » change ; aucun texte de l'article n'est modifié.
Raisons consignées : non établi sous D7 (compartiment interne : indices de présence seuls ; externe : Shannon
seul), confondu avec l'ordre de traitement (femelles disséquées plus tôt, rang médian 5 contre 8, p = 0,02),
déséquilibré entre stations (p = 0,06), et le sexe n'est pas une question de l'article.
python-docx absent de meso : exécution hors cluster. Garde md5 en entrée.
"""
import hashlib, os
import docx

M = os.environ.get("MS_DIR", "docs/manuscrit/"); OUT = os.environ.get("OUT_DIR", M)
MD5_IN = "5daac3ef17056f1b715e2335bdd69112"                       # commit cd6f2d0
assert hashlib.md5(open(M + "Article.docx", "rb").read()).hexdigest() == MD5_IN, "md5 d'entrée inattendu"
d = docx.Document(M + "Article.docx")
P = [p for p in d.paragraphs if p.text.startswith("Hybrids were transgressive in none of the 32 combinations")]
assert len(P) == 1
G = [r for r in P[0].runs if r.text.lstrip().startswith("[Contrôle (v) :")]
assert len(G) == 1 and "décision de JF attendue" in G[0].text
G[0].text = (" [Contrôle (v) : plan docs/plan_R31_ordre_2026-10-06.md (f3916c1), scripts/51, R36 ; intégré sur décision "
             "de JF du 2026-10-06. Contraste femelles/mâles (R27) : NON RAPPORTÉ, décision de JF du 2026-10-06 — non établi "
             "sous D7, confondu avec l'ordre de traitement (femelles disséquées plus tôt, rang médian 5 contre 8, p = 0,02) "
             "et déséquilibré entre stations ; le sexe n'est pas une question de l'article. À retirer avant soumission.]")
d.save(OUT + "Article.docx")
print("écrit :", OUT + "Article.docx", hashlib.md5(open(OUT + "Article.docx", "rb").read()).hexdigest())
