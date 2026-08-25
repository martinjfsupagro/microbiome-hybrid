#!/bin/bash
# Suivi du depot en cours. Trouve le job et le journal automatiquement.
#   bash suivi.sh          # etat instantane
#   bash suivi.sh -f       # suivi continu
D=/home/martinj/work/projects/microbiome-hybrid/ena_deposit
J=$(squeue -u "$USER" -h -o "%i %j %T %M %l %R" 2>/dev/null | grep -E 'ena_(test|prod)' | head -1)
MODE=$(printf '%s' "$J" | awk '{print $2}' | sed 's/ena_//')
[ -z "$MODE" ] && MODE=$(ls -t "$D"/submit_*.log 2>/dev/null | head -1 | sed -E 's/.*submit_(test|prod)_.*/\1/')
[ -z "$MODE" ] && { echo "Aucun depot en cours ni journal trouve."; exit 0; }

L=$(ls -t "$D"/submit_${MODE}_*.log 2>/dev/null | head -1)
DONE=$D/done_runs_${MODE}.txt
N=$(ls "$D"/manifests/*.txt 2>/dev/null | wc -l)

etat() {
  local ok ko tot pct
  ok=$(grep -cP '\tOK\t' "$L" 2>/dev/null || true); ok=${ok:-0}
  ko=$(grep -cP '\tECHEC' "$L" 2>/dev/null || true); ko=${ko:-0}
  tot=$(wc -l < "$DONE" 2>/dev/null || echo 0)
  pct=$(awk -v t="$tot" -v n="$N" 'BEGIN{printf "%.1f", (n>0? 100*t/n : 0)}')
  printf '\r  %s/%s runs (%s%%)  ok=%s  echecs=%s   ' "$tot" "$N" "$pct" "$ok" "$ko"
}

if [ -n "$J" ]; then
  echo "job SLURM : $J"
else
  echo "aucun job en file (termine ou interrompu)"
fi
echo "mode      : $MODE"
echo "journal   : $L"
echo

if [ "${1:-}" = "-f" ]; then
  echo "Suivi continu (Ctrl-C pour sortir)"
  while true; do
    etat
    squeue -u "$USER" -h -o "%j" 2>/dev/null | grep -q "ena_$MODE" || { echo; echo "Job termine."; break; }
    sleep 20
  done
else
  etat; echo
fi

echo
KO=$(grep -cP '\tECHEC' "$L" 2>/dev/null || true)
if [ "${KO:-0}" -gt 0 ]; then
  echo "Types d'erreurs rencontrees :"
  grep -oP 'ERROR: .{0,90}' "$L" 2>/dev/null | sed 's/[A-Z]\{3\}[0-9]\{6,\}/<acc>/g' \
    | sort | uniq -c | sort -rn | head -5 | sed 's/^/  /'
  echo
  echo "  \"already exists ... accession\" = run deja soumis (chronometrage) : sans consequence."
  echo "  Toute autre erreur : relancez le script, seuls les runs non aboutis repartent."
fi
