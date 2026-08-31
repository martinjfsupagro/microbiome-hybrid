#!/bin/bash -l
#SBATCH --job-name=permdisp
#SBATCH --account=ondemand@biomics
#SBATCH --qos=cpu-ondemand-long
#SBATCH --partition=cpu-ondemand
#SBATCH --time=04:00:00
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
set -eEuo pipefail

# 24-permdisp.sh — DISPERSION de la composition par categorie genotypique
#
# POURQUOI CE N'EST PAS UN SIMPLE CONTROLE. L'hypothese "transgressive" porte en partie
# sur la VARIABILITE du microbiote hybride, pas seulement sur la position de son
# centroide. La PERMANOVA ne teste que la position ; c'est betadisper qui teste la
# dispersion. Sans lui, une moitie de la question reste non posee. Accessoirement, la
# PERMANOVA est elle-meme sensible a une heterogeneite de dispersion, donc son
# interpretation en depend.
#
# PREDICTION DIRECTIONNELLE. "Transgressif" au sens dispersion = les hybrides PLUS
# disperses que LES DEUX parentaux. Un test global significatif ne suffit donc pas : on
# rapporte la distance mediane au centre par categorie et les comparaisons par paires,
# pour que la direction soit lisible et puisse contredire la prediction.
#
# DEUX DISPOSITIFS, parce que la categorie est confondue avec la station.
#   (a) GLOBAL : betadisper sur tous les echantillons d'une strate, permutations
#       contraintes dans les blocs de station. Le null est "les etiquettes de categorie
#       sont echangeables A L'INTERIEUR d'une station" — plus de puissance, mais le
#       centre de groupe reste calcule globalement, donc la statistique melange encore
#       un peu la station.
#   (b) INTRA-STATION : betadisper separement dans chacune des trois stations a gradient
#       complet. Une difference de dispersion n'y peut pas etre spatiale. Moins de
#       puissance, mais propre par construction.
#
# CE QUI N'EST PAS CONTROLE. L'effet de position dans la plaque (script 17/18) agit sur
# la composition ; il pourrait gonfler la dispersion d'une categorie dont les echantillons
# sont plus etales en colonne. betadisper n'accepte pas de covariable, donc ce point n'est
# PAS separe ici. A declarer comme reserve, pas a passer sous silence.
#
# Sortie : results/permdisp/permdisp.tsv (ecriture incrementale) + .txt

cd "$HOME/work/projects/microbiome-hybrid"
OUT=results/permdisp
mkdir -p "$OUT" logs
GIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo NA)
printf '%s\tSTART\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log

$HOME/bin/envs/dada2/bin/Rscript - <<'RS' 2>&1 | tee results/permdisp/permdisp.txt
suppressMessages({library(vegan); library(permute)})
t0 <- Sys.time()
lg <- function(...) { cat(sprintf("[%6.1fs] ", as.numeric(difftime(Sys.time(), t0, units="secs"))),
                          ..., "\n", sep=""); flush.console() }
OUT <- "results/permdisp"; NPERM <- 999

# ---------------------------------------------------------------- VALIDATION
lg("=== validation des interfaces ===")
fb <- names(formals(betadisper)); fp <- names(formals(vegan:::permutest.betadisper))
lg("  betadisper : ", paste(fb, collapse=", "))
lg("  permutest  : ", paste(fp, collapse=", "))
stopifnot(all(c("d","group","type") %in% fb))
stopifnot(all(c("pairwise","permutations") %in% fp))
lg("  vegan ", as.character(packageVersion("vegan")))
# type par defaut : on l'explicite pour ne pas dependre de la version
TYPE <- "median"   # mediane spatiale, plus robuste que le centroide

MD <- read.csv("metadata/analysis_metadata.csv", stringsAsFactors = FALSE)
rownames(MD) <- MD$dada2_id
files <- Sys.glob("results/rarefaction/beta_mean_*.rds")
stopifnot(length(files) > 0)
lg("  matrices : ", paste(basename(files), collapse=", "))

TISSUS <- c("caudale","branchie","midgut","hindgut")
CATS   <- c("Cn","Hy","Pt")

TSV <- file.path(OUT, "permdisp.tsv")
cat("metrique\tdispositif\tstation\ttissu\trun\tn\tn_Cn\tn_Hy\tn_Pt\tF\tp\t",
    "dist_Cn\tdist_Hy\tdist_Pt\tp_Hy_vs_Cn\tp_Hy_vs_Pt\tneg_eig_pct\n", sep="", file = TSV)

emit <- function(...) cat(paste(c(...), collapse="\t"), "\n", sep="", file = TSV, append = TRUE)

one <- function(D, md, metrique, dispositif, station, tissu, run) {
  g <- factor(md$categorie, levels = CATS)
  g <- droplevels(g)
  if (nlevels(g) < 2) return(invisible(NULL))
  if (min(table(g)) < 3) return(invisible(NULL))
  bd <- betadisper(D, g, type = TYPE)
  # part de valeurs propres negatives : la matrice moyennee n'est pas garantie metrique
  ev <- bd$eig; negpct <- 100 * sum(abs(ev[ev < 0])) / sum(abs(ev))
  h  <- how(nperm = NPERM)
  if (dispositif == "global_station_bloquee") h <- how(nperm = NPERM, blocks = factor(md$station))
  pt <- permutest(bd, pairwise = TRUE, permutations = h)
  Fv <- pt$tab[1, "F"]; pv <- pt$tab[1, "Pr(>F)"]
  dm <- tapply(bd$distances, g, median)
  gp <- function(a, b) {
    if (!(a %in% levels(g)) || !(b %in% levels(g))) return(NA_real_)
    m <- pt$pairwise$permuted
    nm1 <- paste(a, b, sep = "-"); nm2 <- paste(b, a, sep = "-")
    if (nm1 %in% names(m)) return(unname(m[nm1]))
    if (nm2 %in% names(m)) return(unname(m[nm2]))
    NA_real_
  }
  f4 <- function(x) if (is.null(x) || is.na(x)) "NA" else sprintf("%.4f", x)
  emit(metrique, dispositif, station, tissu, run, nrow(md),
       sum(g == "Cn"), sum(g == "Hy"), sum(g == "Pt"),
       f4(Fv), f4(pv), f4(dm["Cn"]), f4(dm["Hy"]), f4(dm["Pt"]),
       f4(gp("Hy","Cn")), f4(gp("Hy","Pt")), sprintf("%.2f", negpct))
  invisible(NULL)
}

for (f in files) {
  metrique <- sub("^beta_mean_(.*)_N400\\.rds$", "\\1", basename(f))
  lg("################ ", metrique)
  M <- as.matrix(readRDS(f)); lab <- rownames(M)
  keep0 <- lab[lab %in% MD$dada2_id]
  # stations a gradient complet, calculees sur les donnees et non ecrites en dur
  mdall <- MD[keep0, ]
  full <- names(which(sapply(split(mdall$categorie, mdall$station),
                             function(z) length(unique(z)) == 3)))
  lg("  stations a gradient complet : ", paste(full, collapse=", "))
  for (run in c("durance1","durance2","durance3")) {
    for (ti in TISSUS) {
      sel <- keep0[MD[keep0, "run_label"] == run & MD[keep0, "tissue"] == ti]
      if (length(sel) < 15) next
      md <- MD[sel, ]
      D  <- as.dist(M[sel, sel])
      one(D, md, metrique, "global_station_bloquee", "toutes", ti, run)
      for (st in full) {
        s2 <- sel[MD[sel, "station"] == st]
        if (length(s2) < 12) next
        one(as.dist(M[s2, s2]), MD[s2, ], metrique, "intra_station", st, ti, run)
      }
    }
    lg("  ", run, " termine")
  }
}

lg("=== SYNTHESE ===")
t <- read.delim(TSV, stringsAsFactors = FALSE)
for (disp in unique(t$dispositif)) {
  s <- t[t$dispositif == disp, ]
  cat(sprintf("\n-- %s : %d tests, %d avec p < 0.05\n", disp, nrow(s), sum(s$p < 0.05, na.rm = TRUE)))
  for (me in unique(s$metrique)) {
    for (ti in TISSUS) {
      z <- s[s$metrique == me & s$tissu == ti, ]
      if (!nrow(z)) next
      hy_sup <- sum(z$dist_Hy > z$dist_Cn & z$dist_Hy > z$dist_Pt, na.rm = TRUE)
      cat(sprintf("   %-20s %-9s %2d tests | p<0.05 : %2d | Hy le plus disperse : %2d/%d\n",
                  me, ti, nrow(z), sum(z$p < 0.05, na.rm = TRUE), hy_sup, nrow(z)))
    }
  }
}
cat(sprintf("\nnon-metricite (part de vp negatives) : mediane %.2f %%, max %.2f %%\n",
            median(t$neg_eig_pct, na.rm=TRUE), max(t$neg_eig_pct, na.rm=TRUE)))
lg("TERMINE")
RS

printf '%s\tEND\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log
