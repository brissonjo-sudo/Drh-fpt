# drh-fpt — Skill DRH Fonction Publique Territoriale

Skill Claude d'expertise en gestion des ressources humaines de la
**fonction publique territoriale**, à la fois opérationnel et
juridiquement sourcé.

## Périmètre

> **Ce skill est conçu pour les collectivités territoriales de plus de
> 350 agents uniquement.**

À cette strate, la plupart des seuils planchers sont franchis (CST propre,
formation spécialisée à 200 agents, obligation d'emploi de travailleurs
handicapés, rapport social unique). Le skill répond donc directement sur
ces points, sans les conditionner.

Les collectivités de **moins de 350 agents** (rattachement obligatoire au
centre de gestion, absence de certaines instances propres, seuils
spécifiques) **ne sont pas traitées** par cette version.

## Posture

Hybride :

- **Opérationnel par défaut** — réponse rapide, orientée décision et
  livrable.
- **Vérifié sur déclencheur** — une **matrice métier/juridique** explicite
  indique quand vérifier la source (procédure, calcul, délai, condition
  d'accès, compétence d'instance, jurisprudence). Le skill embarque un **noyau
  de vérification autonome** (primarité, date de référence, conflit de normes,
  abstention) et **s'appuie sur le skill `recherche-juridique`** pour
  l'approfondissement.

## Cadrage d'ouverture

À la première question d'une session, le skill peut établir (en option) le
**profil de la collectivité** — type, statut particulier, affiliation, filières —
pour calibrer ses réponses et cibler ses recherches. Profil réutilisable
(fiche à recoller, mémoire Claude, ou fichier local). Voir
`assets/fiche-profil-collectivite.md`.

## Couverture (six branches de la DRH)

Les six branches sont disponibles, toutes construites sur le même gabarit
décisionnel :

1. **Carrière & paie**
2. **QVT & santé**
3. **Recrutement & formation**
4. **CST & dialogue social**
5. **SI RH & masse salariale**
6. **Communication interne**

## Structure

```
drh-fpt/
├── SKILL.md                              Cœur : routeur, posture, méthode
├── README.md                             Ce fichier
├── JOURNAL.md                            Journal des cas (apprentissage)
├── CHANGELOG.md                          Historique des versions
├── SYNTHESE-CRITIQUES-v0.2.0.md          Trace de décision (challenge externe)
├── references/
│   ├── _gabarit-branche.md               Gabarit décisionnel des branches
│   ├── socle-sources-verification.md     Sources FPT, conflits de normes, données volatiles
│   ├── parametres-collectivite.md        Variables +350 agents + garde-fou régimes spécifiques
│   └── carriere-paie.md                  Branche pilote (gabarit décisionnel)
└── assets/
    └── README.md                         Logique des gabarits de livrables
```

## Apprentissage et amélioration

Le skill s'améliore par une boucle pilotée et traçable :

- `JOURNAL.md` recense lacunes, erreurs, cas nouveaux et livrables
  récurrents ;
- la relecture du journal alimente de nouvelles versions, consignées dans
  `CHANGELOG.md` ;
- une auto-vérification à chaque sortie élève la qualité sans réécriture.

Aucune donnée nominative d'agent ne doit être consignée : décrire les cas
de façon anonymisée.

## Dépendance

Recommandé : le skill **`recherche-juridique`** pour l'approfondissement du
volet juridique. Le skill DRH reste fonctionnel sans lui grâce à son noyau de
vérification autonome, mais les deux ensemble offrent la meilleure fiabilité.

## Installation et usage

**Sur Claude / Claude Code** : récupérer le build `drh-fpt.skill` et le charger
comme skill. Il s'active automatiquement sur les questions RH territoriales.

**Sur un autre LLM** : coller le contenu de `drh-fpt-bundle-pour-LLM.md` en tête
de conversation (instructions système). Tous les fichiers du skill y sont
consolidés avec une consigne d'adhérence et d'anti-hallucination.

## Validation

Skill éprouvé avant publication : **3 tests internes** (régime indemnitaire
police municipale, sanction disciplinaire, PSC santé) et **5 portages externes**
(Gemini, ChatGPT, Grok réussis ; Vibe conservé comme contre-exemple). Détail :
`JOURNAL.md`, `SYNTHESE-CRITIQUES-v0.2.0.md`, `CHANGELOG.md`.

## Version

v0.3.0 — six branches déroulées sur gabarit décisionnel. Voir `CHANGELOG.md`.
