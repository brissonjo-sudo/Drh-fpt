# Validation de DRH-FPT

`cas-de-test.json` contient 32 variantes : **30 cas d’intégration et 30 cas dégradés**.
Chaque réponse vient d’une session indépendante puis d’un modèle juge distinct.

## Consultation réelle avant intégration

Le collecteur utilise le script PISTE du compagnon juridique. Les identifiants
restent dans son environnement local. Le manifeste fixe les textes, passages,
cas et date de référence ; mettre cette date à jour pour une nouvelle revue.

```powershell
python -X utf8 tests/live_sources.py --manifest tests/sources-manifest.json `
  --legal-skill 'C:\chemin\droit-francais-skill' `
  --output tests/resultats/sources
```

Les réponses originales sont archivées sous `raw/*.json.gz`. Chaque trace
contient l’identifiant officiel, la requête, l’horodatage, la date applicable,
le texte lu (avec NOTA transitoires), le chemin de l’archive et son SHA256.
Le validateur contrôle ces champs contre l’archive et refuse une consultation
de plus de 24 heures au démarrage. Les publications JORF prouvent le texte publié
et sont recoupées avec la consolidation. La page CNRACL documente l’affiliation.

Les passages officiels vont **au répondant et au juge**. Les critères et
conclusions attendues vont seulement au juge. Un lien sans trace ne suffit pas.
`rules` évalue les garde-fous ; `snapshot --source-pack` charge des Markdown
datés sans prouver le droit actuel. L’intégration stricte exige `live`.
Le mode dégradé exclut une vérification live et teste le cadrage et l’abstention.

## Deux campagnes complètes

Partir d’un commit propre, avec un compagnon propre et versionné.
Exemple avec le CLI Codex déjà connecté au compte de l’utilisateur :

```powershell
python -X utf8 tests/run_tests.py --provider codex --model gpt-6.1-sol `
  --judge --judge-provider codex --judge-model gpt-6-sol `
  --reasoning-effort medium --judge-reasoning-effort medium `
  --strict --workers 2 --context-mode selective `
  --legal-skill 'C:\chemin\droit-francais-skill' `
  --evidence-mode live --evidence-file tests/resultats/sources/evidence.json

python -X utf8 tests/run_tests.py --mode degraded --provider codex --model gpt-6.1-sol `
  --judge --judge-provider codex --judge-model gpt-6-sol `
  --reasoning-effort medium --judge-reasoning-effort medium `
  --strict --workers 2 --context-mode selective

python -X utf8 tests/release_gate.py --integration '<bilan-integration.json>' `
  --degraded '<bilan-degraded.json>' --output tests/resultats/gate-publication.json
```

Utiliser une paire de modèles distincts disponible sur le compte.
Anthropic Messages (`ANTHROPIC_API_KEY`) et OpenAI Responses (`OPENAI_API_KEY`)
restent pris en charge. Les paramètres incompatibles échouent explicitement.
Aucun coût n’est calculé sans tarif vérifié.

Codex utilise une session éphémère en répertoire temporaire, ignore la
configuration utilisateur, désactive la recherche et refuse les outils.
Les journaux JSONL sont conservés. Le plafond de sortie du CLI est **indicatif** ;
un tour final complet reste obligatoire. `--workers` autorise 1 à 4 cas concurrents.

## Critères, contexte et reprise

Chaque attendu possède un identifiant stable et un texte exact. Le juge
restitue chaque critère avec une justification. Un critère PARTIEL ou ABSENT,
une erreur, une troncature ou un verdict incohérent fait échouer le gate.
`attendus_degraded` et `echec_si_degraded` remplacent les critères nominaux.

`--context-mode selective` charge le noyau, les branches et le gabarit demandé.
`full` charge le bundle. Une sélection `--case` sert seulement au diagnostic.

`--resume <campagne-id>` conserve les réponses et crée une nouvelle évaluation.
`--judge-only <campagne-id>` rejoue le juge. Reprendre avec les mêmes options
de répondant, sources et contexte ; le compagnon reste requis en intégration.
SHA Git, état du dépôt, cas, bundle, compagnon, preuves et contextes doivent
correspondre. Un corpus modifié ne peut pas être associé à d’anciennes réponses.

## Rapports et gate commun

```text
resultats/<campagne-id>/
  _provenance.json
  <cas>.md
  <cas>-response.json
  <cas>-respondant.jsonl          # Codex
  evaluations/<evaluation-id>/
    <cas>-eval.json
    <cas>-juge.jsonl              # Codex
    _bilan.json
```

Le gate commun vérifie les deux bilans stricts, les 30 réponses et jugements
réels par mode, les critères et empreintes, le même commit propre, bundle
et cas. Un sous-ensemble ou un simple verdict favorable ne valide pas une version.
Les deux campagnes définitives suivent les corrections et utilisent le même commit.

Préserver rapports, réponses, jugements, traces et archives sources.
Un commit publiant seulement les preuves doit identifier le commit testé ;
il ne constitue pas une nouvelle exécution du skill.

## Contrôles locaux

```powershell
python -X utf8 -m unittest discover -s tests -p 'test_*.py'
python -X utf8 scripts/build_bundle.py --check
python -X utf8 scripts/check_coherence.py
```

## Validation de la PR18 — 11 octobre 2026

[Rapport complet et archive portable](rapports/VALIDATION-PR18-2026-10-11.md).
Deux campagnes de 30 cas sur le même commit propre, gate commun réussi.
Les preuves et la documentation sont publiées dans un commit distinct ;
le commit testé est identifié dans le rapport et la mesure.
