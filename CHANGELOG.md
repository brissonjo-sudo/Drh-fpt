# Changelog — drh-fpt

Format : versionnage sémantique MAJEUR.MINEUR.PATCH.

## [0.4.4] — 2026-06-27 — Tests : cas de co-activation (barème rectifié)

### Ajouté
- `tests/cas-co-activation.md` : cas transverse `drh-fpt` × `recherche-juridique`
  (abandon de poste / radiation des cadres), avec barème de correction.

### Corrigé (barème de test, suite à un test réel)
- Fondement de l'abandon de poste : **L. 553-1, 1° du CGFP** est un fondement
  **textuel** (ordonnance 2021-1574) — le citer n'est pas une invention. Seul le
  régime de la mise en demeure est jurisprudentiel.
- L'**épuisement des droits à congé de maladie n'est pas un critère** de l'abandon
  de poste (absence injustifiée + non-réponse à mise en demeure). Les congés
  maladie statutaires restent par ailleurs plafonnés (CMO 12 mois, CLM 3 ans,
  CLD 5 ans).

### Note
- Modification limitée au dossier `tests/` : le comportement du skill est inchangé.

## [0.4.3] — 2026-06-27 — Procédure régime indemnitaire (re-test)

### Corrigé
- **Régime indemnitaire / ISFE (carriere-paie.md)** — ajout explicite de la
  **procédure d'institution** : *avis préalable du CST → délibération → arrêtés
  individuels*. Un re-test a montré qu'un répondant frais pouvait omettre l'avis
  du CST faute de l'avoir sous les yeux dans la branche carrière-paie (il n'était
  rappelé que dans la branche CST).
- **Date du décret 2024-614 (carriere-paie.md)** — précision : décret applicable
  **depuis sa publication (2024)** ; seuls les anciens régimes sont abrogés au
  1er janvier 2025 — ne pas dater l'entrée en vigueur de l'ISFE au 1/1/2025.

### Re-test
- Re-test des 5 cas impactés par la v0.4.2 : **Q6 4,5→5,0**, **Q9 4,5→5,0**,
  **Q8 et Q2 maintenus à 5,0**. Les corrections v0.4.2 sont validées. Q1 a fait
  apparaître la lacune ci-dessus (procédure CST), traitée par cette version.

### Modifié
- Bundle `drh-fpt-bundle-pour-LLM.md` resynchronisé.

## [0.4.2] — 2026-06-27 — Corrections issues de l'évaluation 10 cas

### Corrigé
- **CITIS (qvt-sante.md)** — ajout du visa FPT exact : **CGFP art. L. 822-18 et s.**
  et **décret n° 2019-301 du 10 avril 2019**, avec mise en garde explicite contre
  le décret n° 2019-122 (propre à la fonction publique d'État). Corrige le seul
  risque d'erreur factuelle recopiable dans un acte (cas Q6).
- **Régime indemnitaire police municipale (carriere-paie.md)** — les anciens
  régimes remplacés par l'ISFE sont désormais nommés précisément (décrets
  n° 97-702, 2000-45 et 2006-1397), en lieu et place de la mention imprécise
  « ISMF, ISF… » (cas Q1, cohérent avec `SYNTHESE-CRITIQUES-v0.2.0.md`).
- **Seuils des instances (cst-dialogue-social.md)** — clarification : **CST propre
  dès 50 agents**, à ne pas confondre avec les **200 agents** (formation
  spécialisée SSCT) ni les **350 agents** (affiliation CDG / périmètre du skill)
  (cas Q2/Q8).

### Modifié
- **Réflexe « Primarité » (SKILL.md §3)** — consigne renforcée : toute référence
  numérotée/datée ou date d'entrée en vigueur citée sans vérification en séance,
  *a fortiori* pour une réforme récente, est assortie de « à confirmer en version
  consolidée » (cas Q9).
- **Bundle** `drh-fpt-bundle-pour-LLM.md` régénéré en cohérence (et resynchronisé
  à la version courante).

### Évaluation
- Protocole 10 cas (`tests/prompt-claude-code.md`), double sous-agent
  répondant/juge : **10/10 réussites, moyenne 4,9/5, 0 invention** avant
  corrections. Les corrections ci-dessus traitent les réserves résiduelles.

## [0.4.1] — 2026-06-26 — Dispositif de tests

### Ajouté
- Dossier `tests/` : harness de validation par **sous-agents à contexte vierge**.
  Chaque cas est traité par un appel API isolé (skill en `system` + cas en `user`),
  avec un **juge LLM** optionnel qui note la réponse contre une grille d'attendus.
- `tests/cas-de-test.json` : 6 cas (un par branche) + critères.
- `tests/run_tests.py`, `tests/README.md`.

### Note
- Les tests s'exécutent avec une clé API Anthropic (non figée dans le dépôt).
  Le comportement du skill est inchangé.

## [0.4.0] — 2026-06-26 — Cadrage d'ouverture & profil de collectivité

### Ajouté
- **Module de cadrage d'ouverture** (SKILL.md §6.1, opt-in) : établit en début de
  session le profil de la collectivité (type, statut particulier, effectif,
  affiliation CDG, filières) pour calibrer les réponses et **cibler les recherches
  juridiques**.
- **Fiche profil réutilisable** (`assets/fiche-profil-collectivite.md`) avec trois
  modes de persistance : recoller (défaut), mémoire Claude, fichier local.
- **Typologie des collectivités à fonctionnement particulier**
  (`parametres-collectivite.md` §6) : Ville de Paris (corps propres), métropole de
  Lyon, AMP, EPT Grand Paris, Corse, CTU, outre-mer → vigilance renforcée et
  recherche ciblée.

### Intention
- Skill conçu pour la **diffusion** : reste neutre tous types d'employeurs, mais
  s'auto-calibre via le profil plutôt que de se spécialiser par type.

## [0.3.2] — 2026-06-26 — Distinction volatil / réglementaire

### Modifié
- Règle des valeurs chiffrées **scindée en deux** (socle, carrière-paie, SKILL) :
  - **valeurs d'indexation** (point d'indice, cotisations, GIPA, planchers PSC) :
    jamais de mémoire ;
  - **plafonds réglementaires** fixés par décret (ISFE 33/32/30 % et
    9 500/7 000/5 000 €, RIFSEEP par groupe, contingent IHTS) : **citables** si
    datés et assortis de « à confirmer en version consolidée ».
- Branche carrière-paie : plafonds ISFE désormais explicités (avec réserve).

### Contexte
- Amélioration détectée lors du 4ᵉ portage externe (Grok) : refuser de citer un
  plafond réglementaire stable rendait le skill moins utile qu'un modèle qui le
  cite correctement. Bilan : 3 portages réussis (Gemini, ChatGPT, Grok), 1
  contre-exemple (Vibe, modèle ignorant la base).

## [0.3.1] — 2026-06-26 — Corrections issues des tests

### Ajouté
- Branche carrière-paie : sous-section **droits de la défense** (communication
  du dossier, assistance, délai) et rappel de la **prescription** disciplinaire.
- `SKILL.md` : note **renvois inter-branches** dans le routeur.

### Contexte
- Améliorations détectées lors de trois tests grandeur nature (régime
  indemnitaire police municipale, sanction disciplinaire, PSC santé), tous
  passés avec succès.

## [0.3.0] — 2026-06-26 — Déroulé des six branches

### Ajouté
- Cinq branches rédigées sur le **gabarit décisionnel**, complétant la branche
  pilote carrière-paie :
  - `qvt-sante.md` — prévention (DUERP, RPS), conseil médical, congés et CITIS,
    handicap, télétravail, action sociale, **PSC** (prévoyance obligatoire 2025,
    santé obligatoire 2026, généralisation prévoyance 2029 — loi 2025-1251).
  - `recrutement-formation.md` — concours, contractuels (loi 2019), déclaration
    de vacance, formations CNFPT, CPF, entretien professionnel.
  - `cst-dialogue-social.md` — CST (fusion 2022), formation spécialisée, CAP/CCP,
    élections, droit syndical, LDG, RSU, négociation collective.
  - `si-rh-masse-salariale.md` — chapitre 012, GVT / noria / report, DSN, RSU,
    GPEEC, tableau des effectifs.
  - `communication-interne.md` — onboarding, information obligatoire (LDG, RSU),
    marque employeur, RGPD.
- Routeur du `SKILL.md` mis à jour : les six branches sont disponibles.

### Vérifié sur sources officielles
- Calendrier **PSC** territorial (prévoyance 2025 / santé 2026 / généralisation
  prévoyance 2029).

### À venir (v0.4.0)
- Premiers gabarits concrets dans `assets/`.
- Jeu de tests de validation (déclenchement + qualité par branche).

## [0.2.0] — 2026-06-26 — Refonte après challenge externe

Intégration de la feuille de route issue du tri de trois critiques externes
(Gemini, ChatGPT, « Vibe »), avec deux corrections juridiques vérifiées sur
sources officielles. Détail → `SYNTHESE-CRITIQUES-v0.2.0.md`.

### Corrigé (juridique, vérifié)
- **Police municipale** : retrait de l'amalgame avec le RIFSEEP. Régime propre
  **ISFE** (décret n° 2024-614 du 26 juin 2024), deux parts, art. L714-13 CGFP.
- **Source RIFSEEP FPT** : viser le décret n° **91-875** + délibération locale,
  et non le seul décret État 2014-513.
- **Affiliation CNRACL** : distinction **temps non complet (≥ 28 h)** vs **temps
  partiel** (un agent à temps partiel reste CNRACL).
- **Échelle des sanctions** : tableau vérifié (CGFP L533-1 s.), conseil de
  discipline requis dès le **2e groupe** ; exclusion ≤ 3 jours au **1er groupe**.
- **CAP** : ajout des **saisines à l'initiative de l'agent** (révision du CREP,
  refus de télétravail / temps partiel / CPF).
- Formulations nuancées : avancement d'échelon « de plein droit sous réserve » ;
  principe de parité non synthétisé.

### Ajouté (architecture & conception LLM)
- **Matrice métier / juridique** explicite (quand vérifier la source).
- **Noyau de vérification autonome** (4 réflexes) + renvoi `recherche-juridique`.
- **Gabarit décisionnel** normalisé des branches (`_gabarit-branche.md`).
- **Posture conseil** (alternative légale plutôt que refus sec).
- **Niveau de confiance** gradué.
- **Règle de résolution des conflits de normes** (socle).
- **Liste des données volatiles** à vérifier, sans figer les valeurs (socle).
- **Garde-fou régimes spécifiques** (PM, SPP, OPH, CCAS).
- **Rubrique Calculs** et **livrables classés par niveau** + éléments obligatoires.
- Mécanisme `JOURNAL.md` clarifié (écriture via outil ou bloc à copier-coller).
- Métadonnées : dépendance versionnée, compatibilité.

### Écarté (motivé dans la synthèse)
- Réintégration de la PM au RIFSEEP (faux). Cache de valeurs datées
  (contre-productif). Sur-process de maintenance.

### À venir (v0.3.0)
- Déroulé des 5 branches restantes sur le gabarit décisionnel.
- Premiers gabarits concrets dans `assets/`.
- Jeu de tests de validation.

## [0.1.0] — 2026-06-26 — MVP

### Ajouté
- `SKILL.md`, socle des sources, paramètres collectivité, branche pilote
  carrière-paie, `README.md`, `JOURNAL.md`, `assets/README.md`.

### Périmètre
- Collectivités de plus de 350 agents uniquement.
