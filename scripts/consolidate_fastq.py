#!/usr/bin/env python3
"""Centralise les fastq R1/R2 des trois runs dans consolidated_dataset/.

Usage :
    python3 scripts/consolidate_fastq.py metadata/samples_all.csv
    python3 scripts/consolidate_fastq.py metadata/samples_all.csv --apply
    python3 scripts/consolidate_fastq.py --revert metadata/consolidate_manifest.csv

Migration unique, pas une étape de pipeline rejouable : les fastq sont
DÉPLACÉS depuis data/ vers consolidated_dataset/<run>/, un sous-dossier par run
(durance1/durance3 partagent les mêmes noms de fichiers — à plat ils
s'écraseraient). durance2, livré en .fastq, est compressé en .fastq.gz au
passage. Seuls R1/R2 bougent ; les index I1/I2 restent dans data/.

Les colonnes fastq_r1/fastq_r2 de samples_all.csv (et des CSV par run) sont
réécrites vers les nouveaux chemins, relatifs à la racine du projet. Un
manifeste réversible est écrit dans metadata/.

data/ n'est pas versionné : le manifeste (versionné) est le seul filet.
`--revert` remet les fichiers en place (et re-décompresse durance2).
"""

import argparse
import csv
import gzip
import shutil
import sys
from pathlib import Path

DEST_ROOT = "consolidated_dataset"
DATA_ROOT = "data"
# CSV dont les chemins fastq doivent suivre le déplacement.
CSVS_A_REECRIRE = [
    "metadata/samples_all.csv",
    "metadata/samples_durance1.csv",
    "metadata/samples_durance2.csv",
    "metadata/samples_durance3.csv",
]


def source_path(root, r):
    """Chemin actuel d'un fastq : data/<label>/<run>/<fastq_r1>."""
    return root / DATA_ROOT / r["run_label"] / r["run"] / r["fastq_r1"]


def plan(rows):
    """Retourne la liste des (label, src_rel, dst_rel, compress) à effectuer.

    Une entrée par fichier R1 et R2. src_rel/dst_rel sont relatifs à la racine
    du projet ; compress=True quand un .fastq devient .fastq.gz.
    """
    moves = []
    for r in rows:
        for col in ("fastq_r1", "fastq_r2"):
            rel = r[col]
            if not rel:
                continue
            label, run = r["run_label"], r["run"]
            src = f"{DATA_ROOT}/{label}/{run}/{rel}"
            base = Path(rel).name
            compress = base.endswith(".fastq")
            if compress:
                base += ".gz"
            dst = f"{DEST_ROOT}/{label}/{base}"
            moves.append((label, src, dst, compress))
    return moves


def do_consolidate(args):
    root = Path.cwd()
    with open(args.samples, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    moves = plan(rows)

    # Vérifs avant tout déplacement : sources présentes, cibles libres, pas deux
    # sources vers la même cible (collision).
    problems, dests = [], {}
    for label, src, dst, _ in moves:
        if not (root / src).exists():
            problems.append(f"source absente : {src}")
        if (root / dst).exists():
            problems.append(f"cible déjà présente : {dst}")
        if dst in dests and dests[dst] != src:
            problems.append(f"COLLISION : {dests[dst]} et {src} -> {dst}")
        dests[dst] = src
    if problems:
        sys.exit("Abandon :\n  " + "\n  ".join(problems[:30])
                 + (f"\n  … (+{len(problems)-30})" if len(problems) > 30 else ""))

    by_run = {}
    for label, *_ in moves:
        by_run[label] = by_run.get(label, 0) + 1
    n_gz = sum(1 for _, _, _, c in moves if c)
    print(f"{len(moves)} fichiers à déplacer ({n_gz} à compresser) :")
    for label in sorted(by_run):
        print(f"   {label}: {by_run[label]} fichiers -> {DEST_ROOT}/{label}/")
    for _, src, dst, c in moves[:4]:
        print(f"   {src}\n     -> {dst}{'  (gzip)' if c else ''}")
    print(f"   … (+{max(0, len(moves)-4)})")

    if not args.apply:
        print("\nDry-run : rien déplacé. Relancer avec --apply.")
        return

    for label in by_run:
        (root / DEST_ROOT / label).mkdir(parents=True, exist_ok=True)

    manifest = Path(args.manifest)
    manifest.parent.mkdir(parents=True, exist_ok=True)
    with open(manifest, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["src", "dst", "action"])
        for _, src, dst, compress in moves:
            s, d = root / src, root / dst
            if compress:
                with open(s, "rb") as fi, gzip.open(d, "wb", compresslevel=6) as fo:
                    shutil.copyfileobj(fi, fo, length=1 << 20)
                s.unlink()
            else:
                s.rename(d)
            w.writerow([src, dst, "gzip" if compress else "move"])

    rewrite_csvs(root, moves)
    print(f"\nFait. {len(moves)} fichiers dans {DEST_ROOT}/. "
          f"Manifeste : {manifest}\nChemins réécrits dans {len(CSVS_A_REECRIRE)} CSV.")


def rewrite_csvs(root, moves):
    """Réécrit fastq_r1/fastq_r2 vers les nouveaux chemins, par (label, base)."""
    newmap = {}  # (label, basename source) -> nouveau chemin projet-relatif
    for label, src, dst, _ in moves:
        newmap[(label, Path(src).name)] = dst
    for rel in CSVS_A_REECRIRE:
        p = root / rel
        if not p.exists():
            continue
        with open(p, newline="", encoding="utf-8") as fh:
            rd = csv.DictReader(fh)
            fields, data = rd.fieldnames, list(rd)
        for r in data:
            for col in ("fastq_r1", "fastq_r2"):
                if r.get(col):
                    r[col] = newmap.get((r["run_label"], Path(r[col]).name), r[col])
        with open(p, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            w.writeheader()
            w.writerows(data)


def do_revert(args):
    root = Path.cwd()
    with open(args.revert, newline="", encoding="utf-8") as fh:
        entries = list(csv.DictReader(fh))
    n = 0
    for e in entries:
        s, d = root / e["src"], root / e["dst"]
        if not d.exists():
            continue
        s.parent.mkdir(parents=True, exist_ok=True)
        if e["action"] == "gzip":
            with gzip.open(d, "rb") as fi, open(s, "wb") as fo:
                shutil.copyfileobj(fi, fo, length=1 << 20)
            d.unlink()
        else:
            d.rename(s)
        n += 1
    print(f"Annulé : {n} fichiers remis dans {DATA_ROOT}/. "
          f"Pense à régénérer les CSV (build + merge) pour restaurer les chemins.")


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("samples", nargs="?", help="metadata/samples_all.csv")
    ap.add_argument("--apply", action="store_true", help="exécute (sinon dry-run)")
    ap.add_argument("--manifest", default="metadata/consolidate_manifest.csv")
    ap.add_argument("--revert", metavar="MANIFESTE")
    args = ap.parse_args()

    if args.revert:
        do_revert(args)
    elif args.samples:
        do_consolidate(args)
    else:
        ap.error("fournir samples_all.csv, ou --revert <manifeste>")


if __name__ == "__main__":
    main()
