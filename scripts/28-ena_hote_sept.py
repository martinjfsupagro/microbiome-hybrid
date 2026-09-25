#!/usr/bin/env python3
# scripts/28-ena_hote_sept.py — correction de l'identite d'hote du depot ENA PRJEB124417
# selon la classification genotypique a 25 chromosomes (septembre 2026).
#
# POURQUOI. La correction MODIFY du 2026-08-31 a pose `host scientific name` d'apres la
# classification d'aout (12 chromosomes, 59 Cn / 30 Hy / 91 Pt). Elle n'a touche ni le TITRE
# de l'echantillon ni `host common name`, restes a l'identification MORPHOLOGIQUE : 531
# echantillons disent encore « Chondrostoma sp. », et 33 ont un titre qui contredit leur
# nom scientifique. Ce script aligne les TROIS champs sur `categorie` de
# metadata/analysis_metadata.csv (septembre : 59 Cn / 42 Hy / 79 Pt ; les 22 quasi-purs sont
# des hybrides dans cette classification — le depot decrit le genotype, pas une passe
# d'analyse).
#
# PRINCIPE (repris de build_ena_modify.py). MODIFY REMPLACE l'objet entier : on part du XML
# EFFECTIVEMENT DEPOSE (ena_update/sample.xml, soumis en production le 2026-08-31 a 21:16,
# recu receipt_modify_prod_20260831_211649.xml) et on n'y change que ces trois champs. Seuls
# les echantillons modifies sont soumis ; les 41 controles et les echantillons inchanges ne
# sont pas envoyes.
#
# Sorties (ena_deposit/) :
#   ena_corrections_hote_sept.tsv   une ligne par (echantillon x champ modifie)
#   ena_update_sept/                sample.xml + submission.xml (MODIFY)   -> production
#   ena_update_sept_test/           sample.xml + submission.xml (ADD, alias suffixes, sans
#                                   accession) -> serveur de test, valide les valeurs
import csv, collections, copy, hashlib, os, sys, time
import xml.etree.ElementTree as ET

P = "/home/martinj/work/projects/microbiome-hybrid"
D = f"{P}/ena_deposit"
BASE = f"{D}/ena_update/sample.xml"
RECU = f"{D}/receipt_modify_prod_20260831_211649.xml"

SCI = {"Cn": "Chondrostoma nasus", "Pt": "Parachondrostoma toxostoma",
       "Hy": "Chondrostoma nasus x Parachondrostoma toxostoma"}
COMMON = {"Cn": "nase", "Pt": "toxostome", "Hy": "nase x toxostome hybrid"}
TISSUS = (" caudal fin ", " gill ", " midgut ", " hindgut ")

# --- classification par echantillon depose (durance1 = un echantillon par tissu et poisson)
M = [r for r in csv.DictReader(open(f"{P}/metadata/analysis_metadata.csv")) if r["run_label"] == "durance1"]
for k in ("dada2_id", "categorie", "categorie_aout_12chr", "individual_id"):
    assert k in M[0], f"colonne absente : {k}"
for r in M:
    assert r["dada2_id"].endswith("__durance1"), r["dada2_id"]
    r["stem"] = r["dada2_id"][: -len("__durance1")]   # nom d'origine de l'echantillon
cat = {r["stem"]: r for r in M}
assert len(cat) == len(M) == 727, (len(cat), len(M))

# --- XML depose et accessions de production
tree = ET.parse(BASE); root = tree.getroot()
recu = {s.get("alias"): s.get("accession") for s in ET.parse(RECU).getroot().iter("SAMPLE")}
bio = [s for s in root if s.get("accession")]
assert len(root) == 768 and len(bio) == 727, (len(root), len(bio))

def attrs(s):
    return {a.find("TAG").text: a for a in s.iter("SAMPLE_ATTRIBUTE")}

rows, keep, final = [], [], []
temoin_aout = collections.Counter()
for s in bio:
    alias, acc = s.get("alias"), s.get("accession")
    assert recu.get(alias) == acc, f"accession differente du recu pour {alias}"
    A = attrs(s)
    # cle = alias sans prefixe (identique au nom dans dada2_id). Pour 10 echantillons,
    # 'original sample name' porte une espace ou un '_' la ou alias et dada2_id portent '-'
    # (ex. '14Per2011Ch01A_bis' / alias ...14Per2011Ch01A-bis) : on le verifie explicitement.
    stem = alias[len("DURANCE16S_"):]
    orig = A["original sample name"].find("VALUE").text
    assert alias.startswith("DURANCE16S_") and orig.replace(" ", "-").replace("_", "-") == stem, (alias, orig)
    m = cat.get(stem)
    assert m is not None, f"echantillon depose absent de analysis_metadata : {stem}"
    cur_sci = A["host scientific name"].find("VALUE").text
    # TEMOIN : le depot doit porter exactement la classification d'aout (correction du 31/08)
    temoin_aout[cur_sci == SCI[m["categorie_aout_12chr"]]] += 1
    new = m["categorie"]
    title = s.find("TITLE").text
    tissu = next((t for t in TISSUS if t in title), None)
    assert tissu is not None, f"tissu introuvable dans le titre : {title!r}"
    new_title = SCI[new] + tissu + title.split(tissu, 1)[1]
    final.append((acc, new_title, SCI[new], COMMON[new]))   # etat attendu apres MODIFY, 727
    changes = []
    for champ, old, val in (("TITLE", title, new_title),
                            ("host scientific name", cur_sci, SCI[new]),
                            ("host common name", A["host common name"].find("VALUE").text, COMMON[new])):
        if old != val:
            changes.append((champ, old, val))
    if changes:
        motif = (f"classification a 25 chromosomes (sept. 2026) : {new} ; "
                 f"depot du 2026-08-31 = {m['categorie_aout_12chr']} (12 chr) pour le nom scientifique, "
                 f"titre et nom commun restes a l'identification morphologique")
        for champ, old, val in changes:
            rows.append(dict(alias=alias, accession=acc, stem=stem, individual_id=m["individual_id"],
                             champ=champ, valeur_deposee=old, valeur_corrigee=val, motif=motif))
        keep.append((s, dict((c, v) for c, _, v in changes)))

print("temoin : nom scientifique depose == classification d'aout :", dict(temoin_aout))
assert temoin_aout == {True: 727}, "le depot ne porte pas la classification d'aout : NE PAS SOUMETTRE"

def ecrire(outdir, action, strip, suffix):
    os.makedirs(outdir, exist_ok=True)
    new_root = ET.Element(root.tag, root.attrib)
    for s, ch in keep:
        e = copy.deepcopy(s)
        if "TITLE" in ch: e.find("TITLE").text = ch["TITLE"]
        A = attrs(e)
        for champ in ("host scientific name", "host common name"):
            if champ in ch: A[champ].find("VALUE").text = ch[champ]
        if strip: del e.attrib["accession"]
        if suffix: e.set("alias", e.get("alias") + suffix)
        new_root.append(e)
    ET.ElementTree(new_root).write(f"{outdir}/sample.xml", encoding="UTF-8", xml_declaration=True)
    with open(f"{outdir}/submission.xml", "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<SUBMISSION>\n  <ACTIONS>\n    <ACTION>\n'
                f'      <{action}/>\n    </ACTION>\n  </ACTIONS>\n</SUBMISSION>\n')
    return new_root

prod = ecrire(f"{D}/ena_update_sept", "MODIFY", False, None)
ecrire(f"{D}/ena_update_sept_test", "ADD", True, "_VAL" + time.strftime("%H%M%S"))

# --- CONTROLE : relu depuis le disque, chaque echantillon soumis ne differe du depot que
#     sur les champs de la table, et les valeurs sont celles de la table
base_by = {s.get("alias"): s for s in bio}
exp = collections.defaultdict(dict)
for r in rows: exp[r["alias"]][r["champ"]] = r["valeur_corrigee"]
relu = ET.parse(f"{D}/ena_update_sept/sample.xml").getroot()
def plat(s):
    d = {"TITLE": s.find("TITLE").text, "accession": s.get("accession"), "alias": s.get("alias"),
         "SAMPLE_NAME": ET.tostring(s.find("SAMPLE_NAME"))}
    d.update({k: v.find("VALUE").text for k, v in attrs(s).items()})
    d["_ordre"] = tuple(attrs(s))
    return d
hors = 0
for s in relu:
    a, b = plat(base_by[s.get("alias")]), plat(s)
    diff = {k for k in set(a) | set(b) if a.get(k) != b.get(k)}
    assert diff == set(exp[s.get("alias")]), (s.get("alias"), diff)
    for k in diff: assert b[k] == exp[s.get("alias")][k]
assert len(relu) == len(exp)

with open(f"{D}/ena_corrections_hote_sept.tsv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t"); w.writeheader(); w.writerows(rows)

assert len(final) == 727 and len({f[0] for f in final}) == 727
assert all("\t" not in x for f in final for x in f)
with open(f"{D}/ena_etat_final_hote_sept.tsv", "w", encoding="utf-8") as f:
    f.write("accession\tTITLE\thost scientific name\thost common name\n")
    for x in final: f.write("\t".join(x) + "\n")

cc = collections.Counter(r["champ"] for r in rows)
ch_sci = collections.Counter((r["valeur_deposee"], r["valeur_corrigee"]) for r in rows if r["champ"] == "host scientific name")
fin = collections.Counter()
for s in bio:
    fin[SCI[cat[s.get("alias")[len("DURANCE16S_"):]]["categorie"]]] += 1
print(f"echantillons a modifier : {len(keep)} sur 727 (controles : 0)")
print("champs modifies        :", dict(cc))
print("nom scientifique       :", {f"{a} -> {b}": n for (a, b), n in ch_sci.items()})
print("etat final attendu     :", dict(fin))
print("controle relecture     : seuls les champs de la table different, valeurs conformes")
print("md5 sample.xml (prod)  :", hashlib.md5(open(f"{D}/ena_update_sept/sample.xml", "rb").read()).hexdigest())
