# Réponses d'André du 2026-10-06 (questions de suivi du 2026-10-03)

Transmises par JF le 2026-10-06. Questions en gras, réponses **mot pour mot** (aucune reformulation).

**1. Autorisations : quelle autorisation DDT couvre les stations de l'Ain (Suran) et de l'Ardèche ?
Les deux numéros cités relèvent de l'ONEMA et des DDT 04, 05 et 84.**

> il faut rajouter Benjamin Hérodet - Fédération de Pêche 01 (AIN)
> pour l'Ardèche c'était l'ONEMA 07

**2. Euthanasie : confirmer la dislocation cervicale juste avant chaque dissection.**

> Oui seule methode possible pour ne pas perturber l'expression de gene

**3. Conservation : température du tube en éthanol à 95 % destiné au microbiote (−80 °C dans
Guivier et al. 2017).**

> Oui éthanol à 95 % destiné au microbiote  dans de la glace sur le terrain oui stocké à −80 °C  au labo dans un congelateur

**4. Financement : confirmer que le contrat de thèse EDF-CNRS AGDI 428481 relève bien du projet FACIES.**

> Honnêtement je ne sais pas on enleve la reference au projet facies

**5. Code de sexe « X » : sa signification (52 individus).**

> X c'est comme des NA, la difference c'est qu'une des deux categories sont des juveniles, l'autre est non attribuée.

---

## Ce qui reste ouvert après ces réponses `[À CONFIRMER]`

- **(1)** Aucun numéro d'autorisation n'est donné pour le Suran ni pour l'Ardèche. La place de
  Benjamin Hérodet (Fédération de l'Ain pour la pêche et la protection des milieux aquatiques)
  n'est pas précisée : déclaration d'éthique, remerciements ou liste des auteurs.
- **(5)** Les individus non sexés relèvent de **deux** codes dans
  `metadata/genotypes_verifies_sept_180.csv` : `X` (52) et vide (17, « – » dans la Table S2).
  L'un désigne des juvéniles, l'autre des individus non attribués ; **lequel est lequel n'est pas
  dit**. Sans effet sur le contraste femelles/mâles de R27 (script 29, codes `F` = 33 et `M` = 78
  seuls), qui n'utilise aucun des deux.
- **(4)** La mention « the contract that also funded Guivier et al. [31] » reposait sur le même
  rattachement au projet FACIES ; elle est retirée avec lui (décision de l'agent, à valider par JF).

## Second lot (2026-10-06 après-midi, transmis par JF)

- **Codes de sexe** : X = juvéniles (confirmé). X et cases vides deviennent NA dans la Table S2 (déjà fait,
  scripts/57) ; les fichiers de métadonnées du projet **gardent X et le vide**.
- **Autorisations** : pas de numéro pour le Suran ni pour l'Ardèche ; la mention de la Fédération de l'Ain pour la
  pêche et la protection des milieux aquatiques (Suran) et de l'ONEMA 07 (Ardèche) suffit. Texte de l'article
  inchangé, notes grises mises à jour (scripts/63).
- **Benjamin Hérodet** : dans les remerciements (phrase ajoutée, son rôle reste à préciser en note grise).
- **Remerciements (reste) et contributions des auteurs** : vus en fin de manuscrit. Plus rien d'autre en attente
  d'André.
