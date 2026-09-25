#!/bin/bash -l
#SBATCH --job-name=var_part_cat
#SBATCH --account=ondemand@biomics
#SBATCH --qos=cpu-ondemand-long
#SBATCH --partition=cpu-ondemand
#SBATCH --time=03:00:00
#SBATCH --cpus-per-task=16
#SBATCH --mem=32G
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
set -eEuo pipefail

# 20-variance_partition_category.sh — part de variance de la CATEGORIE, encadree
#
# OBJET. Chiffrer ce que la categorie genotypique (Cn / Hy / Pt) explique de la
# composition, en presence des deux facteurs avec lesquels elle est confondue :
# la STATION et la POSITION dans la plaque.
#
# POURQUOI UN ENCADREMENT ET NON UNE VALEUR. En PERMANOVA sequentielle chaque terme
# prend ce qui reste apres les precedents. Les trois facteurs etant enchevetres
# (categorie x colonne : V de Cramer = 0.504 sur l'ensemble, 0.56 a 0.69 dans les trois
# stations a gradient complet), l'ordre change la valeur. Les DEUX ordres sont donc
# rapportes :
#   ordre MIN : position + station + categorie  -> categorie servie en dernier
#   ordre MAX : categorie + station + position  -> categorie servie en premier
# L'intervalle entre les deux est le degre d'incertitude imputable au confondant.
# Rapporter un seul ordre serait choisir la reponse.
#
# POURQUOI STRATIFIE PAR TISSU, ET POURQUOI PAS DE TERME D'IDENTITE DU POISSON.
# Verifie sur les donnees : 168 des 180 poissons occupent la MEME colonne dans les
# quatre tissus (meme puits sur quatre plaques differentes). Dans un modele groupe
# portant l'identite du poisson, la position est donc entierement absorbee et n'est
# PAS estimable. Elle ne l'est qu'a tissu stratifie, ou il y a un echantillon par
# poisson. C'est aussi pour cela que la partition du script 14 ne pouvait pas porter
# de terme de position : ce n'est pas un oubli reparable, c'est une contrainte du plan.
#
# CHAQUE RUN SEPAREMENT. La position est identique dans les 3 runs (memes librairies) :
# les empiler serait de la pseudo-replication. Un effet reel doit se repliquer.
#
# TROIS TEMOINS
#  (a) test de categorie a STATION FIXE : permutations contraintes dans les blocs de
#      station, position servie d'abord. C'est le test conservateur pour la categorie.
#  (b) ROSIERES, seule station ou categorie et position sont statistiquement
#      independantes (V = 0.181, p = 0.35 ; 96 des 100 echantillons en colonnes
#      partagees). Contraste Hy vs Pt affranchi de la position — mais 4 hybrides
#      seulement, donc temoin et non test principal.
#  (c) SOUS-PLAN SEPARABLE : echantillons situes dans des colonnes occupees par TOUTES
#      les categories de leur station (90 individus, dont 32 dans une station a
#      gradient complet). Analyse de sensibilite : si la conclusion y change de signe,
#      le confondant la produit.
#
# NB vegan 2.7 : by= vaut NULL par defaut (test global unique). by="terms" et
# by="margin" sont donc EXPLICITES partout.
#
# METRIQUES. Le script balaie results/rarefaction/beta_mean_*.rds : il prend donc
# automatiquement UniFrac en compte des que le script 21 l'aura produit. La colonne
# `metrique` est ecrite dans la table de sortie (defaut du script 17, corrige ici).
#
# Sorties : results/var_partition_cat/{category_partition.tsv, category_summary.txt}

cd "$HOME/work/projects/microbiome-hybrid"
OUT="${CATPART_OUTDIR:-results/var_partition_cat}"
mkdir -p "$OUT" logs
RSCRIPT=$HOME/bin/envs/dada2/bin/Rscript
GIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo NA)
printf '%s\tSTART\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log

"$RSCRIPT" - <<'RS' > "$OUT"/category_summary.txt
suppressMessages({library(vegan); library(permute)})
set.seed(20260830)
NPERM <- 999
NCPU  <- as.integer(Sys.getenv("SLURM_CPUS_PER_TASK", "8"))
OUT   <- Sys.getenv("CATPART_OUTDIR", "results/var_partition_cat")
TSV   <- file.path(OUT, "category_partition.tsv")
cat("metrique\tsous_ensemble\trun\ttissu\tn\tmodele\tterme\tdf\tR2\tF\tp\n", file = TSV)

MD <- read.csv("metadata/analysis_metadata.csv", stringsAsFactors = FALSE)
for (cn in c("dada2_id","individual_id","run_label","tissue","station","categorie",
             "well_col","col_rank_station"))
  stopifnot(cn %in% names(MD))

# ---------------------------------------------------------------- PASSE (2026-09-25)
# PASSE=aout : categorie d'aout (12 chr) | 2 : septembre, 42 Hy, n=180 |
# 1 : septembre, 22 quasi-purs EXCLUS (pas reverses dans leur classe parentale), n=158.
PASSE <- Sys.getenv("PASSE", "")
if (!PASSE %in% c("aout","2","1")) stop("PASSE doit valoir aout, 2 ou 1 (recu : '", PASSE, "')")
stopifnot(all(c("categorie","categorie_aout_12chr","inclus_passe1") %in% names(MD)))
if (PASSE == "aout") MD$categorie <- MD$categorie_aout_12chr
if (PASSE == "1")    MD <- MD[as.character(MD$inclus_passe1) %in% c("True","TRUE"), ]
.u <- !duplicated(MD$individual_id)
cat(sprintf("PASSE=%s : %d echantillons, %d individus | %s\n", PASSE, nrow(MD), sum(.u),
            paste(names(table(MD$categorie[.u])), table(MD$categorie[.u]), sep="=", collapse=" ")))
rownames(MD) <- MD$dada2_id

fmt <- function(x) if (is.null(x) || length(x)==0 || is.na(x)) "NA" else
                   if (is.numeric(x)) formatC(x, digits=5, format="g") else as.character(x)
emit <- function(a, met, sub, run, tis, n, model) {
  if (is.null(a)) return(invisible(NULL))
  d <- as.data.frame(a); fc <- grep("^F", names(d))[1]; pc <- grep("^Pr", names(d))[1]
  for (i in seq_len(nrow(d))) {
    tn <- rownames(d)[i]
    if (tn %in% c("Residual","Total")) next
    cat(sprintf("%s\t%s\t%s\t%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s\n", met, sub, run, tis, n,
                model, tn, fmt(d$Df[i]), fmt(d$R2[i]), fmt(d[[fc]][i]), fmt(d[[pc]][i])),
        file = TSV, append = TRUE)
  }
}
safe <- function(e) tryCatch(e, error=function(err){cat("   ERREUR:",conditionMessage(err),"\n"); NULL})
gv <- function(a, term, what="R2") { if (is.null(a)) return(NA_real_)
  d <- as.data.frame(a); i <- match(term, rownames(d)); if (is.na(i)) return(NA_real_)
  if (what=="R2") d$R2[i] else d[[grep("^Pr",names(d))[1]]][i] }

# colonnes partagees par TOUTES les categories d'une station -> sous-plan separable
shared_ids <- function(md) {
  keep <- character(0)
  for (st in unique(md$station)) {
    s <- md[md$station == st, ]
    if (length(unique(s$categorie)) < 2) next
    t <- table(s$categorie, s$well_col)
    cols <- colnames(t)[colSums(t > 0) == nrow(t)]
    keep <- c(keep, s$dada2_id[as.character(s$well_col) %in% cols])
  }
  keep
}

files <- Sys.glob(Sys.getenv("CATPART_GLOB", "results/rarefaction/beta_mean_*.rds"))
stopifnot(length(files) > 0)
cat("matrices trouvees :", paste(basename(files), collapse=", "), "\n")

for (f in files) {
  met <- sub("^beta_mean_(.*)_N[0-9]+\\.rds$", "\\1", basename(f))
  M <- as.matrix(readRDS(f)); lab <- rownames(M)
  cat("\n##################### metrique:", met, "#####################\n")

  for (run in c("durance1","durance2","durance3")) {
    for (tis in c("caudale","branchie","midgut","hindgut")) {
      base <- lab[lab %in% MD$dada2_id]
      md0 <- MD[base, ]
      ids <- base[md0$run_label == run & md0$tissue == tis]
      if (length(ids) < 30) next
      md <- MD[ids, ]
      md$cat <- factor(md$categorie); md$st <- factor(md$station)
      md$pos <- as.numeric(md$col_rank_station)
      stopifnot(!any(is.na(md$pos)))
      if (nlevels(md$cat) < 2 || nlevels(md$st) < 2) next
      D <- as.dist(M[ids, ids]); n <- length(ids)
      cat(sprintf("\n--- %s / %s : n=%d | %d categories | %d stations ---\n",
                  run, tis, n, nlevels(md$cat), nlevels(md$st)))

      # ENCADREMENT
      aMIN <- safe(adonis2(D ~ pos + st + cat, data=md, permutations=NPERM,
                           by="terms", parallel=NCPU))
      emit(aMIN, met, "complet", run, tis, n, "ordre_MIN_pos_st_cat")
      aMAX <- safe(adonis2(D ~ cat + st + pos, data=md, permutations=NPERM,
                           by="terms", parallel=NCPU))
      emit(aMAX, met, "complet", run, tis, n, "ordre_MAX_cat_st_pos")
      aMRG <- safe(adonis2(D ~ cat + st + pos, data=md, permutations=NPERM,
                           by="margin", parallel=NCPU))
      emit(aMRG, met, "complet", run, tis, n, "marginal")
      cat(sprintf("   categorie : R2 min=%.4f  max=%.4f  unique(marginal)=%.4f\n",
                  gv(aMIN,"cat"), gv(aMAX,"cat"), gv(aMRG,"cat")))
      cat(sprintf("   station   : R2 min=%.4f  max=%.4f | position : min=%.4f max=%.4f\n",
                  gv(aMAX,"st"), gv(aMIN,"st"), gv(aMAX,"pos"), gv(aMIN,"pos")))

      # TEMOIN (a) : categorie a station FIXE par les blocs, position servie d'abord
      h <- how(nperm=NPERM, blocks=md$st)
      aBLK <- safe(adonis2(D ~ pos + cat, data=md, permutations=h, by="terms",
                           parallel=NCPU))
      emit(aBLK, met, "complet", run, tis, n, "cat_apres_pos_station_bloquee")
      cat(sprintf("   [station fixee] categorie R2=%.4f  p=%s\n",
                  gv(aBLK,"cat"), fmt(gv(aBLK,"cat","p"))))

      # SANS POSITION (decision D2, 2026-09-25) : modele principal. Les modeles avec position
      # ci-dessus deviennent l'analyse de sensibilite. Le flux aleatoire est sauvegarde puis
      # restaure : les modeles d'origine recoivent exactement les memes permutations qu'avant,
      # donc la passe "aout" doit reproduire a l'identique les R2 ET les p-values d'aout.
      .rs <- get(".Random.seed", envir = globalenv())
      .k <- utf8ToInt(paste(met, run, tis)); set.seed(20260925L + sum(.k * seq_along(.k)))  # distincte par strate ET par run
      aN1 <- safe(adonis2(D ~ st + cat, data=md, permutations=NPERM, by="terms", parallel=NCPU))
      emit(aN1, met, "complet", run, tis, n, "sanspos_MIN_st_cat")
      aN2 <- safe(adonis2(D ~ cat + st, data=md, permutations=NPERM, by="terms", parallel=NCPU))
      emit(aN2, met, "complet", run, tis, n, "sanspos_MAX_cat_st")
      aN3 <- safe(adonis2(D ~ cat, data=md, permutations=how(nperm=NPERM, blocks=md$st),
                          by="terms", parallel=NCPU))
      emit(aN3, met, "complet", run, tis, n, "sanspos_cat_station_bloquee")
      assign(".Random.seed", .rs, envir = globalenv())
      cat(sprintf("   [SANS position] categorie R2 min=%.4f max=%.4f | station fixee R2=%.4f p=%s\n",
                  gv(aN1,"cat"), gv(aN2,"cat"), gv(aN3,"cat"), fmt(gv(aN3,"cat","p"))))

      # TEMOIN (c) : sous-plan separable
      sids <- intersect(ids, shared_ids(md))
      if (length(sids) >= 30) {
        ms <- MD[sids, ]; ms$cat <- factor(ms$categorie); ms$st <- factor(ms$station)
        ms$pos <- as.numeric(ms$col_rank_station)
        if (nlevels(ms$cat) >= 2 && nlevels(ms$st) >= 2) {
          Ds <- as.dist(M[sids, sids])
          hs <- how(nperm=NPERM, blocks=ms$st)
          aS <- safe(adonis2(Ds ~ pos + cat, data=ms, permutations=hs, by="terms",
                             parallel=NCPU))
          emit(aS, met, "separable", run, tis, length(sids), "cat_apres_pos_station_bloquee")
          cat(sprintf("   [sous-plan separable n=%d] categorie R2=%.4f  p=%s\n",
                      length(sids), gv(aS,"cat"), fmt(gv(aS,"cat","p"))))
        }
      } else cat(sprintf("   [sous-plan separable] n=%d -> trop petit\n", length(sids)))

      # TEMOIN (b) : Rosieres, position independante de la categorie
      rids <- ids[md$station == "Rosieres"]
      if (length(rids) >= 15) {
        mr <- MD[rids, ]; mr$cat <- factor(mr$categorie)
        mr$pos <- as.numeric(mr$col_rank_station)
        if (nlevels(mr$cat) >= 2 && length(unique(mr$pos)) >= 2) {
          Dr <- as.dist(M[rids, rids])
          aR <- safe(adonis2(Dr ~ cat, data=mr, permutations=NPERM, by="terms",
                             parallel=NCPU))
          emit(aR, met, "rosieres", run, tis, length(rids), "cat_seule")
          aRp <- safe(adonis2(Dr ~ pos + cat, data=mr, permutations=NPERM, by="terms",
                              parallel=NCPU))
          emit(aRp, met, "rosieres", run, tis, length(rids), "cat_apres_pos")
          cat(sprintf("   [Rosieres n=%d, %d cat.] categorie seule R2=%.4f p=%s | apres position R2=%.4f p=%s\n",
                      length(rids), nlevels(mr$cat), gv(aR,"cat"), fmt(gv(aR,"cat","p")),
                      gv(aRp,"cat"), fmt(gv(aRp,"cat","p"))))
        }
      }
      flush.console()
    }
  }
}

cat("\n\n=============== SYNTHESE ===============\n")
t <- read.delim(TSV, stringsAsFactors = FALSE)
cat("\n--- encadrement de la categorie (R2), par metrique ---\n")
for (me in unique(t$metrique)) {
  mn <- t[t$metrique==me & t$modele=="ordre_MIN_pos_st_cat" & t$terme=="cat" & t$sous_ensemble=="complet",]
  mx <- t[t$metrique==me & t$modele=="ordre_MAX_cat_st_pos" & t$terme=="cat" & t$sous_ensemble=="complet",]
  mg <- t[t$metrique==me & t$modele=="marginal" & t$terme=="cat" & t$sous_ensemble=="complet",]
  cat(sprintf("  %-10s R2 min median=%.4f | max median=%.4f | unique median=%.4f  (%d strates)\n",
              me, median(mn$R2,na.rm=TRUE), median(mx$R2,na.rm=TRUE),
              median(mg$R2,na.rm=TRUE), nrow(mn)))
}
cat("\n--- SANS POSITION (D2) : encadrement et station fixee ---\n")
for (me in unique(t$metrique)) {
  mn <- t[t$metrique==me & t$modele=="sanspos_MIN_st_cat" & t$terme=="cat",]
  mx <- t[t$metrique==me & t$modele=="sanspos_MAX_cat_st" & t$terme=="cat",]
  bk <- t[t$metrique==me & t$modele=="sanspos_cat_station_bloquee" & t$terme=="cat",]
  cat(sprintf("  %-20s R2 min median=%.4f | max median=%.4f | station fixee %2d/%2d p<0.05\n",
              me, median(mn$R2,na.rm=TRUE), median(mx$R2,na.rm=TRUE),
              sum(bk$p<0.05,na.rm=TRUE), nrow(bk)))
}
cat("\n--- categorie a station fixee : significativite par strate ---\n")
b <- t[t$modele=="cat_apres_pos_station_bloquee" & t$terme=="cat",]
for (me in unique(b$metrique)) for (su in unique(b$sous_ensemble)) {
  s <- b[b$metrique==me & b$sous_ensemble==su,]
  if (!nrow(s)) next
  cat(sprintf("  %-10s %-10s %2d/%2d strates p<0.05 | R2 median=%.4f\n",
              me, su, sum(s$p<0.05, na.rm=TRUE), nrow(s), median(s$R2, na.rm=TRUE)))
}
cat("\n--- detail par strate (jeu complet, station fixee) ---\n")
bb <- b[b$sous_ensemble=="complet",]
print(bb[order(bb$metrique, bb$tissu, bb$run), c("metrique","run","tissu","n","df","R2","p")],
      row.names = FALSE)
cat("\n--- temoin Rosieres (position independante de la categorie) ---\n")
r <- t[t$sous_ensemble=="rosieres" & t$terme=="cat",]
if (nrow(r)) print(r[order(r$metrique,r$tissu,r$run,r$modele),
                     c("metrique","run","tissu","n","modele","R2","p")], row.names=FALSE) else
  cat("  (aucune strate exploitable)\n")
cat("\n--- position et station, pour situer les ordres de grandeur ---\n")
for (tm in c("pos","st")) {
  s <- t[t$modele=="ordre_MIN_pos_st_cat" & t$terme==tm & t$sous_ensemble=="complet",]
  cat(sprintf("  %-3s R2 median (servi en premier pour pos) = %.4f  [%.4f - %.4f]\n",
              tm, median(s$R2,na.rm=TRUE), min(s$R2,na.rm=TRUE), max(s$R2,na.rm=TRUE)))
}
cat("\n=== termine ===\n")
RS

printf '%s\tEND\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log
tail -60 "$OUT"/category_summary.txt
