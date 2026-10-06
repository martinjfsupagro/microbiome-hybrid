# Paquet de soumission — Animal Microbiome (Research article)

Produit le 2026-10-06 à partir de la version de travail (docs/manuscrit/Article.docx md5 45f52898, Supplementary_Data.docx md5 e050a354),
qui reste la référence annotée (notes grises conservées). Ce dossier est entièrement dérivé par script : ne pas l'éditer à la main,
modifier la version de travail puis régénérer.

| Fichier | Contenu |
|---|---|
| Manuscript_microbiome-hybrid.docx | manuscrit sans notes, Additional files 1–18 cités dans l'ordre, double interligne, lignes et pages numérotées, 8 marqueurs [TO COMPLETE] |
| figures/Fig1.png … Fig5.png | figures principales, une par fichier, dans l'ordre d'appel (≈300 dpi à 170 mm) |
| additional_files/Additional_file_1 … 18 | un fichier par élément du supplément (tables .xlsx, notes .docx, figures .pdf) ; bilan_additional_files.tsv = tailles et md5 |
| correspondance_additional_files.tsv | ancien libellé (Table S1…) → numéro d'Additional file, titre, format, source |
| controle_paquet.tsv | 113 contrôles des consignes (scripts/75) : 112 OK, 1 « à compléter » (marqueurs) |
| consignes/ | consignes de la revue lues le 2026-10-06 (Prepare your manuscript, Prepare supporting information, Research article) |

## Régénération (poste local : python-docx, openpyxl, Pillow ; non disponibles dans le python système de meso)

    python scripts/74-maj_image_fig_S3.py <Supplementary_Data.docx e6b95f56> docs/manuscrit/figures/fig_S3_phyla.png 6aeed410584bb617601c64bf0b28f8b1 <sortie>   # déjà appliqué
    python scripts/73-additional_files.py docs/manuscrit/Supplementary_Data.docx docs/soumission/correspondance_additional_files.tsv \
        docs/manuscrit/ENA_accessions_durance.tsv ena_deposit/sample_accessions.tsv ena_deposit/ena_etat_final_oct.tsv docs/manuscrit/figures docs/soumission/additional_files
    python scripts/72-article_soumission.py docs/manuscrit/Article.docx docs/manuscrit/Supplementary_Data.docx docs/soumission/Manuscript_microbiome-hybrid.docx docs/soumission/correspondance_additional_files.tsv
    python scripts/75-controle_paquet.py docs/soumission/Manuscript_microbiome-hybrid.docx docs/soumission/figures docs/soumission/additional_files docs/soumission/correspondance_additional_files.tsv docs/soumission/controle_paquet.tsv

Les md5 des .xlsx et .pdf changent à chaque exécution (date de création écrite par openpyxl et Pillow) ; le contenu est déterministe.

## Différences voulues entre version de travail et copies de soumission (scripts/soumission_commun.py)

- notes grises retirées ; renvois « Table/Figure/Note Sn » → « Additional file n » ;
- « 16S » seul → « 16S rRNA gene » (TERMES) ; « Materials and Methods » → « Methods » (intitulé de la revue) ;
- historique du brouillon retiré (HISTORIQUE, 5 passages des Additional files 1, 6, 12, 17 ; décision JF 2026-10-06) ;
- Additional file 10 : 2 304 runs complets + sample_accession (reçu ENA) ; année de collecte de l'état ENA actuel
  (15Per2015Ch03A, pêché le 2014-08-20 : 2015 → 2014 sur 3 runs) ;
- page de titre, DOI Zenodo, rôle des financeurs, contributions, remerciements : marqueurs [TO COMPLETE].

## Constat ouvert

Le TITLE ENA de ERS31168490 (15Per2015Ch03A) indique « Per 2015 » alors que la pêche date du 2014-08-20 (567/568 titres
suivent « <site> <année> ») ; la vérification exhaustive l'a déclaré conforme parce que la valeur de référence portait la même
erreur. Non corrigé à ce jour.
