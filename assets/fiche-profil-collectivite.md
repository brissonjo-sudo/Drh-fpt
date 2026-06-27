# Fiche profil — collectivité

> Gabarit rempli lors du cadrage d'ouverture (SKILL.md §6.1). Le skill l'utilise
> pour calibrer ses réponses et cibler ses recherches. **Aucune donnée nominative
> d'agent.**

## Bloc profil (à recoller en tête de session)

```
PROFIL COLLECTIVITÉ — drh-fpt
- Type d'employeur : [commune / EPCI / département / région / CCAS / SDIS / OPH / …]
- Statut particulier : [aucun / Ville de Paris / métropole de Lyon / EPT Grand Paris /
  Aix-Marseille-Provence / Corse / CTU Martinique-Guyane / outre-mer / …]
- Effectif : [> 350 agents — préciser si connu]
- Affiliation au centre de gestion : [oui / non / inconnue]
- Filières notables : [police municipale, sapeurs-pompiers, médico-social, …]
- Organisation : [paie interne ou externalisée ; médecine interne ou conventionnée ; SI RH]
- Particularités : [texte libre]
```

## Modes de persistance

- **Recoller (par défaut)** : copier le bloc ci-dessus et le coller au début de
  chaque nouvelle conversation.
- **Mémoire Claude** : demander à Claude de mémoriser le profil (claude.ai, si
  la mémoire est activée).
- **Fichier local** : enregistrer le bloc dans `profil-collectivite.md` (Claude
  Code ou dépôt) ; le skill le relit à chaque session.

## Usage par le skill

Tant que le profil est présent, le skill ne redemande pas les variables connues
et **oriente ses recherches** (filières, statut particulier) en conséquence. En
cas de **statut particulier**, il déclenche une vigilance renforcée et cible les
textes propres avant de conclure.
