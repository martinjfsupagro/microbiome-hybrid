#!/bin/bash
# Lance l'etape 3 comme job SLURM plutot que sur la frontale.
#
# Pourquoi : la frontale est chargee (load ~220 pour 31 coeurs, 15 utilisateurs).
# Un noeud de calcul a le meme acces reseau (verifie : TCP 33001 vers fasp.ebi.ac.uk,
# HTTPS vers l'EBI, singularity et ascp disponibles), et le job survit a la deconnexion.
#
#   bash 3c_lancer_en_job.sh test 8      # mode, parallelisme
#   bash 3c_lancer_en_job.sh prod 8
#
# Suivi :  squeue -u $USER
#          tail -f ena_submit_<jobid>.out

set -uo pipefail
MODE="${1:-}"; PAR="${2:-8}"
[ "$MODE" = "test" ] || [ "$MODE" = "prod" ] || { echo "Usage : bash $0 test|prod [parallelisme]"; exit 1; }

D=/home/martinj/work/projects/microbiome-hybrid/ena_deposit

# Le mot de passe est saisi MAINTENANT, en interactif, et depose dans un fichier
# en droits 600 que le job lira. Il n'apparait ni dans le script sbatch, ni dans
# la ligne de commande, ni dans les journaux SLURM.
U=""; P=""
while [ -z "$U" ]; do printf "Identifiant Webin : " > /dev/tty; IFS= read -r U < /dev/tty; U="${U//[[:space:]]/}"; done
while [ -z "$P" ]; do printf "Mot de passe Webin : " > /dev/tty; IFS= read -rs P < /dev/tty; echo > /dev/tty; done
PWF=$D/.webin_pw; umask 077; printf '%s' "$P" > "$PWF"; chmod 600 "$PWF"; unset P
echo "  identifiant '$U', mot de passe stocke temporairement dans $PWF (droits 600)"
echo

if [ "$MODE" = "prod" ]; then
  echo "ATTENTION : soumission REELLE vers l'ENA. Les donnees seront publiques."
  printf "Taper OUI pour confirmer : "; read -r C
  [ "$C" = "OUI" ] || { rm -f "$PWF"; echo "annule."; exit 1; }
  echo
fi

# Duree demandee : 3x l'estimation (2304 runs x ~20 s / PAR), plancher 2 h.
# La QOS par defaut (ondemand-short) plafonne a 1 h : d'ou --qos=cpu-ondemand-long,
# sans quoi le job reste indefiniment en attente (QOSMaxWallDurationPerJobLimit).
WALL=$(awk -v p="$PAR" 'BEGIN{h=3*2304*20/p/3600; if(h<2)h=2; printf "%02d:00:00", (h==int(h)?h:int(h)+1)}')

SB=$(mktemp)
cat > "$SB" <<SBATCH
#!/bin/bash
#SBATCH --job-name=ena_$MODE
#SBATCH --account=ondemand@biomics
#SBATCH --partition=cpu-ondemand
#SBATCH --qos=cpu-ondemand-long
#SBATCH --time=$WALL
#SBATCH --cpus-per-task=$PAR
#SBATCH --mem=$(( PAR * 3 ))G
#SBATCH --output=$D/ena_submit_%j.out

cd $D
export WEBIN_USER='$U'
export WEBIN_PWF='$PWF'
export PAR=$PAR
export NONINTERACTIF=1
bash 3_transferer_et_soumettre.sh $MODE
rm -f '$PWF'
SBATCH

echo "=== Soumission du job ==="
echo "  mode         : $MODE"
echo "  parallelisme : $PAR  (=> $PAR CPU, $(( PAR * 3 )) Go)"
echo "  duree max    : $WALL   (QOS cpu-ondemand-long)"
echo "  estimation   : ~$(awk -v p="$PAR" 'BEGIN{printf "%.1f", 2304*20/p/3600}') h a 20 s/run"
sbatch "$SB"
rm -f "$SB"
echo
echo "Suivi :"
echo "  squeue -u \$USER"
echo "  tail -f $D/ena_submit_<jobid>.out"
echo
echo "Le mot de passe sera supprime automatiquement a la fin du job."
