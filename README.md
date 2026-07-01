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
centre de gestion — seuil compté en **fonctionnaires** —, absence de
certaines instances propres, seuils spécifiques) **ne sont pas traitées**
par cette version.

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
├── LICENSE                               CC BY-SA 4.0
├── JOURNAL.md                            Journal des cas (apprentissage)
├── CHANGELOG.md                          Historique des versions
├── SYNTHESE-CRITIQUES-v0.2.0.md          Trace de décision (challenge externe)
├── drh-fpt-bundle-pour-LLM.md            Bundle mono-fichier (portage autres LLM)
├── scripts/
│   ├── build_bundle.py                   Régénère le bundle depuis les sources (+ --check, --package)
│   ├── bundle-preambule.md               Gabarit du préambule du bundle (placeholder {{VERSION}})
│   └── check_coherence.py                Vérifie version/bundle/CHANGELOG/renvois/arbre README
├── references/
│   ├── _gabarit-branche.md               Gabarit décisionnel des branches
│   ├── socle-sources-verification.md     Sources FPT, conflits de normes, valeurs chiffrées
│   ├── parametres-collectivite.md        Variables +350 agents + garde-fous régimes spécifiques
│   ├── carriere-paie.md                  Branche carrière & paie
│   ├── qvt-sante.md                      Branche QVT & santé
│   ├── recrutement-formation.md          Branche recrutement & formation
│   ├── cst-dialogue-social.md            Branche CST & dialogue social
│   ├── si-rh-masse-salariale.md          Branche SI RH & masse salariale
│   └── communication-interne.md          Branche communication interne
├── assets/
│   ├── README.md                         Logique et index des gabarits
│   ├── fiche-profil-collectivite.md      Profil de collectivité (cadrage d'ouverture)
│   ├── decision-modele.md                Gabarit arrêté / décision individuelle
│   ├── procedure-modele.md               Gabarit fiche de procédure
│   ├── note-modele.md                    Gabarit note d'aide à la décision
│   ├── deliberation-modele.md            Gabarit délibération
│   └── courrier-modele.md                Gabarit courrier d'agent / note de service
└── tests/
    ├── README.md                         Dispositif de tests (deux protocoles)
    ├── cas-de-test.json                  Source unique des cas (12 standard + 5 adversariaux)
    ├── run_tests.py                      Harnais API (répondant + juge)
    ├── prompt-claude-code.md             Protocole sous-agents Claude Code (lit cas-de-test.json)
    ├── cas-co-activation.md              Cas transverse drh-fpt × recherche-juridique
    └── rapports/                         Rapports de campagnes validés (datés)
        └── RAPPORT-2026-06-27.md         Campagne 10 cas (v0.4.2, archivée)
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

Recommandé : le skill **`recherche-juridique`** (v2.2.0 ou supérieure) pour
l'approfondissement du volet juridique. Le skill DRH reste fonctionnel sans lui
grâce à son noyau de vérification autonome, mais les deux ensemble offrent la
meilleure fiabilité (co-activation validée — voir Validation).

## Installation et usage

**Sur Claude / Claude Code** : charger le dossier du skill (`SKILL.md` +
`references/` + `assets/`) — ou l'archive de la release — comme skill. Il
s'active automatiquement sur les questions RH territoriales.

**Sur un autre LLM** : coller le contenu de `drh-fpt-bundle-pour-LLM.md` en tête
de conversation (instructions système). Les fichiers de connaissance et de
règles y sont consolidés avec une consigne d'adhérence et d'anti-hallucination
(les gabarits de livrables `assets/` ne sont pas inclus dans le bundle).

## Validation

Le skill est éprouvé par un dispositif de tests anti-triche (sous-agents
répondant/juge à contextes séparés — voir `tests/`) :

- **Campagne 10 cas** (v0.4.2, 2026-06-27) : **10/10 réussites, moyenne
  4,9/5, 0 référence inventée** ; les réserves détectées ont été corrigées
  (v0.4.2 → v0.4.5) puis re-testées.
- **Co-activation réelle** avec `recherche-juridique` (abandon de poste) :
  **réussite 5/5 sur 9 critères**.
- Historique : 3 tests internes initiaux + 5 portages externes (Gemini,
  ChatGPT, Grok réussis ; Vibe conservé comme contre-exemple).

Détail : `tests/rapports/`, `JOURNAL.md`, `CHANGELOG.md`.

## Licence

**CC BY-SA 4.0** — voir `LICENSE`.

## Version

Version courante : voir l'en-tête YAML de `SKILL.md` (source unique) et le
détail des évolutions dans `CHANGELOG.md`.
