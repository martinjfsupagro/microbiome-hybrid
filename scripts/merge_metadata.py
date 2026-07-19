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
import sys


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

    # -- réplicats techniques inter-runs -------------------------------------
    key = lambda r: (r["year"], r["site"], r["individual"], r["tissue_code"])
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
