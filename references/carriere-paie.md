# Branche — Carrière & paie

> Structure conforme à `_gabarit-branche.md`. Valeurs chiffrées : régime du
> socle §6 — indexations (point, cotisations) jamais de mémoire ; plafonds
> réglementaires citables si datés et « à confirmer en version consolidée ».

## 1. Périmètre

Gestion statutaire et financière de l'agent, de l'entrée à la sortie :
déroulement de carrière, positions, instances de carrière, discipline, et
rémunération (traitement et régime indemnitaire).

## 2. Questions couvertes

Avancement (échelon, grade), promotion interne, positions statutaires,
discipline, traitement indiciaire, régime indemnitaire (RIFSEEP / ISFE),
NBI, SFT, cotisations et affiliation retraite, temps de travail (durée
annuelle, cycles, astreintes, CET, congés), fin de fonctions (dont retraite
progressive), **emplois fonctionnels et fin de détachement dans l'intérêt du
service**, **grève et retenue sur traitement**, **chômage des agents publics
(auto-assurance)**.

## 3. Arbre de traitement

`question → variables à lever (§4) → décision → vérification (§7) → livrable (§10)`

Ne pas dérouler une réponse assertive tant que les variables déterminantes ne
sont pas levées.

## 4. Variables à lever

- **Affiliation au centre de gestion** (promotion interne, CAP : circuit propre
  si non affiliée — cas fréquent au-dessus de 350 agents).
- **Filière et cadre d'emplois** (conditionne la grille, l'éligibilité au
  régime indemnitaire, le décret statutaire applicable).
- **Statut de l'agent** : titulaire / stagiaire / contractuel ; temps complet /
  temps non complet / temps partiel.
- **Date de référence** (faits, jour, date d'effet de l'acte).

## 5. Règles métier — modules à charger selon le dossier

- Statut, carrière, instances et discipline : `references/carriere-paie/statut-discipline.md`.
- Traitement, régime indemnitaire, cotisations et retraite : `references/carriere-paie/remuneration-paie.md`.
- Temps de travail, abandon de poste, emplois fonctionnels, grève et fin de fonctions : `references/carriere-paie/temps-fin-fonctions.md`.

Lire plusieurs modules si le dossier les croise. Le fichier présent conserve les calculs, déclencheurs de vérification, pièges, livrables et contrôles communs.

## 6. Calculs

Pour tout calcul (traitement, ancienneté, reclassement, NBI, SFT, coût
employeur) :
- annoncer les **hypothèses** retenues ;
- **demander** les données manquantes (indice, quotité, situation familiale) ;
- distinguer **données connues** et **estimées** ;
- signaler les **valeurs volatiles** (§9) à confirmer et les **paramètres
  locaux** (délibération indemnitaire, régime du temps de travail) ;
- pour tout **calcul de régime indemnitaire** : d'abord **croiser filière et
  cadre d'emplois du grade concerné avec le régime** (RIFSEEP vs ISFE police
  municipale/gardes champêtres — cf. §5.7) **avant de nommer le régime**, sans le
  déduire du profil de l'interlocuteur.

Ne jamais produire un montant ferme sur une valeur de mémoire. **La vérification
de la source précède la réponse chiffrée — elle n'est jamais différée à une
relance de l'utilisateur** (SKILL.md §2.2).

## 7. Déclencheurs de vérification

Appliquer le noyau de vérification (matrice §2.2 du SKILL.md) dès que :
- un **calcul d'indice, de traitement ou indemnitaire** est demandé ;
- un **acte défavorable** est en jeu (refus d'avancement, de disponibilité,
  sanction) → base statutaire + **motivation** + **voies de recours** +
  vérifier l'obligation de **transmission au contrôle de légalité** ;
- une **délibération** est rédigée (RIFSEEP/ISFE, ratios) → vérifier le décret
  support, la parité et la délibération locale ;
- une **réforme récente** conditionne la réponse (ISFE, retraites, positions).

## 8. Pièges & confusions fréquentes

1. Citer une **valeur d'indexation de mémoire** (point, cotisation) → erreur de version. (Un plafond réglementaire daté reste, lui, citable sous réserve.)
2. Confondre **avancement d'échelon** (ancienneté) et **avancement de grade**
   (tableau + ratios).
3. Confondre **avancement de grade** (même cadre d'emplois) et **promotion
   interne** (changement de cadre d'emplois).
4. Croire la **CAP compétente** sur l'avancement (faux), **ou** oublier ses
   **saisines par l'agent** (révision CREP, refus divers).
5. Placer l'**exclusion ≤ 3 jours** au mauvais groupe : elle est au **1er
   groupe**, **sans** conseil de discipline.
6. Ajouter le **déplacement d'office** à l'échelle FPT ou proposer un
   **conseil de discipline de recours** supprimé.
7. Déclarer toutes les sanctions transmissibles au contrôle de légalité sans
   vérifier la version en vigueur de l'article L2131-2 du CGCT.
8. Appliquer le **RIFSEEP** à la **police municipale** (régime propre = ISFE).
9. Citer le **décret État 2014-513** comme source FPT directe (viser 91-875 +
   délibération).
10. Basculer à tort un agent à **temps partiel** vers l'IRCANTEC (il reste
   CNRACL).
11. Confondre **détachement** et **mise à disposition**.
12. Appliquer la règle du **trentième indivisible** (propre à l'**État**) à
     une retenue pour grève dans la **FPT** — la retenue FPT est
     **proportionnelle à la durée réelle** de l'absence de service fait.
13. **Décharger un emploi fonctionnel dans les 6 mois** suivant le plus
     tardif de la nomination de l'agent dans l'emploi ou de la désignation de
     l'autorité territoriale (protection d'ordre public, cause d'illégalité
     quasi automatique).
14. **Oublier le coût chômage** (auto-assurance) d'un non-renouvellement de
     contrat ou d'un licenciement — le décider sans avoir chiffré l'impact
     budgétaire de l'ARE à la charge de la collectivité.

## 9. Valeurs chiffrées (cf. socle §6)

- **Volatiles, jamais de mémoire** : valeur du point d'indice, minimum de
  traitement, grilles indiciaires, montant GIPA, taux de cotisation, barèmes
  d'astreinte/permanence, montants forfaitaires d'indemnisation du CET.
- **Réglementaires, citables si datées + « à confirmer en version consolidée »** :
  plafonds ISFE (33/32/30 % ; 9 500/7 000/5 000 €), plafonds RIFSEEP par groupe
  de fonctions, contingent IHTS (25 h), garanties minimales de temps de travail
  (décret 2000-815 : 10 h/jour, 48 h/semaine), plafond CET (60 jours) et seuil
  de monétisation (15 jours épargnés, décret 2004-878), durée de la protection
  des 6 mois des emplois fonctionnels et effet différé de la décharge (art.
  L. 544-1 CGFP), exclusion ARE de l'abandon de poste (décret 2020-741).
  Rappel : un taux plafond est stable, le montant en euros qui en découle
  dépend du point (volatile).
- **Registre de vérification interne (maintenance)** :
  `references/cache-plafonds-regime-indemnitaire.md` consigne les plafonds
  réglementaires déjà vérifiés (ISFE) et les gaps à combler (RIFSEEP attachés).
  C'est un **aide-mémoire de maintenance, jamais une source** : toujours
  reconfirmer la valeur en vigueur avant usage en acte, et **ne pas le citer**
  comme référence dans un livrable formel.

## 10. Livrables (classés par niveau)

1. **Décision** — arrêté individuel (avancement d'échelon/grade, mise en
   disponibilité, temps partiel, sanction). Acte faisant grief si défavorable :
   **motivation + voies de recours** + vérifier la transmission au contrôle de
   légalité.
2. **Organisation** — fiche de procédure (tableau d'avancement, campagne de
   promotion interne, procédure disciplinaire).
3. **Pilotage** — note au DGS/Maire sur une situation de carrière ;
   délibération RIFSEEP/ISFE ou ratios promus-promouvables.
4. **Communication** — courrier de réponse à une demande d'agent (disponibilité,
   temps partiel, mobilité).

Gabarits → `assets/`.

## 11. Niveau de confiance (repères de la branche)

- **Stable** : architecture des catégories/grades, mécanique
  échelon/grade/promotion, échelle des sanctions (CGFP L533) ; retenue de
  traitement FPT proportionnelle à la durée réelle de l'absence (≠ trentième
  indivisible État) ; nature non disciplinaire de la décharge de fonctions ;
  auto-assurance chômage obligatoire pour titulaires/stagiaires.
- **À vérifier** : toute valeur chiffrée ; plafonds RIFSEEP/ISFE ; règles de
  retraite (dont retraite progressive) ; rupture conventionnelle ; liste
  exacte des positions ; durée exacte de la protection des 6 mois et de
  l'effet différé des emplois fonctionnels ; périmètre du service minimum
  (art. 56 loi 2019-828) ; conditions du droit à l'ARE en cas d'abandon de
  poste au regard de la caractérisation retenue.
- **Débattu** : application du principe de parité selon les primes — éviter
  toute synthèse péremptoire, vérifier au cas par cas.

## 12. Checklist de branche

1. Statut (titulaire/contractuel) et quotité (temps complet / non complet /
   partiel) identifiés ?
2. Cadre d'emplois et **décret statutaire** repérés ?
3. Régime indemnitaire correct selon la filière (RIFSEEP vs **ISFE** PM vs SPP) ?
4. Affiliation CDG levée avant de décrire un circuit de promotion interne / CAP ?
5. Valeurs chiffrées vérifiées, jamais de mémoire ?
6. Si acte défavorable : motivation, voies de recours, transmission contrôle de
   légalité ?
7. Emploi fonctionnel : protection des 6 mois (nomination agent OU désignation
   autorité, le plus tardif), entretien préalable, information assemblée +
   CNFPT/CDG, effet différé tous vérifiés avant toute décharge ?
8. Fin de fonctions : impact budgétaire du chômage (auto-assurance) évalué et
   signalé au décideur ?
