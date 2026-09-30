#!/bin/bash
# Verification EXHAUSTIVE du depot PRJEB124417, sur l'etat attendu CUMULE.
#
#   bash 7_verifier_exhaustif.sh                       # tables appliquees par defaut
#   bash 7_verifier_exhaustif.sh t1.tsv t2.tsv ...     # liste explicite, DANS L'ORDRE
#
# POURQUOI CUMULE (lecon du 2026-09-30)
# La v1 comparait le depot a la seule table d'aout. Apres la campagne du 25/09 sur
# l'identite d'hote, elle signalait 59 "non conformes" qui etaient en realite les
# valeurs de septembre, correctement appliquees. Le depot etait juste, le verificateur
# perime. Il faut donc chainer TOUTES les tables soumises, dans l'ordre chronologique.
#
# REGLE : ne lister ici que les tables EFFECTIVEMENT SOUMISES. Une table preparee mais
# non soumise (dates de Pertuis, host subject id) ferait apparaitre de faux ecarts.
#
# Lecture seule : n'ecrit que son rapport.

set -uo pipefail
D=/home/martinj/work/projects/microbiome-hybrid/ena_deposit
cd "$D" || exit 1

if [ "$#" -gt 0 ]; then
  TABLES=("$@")
else
  TABLES=(ena_corrections.tsv ena_corrections_hote_sept.tsv)   # soumises : 31/08 puis 25/09
fi
for t in "${TABLES[@]}"; do
  [ -f "$t" ] || { echo "ERREUR : table introuvable : $t"; exit 1; }
done
echo "tables chainees (dans cet ordre) :"
for t in "${TABLES[@]}"; do echo "  - $t  ($(( $(wc -l < "$t") - 1 )) lignes)"; done
echo

U=""; P=""
while [ -z "$U" ]; do printf "Identifiant Webin : " > /dev/tty; IFS= read -r U < /dev/tty; U="${U//[[:space:]]/}"; done
while [ -z "$P" ]; do printf "Mot de passe Webin : " > /dev/tty; IFS= read -rs P < /dev/tty; echo > /dev/tty; done
echo

# --- etat attendu, par chainage des tables
ATT=$(mktemp); CHAIN=$(mktemp)
python3 - "$ATT" "$CHAIN" "${TABLES[@]}" <<'PY'
import sys, csv
att_out, chain_out, tables = sys.argv[1], sys.argv[2], sys.argv[3:]
attendu = {}            # (accession, champ) -> valeur attendue
origine = {}            # (accession, champ) -> valeur initiale du depot
ruptures = []
for t in tables:
    for r in csv.DictReader(open(t, newline="", encoding="utf-8"), delimiter="\t"):
        k = (r["accession"], r["champ"])
        if k not in attendu:
            origine[k] = r["valeur_deposee"]
        elif r["valeur_deposee"] != attendu[k]:
            # la table suppose un etat de depart different de celui que le chainage predit
            ruptures.append((t, k[0], k[1], attendu[k], r["valeur_deposee"]))
        attendu[k] = r["valeur_corrigee"]
with open(att_out, "w", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    for (acc, champ), v in attendu.items():
        w.writerow([acc, champ, v, origine[(acc, champ)]])
with open(chain_out, "w", newline="") as f:
    csv.writer(f, delimiter="\t").writerows(ruptures)
print(f"etat attendu : {len(attendu)} champs sur {len({a for a,_ in attendu})} echantillons")
print(f"ruptures de chainage : {len(ruptures)}")
PY
if [ -s "$CHAIN" ]; then
  echo
  echo "ATTENTION : des tables ne s'enchainent pas (une table part d'un etat que la"
  echo "precedente ne produit pas). Ordre errone, ou table manquante :"
  head -5 "$CHAIN" | while IFS=$'\t' read -r t a c pred dep; do
    echo "   $t | $a | $c : chainage predit $pred, la table part de $dep"
  done
fi
echo

mapfile -t ACCS < <(cut -f1 "$ATT" | sort -u)
echo "echantillons a interroger : ${#ACCS[@]}"
TD=$(mktemp -d); trap 'rm -rf "$TD" "$ATT" "$CHAIN"' EXIT
LOT=100; i=0; n=0
while [ $i -lt ${#ACCS[@]} ]; do
  IDS=$(printf "%s," "${ACCS[@]:$i:$LOT}" | sed 's/,$//'); n=$((n+1))
  code=$(curl -sS --connect-timeout 30 --max-time 300 --retry 2 -u "$U:$P" \
          -w '%{http_code}' -o "$TD/lot_$n.xml" \
          "https://www.ebi.ac.uk/ena/submit/report/samples/xml/$IDS")
  rc=$?
  if [ "$rc" -ne 0 ] || [ "$code" != "200" ] || [ ! -s "$TD/lot_$n.xml" ]; then
    echo "  lot $n : ECHEC (HTTP $code, rc=$rc) — verification incomplete"; unset P; exit 1
  fi
  printf "  lot %d : %d echantillons\n" "$n" "$(grep -c '<SAMPLE ' "$TD/lot_$n.xml")"
  i=$((i+LOT))
done
unset P
echo

python3 - "$TD" "$ATT" <<'PY'
import sys, os, csv, glob, collections, datetime
import xml.etree.ElementTree as ET
TD, ATT = sys.argv[1], sys.argv[2]

courant = {}
for f in sorted(glob.glob(os.path.join(TD, "lot_*.xml"))):
    for s in ET.parse(f).getroot().iter("SAMPLE"):
        d = {x.find("TAG").text: (x.find("VALUE").text if x.find("VALUE") is not None else None)
             for x in s.iter("SAMPLE_ATTRIBUTE")}
        d["TITLE"] = s.findtext("TITLE")        # TITLE est un element, pas un attribut
        courant[s.get("accession")] = d

attendu = [tuple(r) for r in csv.reader(open(ATT), delimiter="\t")]
ok = ko = absent = 0
ecarts = []; par_champ = collections.Counter()
for acc, champ, vatt, vorig in attendu:
    if acc not in courant:
        absent += 1; continue
    cur = courant[acc].get(champ)
    if cur == vatt:
        ok += 1; par_champ[champ] += 1
    else:
        ko += 1
        etat = "valeur INITIALE (correction non appliquee)" if cur == vorig else "valeur INATTENDUE"
        ecarts.append((acc, champ, vatt, cur, etat))

print(f"echantillons interroges : {len(courant)}")
print(f"champs verifies         : {len(attendu)}")
print(f"  conformes a l'etat attendu : {ok}")
print(f"  non conformes              : {ko}")
print(f"  echantillons introuvables  : {absent}")
print()
for c, v in sorted(par_champ.items()):
    print(f"  {c:45s} {v}")
if ecarts:
    print(f"\n{len(ecarts)} ecart(s), 10 premiers :")
    for e in ecarts[:10]:
        print(f"  {e[0]} | {e[1]}\n     attendu={e[2]!r}  courant={e[3]!r}  ({e[4]})")
    print("\nUn ecart 'valeur INATTENDUE' massif signifie en general qu'une campagne de")
    print("correction posterieure n'est pas listee dans les tables chainees ci-dessus.")

rap = "verification_cumulee_%s.txt" % datetime.datetime.now().strftime("%Y%m%d_%H%M")
with open(rap, "w") as f:
    f.write("Verification cumulee du depot PRJEB124417\n")
    f.write(f"echantillons {len(courant)} | champs {len(attendu)} | conformes {ok} | ecarts {ko}\n")
    for c, v in sorted(par_champ.items()): f.write(f"{c}\t{v}\n")
    for e in ecarts: f.write("ECART\t" + "\t".join(str(x) for x in e) + "\n")
print(f"\nrapport : {rap}")
print()
if ko == 0 and absent == 0:
    print(f"LES {len(attendu)} VALEURS ATTENDUES SONT EN PLACE sur les {len(courant)} echantillons.")
else:
    print("Etat NON CONFORME a l'attendu — me transmettre le rapport.")
PY
