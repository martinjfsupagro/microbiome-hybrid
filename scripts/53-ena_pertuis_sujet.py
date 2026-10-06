#!/usr/bin/env python3
# scripts/53-ena_pertuis_sujet.py — MODIFY du dépôt ENA PRJEB124417 : dates de Pertuis (44) et
# host subject id préfixé par la campagne (727), décision de JF du 2026-10-03.
#
# POURQUOI CE SCRIPT (incident du 2026-10-06). La commande de MEMO_corrections_restantes.md
# construisait le MODIFY avec build_ena_modify.py --deposited ena_submission/sample.xml, le XML
# d'ORIGINE du 22/08. build_ena_modify.py ne compare jamais `valeur_deposee` au XML : il écrase
# les champs listés et recopie le reste. MODIFY remplaçant l'objet entier, la soumission aurait
# ramené à leur valeur du 22/08 les 4 612 champs corrigés le 31/08 et le 25/09 (R28), sur les
# 727 échantillons. Mesuré sur meso le 2026-10-06, sans soumission.
#
# PRINCIPE (repris de scripts/28).
#   1. Base = état EFFECTIVEMENT DÉPOSÉ, reconstitué objet par objet : le XML soumis le 25/09
#      (ena_update_sept, 568 échantillons) quand l'échantillon y figure, sinon celui du 31/08
#      (ena_update, 768 objets). Accessions contrôlées contre les reçus de production.
#   2. TÉMOIN (bloquant) : la base porte exactement l'état obtenu en chaînant les tables soumises
#      (ena_corrections.tsv puis ena_corrections_hote_sept.tsv) — l'état que R28 a vérifié en
#      direct sur l'ENA le 30/09 (4 612/4 612) — et ne diffère du XML d'origine que sur ces champs.
#   3. Chaînage (bloquant) : pour chaque ligne des deux tables du jour, `valeur_deposee` == valeur
#      de la base. C'est le contrôle qui manquait à build_ena_modify.py.
#   4. Seuls les échantillons modifiés sont soumis ; les 41 contrôles ne sont pas envoyés.
#   5. Relecture depuis le disque : chaque objet soumis ne diffère de la base que sur les champs
#      des deux tables, avec leurs valeurs.
#
# Sorties (ena_deposit/) :
#   ena_update_oct/        sample.xml + submission.xml (MODIFY)  -> production
#   ena_update_oct_test/   sample.xml + submission.xml (ADD, alias suffixés, sans accession)
#   ena_etat_final_oct.tsv état attendu après MODIFY, (accession, champ, valeur) pour les champs
#                          des quatre tables chaînées
# Ne soumet rien. Lecture seule hors de ces sorties. Python système.
import csv, collections, copy, hashlib, os, sys, time
import xml.etree.ElementTree as ET

D = "/home/martinj/work/projects/microbiome-hybrid/ena_deposit"
ORIG, AUG, SEP = f"{D}/ena_submission/sample.xml", f"{D}/ena_update/sample.xml", f"{D}/ena_update_sept/sample.xml"
REC_ADD, REC_AUG, REC_SEP = (f"{D}/receipt_prod_20260825_1116.xml", f"{D}/receipt_modify_prod_20260831_211649.xml",
                             f"{D}/receipt_hote_sept_prod_20260925_180826.xml")
SOUMISES = [f"{D}/ena_corrections.tsv", f"{D}/ena_corrections_hote_sept.tsv"]            # 31/08 puis 25/09
NOUVELLES = [f"{D}/ena_corrections_pertuis_dates.tsv", f"{D}/ena_corrections_subject_id.tsv"]
for f in [ORIG, AUG, SEP, REC_ADD, REC_AUG, REC_SEP] + SOUMISES + NOUVELLES:
    assert os.path.isfile(f), f"introuvable : {f}"


def attrs(s):
    return {a.find("TAG").text: a for a in s.iter("SAMPLE_ATTRIBUTE")}


def plat(s):
    d = {"TITLE": s.find("TITLE").text, "accession": s.get("accession"), "alias": s.get("alias"),
         "SAMPLE_NAME": ET.tostring(s.find("SAMPLE_NAME"))}
    d.update({k: (v.find("VALUE").text or "") for k, v in attrs(s).items()})
    d["_ordre"] = tuple(attrs(s))
    return d


def val(s, champ):
    return s.find("TITLE").text if champ == "TITLE" else (attrs(s)[champ].find("VALUE").text or "")


def recu(p):
    r = ET.parse(p).getroot()
    return {s.get("alias"): s.get("accession") for s in r.iter("SAMPLE")}, r


# ── 1. base = état déposé ───────────────────────────────────────────────────────────────────
root_orig = ET.parse(ORIG).getroot(); root_aug = ET.parse(AUG).getroot(); root_sep = ET.parse(SEP).getroot()
acc_add, _ = recu(REC_ADD); acc_aug, r_aug = recu(REC_AUG); acc_sep, r_sep = recu(REC_SEP)
for nom, r in (("31/08", r_aug), ("25/09", r_sep)):
    assert r.get("success") == "true", f"reçu {nom} sans success=true"
orig = {s.get("alias"): s for s in root_orig}
aug = {s.get("alias"): s for s in root_aug}
sep = {s.get("alias"): s for s in root_sep}
assert len(orig) == len(aug) == 768 and len(sep) == 568, (len(orig), len(aug), len(sep))
assert set(sep) <= set(aug) == set(orig)
bio = [a for a, s in aug.items() if s.get("accession")]
assert len(bio) == 727, len(bio)
for a in bio:                                                     # accessions stables d'un reçu à l'autre
    assert acc_add.get(a) == aug[a].get("accession") == acc_aug.get(a), f"accession 31/08 : {a}"
for a in sep:
    assert sep[a].get("accession") == acc_sep.get(a) == acc_add.get(a), f"accession 25/09 : {a}"
assert set(acc_sep) == set(sep), "le reçu du 25/09 ne couvre pas exactement le XML du 25/09"
base = {a: (sep[a] if a in sep else aug[a]) for a in bio}
src = collections.Counter("25/09" if a in sep else "31/08" for a in bio)
print("base reconstituée :", dict(src), "| total", len(base))

# ── 2. témoin : la base = chaînage des tables soumises (état vérifié par R28) ───────────────
acc2alias = {base[a].get("accession"): a for a in base}
attendu, ruptures = {}, []
for t in SOUMISES:
    for r in csv.DictReader(open(t, newline="", encoding="utf-8"), delimiter="\t"):
        k = (r["accession"], r["champ"])
        if k in attendu and r["valeur_deposee"] != attendu[k]:
            ruptures.append((t, k))
        attendu[k] = r["valeur_corrigee"]
assert not ruptures, f"chaînage des tables soumises rompu : {ruptures[:3]}"
ko = [(k, v, val(base[acc2alias[k[0]]], k[1])) for k, v in attendu.items() if val(base[acc2alias[k[0]]], k[1]) != v]
print(f"témoin chaînage : {len(attendu) - len(ko)} / {len(attendu)} champs conformes à l'état vérifié (R28 : 4 612)")
assert not ko and len(attendu) == 4612, ("base non conforme à l'état déposé : NE PAS SOUMETTRE", len(ko), ko[:3])
hors = collections.Counter()
for a in bio:
    po, pb = plat(orig[a]), plat(base[a])
    for k in set(po) | set(pb):
        if po.get(k) != pb.get(k) and k not in ("accession",) and (pb["accession"], k) not in attendu:
            hors[k] += 1
print("champs différant de l'origine hors des tables soumises :", dict(hors) or "aucun")
assert not hors, "la base porte des changements non tracés par les tables : NE PAS SOUMETTRE"

# ── 3. tables du jour : chaînage sur la base ────────────────────────────────────────────────
corr = collections.defaultdict(dict); rows = 0; ecart = []
for t in NOUVELLES:
    for r in csv.DictReader(open(t, newline="", encoding="utf-8"), delimiter="\t"):
        a = r["alias"]
        assert a in base and base[a].get("accession") == r["accession"], f"alias/accession inconnus : {a}"
        assert r["champ"] in attrs(base[a]), f"attribut absent : {a} {r['champ']}"
        assert r["champ"] not in corr[a], f"champ corrigé deux fois : {a} {r['champ']}"
        if val(base[a], r["champ"]) != r["valeur_deposee"]:
            ecart.append((a, r["champ"], r["valeur_deposee"], val(base[a], r["champ"])))
        corr[a][r["champ"]] = r["valeur_corrigee"]; rows += 1
print(f"tables du jour : {rows} lignes sur {len(corr)} échantillons ; valeur_deposee == base : {rows - len(ecart)} / {rows}")
assert not ecart, ("valeur_deposee ne correspond pas à l'état déposé : NE PAS SOUMETTRE", ecart[:3])
chg = {a: {k: v for k, v in c.items() if val(base[a], k) != v} for a, c in corr.items()}
noop = rows - sum(len(c) for c in chg.values())
chg = {a: c for a, c in chg.items() if c}
print(f"champs réellement modifiés : {sum(len(c) for c in chg.values())} ; déjà à la valeur cible : {noop} ;"
      f" échantillons à soumettre : {len(chg)}")

# ── 4. écriture ─────────────────────────────────────────────────────────────────────────────
SFX = "_VAL" + time.strftime("%H%M%S")


def ecrire(outdir, action, strip, suffix):
    os.makedirs(outdir, exist_ok=True)
    nr = ET.Element(root_aug.tag, root_aug.attrib)
    for a in bio:                                   # ordre du dépôt
        if a not in chg: continue
        e = copy.deepcopy(base[a]); A = attrs(e)
        for k, v in chg[a].items(): A[k].find("VALUE").text = v
        if strip: del e.attrib["accession"]
        if suffix: e.set("alias", e.get("alias") + suffix)
        nr.append(e)
    ET.ElementTree(nr).write(f"{outdir}/sample.xml", encoding="UTF-8", xml_declaration=True)
    with open(f"{outdir}/submission.xml", "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<SUBMISSION>\n  <ACTIONS>\n    <ACTION>\n'
                f'      <{action}/>\n    </ACTION>\n  </ACTIONS>\n</SUBMISSION>\n')


for d in ("ena_update_oct", "ena_update_oct_test"):
    assert not os.path.exists(f"{D}/{d}"), f"{d} existe déjà : ne pas écraser"
ecrire(f"{D}/ena_update_oct", "MODIFY", False, None)
ecrire(f"{D}/ena_update_oct_test", "ADD", True, SFX)

# ── 5. relecture depuis le disque ───────────────────────────────────────────────────────────
for d, strip, suffix in (("ena_update_oct", False, None), ("ena_update_oct_test", True, SFX)):
    relu = ET.parse(f"{D}/{d}/sample.xml").getroot()
    assert len(relu) == len(chg), (d, len(relu))
    for s in relu:
        a = s.get("alias")[: -len(suffix)] if suffix else s.get("alias")
        pb, ps = plat(base[a]), plat(s)
        diff = {k for k in set(pb) | set(ps) if pb.get(k) != ps.get(k)}
        attendu_diff = set(chg[a]) | ({"accession"} if strip else set()) | ({"alias"} if suffix else set())
        assert diff == attendu_diff, (d, a, diff)
        for k in chg[a]: assert ps[k] == chg[a][k], (d, a, k)
    print(f"relecture {d} : {len(relu)} objets, seuls les champs des tables diffèrent de la base")
assert "<MODIFY/>" in open(f"{D}/ena_update_oct/submission.xml").read()
assert "<ADD/>" in open(f"{D}/ena_update_oct_test/submission.xml").read()

# ── état final attendu (pour 7_verifier_exhaustif.sh, tables à ajouter en fin de liste) ─────
fin = dict(attendu)
for a, c in corr.items():
    for k, v in c.items(): fin[(base[a].get("accession"), k)] = v
with open(f"{D}/ena_etat_final_oct.tsv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t"); w.writerow(["accession", "champ", "valeur"])
    for (acc, k), v in sorted(fin.items()): w.writerow([acc, k, v])
cc = collections.Counter(k for c in chg.values() for k in c)
print("champs modifiés par type :", dict(cc))
print(f"état final attendu : {len(fin)} champs (4 612 + {len(fin) - 4612})")
for d in ("ena_update_oct", "ena_update_oct_test"):
    print(f"md5 {d}/sample.xml :", hashlib.md5(open(f"{D}/{d}/sample.xml", "rb").read()).hexdigest())
print("suffixe des alias de test :", SFX)
