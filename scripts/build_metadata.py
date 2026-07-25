#!/usr/bin/env python3
"""Construit le fichier de métadonnées d'un run.

Usage :
    python3 scripts/build_metadata.py <source> <sortie.csv> [--label durance1]

<source> est soit un dossier de run MiSeq contenant une SampleSheet.csv, soit
un dossier de fastq déjà démultiplexés (cas de durance2, livré sans run dir).
Dans ce second cas les noms d'échantillons sont reconstruits depuis les noms
de fichiers : Illumina y a remplacé espaces et underscores par des tirets, et
les colonnes de plaque et d'index restent vides — elles ne sont pas
récupérables depuis les fastq et ne sont pas reprises d'un autre run.

Parse les noms d'échantillons selon le schéma
    {année}{Site}{individu}{Taxon}{tissu}{réplicat}
en normalisant au préalable les anomalies de saisie (espaces, tirets, casse).
Chaque anomalie corrigée est tracée dans la colonne `flags` : rien n'est
silencieusement réparé.
"""

import argparse
import csv
import re
import sys
from pathlib import Path

TAXONS = {
    "ch": ("chevesne", "Squalius cephalus"),
    "cn": ("hotu", "Chondrostoma nasus"),
    "pt": ("toxostome", "Parachondrostoma toxostoma"),
}

# La SampleSheet de durance1 nomme deux échantillons `14Bue1006Cn05A`, en B07
# et C07. durance2 et durance3 appellent celui de C07 `14Bue1006Cn05Abis` : le
# suffixe a sauté à la saisie de durance1. Même puits dans les trois runs,
# l'identification est certaine. Corrigé ici, tracé par le flag `bis`.
NOMS_CORRIGES = {
    ("170710_M03930_0062_000000000-BBHKV", "223"): "14Bue1006Cn05Abis",
}

# Correspondance code tissu ↔ tissu, confirmée par la personne qui a acquis les
# données (2026-07-25) : elle recoupe le plan de plaque, où chaque bloc de 192
# librairies porte un blanc nommé (Blanc-Caudal/Branchie/Midgut/Hindgut).
TISSUS = {
    "01": "caudale",
    "02": "midgut",
    "03": "hindgut",
    "05": "branchie",
}

# Taxon absent de la SampleSheet (bloc de saisie manquant : Ain 2014, individus
# 1036 à 1043), complété d'après la feuille de terrain (collègue, 2026-07-25).
# Clé : (année, site, individu). Appliqué à tous les tissus de l'individu et à
# tous les runs, tracé par le flag `taxon_saisi_manuellement`.
TAXON_MANUEL = {
    ("2014", "Ain", "1036"): "Cn",
    ("2014", "Ain", "1037"): "Cn",
    ("2014", "Ain", "1038"): "Pt",
    ("2014", "Ain", "1039"): "Pt",
    ("2014", "Ain", "1040"): "Pt",
    ("2014", "Ain", "1041"): "Pt",
    ("2014", "Ain", "1042"): "Pt",
    ("2014", "Ain", "1043"): "Pt",
}

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
    """Retourne les lignes de la section [Data] comme dicts.

    Tolère la SampleSheet de durance2, où la virgule entre Sample_Name et
    Sample_Plate a sauté : les deux colonnes sont fusionnées en tête comme dans
    chaque ligne, la valeur étant `{nom}{plaque}` (plaque = dernier chiffre,
    1 à 8 ; le nom se termine toujours par une lettre ou un chiffre de tissu).
    On rescinde la colonne pour retrouver Sample_Name et Sample_Plate.
    """
    with open(path, newline="", encoding="utf-8", errors="replace") as fh:
        lines = fh.read().splitlines()
    try:
        start = next(i for i, l in enumerate(lines) if l.startswith("Sample_ID,"))
    except StopIteration:
        sys.exit(f"Section [Data] introuvable dans {path}")
    recs = list(csv.DictReader(lines[start:]))

    if recs and "Sample_Name" not in recs[0] and "Sample_NameSample_Plate" in recs[0]:
        for rec in recs:
            merged = (rec.pop("Sample_NameSample_Plate") or "").strip()
            rec["Sample_Name"], rec["Sample_Plate"] = merged[:-1], merged[-1:]
    return recs


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


def parse_name(raw, from_filename=False):
    """Normalise puis décompose un nom. Retourne (champs, flags).

    `from_filename` : le nom vient d'un fastq, où Illumina a déjà transformé
    les espaces en tirets. Le tiret n'est alors pas une anomalie de saisie et
    n'est pas signalé comme telle.
    """
    flags = []
    name = raw.strip()

    # Suffixe «bis» : séparé par un underscore dans les SampleSheet, par un
    # tiret dans les noms de fichiers (conversion Illumina), et collé au nom
    # pour 14Bue1006Cn05A — saisi sans suffixe dans durance1, avec dans les
    # deux autres runs. Même puits, même index : c'est bien la même librairie.
    m_bis = re.match(r"^(.*?)[-_ ]?bis$", name, re.IGNORECASE)
    if m_bis:
        name = m_bis.group(1)
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
    if "-" in name and not from_filename:
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
    "tissue_code", "tissue", "replicate", "extraction",
    "plate", "well", "i7_id", "i7_index", "i5_id", "i5_index",
    "fastq_r1", "fastq_r2", "fastq_ok", "size_r1", "size_r2",
    "run", "run_label", "flags",
]

# Un fastq démultiplexé Illumina : {nom}_S{n}_L001_R{1,2}_001.fastq[.gz]
RE_FASTQ = re.compile(
    r"^(?P<name>.+)_S(?P<snum>\d+)_L001_R(?P<read>[12])_001\.fastq(?:\.gz)?$"
)


def collect_from_samplesheet(rundir):
    """Run MiSeq complet : la SampleSheet fait foi, les fastq sont vérifiés."""
    sheet = rundir / "SampleSheet.csv"
    basecalls = rundir / "Data" / "Intensities" / "BaseCalls"
    fastqs = {f.name: f for f in basecalls.glob("*.fastq.gz")}

    recs = []
    for i, rec in enumerate(read_samplesheet(sheet), start=1):
        raw = (rec.get("Sample_Name") or "").strip()
        # Illumina remplace espaces et underscores par des tirets dans les noms
        # de fichiers, et suffixe par _S{n} (n = ordre dans la SampleSheet).
        fs_name = re.sub(r"[\s_]+", "-", raw)
        r1 = f"{fs_name}_S{i}_L001_R1_001.fastq.gz"
        r2 = f"{fs_name}_S{i}_L001_R2_001.fastq.gz"
        recs.append({
            "sample_id": rec.get("Sample_ID", ""),
            "sample_name": raw,
            "from_filename": False,
            "plate": rec.get("Sample_Plate", ""),
            "well": rec.get("Sample_Well", ""),
            "i7_id": rec.get("I7_Index_ID", ""),
            "i7_index": rec.get("index", ""),
            "i5_id": rec.get("I5_Index_ID", ""),
            "i5_index": rec.get("index2", ""),
            "r1_name": r1, "r2_name": r2,
            "r1": fastqs.get(r1), "r2": fastqs.get(r2),
        })
    return recs


def collect_from_fastqdir(root):
    """Fastq démultiplexés seuls : tout vient du nom de fichier.

    Parcours récursif — durance2 range ses témoins dans un sous-dossier
    `control/`. Le n° _S{n} sert de sample_id : c'est le rang de l'échantillon
    dans la SampleSheet du run d'origine, non livrée ici.
    """
    pairs = {}
    for f in sorted(root.rglob("*.fastq*")):
        m = RE_FASTQ.match(f.name)
        if not m:
            continue
        key = (m.group("name"), int(m.group("snum")))
        pairs.setdefault(key, {})[m.group("read")] = f

    recs = []
    for (name, snum), reads in sorted(pairs.items(), key=lambda kv: kv[0][1]):
        p1, p2 = reads.get("1"), reads.get("2")
        recs.append({
            "sample_id": str(snum),
            "sample_name": name,
            "from_filename": True,
            "plate": "", "well": "",
            "i7_id": "", "i7_index": "", "i5_id": "", "i5_index": "",
            "r1_name": p1.name if p1 else "",
            "r2_name": p2.name if p2 else "",
            "r1": p1, "r2": p2,
        })
    return recs


def _normkey(name):
    """Clé de rapprochement d'un nom, insensible aux séparateurs et à la casse.

    Les noms de fichiers portent des tirets là où la SampleSheet a des espaces
    ou des underscores (conversion Illumina) : on efface les trois pour
    rapprocher un fastq de sa ligne de SampleSheet.
    """
    return re.sub(r"[\s_-]+", "", name.strip()).lower()


def find_samplesheet(root):
    """Cherche dans `root` un CSV contenant une section [Data] de SampleSheet.

    durance2 est livré sans SampleSheet.csv canonique mais avec la feuille
    d'origine sous un autre nom, déposée dans le dossier des fastq.
    """
    for f in sorted(root.rglob("*.csv")):
        try:
            head = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if any(l.startswith("Sample_ID,") for l in head.splitlines()):
            return f
    return None


def index_samplesheet(path):
    """Indexe plaque/puits/index d'une SampleSheet par nom normalisé.

    Sert à enrichir des fastq démultiplexés livrés sans leur SampleSheet
    canonique. Le rapprochement se fait sur le nom (le Sample_ID de la feuille
    est un renumérotage propre au run, sans lien avec le _S{n} des fichiers).
    """
    idx, collisions = {}, set()
    for rec in read_samplesheet(path):
        k = _normkey(rec.get("Sample_Name") or "")
        if not k:
            continue
        if k in idx:
            collisions.add(k)
        idx[k] = {
            "plate": rec.get("Sample_Plate", ""),
            "well": rec.get("Sample_Well", ""),
            "i7_id": rec.get("I7_Index_ID", ""),
            "i7_index": rec.get("index", ""),
            "i5_id": rec.get("I5_Index_ID", ""),
            "i5_index": rec.get("index2", ""),
        }
    for k in collisions:  # ambigu : on n'enrichit pas à l'aveugle
        idx.pop(k, None)
    return idx, collisions


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="dossier de run MiSeq, ou dossier de fastq")
    ap.add_argument("output")
    ap.add_argument("--label", default="",
                    help="nom court du lot (durance1, durance2, ...) ; "
                         "sert d'étiquette de run à la fusion")
    ap.add_argument("--samplesheet", default="",
                    help="SampleSheet à part, pour enrichir des fastq livrés "
                         "sans elle (plaque, puits, index). Autodétectée dans "
                         "le dossier source si absente.")
    args = ap.parse_args()

    src = Path(args.source).resolve()
    out = Path(args.output)
    if not src.is_dir():
        sys.exit(f"Source introuvable : {src}")

    ss_idx = {}
    if (src / "SampleSheet.csv").exists():
        recs = collect_from_samplesheet(src)
        mode = "SampleSheet"
    else:
        recs = collect_from_fastqdir(src)
        mode = "noms de fichiers"
        if not recs:
            sys.exit(f"Ni SampleSheet.csv ni fastq démultiplexés dans {src}")
        # Enrichissement plaque/puits/index depuis une SampleSheet à part.
        ss_path = Path(args.samplesheet) if args.samplesheet else find_samplesheet(src)
        if ss_path and ss_path.exists():
            ss_idx, collisions = index_samplesheet(ss_path)
            note = f" ({len(collisions)} noms ambigus écartés)" if collisions else ""
            print(f"{src.name} : enrichi par {ss_path.name}{note}")
    print(f"{src.name} : source = {mode}")

    rows, n_unparsed = [], 0
    for rec in recs:
        raw = rec["sample_name"]
        pre_flags = []
        fixed = NOMS_CORRIGES.get((src.name, rec["sample_id"]))
        if fixed and fixed != raw:
            raw, pre_flags = fixed, ["nom_corrige"]
        stype = classify(raw)

        if stype == "biological":
            fields, flags = parse_name(raw, from_filename=rec["from_filename"])
            if fields is None:
                fields, n_unparsed = dict(EMPTY_FIELDS), n_unparsed + 1
        else:
            fields, flags = dict(EMPTY_FIELDS), []
        flags = pre_flags + flags

        if rec["from_filename"]:
            flags = flags + ["nom_depuis_fichier"]

        # Enrichissement par la SampleSheet à part (mode fastqdir) : plaque,
        # puits et index, rapprochés par le nom. Le _S{n} du fichier reste le
        # sample_id — il est cohérent d'un run à l'autre, pas le Sample_ID de
        # cette feuille (renumérotage propre au run).
        meta = ss_idx.get(_normkey(raw)) if ss_idx else None
        if ss_idx and meta is None and stype == "biological":
            flags = flags + ["absent_samplesheet"]
        meta = meta or rec

        p1, p2 = rec["r1"], rec["r2"]
        if not (p1 and p2):
            flags = flags + ["fastq_manquant"]

        rows.append({
            "sample_id": rec["sample_id"],
            "sample_name": raw,
            "sample_type": stype,
            **fields,
            # `bis` = seconde extraction d'ADN du même tissu (et non un second
            # prélèvement) : même unité biologique, extraction distincte.
            "extraction": "bis" if "bis" in flags else (
                "initiale" if stype == "biological" else ""),
            "plate": meta["plate"],
            "well": meta["well"],
            "i7_id": meta["i7_id"],
            "i7_index": meta["i7_index"],
            "i5_id": meta["i5_id"],
            "i5_index": meta["i5_index"],
            # Chemin relatif à la source : durance2 range ses témoins dans un
            # sous-dossier, le seul nom de fichier ne suffit pas à les situer.
            "fastq_r1": str(p1.relative_to(src)) if p1 else "",
            "fastq_r2": str(p2.relative_to(src)) if p2 else "",
            "fastq_ok": "yes" if (p1 and p2) else "no",
            "size_r1": p1.stat().st_size if p1 else "",
            "size_r2": p2.stat().st_size if p2 else "",
            "run": src.name,
            "run_label": args.label or src.name,
            "flags": ";".join(flags),
        })

    # Taxon saisi manuellement (feuille de terrain) : les individus dont le
    # code espèce manquait dans les noms. Appliqué avant la propagation, pour
    # que les autres tissus du même individu en héritent le cas échéant.
    for r in rows:
        if r["sample_type"] != "biological":
            continue
        code = TAXON_MANUEL.get((r["year"], r["site"], r["individual"]))
        if code and not r["taxon_code"]:
            fr, lat = TAXONS[code.lower()]
            r.update(taxon_code=code, taxon=fr, species=lat)
            r["flags"] = ";".join(
                [f for f in r["flags"].split(";") if f and f != "taxon_absent"]
                + ["taxon_saisi_manuellement"])

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
