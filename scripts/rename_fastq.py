#!/usr/bin/env python3
"""Renomme les fastq bruts vers le nom canonique corrigé, et les SampleSheet.

Usage :
    python3 scripts/rename_fastq.py metadata/samples_all.csv --data-root data
    python3 scripts/rename_fastq.py metadata/samples_all.csv --data-root data --apply
    python3 scripts/rename_fastq.py --revert metadata/rename_manifest.csv --data-root data

Concerne les corrections où le nom de fichier ne reflète pas la vérité :
  - code espèce absent des noms (Ain 2014, individus 1036–1043) ;
  - code tissu 04 → 05 (faute de frappe, 15Avi1002).

Sans `--apply`, n'écrit RIEN : affiche le plan (dry-run). Avec `--apply`,
renomme les fastq des trois runs (R1/R2 et, si présents, I1/I2), corrige le
Sample_Name des SampleSheet (une sauvegarde `.orig` est posée à côté), et écrit
un manifeste réversible. `--revert <manifeste>` défait l'opération.

Les données brutes ne sont pas versionnées : le manifeste (dans metadata/, lui
versionné) et les `.orig` sont le seul filet. Ne pas les supprimer.
"""

import argparse
import csv
import re
import sys
from pathlib import Path

RE_FASTQ = re.compile(
    r"^(?P<name>.+)_S(?P<snum>\d+)_L001_R(?P<read>[12])_001\.fastq(?:\.gz)?$"
)


def normkey(name):
    return re.sub(r"[\s_-]+", "", name.strip()).lower()


# Seules ces corrections justifient de toucher aux fichiers bruts. On NE
# renomme PAS pour normaliser une casse, un séparateur ou un suffixe `bis` :
# ces variantes restent dans le nom de fichier d'origine, seules les
# métadonnées les régularisent.
FLAGS_A_RENOMMER = {"taxon_saisi_manuellement", "tissu_corrige"}


def a_renommer(r):
    return bool(FLAGS_A_RENOMMER & set(r["flags"].split(";")))


def canonical(r):
    """Nom canonique d'une ligne biologique, ou None si champ manquant."""
    if r["sample_type"] != "biological":
        return None
    f = (r["year"][-2:], r["site"], r["individual"],
         r["taxon_code"], r["tissue_code"], r["replicate"])
    if not all(f):
        return None
    return "".join(f)


def old_stem(rel_path):
    """Racine du nom de fichier (avant _S{n}), depuis fastq_r1."""
    m = RE_FASTQ.match(Path(rel_path).name)
    return m.group("name") if m else None


def plan_renames(rows, data_root):
    """Retourne (renames, patchmap).

    renames : liste de (old_abs, new_abs) pour tous les fichiers concernés.
    patchmap : normkey(ancien nom) -> nouveau nom canonique, pour les feuilles.
    """
    renames, patchmap, seen_dirs = [], {}, set()
    for r in rows:
        if not r["fastq_r1"] or not a_renommer(r):
            continue
        canon = canonical(r)
        stem = old_stem(r["fastq_r1"])
        if not canon or not stem or canon == stem:
            continue
        patchmap[normkey(stem)] = canon

        src = data_root / r["run_label"] / r["run"]
        fdir = (src / r["fastq_r1"]).parent
        m = RE_FASTQ.match(Path(r["fastq_r1"]).name)
        snum = m.group("snum")
        # Tous les reads du même échantillon : R1/R2 et éventuels I1/I2.
        marker = (fdir, stem, snum)
        if marker in seen_dirs:
            continue
        seen_dirs.add(marker)
        for f in sorted(fdir.glob(f"{stem}_S{snum}_*")):
            if not f.name.startswith(f"{stem}_S{snum}_"):
                continue
            new = f.with_name(canon + f.name[len(stem):])
            renames.append((f, new))
    return renames, patchmap


def patch_samplesheet(path, patchmap, apply):
    """Corrige les Sample_Name d'une SampleSheet. Retourne le nb de lignes touchées.

    Gère la feuille durance2, où Sample_Name et Sample_Plate sont fusionnés
    (valeur = nom + chiffre de plaque collé)."""
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    try:
        h = next(i for i, l in enumerate(lines) if l.startswith("Sample_ID,"))
    except StopIteration:
        return 0
    header = lines[h].split(",")
    merged = "Sample_Name" not in header and "Sample_NameSample_Plate" in header
    col = header.index("Sample_NameSample_Plate" if merged else "Sample_Name")

    n = 0
    for i in range(h + 1, len(lines)):
        if not lines[i].strip():
            continue
        parts = lines[i].split(",")
        if col >= len(parts):
            continue
        val = parts[col]
        name, tail = (val[:-1], val[-1]) if merged else (val, "")
        new = patchmap.get(normkey(name))
        if new and new != name:
            parts[col] = new + tail
            lines[i] = ",".join(parts)
            n += 1
    if apply and n:
        orig = path.with_suffix(path.suffix + ".orig")
        if not orig.exists():
            orig.write_text("\n".join(
                path.read_text(encoding="utf-8", errors="replace").splitlines()
            ) + "\n", encoding="utf-8")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return n


def samplesheets(data_root, rows):
    """Chemins des SampleSheet des runs présents (canonique ou à part)."""
    out = []
    for src in {data_root / r["run_label"] / r["run"] for r in rows}:
        cano = src / "SampleSheet.csv"
        if cano.exists():
            out.append(cano)
        for f in sorted(src.rglob("*.csv")):
            head = f.read_text(encoding="utf-8", errors="replace")
            if any(l.startswith("Sample_ID,") for l in head.splitlines()):
                out.append(f)
    return sorted(set(out))


def do_rename(args):
    data_root = Path(args.data_root).resolve()
    with open(args.samples, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    renames, patchmap = plan_renames(rows, data_root)
    if not renames:
        print("Rien à renommer : tous les noms sont déjà canoniques.")
        return

    # Vérifications avant d'écrire : sources présentes, cibles libres.
    problems = []
    for old, new in renames:
        if not old.exists():
            problems.append(f"source absente : {old}")
        if new.exists() and new != old:
            problems.append(f"cible déjà présente : {new}")
    if problems:
        sys.exit("Abandon :\n  " + "\n  ".join(problems))

    libs = len({(o.parent, o.name.split('_S')[0]) for o, _ in renames})
    print(f"{len(renames)} fichiers, {libs} librairies × runs, "
          f"{len(patchmap)} noms de SampleSheet à corriger.")
    for old, new in renames[:6]:
        print(f"  {old.relative_to(data_root)}\n    -> {new.name}")
    if len(renames) > 6:
        print(f"  … (+{len(renames) - 6})")

    if not args.apply:
        print("\nDry-run : rien n'a été modifié. Relancer avec --apply.")
        return

    manifest = Path(args.manifest)
    manifest.parent.mkdir(parents=True, exist_ok=True)
    with open(manifest, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["old", "new"])
        for old, new in renames:
            old.rename(new)
            w.writerow([str(old.relative_to(data_root)),
                        str(new.relative_to(data_root))])
    touched = sum(patch_samplesheet(s, patchmap, apply=True)
                  for s in samplesheets(data_root, rows))
    print(f"\nFait. {len(renames)} fichiers renommés, {touched} lignes de "
          f"SampleSheet corrigées.\nManifeste : {manifest}")


def do_revert(args):
    data_root = Path(args.data_root).resolve()
    with open(args.revert, newline="", encoding="utf-8") as fh:
        pairs = [(data_root / r["new"], data_root / r["old"])
                 for r in csv.DictReader(fh)]
    n = 0
    for new, old in pairs:
        if new.exists():
            new.rename(old)
            n += 1
    # Restaure les SampleSheet depuis les sauvegardes .orig.
    s = 0
    for orig in data_root.rglob("*.orig"):
        orig.replace(orig.with_suffix(""))
        s += 1
    print(f"Annulé : {n} fichiers restaurés, {s} SampleSheet restaurées.")


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("samples", nargs="?", help="metadata/samples_all.csv")
    ap.add_argument("--data-root", required=True)
    ap.add_argument("--apply", action="store_true", help="exécute (sinon dry-run)")
    ap.add_argument("--manifest", default="metadata/rename_manifest.csv")
    ap.add_argument("--revert", metavar="MANIFESTE",
                    help="défait le renommage décrit par ce manifeste")
    args = ap.parse_args()

    if args.revert:
        do_revert(args)
    elif args.samples:
        do_rename(args)
    else:
        ap.error("fournir samples_all.csv, ou --revert <manifeste>")


if __name__ == "__main__":
    main()
