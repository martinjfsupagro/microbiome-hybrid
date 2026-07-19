#!/usr/bin/env python3
"""Construit le fichier de métadonnées à partir de la SampleSheet d'un run.

Usage :
    python3 scripts/build_metadata.py <rundir> <sortie.csv>

Parse les noms d'échantillons selon le schéma
    {année}{Site}{individu}{Taxon}{tissu}{réplicat}
en normalisant au préalable les anomalies de saisie (espaces, tirets, casse).
Chaque anomalie corrigée est tracée dans la colonne `flags` : rien n'est
silencieusement réparé.
"""

import csv
import re
import sys
from pathlib import Path

TAXONS = {
    "ch": ("chevesne", "Squalius cephalus"),
    "cn": ("hotu", "Chondrostoma nasus"),
    "pt": ("toxostome", "Parachondrostoma toxostoma"),
}

# Le code tissu (01/02/03/05) n'est pas encore relié à un tissu nommé.
# Les 4 blancs (Blanc-Caudal/Branchie/Midgut/Hindgut) donnent les 4 niveaux
# attendus ; compléter ce dictionnaire une fois la correspondance confirmée.
TISSUS = {}

RE_SAMPLE = re.compile(
    r"^(?P<year>14|15)"
    r"(?P<site>[A-Za-z]{3})"
    r"(?P<indiv>\d{4})"
    r"(?P<taxon>[A-Za-z]{2})?"
    r"(?P<tissue>\d{2})"
    r"(?P<rep>[A-Z])$",
    re.IGNORECASE,
)


def read_samplesheet(path):
    """Retourne les lignes de la section [Data] comme dicts."""
    with open(path, newline="", encoding="utf-8", errors="replace") as fh:
        lines = fh.read().splitlines()
    try:
        start = next(i for i, l in enumerate(lines) if l.startswith("Sample_ID,"))
    except StopIteration:
        sys.exit(f"Section [Data] introuvable dans {path}")
    return list(csv.DictReader(lines[start:]))


def classify(raw):
    """Type d'échantillon d'après le nom brut."""
    low = raw.lower()
    if low.startswith("empty"):
        return "empty"
    if low.startswith("blanc"):
        return "blank"
    if low.startswith("mock"):
        return "mock"
    if re.match(r"^t[-_ ]?\d+$", low):
        return "temoin"
    return "biological"


def parse_name(raw):
    """Normalise puis décompose un nom. Retourne (champs, flags)."""
    flags = []
    name = raw.strip()

    if name.lower().endswith("_bis"):
        name = name[:-4]
        flags.append("bis")

    # Chez Caa/Jus 2015, 38 échantillons portent le code tissu «0» au lieu de
    # «02» : pour chacun de ces individus les tissus 01/03/05 existent et 02
    # manque, et le total retombe sur 39 individus × 4 tissus. Corrigé, tracé.
    m0 = re.match(r"^(.*[A-Za-z]{2})0([A-Z])$", name)
    if m0:
        name = f"{m0.group(1)}02{m0.group(2)}"
        flags.append("tissu_0_corrige_02")

    if " " in name:
        flags.append("espace_interne")
    if "-" in name:
        flags.append("tiret_interne")
    name = re.sub(r"[\s-]+", "", name)

    m = RE_SAMPLE.match(name)
    if not m:
        return None, flags + ["non_parse"]

    site_raw = m.group("site")
    site = site_raw.capitalize()
    if site_raw != site:
        flags.append("casse_site")

    taxon_raw = m.group("taxon")
    if taxon_raw is None:
        taxon_code, taxon_fr, taxon_lat = "", "", ""
        flags.append("taxon_absent")
    else:
        key = taxon_raw.lower()
        if taxon_raw != taxon_raw.capitalize():
            flags.append("casse_taxon")
        if key not in TAXONS:
            flags.append("taxon_inconnu")
            taxon_code, taxon_fr, taxon_lat = taxon_raw.capitalize(), "", ""
        else:
            taxon_fr, taxon_lat = TAXONS[key]
            taxon_code = taxon_raw.capitalize()

    tissue = m.group("tissue")
    if tissue not in {"01", "02", "03", "05"}:
        flags.append("tissu_inattendu")

    return {
        "year": "20" + m.group("year"),
        "site": site,
        "individual": m.group("indiv"),
        "taxon_code": taxon_code,
        "taxon": taxon_fr,
        "species": taxon_lat,
        "tissue_code": tissue,
        "tissue": TISSUS.get(tissue, ""),
        "replicate": m.group("rep").upper(),
    }, flags


EMPTY_FIELDS = {
    "year": "", "site": "", "individual": "", "taxon_code": "", "taxon": "",
    "species": "", "tissue_code": "", "tissue": "", "replicate": "",
}

COLUMNS = [
    "sample_id", "sample_name", "sample_type",
    "year", "site", "individual",
    "taxon_code", "taxon", "species",
    "tissue_code", "tissue", "replicate",
    "plate", "well", "i7_id", "i7_index", "i5_id", "i5_index",
    "fastq_r1", "fastq_r2", "fastq_ok", "size_r1", "size_r2",
    "run", "flags",
]


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    rundir = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2])

    sheet = rundir / "SampleSheet.csv"
    basecalls = rundir / "Data" / "Intensities" / "BaseCalls"
    if not sheet.exists():
        sys.exit(f"SampleSheet introuvable : {sheet}")

    # Index des fastq réellement présents, par préfixe {name}_{S}
    fastqs = {}
    for f in basecalls.glob("*.fastq.gz"):
        fastqs[f.name] = f

    rows, n_unparsed = [], 0
    for i, rec in enumerate(read_samplesheet(sheet), start=1):
        raw = (rec.get("Sample_Name") or "").strip()
        stype = classify(raw)

        if stype == "biological":
            fields, flags = parse_name(raw)
            if fields is None:
                fields, n_unparsed = dict(EMPTY_FIELDS), n_unparsed + 1
        else:
            fields, flags = dict(EMPTY_FIELDS), []

        # Illumina remplace espaces et underscores par des tirets dans les noms
        # de fichiers, et suffixe par _S{n} (n = ordre dans la SampleSheet).
        fs_name = re.sub(r"[\s_]+", "-", raw)
        r1 = f"{fs_name}_S{i}_L001_R1_001.fastq.gz"
        r2 = f"{fs_name}_S{i}_L001_R2_001.fastq.gz"
        p1, p2 = fastqs.get(r1), fastqs.get(r2)
        if not (p1 and p2):
            flags = flags + ["fastq_manquant"]

        rows.append({
            "sample_id": rec.get("Sample_ID", ""),
            "sample_name": raw,
            "sample_type": stype,
            **fields,
            "plate": rec.get("Sample_Plate", ""),
            "well": rec.get("Sample_Well", ""),
            "i7_id": rec.get("I7_Index_ID", ""),
            "i7_index": rec.get("index", ""),
            "i5_id": rec.get("I5_Index_ID", ""),
            "i5_index": rec.get("index2", ""),
            "fastq_r1": r1 if p1 else "",
            "fastq_r2": r2 if p2 else "",
            "fastq_ok": "yes" if (p1 and p2) else "no",
            "size_r1": p1.stat().st_size if p1 else "",
            "size_r2": p2.stat().st_size if p2 else "",
            "run": rundir.name,
            "flags": ";".join(flags),
        })

    # Propagation du taxon : si un échantillon n'a pas de code taxon mais
    # qu'un autre échantillon du même individu (année+site+n°) en porte un,
    # on le reprend. Sans ambiguïté possible — un individu a un seul taxon.
    known = {}
    for r in rows:
        if r["sample_type"] == "biological" and r["taxon_code"]:
            known.setdefault((r["year"], r["site"], r["individual"]),
                             set()).add(r["taxon_code"])
    for r in rows:
        if r["sample_type"] != "biological" or r["taxon_code"]:
            continue
        cand = known.get((r["year"], r["site"], r["individual"]), set())
        if len(cand) == 1:
            code = next(iter(cand))
            fr, lat = TAXONS[code.lower()]
            r.update(taxon_code=code, taxon=fr, species=lat)
            r["flags"] = ";".join(
                [f for f in r["flags"].split(";") if f and f != "taxon_absent"]
                + ["taxon_infere"])

    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)

    n_flag = sum(1 for r in rows if r["flags"])
    n_miss = sum(1 for r in rows if r["fastq_ok"] == "no")
    print(f"{len(rows)} échantillons → {out}")
    print(f"  non parsés     : {n_unparsed}")
    print(f"  avec flags     : {n_flag}")
    print(f"  fastq manquant : {n_miss}")


if __name__ == "__main__":
    main()
