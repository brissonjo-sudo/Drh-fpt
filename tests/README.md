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
entre deux jeux de cas. Ce fichier contient actuellement **30 cas** :

- **20 cas `"standard"`** — questions RH représentatives des huit branches,
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
éventuellement vide — conditions disqualifiantes spécifiques au cas).

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
   reproductible : injecte le bundle en `system` et rejoue tous les cas du
   JSON (standard, architecturaux et adversariaux) ; le juge applique
   `echec_si` et, pour les cas adversariaux, inverse la logique de verdict
   (réussite = refus correct).
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
- `prompt-claude-code.md` — protocole sous-agents (renvoie à `cas-de-test.json`
  pour les cas et barèmes, ne les duplique plus).
- `cas-co-activation.md` — cas transverse deux skills + barème + variante
  dégradée (drh-fpt seul).
- `resultats/` — sorties brutes générées (non versionnées).
- `rapports/` — rapports de campagnes validés, datés (versionnés).

## Usage

```bash
export ANTHROPIC_API_KEY=sk-...
python tests/run_tests.py            # répond aux 30 cas (contexte vierge)
python tests/run_tests.py --judge    # répond + évalue (note sur 5 par cas)
```

Options : `--model` (répondant, défaut `claude-sonnet-4-6`), `--judge-model`
(juge, défaut `claude-opus-4-8`).

## Lecture des résultats

- `resultats/<id>.md` — la réponse du sous-agent vierge.
- `resultats/<id>-eval.json` — l'évaluation (statut par critère, erreurs, score).
- `resultats/_bilan.json` — moyenne globale (inclut le `type` par cas).

## Étendre

Ajouter un cas = un objet dans `cas-de-test.json` (`id`, `branche`, `type`,
`prompt`, `attendus`, `echec_si`). Viser les comportements sensibles : données
volatiles, statuts particuliers, actes faisant grief, pièges de qualification.
Pour un cas adversarial, mettre `type: "echec_attendu"`, décrire dans
`attendus` le comportement de refus/abstention attendu, et lister dans
`echec_si` les comportements disqualifiants (répond normalement, invente,
transpose).
