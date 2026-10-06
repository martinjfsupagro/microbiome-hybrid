#!/usr/bin/env python3
"""64-etat_ena_1006.py — met l'article (§9) et le supplément (Note S2 « ENA metadata corrections » et « Metadata
completeness », Note S3) à l'état du dépôt ENA après la correction du 2026-10-06 :
  - MODIFY soumis le 2026-10-06 (reçu ena_deposit/receipt_pertuis_sujet_prod_20261006_111847.xml, success=true) :
    collection date des 44 échantillons de Pertuis (16 au 2014-07-07, 28 au 2014-08-20 ; table
    ena_corrections_pertuis_dates.tsv) et host subject id préfixé par la campagne sur les 727 échantillons
    biologiques (156 valeurs distinctes -> 180 ; table ena_corrections_subject_id.tsv) ; 15Per2015Ch03A reçoit
    14Per2015 comme ses trois autres tissus ;
  - vérification sur l'archive le 2026-10-06 à 15:02 par JF (7_verifier_exhaustif.sh sur les quatre tables
    chaînées) : 727 échantillons interrogés, 5 339 champs conformes, 0 non conforme, 0 introuvable
    (ena_deposit/verification_cumulee_20261006_1502.txt).
python-docx requis (absent sur meso) : exécuté hors cluster, fichiers déposés avec garde md5.
Usage : 64-etat_ena_1006.py <dossier_entree> <dossier_sortie>
"""
import sys, copy, hashlib
import docx
from docx.text.run import Run

IN, OUTD = sys.argv[1], sys.argv[2]
MD5 = {"Article.docx": "cd2e6b6cf9b00be6624b2c979a1a84b8", "Supplementary_Data.docx": "43a118b1db95af90694cd2047c6a1038"}
for f, h in MD5.items():
    assert hashlib.md5(open(f"{IN}/{f}", "rb").read()).hexdigest() == h, f"{f} : md5 inattendu"


def replace_once(par, old, new):
    hits = [r for r in par.runs if old in r.text]
    assert len(hits) == 1 and hits[0].text.count(old) == 1, (old[:60], len(hits))
    hits[0].text = hits[0].text.replace(old, new)


def set_segments(par, k, segs):
    """Remplace le texte du paragraphe à partir du run k par les segments (texte, italique) ; runs vides avant k gardés."""
    runs = par.runs
    assert all(r.text == "" for r in runs[:k]) and runs[k].text, "structure inattendue"
    base = runs[k]._r
    for r in runs[k + 1:]:
        r._r.getparent().remove(r._r)
    prev = base
    for j, (t, it) in enumerate(segs):
        el = base if j == 0 else copy.deepcopy(base)
        if j: prev.addnext(el)
        rr = Run(el, par); rr.text = t; rr.italic = True if it else False
        prev = el

# ------------------------------------------------------------------ article, §9
A = docx.Document(f"{IN}/Article.docx"); P = A.paragraphs
assert P[63].text.startswith("9. Reproducibility")
replace_once(P[66],
    "ENA metadata were corrected after the initial deposit to field-record coordinates, exact collection dates and genotype-resolved "
    "host identities, without altering any accession, alias or sequence file (Supplementary Note S2); host subject identifiers are "
    "reused between years (Supplementary Note S3). Collection dates are given at day resolution for every station except Pertuis, "
    "where the two 2014 fishing campaigns are deposited as the interval 2014-07-07/2014-08-20.",
    "ENA metadata were corrected after the initial deposit to field-record coordinates, exact collection dates, genotype-resolved "
    "host identities and campaign-prefixed host subject identifiers, without altering any accession, alias or sequence file, and the "
    "corrected state was verified against the archive (5,339 fields on 727 samples; Supplementary Note S2); host subject identifiers "
    "reused between years in the field records are disambiguated by the campaign prefix (Supplementary Note S3). Collection dates are "
    "given at day resolution for every station, the two 2014 fishing campaigns at Pertuis being dated separately (2014-07-07 and "
    "2014-08-20).")
assert P[67].text.startswith("[Pertuis : les individus sont désormais assignés") and len(P[67].runs) == 1
P[67].runs[0].text = ("[ENA : MODIFY du 2026-10-06 (dates des deux pêches de Pertuis, 44 échantillons ; host subject id préfixé par la "
                      "campagne, 727 échantillons) — reçu ena_deposit/receipt_pertuis_sujet_prod_20261006_111847.xml, success=true, "
                      "accessions inchangées ; vérifié sur l'archive par JF le 2026-10-06 à 15:02 : 5 339 champs conformes sur 727 "
                      "échantillons, aucun écart (ena_deposit/verification_cumulee_20261006_1502.txt). À retirer avant soumission.]")
A.save(f"{OUTD}/Article.docx")

# ------------------------------------------------------------------ supplément
S = docx.Document(f"{IN}/Supplementary_Data.docx"); Q = S.paragraphs
assert Q[46].text.startswith("ENA metadata corrections.") and Q[47].text.startswith("Metadata completeness.")
replace_once(Q[46], "Neither correction altered a sample accession, an alias or a sequence file.",
    "A third correction, on 2026-10-06, dated the 44 Pertuis samples to their fishing campaign (2014-07-07 or 2014-08-20) and "
    "prefixed the host subject id of the 727 biological samples with the campaign (Note S3), 771 fields in all. The cumulative "
    "state left by the three corrections was then verified against the archive: 727 samples queried, 5,339 fields conforming, none "
    "discrepant and no sample missing. None of the corrections altered a sample accession, an alias or a sequence file.")
replace_once(Q[47], "Collection dates are given at day resolution for every station except Pertuis, where the two 2014 fishing "
    "campaigns are deposited as the interval 2014-07-07/2014-08-20.",
    "Collection dates are given at day resolution for every station, the two 2014 fishing campaigns at Pertuis being dated "
    "separately (2014-07-07 and 2014-08-20).")
replace_once(Q[84], "Note S3. Host subject identifiers are reused between years",
             "Note S3. Host subject identifiers are prefixed with the sampling campaign")
set_segments(Q[85], 3, [(
    "In the field records, fish identifiers (e.g. Bue1004) were assigned per station and per sampling campaign, and 24 of them were "
    "reused between the 2014 and 2015 campaigns for different individuals. As first deposited, the MIxS attribute 'host subject id' "
    "carried these identifiers, so that grouping the samples by it merged 24 pairs of distinct fish and yielded 156 apparent "
    "individuals instead of 180.", False)])
set_segments(Q[86], 4, [
    ("Since 2026-10-06 the deposited 'host subject id' is prefixed with the campaign (e.g. 14Bue1004 and 15Bue1004) and identifies "
     "the 180 individuals unambiguously — 79 ", False), ("Parachondrostoma toxostoma", True), (", 59 ", False),
    ("Chondrostoma nasus", True),
    (" and 42 hybrids. One sample, 15Per2015Ch03A, carries a mistyped campaign prefix in its alias: the fish was collected in 2014 and "
     "its three other tissues are named 14Per2015Ch01A, 02A and 05A. Its host subject id is 14Per2015, like those of its other tissues, "
     "and its collection date is that of its 2014 campaign; the alias itself is left unchanged, an alias being an identifier rather "
     "than a datum. Each individual is represented by four tissues, and each tissue by two library preparations (see Table S3).", False)])
set_segments(Q[87], 5, [(
    "[Note réécrite le 2026-10-06 après la correction MODIFY du même jour (host subject id préfixé par la campagne, 727 échantillons) "
    "et sa vérification sur l'archive par JF (5 339 champs conformes, ena_deposit/verification_cumulee_20261006_1502.txt). "
    "À retirer avant soumission.]", True)])
txt = "\n".join(p.text for p in S.paragraphs)
assert "2014-07-07/2014-08-20" not in txt and "reused between years" not in txt and txt.count("5,339") == 1
S.save(f"{OUTD}/Supplementary_Data.docx")
for f in MD5:
    print(f, hashlib.md5(open(f"{OUTD}/{f}", "rb").read()).hexdigest())
