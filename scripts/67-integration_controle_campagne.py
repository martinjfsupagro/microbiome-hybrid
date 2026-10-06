#!/usr/bin/env python3
"""67-integration_controle_campagne.py — intègre à l'article le contrôle (vi), campagne de pêche (décision de JF du
2026-10-06 : « intègre les changements pour l'article ») : plan docs/plan_controle_campagne_2026-10-06.md,
scripts/66 (commit 118d09a), sorties results/controle_campagne/.
  - Methods §8.12 : déclaration du contrôle (vi), après le (v), déclaré après observation (ordination exploratoire) ;
  - Results « Composition by genotypic category » : paragraphe de résultats inséré avant la section Dispersion,
    avec note grise de traçabilité ;
  - Discussion, première limite : effet propre de la campagne, contrôlé pour les tests de catégorie.
Chiffres (contrôlés par scripts/40) : 96 strates ; 46 détections à blocs de station, 52 à blocs station × campagne,
2 perdues (UniFrac non pondéré, passe 2, p 0,042–0,045 -> 0,065–0,068) ; R² médian de la catégorie 1,53 % après
station, 1,46 % après station × campagne ; parentaux : campagne 6,7–27,3 % de la variance, p <= 0,039 (48 strates).
python-docx requis (absent sur meso) : exécuté hors cluster, fichier déposé avec garde md5.
Usage : 67-integration_controle_campagne.py <dossier_entree> <dossier_sortie>
"""
import sys, copy, hashlib
import docx
from docx.text.paragraph import Paragraph
from docx.text.run import Run

IN, OUTD = sys.argv[1], sys.argv[2]
H = "dbdfd8991882675d965beec5719ea5c0"
assert hashlib.md5(open(f"{IN}/Article.docx", "rb").read()).hexdigest() == H, "Article.docx : md5 inattendu"
A = docx.Document(f"{IN}/Article.docx"); P = A.paragraphs


def replace_once(par, old, new):
    hits = [r for r in par.runs if old in r.text]
    assert len(hits) == 1 and hits[0].text.count(old) == 1, (old[:60], len(hits))
    hits[0].text = hits[0].text.replace(old, new)


def add_run_like(par, model_run, text, italic=None):
    el = copy.deepcopy(model_run._r); par._p.append(el)
    r = Run(el, par); r.text = text; r.italic = italic
    return r

assert P[61].text.strip() == "8.12 Pre-declared controls" and P[83].text.strip() == "Composition by genotypic category"
assert P[87].text.strip() == "Dispersion" and P[99].text.startswith("Four limits bound these conclusions.")
# ---- Methods §8.12 : contrôle (vi)
last = P[62].runs[-1]
assert P[62].text.endswith("P. toxostoma within stations."), repr(P[62].text[-40:])
add_run_like(P[62], P[62].runs[0],
    " A sixth control was declared after an exploratory ordination showed the samples of one station separating by fishing "
    "campaign, in a document committed before its own computation. (vi) Whether fishing campaign, which the models do not "
    "include within stations, could produce the category effects: at the five stations fished twice, hybrids were mostly "
    "sampled in the second campaign, so the principal model was refitted with permutations restricted within the 14 "
    "station × campaign blocks (station × year, the two 2014 fishing days at Pertuis kept separate), the share of category "
    "was re-estimated after these blocks, and the effect of campaign was tested in the parental species alone, with "
    "permutations within station × species blocks.")
# ---- Results : nouveau paragraphe avant « Dispersion »
new = copy.deepcopy(P[86]._p)
for r in new.xpath("./w:r"): new.remove(r)
P[87]._p.addprevious(new)
np_ = Paragraph(new, P[86]._parent)
body = P[85].runs[0]
add_run_like(np_, body,
    "Restricting permutations to the 14 station × campaign blocks (§8.12, control vi) left these detections unchanged in "
    "substance. The midgut on Jaccard remained significant in all three runs of both passes, and the caudal fin on weighted "
    "UniFrac in all three runs of pass 1. Of the 96 metric × tissue × run × pass strata, 46 were significant with station "
    "blocks and 52 with station × campaign blocks; the 2 lost were both on unweighted UniFrac in pass 2, with p moving from "
    "0.042–0.045 to 0.065–0.068. The share of category fitted after the station × campaign blocks (median 1.46 % over the 96 "
    "strata) was that fitted after station (1.53 %). Fishing campaign nevertheless structured composition on its own: in the "
    "parental species alone, at the five stations fished twice, it accounted for 6.7–27.3 % of variance within station and "
    "species (p ≤ 0.039 in all 48 metric × tissue × run strata). ")
grey = [r for r in P[86].runs if r.text.lstrip().startswith("[")]
assert grey, "note grise modèle introuvable"
add_run_like(np_, grey[0],
    "[Contrôle (vi), campagne de pêche : plan docs/plan_controle_campagne_2026-10-06.md, scripts/66-controle_campagne.R "
    "(commit 118d09a), sorties results/controle_campagne/ ; déclaré après observation (ordinations exploratoires du script 65, "
    "figure candidate non retenue à ce jour). Témoin de montage : la référence à blocs de station reproduit les p et R² de "
    "results/recat dans les 96 strates. À retirer avant soumission.]", italic=grey[0].italic)
# ---- Discussion, première limite
replace_once(P[99], "so that category effects are estimated mostly between stations.",
    "so that category effects are estimated mostly between stations. Station itself includes, at the five stations fished "
    "twice, a difference between fishing campaigns that accounted for 7–27 % of compositional variance in the parental "
    "species alone; restricting permutations within campaigns left the category results unchanged (§8.12, control vi), and "
    "what this campaign effect consists of — year, date or conditions of capture and handling — is not resolved by these data.")
txt = "\n".join(p.text for p in A.paragraphs)
for s in ("(vi) Whether fishing campaign", "station × campaign blocks (§8.12, control vi)", "control vi), and what this campaign"):
    assert txt.count(s) == 1, s
A.save(f"{OUTD}/Article.docx")
print("Article.docx", hashlib.md5(open(f"{OUTD}/Article.docx", "rb").read()).hexdigest())
