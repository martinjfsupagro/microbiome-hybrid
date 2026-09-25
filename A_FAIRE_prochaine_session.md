# À faire à la prochaine ouverture de session

*Écrit le 2026-09-25. À lire en premier ; supprimer chaque point une fois fait.*

## 1. Vérifier la correction ENA du 25/09 (PRJEB124417, identité d'hôte, 25 chromosomes)

Soumise en production le 2026-09-25 à 18:08 : `success=true`, 568/568 accessions identiques
(reçu `ena_deposit/receipt_hote_sept_prod_20260925_180826.xml`). L'application effective n'est
**pas encore vérifiée**.

```bash
cd ~/work/projects/microbiome-hybrid/ena_deposit
bash 9_verifier_hote_sept.sh
```

Attendu : `etat final (727 echantillons) : conformes 727 | non conformes 0` et
`LES 1199 CORRECTIONS D'HOTE SONT APPLIQUEES.`

- Si conforme : retirer la note grise « À CORRIGER DANS LE DÉPÔT » sous *Host identity* dans
  `docs/manuscrit/Supplementary_Data.docx`, et mettre à jour `docs/checklist_avant_ecologie.csv`.
- Si non conforme : ne rien resoumettre ; lire le rapport `verification_hote_sept_*.txt`
  (valeur INITIALE = pas encore propagé ou non appliqué ; valeur INATTENDUE = problème).

Détail : `ena_deposit/MEMO_correction_hote_sept.md`.
