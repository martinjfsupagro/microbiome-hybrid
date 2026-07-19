#!/usr/bin/env python3
"""Extrait les échantillons dont les métadonnées demandent une vérification.

Usage :
    python3 scripts/extract_a_verifier.py metadata/samples_all.csv \
            metadata/a_verifier.csv

Une ligne par librairie (et non par séquençage) : les trois runs contiennent
les mêmes 768 librairies, c'est le plan de plaque qui est en cause, pas le
séquençage. On prend donc durance1 comme référence, en signalant les noms qui
diffèrent dans les autres runs.

La colonne `question` dit ce qu'on attend de la vérification ; `reponse` est
laissée vide, à remplir par la personne qui a acquis les données.
"""

import argparse
import csv

REF_RUN = "durance1"

COLUMNS = [
    "question", "reponse",
    "sample_name", "autres_noms", "year", "site", "individual",
    "tissue_code", "extraction", "plate", "well", "sample_id", "flags",
]


def selectionner(rows):
    """Retourne (question, ligne) pour chaque échantillon à vérifier."""
    for r in rows:
        if r["sample_type"] != "biological":
            continue

        # 1. Taxon jamais saisi : Ain 2014, individus 1036 à 1043.
        if not r["taxon"]:
            yield ("taxon manquant : quelle espèce pour cet individu ?", r)

        # 2. Code tissu hors des quatre attendus.
        elif r["tissue_code"] not in {"01", "02", "03", "05"}:
            yield (f"code tissu {r['tissue_code']} inattendu : "
                   f"faute de frappe pour 05, ou 5e tissu ?", r)

        # 3. Ré-extractions : confirmer qu'il s'agit bien du même tissu.
        elif r["extraction"] == "bis":
            yield ("ré-extraction : bien le même tissu que l'extraction "
                   "initiale ?", r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    args = ap.parse_args()

    with open(args.input, newline="", encoding="utf-8") as fh:
        allrows = list(csv.DictReader(fh))

    # Noms portés par la même librairie dans les autres runs, quand ils
    # diffèrent : c'est là que se voient les suffixes perdus à la saisie.
    noms = {}
    for r in allrows:
        noms.setdefault(r["sample_id"], {})[r["run_short"]] = r["sample_name"]

    ref = [r for r in allrows if r["run_short"] == REF_RUN]
    ref.sort(key=lambda r: int(r["sample_id"]))

    out = []
    for question, r in selectionner(ref):
        autres = sorted({n for run, n in noms[r["sample_id"]].items()
                         if run != REF_RUN and n != r["sample_name"]})
        out.append({
            "question": question,
            "reponse": "",
            "sample_name": r["sample_name"],
            "autres_noms": " / ".join(autres),
            "year": r["year"], "site": r["site"],
            "individual": r["individual"],
            "tissue_code": r["tissue_code"],
            "extraction": r["extraction"],
            "plate": r["plate"], "well": r["well"],
            "sample_id": r["sample_id"],
            "flags": r["flags"],
        })

    with open(args.output, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(out)

    print(f"{len(out)} librairies à vérifier → {args.output}")
    for q in sorted({r["question"] for r in out}):
        n = sum(1 for r in out if r["question"] == q)
        print(f"  {n:3d}  {q}")


if __name__ == "__main__":
    main()
