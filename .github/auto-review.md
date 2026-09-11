# Règles de relecture du dépôt

Ce dépôt est le skill DRH « source », dont `ansm-drh` reprend l'architecture.
Il n'a **aucune CI** avant l'ajout du présent workflow : `scripts/check_coherence.py`
et `tests/run_tests.py` existent mais ne s'exécutent nulle part automatiquement.
La relecture est donc le seul filet avant fusion, pas un complément à des
contrôles déjà en place.

## À vérifier en priorité, dans cet ordre

- **Cohérence version / bundle / CHANGELOG**, ce que
  `scripts/check_coherence.py` vérifierait s'il tournait : si le diff change
  la `version:` du YAML de `SKILL.md`, `CHANGELOG.md` doit contenir une
  entrée `## [version]` correspondante. Si le diff modifie `SKILL.md` ou un
  fichier de `references/`, `drh-fpt-bundle-pour-LLM.md` doit être régénéré
  dans le même diff (ou son absence explicitement assumée) : c'est un
  fichier dérivé, pas une source indépendante.
- **Le périmètre est strictement les collectivités de plus de 350 agents.**
  Un ajout ou une modification qui traite, même en passant, d'un seuil ou
  d'une règle propre aux collectivités plus petites (rattachement au centre
  de gestion, seuils spécifiques) sans le signaler comme hors périmètre est
  un problème.
- **Aucune valeur, délai ou procédure inventés** sans source primaire
  identifiée dans `references/socle-sources-verification.md`.
- **Toute branche modifiée dans `references/` suit la structure imposée par
  `references/_gabarit-branche.md`**, dans l'ordre : bandeau de maturité,
  périmètre, questions couvertes, arbre de traitement, variables à lever,
  règles métier, déclencheurs de vérification, pièges et confusions,
  données volatiles, livrables, niveau de confiance, checklist.
- **Une correction de fond sur une branche doit mettre à jour ensemble** la
  branche, `JOURNAL.md` et `CHANGELOG.md` (boucle de versioning décrite en
  §9 de `SKILL.md`).

## À ne pas signaler

- Le style d'écriture des fiches métier.
- Un `drh-fpt-bundle-pour-LLM.md` non régénéré si le diff ne touche ni
  `SKILL.md` ni `references/`.
