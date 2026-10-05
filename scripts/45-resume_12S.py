#!/usr/bin/env python3
"""45-resume_12S.py — part des lectures écartées comme 12S de l'hôte ou dimères d'amorces (lectures < 240 pb après
coupe, scripts/02-remove_12S_worker.sh), par run et par échantillon biologique, depuis logs/rm12S_durance*_*.out.
Remplace les chiffres « 15–67 % » (article, §5) et « 14 à 67 % » (R2), qu'aucun calcul ne reproduisait.
Sortie : results/verif_article/part_12S.tsv. Lancer depuis la racine du dépôt (python3 système)."""
import re, glob, csv, statistics as st
typ = {(r["run_label"], r["sample_name"]): r["sample_type"] for r in csv.DictReader(open("metadata/samples_all.csv", encoding="utf-8"))}
rows, allp = [], []
for f in sorted(glob.glob("logs/rm12S_durance*_*.out")):
    run = re.search(r"(durance\d)", f).group(1); p, s12, lus = [], 0, 0
    for line in open(f, encoding="utf-8"):
        m = re.match(r"\s+(\S+)\s+:\s+(\d+) lus\s+(\d+) V4\s+(\d+) 12S/dim\S+ \((\d+)%\)", line)
        if not m or typ.get((run, m.group(1))) != "biological": continue
        a, c = int(m.group(2)), int(m.group(4))
        if a: p.append(100 * c / a)
        s12 += c; lus += a
    allp += p
    rows.append(dict(run=run, n_biologiques=len(p), pct_global=round(100 * s12 / lus, 2), mediane=round(st.median(p), 2),
                     minimum=round(min(p), 2), maximum=round(max(p), 2)))
assert len(rows) == 3 and all(r["n_biologiques"] > 700 for r in rows), rows
rows.append(dict(run="tous", n_biologiques=len(allp), pct_global=None, mediane=round(st.median(allp), 2),
                 minimum=round(min(allp), 2), maximum=round(max(allp), 2)))
with open("results/verif_article/part_12S.tsv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]), delimiter="\t"); w.writeheader(); w.writerows(rows)
for r in rows: print(r)
