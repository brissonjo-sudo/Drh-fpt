# Tests — drh-fpt

Dispositif de test du skill par **sous-agents à contexte vierge**.

## Principe

Chaque cas est traité par un **appel API indépendant** dont le seul contexte est
le bundle du skill (en `system`) + le cas (en `user`). Le modèle ne connaît ni
l'historique de conception, ni les réponses attendues : il répond « à froid ».
C'est l'équivalent d'un sous-agent neutre, reproductible.

Un second appel (le **juge**), tout aussi vierge, note chaque réponse contre la
grille d'attendus et repère les affirmations fausses ou inventées.

## `cas-de-test.json` — source unique des cas

**Tous** les cas de test (harnais API et protocole sous-agents Claude Code)
vivent désormais dans **`cas-de-test.json`**, pour éviter toute divergence
entre deux jeux de cas. Ce fichier contient actuellement **32 cas**, dont
**30 sont actifs dans chaque mode de campagne** :

- **22 cas `"standard"`** — questions RH représentatives des huit branches,
  avec leurs `attendus` (critères de réussite) ;
- **5 cas `"echec_attendu"`** — cas **adversariaux** : le skill promet de
  s'abstenir/rediriger dans certaines situations (hors périmètre, données
  volatiles, sujet non couvert, transposition indue) ; ici la **réussite**
  consiste à refuser de répondre normalement ;
- **5 cas `"architectural"`** — cas transversaux qui évaluent la chaîne
  d'exécution indépendamment de la seule exactitude juridique : qualification,
  variables bloquantes, règle nationale versus choix local, activation de
  plusieurs branches, décision, recommandation, plan d'action et production
  effective du livrable demandé.

Champs par cas : `id`, `branche`, `type` (`standard`, `echec_attendu` ou
`architectural`), `prompt`, `attendus` (liste), `echec_si` (liste,
éventuellement vide — conditions disqualifiantes spécifiques au cas) et,
pour les variantes conditionnelles, `modes` (`integration` ou `degraded`).

Les cas 15 et 16 existent dans deux variantes :

- **intégration** : le compagnon est disponible, la réussite consiste à
  vérifier puis répondre avec une source officielle traçable ;
- **mode dégradé** : le compagnon est indisponible, la réussite consiste à
  annoncer ce mode et à s'abstenir de fournir la donnée exacte non vérifiée.

## Critères architecturaux

Les cas architecturaux sont jugés comme des cas de réussite ordinaires, avec
des critères transversaux renforcés. Une réponse peut être juridiquement juste
et néanmoins échouer si elle :

- conclut avant d'avoir qualifié le dossier et identifié les variables
  bloquantes ;
- confond une règle nationale impérative avec une délibération ou un choix
  local ;
- ignore une branche nécessaire ou applique le régime du titulaire à un
  contractuel ;
- ne formule ni état de décision ni recommandation ;
- ne fournit pas de plan d'action opérationnel ;
- annonce un livrable sans le produire réellement.

Réciproquement, une architecture réussie ne compense pas une affirmation
juridique fausse. Le juge rend deux appréciations distinctes :

- **architecture d'exécution** ;
- **fiabilité juridique**.

Une erreur juridique, y compris dans un développement surnuméraire, fait
échouer la fiabilité juridique et le verdict global. Une référence récente ou
postérieure à une date de cutoff ne peut pas être déclarée inventée pour ce seul
motif : elle doit être vérifiée sur une source officielle ou rester classée
comme non tranchée.

Le référentiel de ces exigences est
`references/contrat-execution.md`. L'ajout des cas au JSON ne constitue pas une
preuve de réussite : seuls une campagne répondant + juge effectivement exécutée
et son rapport permettent de conclure sur le comportement du modèle.

## Deux protocoles, une seule source de cas

1. **Harnais API** (`run_tests.py` + `cas-de-test.json`) — automatisé,
   reproductible : en mode nominal, injecte le bundle DRH et le dépôt ou bundle
   du compagnon dans `system`; en mode dégradé, injecte le bundle DRH avec
   l'indisponibilité explicite du compagnon. Il rejoue les 30 cas actifs du
   mode choisi ; le juge applique `echec_si` et, pour les cas adversariaux,
   inverse la logique de verdict (réussite = refus correct).
2. **Protocole sous-agents Claude Code** (`prompt-claude-code.md`) — orchestré
   par Claude Code sur le dépôt courant (pas de clonage) : un sous-agent
   **répondant** au contexte frais par cas, puis un sous-agent **juge**
   indépendant qui lit `cas-de-test.json` pour les critères et les règles
   transverses (référence inventée → ÉCHEC ; cas adversarial → réussite si
   refus/abstention/redirection).

S'y ajoute `cas-co-activation.md` : cas transverse testant la collaboration
`drh-fpt` × `recherche-juridique` (abandon de poste / radiation des cadres),
jouable aussi en variante dégradée avec `drh-fpt` seul.

## Contenu

- `cas-de-test.json` — **source unique** des cas (standard + architecturaux +
  adversariaux),
  attendus et `echec_si` (harnais API + protocole sous-agents).
- `run_tests.py` — harnais (réponse + évaluation optionnelle), lit `type` et
  `echec_si` pour juger correctement les cas adversariaux.
- `test_harness.py` — contrôles locaux sans API : JSON, séparation des modes,
  chargement du compagnon et composition du contexte.
- `prompt-claude-code.md` — protocole sous-agents (renvoie à `cas-de-test.json`
  pour les cas et barèmes, ne les duplique plus).
- `cas-co-activation.md` — cas transverse deux skills + barème + variante
  dégradée (drh-fpt seul).
- `resultats/` — sorties brutes générées (non versionnées).
- `rapports/` — rapports de campagnes validés, datés (versionnés).

## Usage

```bash
export ANTHROPIC_API_KEY=sk-...
python tests/run_tests.py --legal-skill /chemin/recherche-juridique
python tests/run_tests.py --judge --strict --legal-skill /chemin/recherche-juridique
python tests/run_tests.py --mode degraded --judge --strict
```

Le chemin du compagnon peut viser son dépôt, son dossier `skill/` ou un bundle
Markdown. Le chargeur résout notamment la structure actuelle
`droit-francais-skill/skill/SKILL.md`.

Options : `--model` (répondant, défaut `claude-sonnet-4-6`), `--judge-model`
(juge, défaut `claude-opus-4-8`), `--mode` (`integration` par défaut ou
`degraded`) et `--legal-skill` (dépôt ou bundle Markdown du compagnon,
obligatoire en intégration). `--strict` exige `--judge` et renvoie un code
non nul si la campagne est incomplète, tronquée, non parsable, exécutée depuis
un dépôt sale, si un critère n'est pas entièrement satisfait ou si l'un des
verdicts attendus est en échec.

Le juge API reçoit le même corpus de skills que le répondant afin de contrôler
les règles applicables. Il ne dispose toutefois d'aucun accès direct à
Légifrance : cette campagne est un **préflight reproductible**, pas une preuve
autonome de fraîcheur juridique. Toute référence non contrôlable dans le corpus
doit rester signalée comme non tranchée.

Chaque campagne enregistre automatiquement :

- un identifiant de campagne et les dates UTC ;
- le mode et les modèles ;
- la version, le SHA Git et l'état propre/sale de chaque skill ;
- le SHA-256 de chaque contexte chargé et la liste des sources du compagnon ;
- ces éléments dans `_provenance.json`, `_bilan.json` et l'en-tête de chaque
  réponse brute.

## Lecture des résultats

- `resultats/<campagne-id>/<id>.md` — la réponse du sous-agent vierge.
- `resultats/<campagne-id>/<id>-eval.json` — l'évaluation (statut par critère,
  erreurs, score).
- `resultats/<campagne-id>/_provenance.json` — empreinte reproductible des deux
  skills, du JSON des cas et de la campagne.
- `resultats/<campagne-id>/_bilan.json` — moyenne globale (inclut le `type` par
  cas) et résultat détaillé du gate strict.

## Gate de sortie de brouillon

La validation finale d'une version exige **deux campagnes distinctes** avec le
protocole outillé `prompt-claude-code.md` :

1. `integration` — 30 cas, avec `recherche-juridique` réellement chargé ;
2. `degraded` — 30 cas, sans compagnon, pour vérifier l'abstention.

Chaque campagne doit porter sur le même SHA propre du candidat et satisfaire
simultanément les conditions suivantes :

- 30 réponses et 30 jugements exploitables ;
- aucune erreur API/outillage, troncature ou sortie non parsable ;
- tous les critères `SATISFAIT` ;
- 30 verdicts globaux `REUSSITE` ;
- 30 verdicts de fiabilité juridique `REUSSITE` ;
- architecture `REUSSITE` pour chaque cas architectural et aucun verdict
  d'architecture `ECHEC` ;
- aucune erreur juridique, référence inventée ou référence suspecte non
  résolue après contrôle en source officielle.

Un échec impose une correction puis le rejeu complet du mode concerné sur le
nouveau SHA. Seuls les rapports qui satisfont ces critères sont copiés dans
`tests/rapports/` et versionnés. La sortie de brouillon intervient après la
publication des deux rapports et la réussite des contrôles déterministes.

## Étendre

Ajouter un cas = un objet dans `cas-de-test.json` (`id`, `branche`, `type`,
`prompt`, `attendus`, `echec_si`). Viser les comportements sensibles : données
volatiles, statuts particuliers, actes faisant grief, pièges de qualification.
Pour un cas adversarial, mettre `type: "echec_attendu"`, décrire dans
`attendus` le comportement de refus/abstention attendu, et lister dans
`echec_si` les comportements disqualifiants (répond normalement, invente,
transpose).
