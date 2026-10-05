#!/usr/bin/env python3
"""43-retention_profondeur.py — rétention des échantillons selon la profondeur de raréfaction, par catégorie.
Recalcule les écarts de rétention P. toxostoma − hybrides cités au §8.6 de l'article (et tracés en Figure S1,
ex-S2, panneau b), qu'aucun script du dépôt ne produisait : la figure portait des valeurs recopiées d'une trace
antérieure à la reclassification de septembre.
Unité : l'échantillon (individu × tissu × run), runs confondus (run = "tous") et par run, sur les 2 180 colonnes de
results/decontam/asv_table_clean.tsv (profondeur = somme de colonne). Retenu à la profondeur d si profondeur >= d.
Passe 1 : quasi-purs exclus (inclus_passe1) ; passe 2 : tous. Écart = 100 × (rétention Pt − rétention Hy), en points.
Sorties : results/depth_agreement/retention_par_categorie.tsv (long), retention_par_station.tsv (stations à
gradient complet), retention_effectifs.tsv. Les valeurs du §8.6 (50 % / 86 %, 36 et 20 points, 3,8 et 5,7 points,
14,0 et 8,9 points) sont celles du run durance1 (contrôlées par le script 40) ; les effectifs (2 067, 1 825), tous runs. Lancer depuis la racine du dépôt (python3 système)."""
import csv, collections
DEP = [500, 750, 1000, 1500, 2000, 3000]
OUT = "results/depth_agreement/"
# profondeurs
with open("results/decontam/asv_table_clean.tsv") as fh:
    hdr = fh.readline().rstrip("\n").split("\t")[1:]
    tot = [0] * len(hdr)
    for line in fh:
        v = line.rstrip("\n").split("\t")[1:]
        for i, x in enumerate(v):
            if x and x != "0": tot[i] += int(float(x))
depth = dict(zip(hdr, tot))
assert len(depth) == 2180, len(depth)
md = {r["dada2_id"]: r for r in csv.DictReader(open("metadata/analysis_metadata.csv", encoding="utf-8"))}
miss = [s for s in depth if s not in md]; assert not miss, miss[:3]
S = [dict(md[s], depth=depth[s]) for s in depth]
def p1(r): return r["inclus_passe1"] in ("True", "TRUE")
rows, eff = [], []
for ps in ("1", "2"):
    sub = [r for r in S if ps == "2" or p1(r)]
    for d in DEP:
        eff.append(dict(passe=ps, profondeur=d, n_total=len(sub), n_retenus=sum(r["depth"] >= d for r in sub)))
    for run in ("tous", "durance1", "durance2", "durance3"):
      for tis in sorted({r["tissue"] for r in sub}):
        st = [r for r in sub if r["tissue"] == tis and run in ("tous", r["run_label"])]
        for d in DEP:
            ret = {}
            for c in ("Cn", "Hy", "Pt"):
                x = [r["depth"] >= d for r in st if r["categorie"] == c]
                ret[c] = (sum(x), len(x))
            g = 100 * (ret["Pt"][0] / ret["Pt"][1] - ret["Hy"][0] / ret["Hy"][1])
            rows.append(dict(passe=ps, run=run, tissu=tis, profondeur=d,
                             **{f"retenus_{c}": ret[c][0] for c in ret}, **{f"n_{c}": ret[c][1] for c in ret},
                             **{f"retention_{c}": round(100 * ret[c][0] / ret[c][1], 2) for c in ret},
                             ecart_Pt_moins_Hy=round(g, 2)))
def w(path, R):
    with open(path, "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(R[0]), delimiter="\t"); wr.writeheader(); wr.writerows(R)
w(OUT + "retention_par_categorie.tsv", rows); w(OUT + "retention_effectifs.tsv", eff)
# stations à gradient complet, par passe
srows = []
for ps in ("1", "2"):
    sub = [r for r in S if ps == "2" or p1(r)]
    cats = collections.defaultdict(set)
    for r in sub: cats[r["station"]].add(r["categorie"])
    full = sorted(s for s, c in cats.items() if c >= {"Cn", "Hy", "Pt"})
    for stn in full:
      for run in ("tous", "durance1", "durance2", "durance3"):
        for tis in sorted({r["tissue"] for r in sub}):
            for d in DEP:
                st = [r for r in sub if r["station"] == stn and r["tissue"] == tis and run in ("tous", r["run_label"])]
                ret = {c: [r["depth"] >= d for r in st if r["categorie"] == c] for c in ("Hy", "Pt")}
                if not ret["Hy"] or not ret["Pt"]: continue
                srows.append(dict(passe=ps, run=run, station=stn, tissu=tis, profondeur=d, n_Hy=len(ret["Hy"]), n_Pt=len(ret["Pt"]),
                                  ecart_Pt_moins_Hy=round(100 * (sum(ret["Pt"]) / len(ret["Pt"]) - sum(ret["Hy"]) / len(ret["Hy"])), 2)))
w(OUT + "retention_par_station.tsv", srows)
for r in rows:
    if r["profondeur"] in (500, 3000) and r["tissu"] in ("caudale", "midgut") and r["run"] in ("tous", "durance1"): print(r["run"], r["passe"], r["tissu"], r["profondeur"], r["retention_Hy"], r["retention_Pt"], r["ecart_Pt_moins_Hy"])
for e in eff:
    if e["profondeur"] in (500, 3000): print(e)
