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


# Mesures faisant autorité, fournies par le collègue quand le xlsx est en
# conflit (deux lignes divergentes pour le même individu). Clé : (année sur
# 2 chiffres, site, individu) → (size_cm, weight_g, sex). Le sexe est repris de
# la ligne du xlsx dont la taille/poids correspond à la valeur retenue.
MESURES_CORRIGEES = {
    ("15", "Jus", "1006"): (15, 41, "X"),
    ("15", "Jus", "1007"): (17, 51, "M"),
    ("15", "Jus", "1008"): (16, 43, "X"),
}


def _sex(v):
    """Normalise le sexe : x/X → X (non défini), NA conservé (juvénile)."""
    s = str(v).strip()
    if s.lower() == "x":
        return "X"
    return s  # M, F, NA


def load_measurements(path):
    """Indexe taille/poids/sexe par individu depuis HotuToxo_taillepoids.xlsx.

    Clé : (année sur 2 chiffres, site, individu), SANS le taxon — le code
    séquençage `Ch` est un chondrostome non résolu, l'espèce du xlsx peut donc
    différer sur le même poisson. Taille, poids et sexe sont propres au poisson :
    la jointure se fait sur son identité, pas sur son étiquette.

    Taille en cm, poids en g. Sexe : M / F / X (non défini, `x` et `X` du xlsx
    homogénéisés) / NA (juvénile).

    Un individu peut avoir plusieurs lignes (mesures dupliquées) : par champ, si
    les valeurs présentes s'accordent on la garde, sinon on la laisse vide. Un
    individu de MESURES_CORRIGEES reçoit les valeurs faisant autorité. Retourne
    {clé: (size, weight, sex, status)} avec status ∈ {ok, conflit, corrige}.
    """
    import openpyxl
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True).active
    rows = list(ws.iter_rows(values_only=True))[1:]  # saute l'en-tête

    by = collections.defaultdict(lambda: {"size": set(), "weight": set(),
                                           "sex": set()})
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
        if r[8] is not None and str(r[8]).strip():
            by[k]["sex"].add(_sex(r[8]))

    def one(s):
        return (next(iter(s)) if len(s) == 1 else "")

    out = {}
    for k, v in by.items():
        if k in MESURES_CORRIGEES:
            out[k] = (*MESURES_CORRIGEES[k], "corrige")
            continue
        conflit = any(len(v[f]) > 1 for f in ("size", "weight", "sex"))
        out[k] = (one(v["size"]), one(v["weight"]), one(v["sex"]),
                  "conflit" if conflit else "ok")
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

    # -- taille / poids / sexe par individu (optionnel) ----------------------
    # Mesures propres au poisson : appliquées à tous ses tissus et tous les runs.
    for r in rows:
        r["size_cm"], r["weight_g"], r["sex"] = "", "", ""
    if fields is not None:
        fields = fields + ["size_cm", "weight_g", "sex"]
    if args.measurements:
        meas = load_measurements(args.measurements)
        n_ok = n_abs = n_conf = n_corr = 0
        for r in bio:
            k = (r["year"][-2:], r["site"], r["individual"])
            hit = meas.get(k)
            if hit is None:
                n_abs += 1
                continue
            size, weight, sex, status = hit
            # Affectation champ par champ : un champ qui diverge est resté vide
            # (cf. load_measurements), les autres sont repris. On flague le
            # conflit sans jeter les mesures cohérentes.
            r["size_cm"], r["weight_g"], r["sex"] = size, weight, sex
            if status == "conflit":
                r["flags"] = ";".join(
                    [f for f in r["flags"].split(";") if f] + ["mesures_conflit"])
                n_conf += 1
            elif status == "corrige":
                r["flags"] = ";".join(
                    [f for f in r["flags"].split(";") if f] + ["mesures_corrigees"])
                n_corr += 1
            else:
                n_ok += 1
        indiv = len({(r["year"][-2:], r["site"], r["individual"]) for r in bio})
        print(f"\n-- taille/poids/sexe : {n_ok} lignes renseignées, {n_corr} "
              f"corrigées, {n_abs} sans mesure, {n_conf} en conflit "
              f"({indiv} individus séquencés) --")

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
