#!/bin/bash -l
#SBATCH --job-name=pos_control
#SBATCH --account=ondemand@biomics
#SBATCH --qos=cpu-ondemand-long
#SBATCH --partition=cpu-ondemand
#SBATCH --time=02:00:00
#SBATCH --cpus-per-task=16
#SBATCH --mem=32G
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
set -eEuo pipefail

# 18-position_control.sh — l'effet de position est-il distinct de l'EFFET TAXON ?
#
# CE QUE 17 A ETABLI. L'effet de la colonne de plaque sur la composition est
# significatif dans les 24 strates (12 strates x 2 metriques, p <= 0.007), replique
# dans les 3 runs, avec un site tenu fixe par les blocs de permutation. Il n'est donc
# PAS un effet site.
#
# LA FAILLE DE 17. Le blocage par site ne fixe PAS le taxon. Or dans les 4 sites ou le
# taxon varie, colonne et taxon sont fortement confondus :
#   Ain V=0.502 | Avi V=0.588 | Bue V=0.826 | Man V=0.951
# L'effet colonne mesure par 17 pourrait donc etre, en partie, un effet taxon.
#
# LE TEMOIN QUI ISOLE. Cinq sites n'ont QU'UN SEUL taxon sequence :
#   Bau (Ch), Caa (Ch), Cab (Ch), Jus (Ch), Per (Ch)
# Dans ces sites, avec le site fixe par les blocs de permutation, le taxon est constant
# par construction : un effet colonne y est necessairement POSITIONNEL, pas taxonomique.
#
# Cab est ECARTE de ce temoin : il couvre DEUX stations physiques du Suran (Pont-d'Ain
# et Chavannes, cf docs/decision_stations.md §2), donc la colonne pourrait y encoder la
# station, qui resoudra en genotypes differents. Le temoin retient Bau, Caa, Jus, Per.
#
# CONTRE-TEMOIN. Le meme test est fait sur les sites MULTI-taxons : si l'effet colonne
# y est plus fort, c'est que le taxon y contribue.
#
# TEST SYMETRIQUE. D ~ taxon + colonne (taxon en PREMIER) : la colonne conserve-t-elle
# un signal une fois le taxon servi d'abord ? C'est l'ordre defavorable a la colonne.
#
# NB vegan 2.7 : by="terms" est explicite (defaut = NULL, test global unique).
#
# Sortie : results/position_effect/position_control.txt (+ position_control.tsv)

cd "$HOME/work/projects/microbiome-hybrid"
OUT="${POS_OUTDIR:-results/position_effect}"
mkdir -p "$OUT" logs
RSCRIPT=$HOME/bin/envs/dada2/bin/Rscript
GIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo NA)
printf '%s\tSTART\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log

"$RSCRIPT" - <<'RS' > "$OUT"/position_control.txt
suppressMessages({library(vegan); library(permute)})
set.seed(20260830)
NPERM <- 999
NCPU  <- as.integer(Sys.getenv("SLURM_CPUS_PER_TASK", "8"))
TSV   <- file.path(Sys.getenv("POS_OUTDIR", "results/position_effect"), "position_control.tsv")
cat("metric\tsubset\trun\ttissue\tn\tmodel\tterm\tdf\tR2\tF\tp\n", file = TSV)

meta <- read.csv("metadata/samples_all.csv", stringsAsFactors = FALSE)
rownames(meta) <- meta$dada2_id

# ---------------------------------------------------------------- PASSE (2026-09-25)
# PASSE=morpho : comportement d'origine (taxon morphologique de samples_all.csv).
# PASSE=aout   : categorie genotypique d'aout (12 chr), 180 individus.
# PASSE=2      : categorie de septembre (25 chr), 42 Hy, 180 individus.
# PASSE=1      : categorie de septembre, 22 quasi-purs EXCLUS, 158 individus.
PASSE <- Sys.getenv("PASSE", "")
if (!PASSE %in% c("morpho","aout","2","1"))
  stop("PASSE doit valoir morpho, aout, 2 ou 1 (recu : '", PASSE, "')")
if (PASSE != "morpho") {
  AM <- read.csv("metadata/analysis_metadata.csv", stringsAsFactors = FALSE)
  stopifnot(all(c("dada2_id","individual_id","categorie","categorie_aout_12chr","inclus_passe1") %in% names(AM)))
  if (PASSE == "1") AM <- AM[as.character(AM$inclus_passe1) %in% c("True","TRUE"), ]
  catv <- if (PASSE == "aout") AM$categorie_aout_12chr else AM$categorie
  names(catv) <- AM$dada2_id
  meta <- meta[rownames(meta) %in% AM$dada2_id, , drop = FALSE]
  meta$taxon <- unname(catv[rownames(meta)])
  u <- !duplicated(AM$individual_id)
  cat(sprintf("PASSE=%s : %d echantillons dans meta, %d individus | %s\n", PASSE, nrow(meta),
              sum(u), paste(names(table(catv[u])), table(catv[u]), sep="=", collapse=" ")))
} else cat("PASSE=morpho : taxon morphologique de samples_all.csv (comportement d'origine)\n")

MONO  <- c("Bau","Caa","Jus","Per")               # un seul taxon ET une seule station
MULTI <- c("Ain","Avi","Bue","Man")               # taxon variable -> contre-temoin

# ---------------------------------------------------------------- SOUS-ENSEMBLES (2026-09-25)
# DEFAUT DU TEMOIN D'ORIGINE. MONO a ete choisi sur le taxon MORPHOLOGIQUE : ces quatre sites
# ne portaient que des "chondrostome" (Ch), c'est-a-dire des poissons NON RESOLUS au terrain.
# Genotypes, aucun n'est mono-categorie (aout : Bau 0/4/21, Caa 8/4/8, Jus 8/3/8, Per 0/1/8).
# Sous toute classification genotypique, AUCUN code de site n'est mono-categorie. Le temoin
# "taxon constant par construction" n'existe donc plus sous cette forme.
# REMPLACEMENT VALIDE : sous-ensembles INTRA-CATEGORIE (seuls les Cn, seuls les Pt, seuls
# les Hy), blocs de site. La categorie y est constante par construction : un effet colonne y
# est necessairement positionnel au regard de la categorie. "toutes" garde le test
# symetrique (categorie d'abord, colonne ensuite) sur l'ensemble des sites.
# En PASSE=morpho, les sous-ensembles d'origine sont conserves a l'identique (reproduction).
if (PASSE == "morpho") {
  SUBS <- list(mono_taxon  = function(md) md$site %in% MONO,
               multi_taxon = function(md) md$site %in% MULTI)
} else {
  SUBS <- list(toutes   = function(md) rep(TRUE, nrow(md)),
               intra_Cn = function(md) !is.na(md$taxon) & md$taxon == "Cn",
               intra_Pt = function(md) !is.na(md$taxon) & md$taxon == "Pt",
               intra_Hy = function(md) !is.na(md$taxon) & md$taxon == "Hy")
}

fmt <- function(x) if (is.null(x) || length(x)==0 || is.na(x)) "NA" else
                   if (is.numeric(x)) formatC(x, digits=5, format="g") else as.character(x)
emit <- function(a, met, sub, run, tis, n, model) {
  if (is.null(a)) return(invisible(NULL))
  d <- as.data.frame(a)
  fc <- grep("^F", names(d))[1]; pc <- grep("^Pr", names(d))[1]
  for (i in seq_len(nrow(d))) {
    tn <- rownames(d)[i]
    if (tn %in% c("Residual","Total")) next
    cat(sprintf("%s\t%s\t%s\t%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s\n", met, sub, run, tis, n,
                model, tn, fmt(d$Df[i]), fmt(d$R2[i]), fmt(d[[fc]][i]), fmt(d[[pc]][i])),
        file = TSV, append = TRUE)
  }
}
safe <- function(e) tryCatch(e, error=function(err){cat("  ERREUR:",conditionMessage(err),"\n"); NULL})
getv <- function(a, term, what="R2") { if (is.null(a)) return(NA_real_)
  d <- as.data.frame(a); i <- match(term, rownames(d)); if (is.na(i)) return(NA_real_)
  if (what=="R2") d$R2[i] else d[[grep("^Pr",names(d))[1]]][i] }

for (met in c("bray","jaccard")) {
  M <- as.matrix(readRDS(sprintf("results/rarefaction/beta_mean_%s_N400.rds", met)))
  lab <- rownames(M)
  cat("\n##########", met, "##########\n")

  for (sub in names(SUBS)) {
    fsub <- SUBS[[sub]]
    cat(sprintf("\n=== sous-ensemble %s ===\n", sub))
    for (run in c("durance1","durance2","durance3")) {
      for (tis in c("caudale","branchie","midgut","hindgut")) {
        keep <- lab[sub("^.*__","",lab)==run]
        md <- meta[keep, , drop=FALSE]
        sel <- !is.na(md$tissue) & md$tissue==tis & fsub(md)
        keep <- keep[sel]; md <- meta[keep, , drop=FALSE]
        md$col <- suppressWarnings(as.integer(sub("^[A-Z]","",md$well)))
        ok <- !is.na(md$col) & nzchar(md$site); md <- md[ok,]; keep <- keep[ok]
        cc <- names(which(table(md$col) >= 3)); ss <- names(which(table(md$site) >= 3))
        s2 <- as.character(md$col) %in% cc & md$site %in% ss
        md <- md[s2,]; keep <- keep[s2]
        n <- length(keep)
        if (n < 30 || length(unique(md$col)) < 3 || length(unique(md$site)) < 2) {
          cat(sprintf("  %s / %s : n=%d -> ignore\n", run, tis, n)); next }
        md$colf <- factor(md$col); md$sitef <- factor(md$site)
        md$taxf <- factor(ifelse(nzchar(md$taxon), md$taxon, "inconnu"))
        # rang de colonne DANS le site : alternative a 1 df, plus puissante
        # rang de colonne DANS le site, par affectation explicite (pas de reindexation
        # implicite : l'astuce split/unlist/order est correcte mais invérifiable a la lecture)
        md$crank <- NA_real_
        for (ss_ in levels(md$sitef)) {
          ii_ <- which(md$sitef == ss_)
          md$crank[ii_] <- as.numeric(factor(md$col[ii_]))
        }
        stopifnot(!any(is.na(md$crank)))
        D <- as.dist(M[keep, keep])
        ntax <- length(unique(md$taxf))
        cat(sprintf("\n  --- %s / %s : n=%d | %d colonnes | %d sites | %d taxon(s) ---\n",
                    run, tis, n, length(unique(md$col)), length(unique(md$site)), ntax))
        h <- how(nperm=NPERM, blocks=md$sitef)

        a1 <- safe(adonis2(D ~ colf, data=md, permutations=h, by="terms", parallel=NCPU))
        emit(a1, met, sub, run, tis, n, "col_blocked_by_site")
        cat(sprintf("     colonne (facteur, %s df) : R2=%.4f  p=%s\n",
                    fmt(as.data.frame(a1)$Df[1]), getv(a1,"colf"), fmt(getv(a1,"colf","p"))))

        a2 <- safe(adonis2(D ~ crank, data=md, permutations=h, by="terms", parallel=NCPU))
        emit(a2, met, sub, run, tis, n, "colrank_blocked_by_site")
        cat(sprintf("     rang de colonne dans le site (1 df) : R2=%.4f  p=%s\n",
                    getv(a2,"crank"), fmt(getv(a2,"crank","p"))))

        # test symetrique : taxon EN PREMIER, colonne ensuite (ordre defavorable)
        if (ntax >= 2) {
          a3 <- safe(adonis2(D ~ taxf + colf, data=md, permutations=h, by="terms", parallel=NCPU))
          emit(a3, met, sub, run, tis, n, "taxon_first_then_col")
          cat(sprintf("     [taxon d'abord] taxon R2=%.4f p=%s | colonne R2=%.4f p=%s\n",
                      getv(a3,"taxf"), fmt(getv(a3,"taxf","p")),
                      getv(a3,"colf"), fmt(getv(a3,"colf","p"))))
        } else {
          cat("     taxon constant dans ce sous-ensemble : effet colonne NECESSAIREMENT positionnel\n")
        }
        flush.console()
      }
    }
  }
}
cat("\n=== termine ===\n")
RS

printf '%s\tEND\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log
tail -40 "$OUT"/position_control.txt
