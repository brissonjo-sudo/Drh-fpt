# Tests — drh-fpt

Dispositif de test du skill par **sous-agents à contexte vierge**.

## Principe

Chaque cas est traité par un **appel API indépendant** dont le seul contexte est
le bundle du skill (en `system`) + le cas (en `user`). Le modèle ne connaît ni
l'historique de conception, ni les réponses attendues : il répond « à froid ».
C'est l'équivalent d'un sous-agent neutre, reproductible.

Un second appel (le **juge**), tout aussi vierge, note chaque réponse contre la
grille d'attendus et repère les affirmations fausses ou inventées.

## Deux protocoles

1. **Harnais API** (`run_tests.py` + `cas-de-test.json`) — automatisé,
   reproductible : injecte le bundle en `system` et rejoue les cas du JSON.
2. **Protocole sous-agents Claude Code** (`prompt-claude-code.md`) — 10 cas
   orchestrés par Claude Code : un sous-agent **répondant** au contexte frais
   par question, puis un sous-agent **juge** indépendant qui applique les
   critères et les règles transverses (référence inventée → ÉCHEC).

S'y ajoute `cas-co-activation.md` : cas transverse testant la collaboration
`drh-fpt` × `recherche-juridique` (abandon de poste / radiation des cadres).

## Contenu

- `cas-de-test.json` — cas + attendus (harnais API).
- `run_tests.py` — harnais (réponse + évaluation optionnelle).
- `prompt-claude-code.md` — protocole sous-agents (10 cas + barèmes).
- `cas-co-activation.md` — cas transverse deux skills + barème.
- `resultats/` — sorties brutes générées (non versionnées).
- `rapports/` — rapports de campagnes validés, datés (versionnés).

## Usage

```bash
export ANTHROPIC_API_KEY=sk-...
python tests/run_tests.py            # répond aux 6 cas (contexte vierge)
python tests/run_tests.py --judge    # répond + évalue (note sur 5 par cas)
```

Options : `--model` (répondant, défaut `claude-sonnet-4-6`), `--judge-model`
(juge, défaut `claude-opus-4-8`).

## Lecture des résultats

- `resultats/<id>.md` — la réponse du sous-agent vierge.
- `resultats/<id>-eval.json` — l'évaluation (statut par critère, erreurs, score).
- `resultats/_bilan.json` — moyenne globale.

## Étendre

Ajouter un cas = un objet dans `cas-de-test.json` (`id`, `branche`, `prompt`,
`attendus`). Viser les comportements sensibles : données volatiles, statuts
particuliers, actes faisant grief, pièges de qualification.
