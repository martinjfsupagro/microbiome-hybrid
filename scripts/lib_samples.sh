#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Fonctions partagées pour retrouver les échantillons et leurs fichiers.
# À sourcer : source "$PROJECT_DIR/scripts/lib_samples.sh"
#
# Repris de azelie. Nommage des fastq consolidés (Illumina) :
#   14Ain1001Cn01A_S1_L001_R1_001.fastq.gz   → échantillon « 14Ain1001Cn01A »
# ─────────────────────────────────────────────────────────────────────────────

# lister_R1 <dossier>
#   Affiche les chemins des fichiers R1, un par ligne, triés.
lister_R1() {
    local dir="$1"
    find "$dir" -maxdepth 1 -type f \
        \( -name '*_R1_001.fastq.gz' -o -name '*_R1_001.fastq' \
        -o -name '*_R1.fastq.gz'     -o -name '*_R1.fastq' \) \
        | sort
}

# fichier_R2 <chemin_R1>
#   Donne le R2 correspondant. Ne remplace que la DERNIÈRE occurrence de _R1,
#   pour ne pas casser un nom d'échantillon qui contiendrait « _R1 ».
fichier_R2() {
    local r1="$1" base dir
    dir="$(dirname "$r1")"; base="$(basename "$r1")"
    echo "$dir/$(echo "$base" | sed 's/\(.*\)_R1/\1_R2/')"
}

# nom_echantillon <chemin_R1>
#   Retire l'habillage Illumina (_S123_L001_R1_001) ou le simple _R1,
#   ainsi que l'extension. « 14Ain1001Cn01A_S1_L001_R1_001.fastq.gz » → « 14Ain1001Cn01A »
nom_echantillon() {
    local b; b="$(basename "$1")"
    b="${b%.gz}"; b="${b%.fastq}"; b="${b%.fq}"
    b="$(echo "$b" | sed -E 's/_S[0-9]+_L[0-9]+_R1(_[0-9]+)?$//')"   # Illumina
    b="${b%_R1_001}"; b="${b%_R1}"                                    # simple
    echo "$b"
}

# verifier_paires <dossier>
#   Contrôle que chaque R1 a son R2. Renvoie 1 si un R2 manque.
verifier_paires() {
    local dir="$1" r1 r2 manquants=0 total=0
    while IFS= read -r r1; do
        total=$(( total + 1 ))
        r2="$(fichier_R2 "$r1")"
        if [[ ! -f "$r2" ]]; then
            echo "  ⚠ R2 manquant pour $(basename "$r1")" >&2
            manquants=$(( manquants + 1 ))
        fi
    done < <(lister_R1 "$dir")
    if (( total == 0 )); then
        echo "  ERREUR : aucun fichier R1 trouvé dans $dir" >&2
        return 1
    fi
    if (( manquants > 0 )); then
        echo "  ERREUR : $manquants paire(s) incomplète(s) sur $total" >&2
        return 1
    fi
    echo "  ✓ $total paires R1/R2 complètes"
    return 0
}

# noms_dupliques <dossier>
#   Deux fichiers différents peuvent donner le même nom d'échantillon après
#   nettoyage : les sorties s'écraseraient silencieusement. Renvoie 1 si c'est
#   le cas.
noms_dupliques() {
    local dir="$1" dups
    dups="$(while IFS= read -r f; do nom_echantillon "$f"; done < <(lister_R1 "$dir") | sort | uniq -d)"
    if [[ -n "$dups" ]]; then
        echo "  ERREUR : noms d'échantillon en double après normalisation :" >&2
        echo "$dups" | sed 's/^/    /' >&2
        return 1
    fi
    return 0
}
