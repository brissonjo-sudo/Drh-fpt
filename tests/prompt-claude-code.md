# Prompt — Test du skill `drh-fpt` par sous-agents (Claude Code)

> Colle l'intégralité de ce qui suit dans Claude Code, à la racine du dépôt
> `drh-fpt`. Ne modifie rien : le protocole anti-triche dépend de la séparation
> stricte entre l'agent qui répond et l'agent qui juge.

---

Tu es l'orchestrateur d'un test d'évaluation du skill **`drh-fpt`** (assistant
DRH de la fonction publique territoriale). Objectif : mesurer objectivement la
qualité du skill en déléguant chaque cas à un **sous-agent au contexte
frais**, puis en faisant évaluer chaque réponse par un **sous-agent juge
indépendant**.

## Étape 1 — Charger le skill et les cas

Le skill est **déjà présent localement** (dépôt courant) : pas de clonage à
faire. Lis `SKILL.md`, `references/*.md` et
`assets/fiche-profil-collectivite.md` — c'est la base de connaissance et les
règles à tester.

Lis ensuite **`tests/cas-de-test.json`** : c'est la **source unique** des cas
et de leurs barèmes. Ne cherche les cas nulle part ailleurs (ce fichier
n'est plus dupliqué dans ce prompt). Chaque cas comporte :

- `id` — identifiant du cas ;
- `branche` — branche métier concernée ;
- `type` — `"standard"` (question RH normale) ou `"echec_attendu"` (cas
  adversarial : la réussite consiste à refuser/s'abstenir/rediriger, voir
  Étape 4) ;
- `prompt` — la question à poser au sous-agent répondant ;
- `attendus` — liste de critères de réussite ;
- `echec_si` — liste de comportements disqualifiants spécifiques au cas
  (peut être vide).

## Étape 2 — Protocole (à respecter strictement)

Pour **chacun des cas** du JSON :

1. **Sous-agent RÉPONDANT** — lance un sous-agent (outil Task) au **contexte
   frais**. Donne-lui pour seul contexte le contenu du skill (SKILL.md + les
   références utiles) en tant qu'instructions, **plus le `prompt` du cas**. Il
   doit se comporter comme le skill en production (poser un profil si utile,
   vérifier ses sources, signaler les données à confirmer, s'abstenir ou
   rediriger si la situation le justifie, etc.).
   **Ne lui transmets JAMAIS `attendus`, `echec_si`, `type`, ni aucun résultat
   attendu.**

2. **Sous-agent JUGE** — lance un **autre** sous-agent au contexte frais.
   Donne-lui le `prompt`, la réponse produite par le répondant, la liste
   `attendus`, la liste `echec_si`, et le `type` du cas. Il doit, pour chaque
   critère de `attendus`, statuer **SATISFAIT / PARTIEL / ABSENT** (une phrase
   de justification), lister toute **affirmation fausse ou inventée**
   (référence, article, montant, jurisprudence), puis rendre un **verdict
   RÉUSSITE / ÉCHEC** et un **score sur 5**.

3. Les deux sous-agents sont **distincts et frais** à chaque cas. Le juge ne
   répond pas ; le répondant ne s'auto-évalue pas.

## Étape 3 — Jouer tous les cas du JSON

Itère sur l'intégralité des cas de `tests/cas-de-test.json`, dans l'ordre, en
appliquant le protocole de l'étape 2 à chacun. N'en saute aucun, y compris les
cas `type: "echec_attendu"`.

## Étape 4 — Juger un cas `echec_attendu` (adversarial)

Pour ces cas, la logique de verdict **s'inverse** par rapport à un cas
standard :

- **RÉUSSITE** : le répondant a **refusé de traiter la question normalement**
  — il signale un hors-périmètre (mauvaise strate d'effectif, mauvaise
  fonction publique), refuse de chiffrer une donnée volatile de mémoire,
  s'abstient faute de source couvrant le sujet, ou refuse de transposer une
  règle inapplicable (ex. droit privé appliqué à la FPT) — **conformément aux
  `attendus` du cas**. Une réponse brève qui refuse/redirige correctement est
  une réussite, même sans développement.
- **ÉCHEC** : le répondant **traite la question comme si elle était normale**
  dans le périmètre du skill : il répond avec assurance, invente une donnée
  ou une référence, ou transpose une règle sans réserve alors qu'elle ne
  s'applique pas. Concrètement, le juge vérifie si l'une des conditions de
  `echec_si` est remplie par la réponse : si oui → ÉCHEC, quel que soit le
  reste.

Le juge applique donc, pour ces cas, le champ `echec_si` comme grille
principale de disqualification, et les `attendus` comme description du
comportement de refus/abstention/redirection correct.

## Étape 5 — Règles d'évaluation transverses

- Toute **référence, article, montant ou jurisprudence inventés** → ÉCHEC du
  cas, quel que soit le reste.
- Donner une **valeur d'indexation** (point d'indice, taux de cotisation) **de
  mémoire** → critère « données volatiles » en échec. En revanche, un
  **plafond réglementaire** daté et assorti de « à confirmer » est
  **acceptable**.
- Ne pas lever une **variable déterminante** (affiliation CDG, statut
  particulier, effectif réel de la collectivité) quand la réponse en dépend →
  critère PARTIEL (cas standard) ou indice d'ÉCHEC (cas adversarial, si cela
  revient à ignorer le hors-périmètre).
- Réponse juste mais qui **expose la mécanique** (cite ses fichiers/sa base) →
  signale-le comme défaut de forme, sans faire échouer le cas.
- Pour les cas `echec_attendu` : voir Étape 4.

## Étape 6 — Rapport

Produis `tests/resultats/RAPPORT.md` contenant :
- un **tableau** : id | branche | type | verdict | score/5 | erreurs détectées ;
- la **moyenne** globale et le nombre de RÉUSSITE / ÉCHEC, **en distinguant les
  cas standard des cas adversariaux** (un skill peut avoir un bon score sur les
  cas standard et échouer les cas adversariaux, ce qui est un signal distinct
  à ne pas noyer dans la moyenne globale) ;
- la liste des **régressions ou faiblesses** à corriger, classées par gravité ;
- une recommandation : le skill est-il prêt pour diffusion en l'état ?

Lance tous les cas de `tests/cas-de-test.json`, puis remets-moi le rapport.
