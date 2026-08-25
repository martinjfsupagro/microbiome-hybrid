#!/usr/bin/env python3
"""Genere les XML de soumission ENA pour le projet Durance 16S.

Usage:  python3 build_ena_xml.py [--sites ENA_sites_completes.csv] [--outdir ena_submission]

Sans --sites, les champs geographiques MIxS obligatoires (lat/lon, contextes ENVO)
sont ecrits avec la valeur controlee "not provided" et le checklist bascule sur
ERC000011 (checklist par defaut ENA). Avec --sites, le checklist ERC000013
(GSC MIxS host associated) est utilise et les coordonnees sont injectees par site.
"""
import argparse, csv, os, sys
from xml.sax.saxutils import escape

PREFIX = "DURANCE16S"
STUDY_ALIAS = f"{PREFIX}_STUDY"
STUDY_TITLE = ("Bacterial microbiota of four tissues in a Chondrostoma nasus x "
               "Parachondrostoma toxostoma hybrid zone (Rhone drainage, France): "
               "16S V4 amplicon sequencing with three technical sequencing replicates")
STUDY_ABSTRACT = (
 "Host-associated bacterial microbiota of two interbreeding cyprinid fishes, the nase "
 "Chondrostoma nasus and the toxostome Parachondrostoma toxostoma, together with "
 "unassigned Chondrostoma sp. individuals from their contact zone, sampled across nine "
 "sites of the Rhone drainage (Durance and Ardeche rivers, France) in 2014 and 2015. "
 "Four tissues were sampled per fish (caudal fin, midgut, hindgut and gill). The V4 region "
 "of the bacterial 16S rRNA gene was amplified with the 515F/806R primer pair following the "
 "dual-index strategy of Kozich et al. (2013) and sequenced on an Illumina MiSeq (v3, 2x300). "
 "The same 768 libraries were sequenced three independent times (runs durance1, durance2 and "
 "durance3; distinct flow cells), so that every library is present as three technical "
 "replicates and the sequencing-run effect can be estimated unconfounded with any biological "
 "factor. The submission includes extraction blanks, no-template PCR controls, ZymoBIOMICS "
 "mock community positive controls and empty wells used to monitor index hopping.")

def el(tag, text=None, attrs=None, indent=0):
    a = "".join(f' {k}="{escape(str(v), {chr(34): "&quot;"})}"' for k, v in (attrs or {}).items())
    pad = "  " * indent
    if text is None:
        return f"{pad}<{tag}{a}/>\n"
    return f"{pad}<{tag}{a}>{escape(str(text))}</{tag}>\n"

def attribute(tag, value, units=None, indent=3):
    pad = "  " * indent
    s = f"{pad}<SAMPLE_ATTRIBUTE>\n"
    s += el("TAG", tag, indent=indent + 1)
    s += el("VALUE", value, indent=indent + 1)
    if units:
        s += el("UNITS", units, indent=indent + 1)
    s += f"{pad}</SAMPLE_ATTRIBUTE>\n"
    return s

def read_tsv(p):
    with open(p, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))

def build_project(out):
    x = '<?xml version="1.0" encoding="UTF-8"?>\n<PROJECT_SET>\n'
    x += f'  <PROJECT alias="{STUDY_ALIAS}">\n'
    x += el("TITLE", STUDY_TITLE, indent=2)
    x += el("DESCRIPTION", STUDY_ABSTRACT, indent=2)
    x += "    <SUBMISSION_PROJECT>\n      <SEQUENCING_PROJECT/>\n    </SUBMISSION_PROJECT>\n"
    x += "  </PROJECT>\n</PROJECT_SET>\n"
    open(out, "w", encoding="utf-8").write(x)

def build_samples(samples, sites, checklist, out):
    x = '<?xml version="1.0" encoding="UTF-8"?>\n<SAMPLE_SET>\n'
    for s in samples:
        ctrl = s["is_control"] == "True"
        x += f'  <SAMPLE alias="{escape(s["alias"])}">\n'
        x += el("TITLE", s["title"], indent=2)
        x += "    <SAMPLE_NAME>\n"
        x += el("TAXON_ID", s["taxon_id"], indent=3)
        x += el("SCIENTIFIC_NAME", s["taxon_name"], indent=3)
        x += "    </SAMPLE_NAME>\n"
        x += "    <SAMPLE_ATTRIBUTES>\n"
        x += attribute("ENA-CHECKLIST", checklist)
        x += attribute("project name", "Durance hybrid zone fish microbiota")
        x += attribute("sample type", {"biological": "biological sample",
                                       "blank": "DNA extraction blank",
                                       "temoin": "no-template PCR control",
                                       "mock": "mock community positive control",
                                       "empty": "empty well (index-hopping monitor)"}[s["sample_type_ena"]])
        x += attribute("collection date", s["collection_date"])
        x += attribute("geographic location (country and/or sea)", s["geographic_location_country_andor_sea"])

        site = s.get("site_code", "")
        info = sites.get(site) if (sites and site) else None
        if ctrl:
            lat = lon = "missing: control sample"
            broad = local = medium = "missing: control sample"
        elif info:
            lat, lon = info["latitude"], info["longitude"]
            broad, local, medium = info["broad"], info["local"], info["medium"]
        else:
            lat = lon = "not provided"
            broad = local = medium = "not provided"

        if checklist == "ERC000013":
            x += attribute("geographic location (latitude)", lat, units="DD")
            x += attribute("geographic location (longitude)", lon, units="DD")
            x += attribute("broad-scale environmental context", broad)
            x += attribute("local environmental context", local)
            x += attribute("environmental medium", medium)
        elif not ctrl and info:
            x += attribute("lat_lon", f"{lat} {lon}")

        if s["host_scientific_name"]:
            x += attribute("host scientific name", s["host_scientific_name"])
            x += attribute("host common name", s["host_common_name"])
            x += attribute("host tissue sampled", s["host_tissue_sampled"])
            x += attribute("host subject id", s["host_individual_id"])
        if not ctrl and info and info.get("locality"):
            x += attribute("geographic location (region and locality)", info["locality"])
        if not ctrl and site:
            x += attribute("collection site code", site)
        x += attribute("target gene", "16S rRNA")
        x += attribute("target subfragment", "V4")
        x += attribute("pcr primers", "FWD:GTGCCAGCMGCCGCGGTAA; REV:GGACTACHVGGGTWTCTAAT")
        x += attribute("sequencing method", "Illumina MiSeq")
        x += attribute("plate", s["plate"])
        x += attribute("well", s["well"])
        x += attribute("original sample name", s["sample_name_projet"])
        x += "    </SAMPLE_ATTRIBUTES>\n  </SAMPLE>\n"
    x += "</SAMPLE_SET>\n"
    open(out, "w", encoding="utf-8").write(x)

def build_experiments(runs, out):
    x = '<?xml version="1.0" encoding="UTF-8"?>\n<EXPERIMENT_SET>\n'
    for r in runs:
        x += f'  <EXPERIMENT alias="{escape(r["exp_alias"])}">\n'
        x += el("TITLE", f'16S V4 amplicon, {r["library_name"]}', indent=2)
        x += f'    <STUDY_REF refname="{STUDY_ALIAS}"/>\n'
        x += "    <DESIGN>\n"
        x += el("DESIGN_DESCRIPTION",
                f'Dual-index 16S rRNA V4 amplicon library (Kozich et al. 2013), sequencing run '
                f'{r["sequencing_run"]}, flow cell {r["flowcell"]}, i7 {r["i7_id"]} / i5 {r["i5_id"]}', indent=3)
        x += f'      <SAMPLE_DESCRIPTOR refname="{escape(r["sample_alias"])}"/>\n'
        x += "      <LIBRARY_DESCRIPTOR>\n"
        x += el("LIBRARY_NAME", r["library_name"], indent=4)
        x += el("LIBRARY_STRATEGY", r["library_strategy"], indent=4)
        x += el("LIBRARY_SOURCE", r["library_source"], indent=4)
        x += el("LIBRARY_SELECTION", r["library_selection"], indent=4)
        x += "        <LIBRARY_LAYOUT>\n"
        x += f'          <PAIRED NOMINAL_LENGTH="{r["nominal_length"]}"/>\n'
        x += "        </LIBRARY_LAYOUT>\n"
        x += el("LIBRARY_CONSTRUCTION_PROTOCOL",
                "DNA extracted with the Qiagen Food Mericon kit. The V4 region of the bacterial 16S "
                "rRNA gene was amplified with primers 515F (GTGCCAGCMGCCGCGGTAA) and 806R "
                "(GGACTACHVGGGTWTCTAAT) carrying 8 bp dual indices and Illumina adapters, following "
                "Kozich et al. (2013); amplification, purification and pooling followed Galan et al. "
                "(2016). Libraries were quantified with the Kapa quantification kit and sequenced on "
                "an Illumina MiSeq with reagent kit v3 (2x300 cycles) and a 10% PhiX spike-in.", indent=4)
        x += "      </LIBRARY_DESCRIPTOR>\n    </DESIGN>\n"
        x += "    <PLATFORM>\n      <ILLUMINA>\n"
        x += el("INSTRUMENT_MODEL", r["instrument_model"], indent=4)
        x += "      </ILLUMINA>\n    </PLATFORM>\n"
        x += "  </EXPERIMENT>\n"
    x += "</EXPERIMENT_SET>\n"
    open(out, "w", encoding="utf-8").write(x)

def build_runs(runs, out):
    x = '<?xml version="1.0" encoding="UTF-8"?>\n<RUN_SET>\n'
    for r in runs:
        x += f'  <RUN alias="{escape(r["run_alias"])}">\n'
        x += f'    <EXPERIMENT_REF refname="{escape(r["exp_alias"])}"/>\n'
        x += "    <DATA_BLOCK>\n      <FILES>\n"
        for side in ("r1", "r2"):
            x += (f'        <FILE filename="{escape(r["upload_" + side])}" filetype="fastq" '
                  f'checksum_method="MD5" checksum="{r["md5_" + side]}"/>\n')
        x += "      </FILES>\n    </DATA_BLOCK>\n  </RUN>\n"
    x += "</RUN_SET>\n"
    open(out, "w", encoding="utf-8").write(x)

def build_submission(out, hold_date=None):
    x = '<?xml version="1.0" encoding="UTF-8"?>\n<SUBMISSION>\n  <ACTIONS>\n'
    x += "    <ACTION>\n      <ADD/>\n    </ACTION>\n"
    if hold_date:
        x += f'    <ACTION>\n      <HOLD HoldUntilDate="{hold_date}"/>\n    </ACTION>\n'
    x += "  </ACTIONS>\n</SUBMISSION>\n"
    open(out, "w", encoding="utf-8").write(x)

def load_sites(p):
    sites = {}
    with open(p, newline="", encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            lat = (row.get("latitude_WGS84_A_REMPLIR") or "").strip()
            lon = (row.get("longitude_WGS84_A_REMPLIR") or "").strip()
            if not lat or not lon:
                continue
            sites[row["site_code"].strip()] = dict(
                latitude=lat, longitude=lon,
                locality=(row.get("commune_ou_lieu_dit_A_REMPLIR") or "").strip(),
                broad=(row.get("broad_env_context_propose") or "freshwater river biome [ENVO:01000253]").strip(),
                local=(row.get("local_env_context_propose") or "river [ENVO:00000022]").strip(),
                medium=(row.get("environmental_medium_propose") or "river water [ENVO:01000599]").strip())
    return sites

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--samples", default="ena_samples.tsv")
    ap.add_argument("--runs", default="ena_experiments_runs.tsv")
    ap.add_argument("--sites", default=None)
    ap.add_argument("--outdir", default="ena_submission")
    ap.add_argument("--hold-date", default=None, help="AAAA-MM-JJ ; embargo jusqu'a cette date")
    a = ap.parse_args()

    samples, runs = read_tsv(a.samples), read_tsv(a.runs)
    sites = load_sites(a.sites) if a.sites else {}
    bio_sites = {s["site_code"] for s in samples if s["is_control"] != "True" and s["site_code"]}
    missing = sorted(bio_sites - set(sites)) if sites else sorted(bio_sites)
    checklist = "ERC000013" if (sites and not missing) else "ERC000011"

    os.makedirs(a.outdir, exist_ok=True)
    for r in runs:
        r["upload_r1"] = f'{r["sequencing_run"]}/{r["file_r1"]}'
        r["upload_r2"] = f'{r["sequencing_run"]}/{r["file_r2"]}'

    build_project(f"{a.outdir}/project.xml")
    build_samples(samples, sites, checklist, f"{a.outdir}/sample.xml")
    build_experiments(runs, f"{a.outdir}/experiment.xml")
    build_runs(runs, f"{a.outdir}/run.xml")
    build_submission(f"{a.outdir}/submission.xml", a.hold_date)

    print(f"checklist  : {checklist}")
    print(f"samples    : {len(samples)}")
    print(f"experiments: {len(runs)}")
    print(f"runs       : {len(runs)}  ({2 * len(runs)} fichiers)")
    if missing:
        print(f"\nATTENTION - coordonnees absentes pour {len(missing)} site(s): {', '.join(missing)}")
        print("  -> checklist ERC000011 utilise. Completez le CSV des sites et relancez")
        print("     avec --sites pour produire une soumission ERC000013 (MIxS).")

if __name__ == "__main__":
    main()
