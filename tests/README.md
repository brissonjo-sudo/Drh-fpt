# Tests — drh-fpt

Le harnais exécute chaque cas dans un contexte indépendant, puis peut faire
juger la réponse par un second modèle. `cas-de-test.json` reste la source unique
des 32 variantes, dont 30 actives par mode.

## Schéma des cas

Chaque cas contient `id`, `branche`, `type`, `prompt`, `echec_si`, `contextes`
et `attendus`. Chaque attendu possède un `id` stable et un `texte`. Le juge doit
restituer exactement tous ces identifiants et libellés. Le gate refuse un
critère absent, inconnu, dupliqué, renommé ou sans justification.

`contextes` désigne les branches ou modules à charger en mode sélectif. Une
sélection via `--case` sert au diagnostic et ne peut valider une version.

## Fournisseurs et métriques

Le harnais prend en charge :

- Anthropic Messages API avec `ANTHROPIC_API_KEY` ;
- OpenAI Responses API avec `OPENAI_API_KEY`.

`--provider` et `--judge-provider` peuvent différer. Les paramètres d'effort
sont transmis uniquement par l'adaptateur qui les prend en charge ; un paramètre
incompatible provoque une erreur explicite. Chaque appel conserve durée,
tokens, identifiant de réponse et état de troncature. Aucun coût n'est calculé
sans grille tarifaire datée et vérifiée.

## Contextes

- `--context-mode full` charge le bundle de compatibilité ;
- `--context-mode selective` charge le noyau, les branches déclarées par le cas
  et le gabarit demandé.

Carrière-paie est réparti entre statut/discipline, rémunération/paie et
temps de travail/fin de fonctions. Les dossiers mixtes déclarent plusieurs
contextes.

## Niveaux de preuve

- `rules` : vérifie l'obéissance aux instructions et l'abstention ;
- `snapshot` : ajoute un dossier de sources figées avec `--source-pack` ;
- `live` : exige `--evidence-file`, qui trace par cas la source officielle, la
  date de consultation, la version, le passage utile et la conclusion soutenue.

Un lien présent dans une réponse ne prouve pas une consultation. Le mode
`snapshot` reste une évaluation reproductible d'un corpus daté ; il ne prouve
pas l'état actuel du droit.

Exemple de trace :

```json
{
  "consultations": [{
    "case_id": "01",
    "source_url": "https://www.legifrance.gouv.fr/...",
    "consulted_at": "2026-09-19T10:00:00Z",
    "version_or_date": "version en vigueur au 2026-09-19",
    "supporting_excerpt": "Passage utile, limité au nécessaire",
    "conclusion_supported": "Conclusion juridique soutenue"
  }]
}
```

## Commandes

```bash
# Campagne Anthropic complète
export ANTHROPIC_API_KEY=sk-...
python tests/run_tests.py --judge --strict \
  --legal-skill /chemin/recherche-juridique

# Mode dégradé
python tests/run_tests.py --mode degraded --judge --strict

# Diagnostic ciblé en contexte sélectif
python tests/run_tests.py --case 01 --case 07 --context-mode selective \
  --legal-skill /chemin/recherche-juridique

# Reprise compatible ; les réponses terminées ne sont pas régénérées
python tests/run_tests.py --resume <campagne-id> --judge \
  --legal-skill /chemin/recherche-juridique

# Nouveau jugement des réponses existantes
python tests/run_tests.py --judge-only <campagne-id> \
  --legal-skill /chemin/recherche-juridique \
  --judge-provider openai --judge-model <modele>

# Preuve par corpus figé ou traces de consultation
python tests/run_tests.py --evidence-mode snapshot --source-pack sources/...
python tests/run_tests.py --evidence-mode live --evidence-file traces.json
```

Une reprise exige la même empreinte des cas, le même contexte, le même modèle
répondant et les mêmes paramètres. Un jugement ultérieur reçoit un identifiant
propre dans `evaluations/` et ne remplace pas les évaluations précédentes.

## Résultats

```text
resultats/<campagne-id>/
├── _provenance.json
├── <cas>.md
├── <cas>-response.json
└── evaluations/<evaluation-id>/
    ├── <cas>-eval.json
    └── _bilan.json
```

Les réponses Markdown restent lisibles. Les fichiers JSON portent les
métriques, les empreintes et la validation automatisée.

## Gate de publication

Une version exige une campagne complète `integration` et une campagne complète
`degraded` sur le même commit propre. Chaque campagne doit fournir les 30
réponses et jugements, sans incident, troncature, critère incomplet, erreur
juridique ou échec d'architecture. Le mode `live` exige en plus les traces de
consultation pour les cas juridiquement engageants.

Le gate strict impose `live` à la campagne d'intégration et un modèle juge
distinct du répondant. La campagne dégradée vérifie l'abstention sans prétendre
avoir consulté les sources.

Les campagnes ciblées servent à corriger. Après une modification du skill, le
mode concerné est rejoué en entier. Les rapports validés sont copiés dans
`tests/rapports/` avec le commit, les modèles, les paramètres et les empreintes.

## Contrôles locaux

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 -m py_compile scripts/*.py tests/*.py
python3 -m json.tool tests/cas-de-test.json >/dev/null
python3 scripts/build_bundle.py --check
python3 scripts/check_coherence.py
```
