# Tests — drh-fpt

Dispositif de test du skill par **sous-agents à contexte vierge**.

## Principe

Chaque cas est traité par un **appel API indépendant** dont le seul contexte est
le bundle du skill (en `system`) + le cas (en `user`). Le modèle ne connaît ni
l'historique de conception, ni les réponses attendues : il répond « à froid ».
C'est l'équivalent d'un sous-agent neutre, reproductible.

Un second appel (le **juge**), tout aussi vierge, note chaque réponse contre la
grille d'attendus et repère les affirmations fausses ou inventées.

## Contenu

- `cas-de-test.json` — 6 cas (un par branche) + attendus.
- `run_tests.py` — harness (réponse + évaluation optionnelle).
- `resultats/` — réponses et évaluations générées.

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
