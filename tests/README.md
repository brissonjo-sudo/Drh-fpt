# Validation de DRH-FPT

`cas-de-test.json` contient 32 variantes : **30 cas d’intégration et 30 cas dégradés**.
Chaque réponse vient d’une session indépendante puis d’un modèle juge distinct.

## Protocole après relecture du 12 octobre 2026

| Suite | Cas par mode | Usage |
|---|---:|---|
| `developpement` (défaut) | 30 | Corpus déjà utilisé pour corriger le skill |
| `regression-ciblee-v1` | 14 | Cas touchés et critiques, sans revendication de qualification |
| `qualification-a-v1` | 12 | Première qualification sur cas neufs |
| `qualification-reserve-v1` | 12 | Réserve après échec A, jamais une relance de A |

Les jeux neufs sont écrits par Claude, relus par Codex puis soumis à **Jo**.
Le gel est refusé sans décision humaine explicite sur les fichiers concrets,
leurs empreintes et les quatre profils (modèles, efforts, versions CLI).
Les seals restent locaux pendant les campagnes pour conserver un commit testé
propre ; ils seront inclus dans les preuves publiées. Ils prouvent une
traçabilité locale, pas une signature d'identité humaine ou fournisseur.

Avant gel, les suites de qualification refusent tout appel. Après lancement,
chaque créneau est consommé ; `--case`, `--resume` et `--judge-only` sont
interdits pour la qualification. Une correction du candidat consomme A ; le
premier lancement de B fixe le nouveau commit, identique pour ses quatre
campagnes. Les barèmes B et profils restent ceux approuvés. Si B échoue, le
candidat est non qualifié et un nouveau cycle distinct doit être préparé.

Ordre : A Codex intégration/dégradé (juge Claude), A Claude natif
intégration/dégradé (juge Codex), puis développement ciblé avec
`gpt-6.1-sol` / `gpt-6-sol`, efforts `high`. Le cycle A compte au maximum
76 réponses et 76 jugements, hors rédaction, revue des cas et arbitrages.

### Profil Claude natif

`--provider claude-cli --execution-profile claude-native` prépare un projet
éphémère : skill DRH, compagnon en intégration, documents officiels du seul
cas. Le CLI utilise l'authentification OAuth existante dans une configuration
temporaire séparée ; aucun secret ni fichier de configuration n'est copié dans
le corpus ou les preuves. Outils limités à Read/Glob/Grep/Skill, hooks et MCP
désactivés, aucun Bash, aucune écriture, aucun fallback ni reprise de session.
Une connexion expirée ou disposant de moins d'une heure est refusée avant
copie et appel : reconnecter Claude par son flux normal. L'adaptateur n'écrit
jamais dans le magasin de connexion permanent.
Le répondant reçoit la question et l'emplacement des documents : pas de bundle,
de rappel final ajouté, de critères ni de réponses antérieures.

Le contrôle commun recoupe les traces JSONL, le modèle exact, les empreintes
du runtime et les fichiers nécessaires réellement lus. Le corpus préparé et
les fichiers lus sont deux mesures différentes. Le juge Claude utilise une
session séparée, sans outils. Les traces vérifient la cohérence des preuves,
**pas l'authenticité cryptographique des appels fournisseur**.

Ce test natif fournit des documents préconsultés. Il **ne valide pas** la
recherche autonome via le serveur juridique en fonctionnement nominal.

### Seuil et arbitrage

Seuil fixé avant lancement : **tous les critères obligatoires satisfaits,
zéro erreur juridique confirmée, aucun doute non tranché**. Scores de style
indicatifs. Une preuve absente, altérée, mal formée ou tronquée bloque toujours.

`--arbitrations <fichier.json>` fournit au contrôle commun des décisions de
Jo séparées : cas, critère/erreur/doute, empreintes suite/réponse/jugement,
décision confirmée, date, motif, sources et trace de l'accord humain. Aucun
jugement original n'est réécrit. Scores bruts et après arbitrage sont rapportés
séparément. Un arbitrage ne peut pas réparer une preuve technique invalide.

Le contrôle commun de qualification exige également `--claude-integration`
et `--claude-degraded`. `--close-game` clôture le jeu seulement après les
quatre campagnes et la résolution des disputes ; la réserve reste bloquée
tant que A n'est pas clos en échec. Ne pas renseigner une décision humaine
sur la seule initiative d'un modèle.

Si un processus est interrompu avant bilan, ne pas inventer de résultats pour
clôturer A. `qualification_control.py abandon` consomme le jeu en échec
technique, avec motif, provenance et empreintes des fichiers déjà produits.
Il n'autorise aucune relance de A ni réussite métier. Le gel concret s'effectue
avec `qualification_control.py freeze --suite <nom> --approval <décision-Jo.json>`.
La réserve peut ensuite qualifier le candidat corrigé sous son propre commit.
Le contrôle exige le registre de consommation ; pour une archive portable,
fournir `--launch-state <registre.json>`. Un jeu clos en échec reste refusé
même si des bilans anciens paraissent favorables.

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

## Deux campagnes de développement complètes (historique)

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

## Développement de la PR18 — 11 octobre 2026

[Rapport complet et archive portable](rapports/VALIDATION-PR18-2026-10-11.md).
Deux campagnes de 30 cas sur le même commit propre, gate commun réussi.
Ces résultats suivent des corrections sur le même corpus et ne constituent
pas la nouvelle qualification sur cas neufs.
Les preuves et la documentation sont publiées dans un commit distinct ;
le commit testé est identifié dans le rapport et la mesure.
