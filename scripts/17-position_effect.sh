#!/bin/bash -l
#SBATCH --job-name=pos_effect
#SBATCH --account=ondemand@biomics
#SBATCH --qos=cpu-ondemand-long
#SBATCH --partition=cpu-ondemand
#SBATCH --time=03:00:00
#SBATCH --cpus-per-task=16
#SBATCH --mem=32G
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
set -eEuo pipefail

# 17-position_effect.sh — la position dans la plaque affecte-t-elle la COMPOSITION ?
#
# CONTEXTE. Andre (2026-08-30) : la numerotation des individus au terrain n'est pas
# aleatoire vis-a-vis du genotype (les hotu sont traites en premier car plus fragiles).
# Consequence mesuree : taxon x colonne de plaque, chi2=330, V de Cramer=0.477 ; le
# toxostome n'occupe que les colonnes 1, 2 et 10. Un effet de position pourrait donc
# se faire passer pour un effet taxon. cf docs/decision_stations.md §4.
#
# CE QUI EST DEJA SU. L'effet de la colonne sur la PROFONDEUR persiste a tissu
# constant dans les 4 tissus. Mais la profondeur n'est pas la variable d'interet : la
# rarefaction l'egalise. Ce script teste la COMPOSITION, seule question qui compte.
#
# TROIS PRECAUTIONS DE DESIGN
#
# 1. TISSU TENU CONSTANT. La plaque est ENTIEREMENT determinee par le tissu (1-2
#    caudale, 3-4 branchie, 5-6 hindgut, 7-8 midgut). Un effet "plaque" brut serait un
#    effet tissu deja connu. L'analyse est donc stratifiee PAR TISSU.
#
# 2. SITE TENU FIXE PAR LE SCHEMA DE PERMUTATION. site x colonne sont fortement
#    associes (V=0.593) mais PAS confondus : chaque colonne contient >=2 sites dans
#    chaque tissu. Le test principal utilise des permutations contraintes DANS les
#    blocs de site (how(blocks=site)) : le site est alors fixe par construction, et un
#    effet colonne significatif NE PEUT PAS etre un effet site.
#
# 3. REPLICATION ENTRE RUNS. La position est IDENTIQUE dans les 3 runs (memes
#    librairies), donc les empiler serait de la pseudo-replication (n triple,
#    p anticonservateurs). Chaque run est analyse SEPAREMENT : un effet de position
#    reel doit se repliquer dans les trois ; un artefact ne le fera pas. C'est le
#    temoin qui distingue les deux.
#
# ORDRES SEQUENTIELS RAPPORTES. En PERMANOVA sequentielle chaque terme prend ce qui
# reste apres les precedents. Les deux ordres sont donnes :
#   - colonne EN PREMIER  -> variance MAXIMALE attribuable a la position
#   - colonne APRES site  -> variance UNIQUEMENT attribuable a la position
# Et : colonne d'abord puis taxon -> le signal taxon survit-il a l'ajustement ?
#
# NB vegan 2.7 : adonis2() a by=NULL par defaut (test global unique). by="terms" est
# donc EXPLICITE partout, sans quoi les tests sequentiels ne seraient pas calcules.
#
# RESERVE. La matrice de dissimilarite est une MOYENNE sur 400 rarefactions
# (decision_rarefaction_mode.md). Une moyenne de matrices de Bray-Curtis n'est pas
# garantie de respecter l'inegalite triangulaire ; PERMANOVA n'exige pas la metricite
# mais des valeurs propres negatives sont possibles. Leur part est rapportee.
#
# Sorties : results/position_effect/{position_summary.txt, position_tests.tsv,
#           position_effect_sizes.tsv}
# Ecriture INCREMENTALE : chaque strate est ecrite des qu'elle est calculee, pour que
# un depassement de walltime ne perde pas tout (defaut du script 15, corrige ici).

cd "$HOME/work/projects/microbiome-hybrid"
OUT="${POS_OUTDIR:-results/position_effect}"
mkdir -p "$OUT" logs

RSCRIPT=$HOME/bin/envs/dada2/bin/Rscript
GIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo NA)
printf '%s\tSTART\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log

"$RSCRIPT" - <<'RS'
suppressMessages({library(vegan); library(permute)})
set.seed(20260830)
NPERM <- 999
NCPU  <- as.integer(Sys.getenv("SLURM_CPUS_PER_TASK", "8"))
OUT   <- Sys.getenv("POS_OUTDIR", "results/position_effect")

TESTS <- file.path(OUT, "position_tests.tsv")
EFFS  <- file.path(OUT, "position_effect_sizes.tsv")
cat("run\ttissue\tn\tmodel\tterm\tdf\tR2\tF\tp\n", file = TESTS)
cat("run\ttissue\tn\tterm\tR2_first\tR2_after_site\tp_blocked\n", file = EFFS)

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

add_rows <- function(a, run, tis, n, model) {
  if (is.null(a)) return(invisible(NULL))
  df <- as.data.frame(a)
  for (i in seq_len(nrow(df))) {
    tn <- rownames(df)[i]
    if (tn %in% c("Residual", "Total")) next
    cat(sprintf("%s\t%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s\n", run, tis, n, model, tn,
                fmt(df$Df[i]), fmt(df$R2[i]), fmt(df[[grep("^F", names(df))[1]]][i]),
                fmt(df[[grep("^Pr", names(df))[1]]][i])),
        file = TESTS, append = TRUE)
  }
}
fmt <- function(x) if (is.null(x) || length(x) == 0 || is.na(x)) "NA" else
                   if (is.numeric(x)) formatC(x, digits = 5, format = "g") else as.character(x)

safe <- function(expr) tryCatch(expr, error = function(e) { cat("   ERREUR:", conditionMessage(e), "\n"); NULL })

for (met in c("bray", "jaccard")) {
  f <- sprintf("results/rarefaction/beta_mean_%s_N400.rds", met)
  if (!file.exists(f)) { cat("absent:", f, "\n"); next }
  Dfull <- readRDS(f)
  lab <- attr(Dfull, "Labels")
  M <- as.matrix(Dfull); rm(Dfull); gc(verbose = FALSE)
  cat("\n########## metrique:", met, "##########\n")

  # part de valeurs propres negatives (reserve sur la moyenne de matrices).
  # double-centrage par sweep : evite deux produits matriciels 1784^3.
  D2 <- M^2
  D2 <- sweep(D2, 1, rowMeans(D2))
  D2 <- sweep(D2, 2, colMeans(D2))
  B  <- -0.5 * (D2 + mean(M^2))
  rm(D2); gc(verbose = FALSE)
  ev <- eigen(B, only.values = TRUE, symmetric = TRUE)$values
  rm(B); gc(verbose = FALSE)
  cat(sprintf("valeurs propres negatives : %.3f %% de la somme des |vp|\n",
              100 * sum(abs(ev[ev < 0])) / sum(abs(ev))))

  for (run in c("durance1", "durance2", "durance3")) {
    for (tis in c("caudale", "branchie", "midgut", "hindgut")) {
      keep <- lab[sub("^.*__", "", lab) == run]
      md0  <- meta[keep, , drop = FALSE]
      keep <- keep[!is.na(md0$tissue) & md0$tissue == tis]
      if (length(keep) < 30) next
      md <- meta[keep, , drop = FALSE]
      md$col  <- suppressWarnings(as.integer(sub("^[A-Z]", "", md$well)))
      md$rw   <- substr(md$well, 1, 1)
      md$edge <- factor(ifelse(md$rw %in% c("A","H") | md$col %in% c(1,12), "bord", "interieur"))
      ok <- !is.na(md$col) & !is.na(md$site) & nzchar(md$site)
      md <- md[ok, ]; keep <- keep[ok]
      # ne garder que les niveaux a >=3 echantillons (colonne et site)
      cc <- names(which(table(md$col)  >= 3))
      ss <- names(which(table(md$site) >= 3))
      sel <- as.character(md$col) %in% cc & md$site %in% ss
      md <- md[sel, ]; keep <- keep[sel]
      n <- length(keep)
      if (n < 30 || length(unique(md$col)) < 3 || length(unique(md$site)) < 2) next
      md$colf <- factor(md$col); md$sitef <- factor(md$site)
      md$taxf <- factor(ifelse(nzchar(md$taxon), md$taxon, "inconnu"))
      D <- as.dist(M[keep, keep])
      cat(sprintf("\n--- %s / %s : n=%d, %d colonnes, %d sites ---\n",
                  run, tis, n, length(unique(md$col)), length(unique(md$site))))

      # TEST PRINCIPAL : colonne, permutations contraintes DANS les blocs de site
      h <- how(nperm = NPERM, blocks = md$sitef)
      a_blk <- safe(adonis2(D ~ colf, data = md, permutations = h, by = "terms",
                           parallel = NCPU))
      add_rows(a_blk, run, tis, n, "col_blocked_by_site")

      # ordres sequentiels
      a_cf <- safe(adonis2(D ~ colf + sitef, data = md, permutations = NPERM,
                          by = "terms", parallel = NCPU))
      add_rows(a_cf, run, tis, n, "col_first_then_site")
      a_sf <- safe(adonis2(D ~ sitef + colf, data = md, permutations = NPERM,
                          by = "terms", parallel = NCPU))
      add_rows(a_sf, run, tis, n, "site_first_then_col")

      # Le signal taxon survit-il a l'ajustement sur la colonne ?
      # PRECAUTION : taxon et site sont largement confondus dans ce plan. Si le taxon
      # est NICHE dans le site (un seul taxon par site), il n'est pas separable du site
      # et le test serait un test de site deguise. On verifie donc d'abord que le taxon
      # VARIE a l'interieur d'au moins un site, et on permute dans les blocs de site :
      # le site est alors fixe, et seule la part de taxon separable du site est testee.
      tax_within <- sum(tapply(as.character(md$taxf), md$sitef,
                               function(z) length(unique(z)) > 1), na.rm = TRUE)
      cat(sprintf("   taxon variable a l'interieur de %d site(s) sur %d\n",
                  tax_within, length(unique(md$sitef))))
      if (tax_within >= 1 && length(unique(md$taxf)) >= 2) {
        a_ct <- safe(adonis2(D ~ colf + taxf, data = md, permutations = h,
                            by = "terms", parallel = NCPU))
        add_rows(a_ct, run, tis, n, "col_then_taxon_blocked_by_site")
      } else {
        cat("   -> taxon NICHE dans le site : non separable, test non effectue\n")
        cat(sprintf("%s\t%s\t%d\ttaxon_nested_in_site\ttaxf\tNA\tNA\tNA\tNA\n",
                    run, tis, n), file = TESTS, append = TRUE)
      }

      # rangee et bord (artefacts de plaque classiques), site fixe par les blocs
      a_rw <- safe(adonis2(D ~ factor(rw), data = md, permutations = h, by = "terms",
                          parallel = NCPU))
      add_rows(a_rw, run, tis, n, "row_blocked_by_site")
      a_ed <- safe(adonis2(D ~ edge, data = md, permutations = h, by = "terms",
                          parallel = NCPU))
      add_rows(a_ed, run, tis, n, "edge_blocked_by_site")

      # synthese des tailles d'effet pour la colonne
      g <- function(a, term) { if (is.null(a)) return(NA_real_)
        d <- as.data.frame(a); i <- match(term, rownames(d)); if (is.na(i)) NA_real_ else d$R2[i] }
      gp <- function(a, term) { if (is.null(a)) return(NA_real_)
        d <- as.data.frame(a); i <- match(term, rownames(d)); if (is.na(i)) NA_real_ else
        d[[grep("^Pr", names(d))[1]]][i] }
      cat(sprintf("%s\t%s\t%d\tcolonne\t%s\t%s\t%s\n", run, tis, n,
                  fmt(g(a_cf, "colf")), fmt(g(a_sf, "colf")), fmt(gp(a_blk, "colf"))),
          file = EFFS, append = TRUE)
      cat(sprintf("   colonne : R2 en premier=%.4f | R2 apres site=%.4f | p (blocs site)=%s\n",
                  g(a_cf, "colf"), g(a_sf, "colf"), fmt(gp(a_blk, "colf"))))
      cat(sprintf("   site    : R2 en premier=%.4f | R2 apres colonne=%.4f\n",
                  g(a_sf, "sitef"), g(a_cf, "sitef")))
      flush.console()
    }
  }
  # une seule metrique suffit pour la decision ; jaccard en confirmation
  if (met == "bray") cat("\n(bray termine ; jaccard en confirmation)\n")
}
cat("\n=== termine ===\n")
RS

# synthese lisible
$HOME/bin/envs/dada2/bin/Rscript - <<'RS' > "$OUT"/position_summary.txt
OUT <- Sys.getenv("POS_OUTDIR", "results/position_effect")
t <- read.delim(file.path(OUT, "position_tests.tsv"), stringsAsFactors = FALSE)
e <- read.delim(file.path(OUT, "position_effect_sizes.tsv"), stringsAsFactors = FALSE)
cat("=== EFFET DE POSITION SUR LA COMPOSITION ===\n\n")
cat("Test principal : colonne de plaque, permutations contraintes dans les blocs de\n")
cat("site (le site est fixe par construction, un effet colonne ne peut pas etre un\n")
cat("effet site). Stratifie par tissu, chaque run analyse separement.\n\n")
b <- t[t$model == "col_blocked_by_site" & t$term == "colf", ]
cat(sprintf("strates testees : %d\n", nrow(b)))
cat(sprintf("dont p < 0.05   : %d\n", sum(b$p < 0.05, na.rm = TRUE)))
cat(sprintf("R2 de la colonne : median %.4f  [%.4f - %.4f]\n\n",
            median(b$R2, na.rm = TRUE), min(b$R2, na.rm = TRUE), max(b$R2, na.rm = TRUE)))
cat("--- par strate (test contraint par site) ---\n")
print(b[order(b$run, b$tissue), c("run","tissue","n","df","R2","F","p")], row.names = FALSE)
cat("\n--- replication entre runs (un effet reel doit se repliquer) ---\n")
for (ti in unique(b$tissue)) {
  s <- b[b$tissue == ti, ]
  cat(sprintf("  %-9s p = %s\n", ti, paste(sprintf("%s:%.3f", s$run, s$p), collapse = "  ")))
}
cat("\n--- taille d'effet de la colonne selon l'ordre ---\n")
print(e[order(e$run, e$tissue), ], row.names = FALSE)
cat("\n--- taxon apres ajustement sur la colonne (site fixe par les blocs) ---\n")
cat("    NB : les strates ou le taxon est niche dans le site sont marquees NA :\n")
cat("    le taxon n'y est pas separable du site, le test serait un test de site.\n")
x <- t[t$model %in% c("col_then_taxon_blocked_by_site","taxon_nested_in_site"), ]
print(x[order(x$run, x$tissue, x$term), c("run","tissue","term","df","R2","p")], row.names = FALSE)
cat("\n--- rangee et bord (artefacts de plaque classiques) ---\n")
y <- t[t$model %in% c("row_blocked_by_site","edge_blocked_by_site"), ]
print(y[order(y$model, y$run, y$tissue), c("model","run","tissue","term","R2","p")], row.names = FALSE)
cat("\n--- reference : site et tissu, pour comparer les ordres de grandeur ---\n")
z <- t[t$model == "site_first_then_col" & t$term == "sitef", ]
cat(sprintf("R2 du site (en premier) : median %.4f  [%.4f - %.4f]\n",
            median(z$R2, na.rm = TRUE), min(z$R2, na.rm = TRUE), max(z$R2, na.rm = TRUE)))
RS

printf '%s\tEND\t%s\t%s\t%s\n' "$(date -Is)" "${SLURM_JOB_ID:-local}" "$GIT_HASH" "$(basename "$0")" >> runs.log
cat "$OUT"/position_summary.txt
