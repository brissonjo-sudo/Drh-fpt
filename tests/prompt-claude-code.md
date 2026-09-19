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

## Étape 1 — Fixer le mode et enregistrer la provenance

Par défaut, exécute la campagne en **mode `integration`**. Le dépôt courant
contient `drh-fpt` ; le skill obligatoire `recherche-juridique >= 2.2.0` doit
être présent localement et réellement chargé par chaque répondant. Si son
chemin n'est pas fourni ou si son `SKILL.md` est introuvable, arrête la
campagne : ne simule pas sa présence. Accepte soit un dossier portant
directement `SKILL.md`, soit la structure actuelle du dépôt compagnon
`droit-francais-skill/skill/SKILL.md`.

Le mode `degraded` est une campagne séparée, explicitement demandée, qui teste
le filet de sécurité sans compagnon.

Avant tout sous-agent, crée un identifiant de campagne puis écris
`tests/resultats/<campagne-id>/_provenance.json` avec :

- identifiant de campagne et date UTC ;
- mode choisi ;
- modèle répondant et modèle juge ;
- chemin, version déclarée, SHA Git complet et état propre/sale de `drh-fpt` ;
- mêmes informations pour `recherche-juridique` en mode intégration ;
- liste des fichiers effectivement chargés par les répondants ;
- chemin et SHA-256 de `tests/cas-de-test.json`.

Le dépôt `drh-fpt` doit être propre. En mode intégration, le dépôt compagnon
doit l'être aussi. Si un état est sale, un SHA est absent ou le candidat ne se
déclare pas `v0.6.0`, arrête la campagne : sa provenance ne permettrait pas une
validation de release.

Lis ensuite `SKILL.md`, `references/*.md` et
`assets/fiche-profil-collectivite.md`. En mode intégration, lis aussi
intégralement le `SKILL.md` du compagnon et ses références requises.

Lis ensuite **`tests/cas-de-test.json`** : c'est la **source unique** des cas
et de leurs barèmes. Ne cherche les cas nulle part ailleurs (ce fichier
n'est plus dupliqué dans ce prompt). Chaque cas comporte :

- `id` — identifiant du cas ;
- `branche` — branche métier concernée ;
- `type` — `"standard"` (question RH normale), `"architectural"` (chaîne
  d'exécution transversale, jugée comme une réussite ordinaire) ou
  `"echec_attendu"` (cas adversarial : la réussite consiste à
  refuser/s'abstenir/rediriger, voir Étape 4) ;
- `prompt` — la question à poser au sous-agent répondant ;
- `attendus` — liste de critères de réussite ;
- `echec_si` — liste de comportements disqualifiants spécifiques au cas
  (peut être vide).
- `modes` — modes dans lesquels la variante est active ; si le champ est
  absent, le cas est actif dans les deux modes.

## Étape 2 — Protocole (à respecter strictement)

Pour **chacun des cas** du JSON :

1. **Sous-agent RÉPONDANT** — lance un sous-agent (outil Task) au **contexte
   frais**. En mode intégration, donne-lui pour contexte les deux skills
   réellement chargés : `drh-fpt` qualifie, décide et livre ;
   `recherche-juridique` vérifie les sources officielles. En mode dégradé,
   donne-lui `drh-fpt` et indique explicitement que le compagnon est
   indisponible. Ajoute uniquement le `prompt` du cas.
   **Ne lui transmets JAMAIS `attendus`, `echec_si`, `type`, ni aucun résultat
   attendu.**

2. **Sous-agent JUGE** — lance un **autre** sous-agent au contexte frais.
   Donne-lui le `prompt`, la réponse produite par le répondant, la liste
   `attendus`, la liste `echec_si`, et le `type` du cas. Il doit, pour chaque
   critère de `attendus`, statuer **SATISFAIT / PARTIEL / ABSENT** (une phrase
   de justification), lister toute **affirmation fausse ou inventée**
   (référence, article, montant, jurisprudence), puis rendre un **verdict
   RÉUSSITE / ÉCHEC** et un **score sur 5**. Il rend aussi deux évaluations
   distinctes : **architecture d'exécution** et **fiabilité juridique**. Une
   erreur juridique fait échouer le verdict global même si l'architecture est
   réussie. Donne également au juge le corpus des deux skills effectivement
   chargés. Il doit utiliser les outils de recherche disponibles pour vérifier
   en source primaire toute référence officielle produite par le répondant ;
   il consigne le lien ou l'identifiant récupéré dans son évaluation. Une
   référence impossible à contrôler reste « non tranchée » et empêche la
   validation de release.

3. Les deux sous-agents sont **distincts et frais** à chaque cas. Le juge ne
   répond pas ; le répondant ne s'auto-évalue pas.

## Étape 3 — Jouer tous les cas du JSON

Itère sur les cas de `tests/cas-de-test.json` actifs pour le mode choisi, dans
l'ordre, en appliquant le protocole de l'étape 2 à chacun. Un cas sans champ
`modes` est actif dans les deux modes. Une campagne normale comporte 30 cas :
ne mélange jamais les variantes `integration` et `degraded` dans le même bilan.

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
  cas, quel que soit le reste. La même règle s'applique à toute affirmation
  juridique fausse ajoutée dans un développement surnuméraire.
- Une référence récente ou postérieure à une date de cutoff n'est **jamais**
  réputée inventée pour ce seul motif : le juge la vérifie sur une source
  officielle ou signale l'impossibilité de trancher sans accuser de
  fabrication.
- Une mention « vérifié » ou « confirmé » sans lien ni identifiant officiel
  exploitable est une vérification non traçable. Elle ne sécurise pas une
  donnée exacte destinée à la paie, à un calcul ou à un acte.
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
- Pour les cas `architectural` : présenter séparément le verdict
  d'architecture et le verdict de fiabilité juridique. L'un ne compense pas
  l'autre.

## Étape 6 — Rapport

Produis `tests/resultats/<campagne-id>/RAPPORT.md` contenant :
- la provenance complète de la campagne, reprise de `_provenance.json` ;
- un **tableau** : id | branche | type | verdict architecture | verdict
  juridique | verdict global | score/5 | erreurs détectées ;
- la **moyenne** globale et le nombre de RÉUSSITE / ÉCHEC, **en distinguant les
  cas standard, architecturaux et adversariaux**, ainsi que les deux axes
  architecture / fiabilité juridique (un bon résultat sur un axe ne doit pas
  masquer un échec sur l'autre) ;
- la liste des **régressions ou faiblesses** à corriger, classées par gravité ;
- un inventaire des références officielles produites par les répondants avec,
  pour chacune, le lien ou l'identifiant primaire récupéré par le juge et le
  résultat du contrôle ;
- une recommandation : le skill est-il prêt pour diffusion en l'état ?

## Étape 7 — Gate de release et promotion du rapport

La campagne ne passe que si les conditions sont toutes réunies :

- exactement 30 réponses et 30 jugements exploitables ;
- aucune erreur d'outil/API, troncature ou sortie non parsable ;
- tous les critères sont `SATISFAIT` ;
- 30 verdicts globaux `REUSSITE` et 30 verdicts juridiques `REUSSITE` ;
- architecture `REUSSITE` pour chaque cas architectural et aucun verdict
  d'architecture `ECHEC` ;
- aucune erreur juridique, référence inventée ou référence suspecte non
  résolue après contrôle en source primaire.

Si une condition échoue, conserve les résultats bruts mais ne copie pas le
rapport dans `tests/rapports/`. Liste les correctifs nécessaires ; après toute
correction, le mode concerné doit être rejoué intégralement sur le nouveau SHA.

Si toutes les conditions passent, copie le rapport sans réécriture vers
`tests/rapports/RAPPORT-v0.6.0-<date>-<mode>.md`. Lance tous les cas actifs du
mode choisi, puis remets-moi le rapport et les réponses brutes sans les
réécrire.
