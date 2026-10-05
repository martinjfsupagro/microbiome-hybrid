#!/usr/bin/env python3
"""46-corrections_bib.py — propage dans docs/biblio/microbiome_hybrid_all_refs.bib les deux corrections signalées le
2026-10-03 (note grise de l'introduction) : Small et al. (c2018highly) daté 2019 comme son DOI ; corégone
(m2018intestinal) remplacé par la version publiée (Sevellec et al. 2019, Ecol Evol, 10.1002/ece3.5676), le préprint
étant gardé en note. Métadonnées : docs/biblio/crossref_bib_fix.json (Crossref, 2026-10-05). Clés inchangées."""
import re, json, hashlib, sys
B = "docs/biblio/microbiome_hybrid_all_refs.bib"
EXP = sys.argv[1]  # md5 attendu du .bib avant correction
t = open(B, encoding="utf-8").read(); assert hashlib.md5(t.encode("utf-8")).hexdigest() == EXP, "md5 .bib inattendu"
M = json.load(open("docs/biblio/crossref_bib_fix.json", encoding="utf-8"))
class _E:
    def __init__(self, s): self.s = s
    def group(self, i=0): return self.s
def entry(key):
    i = t.find("{" + key + ",")
    assert i > 0 and t.count("{" + key + ",") == 1, key
    i = t.rfind("@", 0, i); j = t.find("\n@", i + 1); j = len(t) if j < 0 else j
    return _E(t[i:j].rstrip())
e = entry("c2018highly"); old = e.group(0)
new = re.sub(r"year = \{2018\}", "year = {2019}", old, count=1); assert new != old
new = new.replace("note = {", "note = {année corrigée 2018 -> 2019 d'après Crossref (2026-10-05) ; ", 1)
t = t.replace(old, new)
e = entry("m2018intestinal"); old = e.group(0); s = M["10.1002/ece3.5676"]
def setf(txt, field, value):
    pat = re.compile(r"(\n\s*" + field + r"\s*=\s*\{)[^\n]*?(\},?\n)")
    if pat.search(txt): return pat.sub(lambda m: m.group(1) + value + m.group(2), txt, count=1)
    return txt.replace("\n  doi = {", "\n  " + field + " = {" + value + "},\n  doi = {", 1)
new = old
new = setf(new, "title", "Evidence for host effect on the intestinal microbiota of whitefish (Coregonus sp.) species pairs and their hybrids")
new = setf(new, "author", " and ".join(s["authors"]))
new = setf(new, "year", str(s["year"]))
new = setf(new, "journal", s["journal"])
new = setf(new, "volume", s["volume"]); new = setf(new, "number", s["issue"]); new = setf(new, "pages", s["page"].replace("-", "--"))
new = setf(new, "doi", "10.1002/ece3.5676"); new = setf(new, "url", "https://doi.org/10.1002/ece3.5676")
new = setf(new, "note", "version publiée (Crossref, 2026-10-05) ; préprint bioRxiv 10.1101/312231 (2018), dont le résumé ci-dessus est tiré ; sources: hybrides")
assert new.count("\n") == old.count("\n") + 3 and "keywords" in new and "abstract" in new, "structure"
t = t.replace(old, new)
open(B, "w", encoding="utf-8").write(t)
print("ok", hashlib.md5(t.encode("utf-8")).hexdigest())
