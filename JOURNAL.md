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
- Statut : à traiter | intégré (vX.Y.Z) | intégré (bundle) | validé (vX.Y.Z)
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
- Statut : intégré (v0.3.0)

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
- Statut : intégré (v0.4.1 pour les tests, v0.4.6 pour les gabarits)

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

### 2026-06-27 — Évaluation 10 cas (double sous-agent) + v0.4.2
- Type : erreur (mineure) + amélioration
- Branche : qvt-sante, carrière-paie, cst-dialogue-social, SKILL
- Contexte : protocole 10 cas exécuté par sous-agents frais (répondant Sonnet +
  juge Opus indépendant). Résultat 10/10, 4,9/5, 0 invention.
- Constat : 4 réserves — visa CITIS rattaché au décret FPE 2019-122 au lieu du
  2019-301 (FPT) ; mention imprécise « ISMF » des régimes PM antérieurs ; seuils
  d'instances (CST propre 50 vs 350) ; balisage incomplet des références datées.
- Action : visa CITIS FPT (décret 2019-301) ; régimes PM (décrets 97-702/2000-45/
  2006-1397) ; clarification seuils 50/200/350 ; réflexe Primarité renforcé.
- Statut : intégré (v0.4.2)

### 2026-06-27 — Re-test des cas corrigés + v0.4.3
- Type : erreur (variance) + amélioration
- Branche : carrière-paie
- Contexte : re-test des 5 cas impactés. Q6 et Q9 passent de 4,5 à 5,0 ; Q8/Q2
  maintenus. Q1 (régime indemnitaire PM) a chuté par variance.
- Constat : la procédure d'institution (avis CST → délibération → arrêtés) n'était
  rappelée que dans la branche CST → un répondant frais sur deux l'omettait ; date
  d'application du décret 2024-614 confondue avec l'abrogation au 1/1/2025.
- Action : procédure d'institution explicitée dans carriere-paie ; date du décret
  précisée. Re-test sur 3 répondants : avis CST cité 3/3.
- Statut : intégré (v0.4.3)

### 2026-06-27 — Cas de co-activation + abandon de poste (v0.4.4 / v0.4.5)
- Type : lacune + cas nouveau
- Branche : carrière-paie + tests
- Contexte : ajout d'un cas transverse drh-fpt × recherche-juridique (abandon de
  poste / radiation). Un test réel a révélé que le skill n'avait aucune section
  abandon de poste.
- Constat : répondant frais traitait l'abandon comme « entièrement jurisprudentiel »
  (omission du fondement textuel L. 553-1, 1° CGFP), surfaçait un nom d'arrêt
  erroné (« Béziers » à la place de Casagranda) et transmettait l'arrêté au
  contrôle de légalité (à tort). Points vérifiés sur Légifrance/CGCT.
- Action : tests/cas-co-activation.md (v0.4.4) ; section §5.10 « Abandon de poste »
  (v0.4.5) — fondement L. 553-1, 1° CGFP, mise en demeure jurisprudentielle
  (CE Sect. 11 déc. 1998, Casagranda, n° 147511), distracteur CMO, non-application
  de la présomption de démission du privé, arrêté non rétroactif / non transmissible.
- Statut : intégré (v0.4.5)

### 2026-06-27 — Validation de la co-activation réelle (2 skills chargés)
- Type : validation
- Branche : carrière-paie + co-activation recherche-juridique
- Contexte : énoncé abandon de poste rejoué avec les DEUX skills (drh-fpt +
  recherche-juridique) chargés simultanément ; juge indépendant.
- Constat : RÉUSSITE 5/5 sur les 9 critères du barème, dont la co-activation
  visible. drh-fpt cadre et produit les actes ; recherche-juridique sécurise
  (ratio decidendi, réserves de source, table de vérification en source primaire,
  auto-critique adversariale). 0 référence présentée comme vérifiée à tort.
- Action : aucune correction nécessaire — comportement validé.
- Statut : validé (v0.4.5)

### 2026-07-01 — Audit complet et extension de couverture (v0.4.7 → v0.5.0)
- Type : lacune + cas nouveau
- Branche : carrière-paie, qvt-sante, recrutement-formation + deux branches
  nouvelles (agents contractuels ; statut : garanties, déontologie &
  signalements)
- Contexte : audit complet du skill sur trois axes (juridique, outillage,
  couverture). Constat d'audit : les agents contractuels (20-25 % des
  effectifs d'une grande collectivité) et plusieurs flux hebdomadaires d'une
  DRH (protection fonctionnelle, déontologie/cumul, signalements/harcèlement,
  RGPD RH) n'avaient aucune branche dédiée ; par ailleurs carriere-paie,
  qvt-sante et recrutement-formation présentaient des lacunes ponctuelles
  (emplois fonctionnels et décharge de fonctions, temps de travail détaillé,
  grève et retenue sur traitement, chômage des agents publics, inaptitude/
  reclassement/PPR, égalité professionnelle, vacataires, apprentissage).
- Action proposée : quick wins juridiques déjà traités en v0.4.7 ; outillage
  (build du bundle, vérification de cohérence, harnais de tests durci) traité
  en v0.4.8-v0.4.9 ; puis rédaction de deux nouvelles branches complètes
  (`contractuels.md`, `statut-garanties.md`) et d'extensions ciblées des trois
  branches existantes, rédigées par Sonnet puis **vérifiées adversarialement
  par Opus** sur sources officielles avant intégration (corrections
  appliquées : protection des 6 mois des emplois fonctionnels courant du plus
  tardif nomination agent/désignation autorité, information CNFPT/CDG en sus
  de l'assemblée, effet différé de la décharge, exclusion ARE de l'abandon de
  poste, auto-assurance obligatoire pour titulaires/stagiaires, plafond CET
  60 jours, PPR avec report/prolongation, fonds usure professionnelle FPT
  inexistant à ce jour, échéance de l'expérimentation titularisation handicap
  au 6 août 2025, pénalité plan d'action égalité réductible à 0,5 %). 5 cas de
  test nouveaux ajoutés (protection fonctionnelle, licenciement d'un
  contractuel, grève/retenue FPT, décharge de fonctions d'un DGS, inaptitude/
  PPR).
- Statut : intégré (v0.5.0)
