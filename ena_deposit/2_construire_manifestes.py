#!/usr/bin/env python3
"""ETAPE 2/3 : construire les 2304 manifestes webin-cli.

Chaque manifeste decrit un run (une librairie sequencee sur un des trois runs) et
reference l'accession ERS obtenue a l'etape 1, plus l'accession de l'etude.

  python3 2_construire_manifestes.py

Produit : manifests/<run_alias>.txt  (2304 fichiers)
"""
import csv, os, sys

D = "/home/martinj/work/projects/microbiome-hybrid/ena_deposit"
ACC = os.path.join(D, "sample_accessions.tsv")
RUNS = os.path.join(D, "ena_experiments_runs.tsv")
OUT = os.path.join(D, "manifests")

if not os.path.exists(ACC):
    sys.exit(f"ERREUR : {ACC} introuvable. Lancer d'abord 1_soumettre_metadonnees.sh")

acc = {}
with open(ACC, newline="") as f:
    for row in csv.DictReader(f, delimiter="\t"):
        acc[row["alias"]] = row["accession"]

study = next((v for k, v in acc.items() if v.startswith(("PRJEB", "ERP"))), None)
if not study:
    sys.exit("ERREUR : aucune accession d'etude (PRJEB/ERP) dans sample_accessions.tsv")
print(f"etude : {study}")
print(f"echantillons connus : {sum(1 for v in acc.values() if v.startswith('ERS'))}")

os.makedirs(OUT, exist_ok=True)
for old in os.listdir(OUT):
    os.remove(os.path.join(OUT, old))

n, manquants = 0, set()
with open(RUNS, newline="") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        ers = acc.get(r["sample_alias"])
        if not ers or not ers.startswith("ERS"):
            manquants.add(r["sample_alias"]); continue
        lines = [
            ("STUDY", study),
            ("SAMPLE", ers),
            ("NAME", r["run_alias"]),
            ("INSTRUMENT", r["instrument_model"]),
            ("LIBRARY_NAME", r["library_name"]),
            ("LIBRARY_SOURCE", r["library_source"]),
            ("LIBRARY_SELECTION", r["library_selection"]),
            ("LIBRARY_STRATEGY", r["library_strategy"]),
            ("INSERT_SIZE", r["nominal_length"]),
            ("FASTQ", r["upload_r1"]),
            ("FASTQ", r["upload_r2"]),
        ]
        with open(os.path.join(OUT, r["run_alias"] + ".txt"), "w") as g:
            for k, v in lines:
                g.write(f"{k}\t{v}\n")
        n += 1

print(f"manifestes ecrits : {n}")
if manquants:
    print(f"ATTENTION : {len(manquants)} echantillon(s) sans accession ERS, runs ignores")
    for a in sorted(manquants)[:10]:
        print("   ", a)
print()
print("Etape suivante : bash 3_transferer_et_soumettre.sh test")
