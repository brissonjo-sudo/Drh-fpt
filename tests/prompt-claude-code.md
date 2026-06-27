# Prompt — Test du skill `drh-fpt` par sous-agents (Claude Code)

> Colle l'intégralité de ce qui suit dans Claude Code, à la racine d'un dossier
> de travail. Ne modifie rien : le protocole anti-triche dépend de la séparation
> stricte entre l'agent qui répond et l'agent qui juge.

---

Tu es l'orchestrateur d'un test d'évaluation du skill **`drh-fpt`** (assistant
DRH de la fonction publique territoriale). Objectif : mesurer objectivement la
qualité du skill en déléguant chaque question à un **sous-agent au contexte
frais**, puis en faisant évaluer chaque réponse par un **sous-agent juge
indépendant**.

## Étape 1 — Récupérer le skill

Clone le dépôt (ou réutilise-le s'il est déjà présent) :

```
git clone https://github.com/brissonjo-sudo/drh-fpt.git
```

Lis `drh-fpt/SKILL.md`, `drh-fpt/references/*.md` et
`drh-fpt/assets/fiche-profil-collectivite.md`. C'est la base de connaissance et
les règles à tester.

## Étape 2 — Protocole (à respecter strictement)

Pour **chacune des 10 questions** de l'étape 3 :

1. **Sous-agent RÉPONDANT** — lance un sous-agent (outil Task) au **contexte
   frais**. Donne-lui pour seul contexte le contenu du skill (SKILL.md + les
   références utiles) en tant qu'instructions, **plus la question**. Il doit se
   comporter comme le skill en production (poser un profil si utile, vérifier ses
   sources, signaler les données à confirmer, etc.).
   **Ne lui transmets JAMAIS les critères ni le résultat attendu.**

2. **Sous-agent JUGE** — lance un **autre** sous-agent au contexte frais. Donne-lui
   la question, la réponse produite par le répondant, et **les critères de cette
   question**. Il doit, pour chaque critère, statuer **SATISFAIT / PARTIEL /
   ABSENT** (une phrase de justification), lister toute **affirmation fausse ou
   inventée** (référence, article, montant, jurisprudence), puis rendre un
   **verdict RÉUSSITE / ÉCHEC** et un **score sur 5**.

3. Les deux sous-agents sont **distincts et frais** à chaque question. Le juge ne
   répond pas ; le répondant ne s'auto-évalue pas.

## Étape 3 — Les 10 questions et leurs critères

**Q1 — Régime indemnitaire police municipale.**
*« Commune > 350 agents. Je veux instaurer le régime indemnitaire de mes agents
de police municipale. Que puis-je verser et comment procéder ? »*
RÉUSSITE si : cite l'**ISFE** (décret n° 2024-614, art. L714-13 CGFP), deux
parts, **exclut explicitement le RIFSEEP**, mentionne la clause de sauvegarde et
la procédure (avis CST → délibération → arrêtés).
ÉCHEC si : applique le RIFSEEP à la police municipale, ou invente un texte.

**Q2 — Sanction : exclusion temporaire de 5 jours.**
*« Quelle procédure pour exclure temporairement un agent 5 jours ? »*
RÉUSSITE si : situe les 5 jours au **2e groupe**, **conseil de discipline
obligatoire**, droits de la défense (dossier, assistance), acte faisant grief
(motivation + voies de recours).
ÉCHEC si : place la sanction au 1er groupe, ou dit qu'aucun conseil de discipline
n'est requis.

**Q3 — Affiliation retraite et temps partiel.**
*« Un agent à temps partiel 80 % sur un poste à temps complet reste-t-il à la
CNRACL ? »*
RÉUSSITE si : **oui, reste à la CNRACL**, et distingue temps partiel (choix de
l'agent) du temps non complet < 28 h.
ÉCHEC si : le bascule à l'IRCANTEC.

**Q4 — Plafonds de l'ISFE (données chiffrées).**
*« Quels sont les plafonds de l'ISFE pour un directeur de police municipale ? »*
RÉUSSITE si : traite ces plafonds comme **réglementaires** — peut les citer (part
fixe 33 %, part variable 9 500 €) **en datant le décret 2024-614 et en signalant
« à confirmer en version consolidée »**, et précise que le montant en euros de la
part fixe dépend de la valeur du point ; OU renvoie au décret sans inventer.
ÉCHEC si : invente des chiffres, ou les donne sans aucune réserve de source.

**Q5 — Participation employeur complémentaire santé (PSC).**
*« Pour mon budget 2026 : quelle est mon obligation de participation à la
complémentaire santé, depuis quand, et l'adhésion des agents est-elle
obligatoire ? Et la prévoyance ? »*
RÉUSSITE si : santé **obligatoire depuis le 1er janvier 2026**, montant traité
comme à vérifier, **adhésion santé facultative**, prévoyance obligatoire depuis
2025 et **généralisation collective au 1er janvier 2029**.
ÉCHEC si : affirme que la santé n'est pas encore obligatoire, ou invente un
calendrier/montant.

**Q6 — Accident en service.**
*« Un agent titulaire se blesse en intervention. Quel congé, et qui décide de
l'imputabilité au service ? »*
RÉUSSITE si : **CITIS** / accident de service (pas maladie ordinaire),
imputabilité décidée par l'autorité territoriale (conseil médical selon les cas),
décision pouvant faire grief.
ÉCHEC si : traite en congé maladie ordinaire ou ignore l'imputabilité.

**Q7 — Recrutement d'un contractuel sur poste permanent.**
*« Puis-je recruter un contractuel sur un poste permanent vacant de catégorie B,
et à quelles conditions ? »*
RÉUSSITE si : exige un **fondement juridique précis** (CGFP, cas élargis par la
loi de 2019), mentionne la **déclaration de vacance** et la publicité, et signale
le fondement exact comme à vérifier.
ÉCHEC si : répond « oui, librement » sans fondement ni procédure.

**Q8 — Adoption des lignes directrices de gestion.**
*« Quelle instance consulter pour adopter mes LDG, et selon quelle procédure ? »*
RÉUSSITE si : LDG établies par l'autorité territoriale **après avis du CST**,
**pas la CAP**, portées à la connaissance des agents.
ÉCHEC si : désigne la CAP, ou omet l'avis préalable du CST.

**Q9 — Projection de masse salariale.**
*« Comment estimer l'évolution de ma masse salariale l'an prochain ? »*
RÉUSSITE si : distingue mesures générales (point) / catégorielles / individuelles,
cite **GVT positif, effet de noria, effet report**, applique une méthode (poser
les hypothèses, demander les données), et traite le point/les cotisations comme
**données volatiles à vérifier**.
ÉCHEC si : avance un chiffre ferme de mémoire, ou oublie noria/report.

**Q10 — Statut particulier (Ville de Paris).**
*« Je suis DRH à la Ville de Paris. Mes attachés relèvent-ils exactement du même
statut que dans une commune ordinaire ? »*
RÉUSSITE si : signale le **statut particulier** de la Ville de Paris / les **corps
propres des administrations parisiennes**, déclenche une **vigilance renforcée**,
et invite à vérifier les textes propres plutôt qu'appliquer le droit commun.
ÉCHEC si : applique le droit FPT commun sans la moindre réserve.

## Étape 4 — Règles d'évaluation transverses

- Toute **référence, article, montant ou jurisprudence inventés** → ÉCHEC du cas,
  quel que soit le reste.
- Donner une **valeur d'indexation** (point d'indice, taux de cotisation) **de
  mémoire** → critère « données volatiles » en échec. En revanche, un **plafond
  réglementaire** daté et assorti de « à confirmer » est **acceptable**.
- Ne pas lever une **variable déterminante** (affiliation CDG, statut particulier)
  quand la réponse en dépend → critère PARTIEL.
- Réponse juste mais qui **expose la mécanique** (cite ses fichiers/sa base) →
  signale-le comme défaut de forme, sans faire échouer le cas.

## Étape 5 — Rapport

Produis `tests/resultats/RAPPORT.md` contenant :
- un **tableau** : question | verdict | score/5 | erreurs détectées ;
- la **moyenne** globale et le nombre de RÉUSSITE / ÉCHEC ;
- la liste des **régressions ou faiblesses** à corriger, classées par gravité ;
- une recommandation : le skill est-il prêt pour diffusion en l'état ?

Lance les 10 cas, puis remets-moi le rapport.
