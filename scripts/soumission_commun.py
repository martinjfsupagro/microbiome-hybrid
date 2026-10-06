"""soumission_commun.py — fonctions partagées par scripts/72 (article de soumission) et scripts/73 (Additional files),
formatage pour Animal Microbiome (consignes lues le 2026-10-06 : « Prepare your manuscript », article type Research).

- AF : correspondance élément du supplément -> numéro d'Additional file, dans l'ordre de première citation dans
  l'article (hors notes grises) ; table docs/soumission/correspondance_additional_files.tsv ;
- conv(texte) : « Supplementary Table S6 and Figure S1 » -> « Additional files 8 and 9 », « Table S3 » -> « Additional
  file 3 », listes et intervalles compris ; les renvois à un matériel supplémentaire externe (« Table S.4.1 ») ne sont
  pas touchés (ils n'existent que dans des notes grises) ;
- est_note(run) : run d'une note éditoriale (couleur 888888) ;
- italiques : noms d'espèces hôtes et de taxons microbiens (consigne de la revue : tous les rangs en italique).
"""
import re, copy
from docx.text.run import Run

ORDER = ["T1", "T2", "T3", "N1", "T4", "N2", "T5", "T6", "F1", "T7", "N3", "T8", "F2", "F3", "T9", "F4", "T10", "F5"]
AF = {lab: i + 1 for i, lab in enumerate(ORDER)}
KIND = {"Table": "T", "Figure": "F", "Note": "N"}
FMT = {"T": "xlsx", "N": "docx", "F": "pdf"}

_ITEM = r"(?:(?:Table|Figure|Note)s?\s+)?S\d+(?:\s*[–-]\s*S?\d+)?"
PAT = re.compile(r"(?:Supplementary\s+)?(?:Table|Figure|Note)s?\s+S\d+(?:\s*[–-]\s*S?\d+)?(?:(?:\s*,\s*|\s+and\s+)" + _ITEM + r")*")


def _labels(span):
    labs, kind = [], None
    for m in re.finditer(r"(?:(Table|Figure|Note)s?\s+)?S(\d+)(?:\s*[–-]\s*S?(\d+))?", span):
        if m.group(1): kind = KIND[m.group(1)]
        a = int(m.group(2)); b = int(m.group(3)) if m.group(3) else a
        labs += [f"{kind}{k}" for k in range(a, b + 1)]
    return labs


def _fmt(nums):
    nums = sorted(set(nums))
    if len(nums) == 1: return f"Additional file {nums[0]}"
    return "Additional files " + ", ".join(map(str, nums[:-1])) + f" and {nums[-1]}"


def conv(text):
    def rep(m):
        labs = _labels(m.group(0))
        assert all(l in AF for l in labs), (m.group(0), labs)
        return _fmt([AF[l] for l in labs])
    return PAT.sub(rep, text)


def residuel(text):
    """Renvois S restants (hors matériel externe du type « S.4.1 »)."""
    return re.findall(r"(?:Table|Figure|Note)s?\s+S\d+(?!\.\d)", text)


def couleur(r):
    try:
        return str(r.font.color.rgb) if r.font.color is not None and r.font.color.type is not None else None
    except Exception:
        return None


def est_note(r):
    return couleur(r) == "888888"


ESPECES = ["Parachondrostoma toxostoma", "Chondrostoma nasus", "P. toxostoma", "C. nasus"]
TAXONS = ["Pseudomonadota", "Fusobacteriota", "Bacteroidota", "Bacillota", "Verrucomicrobiota", "Thermodesulfobacteriota",
          "Deinococcota", "Chlamydiota", "Planctomycetota", "Actinomycetota", "Spirochaetota", "Cyanobacteriota",
          "Proteobacteria", "Firmicutes", "Bacteroidetes", "Fusobacteria", "Actinobacteria", "Cyanobacteria", "Tenericutes",
          "Mollicutes", "Mycoplasmatales", "Deltaproteobacteria", "Desulfuromonadia", "Desulfovibrionia", "Desulfobulbia"]
ITAL = re.compile(r"\b(" + "|".join(re.escape(x) for x in ESPECES + TAXONS) + r")\b")


def segments_italiques(text):
    """Découpe un texte en (morceau, italique) : espèces et taxons en italique."""
    out, pos = [], 0
    for m in ITAL.finditer(text):
        if m.start() > pos: out.append((text[pos:m.start()], False))
        out.append((m.group(0), True)); pos = m.end()
    if pos < len(text): out.append((text[pos:], False))
    return out


def italiciser_run(par, run):
    """Remplace un run romain contenant des noms à italiser par une suite de runs ; les runs déjà italiques sont laissés."""
    if run.italic or not ITAL.search(run.text): return
    segs = segments_italiques(run.text)
    run.text = segs[0][0]; run.italic = True if segs[0][1] else run.italic
    prev = run._r
    for t, it in segs[1:]:
        el = copy.deepcopy(run._r); prev.addnext(el); prev = el
        r = Run(el, par); r.text = t; r.italic = True if it else None


TERMES = [("DNA extraction, 16S library preparation and sequencing", "DNA extraction, 16S rRNA gene library preparation and sequencing"),
          ("The 16S V4 primers co-amplify", "The 16S rRNA gene V4 primers co-amplify"),
          ("no measurable effect on 16S community composition", "no measurable effect on 16S rRNA gene-based community composition"),
          ("no measurable effect on 16S composition", "no measurable effect on 16S rRNA gene-based composition"),
          ("composition of the 16S microbiota", "composition of the bacterial microbiota (16S rRNA gene)"),
          # Note S2 (Additional file 6)
          ("The 16S V4 primers, being", "The 16S rRNA gene V4 primers, being"),
          ("eight bacterial 16S sequences", "eight bacterial 16S rRNA gene sequences"),
          ("multiple non-identical 16S operons", "multiple non-identical 16S rRNA gene copies"),
          ("the 16S sequences of the two reference sets", "the 16S rRNA gene sequences of the two reference sets"),
          ("whose full-length 16S differ", "whose full-length 16S rRNA gene sequences differ"),
          # intitulé de section de la revue (« Methods ») ; la version de travail renvoie à « Materials and Methods »
          ("Materials and Methods", "Methods")]


# Historique du brouillon (« an earlier version of this table/note… ») retiré des copies de soumission seulement
# (décision de JF, 2026-10-06) ; la version de travail le conserve. L'historique public des corrections ENA reste.
HISTORIQUE = [
    ("Correction (2026-08-31). An earlier version of this table reported coordinates that were extrapolated from commune "
     "names rather than field records. Georeferences, river names and collection dates are now those supplied by the field "
     "team: five river names were wrong (Suran, Beaume, Buech and a canal were reported as Ain, Ardèche and Durance) and six "
     "positions were displaced by more than 5 km, up to 41.4 km.",
     "Georeferences, river names and collection dates are those supplied by the field team."),
    (" An earlier version of this note gave 181: one fish had been split into two records by a mistyped year prefix in a "
     "sample name, which the per-year count double-counted and the collapsed count did not.", ""),
    ("; the paragraphs are those of an earlier, longer version of the Methods, moved here unchanged except for "
     "cross-references.", "."),
    ("They replace an earlier witness on single-category site codes, which rested on individuals unresolved by morphology: "
     "under genotyping, no site code carries a single category.",
     "Single-category site codes cannot serve as such a witness: under genotyping, no site code carries a single category."),
    ("; this version replaces an earlier, uncorrected table.", "."),
]
HIST_COMPTE = {a: 0 for a, _ in HISTORIQUE}


def historique(text):
    for a, b in HISTORIQUE:
        if a in text: HIST_COMPTE[a] += text.count(a); text = text.replace(a, b)
    return text


def terminologie(text):
    """« 16S » seul -> « 16S rRNA gene » (terminologie demandée par Animal Microbiome, d'après Marchesi et al.) ;
    retrait de l'historique du brouillon (HISTORIQUE)."""
    text = historique(text)
    for a, b in TERMES: text = text.replace(a, b)
    return text


def historique_paragraphe(par):
    """HISTORIQUE appliqué à un paragraphe docx : les runs couvrant le passage sont fusionnés (même mise en forme)."""
    for a, b in HISTORIQUE:
        while a in par.text:
            i = par.text.index(a); j = i + len(a); pos = 0; span = []
            for r in par.runs:
                x, y = pos, pos + len(r.text); pos = y
                if y > i and x < j: span.append((r, x))
            assert len({(bool(r.italic), bool(r.bold)) for r, _ in span}) == 1, ("mise en forme mixte", a[:40])
            r0, x0 = span[0]; full = "".join(r.text for r, _ in span)
            r0.text = full.replace(a, b, 1)
            for r, _ in span[1:]: r._r.getparent().remove(r._r)
            HIST_COMPTE[a] += 1


def seize_s_isole(text):
    return re.findall(r".{0,30}16S(?! rRNA)(?!_).{0,20}", text)  # hors identifiants DURANCE16S_…


def conv_paragraphe(par):
    """Conversion des appels, y compris ceux répartis sur plusieurs runs : pour chaque appel (dans le texte du
    paragraphe), les runs qu'il couvre sont d'abord fusionnés dans le premier (même mise en forme italique/gras exigée),
    puis l'appel entier est converti — « Table S8 and Figure S2 » donne « Additional files 12 and 13 »."""
    guard = 0
    while True:
        txt = par.text; m = next((x for x in PAT.finditer(txt) if residuel(x.group(0))), None)
        if not m: return
        guard += 1; assert guard < 100, txt[:80]
        pos = 0; span = []
        for r in par.runs:
            a, b = pos, pos + len(r.text); pos = b
            if b > m.start() and a < m.end(): span.append(r)
        if len(span) > 1:
            assert len({(bool(r.italic), bool(r.bold)) for r in span}) == 1, ("mise en forme mixte", m.group(0))
            span[0].text = "".join(r.text for r in span)
            for r in span[1:]: r._r.getparent().remove(r._r)
        span[0].text = conv(span[0].text)


def elements_supplement(S):
    """Découpage du supplément de travail : [(k0, k1, élément, titre)] sur la liste des enfants du corps ; tables et notes
    commencent à leur titre (style Heading « Table Sn. » / « Note Sn. »), figures au paragraphe d'image suivi de la légende
    « Figure Sn. » (titre None)."""
    from docx.text.paragraph import Paragraph
    body = list(S.element.body.iterchildren()); starts = []
    for k, el in enumerate(body):
        if not el.tag.endswith("}p"): continue
        p = Paragraph(el, S); t = p.text
        m = re.match(r"(Table|Note) S(\d+)\. ", t) if p.style.name.startswith("Heading") else None
        if m: starts.append((k, m.group(1)[0] + m.group(2), t.split(". ", 1)[1]))
        elif el.xpath(".//w:drawing"):
            f = re.match(r"Figure S(\d+)\. ", Paragraph(body[k + 1], S).text); starts.append((k, "F" + f.group(1), None))
    starts.sort()
    out = [(k0, starts[j + 1][0] if j + 1 < len(starts) else len(body), lab, tit) for j, (k0, lab, tit) in enumerate(starts)]
    assert sorted(o[2] for o in out) == sorted(ORDER), [o[2] for o in out]
    return body, out


# Additional file 10 : le fichier livré contient les 2 304 runs (et non un extrait) ; noms de colonnes du fichier ENA.
T7_REMPL = [("The complete table of 2,304 runs is provided as a separate tab-separated file (ENA_accessions_durance.tsv) "
             "because of its size.", "This file gives the complete table of 2,304 runs."),
            ("The excerpt below shows the three runs of one sample; column names are those of the file.",
             "Column names are those of the tab-separated file prepared for the ENA submission, with the sample accession "
             "(sample_accession) added from the ENA receipt; collection year is that of the current ENA record.")]


def texte_T7(t):
    for a, b in T7_REMPL: t = t.replace(a, b)
    return t
