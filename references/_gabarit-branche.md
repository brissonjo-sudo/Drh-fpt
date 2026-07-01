# Gabarit décisionnel des branches

> Méta-document (instructions de conception, pas de contenu métier). Toute
> branche de `references/` suit **exactement** cette structure, dans cet ordre.
> Objectif : une écriture interprétable par le modèle, orientée **décision**
> plutôt que description.

## Structure imposée d'une branche

1. **Périmètre** — ce que couvre la branche, en deux phrases.
2. **Questions couvertes** — les familles de questions typiques (liste courte).
3. **Arbre de traitement** — le réflexe de raisonnement :
   `question → variables à lever → décision → vérification → livrable`.
4. **Variables à lever** — paramètres collectivité et données manquantes
   propres à la branche, à clarifier avant de trancher.
5. **Règles métier** — le fond, par sous-domaine. Distinguer toujours :
   national / choix local, obligation / faculté, titulaire / contractuel.
6. **Calculs** (si la branche en comporte) — méthode imposée :
   - annoncer les **hypothèses** ;
   - **demander** les données manquantes ;
   - séparer **données connues** et **estimées** ;
   - signaler les **paramètres locaux** et les **valeurs volatiles** à vérifier.
7. **Déclencheurs de vérification** — les points qui imposent le noyau de
   vérification (matrice §2.2 du SKILL.md).
8. **Pièges & confusions fréquentes** — erreurs typiques à bloquer.
9. **Données volatiles à vérifier** — valeurs à ne jamais donner de mémoire.
10. **Livrables** — classés par niveau (décision / organisation / pilotage /
    communication) + éléments obligatoires (ex. voies de recours).
11. **Niveau de confiance** — repères stable / à vérifier / débattu pour la branche.
12. **Checklist de branche** — contrôles spécifiques avant sortie.

## Règles d'écriture

- Imperatif, phrases courtes, une idée par point.
- Valeurs chiffrées : appliquer le **régime du socle §6** — les **valeurs
  d'indexation** (point, cotisations, GIPA, planchers PSC) ne sont jamais
  figées ni données de mémoire ; les **plafonds et barèmes réglementaires**
  (fixés par un décret identifié) sont citables s'ils sont **datés** et assortis
  de « à confirmer en version consolidée ».
- Citer les **références structurelles stables** (codes, numéros de décrets
  fondateurs) en rappelant la vérification de version.
- Pas d'instruction de méta-conception dans le corps métier : elle reste ici.
