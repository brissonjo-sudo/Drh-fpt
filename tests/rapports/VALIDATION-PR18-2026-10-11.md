# Validation de la PR 18 — 11 octobre 2026

Chaque campagne d’intégration utilise des consultations officielles archivées antérieures à son lancement. Les cas sont fictifs et publics ; les réponses et jugements sont conservés sans correction manuelle.

## Résultats

| Série | Mode | Commit testé | Cas entièrement satisfaits | Gate strict |
|-------|------|--------------|---------------------------|-------------|
| Initiale | integration | `a83f031f9884965ae3afbe374ff925d3299ffe6d` | 9/30 | Échec |
| Initiale | degraded | `a83f031f9884965ae3afbe374ff925d3299ffe6d` | 10/30 | Échec |
| Deuxième | integration | `595d62e45f4400cedff1cf8696095cca8e3748a8` | 17/30 | Échec |
| Deuxième | degraded | `595d62e45f4400cedff1cf8696095cca8e3748a8` | 22/30 | Échec |
| Troisième | integration | `2dc44ac7ab75e195fc0d944d22c7f48d5e2d604e` | 20/30 | Échec |
| Troisième | degraded | `2dc44ac7ab75e195fc0d944d22c7f48d5e2d604e` | 28/30 | Échec |
| Quatrième | integration | `31060ec80ce68d1448525415acc42b7d4f0e833c` | 27/30 | Échec |
| Quatrième | degraded | `31060ec80ce68d1448525415acc42b7d4f0e833c` | 29/30 | Échec |
| Prévalidation isolée | degraded | `d8680d16237c96685582aa02b0d07cc25e15534d` | 30/30 | Réussite |
| Cinquième | integration | `c3e3a22aaa412efcd932af77e56b9b1bb9a30771` | 26/30 | Échec |
| Cinquième | degraded | `c3e3a22aaa412efcd932af77e56b9b1bb9a30771` | 30/30 | Réussite |
| Sixième | integration | `ee1c59f5d38ec6e1d937ec9b398e7dd367250609` | 28/30 | Échec |
| Sixième | degraded | `ee1c59f5d38ec6e1d937ec9b398e7dd367250609` | 30/30 | Réussite |
| Septième | integration | `2c8cedac367be14fcaa338782954ed4643c2924a` | 28/30 | Échec |
| Septième | degraded | `2c8cedac367be14fcaa338782954ed4643c2924a` | 29/30 | Échec |
| Huitième | integration | `29dbe0d1b934040f11c4d034397bc88f2e05abf8` | 29/30 | Échec |
| Huitième | degraded | `29dbe0d1b934040f11c4d034397bc88f2e05abf8` | 29/30 | Échec |
| Neuvième | integration | `1bee33a7a7f24735ab338979305d9f4cc7c42a42` | 29/30 | Échec |
| Neuvième | degraded | `1bee33a7a7f24735ab338979305d9f4cc7c42a42` | 29/30 | Échec |
| Dixième | integration | `5f8a531ceeb8785444656ebeca9bbdca09306d61` | 27/30 | Échec |
| Dixième | degraded | `5f8a531ceeb8785444656ebeca9bbdca09306d61` | 29/30 | Échec |
| Onzième | integration | `98b6766f29577d8da55be230129f31c14c392024` | 27/30 | Échec |
| Onzième | degraded | `98b6766f29577d8da55be230129f31c14c392024` | 30/30 | Réussite |
| Douzième | integration | `dd4bdd694e0e72de4f52fcf169b9db8d294189d8` | 29/30 | Échec |
| Douzième | degraded | `dd4bdd694e0e72de4f52fcf169b9db8d294189d8` | 29/30 | Échec |
| Treizième | integration | `d52d70af0ed8f4a656981b0749ec7a34bab69d26` | 29/30 | Échec |
| Treizième | degraded | `d52d70af0ed8f4a656981b0749ec7a34bab69d26` | 30/30 | Réussite |
| Quatorzième | integration | `e543b254fea3c1231b14a60338d9ea4de442bb1b` | 28/30 | Échec |
| Quatorzième | degraded | `e543b254fea3c1231b14a60338d9ea4de442bb1b` | 30/30 | Réussite |
| Quinzième | integration | `6505d7e79f3c134183a1d51f90bf2619a2e74043` | 28/30 | Échec |
| Quinzième | degraded | `6505d7e79f3c134183a1d51f90bf2619a2e74043` | 29/30 | Échec |
| Finale | integration | `cc1f56f6f7a18cdfb569e757795d717d7f206b79` | 30/30 | Réussite |
| Finale | degraded | `cc1f56f6f7a18cdfb569e757795d717d7f206b79` | 30/30 | Réussite |

## Protocole

- Répondant `gpt-6.1-sol`, juge distinct `gpt-6-sol` ; sessions Codex éphémères sans outils, réseau, fichiers ni mémoire.
- Effort `medium` dans la série initiale, `high` dans les suivantes. La variation ne mesure donc pas isolément les changements du skill.
- Intégration : compagnon public `recherche-juridique` v3.5.0 et consultations réelles. Dégradé : compagnon et consultations indisponibles, cadrage et abstention.
- 30 cas par mode, critères propres au mode. Tous les critères obligatoires doivent être SATISFAIT. PARTIEL, erreurs juridiques, troncatures, traces invalides et dépôt sale sont refusés.
- Les plafonds CLI sont indicatifs ; les traces établissent la complétude des tours. Aucun coût estimé sans tarif vérifié.
- 293 traces de sources et 40 archives finales couvrent 29 cas ; le cas FPH refuse le traitement hors périmètre et ne nécessite pas de conclusion de droit.
- 56 tests déterministes, bundle et cohérence réussis sur le commit de campagne. La mesure de contexte finale est archivée : réduction moyenne de 59.0 % des octets DRH (les sources et le compagnon sont supplémentaires).
- La prévalidation dégradée isolée porte sur un commit antérieur : elle est conservée et ne remplace aucune des deux campagnes finales.

## Corrections entre les séries

Modules manquants dans les dossiers mixtes, contrôles des variables et garanties, abstention dégradée, date d’effet en abandon de poste, dates CAP et ISFE, indemnité et recours du contractuel. Le juge respecte les équivalences, alternatives et conditions facultatives. Les critères incompatibles avec les sources ou le périmètre ont été corrigés explicitement.

Après la deuxième série : couverture visible des contrôles métier ; proportionnalité de la retenue pour grève (CE 303588, sans transposer la formule des gardes de sapeurs-pompiers) ; CGCT historique au 1er janvier 2004 visant les sanctions soumises à l’avis du conseil de discipline. Les traces historiques ont leur propre date de référence.

Les séries suivantes corrigent la portée des réponses ciblées et l’ordre des consignes : le contexte DRH et la restitution proportionnée restent prioritaires après les documents juridiques. Les sources complémentaires établissent les actes individuels de rémunération, les frais de protection fonctionnelle, les horloges de décharge, le recours gracieux et les régimes voisins des retenues pour grève.

Des critères erronés ont été corrigés après consultation et relecture indépendante : le régime transitoire des anciens recours disciplinaires dépend de la date de la sanction avant publication de la loi (article 94 XI de la loi 2019-828), et l’abandon de poste n’exige pas un silence absolu après mise en demeure (cas 17 puis 12). Les réponses, intentions et justificatifs doivent être examinés avec la non-reprise et le formalisme. Enfin, le cas 25 de la quatrième série a révélé une erreur juridique réelle sur la transmission d’un avancement de grade : le contrôle exige désormais une catégorie légale correspondant à la nature exacte de l’acte. Le dossier indemnitaire du contractuel est complété par les articles 46, 48 et 49 du décret 88-145. Les jugements anciens restent inchangés.

La septième série révèle deux omissions réelles : assistance juridique dans la protection fonctionnelle et accord collectif dans les pièces PSC. Le skill nomme désormais les composantes de la protection et réserve ses modalités à leur vérification ; la fiche PSC distingue participation et adhésion, demande l’accord ou son absence et contrôle ses clauses. Aucun critère ni gate n’est assoupli pour ces corrections.

La huitième série dégradée omet de nommer le tribunal administratif derrière une « juridiction compétente » à confirmer. Le contrôle conserve désormais cette institution comme piste à vérifier, limitée aux décisions administratives de la FPT, sans compétence, recevabilité ou délai certifiés. En intégration, le cas 28 désigne la formation plénière sans écarter explicitement la restreinte ; la restitution répond désormais aux deux termes de cette alternative. Le juge a aussi commis une faute de copie dans le libellé c01 : le contrôle strict rejette cette trace, conservée sans réparation manuelle. Critères, juge et gates restent inchangés.

Dans la neuvième série, une phrase dégradée sur la rupture du lien est ambiguë : son interprétation comme règle ferme est défendable, sans erreur de droit confirmée. Le skill rattache désormais les limites aux pièces et consultations manquantes, et transforme aussi les conditions/effets juridiques négatifs en contrôles. Pour le contractuel, les exceptions à la saisine de la CCP sont réservées séparément de l’ordre particulier de consultation.

La dixième série révèle un conflit de portée : la famille indemnitaire finale exigeait sans condition des éléments de mise en place, malgré une demande de plafonds seuls. Le contrôle est désormais scindé par objet ; une transition reste examinée si elle change la borne demandée. La communication distingue explicitement information et acte adopté ; le dégradé collecte les pièces de rémunération. Le fondement CGFP du cas 07 était fourni par son lien primaire exact : le reproche de numéro non visible est formel et discutable, sans source manquante. Un nouveau paquet conserve les 288 consultations et 39 archives brutes de round7, avec 272 numéros extraits de ces mêmes archives, sans nouvelle consultation ni modification des dates. Leur affichage est amélioré et leur intégrité est contrôlée lorsqu’ils sont présents ; les anciens paquets restent compatibles. Trois tests supplémentaires vérifient cette propriété. Critères, juge et seuils restent inchangés.

La onzième paire réussit en dégradé mais reste insuffisante en intégration : la recherche documentée et l’impossibilité de reclassement motivée étaient présentes, sans expliciter l’absence de garantie d’aboutissement ; une valeur vérifiée était datée et sourcée mais sans niveau de confiance. Pour le contractuel, le juge assimile le critère « fondement contractuel » au fondement légal de recrutement : reproche formel discutable, contrats et clauses déjà recherchés, sans erreur de droit confirmée. La qualification du recours inscrit au contrat, déjà prévue dans la fiche, est néanmoins rendue visible. Ces distinctions restent brèves, sans refaire un recrutement ni allonger les réponses ciblées. Aucun critère, juge ou seuil n’est changé.

La douzième paire relève un renvoi PSC pertinent absent des extraits fournis et une date d’ouverture de procédure seulement désignée par une formule générale en dégradé. Le paquet9 ajoute les articles1/3/4/6 du décret2022-581 à partir du même texte brut déjà consulté, sans modification des archives ou dates :292 traces et39 archives brutes. Les garanties prévoyance et le minimum santé sont ainsi documentés, sans confondre30€ de référence et15€ de participation, ni généraliser7€ ou50% en prévoyance hors du transitoire2025. Le renvoi littéral de l’article5 àL827-11 est conservé, malgré le changement du code ; le financement santé repose surL827-10 et l’article6. La collecte dégradée précise la date d’ouverture, sans lui attribuer un effet juridique non vérifié. Critères, juge et seuils sont inchangés.

La treizième paire réussit en dégradé ; en intégration, la protection est instruite par l’employeur mais la phrase sur les pièces établissant l’absence de faute reste ambiguë, sans erreur de droit certaine. Le critère18-c04 était trop absolu : seul refus pour faute personnelle, et écart d’office dans l’échec associé. La consultation réelle de [CE,7 juin2024,n°476196,§3](https://www.legifrance.gouv.fr/ceta/id/CETATEXT000049675953) confirme la dérogation d’intérêt général sous contrôle du juge. Critère/échec corrigés après relecture indépendante : instruction de la faute par l’employeur, pas de preuve générale d’absence exigée de l’agent, pas de motif de refus inventé ni de faculté discrétionnaire. Les pièces des attaques sont distinguées de cette qualification. Cette décision énonce le principe général codifié, sans règle autonome de charge de preuve ni transposition de modalités propres à la préfecture. Paquet10 : les292 traces précédentes conservées, plus cette nouvelle consultation, soit293 traces et40 archives ; dates antérieures inchangées. Le juge, les seuils et les anciennes traces ne sont pas modifiés.

La quatorzième paire réussit en dégradé mais reste à28/30 en intégration : le décret ISFE est identifié par numéro/fondement/liens mais sa date officielle manque, expressément requise par07-c01 ; incomplétude formelle confirmée sans erreur juridique. La règle transversale de première citation donne intitulé court, numéro et date vérifiés, sans répétitions ni références certifiées en dégradé. La décharge cite les options sans expliciter le retour sur emploi disponible du grade ni le CDG/CNFPT comme acteur de prise en charge. La restitution précise effet, condition et acteur des alternatives utiles ; L544-4/L544-12 et la décision Lyon2024 déjà consultés suffisent au cadrage, conditions détaillées réservées. Relecture indépendante ; aucune modification du paquet10, critères, juge ou seuils.

La quinzième paire relève des omissions de qualification confirmées par relecture indépendante, sans erreur juridique établie : le contrôle dégradé des LDG ne distingue pas explicitement la promotion interne ni la compétence des listes d’aptitude ; le maintien après PPR est distingué de sa prolongation, mais la limite de trois mois n’est citée que pour la procédure de reclassement. Fiche CST et contrôle LDG distinguent orientations locales/promotion interne, affiliation et compétence confiée. La restitution relie le maintien après PPR à la demande, à la prise d’effet et à la limite prévue par le renvoi à l’article 3, sans délai supplémentaire automatique. La réponse sur la transmission est juridiquement correcte mais omet la convention/pratique locale : contrôle documentaire bref rendu explicite pour les questions ciblées de transmission, sans présumer de convention ni créer une obligation légale. L413-6/R413-37 et l’article 2 du décret 85-1054 sont déjà consultés dans le paquet10 ; sources, critères, juge et seuils inchangés.

## Preuves et reproduction

[Archive complète](PREUVES-PR18-2026-10-11.zip) — SHA-256 `c4a5ba062c9befd912262c856fd159f9145654317953b7a72b1688bbe80b6022`.

Les 33 campagnes de 30 cas, y compris les échecs et la prévalidation isolée, sont conservées : réponses, JSONL originaux répondant et juge, bilans, critères de chaque commit, provenances, sources officielles compressées et gate commun. Les diagnostics partiels ne sont pas des campagnes de validation. Aucune clé PISTE ou API n’est incluse. Les archives brutes identiques sont stockées une fois dans sources-round10 ; rehydrate_sources.py les copie dans les anciens dossiers en contrôlant chaque empreinte.

Utiliser le harnais au commit testé indiqué au tableau, puis extraire l’archive. Les chemins absolus d’origine sont informatifs ; utiliser explicitement le dossier de sources pour la vérification portable :

```text
python -X utf8 <archive>/rehydrate_sources.py
python -X utf8 tests/release_gate.py --integration <archive>/20261011T194749Z-f151c110/evaluations/20261011T194749Z-codex-e754d1/_bilan.json --degraded <archive>/20261011T194747Z-ff778f66/evaluations/20261011T194747Z-codex-dc87aa/_bilan.json --expected-commit cc1f56f6f7a18cdfb569e757795d717d7f206b79 --evidence-file <archive>/sources-round10/evidence.json --output <rapport-gate.json>
```

La fraîcheur des sources est vérifiée à la date de la campagne. Une future réponse juridique impose une nouvelle consultation à la date utile.

Le commit de publication ajoute seulement les rapports, archives et documentation associée (README, journal et changelog). Les deux campagnes portent sur le même commit de code indiqué au tableau. Aucune fusion n’est effectuée.

La réussite est limitée à ces cas, modèles, réglages et corpus ; elle ne constitue pas une garantie universelle de réponse juridique correcte.
