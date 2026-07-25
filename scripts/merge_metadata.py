#!/usr/bin/env python3
"""Fusionne les métadonnées de plusieurs runs et diagnostique le plan.

Usage :
    python3 scripts/merge_metadata.py metadata/samples_*.csv -o metadata/samples_all.csv

Au-delà de la concaténation, signale les deux choses qui décident de ce qui
sera analysable :

1. les réplicats techniques — un même (année, site, individu, tissu) séquencé
   dans plusieurs runs. Ce sont eux qui permettent d'estimer l'effet run ;
2. la confusion entre le run et les facteurs biologiques. Si un taxon ou un
   site n'apparaît que dans un run, son effet et l'effet lot sont le même
   paramètre et aucune correction a posteriori ne les séparera.
"""

import argparse
import collections
import csv
import re
import sys


def load_measurements(path):
    """Indexe taille/poids par individu depuis HotuToxo_taillepoids.xlsx.

    Clé : (année sur 2 chiffres, site, individu), SANS le taxon — le code
    séquençage `Ch` est un chondrostome non résolu, l'espèce du xlsx peut donc
    différer sur le même poisson. La taille et le poids, eux, sont propres au
    poisson : la jointure se fait sur son identité, pas sur son étiquette.

    Un individu peut avoir plusieurs lignes (mesures dupliquées) : si elles
    s'accordent (aux valeurs vides près) on garde la valeur ; sinon on la laisse
    vide et on signalera le conflit. Retourne {clé: (size, weight, conflit)}.
    """
    import openpyxl
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True).active
    rows = list(ws.iter_rows(values_only=True))[1:]  # saute l'en-tête

    by = collections.defaultdict(lambda: {"size": set(), "weight": set()})
    for r in rows:
        if not r or r[0] is None:
            continue
        m = re.match(r"^(14|15)([A-Za-z]{3})(\d+)([A-Za-z]{2})$", str(r[0]).strip())
        if not m:
            continue  # lignes hors nomenclature (chevesne Sc, etc.)
        k = (m.group(1), m.group(2), m.group(3))
        if isinstance(r[6], (int, float)):
            by[k]["size"].add(r[6])
        if isinstance(r[7], (int, float)):
            by[k]["weight"].add(r[7])

    out = {}
    for k, v in by.items():
        conflit = len(v["size"]) > 1 or len(v["weight"]) > 1
        size = next(iter(v["size"])) if len(v["size"]) == 1 else ""
        weight = next(iter(v["weight"])) if len(v["weight"]) == 1 else ""
        out[k] = (("", "", True) if conflit else (size, weight, False))
    return out


def crosstab(rows, key, runs, label):
    """Affiche key × run et signale les niveaux présents dans un seul run."""
    t = collections.Counter((r[key] or "(vide)", r["run_short"]) for r in rows)
    levels = sorted({k[0] for k in t})
    w = max((len(x) for x in levels), default=8) + 2
    print(f"\n-- {label} × run --")
    print(" " * w + "".join(f"{r:>12s}" for r in runs) + f"{'total':>9s}")
    single = []
    for lv in levels:
        counts = [t.get((lv, r), 0) for r in runs]
        print(f"{lv:{w}s}" + "".join(f"{c:12d}" for c in counts) + f"{sum(counts):9d}")
        if sum(1 for c in counts if c) == 1 and sum(counts):
            single.append(lv)
    if single:
        print(f"  /!\\ confondu avec le run (présent dans un seul run) : "
              f"{', '.join(single)}")
    return single


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--measurements", default="",
                    help="HotuToxo_taillepoids.xlsx : ajoute size/weight par "
                         "individu")
    args = ap.parse_args()

    rows, fields = [], None
    for path in args.inputs:
        with open(path, newline="", encoding="utf-8") as fh:
            rd = csv.DictReader(fh)
            if fields is None:
                fields = list(rd.fieldnames)
            elif list(rd.fieldnames) != fields:
                sys.exit(f"Colonnes incompatibles dans {path}")
            n = 0
            for r in rd:
                rows.append(r)
                n += 1
        print(f"{path}: {n} lignes")

    # Étiquette de run courte et lisible : celle posée par build_metadata.py
    # (--label), à défaut la date en tête du nom de dossier du run.
    for r in rows:
        r["run_short"] = (r.get("run_label")
                          or (r["run"].split("_")[0] if r["run"] else "?"))
    runs = sorted({r["run_short"] for r in rows})

    bio = [r for r in rows if r["sample_type"] == "biological"]
    print(f"\ntotal : {len(rows)} lignes, {len(bio)} biologiques, "
          f"{len(runs)} runs")

    # -- taille / poids par individu (optionnel) -----------------------------
    # Mesures propres au poisson : appliquées à tous ses tissus et tous les runs.
    for r in rows:
        r["size"], r["weight"] = "", ""
    if fields is not None:
        fields = fields + ["size", "weight"]
    if args.measurements:
        meas = load_measurements(args.measurements)
        n_ok = n_abs = n_conf = 0
        for r in bio:
            k = (r["year"][-2:], r["site"], r["individual"])
            hit = meas.get(k)
            if hit is None:
                n_abs += 1
                continue
            size, weight, conflit = hit
            if conflit:
                r["flags"] = ";".join(
                    [f for f in r["flags"].split(";") if f] + ["mesures_conflit"])
                n_conf += 1
                continue
            r["size"], r["weight"] = size, weight
            n_ok += 1
        indiv = len({(r["year"][-2:], r["site"], r["individual"]) for r in bio})
        print(f"\n-- taille/poids : {n_ok} lignes renseignées, {n_abs} sans "
              f"mesure, {n_conf} en conflit ({indiv} individus séquencés) --")

    # -- réplicats techniques inter-runs -------------------------------------
    # `extraction` fait partie de la clé : une ré-extraction (`bis`) du même
    # tissu est un réplicat d'extraction, pas un réplicat de run. Les confondre
    # ferait passer un effet extraction pour un effet run.
    key = lambda r: (r["year"], r["site"], r["individual"],
                     r["tissue_code"], r["extraction"])
    seen = collections.defaultdict(set)
    for r in bio:
        seen[key(r)].add(r["run_short"])
    reps = {k: v for k, v in seen.items() if len(v) > 1}
    print(f"\n-- réplicats techniques inter-runs : {len(reps)} --")
    for k, v in list(reps.items())[:15]:
        print(f"   {'/'.join(k)} : {', '.join(sorted(v))}")
    if not reps:
        print("   Aucun. L'effet run ne pourra pas être estimé directement ;")
        print("   les mocks et blancs de chaque run deviennent le seul ancrage.")

    # -- confusion run × facteurs -------------------------------------------
    for k, lbl in (("taxon", "Taxon"), ("site", "Site"),
                   ("year", "Année"), ("tissue_code", "Tissu")):
        crosstab(bio, k, runs, lbl)

    # -- contrôles par run ---------------------------------------------------
    print("\n-- contrôles par run --")
    ct = collections.Counter((r["sample_type"], r["run_short"])
                             for r in rows if r["sample_type"] != "biological")
    types = sorted({k[0] for k in ct})
    print(f"{'':12s}" + "".join(f"{r:>12s}" for r in runs))
    for t in types:
        print(f"{t:12s}" + "".join(f"{ct.get((t, r), 0):12d}" for r in runs))

    # -- collisions de noms --------------------------------------------------
    # Un même nom dans plusieurs runs est attendu (reséquençage) ; seul un
    # doublon à l'intérieur d'un run est une anomalie.
    dup = [f"{n} ({r})" for (n, r), c in collections.Counter(
        (x["sample_name"], x["run_short"]) for x in rows).items() if c > 1]
    if dup:
        print(f"\n/!\\ {len(dup)} noms dupliqués au sein d'un même run : "
              f"{', '.join(dup[:10])}")

    with open(args.output, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields + ["run_short"])
        w.writeheader()
        w.writerows(rows)
    print(f"\n→ {args.output}")


if __name__ == "__main__":
    main()
