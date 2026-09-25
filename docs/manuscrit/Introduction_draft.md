# Introduction — draft 1

Projet microbiome-hybrid. Architecture retenue : question hybride en tête, compartiment
tissulaire comme axe de test. Citations en style auteur-date, comme les Methods de
`Article.docx` ; la conversion en style numéroté BMC se fera à la mise en forme.
Clés disponibles dans `docs/biblio/references.bib` et `docs/biblio/microbiome_hybrid_all_refs.bib`.

---

Animals and the microbial communities they harbour form composite biological units in which
microbial composition contributes to host performance and to tolerance of environmental
constraints (Bordenstein and Theis 2015). These associations are established largely by the
sorting of microbial pools from the surrounding environment, a sorting that reflects host ecology
and physiology — feeding behaviour, which selects among available resources, and the immune
pathways underlying tolerance of or resistance to microbes (Shapira 2016; Shropshire and
Bordenstein 2016; Adair and Douglas 2017). Environmental acquisition is particularly important in
fish, which live in a medium favourable to bacterial growth, are continuously exposed to microbes
at their epithelial barriers, and are mostly oviparous with limited maternal effects compared with
mammals (Llewellyn et al. 2014); accordingly, surveys of wild populations report a predominant
environmental component of variation in bacterial composition (Sevellec et al. 2014; Smith et al.
2015; Chiarello et al. 2018). Host genotype is nonetheless not without effect. A fourteen-year
follow-up of wild baboons found microbiome phenotypes to be almost universally heritable, but with
a typically low heritability that depends on context, and its authors concluded that large sample
sizes are required to quantify it (Grieneisen et al. 2021); in stickleback, a host genetic
influence on the gut microbiome became measurable once biological and technical components of
variance had been decomposed beforehand (Small et al. 2019). If host ancestry shapes the fish
microbiota, the expected effect is therefore small relative to the environmental one, and
detecting it requires both substantial sample sizes and explicit control of the spatial and
technical axes along which it could be mimicked.

Secondary contact zones make host ancestry a naturally occurring and naturally replicated
variable, and they are where the question of a genomic contribution to microbiota assembly is
posed most directly. Introgressive hybridisation may disrupt co-adapted gene complexes and thereby
alter close host–microbe interactions (Wang et al. 2015); conversely, hybridisation is a source of
genomic diversity and adaptive novelty involved in speciation and in range expansion into enlarged
ecological niches (Pfennig et al. 2016; Schumer et al. 2018), and this diversity may extend to the
microbiota through the acquisition of new microbial taxa. Three outcomes are usually contrasted:
an intermediate or additive microbiota, varying monotonically with ancestry; dominance, in which
hybrids resemble one parental species; and a transgressive microbiota, lying outside the range of
both parents. Camper et al. (2024) gave this comparison an explicit framework for host-associated
microbiomes, in which four idealised models of taxon membership — Union, Intersection, Gain and
Loss — are never realised in pure form, so that the index measures the relative weight of each and
the four weights sum to one. The Gain–Loss axis of that framework provides an operational
definition of a transgressive microbiota, one that does not presuppose a cost to the host. The
distinction matters, because the equation between transgression and dysbiosis has been challenged:
on an ecologically successful hybrid lizard, Camper et al. (2025) report widespread transgressive
segregation correlated with a restructuring of niche, and argue that the negative conclusions of
the literature rest disproportionately on hybrids of low adaptive value. We follow the framework's
own statement of scope, that the index describes a pattern and not a process, in the same sense as
a beta-diversity measure.

What is known of hybrid microbiota in fish comes almost entirely from controlled crosses.
Reciprocal hybrids of bream and culter, whose parents have contrasting feeding habits, show a
strong correspondence between genotype and intestinal characteristics (Li et al. 2018); in
intrageneric *Takifugu* hybrids, host hybridisation outweighs cohabitation in shaping the gut
microbiota (Jin et al. 2023); reciprocal hybrids of koi and goldfish resemble one parent rather
than the midpoint of the two (Wang et al. 2022); and whitefish species pairs with their reciprocal
hybrids have been compared in natural and controlled environments (Sevellec et al. 2019). This
body of work has been reviewed recently (Cui et al. 2022). Studies of natural hybrid zones in
other vertebrates, for their part, do not converge. Host ancestry predominates in *Neotoma*
woodrats, where habitat determines diet but genotype determines the gut microbiota (Nielsen et al.
2022), and in hybridising brown lemurs along a 180 km transect (Donohue et al. 2025). The opposite
conclusion is reached in baboons spanning a hybrid zone, where site soil properties rather than
genetic ancestry, relatedness or between-population genetic distance explain the gut microbiota
(Grieneisen et al. 2019), and in wild house mice, where an apparent effect of admixture becomes
weak once spatial autocorrelation is taken into account, on two replicates of the same hybrid zone
(Čížková et al. 2023). In hybridising chickadees moved to a common environment, the change of
environment affected microbiota richness but not community composition, while a corresponding
effect of ancestry on composition was not statistically supported (Russell et al. 2026) — a result
that argues for reporting alpha and beta diversity separately rather than for a directed
expectation on either. Across this literature, no study combines a natural hybrid zone in fish,
host ancestry quantified by genotyping rather than assigned by cross class, and several tissue
compartments characterised in the same individual.

The nase *Chondrostoma nasus* and the South-west European nase, or toxostome, *Parachondrostoma
toxostoma* offer that combination. The toxostome is endemic to southern France, where it is
declining and is a species of conservation concern; the nase originates from central Europe and
entered the Rhône basin following the construction of navigable connections across Europe during
the last century (Gilles 1998), so that the two distributions have partially overlapped for about
a hundred years. Hybridisation has been detected in the patchily distributed sympatric areas of
the basin, with an incidence unrelated to habitat characteristics (Costedoat et al. 2005; Sinama
et al. 2013; Guivier et al. 2019) — the configuration of a mosaic hybrid zone (Seehausen et al.
2008). Guivier et al. (2017) characterised the microbiota of four tissue compartments of the two
species in strict parapatry on a single river, and found the tissue compartment to be the first
factor of variation, with a marked contrast between externally and internally exposed tissues and
with proportions of species-specific taxa that were asymmetric between compartments: the nase
carried many specific taxa on its external tissues, the toxostome in its intestine. On that basis
the authors proposed that introgressive hybridisation might affect the microbiota differently
depending on the tissue considered, and closed by announcing the exploration of hybrid microbiota
rearrangement, which their sample of sixteen fish at two stations could not support. The present
study is that exploration, on 180 fish sampled at nine stations over six watercourses of the Rhône
drainage in two years, with host ancestry resolved by genotyping across 25 chromosomes rather than
by morphology, and with the same four compartments — caudal fin, gill, midgut and hindgut —
characterised in each individual.

We ask whether the microbiota of individuals of mixed ancestry is intermediate between the two
parental species, dominated by one of them, or displaced outside their range, and whether the
answer is the same in all four compartments. Three points of design are stated at the outset
rather than introduced with the results. First, because genotyping across 25 chromosomes separates
an intermediate genome from a near-parental genome introgressed on a single chromosome, what counts
as a hybrid is a decision and not a given: the contrast is therefore run twice, on intermediate
genomes alone and on the wider set including introgressed near-parental individuals, with both
passes declared in advance, and the displacement of the result between them measures the
contribution of the introgressed individuals. Second, the comparison is reported both as a
category contrast in a model spanning all stations — the only admissible form given the low
heritability expected from Grieneisen et al. (2021) — and, as a complementary characterisation, as
the four-dimensional index of Camper et al. (2024), whose core threshold and taxonomic rank are
fixed a priori and whose sensitivity is reported, since on a natural hybrid system these choices
move the index more than sample size or sequencing depth do. Third, genotypic category is
entangled with the spatial axis in this design, station being by far the strongest correlate of
composition, and field processing order propagated to plate position; results on category are
consequently reported bracketed between the two sequential orderings rather than as a single
decomposition, adjusted for plate position, and read as patterns co-varying with station and with
category rather than as effects of ancestry alone. Two stations of the same river, 25 km apart and
separated by a weir passable only downstream, were sampled in two successive years and provide an
internal reference in which the two species are in contact geographically without detected
hybridisation. Following Guivier et al. (2017), we expect any hybrid signal to be most pronounced
in the digestive compartments, where the two parental species diverge most, rather than uniformly
across the four tissues.

---

## Notes de rédaction

1. **Longueur** : 5 paragraphes, 1472 mots (264 / 276 / 307 / 281 / 344). C'est long pour une introduction ; je peux
   ramener l'ensemble autour de 1 100 mots en resserrant les §3 et §5 si vous préférez. Les paragraphes 1 et 5 sont les plus longs ; à la
   mise en forme, le §5 peut être scindé en « objectifs » / « précautions de plan » si la revue
   préfère un paragraphe d'hypothèses court.
2. **Le quatrième compartiment n'est pas présenté comme une nouveauté** — Guivier et al. (2017)
   séparait déjà midgut et hindgut. La nouveauté portée par le texte est la zone d'hybridation
   naturelle chez le poisson, l'ascendance génotypée, l'effectif et le témoin parapatrique.
3. **« Transgressif » est défini à sa première occurrence** par l'axe Gain–Loss, et explicitement
   dissocié d'un coût de fitness, conformément à Camper et al. (2025).
4. **La dichotomie branchie = immunité / intestin = régime n'est pas reprise** : le reproche
   adressé à l'introduction du manuscrit d'origine portait exactement là. Le gradient tissulaire
   est décrit par le degré d'exposition au milieu, sans attribution fonctionnelle tranchée.
5. **Le témoin parapatrique est décrit comme une seule barrière sur un seul cours d'eau**,
   échantillonnée deux années de suite. La formule « réplicable sur deux rivières » de
   `recommandations_consolidees.md` §5 est antérieure aux réponses du 30 août et se trouve
   contredite par `decision_stations.md` §6 : le jeu ne contient qu'un obstacle documenté, le
   seuil de 2,5 m du Suran, et les autres sites ne portent qu'une station chacun.
6. **Aucun résultat n'est chiffré**, ce qui est cohérent avec D7 ouverte (métrique non tranchée)
   et avec le recalcul nécessaire des §8.8 et 8.9 sur la classification à 25 chromosomes.
7. **Références à corriger dans le .bib avant soumission** : `Small et al.` est daté 2018 dans
   `microbiome_hybrid_all_refs.bib`, Crossref donne **2019** pour
   `10.1128/msystems.00331-19` ; et le corégone est présent comme préprint
   (`10.1101/312231`) alors qu'une version publiée existe — Sevellec et al. **2019**,
   *Ecology and Evolution*, `10.1002/ece3.5676`. Le texte ci-dessus cite la version publiée.
8. **Deux citations restent à vérifier dans l'usage** : `Wang et al. 2015` et `Sevellec et al.
   2014` proviennent de la liste du manuscrit d'origine (clés `Wang2015`, `Sevellec2014` de
   `references.bib`) ; leur pertinence exacte à l'endroit où elles sont placées mérite une
   relecture, je ne les ai pas lues en texte intégral.
