# Journal des cas — drh-fpt

> Matière première de l'amélioration du skill. À chaque échange
> significatif, consigner ce qui mérite d'être intégré dans une future
> version. **Aucune donnée nominative d'agent** : décrire les cas de
> façon anonymisée.

## Comment consigner

Une entrée par cas, au format ci-dessous.

```
### AAAA-MM-JJ — [titre court]
- Type : lacune | erreur | cas nouveau | livrable récurrent
- Branche : carrière-paie | qvt-sante | recrutement-formation |
  cst-dialogue-social | si-rh-masse-salariale | communication-interne
- Contexte (anonymisé) : ...
- Constat : ce qui a manqué ou mal fonctionné.
- Action proposée : ce qu'il faudrait ajouter/corriger, et dans quel fichier.
- Statut : intégré (v0.2.0) | intégré (vX.Y.Z)
```

## Entrées

### 2026-06-26 — Création du MVP
- Type : cas nouveau
- Branche : carrière-paie
- Contexte : initialisation du skill, branche pilote.
- Constat : socle posé, cinq branches restant à dérouler.
- Action proposée : dérouler qvt-sante, recrutement-formation,
  cst-dialogue-social, si-rh-masse-salariale, communication-interne sur
  le gabarit de carriere-paie.md.
- Statut : à traiter

### 2026-06-26 — Challenge externe (3 IA) et refonte v0.2.0
- Type : erreur + cas nouveau
- Branche : carrière-paie + socle + SKILL
- Contexte : trois IA ont challengé v0.1.0. Tri dans SYNTHESE-CRITIQUES-v0.2.0.md.
- Constat : deux critiques contenaient elles-mêmes des erreurs de droit
  (RIFSEEP police municipale ; tableau des sanctions), écartées après
  vérification sur sources officielles. Apports retenus : matrice métier/
  juridique, gabarit décisionnel, noyau de vérification, posture conseil.
- Action proposée : corrections juridiques P1 + refonte d'architecture P2
  appliquées en v0.2.0. Reste : dérouler les 5 branches sur le gabarit.
- Statut : intégré (v0.2.0)

### 2026-06-26 — Déroulé des 5 branches restantes (v0.3.0)
- Type : cas nouveau
- Branche : qvt-sante, recrutement-formation, cst-dialogue-social,
  si-rh-masse-salariale, communication-interne
- Contexte : extension du skill sur le gabarit décisionnel.
- Constat : couverture complète des six branches de la DRH atteinte.
- Action proposée : amorcer les gabarits de livrables (assets/) et construire un
  jeu de tests de validation par branche.
- Statut : à traiter

### 2026-06-26 — Tests grandeur nature (3 cas) + v0.3.1
- Type : erreur (mineure) + cas nouveau
- Branche : carrière-paie + SKILL
- Contexte : 3 tests (ISFE police municipale, sanction 5 jours, PSC santé 2026),
  tous réussis. Deux manques détectés.
- Constat : droits de la défense implicites en discipline ; renvois inter-branches
  non explicités dans le routeur.
- Action : intégrés en v0.3.1.
- Statut : intégré (v0.3.1)

### 2026-06-26 — Portages externes (4 LLM) + v0.3.2
- Type : amélioration
- Branche : socle + carrière-paie + SKILL
- Contexte : bundle testé sur Gemini, ChatGPT, Vibe, Grok (cas ISFE police municipale).
- Constat : Gemini/ChatGPT/Grok justes ; Vibe a halluciné (modèle ignorant la base).
  Grok a révélé que la règle « données volatiles » était trop large : un plafond
  réglementaire daté (ISFE) est citable et utile.
- Action : distinction volatil / réglementaire intégrée en v0.3.2.
- Statut : intégré (v0.3.2)

### 2026-06-26 — 5e portage (Gemini / PSC) + révision bundle
- Type : amélioration (bundle de portage uniquement)
- Contexte : test PSC santé 2026, réussi (le skill actualise le modèle au-delà
  de son cutoff : généralisation 2029 restituée).
- Constat : 2 travers de portage — citation du nom de fichier source ; ajout
  d'une règle hors base (« montant non proratisable »).
- Action : consigne d'entête du bundle renforcée (réponse naturelle + interdiction
  d'ajouter une règle absente de la base). Skill core inchangé (v0.3.2).
- Statut : intégré (bundle)

### 2026-06-26 — Cadrage d'ouverture & profil (v0.4.0)
- Type : cas nouveau
- Branche : SKILL + parametres-collectivite + assets
- Contexte : optimisation pour la diffusion — calibrer le skill par profil plutôt
  que de le spécialiser par type de collectivité.
- Constat : besoin d'un cadrage opt-in en ouverture + détection des statuts
  particuliers (Ville de Paris, métropole de Lyon…) pour cibler les recherches.
- Action : module de cadrage, fiche profil (3 persistances), typologie statuts
  particuliers. Intégrés en v0.4.0.
- Statut : intégré (v0.4.0)

### 2026-06-26 — Dispositif de tests (v0.4.1)
- Type : cas nouveau
- Contexte : demande de tests délégués à des sous-agents à contexte vierge.
- Constat : pas de clé API dans l'environnement de conception → harness fourni
  pour exécution par l'utilisateur (sous-agents vierges via appels API isolés).
- Action : dossier tests/ (6 cas + run_tests.py + juge LLM optionnel).
- Statut : intégré (v0.4.1)
