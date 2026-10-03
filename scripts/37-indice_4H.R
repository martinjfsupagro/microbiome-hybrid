# 37-indice_4H.R — indice 4H (Camper et al. 2024, HybridMicrobiomes 0.1.1)
#
# Plan pre-declare : docs/plan_4H_2026-10-03.md (commite AVANT tout calcul d'indice).
# Decisions : D4 (deux passes), D5 (rho = 0.5 au genre ; sensibilite rho 0.3 / 0.7 ;
# theta = epsilon = 0), D6 (4 tissus ; strate abandonnee si une classe < 10 individus).
#
# ENSEMBLE D'ECHANTILLONS : identique aux analyses de composition (scripts 15 et 20) —
# echantillons de results/decontam/asv_table_clean.tsv a >= 3000 lectures, presents dans
# metadata/analysis_metadata.csv, restreints a la passe. Verifie contre les lignes de
# results/rarefaction/beta_mean_bray_N400.rds (arret si different).
#
# CLASSES : Progenitor One = 1 = Cn ; Hybrids = 2 = Hy ; Progenitor Two = 3 = Pt (notation
# imposee par le package). Une strate = passe x tissu x run ; chaque run traite a part
# (memes librairies sequencees trois fois : les empiler serait de la pseudo-replication).
#
# EFFECTIF COMMUN : sample_no doit etre < effectif de la plus petite classe (aide du
# package). N = min(classes en passe 1) - 1, applique AUX DEUX passes pour que les deux
# passes soient constituees de la meme facon ; la passe 2 est aussi calculee a son propre
# N (sensibilite).
#
# Usage : Rscript 37-indice_4H.R   (variables : SMOKE=1, BOOT=500, OUTDIR, NCPU)

suppressMessages({library(HybridMicrobiomes); library(phyloseq); library(parallel)})
SMOKE  <- Sys.getenv("SMOKE", "0") == "1"
BOOT   <- as.integer(Sys.getenv("BOOT", if (SMOKE) "3" else "500"))
OUTDIR <- Sys.getenv("OUTDIR", "results/fourH")
NCPU   <- as.integer(Sys.getenv("SLURM_CPUS_PER_TASK", "4"))
DEPTH  <- 3000L   # ensemble commun aux analyses de composition (lectures ASV)
DEPTH4H <- 1000L  # raréfaction 4H, en lectures ASSIGNEES au rang (plan 4H, section Profondeur)
dir.create(OUTDIR, showWarnings = FALSE, recursive = TRUE)
cat(sprintf("HybridMicrobiomes %s | phyloseq %s | BOOT=%d | SMOKE=%s | NCPU=%d\n",
            packageVersion("HybridMicrobiomes"), packageVersion("phyloseq"), BOOT, SMOKE, NCPU))

# ------------------------------------------------------------------ table et ensemble
tabf <- "results/decontam/asv_table_clean.tsv"
hdr <- strsplit(readLines(tabf, n = 1L), "\t")[[1]]; nc <- length(hdr)
dat <- scan(tabf, what = c(list(""), rep(list(0L), nc - 1L)), sep = "\t", skip = 1L, quiet = TRUE)
m <- matrix(0L, nrow = length(dat[[1]]), ncol = nc - 1L, dimnames = list(dat[[1]], hdr[-1]))
for (j in 2:nc) m[, j - 1L] <- dat[[j]]
rm(dat); invisible(gc())

MD <- read.csv("metadata/analysis_metadata.csv", stringsAsFactors = FALSE)
for (cn in c("dada2_id","run_label","tissue","categorie","inclus_passe1")) stopifnot(cn %in% names(MD))
rownames(MD) <- MD$dada2_id
keep <- intersect(colnames(m)[colSums(m) >= DEPTH], MD$dada2_id)
ref  <- intersect(labels(readRDS("results/rarefaction/beta_mean_bray_N400.rds")), MD$dada2_id)  # objet dist : labels(), pas rownames()
stopifnot(length(ref) > 0)
stopifnot(setequal(keep, ref))
cat(sprintf("ensemble : %d echantillons (= lignes beta_mean_bray_N400 x metadonnees)\n", length(keep)))
m <- m[, keep]; m <- m[rowSums(m) > 0, ]

# ------------------------------------------------------------------ agregation taxonomique
tax <- read.delim("results/dada2_final/taxonomy.tsv", stringsAsFactors = FALSE)
stopifnot(all(c("ASV","Family","Genus") %in% names(tax)))
rownames(tax) <- tax$ASV; stopifnot(all(rownames(m) %in% tax$ASV))
agg <- function(rank) {
  lab <- tax[rownames(m), rank]
  ok  <- !is.na(lab) & lab != ""
  # libelle complet pour eviter de fusionner deux genres homonymes de familles differentes
  full <- if (rank == "Genus") paste(tax[rownames(m), "Family"], lab, sep = ";") else lab
  g <- rowsum(m[ok, , drop = FALSE], full[ok])
  list(tab = g, asv_kept = sum(ok), asv_tot = length(ok),
       reads_kept = sum(m[ok, ]), reads_tot = sum(m))
}
AG <- list(genus = agg("Genus"), family = agg("Family"))
cov <- do.call(rbind, lapply(names(AG), function(k) data.frame(rang = k,
         taxons = nrow(AG[[k]]$tab), asv_assignes = AG[[k]]$asv_kept, asv_total = AG[[k]]$asv_tot,
         pct_asv = 100 * AG[[k]]$asv_kept / AG[[k]]$asv_tot,
         pct_lectures = 100 * AG[[k]]$reads_kept / AG[[k]]$reads_tot)))
write.table(cov, file.path(OUTDIR, "couverture_taxonomique.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
print(cov)
# Le package rarefie la table AGREGEE et supprime en silence les echantillons sous `reads`, ce qui
# desaligne class_grouping. On retient donc les echantillons ayant >= DEPTH4H lectures assignees au
# GENRE (la famille en a toujours au moins autant) : meme ensemble pour tous les reglages.
gs <- colSums(AG$genus$tab); stopifnot(all(colSums(AG$family$tab) >= gs))
keep0 <- keep; keep <- keep[gs[keep] >= DEPTH4H]
cat(sprintf("4H : %d / %d echantillons a >= %d lectures assignees au genre\n", length(keep), length(keep0), DEPTH4H))

# ------------------------------------------------------------------ strates
CLS <- c(Cn = 1L, Hy = 2L, Pt = 3L)
strata <- expand.grid(passe = c("1","2"), tissu = c("caudale","branchie","midgut","hindgut"),
                      run = c("durance1","durance2","durance3"), stringsAsFactors = FALSE)
ids_of <- function(passe, tissu, run) {
  md <- MD[keep, ]
  md <- md[md$tissue == tissu & md$run_label == run & md$categorie %in% names(CLS), ]
  if (passe == "1") md <- md[as.character(md$inclus_passe1) %in% c("True","TRUE"), ]
  md$dada2_id
}
eff <- do.call(rbind, lapply(seq_len(nrow(strata)), function(i) {
  s <- strata[i, ]; ids <- ids_of(s$passe, s$tissu, s$run)
  tb <- table(factor(MD[ids, "categorie"], levels = names(CLS)))
  data.frame(s, n_Cn = tb[["Cn"]], n_Hy = tb[["Hy"]], n_Pt = tb[["Pt"]], min_classe = min(tb))
}))
# N commun : celui de la passe 1 de la meme strate tissu x run
eff$N_commun <- NA_integer_
for (i in seq_len(nrow(eff))) {
  j <- which(eff$passe == "1" & eff$tissu == eff$tissu[i] & eff$run == eff$run[i])
  eff$N_commun[i] <- eff$min_classe[j] - 1L
}
eff$N_propre  <- eff$min_classe - 1L
eff$abandonnee <- eff$min_classe < 10 | (eff$min_classe[match(paste("1", eff$tissu, eff$run),
                     paste(eff$passe, eff$tissu, eff$run))] < 10)
write.table(eff, file.path(OUTDIR, "effectifs_strates.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
print(eff)

# ------------------------------------------------------------------ taches
# reglage : fonction, rang, rho, dist, N (commun ou propre)
REG <- data.frame(
  reglage = c("J_genre_0.5","J_genre_0.3","J_genre_0.7","J_famille_0.5","BC_genre_0.5",
              "pre_genre_0.5","nul1_genre_0.5","J_genre_0.5_Npropre"),
  fn   = c("boot","boot","boot","boot","bootA","pre","null","boot"),
  rang = c("genus","genus","genus","family","genus","genus","genus","genus"),
  rho  = c(0.5, 0.3, 0.7, 0.5, 0.5, 0.5, 0.5, 0.5),
  N    = c("commun","commun","commun","commun","commun","commun","commun","propre"),
  stringsAsFactors = FALSE)
tasks <- merge(eff[!eff$abandonnee, ], REG, by = NULL)
tasks <- tasks[!(tasks$N == "propre" & tasks$passe == "1"), ]   # passe 1 : N propre = N commun
if (SMOKE) tasks <- tasks[tasks$passe == "1" & tasks$tissu == "branchie" & tasks$run == "durance1", ]
cat(sprintf("%d taches\n", nrow(tasks)))

mkps <- function(ids, rang) {
  g <- AG[[rang]]$tab[, ids, drop = FALSE]; g <- g[rowSums(g) > 0, , drop = FALSE]
  sd <- data.frame(classe = unname(CLS[MD[ids, "categorie"]]), row.names = ids)
  tt <- matrix(rownames(g), ncol = 1, dimnames = list(rownames(g), "taxon"))   # FourHnull exige une tax_table
  ps <- phyloseq(otu_table(g, taxa_are_rows = TRUE), sample_data(sd), tax_table(tt))
  stopifnot(all(sample_sums(ps) >= DEPTH4H))
  ps
}
run_task <- function(k) {
  t <- tasks[k, ]; ids <- ids_of(t$passe, t$tissu, t$run)
  ps <- mkps(ids, t$rang); cg <- unname(CLS[MD[sample_names(ps), "categorie"]])
  N  <- if (t$N == "commun") t$N_commun else t$N_propre
  ky <- utf8ToInt(paste(t$passe, t$tissu, t$run, t$reglage)); sd <- 20261003L + sum(ky * seq_along(ky))
  set.seed(sd)   # FourHbootstrap/A et FourHpreanalysis n'utilisent pas leur argument seed
  t0 <- Sys.time()
  W <- character(0)
  log <- capture.output(res <- tryCatch(withCallingHandlers(switch(t$fn,
    boot  = FourHbootstrap(ps, cg, t$rho, BOOT, N, reads = DEPTH4H, rarefy_each_step = TRUE, seed = sd, dist = "Jaccard"),
    bootA = FourHbootstrapA(ps, cg, t$rho, BOOT, N, reads = DEPTH4H, rarefy_each_step = TRUE, seed = sd,
                            dist = "Bray-Curtis", representative = "mean", rescale_core = FALSE, use_microViz = "no"),
    pre   = FourHpreanalysis(ps, cg, t$rho, BOOT, N, reads = DEPTH4H, rarefy_each_step = TRUE, seed = sd),
    null  = FourHnull(ps, cg, t$rho, BOOT, N, null_model = 1, reads = DEPTH4H, rarefy_each_step = TRUE,
                      seed = sd, use_microViz = "no")),
    warning = function(w) { W <<- c(W, conditionMessage(w)); invokeRestart("muffleWarning") },
    message = function(mm) { W <<- c(W, paste("MSG:", conditionMessage(mm))); invokeRestart("muffleMessage") }),
    error = function(e) structure(conditionMessage(e), class = "err")), type = "output")
  log <- c(log, W)
  list(t = t, N = N, n_samples = nsamples(ps), n_taxa = ntaxa(ps), res = res, log = log,
       sec = as.numeric(difftime(Sys.time(), t0, units = "secs")))
}
R <- mclapply(seq_len(nrow(tasks)), run_task, mc.cores = min(NCPU, nrow(tasks)), mc.preschedule = FALSE)
saveRDS(R, file.path(OUTDIR, if (SMOKE) "fourH_smoke.rds" else "fourH_brut.rds"))

if (SMOKE) {   # STRUCTURE seulement, aucune valeur d'indice
  for (x in R) {
    r <- x$res
    cat(sprintf("\n[%s] N=%d echant=%d taxons=%d %.1fs class=%s dim=%s\n", x$t$reglage, x$N,
                x$n_samples, x$n_taxa, x$sec, paste(class(r), collapse = "/"),
                paste(dim(r), collapse = "x")))
    if (inherits(r, "err")) cat("   MESSAGE:", r, "\n")
    if (is.list(r) && !is.data.frame(r)) cat("   noms:", paste(names(r), collapse = ","), "\n")
    if (!is.null(colnames(r))) cat("   colonnes:", paste(colnames(r), collapse = ","), "\n")
    cat("   log (lignes):", length(x$log), "|", paste(unique(substr(x$log, 1, 70))[1:min(4, length(unique(x$log)))], collapse = " || "), "\n")
  }
  quit(save = "no")
}

# ------------------------------------------------------------------ mise en forme
B <- list(); C <- list(); NP <- list(); PRE <- list(); ERR <- list()
for (x in R) {
  t <- x$t; r <- x$res; key <- t[, c("passe","tissu","run","reglage")]
  if (inherits(r, "err")) { ERR[[length(ERR)+1]] <- data.frame(key, message = as.character(r)); next }
  if (t$fn %in% c("boot","bootA","null")) {
    d <- as.data.frame(r); d$boot <- seq_len(nrow(d))
    B[[length(B)+1]] <- data.frame(key, N = x$N, d, check.names = FALSE)
    if (t$fn %in% c("boot","bootA")) {
      cen <- as.data.frame(FourHcentroid(r)); C[[length(C)+1]] <- data.frame(key, N = x$N, cen, check.names = FALSE)
    }
    if (t$fn == "boot") {
      grDevices::pdf(NULL); np <- FourHnullplaneD(r); grDevices::dev.off()
      dI <- NULL   # structure de sortie documentee mais non verifiee : recherche recursive de diffI
      fd <- function(o) { if (is.data.frame(o) && "diffI" %in% names(o)) return(o$diffI)
        if (is.list(o)) { if (!is.null(o$diffI)) return(o$diffI); for (e in o) { v <- fd(e); if (!is.null(v)) return(v) } }
        NULL }
      dI <- fd(np); stopifnot(length(dI) == nrow(r))
      NP[[length(NP)+1]] <- data.frame(key, N = x$N, moy_diffI = mean(dI), sd_diffI = sd(dI),
                                       frac_diffI_pos = mean(dI > 0), frac_diffI_neg = mean(dI < 0))
    }
  } else if (t$fn == "pre") {
    d <- as.data.frame(r); stopifnot(all(c("core_fraction_P1","core_fraction_H","core_fraction_P2") %in% names(d)))
    pm <- (mean(d$core_fraction_P1) + mean(d$core_fraction_P2)) / 2
    PRE[[length(PRE)+1]] <- data.frame(key, N = x$N, core_P1 = mean(d$core_fraction_P1), core_H = mean(d$core_fraction_H),
      core_P2 = mean(d$core_fraction_P2), ratio_H_parents = mean(d$core_fraction_H) / pm,
      avertissement_critere_aide = mean(d$core_fraction_H) < 0.5 * pm, lignes_log = length(x$log))
  }
}
wr <- function(L, f) if (length(L)) write.table(do.call(rbind, L), file.path(OUTDIR, f), sep = "\t",
                                                quote = FALSE, row.names = FALSE)
wr(B, "bootstraps.tsv"); wr(C, "centroides.tsv"); wr(NP, "plan_nul.tsv"); wr(PRE, "preanalyse.tsv"); wr(ERR, "erreurs.tsv")
cat(sprintf("OK : %d bootstrap-sets, %d centroides, %d plans nuls, %d preanalyses, %d erreurs\n",
            length(B), length(C), length(NP), length(PRE), length(ERR)))
