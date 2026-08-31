#!/bin/bash
# Correction des metadonnees du depot ENA PRJEB124417 (action MODIFY).
#
#   bash 4_corriger_metadonnees.sh test    # validation en deux temps, rien n'est publie
#   bash 4_corriger_metadonnees.sh prod    # POUR DE VRAI
#
# Ne touche NI aux fichiers FASTQ, NI aux objets EXPERIMENT/RUN.
#
# CE QUE LE SERVEUR DE TEST PEUT, ET NE PEUT PAS, VALIDER  (etabli le 2026-08-31)
# wwwdev partage le registre d'alias du compte soumettant avec la production,
# mais pas les enregistrements BioSamples. Pour NOS alias, donc :
#   - un ADD    est refuse : "already exists ... with accession ERS311680xx"
#                            (accession de PRODUCTION renvoyee par wwwdev)
#   - un MODIFY est refuse : "No new BioSample was created" (BioSamples de dev
#                            ne connait pas ces objets)
# Aucune des deux voies ne valide quoi que ce soit sur les alias reels.
#
# Le mode test cree donc des objets JETABLES sous des alias suffixes, qui
# n'entrent en collision avec rien. Cela valide ce qui est validable : les
# VALEURS corrigees contre le checklist ERC000013, nom d'hote hybride compris.
# La mecanique du MODIFY, elle, n'est pas testable sur wwwdev — en production
# elle est couverte par la comparaison des accessions du recu.

set -uo pipefail
MODE="${1:-}"
D=/home/martinj/work/projects/microbiome-hybrid/ena_deposit
cd "$D" || exit 1

case "$MODE" in
  test) URL=https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit/ ;;
  prod) URL=https://www.ebi.ac.uk/ena/submit/drop-box/submit/ ;;
  *) echo "Usage : bash $0 test|prod"; exit 1 ;;
esac

demander_identifiants() {
  U=""; P=""
  while [ -z "$U" ]; do printf "Identifiant Webin : " > /dev/tty; IFS= read -r U < /dev/tty; U="${U//[[:space:]]/}"; done
  while [ -z "$P" ]; do printf "Mot de passe Webin : " > /dev/tty; IFS= read -rs P < /dev/tty; echo > /dev/tty; done
}

# --- analyse d'un recu : erreurs, et comparaison des accessions a une reference
analyser() {  # $1 = recu   $2 = fichier de reference des accessions (ou "-")
python3 - "$1" "$2" <<'PY'
import sys, os, collections, re
import xml.etree.ElementTree as ET
recu, ref = sys.argv[1], sys.argv[2]
r = ET.parse(recu).getroot()
ok = r.get("success")
print(f"  success = {ok}")
errs = [e.text for e in r.iter("ERROR")]
if errs:
    def famille(e):
        e = re.sub(r"DURANCE16S_\S+", "<alias>", e or "")
        e = re.sub(r"ERS\d+", "<ERS>", e)
        return e
    fam = collections.Counter(famille(e) for e in errs)
    print(f"  {len(errs)} erreur(s), par famille :")
    for k, v in fam.most_common(8):
        print(f"    {v:5d}  {k[:160]}")
    structurel = sum(v for k, v in fam.items()
                     if "already exists" in k or "No new BioSample" in k)
    if structurel:
        print(f"\n  NOTE : {structurel} erreur(s) portent sur l'EXISTENCE des objets")
        print( "  (alias deja pris, ou BioSamples absent), PAS sur le contenu des")
        print( "  metadonnees. Elles ne disent rien de la validite des valeurs.")
    if len(errs) - structurel:
        print(f"\n  {len(errs)-structurel} erreur(s) portent sur le CONTENU — a examiner.")
sam = [(s.get("alias"), s.get("accession")) for s in r.iter("SAMPLE")]
print(f"  echantillons dans le recu : {len(sam)}")
if ok != "true":
    sys.exit(1)
if ref != "-" and os.path.exists(ref):
    old = {}
    for line in open(ref):
        a, acc = line.rstrip("\n").split("\t")[:2]
        old[a] = acc
    diff = [(a, old[a], acc) for a, acc in sam if a in old and acc and acc != old[a]]
    inconnus = [a for a, _ in sam if a not in old]
    print(f"  accessions identiques a la reference : {len(sam)-len(diff)}/{len(sam)}")
    if diff:
        print(f"  ALERTE : {len(diff)} accession(s) DIFFERENTE(S) — un ADD a eu lieu au lieu")
        print( "  d'un MODIFY. NE PAS RELANCER. Contacter datasubs@ebi.ac.uk.")
        for a, o, n in diff[:5]: print(f"     {a}: {o} -> {n}")
        sys.exit(2)
    if inconnus:
        print(f"  ALERTE : {len(inconnus)} alias absent(s) de la reference"); sys.exit(2)
    print("  -> aucune nouvelle accession : c'est bien une modification.")
# journaliser les accessions du recu
out = recu.replace(".xml", "_accessions.tsv")
with open(out, "w") as f:
    for a, acc in sam: f.write(f"{a}\t{acc}\n")
print(f"  accessions ecrites : {os.path.basename(out)}")
PY
}

envoyer() {  # $1 = submission.xml  $2 = sample.xml  $3 = etiquette
  # Renvoie 0 et positionne RECU si et seulement si un recu EXPLOITABLE est
  # revenu. Un recu vide (deja observe en production le 2026-08-31) laisse
  # l'etat du depot INDETERMINE : on ne conclut rien, on le dit.
  local R essai code rc
  for essai in 1 2 3; do
    R=$D/receipt_${3}_$(date +%Y%m%d_%H%M%S).xml
    echo "  envoi ($(du -h "$2" | cut -f1), tentative $essai/3)..."
    code=$(curl -sS --connect-timeout 30 --max-time 1800 --retry 2 --retry-delay 15                 -u "$U:$P" -F "SUBMISSION=@$1" -F "SAMPLE=@$2"                 -w '%{http_code}' -o "$R" "$URL")
    rc=$?
    local taille; taille=$(wc -c < "$R" 2>/dev/null || echo 0)
    echo "  HTTP $code (curl rc=$rc, $taille octets) -> $(basename "$R")"
    if [ "$rc" -eq 0 ] && [ "$code" = "200" ] && [ "$taille" -gt 0 ]        && head -c 200 "$R" | grep -q "RECEIPT"; then
      RECU="$R"; return 0
    fi
    echo "  reponse inexploitable."
    [ "$essai" -lt 3 ] && { echo "  nouvelle tentative dans 30 s..."; sleep 30; }
  done
  RECU=""
  echo
  echo "  ECHEC DE TRANSPORT apres 3 tentatives : aucun recu exploitable."
  echo "  L'etat du depot est INDETERMINE — la soumission a pu aboutir cote ENA"
  echo "  sans que la reponse nous parvienne. NE PAS relancer a l'aveugle."
  echo "  Determiner l'etat reel avant toute action :"
  echo "      bash 6_etat_du_depot.sh"
  return 1
}

# =====================================================================
if [ "$MODE" = "test" ]; then
  SFX="_VAL$(date +%H%M%S)"
  echo "=== Validation des VALEURS sur le serveur de TEST ==="
  echo "  Les echantillons sont soumis sous des alias suffixes ($SFX), afin de"
  echo "  ne pas entrer en collision avec les alias reels du compte. Les objets"
  echo "  crees sont jetables et detruits sous 24 h."
  echo
  echo "  Ce test valide : checklist ERC000013, regex des coordonnees et des dates,"
  echo "  acceptation du nom d'hote hybride."
  echo "  Il ne valide PAS la mecanique du MODIFY (non testable sur wwwdev)."
  echo
  demander_identifiants
  echo

  python3 build_ena_modify.py --deposited ena_submission/sample.xml \
      --corrections ena_corrections.tsv \
      --receipt "$(ls -t receipt_prod_*.xml | head -1)" \
      --outdir ena_update_test --strip-accession --action ADD \
      --alias-suffix "$SFX" || exit 1

  if ! envoyer ena_update_test/submission.xml ena_update_test/sample.xml "valeurs_test"; then
    unset P; exit 1
  fi
  analyser "$RECU" "-"; RC=$?
  unset P
  echo
  if [ $RC -eq 0 ]; then
    echo "VALEURS VALIDEES par l'ENA : le checklist accepte les coordonnees, les"
    echo "dates (intervalle de Pertuis compris) et le nom d'hote hybride."
    echo
    echo "La mecanique du MODIFY n'etant pas testable ici, la production reste"
    echo "protegee par le controle des accessions du recu : si une seule accession"
    echo "differe, le script s'arrete sans relancer."
    echo
    echo "    bash $0 prod"
  else
    echo "Des VALEURS sont refusees — voir les erreurs ci-dessus."
    echo "Les erreurs 'already exists' seraient un probleme d'alias, pas de donnees ;"
    echo "toute autre erreur porte sur le contenu et doit m'etre transmise."
  fi
  exit $RC
fi

# =====================================================================
XML=$D/ena_update
for f in submission.xml sample.xml; do
  [ -f "$XML/$f" ] || { echo "ERREUR : $XML/$f introuvable (lancer build_ena_modify.py)"; exit 1; }
done
grep -q '<MODIFY/>' "$XML/submission.xml" || { echo "ERREUR : submission.xml ne porte pas <MODIFY/>"; exit 1; }
NS=$(grep -c '<SAMPLE ' "$XML/sample.xml"); NA=$(grep -c 'accession="ERS' "$XML/sample.xml")

echo "=== Correction des metadonnees (PRODUCTION) ==="
echo "  echantillons : $NS   (dont $NA cibles par accession)"
echo "  action       : MODIFY (remplace l'objet, ne fusionne pas)"
echo "  cible        : $URL"
echo
echo "ATTENTION : modification REELLE des metadonnees de PRJEB124417."
printf "Taper OUI pour confirmer : "; read -r C
[ "$C" = "OUI" ] || { echo "annule."; exit 1; }
echo
demander_identifiants
echo

# reference = accessions du depot de production
REF=$D/.accessions_prod.tsv
python3 - "$(ls -t "$D"/receipt_prod_*.xml | head -1)" "$REF" <<'PY'
import sys, xml.etree.ElementTree as ET
r = ET.parse(sys.argv[1]).getroot()
with open(sys.argv[2], "w") as f:
    for s in r.iter("SAMPLE"): f.write(f"{s.get('alias')}\t{s.get('accession')}\n")
PY

if ! envoyer "$XML/submission.xml" "$XML/sample.xml" "modify_prod"; then
  unset P; exit 3
fi
analyser "$RECU" "$REF"; RC=$?
unset P
echo
[ $RC -eq 0 ] && { echo "CORRECTION APPLIQUEE. Verifiez dans quelques heures :"; echo "  bash 5_verifier_correction.sh"; }
exit $RC
