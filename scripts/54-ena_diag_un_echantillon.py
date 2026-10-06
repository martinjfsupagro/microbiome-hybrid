#!/usr/bin/env python3
# scripts/54-ena_diag_un_echantillon.py — XML de diagnostic de l'échec du MODIFY du 2026-10-06.
#
# Deux MODIFY d'UN échantillon, DURANCE16S_14Per2011Ch01A (touché par les deux tables du jour) :
#   ena_update_diag_noop/     l'objet tel qu'il est DÉPOSÉ (base de scripts/53), aucune valeur changée
#   ena_update_diag_nouveau/  l'objet de ena_update_oct/ (base + date de Pertuis + host subject id)
# Le dépôt réel a été vérifié le 2026-10-06 à 11:08 (7_verifier_exhaustif.sh : 4 612 / 4 612),
# après la soumission refusée : la base de scripts/53 est donc toujours l'état déposé.
# Contrôles (bloquants) : noop == base champ pour champ ; nouveau == objet de ena_update_oct ;
# nouveau ne diffère de base que sur les deux champs, aux valeurs des tables.
import csv, os
import xml.etree.ElementTree as ET

D = "/home/martinj/work/projects/microbiome-hybrid/ena_deposit"
ALIAS = "DURANCE16S_14Per2011Ch01A"


def attrs(s):
    return {a.find("TAG").text: a for a in s.iter("SAMPLE_ATTRIBUTE")}


def plat(s):
    d = {"TITLE": s.find("TITLE").text, "accession": s.get("accession"), "alias": s.get("alias"),
         "SAMPLE_NAME": ET.tostring(s.find("SAMPLE_NAME"))}
    d.update({k: (v.find("VALUE").text or "") for k, v in attrs(s).items()})
    d["_ordre"] = tuple(attrs(s))
    return d


def un(path):
    root = ET.parse(path).getroot()
    E = [s for s in root if s.get("alias") == ALIAS]
    return root, (E[0] if len(E) == 1 else None)


r_aug, e_aug = un(f"{D}/ena_update/sample.xml")
_, e_sep = un(f"{D}/ena_update_sept/sample.xml")
_, e_oct = un(f"{D}/ena_update_oct/sample.xml")
assert e_aug is not None and e_oct is not None
base, src = (e_sep, "25/09") if e_sep is not None else (e_aug, "31/08")
print("base :", src, "| accession", base.get("accession"))

exp = {}
for t in ("ena_corrections_pertuis_dates.tsv", "ena_corrections_subject_id.tsv"):
    for r in csv.DictReader(open(f"{D}/{t}", newline="", encoding="utf-8"), delimiter="\t"):
        if r["alias"] == ALIAS:
            assert plat(base)[r["champ"]] == r["valeur_deposee"], (t, r["champ"])
            exp[r["champ"]] = r["valeur_corrigee"]
assert set(exp) == {"collection date", "host subject id"}, exp

pb, po = plat(base), plat(e_oct)
diff = {k for k in set(pb) | set(po) if pb.get(k) != po.get(k)}
assert diff == set(exp) and all(po[k] == v for k, v in exp.items()), diff
for k in sorted(exp):
    print(f"  {k} : {pb[k]!r} -> {po[k]!r}")

SUB = ('<?xml version="1.0" encoding="UTF-8"?>\n<SUBMISSION>\n  <ACTIONS>\n    <ACTION>\n'
       '      <MODIFY/>\n    </ACTION>\n  </ACTIONS>\n</SUBMISSION>\n')
for mode, e in (("noop", base), ("nouveau", e_oct)):
    out = f"{D}/ena_update_diag_{mode}"
    assert not os.path.exists(out), f"{out} existe déjà"
    os.makedirs(out)
    nr = ET.Element(r_aug.tag, r_aug.attrib); nr.append(e)
    ET.ElementTree(nr).write(f"{out}/sample.xml", encoding="UTF-8", xml_declaration=True)
    open(f"{out}/submission.xml", "w", encoding="utf-8").write(SUB)
    relu = ET.parse(f"{out}/sample.xml").getroot()
    assert len(relu) == 1 and plat(relu[0]) == plat(e) and relu[0].get("accession") == base.get("accession")
    print(f"{mode} : écrit et relu, 1 objet, identique à {'la base' if mode == 'noop' else 'ena_update_oct'}")
