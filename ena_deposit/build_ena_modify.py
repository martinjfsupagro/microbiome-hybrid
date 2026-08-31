#!/usr/bin/env python3
"""Construit le sample.xml de MODIFICATION du depot ENA PRJEB124417.

PRINCIPE : on ne REGENERE pas le XML depuis les sources — on PATCHE le XML
effectivement depose, en n'appliquant que les differences listees dans
ena_corrections.tsv. Garantie : aucun attribut autre que les 5 corriges ne peut
changer par effet de bord, et les 41 controles restent bit-a-bit identiques.

C'est important parce que l'action MODIFY de l'ENA REMPLACE l'objet entier :
tout attribut absent du XML soumis serait EFFACE du depot.

Usage:
    python3 build_ena_modify.py \
        --deposited ena_submission/sample.xml \
        --corrections ena_corrections.tsv \
        --receipt receipt_prod_20260825_1116.xml \
        --outdir ena_update
"""
import argparse, csv, os, sys, collections
import xml.etree.ElementTree as ET

CHAMPS_ATTENDUS = {
    "geographic location (latitude)",
    "geographic location (longitude)",
    "geographic location (region and locality)",
    "collection date",
    "host scientific name",
    "host subject id",
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--deposited", required=True)
    ap.add_argument("--corrections", required=True, action="append",
                    help="table de corrections ; repetable pour en cumuler plusieurs")
    ap.add_argument("--receipt", required=True)
    ap.add_argument("--outdir", default="ena_update")
    ap.add_argument("--drop-undecided", action="store_true",
                    help="exclut les lignes dont le motif commence par 'A TRANCHER'")
    ap.add_argument("--strip-accession", action="store_true",
                    help="n'ecrit PAS les accessions ERS (variante pour un ADD de "
                         "validation sur le serveur de test, qui ne connait pas les "
                         "accessions de production)")
    ap.add_argument("--action", default="MODIFY", choices=["MODIFY", "ADD"],
                    help="action ecrite dans submission.xml")
    ap.add_argument("--alias-suffix", default=None,
                    help="suffixe ajoute a chaque alias. Sert a creer, sur le serveur "
                         "de test, des objets JETABLES sous des alias qui n'entrent pas "
                         "en collision avec ceux de production, afin de faire valider "
                         "les VALEURS corrigees par le checklist.")
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)

    # --- accessions ERS, depuis le recu de production
    rec = ET.parse(a.receipt).getroot()
    acc = {s.get("alias"): s.get("accession") for s in rec.iter("SAMPLE")}
    print(f"recu           : {len(acc)} accessions ERS")

    # --- corrections
    corr = collections.defaultdict(dict)
    undecided, rows = collections.Counter(), 0
    for chemin in a.corrections:
        n_f = 0
        with open(chemin, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                if r["champ"] not in CHAMPS_ATTENDUS:
                    sys.exit(f"ERREUR : champ inattendu {r['champ']!r} dans {chemin}")
                if r["motif"].startswith("A TRANCHER"):
                    undecided[r["champ"]] += 1
                    if a.drop_undecided:
                        continue
                if r["champ"] in corr[r["alias"]]:
                    sys.exit(f"ERREUR : {r['champ']!r} corrige deux fois pour {r['alias']}")
                corr[r["alias"]][r["champ"]] = r["valeur_corrigee"]
                rows += 1; n_f += 1
        print(f"  {chemin} : {n_f} lignes")
    print(f"corrections    : {rows} lignes sur {len(corr)} echantillons")
    if undecided:
        state = "EXCLUES" if a.drop_undecided else "INCLUSES"
        print(f"  dont 'A TRANCHER' ({state}) : {dict(undecided)}")

    # --- patch du XML depose
    tree = ET.parse(a.deposited)
    root = tree.getroot()
    applied, missing_attr, untouched = 0, [], 0
    for s in list(root):
        alias = s.get("alias")
        if alias not in corr:
            untouched += 1
            continue
        if alias not in acc:
            sys.exit(f"ERREUR : pas d'accession ERS pour {alias}")
        if not a.strip_accession:
            s.set("accession", acc[alias])      # cible explicite du MODIFY
        attrs = {x.find("TAG").text: x for x in s.iter("SAMPLE_ATTRIBUTE")}
        for champ, val in corr[alias].items():
            node = attrs.get(champ)
            if node is None:
                missing_attr.append((alias, champ)); continue
            node.find("VALUE").text = val
            applied += 1

    print(f"echantillons modifies : {len(corr)} | inchanges : {untouched}")
    print(f"valeurs appliquees    : {applied}")
    if missing_attr:
        print(f"ATTENTION : {len(missing_attr)} attribut(s) absent(s) du XML depose")
        for m in missing_attr[:5]: print("   ", m)

    if a.alias_suffix:
        n_sfx = 0
        for s in root:
            s.set("alias", s.get("alias") + a.alias_suffix)
            n_sfx += 1
        print(f"alias suffixes        : {n_sfx} (suffixe {a.alias_suffix!r})")

    out = os.path.join(a.outdir, "sample.xml")
    tree.write(out, encoding="UTF-8", xml_declaration=True)

    sub = os.path.join(a.outdir, "submission.xml")
    with open(sub, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<SUBMISSION>\n  <ACTIONS>\n    <ACTION>\n'
                f'      <{a.action}/>\n'
                '    </ACTION>\n  </ACTIONS>\n</SUBMISSION>\n')
    print(f"\necrit : {out}\n        {sub}")

if __name__ == "__main__":
    main()
