# PR18 — Dossier de validation des jeux A et B

**État : à relire par Jo. Aucun gel, aucun cas de qualification exécuté.**

## Décision attendue

Valider les 24 questions, leurs critères/échecs dans les deux modes et les quatre profils ci-dessous. Le plan approuvé exige cette validation concrète avant tout gel. Une remarque peut conduire à corriger le dossier avant son approbation.

Après accord : A est exécuté une fois sur chaque profil. Un changement après ouverture consomme A ; B reste la réserve, utilisable uniquement après échec de A. Un échec de B termine ce cycle sans qualification.

Seuil fixé avant lancement : 100 % des critères obligatoires, aucune erreur juridique confirmée. Jo arbitre les jugements contestés avec motifs et sources ; un doute non tranché bloque. Le style est indicatif. Les scores bruts et décisions humaines restent séparés.

## Profils proposés

| Répondant | Juge | Modes | Contexte |
|---|---|---|---|
| Codex `gpt-6.1-sol`, high | Claude `claude-sonnet-4-6`, high | intégration + dégradé | assemblage sélectif |
| Claude Code `claude-opus-4-8`, high | Codex `gpt-6.1-sol`, high | intégration + dégradé | activation native des skills |

Versions exactes : Codex `codex-cli 0.162.0-alpha.17.2` ; Claude `2.1.277 (Claude Code)`. [Configuration complète](profiles-v1.json). Aucun remplacement silencieux.

En intégration native, les deux skills sont demandés explicitement et les documents officiels sont préconsultés. Tous les fragments et fichiers obligatoires doivent être effectivement reçus intégralement. Cela ne teste ni la recherche autonome via le serveur juridique ni la co-activation automatique sans demande explicite.

En dégradé : pas de compagnon ni de source. Les faits fournis restent utilisables ; les règles, compétences, durées, plafonds et procédures ne peuvent être certifiés, même avec réserve. Une réponse doit préparer utilement la vérification et la décision conditionnelle.

## Sources et limites

[Archive des sources](../rapports/SOURCES-JEUX-PR18-2026-10-12.zip) : 234 liaisons de preuve aux cas, 19 archives brutes. Ces nombres décrivent l'archive historique du 12/10 ; le PDF RGPD du 14/10 et ses index sont ajoutés séparément, sans réécrire cette archive. Il ne s’agit pas de 234 appels réseau : des passages sont réutilisés entre cas. Dates de consultation originales conservées ; certains horodatages récupérés de l’écriture de l’archive sont signalés comme tels.

Selon le complément du rapport de Claude du 14/10/2026 : dispositif du RGPD lu dans le PDF EUR-Lex `CELEX:02016R0679-20160504` (sans considérants) ; articles 6, 8 et 10-1 de la loi 2016-1691 et réserves CGFP examinés via Légifrance ; deux décisions CE lues intégralement sur Ariane Web. Cette provenance est celle du rapport, pas une nouvelle consultation primaire par Codex. Les archives du 12/10 restent historiques et n'acquièrent pas rétroactivement les nouveaux textes. Les pièces locales absentes restent à rechercher ; les critères permettent une suspension ciblée.

Restent non vérifiés selon ce complément : considérants RGPD 26, 43, 51, lignes directrices CEPD/CNIL et pages CNIL (503 rapporté), partie réglementaire du CGFP sur l'affichage syndical, articles 12 à 13-1 de la loi 2016-1691.

Les références historiques du skill non réellement relues restent réservées. La validation de cette PR ne constitue pas une validation juridique humaine d’un déploiement opérationnel dans une collectivité (ADR0007 du plugin).

## Provenance et coût de validation

Scénarios conçus par Claude Sonnet en sessions fraîches, relus par Codex avec sources primaires, puis corrigés par Claude Opus. Aucune ancienne réponse, ancien score ou ancien barème fourni aux auteurs/relecteurs ; anciens prompts fournis seulement pour contrôler la nouveauté. Aucune réponse aux jeux neufs calibrée. Les originaux, échecs techniques et empreintes sont conservés.

Chaque jeu couvre les huit branches principales (cas 01–08) et quatre transversaux (09–12). Une normalisation ajoute le routeur commun avant les sous-modules ; cinq listes correctives partielles sont appliquées par ID en conservant les critères non cités. Les clauses dégradées identiques sont dédupliquées. Les deux derniers gaps documentaires de B ont été clos par ajout des passages primaires L522-23, R253-7, L221-2 et L223-1 réellement lus.

Cycle A : 48 réponses de qualification et 48 jugements, puis 28 réponses/28 jugements de non-régression ciblée, soit 76+76. La réserve ajoute 48+48. Rédaction, relectures, diagnostics et arbitrages sont comptés à part ; aucun coût monétaire déduit des jetons.

## Corrections et complément du 14 octobre 2026

Premier lot publié : cinq corrections dans `206e428`, puis nuances N1 à N6 dans `f21bec6` ; N7 est conservée. Second lot préparé depuis `f21bec6` puis publié sur `209e1d5` après validation T68 et CI verte. La présente réconciliation RGPD est préparée localement depuis `209e1d5`, sans poussée ni gel. Aucune approbation globale des 24 cas et aucune campagne exécutée.

**A-03 — correction prioritaire** : L332-8 renvoie aux formalités de L313-1 (création de l'emploi par délibération, mention de la possibilité de recruter un contractuel) ; la publicité de la vacance relève de L313-4, auquel renvoie L332-14. L313-1 ne doit plus être présenté comme un texte de publicité. Sa lecture est désormais rapportée par le complément ; les archives de sources du 12/10 ne sont pas modifiées.

Les corrections du tableau RGPD sont répercutées dans A-06-i03/i04, B-05-i02, B-06-i01/i02, B-09-i02 et B-11-i01/i03. B-09-i01 précise les conditions de l'art. 6 I et la voie interne ouverte aux candidats par l'art. 8 I-A 1° de la loi 2016-1691. B-12-i02 reste conforme à N6. L123-7 reste distinct du régime de L123-5 ; L553-3 ne sert pas de texte de procédure (seule l'indemnité éventuelle est visée selon le complément).

**CE 461914 — réserve « résumé web » levée selon le complément** : point 19 lu en texte intégral sur Ariane Web ; décision du 13/07/2022 **inédite**. Le constat concerne le congé de maladie et l'action disciplinaire ; le point ne traite ni du CLM en particulier ni des droits de la défense pendant l'arrêt. Aucun nouveau contrôle primaire indépendant par Codex.

CE, Section, 22/12/2023, n°462455, Lebon : texte intégral lu sur Ariane Web selon le complément ; points 4 et 5 décrits comme motifs décisoires. « Contenu utile à préserver » est une inférence ; la transposition d'un agent de l'État après sanction à une enquête préalable de collectivité est signalée, sans la présenter comme une identité de situations.

### Deux abstentions à conserver

- **Communication syndicale — B-06-i03** : aucun article d'affichage ou de diffusion trouvé dans L213, L214 et L215 de la partie législative du CGFP, selon le complément. Partie réglementaire non lue. Abstention sur la base précise du régime : l'absence de résultat ne signifie pas absence de règle.
- **Rattachement nominatif du SFT — B-08-i02** : L711-5 rend applicable le code du travail ; L3252-3 vise notamment les allocations ou indemnités pour charges de famille, mais **ne nomme pas le SFT**. Le rattachement nominatif du SFT est une **inférence** ; abstention sur toute présentation d'une exclusion nominative explicitement écrite dans ces textes.

### Identifiants, preuves et portée des contrôles

Les identifiants du complément sont ajoutés seulement aux cas qui les visent : L123-7 pour A-01 ; L711-5 pour B-08 ; loi 2016-1691 art. 6, 8 et 10-1 pour B-09/B-12 ; CELEX du dispositif RGPD pour A-06/B-05/B-06/B-09/B-11. L135-4 est déjà présent ; L553-3 n'est pas ajouté puisqu'aucun attendu ne vise son indemnité. Les suffixes abrégés sont développés avec le préfixe LEGIARTI, sans nouveau numéro de mémoire.

Réconciliation RGPD préparée le 14/10/2026 : les 14 liaisons vers les reproductions CNIL des chapitres 2/3/4 sont remplacées, dans les cinq cas A-06/B-05/B-06/B-09/B-11, par l'identifiant déjà présent `CELEX:02016R0679-20160504`, relié au PDF consolidé EUR-Lex archivé ci-dessous. Les recommandations CNIL non vérifiées restent une réserve distincte. Aucun attendu, critère d'échec, profil ou seuil n'est modifié par cette réconciliation.

Les scénarios, profils, modes dégradés et seuils restent inchangés. Toutes les empreintes A/B ci-dessous portent sur les octets bruts, comme `suites.file_sha`, et sont vérifiées par recalcul. Les ZIP T29 restent présents et inchangés ; leur traitement reste soumis à validation séparée avant la fusion. Les profils et le commit de runtime final doivent être approuvés explicitement avant tout gel.

### PDF RGPD — archive documentaire du 14 octobre 2026

**État : prêt pour la relecture de Jo avant gel**, sur les fichiers et réserves explicités ici. Ce statut ne vaut ni approbation globale des 24 cas ni gel ni autorisation de campagne.

Source RGPD à relire : [PDF consolidé EUR-Lex archivé](../rapports/rgpd-2026-10-14/CELEX-02016R0679-20160504-FR-consulte-2026-10-14.pdf) ; identifiant requis `CELEX:02016R0679-20160504` ; [provenance et empreinte](../rapports/rgpd-2026-10-14/provenance.json), [articles et pages par cas](../rapports/rgpd-2026-10-14/articles-rgpd.json).

- PDF français de 78 pages, en-tête `02016R0679 — FR — 04.05.2016 — 000.002`, dispositif avec rectificatif cité dans le document. Les 99 articles sont identifiés ; 17 articles utiles sont extraits sans modification et indexés par pages pour les cinq cas. Les extraits facilitent la relecture ; le PDF reste la pièce primaire conservée.
- SHA-256 brut du PDF : `e5984442f70f842034f9b5cb39bf3d6137630252260830c07b0449f354faa718` ; taille : 662538 octets. Copie identique au fichier local retrouvé et à l'extraction textuelle locale, après normalisation des espaces pour cette dernière comparaison.
- Consultation le **14/10/2026** : date rapportée par le complément de Claude. L'heure exacte n'est pas disponible. L'horodatage du fichier local est enregistré séparément ; il ne devient pas une heure de consultation certifiée. L'archivage de cette copie est daté au moment réel de la copie dans `provenance.json`.
- Une récupération directe EUR-Lex tentée pendant cette reprise a renvoyé une page de contrôle navigateur/HTTP 202, pas un PDF. La copie locale préexistante a été conservée sans altération. Son identité est cohérente avec le rapport et ses textes ; l'attribution à la consultation de Claude reste une inférence de provenance, sans hash de téléchargement original ni signature d'identité.
- Les anciennes archives ZIP demeurent historiques et intactes. Le présent PDF et ses JSON sont ajoutés séparément parmi les preuves ; T29 reste distincte et reportée à la préparation de la fusion.
- Les considérants, recommandations CEPD/CNIL et autres réserves du complément ne sont pas validés par cet archivage. Les deux abstentions communication syndicale/SFT sont conservées.
- **Limite d'exécution** : `provenance.json` et `articles-rgpd.json` sont des preuves documentaires pour la relecture. Le harnais `live_sources.verify_trace` ne reconnaît actuellement pas une archive PDF/CELEX en tant que trace de qualification. Ce tour ne modifie pas le harnais et ne fabrique pas de trace compatible ; cette prise en charge et l'ensemble des autres sources seront à préparer avant de fixer le runtime de campagne. Aucun gel n'est exécuté.

### Contrôles déterministes locaux du 14 octobre 2026

Python 3.13 / Windows : `python -m unittest discover -s tests -p 'test_*.py'` réussit **125/125 tests en cp1252**, puis **125/125 en UTF-8**, sans échec ni test ignoré. Ce sont les mêmes 125 tests exécutés dans deux environnements d’encodage, pas 250 tests distincts. Aucun cas de qualification ni appel modèle lancé.

`python scripts/check_coherence.py` et `python scripts/build_bundle.py --check` réussissent dans les deux environnements. Avertissement conservé : tag `v0.7.0` absent, donc contrôle de l’incrément de version du noyau ignoré. Le contrôle de cohérence force lui-même sa sortie UTF-8 ; le bundle est identique aux sources, sans régénération ni nouveau ZIP. Les empreintes des deux JSON sont recalculées après écriture puis comparées à `suites.file_sha` et aux valeurs ci-dessous.

## Empreintes exactes

- Jeu A : `9f4047721a26b7f4d6ff210e3c4165b3bf6d72ac1baa433b95014cd514150b9c`
- Jeu B : `1f1776debc25b33a73249d425a43150900a5855d5df3680e013dd8d61d238833`
- Profils : `315f90c12e52c28434dc7cbdc4262fa0abacee5d1733eb63c260d05be3645665`
- Archive primaire : `467bd64c3537f98e0793412f581aef496520edb3767a40736118f7a0666eb090`

Le commit exact est joint à la demande d’approbation après publication du candidat propre. Aucun sceau humain n’est créé à ce stade.

## Jeu A — actif

### A-01 — Cumul d’activités

**Question**

Un agent territorial titulaire occupe un emploi permanent à temps non complet (quotité 60 %) dans une collectivité de 400 agents. Il déclare à son autorité territoriale qu'il exerce, en dehors de ses heures de service, une activité de consultant indépendant à titre lucratif. L'autorité territoriale s'interroge sur la légalité de cette situation et sur les conditions dans lesquelles elle peut s'y opposer. Date : 12 octobre 2026. Produire une note d'analyse sur le cadre applicable et une décision motivée sur l'opposition ou l'autorisation.

**Critères obligatoires — intégration**

- **A-01-i01** : L123-5 est identifié comme base de la dérogation : un agent occupant un emploi permanent à temps non complet avec une durée ≤70 % de la durée légale peut exercer une activité privée lucrative ; la compatibilité avec l'interdiction générale de L123-1 est explicitée.
- **A-01-i02** : L'obligation déclarative (L123-6, R123-6) est distinguée de l'autorisation préalable : la déclaration porte sur l'activité envisagée. Son caractère préalable est explicité comme une déduction de R123-6, sans exiger que le texte utilise ce mot.
- **A-01-i03** : Les trois motifs d'opposition de l'autorité territoriale (R123-2 : intérêt du service, informations inexactes, incompatibilité déontologique) sont identifiés et appliqués aux faits ; les motifs sont confrontés aux faits disponibles ; la réponse distingue absence de motif établi et compatibilité démontrée. Elle fournit une position motivée sur les éléments acquis et, si nécessaire, un projet conditionnel en précisant les seules informations manquantes. Elle ne transforme pas le régime déclaratif en autorisation préalable.

**Échecs — intégration**

- L123-5 n'est pas identifié ou le régime de l'activité accessoire autorisée (L123-7) est appliqué à la place.
- L'obligation déclarative est présentée comme une obligation d'autorisation préalable.
- Les motifs d'opposition (R123-2) ne sont pas distingués ou un motif non prévu est certifié.
- Aucune décision motivée n'est produite.

**Critères obligatoires — dégradé**

- **A-01-d01** : La quotité de 60 % est prise comme acquise ; les informations manquantes sont listées : fonctions exercées par l'agent, nature et compatibilité de l'activité avec les fonctions, existence d'un conflit d'intérêts ou d'un lien avec les missions.
- **A-01-d02** : Aucune règle juridique n'est certifiée : le cadre est présenté sous forme de questions à instruire (régime applicable, obligation déclarative ou d'autorisation, motifs d'opposition) sans conclure sur la licéité.
- **A-01-d03** : Un projet de décision conditionnel est proposé avec champs à compléter ; toute certification non vérifiée est un échec.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable, même avec une réserve ; les faits fournis et les références posées comme pistes de recherche restent admis.
- Les informations manquantes sur les fonctions exercées et la nature de l'activité ne sont pas identifiées.
- Aucun projet de décision conditionnel n'est proposé.

**Sources annoncées et réserves**

- CGFP L123-5 et L123-6 — Conditions du cumul pour emploi permanent à temps non complet ≤70 %, obligation déclarative (consulte_dans_dossier).
- CGFP R123-5 et R123-6 — Modalités de la déclaration, information de l'agent (consulte_dans_dossier).
- CGFP R123-2 — Motifs d'opposition au cumul par l'autorité hiérarchique (consulte_dans_dossier).
- CGFP L123-7 — Activité accessoire autorisée : régime distinct de L123-5 ; référence utilisée par le critère d'échec (verifie_selon_complement_2026-10-14).
- Dossier réellement fourni : [Code général de la fonction publique](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000046933345), passages L123-1, L123-5, L123-6, R123-1, R123-2, R123-5, R123-6.

Liste exhaustive des identifiants et critères : [jeuAJSON](cases-a.json).

### A-02 — Reprise en TPT

**Question**

Un agent territorial titulaire est en congé de longue maladie depuis 18 mois dans une collectivité de 400 agents. Son médecin traitant préconise une reprise à temps partiel thérapeutique à 80 % ; un médecin agréé a rendu un avis favorable. La DRH doit organiser la reprise : qui prend la décision d'autorisation, dans quel délai, quel maintien de rémunération s'applique, et dans quels cas le conseil médical intervient-il ? Date : 12 octobre 2026. Produire une note de procédure interne.

**Critères obligatoires — intégration**

- **A-02-i01** : La décision d'autorisation appartient à l'autorité territoriale (art. 13-2 décret 87-602 vérifié) ; le médecin agréé peut être sollicité à l'initiative de l'employeur mais ne prend pas la décision ; le conseil médical intervient en cas de contestation d'un avis médical (art. 13-5 vérifié) ou dans les cas listés art. 5 I (réintégration après expiration des droits, fonctions à conditions de santé particulières, application art. 24) ; ces hypothèses sont distinguées des faits du cas.
- **A-02-i02** : Le maintien de l'intégralité du traitement, du SFT et de l'indemnité de résidence est fondé sur CGFP L823-4 vérifié ; les éléments non couverts (primes, régime indemnitaire) sont identifiés comme nécessitant vérification séparée.
- **A-02-i03** : Le délai de décision après CLM (au plus tard au jour de la reprise, art. 13-2 I décret 87-602 vérifié) est précisé ; l'information obligatoire du médecin de prévention (art. 13-8 vérifié) est mentionnée.

**Échecs — intégration**

- Le conseil médical est présenté comme l'instance qui autorise le TPT.
- Le maintien de rémunération est avancé sans base vérifiée ou une valeur différente de l'intégralité est certifiée.
- Le délai applicable après CLM (art. 13-2 I) est ignoré.
- Les cas d'intervention du conseil médical (contestation art. 13-5 vs hypothèses art. 5 I) ne sont pas distingués.

**Critères obligatoires — dégradé**

- **A-02-d01** : Les variables bloquantes sont identifiées : certificat médical transmis avec quotité/durée/modalités prescrites, avis du médecin agréé formalisé, existence de fonctions à conditions de santé particulières, situation vis-à-vis de l'art. 24 du décret.
- **A-02-d02** : Sans source, aucune procédure juridique n'est certifiée, même avec réserve : compétences, délais et rôle du conseil médical sont présentés comme des points à vérifier avant tout engagement.
- **A-02-d03** : Une organisation de reprise conditionnelle est proposée ; les points non vérifiés (primes, rôle éventuel de la médecine préventive à rechercher) sont explicitement signalés comme à confirmer.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable, même avec une réserve ; les faits fournis et les références posées comme pistes de recherche restent admis.
- Les variables manquantes (certificat médical transmis, avis agréé formalisé, existence de fonctions à conditions de santé particulières, situation vis-à-vis de l'art. 24) ne sont pas identifiées.
- Aucune structure conditionnelle n'est proposée.

**Sources annoncées et réserves**

- CGFP L823-1, L823-2, L823-4, L823-6 — Conditions, rémunération et renouvellement du TPT (articles reproduits au dossier) (consulte_dans_dossier).
- Décret n°87-602, art. 13-1, 13-2, 13-5, 13-8 — Procédure d'autorisation TPT après CLM, délais, médecin agréé, contestation, médecin de prévention (consulte_dans_dossier).
- Décret n°87-602, art. 5 I 3° et 4° et II 2° — Cas de consultation du conseil médical : réintégration, fonctions à conditions particulières, contestation d'avis médical (consulte_dans_dossier).
- Texte régissant le régime indemnitaire (RIFSEEP) pendant le TPT — Maintien ou suspension des primes pendant le TPT (a_consulter).
- Dossier réellement fourni : [Code général de la fonction publique](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044424529), passages L823-1, L823-2, L823-4, L823-6.
- Dossier réellement fourni : [Décret n°87-602 du 30 juillet 1987 relatif à l'organisation des conseils médicaux, aux conditions d'aptitude physique et au régime des congés de maladie des fonctionnaires territoriaux](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000054641701), passages 5, 13-1, 13-2, 13-5, 13-8, 13-13, 24.

Liste exhaustive des identifiants et critères : [jeuAJSON](cases-a.json).

### A-03 — Choix du contrat

**Question**

Une commune de 600 agents doit pourvoir un emploi permanent vacant de responsable de la cybersécurité (catégorie A). La vacance a été publiée il y a quatre mois ; la procédure de recrutement d'un fonctionnaire n'a pas abouti, comme documenté par le service RH. La direction hésite entre L332-8 2° (recrutement contractuel permanent) et L332-14 (vacance temporaire dans l'attente d'un fonctionnaire). La recherche d'un fonctionnaire se poursuit. Date : 12 octobre 2026. Produire une note d'aide à la décision comparant les deux fondements et recommandant le choix.

**Critères obligatoires — intégration**

- **A-03-i01** : La distinction est explicitée avec bases vérifiées : L332-8 2° exige une justification par les besoins ou la nature des fonctions ET un constat d'infructuosité documenté (R332-9 : examen des non-fonctionnaires uniquement après ce constat) ; L332-14 s'applique à la vacance temporaire dans l'attente d'un fonctionnaire, avec condition de publicité L313-4 ; les critères de choix reposent sur l'arbitrage entre une occupation contractuelle durable justifiée par les besoins ou la nature des fonctions et une occupation temporaire dans l'attente d'un fonctionnaire, sans rendre ces démarches légalement exclusives.
- **A-03-i02** : Les durées maximales sont précisées avec bases vérifiées : L332-9 (3 ans renouvelable jusqu'à 6 ans, reconduction expresse pour CDI au-delà, conditions de décompte L332-10) pour L332-8 2° ; L332-14 (1 an, prolongeable jusqu'à 2 ans si procédure fonctionnaire demeurée infructueuse) ; la prolongation de L332-14 est conditionnée à l'échec avéré du recrutement.
- **A-03-i03** : Les pièces nécessaires pour chaque fondement sont distinguées : publicité applicable ; constat préalable requis pour L332-8 2° ; pour L332-14, attente d'un fonctionnaire et justification de l'échec de son recrutement en cas de prolongation ; pour L332-8 2°, justification des besoins ou nature des fonctions ; mentions contractuelles utilisant les dispositions fournies (R331-6 à R331-11) : fondement légal du contrat et, pour L332-14, motif précis et descriptif du poste annexé, sans exiger une énumération exhaustive des clauses.

**Échecs — intégration**

- La distinction entre L332-8 2° et L332-14 n'est pas opérée ou un seul fondement est traité.
- Le constat d'infructuosité documenté (R332-9) est omis.
- Les durées maximales et la condition de prolongation de L332-14 sont ignorées.
- Les mentions contractuelles obligatoires sont certifiées sans source vérifiée.

**Critères obligatoires — dégradé**

- **A-03-d01** : La poursuite de la recherche d'un fonctionnaire et l'infructuosité documentée sont prises comme acquises ; leurs pièces sont demandées pour la seule traçabilité. Les informations manquantes sont identifiées : justification des besoins ou de la nature des fonctions, durée prévisible du besoin.
- **A-03-d02** : Sans source, aucun régime légal n'est certifié : les deux fondements sont présentés comme des scénarios à instruire, conditions et durées posées comme points à vérifier.
- **A-03-d03** : Une note conditionnelle est produite listant les pièces à réunir selon le scénario retenu, avec indication explicite des points à confirmer avant signature.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable, même avec une réserve ; les faits fournis et les références posées comme pistes de recherche restent admis.
- Les informations manquantes (justification des besoins ou de la nature des fonctions, durée prévisible du besoin) ne sont pas identifiées.
- Aucun livrable conditionnel distinguant les deux scénarios n'est proposé.

**Sources annoncées et réserves**

- CGFP L332-8 2°, L332-9, L332-10 — Conditions du recrutement permanent, renvoi de L332-8 à L313-1, durée, renouvellement, CDIsation et décompte des services (consulte_dans_dossier).
- CGFP L332-14 — Vacance temporaire, renvoi de L332-14 à L313-4, durée 1 an prolongeable 2 ans si procédure infructueuse (consulte_dans_dossier).
- CGFP R332-9 — Constat d'infructuosité préalable à l'examen des candidatures non fonctionnaires (consulte_dans_dossier).
- CGFP L313-1 et L313-4 (renvois respectifs de L332-8 et L332-14) — L332-8 renvoie aux formalités de L313-1 (création de l'emploi par délibération, mention de la possibilité de recruter un contractuel) ; la publicité de la vacance relève de L313-4, auquel renvoie L332-14 (verifie_selon_complement_2026-10-14).
- CGFP R331-6 à R331-11 — Fondement légal du contrat, motif précis et descriptif du poste annexé pour L332-14 (consulte_dans_dossier).
- Dossier réellement fourni : [Code général de la fonction publique](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000048778058), passages L332-8, L332-9, L332-10, L332-14, L313-4, R332-9, R332-10, R332-11, R332-12, R332-13, R331-1, R331-2, R331-3, R331-4, R331-5, R331-6, R331-7, R331-8, R331-9, R331-10, R331-11, R331-12, R331-13.
- Dossier réellement fourni : [Décret n°88-145 du 15 février 1988 relatif aux agents contractuels de la fonction publique territoriale](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051980613), passages 1.

Liste exhaustive des identifiants et critères : [jeuAJSON](cases-a.json).

### A-04 — Second examen du CST

**Question**

Le CST d'une collectivité de 800 agents est consulté sur le projet de délibération fixant le taux de promotion au grade d'attaché principal pour l'année N (question relevant de R253-7 12° et dont la mise en œuvre nécessite une délibération de l'organe délibérant). Les représentants du personnel émettent un vote unanime défavorable. Le DGS s'interroge sur les suites obligatoires et sur les conditions du second examen. Date : 12 octobre 2026. Produire un plan de procédure précisant les étapes obligatoires, les délais et les règles de quorum applicables au second examen.

**Critères obligatoires — intégration**

- **A-04-i01** : La procédure de réexamen obligatoire est fondée sur R254-68 vérifié : la question fait l'objet d'un réexamen ; une nouvelle délibération est organisée dans un délai entre 8 et 30 jours ; la nouvelle convocation est adressée dans un délai d'au moins 8 jours à compter de la première séance.
- **A-04-i02** : Les règles du second examen sont précisées à partir de R254-68, sans imposer un numéro d'alinéa non vérifiable : le comité siège valablement quel que soit le nombre de représentants du personnel présents et ne peut être appelé à délibérer une nouvelle fois selon cette procédure. Le quorum du collège employeur, lorsque son avis est recueilli, doit être examiné séparément au regard de R254-56 et de la délibération locale applicable.
- **A-04-i03** : La condition déclenchante est identifiée sur bases vérifiées : vote unanime défavorable sur une question soumise en application de R253-7 et dont la mise en œuvre nécessite une délibération ; le taux de promotion (R253-7 12°, L522-27) satisfait cette double condition ; l'exception de R254-56 est réservée : R254-68 ne s'applique pas lorsque le vote unanime défavorable intervient lors de la seconde réunion organisée après un défaut de quorum ; une conclusion conditionnelle sur ces éléments locaux absents est admise sans remettre en doute les faits fournis.

**Échecs — intégration**

- La procédure de réexamen obligatoire (R254-68) n'est pas identifiée.
- Le délai encadrant la nouvelle délibération (entre 8 et 30 jours) est ignoré ou inexact.
- La règle de quorum allégé au second examen est omise.
- La double condition déclenchante (vote unanime ET question délibératoire) n'est pas traitée.

**Critères obligatoires — dégradé**

- **A-04-d01** : L'unanimité du vote défavorable et le caractère délibératoire de la question sont pris comme acquis ; les vérifications portent sur les seules modalités de séance non décrites : composition et quorum de la première séance, recueil éventuel de l'avis du collège employeur.
- **A-04-d02** : Sans source, aucun délai ni règle de quorum n'est certifié : la procédure de réexamen est présentée comme un point à vérifier ; toute certification non vérifiée est un échec.
- **A-04-d03** : Un plan conditionnel est proposé avec les étapes séquencées ; l'unanimité et le caractère délibératoire étant acquis, les réserves portent sur les modalités de séance non décrites.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable, même avec une réserve ; les faits fournis et les références posées comme pistes de recherche restent admis.
- Les modalités de séance non décrites (composition et quorum de la première séance, recueil éventuel de l'avis du collège employeur) ne sont pas identifiées.
- Aucun plan conditionnel n'est proposé.

**Sources annoncées et réserves**

- CGFP R254-68 — Procédure obligatoire après vote unanime défavorable sur question nécessitant délibération, délais, quorum second examen (consulte_dans_dossier).
- CGFP R253-7 12° — Consultation obligatoire du CST sur le taux d'avancement de grade (consulte_dans_dossier).
- CGFP L522-27 — Taux de promotion fixé par l'assemblée délibérante après avis du CST (consulte_dans_dossier).
- CGFP R254-56 — Quorum du CST territorial et règles pour la seconde réunion (consulte_dans_dossier).
- Dossier réellement fourni : [Code général de la fonction publique](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044425500), passages L522-27, R253-7, R254-38, R254-39, R254-56, R254-58, R254-64, R254-65, R254-66, R254-68.

Liste exhaustive des identifiants et critères : [jeuAJSON](cases-a.json).

### A-05 — Écarts de paie

**Question**

12 octobre 2026, collectivité FPT de 480 agents. Lors de la préparation du budget primitif N+1, la DRH constate que le SIRH présente des écarts d'indice entre la base RH et les bulletins de paie des 18 derniers mois pour une vingtaine d'agents, à la suite d'erreurs de saisie d'échelon lors d'une mise à jour logicielle. Ces écarts génèrent des trop-versés et des sous-versés. Produire un mémo de pilotage : audit et quantification des écarts, obligations de régularisation et délais applicables, impact sur la prévision de masse salariale N+1, alertes coordonnées finances et DSI.

**Critères obligatoires — intégration**

- **A-05-i01** : Distinction des régimes : trop-versé (répétition de l'indu au profit de la collectivité, soumise à prescription biennale, loi 2000-321 art. 37-1, avec exceptions aux alinéas suivants) et sous-versé (créance de l'agent, prescription quadriennale loi 68-1250 art. 1, avec causes d'interruption art. 2).
- **A-05-i02** : Pour les trop-versés : délai de deux ans à compter du premier jour du mois suivant le versement erroné (art. 37-1 al. 1) ; exceptions aux alinéas 2 et 3 vérifiées selon la cause de l'erreur ; modalités de récupération sur paie et information préalable renvoyées à vérification des textes non fournis.
- **A-05-i03** : Rôle de la DSI limité à la correction technique avec traçabilité ; instruction et coordination par la DRH ; validation et décision de régularisation par l'autorité compétente, dont l'identification relève de la collectivité.
- **A-05-i04** : Impact budgétaire intégré à la note de prévision de masse salariale N+1, distinguant la charge récurrente corrigée et le one-shot de régularisation.

**Échecs — intégration**

- Confond le régime du trop-versé et celui du sous-versé
- Certifie des modalités de récupération sur paie non étayées par les textes fournis
- Attribue à la DRH seule le pouvoir décisionnel de régularisation sans identifier l'autorité compétente
- Omet l'impact sur la prévision de masse salariale N+1

**Critères obligatoires — dégradé**

- **A-05-d01** : Recensement des variables manquantes (montants par agent et par versement, dates exactes des versements et pièces permettant de reconstituer les écarts, en utilisant la période et la cause déjà fournies) sans certifier aucun délai, taux ou modalité de récupération.
- **A-05-d02** : Présentation conditionnelle des deux régimes trop-versé/sous-versé, en renvoyant délais et modalités à vérification avant tout acte.
- **A-05-d03** : Plan d'action structuré (audit SIRH → questions de contrôle → notification individuelle → régularisation → note finances) utilisable dès vérification des règles.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable, même avec une réserve ; les faits fournis et les références posées comme pistes de recherche restent admis.
- Refuse de structurer le plan d'action faute de textes vérifiés
- Redemande le nombre d'agents ou la taille de collectivité déjà fournis

**Sources annoncées et réserves**

- Loi 2000-321, art. 37-1 — Délai biennal et exceptions pour la répétition de l'indu en matière de rémunération (verifie).
- Loi 68-1250, art. 1 à 3 — Prescription quadriennale des créances sur la collectivité, causes d'interruption (verifie).
- Modalités de récupération sur paie et bulletins rectificatifs FPT — Procédure de bulletin rectificatif, information préalable de l'agent (a_consulter).
- Dossier réellement fourni : [Code général de la fonction publique](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044424813), passages L712-1, L712-2, L712-3. L712-3, hors sujet selon le rapport, est conservé dans l’archive historique mais retiré des sources exigées du cas A-05.
- Dossier réellement fourni : [Loi n° 2000-321 du 12 avril 2000 relative aux droits des citoyens dans leurs relations avec les administrations](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000042914580), passages 37-1.
- Dossier réellement fourni : [Loi n° 68-1250 du 31 décembre 1968 relative à la prescription des créances sur l'Etat, les départements, les communes et les établissements publics](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006528553), passages 1, 2, 3.

Liste exhaustive des identifiants et critères : [jeuAJSON](cases-a.json).

### A-06 — Annuaire et photos

**Question**

12 octobre 2026, collectivité FPT de 520 agents. La DRH souhaite publier sur l'intranet un annuaire professionnel interne : nom, prénom, photo, service, poste, téléphone professionnel, mail professionnel. Le DPO signale que la photo constitue un traitement de données personnelles soumis au RGPD. Plusieurs agents refusent la publication de leur photo. Produire une note de procédure et un projet de formulaire d'information : analyse de la base légale par finalité et par nature de donnée, gestion des refus de photo, contenu de l'information préalable, rôle du DPO.

**Critères obligatoires — intégration**

- **A-06-i01** : Analyse de la finalité et de la nécessité de l'annuaire pour chaque catégorie de donnée ; exclusion explicite du fondement 'intérêt légitime' (RGPD art. 6 f) pour les traitements relevant des missions publiques ; examen des bases envisageables pour les coordonnées professionnelles et de leur fondement juridique, avec conclusion conditionnelle ou suspension précise du choix si ce fondement manque ; qualification de la base applicable à la photo selon sa nécessité à la finalité retenue.
- **A-06-i02** : Traitement des refus de photo : distinction entre retrait du consentement lorsque le traitement repose sur le consentement (RGPD art. 7) et opposition selon les conditions de l'article 21 lorsque la base retenue est l'exécution d'une mission d'intérêt public ; proposition d'une solution alternative (initiales ou avatar neutre), sans ériger en règle universelle l'absence de contrainte ou de sanction.
- **A-06-i03** : Information préalable comportant au moins : identité et coordonnées du responsable du traitement, finalité et base légale, destinataires, durée de conservation ou, lorsque ce n'est pas possible, critères utilisés pour la déterminer, droits d'accès/rectification/effacement et d'opposition, coordonnées du DPO, droit de retrait si le consentement est retenu comme base, droit de réclamation (RGPD art. 13, notamment §1 e, §2 b et d) ; art. 14 si la donnée n'est pas collectée auprès de l'agent.
- **A-06-i04** : Rôle du DPO : association en temps utile, conseil (RGPD art. 39 §1 a) ; documentation à la charge du responsable du traitement (art. 5 §2), sans substitution du DPO au responsable pour la décision sur les contenus publiés et la tenue du registre.

**Échecs — intégration**

- Retient le fondement 'intérêt légitime' (art. 6 f) pour un traitement relevant des missions publiques
- Impose une base unique pour la photo sans analyse de sa nécessité à la finalité retenue
- Omet l'identité du responsable du traitement ou les droits des agents dans l'information préalable
- Attribue au DPO un pouvoir de validation ou d'autorisation du traitement

**Critères obligatoires — dégradé**

- **A-06-d01** : Identification des catégories de données et de leur sensibilité différenciée, avec analyse préparatoire des bases envisageables, sans certifier la base légale applicable à chaque item.
- **A-06-d02** : Recommandation de gestion : différer la publication des photos refusées et proposer une alternative (initiales ou avatar neutre) pendant la vérification du régime applicable avec le DPO, sans certifier ce régime.
- **A-06-d03** : Trame de formulaire d'information avec rubriques à compléter (responsable, finalité, base légale, droits, DPO) sans inventer les mentions légales définitives.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable, même avec une réserve ; les faits fournis et les références posées comme pistes de recherche restent admis.
- Ne fournit aucune trame utilisable de formulaire faute de textes consultés
- Présente une contrainte ou une sanction comme juridiquement fondée sans sources vérifiées

**Sources annoncées et réserves**

- RGPD art. 6 (dispositif EUR-Lex CELEX:02016R0679-20160504) — Licéité du traitement ; inapplicabilité du point f aux autorités publiques dans l'exécution de leurs missions (verifie_selon_complement_2026-10-14).
- RGPD art. 13 et 14 (dispositif EUR-Lex CELEX:02016R0679-20160504) — Information : destinataires (13 §1 e), opposition (13 §2 b), réclamation (13 §2 d), autres mentions de l'attendu ; art. 14 si la donnée n'est pas collectée auprès de l'agent (verifie_selon_complement_2026-10-14).
- RGPD art. 38-39 et 5 §2 (dispositif EUR-Lex CELEX:02016R0679-20160504) — Association du DPO et conseil (39 §1 a) ; documentation à la charge du responsable du traitement (5 §2), sans pouvoir décisionnel du DPO (verifie_selon_complement_2026-10-14).
- Recommandations CNIL sur les annuaires professionnels — Traitement de la photo d'agent dans un annuaire interne (a_consulter).
- Source RGPD à relire : [PDF consolidé EUR-Lex archivé](../rapports/rgpd-2026-10-14/CELEX-02016R0679-20160504-FR-consulte-2026-10-14.pdf) ; identifiant requis `CELEX:02016R0679-20160504` ; [provenance et empreinte](../rapports/rgpd-2026-10-14/provenance.json), [articles et pages par cas](../rapports/rgpd-2026-10-14/articles-rgpd.json).
- Dossier réellement fourni : [Code civil](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006419288), passages 9. Article 9, hors sujet selon le rapport, conservé dans l’archive historique mais retiré des sources exigées du cas A-06.

Liste exhaustive des identifiants et critères : [jeuAJSON](cases-a.json).

### A-07 — Révision d’un CDI

**Question**

12 octobre 2026, collectivité FPT de 480 agents. Un agent contractuel en CDI de droit public recruté sur le fondement de l'article L332-8 2° du CGFP pour un emploi de chargé de mission numérique (catégorie A) est en poste depuis quatre ans. Il demande par écrit une révision de sa rémunération en invoquant l'évolution significative de ses missions, l'expertise acquise et la comparaison avec la grille indiciaire des attachés. Produire une note d'analyse et un projet d'avenant conditionnel : règles de fixation et de réévaluation de la rémunération d'un CDI contractuel, qualification des changements de fonctions, procédure et éléments à documenter.

**Critères obligatoires — intégration**

- **A-07-i01** : Règles applicables : CGFP L713-1 (fonctions, qualification requise, expérience) ; décret 88-145 art. 1-2 (réévaluation au moins tous les trois ans pour les CDI, notamment au vu des entretiens ou de l'évolution des fonctions) ; premier contrôle : date de la dernière réévaluation effectuée ; distinction entre réévaluation périodique et augmentation discrétionnaire.
- **A-07-i02** : Qualification des changements allégués : distinction évolution normale de l'emploi et éventuelle modification substantielle dont la qualification et les suites restent à vérifier ; les critères précis et formalités applicables (R331-12, R331-13) doivent être vérifiés sur les textes non fournis.
- **A-07-i03** : Procédure à documenter : décision de l'autorité territoriale ; préparation conditionnelle du projet demandé sous réserve de vérification des conditions et formalités applicables, les exigences de transmission et de contrôle ultérieur devant être vérifiées avant toute formalisation.
- **A-07-i04** : Éléments admissibles pour instruire la demande : fonctions exercées, qualification détenue, expérience acquise, comparaison indicative avec la grille FPT sans en faire une obligation ; aucun plafond ou plancher non sourcé certifié.

**Échecs — intégration**

- Applique mécaniquement la grille statutaire des attachés à un contractuel CDI
- Omet la réévaluation périodique prévue pour les CDI et le contrôle de sa dernière occurrence
- Certifie des formalités de procédure (contrôle de légalité, conditions d'avenant) non étayées par les textes fournis
- Confond les règles de rémunération des fonctionnaires et des contractuels

**Critères obligatoires — dégradé**

- **A-07-d01** : Identification des variables manquantes (rémunération actuelle, date de dernière réévaluation, description précise des nouvelles missions) sans certifier aucun plafond, plancher ou formalité.
- **A-07-d02** : Présentation conditionnelle du besoin de formalisation si changement substantiel, en indiquant que qualification et formalités doivent être vérifiées avant tout acte.
- **A-07-d03** : Trame d'avenant conditionnel avec clauses à compléter, sans fixer de montant ni certifier des règles de procédure non vérifiées.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable, même avec une réserve ; les faits fournis et les références posées comme pistes de recherche restent admis.
- Refuse de fournir une trame d'avenant faute de textes consultés
- Redemande le fondement contractuel L332-8 2° ou la durée déjà fournis

**Sources annoncées et réserves**

- CGFP L713-1 — Fixation de la rémunération contractuelle : fonctions, qualification, expérience (verifie).
- Décret 88-145, art. 1-2 — Réévaluation au moins tous les trois ans pour les CDI, entretiens professionnels, évolution des fonctions (verifie).
- CGFP R331-12 et R331-13 — Critères de modification substantielle du contrat et formalités requises (a_consulter).
- Décret 88-145 art. 39-3 — Motifs de licenciement, dont le refus d'une modification substantielle du contrat (4°) (a_consulter).
- Dossier réellement fourni : [Décret n°88-145 du 15 février 1988 relatif aux agents contractuels de la fonction publique territoriale](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000054242039), passages 1-2, 1-3, 39-3.
- Dossier réellement fourni : [Code général de la fonction publique](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044424781), passages L713-1.

Liste exhaustive des identifiants et critères : [jeuAJSON](cases-a.json).

### A-08 — Dossier et témoignages

**Question**

12 octobre 2026, collectivité FPT de 480 agents. Un attaché territorial titulaire fait l'objet d'une enquête préalable pour manquement allégué à l'obligation de discrétion professionnelle ; aucune procédure disciplinaire formelle n'est encore engagée. Il demande par écrit l'accès à l'intégralité de son dossier individuel et aux documents sur lesquels l'autorité territoriale pourrait fonder d'éventuelles poursuites, dont certains comportent des témoignages de collègues identifiables. Produire une note de procédure sécurisée : régime d'accès au dossier individuel, communicabilité des documents d'enquête selon leur état, traitement des témoignages identifiables, risques d'irrégularité et articulation avec une éventuelle procédure disciplinaire ultérieure.

**Critères obligatoires — intégration**

- **A-08-i01** : Distinction entre droit d'accès permanent de tout agent à son dossier individuel (CGFP L137-4) et communication des pièces fondant les poursuites disciplinaires (CGFP L532-4, applicable uniquement après engagement formel) ; la garantie disciplinaire de L532-4 n'est pas encore déclenchée ; examiner séparément les autres droits d'accès applicables.
- **A-08-i02** : Communicabilité des documents d'enquête non versés au dossier : appréciation distinguant l'achèvement du document et son caractère préparatoire à une décision encore en cours d'élaboration (CRPA L311-2 : un document même achevé peut rester préparatoire et non communicable) ; application des exceptions L311-6 et L311-7 ; les pièces ne figurant pas au dossier individuel ne sont pas automatiquement communicables avant engagement.
- **A-08-i03** : Traitement des témoignages identifiables : examen préalable sous le CRPA (notamment protections de L311-6 sans exigence d'un risque avéré) distinct des garanties de défense applicables si une procédure disciplinaire est ensuite engagée ; dans ce dernier cas, évaluation d'un risque avéré de préjudice selon la situation particulière du témoin (CE 22/12/2023, n° 462455, points 4-6) ; contenu utile à la défense à préserver.
- **A-08-i04** : Conduite traçable de la communication : organisation et datation des pièces communicables, identification des documents d'enquête à verser ou non, et anticipation des garanties de défense en cas de procédure disciplinaire ultérieure ; le bordereau n'est qu'un moyen possible, non une forme obligatoire.

**Échecs — intégration**

- Confond droit d'accès permanent au dossier individuel et communication disciplinaire applicable uniquement après engagement formel
- Occulte, refuse ou divulgue des témoignages automatiquement, sans examiner le régime d'accès applicable et les protections pertinentes
- Conclut à une nullité ou annulation automatique sans appréciation concrète de l'utilité des pièces pour la défense
- Cite L135 comme fondement du dossier individuel au lieu de L137

**Critères obligatoires — dégradé**

- **A-08-d01** : Identification des deux régimes (dossier individuel / pièces d'enquête ou de poursuites) sans certifier délais, modalités d'anonymisation ni conséquences procédurales précises.
- **A-08-d02** : Signal du risque opérationnel d'une communication défaillante pour la préparation de la défense, en renvoyant les conséquences juridiques exactes à vérification des textes applicables.
- **A-08-d03** : Questions de contrôle ciblées : nature et état d'achèvement des documents d'enquête, contenu des témoignages, décision de versement ou non au dossier individuel.
- **A-08-d04** : Trame de bordereau de communication utilisable après vérification du contenu communicable, sans certifier ce contenu.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable, même avec une réserve ; les faits fournis et les références posées comme pistes de recherche restent admis.
- Refuse de structurer la procédure ou de fournir un bordereau type faute de textes consultés
- Redemande le grade ou la taille de collectivité déjà fournis

**Sources annoncées et réserves**

- CGFP L137-1 à L137-4 — Dossier individuel : composition, accès permanent de l'agent (verifie).
- CGFP L532-4 — Communication du dossier et assistance après engagement disciplinaire (verifie).
- Décret 89-677, art. 4 — Délai suffisant pour la défense après engagement disciplinaire (a_consulter).
- CE, Section, 22/12/2023, n°462455, Lebon — Texte intégral Ariane Web selon le complément : points 4 et 5, motifs décisoires ; témoignages, risque avéré apprécié selon la situation du témoin, défense utile ; contenu utile à préserver et transposition à une enquête préalable de collectivité à signaler comme inférences (verifie_selon_complement_2026-10-14).
- CRPA L311-2, L311-6, L311-7 — Documents préparatoires non communicables ; occultation des mentions protégées (verifie).
- Dossier réellement fourni : [Code général de la fonction publique](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044427574), passages L137-1, L137-2, L137-3, L137-4, L532-4.
- Dossier réellement fourni : [Code des relations entre le public et l'administration](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000033218946), passages L311-1, L311-2, L311-3, L311-6, L311-7, R311-13.
- Dossier réellement fourni : [Conseil d'État, Section, 22/12/2023, 462455, Publié au recueil Lebon](https://www.legifrance.gouv.fr/ceta/id/CETATEXT000048701432), passages document.

Liste exhaustive des identifiants et critères : [jeuAJSON](cases-a.json).

### A-09 — Discipline pendant un CLM

**Question**

Collectivité FPT >350 agents, 12 octobre 2026. Un adjoint administratif titulaire fait l'objet d'une procédure disciplinaire engagée il y a deux mois pour des faits de harcèlement moral. Le rapport d'enquête interne a été notifié à l'agent. Six semaines après l'engagement, l'agent est placé en congé de longue maladie (CLM). La DRH doit : vérifier que le délai de prescription disciplinaire était respecté à la date d'engagement ; déterminer si la procédure peut légalement continuer pendant le CLM ; identifier les conditions dans lesquelles les droits de la défense restent garantis pendant l'arrêt ; et évaluer le risque contentieux principal si la procédure se poursuit sans adaptation. Produire une note de procédure sécurisée.

**Critères obligatoires — intégration**

- **A-09-i01** : Identifie le point de départ et les éventuels événements affectant la prescription (L532-2) ; conclut lorsque les dates nécessaires sont établies, sinon suspend la seule conclusion sur la prescription et demande les éléments manquants ; distingue cette question de celle d'un délai courant après engagement.
- **A-09-i02** : Détermine si un CLM fait légalement obstacle à la poursuite d'une procédure disciplinaire déjà engagée en s'appuyant sur les textes fournis ; cite CE 13 juillet 2022, n°461914, point 19, en précisant sa portée exacte sur ce point.
- **A-09-i03** : Identifie les garanties de défense exigées : communication intégrale du dossier (L532-4), délai suffisant pour organiser la défense (décret 89-677 art. 4), droit à assistance ; si le conseil de discipline intervient, vérifier la convocation au moins quinze jours avant sa réunion (art. 6) ; précise comment l'état de santé peut affecter concrètement l'exercice de ces droits et quel risque contentieux en résulte.

**Échecs — intégration**

- Affirme que le CLM suspend automatiquement la procédure sans citer de texte vérifiable.
- Confond la prescription initiale (délai pour engager) avec la question d'un délai courant après engagement.
- Omet les garanties de défense applicables (L532-4, décret 89-677 art. 4 ; art. 6 lorsque le conseil de discipline intervient).

**Critères obligatoires — dégradé**

- **A-09-d01** : Signale que la règle sur la continuation d'une procédure disciplinaire pendant un CLM doit être vérifiée avant tout acte, sans certifier de position.
- **A-09-d02** : Collecte les variables absentes : date de connaissance effective des faits par l'administration, stade de la procédure au moment du CLM, type de sanction envisagée.
- **A-09-d03** : Propose de différer la convocation jusqu'à vérification ciblée sur la capacité de l'agent à assurer sa défense, sans bloquer indéfiniment ni clore la procédure, et sans certifier l'interlocuteur compétent.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable, même avec une réserve ; les faits fournis et les références posées comme pistes de recherche restent admis.
- Ne collecte pas la date de connaissance effective des faits, absente du prompt.
- Recommande de clore ou poursuivre sans distinguer les précautions liées à l'état de santé.

**Sources annoncées et réserves**

- CGFP L532-2 — Délai de prescription : connaissance effective de la réalité, nature et ampleur des faits (verifie).
- CGFP L532-4 ; décret 89-677 arts 4 et 6 — Garanties de défense : dossier, délai suffisant, convocation, assistance (verifie).
- CE 13 juillet 2022, n°461914, point 19, inédit — Le congé de maladie ne fait pas obstacle à l'action disciplinaire ; point 19 lu en texte intégral sur Ariane Web selon le complément ; aucune précision sur le CLM en particulier ni sur les droits de la défense pendant l'arrêt (verifie_selon_complement_2026-10-14).
- Dossier réellement fourni : [Code général de la fonction publique](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044425430), passages L532-2, L532-4.
- Dossier réellement fourni : [Décret n°89-677 du 18 septembre 1989 relatif à la procédure disciplinaire applicable aux fonctionnaires territoriaux](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000053007836), passages 4, 6.
- Dossier réellement fourni : [Conseil d'État, 8ème - 3ème chambres réunies, 13/07/2022, 461914, Inédit au recueil Lebon](https://www.legifrance.gouv.fr/ceta/id/CETATEXT000046046053), passages document.

Liste exhaustive des identifiants et critères : [jeuAJSON](cases-a.json).

### A-10 — Déploiement du télétravail

**Question**

Collectivité FPT de 420 agents, 12 octobre 2026. La DRH souhaite instaurer le télétravail de manière pérenne pour les postes éligibles. Elle doit : identifier l'acte normatif applicable et l'instance à consulter selon la portée du projet (R432-1 2°, R253-7, R253-80) ; définir les critères d'éligibilité en distinguant titulaires et contractuels ; gérer le cas d'un agent reconnu en situation de handicap demandant à la fois une dérogation au quota standard et des aménagements sur son lieu de télétravail ; intégrer le suivi des jours dans le SIRH avec les exigences RGPD associées ; et concevoir la communication interne d'accompagnement. Produire un plan de déploiement structuré.

**Critères obligatoires — intégration**

- **A-10-i01** : Identifie la délibération de l'organe délibérant et l'instance à consulter selon l'objet et la portée du projet, en articulant R432-1 2°, L253-6 et R253-80 ; ne pénalise pas une réponse qui cite L253-6. Distingue cet acte d'un accord collectif et qualifie les options proposées à la DRH.
- **A-10-i02** : Détermine si le régime applicable aux contractuels (CDI et CDD) diffère de celui des titulaires sur l'accès au télétravail ; cite la base textuelle applicable sur le versant FPT et signale ce qui reste à vérifier.
- **A-10-i03** : Traite séparément la demande de dérogation au quota (R431-6 1° : conditions et durée maximale) et la demande d'aménagement du lieu de télétravail (R433-3, L131-8 : sous réserve de charges non disproportionnées) ; conclut si l'obligation d'aménagement est automatique ou conditionnelle.
- **A-10-i04** : Propose un suivi opérationnel des jours dans le SIRH et une communication d'accompagnement ; identifie les traitements et les questions RGPD à vérifier, sans certifier les obligations dont les sources sont absentes.

**Échecs — intégration**

- Présente charte et accord comme équivalents sans distinguer portée et procédure dans la FPT.
- Retient une instance incompatible avec la portée du projet au regard de R432-1, R253-7 et R253-80.
- Assimile dérogation quota et aménagement de poste handicap sans distinguer leur régime.

**Critères obligatoires — dégradé**

- **A-10-d01** : Signale que l'acte et l'instance doivent être qualifiés selon la composition locale du CST avant d'annoncer une procédure précise, sans certifier la distinction charte/accord comme acquise.
- **A-10-d02** : Collecte les variables absentes : existence d'une formation spécialisée CST, accord collectif local éventuel, outil SIRH disponible, état de la délibération cadre.
- **A-10-d03** : Traite l'agent handicapé en deux questions distinctes (dérogation quota / aménagement) et signale l'incertitude sur l'étendue de chaque obligation sans les affirmer comme absolues.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable, même avec une réserve ; les faits fournis et les références posées comme pistes de recherche restent admis.
- Confond ou omet la distinction titulaires/contractuels.
- Omet de collecter l'existence d'une formation spécialisée CST ou d'un accord local.

**Sources annoncées et réserves**

- CGFP R432-1 2°, R431-5, R431-6 1° — Délibération FPT, avis formation spécialisée ou CST, quota et dérogation pour handicap ou état de santé (verifie).
- CGFP R253-7 et R253-80 — Compétence du CST seul lorsque le projet relève aussi de ses attributions (verifie).
- CGFP R433-3 et L131-8 — Aménagements du lieu de télétravail pour agent handicapé, sous réserve de charges non disproportionnées (verifie).
- CGFP R433-1 et L430-1 — Égalité de droits agent télétravailleur / agent sur site ; application aux contractuels sur versant FPT à vérifier (a_consulter).
- Dossier réellement fourni : [Code général de la fonction publique](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044426132), passages L430-1, L131-8, L251-9, R253-7, R253-80, R431-1, R431-2, R431-3, R431-4, R431-5, R431-6, R432-1, R432-2, R432-3, R433-3.

Liste exhaustive des identifiants et critères : [jeuAJSON](cases-a.json).

### A-11 — Suppression d’emploi et RQTH

**Question**

Collectivité FPT >350 agents, 12 octobre 2026. Un rédacteur principal de 2e classe, reconnu RQTH et bénéficiaire depuis 18 mois d'un aménagement de poste formalisé (horaires adaptés, matériel ergonomique), voit son emploi supprimé par délibération de l'organe délibérant dans le cadre d'une réorganisation. Aucune inaptitude médicale n'a été constatée. La DRH doit : conduire la procédure de suppression d'emploi (CGFP L542-1 à L542-7) ; vérifier si des obligations spécifiques s'appliquent au titre de la qualité de BOE avant, pendant ou après la suppression ; organiser la recherche d'un poste compatible avec les restrictions fonctionnelles formalisées ; identifier qui valide la compatibilité du nouveau poste. Produire une note de procédure articulant ces régimes.

**Critères obligatoires — intégration**

- **A-11-i01** : Articule recherche de reclassement dès que la suppression est envisagée (L542-1), rapport et avis du CST (L542-2), puis suites conditionnelles selon les emplois pouvant être offerts (L542-5) ; distingue maintien en surnombre (L542-4) et prise en charge (L542-7) ; si les conséquences financières sont évoquées, les rattache à la prise en charge (L542-15).
- **A-11-i02** : Vérifie si les textes disponibles établissent des obligations spécifiques à l'employeur au titre de la qualité de BOE lors de la suppression d'emploi, distinctes de la procédure ordinaire (L131-8) ; indique précisément les limites de ce que le corpus permet d'affirmer.
- **A-11-i03** : Identifie qui doit valider la compatibilité entre les restrictions fonctionnelles existantes et le poste de reclassement proposé ; distingue ce contrôle de la procédure d'inaptitude médicale, non en cause ici ; signale explicitement si cette compétence n'est pas établie dans le corpus.

**Échecs — intégration**

- Traite la suppression d'emploi d'un BOE identiquement à celle d'un agent ordinaire sans mentionner la question des obligations spécifiques.
- Confond reclassement pour inaptitude médicale (conseil médical) et reclassement pour suppression d'emploi.
- Cite une référence au livre III du CGFP pour la suppression d'emploi (articles concernés sont au livre V).

**Critères obligatoires — dégradé**

- **A-11-d01** : Signale que des obligations spécifiques BOE en cas de suppression d'emploi doivent être vérifiées avant d'en affirmer l'existence, sans les certifier.
- **A-11-d02** : Collecte les variables absentes : date envisagée de suppression, postes vacants disponibles dans le grade, état des recherches de reclassement déjà engagées.
- **A-11-d03** : Ne confond pas suppression d'emploi (L542-1 à L542-7) et reclassement pour inaptitude médicale (procédure conseil médical) ; présente deux options conditionnelles selon les postes disponibles, sans certifier de délais.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable, même avec une réserve ; les faits fournis et les références posées comme pistes de recherche restent admis.
- Assimile les deux procédures dans la structure de la réponse.
- Omet de collecter la date envisagée et l'état des recherches de postes, absents du prompt.

**Sources annoncées et réserves**

- CGFP L542-1 à L542-7 et L542-15 (livre V) — Procédure de suppression d'emploi, consultation CST, maintien en surnombre, prise en charge, rémunération (verifie).
- CGFP L131-8 — Mesures appropriées pour conserver un emploi correspondant à la qualification du BOE, sous réserve de charges non disproportionnées (verifie).
- Réglementation sur la validation médicale de compatibilité de poste dans la FPT — Rôle du médecin de prévention ou du conseil médical dans la validation de la compatibilité d'un poste de reclassement avec des restrictions fonctionnelles existantes (hors procédure d'inaptitude) (a_consulter).
- Dossier réellement fourni : [Code général de la fonction publique](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044427678), passages L131-8, L351-1, L542-1, L542-2, L542-3, L542-4, L542-5, L542-6, L542-7, L542-15, L542-17, R253-7.
- Dossier réellement fourni : [Décret n°85-603 du 10 juin 1985 relatif à l'hygiène et à la sécurité du travail ainsi qu'à la médecine professionnelle et préventive dans la fonction publique territoriale](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043498231), passages 24.

Liste exhaustive des identifiants et critères : [jeuAJSON](cases-a.json).

### A-12 — Départs et transmission

**Question**

Collectivité FPT de 380 agents, 12 octobre 2026. La DRH identifie 34 agents susceptibles d'être éligibles à un départ en retraite dans les 18 prochains mois (certains atteignent la limite d'âge, d'autres remplissent potentiellement les conditions de durée de service) ; la répartition entre agents affiliés CNRACL et agents relevant d'un autre régime n'est pas encore établie. Parmi eux, 8 occupent des postes de catégories A et B porteurs de compétences rares. La DRH doit piloter : la préparation administrative des départs confirmés (formalités, dossier pension, cessation de fonctions) ; l'évaluation de l'impact sur la masse salariale N+1 et N+2 ; la planification d'un dispositif de transmission des savoirs pour les postes critiques ; et la présentation d'un rapport de situation devant le CST avant l'ouverture des procédures de recrutement. Produire un plan de pilotage intégré.

**Critères obligatoires — intégration**

- **A-12-i01** : Distingue agents affiliés CNRACL et agents relevant d'un autre régime ; décrit les formalités documentées pour la CNRACL (décret 2003-1306 art. 59 : demande six mois avant, dossier employeur trois mois avant radiation ; art. 27 : entrée en jouissance) ; signale que les formalités du régime général sont absentes du corpus et ne les certifie pas ; distingue l'éligibilité d'un départ confirmé (L556-1, décret 2003-1306 art. 2).
- **A-12-i02** : Précise la méthode d'évaluation de l'impact sur la masse salariale en distinguant économies sur postes libérés et coût des recrutements sur N+1 et N+2 ; souligne que l'impact N+2 dépend des délais de recrutement et du niveau de rémunération des nouveaux entrants.
- **A-12-i03** : Qualifie la présentation d'un rapport devant le CST avant les recrutements : identifie les attributions documentées du CST (L253-5 3° : orientations stratégiques RH ; R253-7 8° : projets de LDG) ; distingue obligation de consultation d'une bonne pratique ; ne certifie pas une obligation de rapport GPEEC non établie dans le corpus.
- **A-12-i04** : Propose un dispositif de transmission des savoirs pour les 8 postes critiques en précisant les outils mobilisables et le calendrier minimal compatible avec les départs confirmés.

**Échecs — intégration**

- Confond régime CNRACL et régime général dans la description des formalités de liquidation.
- Omet l'impact masse salariale N+2 (décalage entre économies immédiates et coût des nouveaux recrutements).
- Affirme une obligation légale de rapport GPEEC devant le CST sans citer de texte vérifiable.
- Assimile l'éligibilité à un départ à une cessation certaine et imminente.

**Critères obligatoires — dégradé**

- **A-12-d01** : Signale que les délais CNRACL et les formalités du régime général doivent être vérifiés ; ne certifie aucun délai.
- **A-12-d02** : Collecte les variables absentes : répartition CNRACL/autre régime parmi les 34 agents, distinction départs souhaités/confirmés vs simple éligibilité, état du SIRH.
- **A-12-d03** : Présente la consultation CST préalable aux recrutements comme une option à qualifier selon l'objet du rapport, sans la certifier obligatoire ; identifie les questions et références à vérifier selon l'objet, avec une préparation de gestion conditionnelle.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable, même avec une réserve ; les faits fournis et les références posées comme pistes de recherche restent admis.
- Présente la consultation CST avant recrutements comme automatiquement obligatoire.
- Ne collecte pas la répartition CNRACL/autre régime ni la distinction éligibilité/départ confirmé.

**Sources annoncées et réserves**

- Décret 2003-1306, art. 59 et 27 — Délais de demande et de transmission du dossier employeur CNRACL ; règles d'entrée en jouissance de la pension (verifie).
- CGFP L556-1 et décret 2003-1306 art. 2 — Limite d'âge, maintien autorisé, admission d'office ; distinction éligibilité et cessation effective (verifie).
- CGFP L253-5 3° et R253-7 8° — Attributions CST : orientations stratégiques RH et projets de LDG ; portée par rapport à un rapport préalable aux recrutements (verifie).
- Dossier réellement fourni : [Code général de la fonction publique](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047452904), passages L556-1, L253-5, R253-7.
- Dossier réellement fourni : [Décret n°2003-1306 du 26 décembre 2003 relatif au régime de retraite des fonctionnaires affiliés à la Caisse nationale de retraites des agents des collectivités locales](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000049428994), passages 2, 27, 59.

Liste exhaustive des identifiants et critères : [jeuAJSON](cases-a.json).

## Jeu B — réserve

### B-01 — Mutation hors classe

**Question**

Un attaché hors classe titulaire exerce dans une collectivité de 8 000 habitants depuis trois ans. Il demande sa mutation vers une commune de 450 agents (12 octobre 2026). Le service RH de la collectivité d'accueil a établi que le plafond statutaire de 10 % des attachés en activité et en détachement au 31 décembre N-1 est déjà atteint pour les promotions au grade hors classe de l'année en cours. Le DRH doit déterminer si la mutation peut néanmoins être acceptée et quelle incidence elle aura sur les promotions futures. Produire une note d'aide à la décision.

**Critères obligatoires — intégration**

- **B-01-i01** : Exception au plafond pour mutation externe identifiée sur source (article 21-1 du décret 87-1099 : plafond de 10 % non opposable à la nomination d'un attaché hors classe arrivant par mutation externe), distinguée des conditions territoriales d'exercice du grade hors classe (article 2 : communes de plus de 10 000 habitants, autres collectivités et établissements assimilés).
- **B-01-i02** : Incidence sur les promotions futures précisée sur source : la nomination par mutation externe est prise en compte dans le calcul du plafond pour les avancements suivants.
- **B-01-i03** : Note d'aide à la décision produite distinguant les éléments déjà établis (atteinte du plafond au titre de l'année en cours), la population de la commune d'accueil restant à documenter au regard des conditions territoriales du grade hors classe, et les données nécessaires au seul chiffrage des avancements suivants ; recommandation conditionnelle.

**Échecs — intégration**

- L'exception pour mutation externe n'est pas identifiée ou le plafond est présenté comme toujours opposable.
- L'incidence de la mutation sur les promotions futures est omise.
- La note d'aide à la décision n'est pas produite.

**Critères obligatoires — dégradé**

- **B-01-d01** : Existence d'une exception possible pour mutation externe posée comme à vérifier sur source ; aucune valeur de plafond ni règle certifiée.
- **B-01-d02** : Variables utiles au chiffrage des avancements futurs identifiées (effectif du cadre d'emplois au 31/12 N-1, attachés hors classe en activité et détachement, mutations déjà prononcées dans l'année), sans en faire un préalable à la reconnaissance de l'exception au plafond déjà établie.
- **B-01-d03** : Mode dégradé déclaré ; suspension réservée aux conclusions nécessitant effectivement une source ou une donnée manquante (notamment la population de la commune d'accueil), sans traiter comme absente l'atteinte du plafond déjà établie.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable, même avec une réserve ; les faits fournis et les références posées comme pistes de recherche restent admis.
- Les données nécessaires au chiffrage des avancements suivants (effectif du cadre au 31/12 N-1, attachés hors classe présents, mutations de l'année) ne sont pas identifiées pour les seules conclusions qui en dépendent.
- Le mode dégradé n'est pas déclaré.

**Sources annoncées et réserves**

- Décret 87-1099 du 30 décembre 1987, article 21-1 — Plafond de 10 % de l'effectif actif et détaché au 31/12 N-1 ; exception : plafond non opposable pour mutation externe ; nomination comptée pour les avancements suivants (consulte_dans_dossier).
- CGFP L522-23 — Dérogation au L522-27 autorisée par les statuts particuliers pour les cadres d'emplois de catégorie A (consulte_dans_dossier).
- Dossier réellement fourni : [Décret n°87-1099 du 30 décembre 1987 portant statut particulier du cadre d'emplois des attachés territoriaux](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000054242026), passages 2, 21-1.
- Dossier réellement fourni : [Code général de la fonction publique](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044425508), passages L522-23.

Liste exhaustive des identifiants et critères : [jeuBJSON](cases-b.json).

### B-02 — Droit de retrait

**Question**

Un agent technique territorial titulaire (collectivité de 450 agents, 12 octobre 2026) quitte son poste en invoquant un droit de retrait : il signale une défectuosité du système de protection d'une machine présentant selon lui un danger grave et imminent pour sa santé. Son supérieur hiérarchique estime le danger non avéré et demande à la DRH d'ordonner la reprise immédiate et, en cas de refus, d'opérer une retenue sur traitement. La DRH doit déterminer : les conditions d'un retrait légitime, si une retenue est possible, et comment instruire la situation. Produire une note de procédure.

**Critères obligatoires — intégration**

- **B-02-i01** : Distingue le signalement d'un danger grave et imminent ou d'une défectuosité et les conditions du droit de retrait. La protection contre sanction et retenue de traitement prévue à l'article 5-1 du décret 85-603 exige un motif raisonnable de penser à un danger grave et imminent ; la seule défectuosité ne suffit pas. L'exercice du retrait ne crée pas pour autrui une nouvelle situation de danger grave et imminent.
- **B-02-i02** : Interdiction de retenue sur traitement et d'aucune sanction lorsque le motif raisonnable est établi, identifiée sur source ; impossibilité pour l'autorité territoriale d'ordonner la reprise si le danger persiste qualifiée.
- **B-02-i03** : Note de procédure produite : instruction conditionnelle (vérifier la défectuosité, apprécier le motif raisonnable avant toute retenue ou sanction, constituer les pièces) ; décision sur la reprise subordonnée au résultat de cette vérification.

**Échecs — intégration**

- La retenue sur traitement est présentée comme applicable sans examen du motif raisonnable.
- Les conditions du droit de retrait (motif raisonnable, danger grave et imminent ou défectuosité) ne sont pas identifiées.
- La note de procédure n'est pas produite.

**Critères obligatoires — dégradé**

- **B-02-d01** : Existence d'un droit de retrait dans la FPT territoriale posée comme à vérifier sur source ; aucune condition ni protection certifiées.
- **B-02-d02** : Variables bloquantes identifiées : nature et réalité de la défectuosité, circonstances du signalement déjà mentionné et éléments disponibles pour documenter la situation, position documentée du supérieur, vérification technique de l'équipement.
- **B-02-d03** : Mode dégradé déclaré ; aucune conclusion sur la légitimité du retrait ni sur la retenue sans vérification de la source.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable, même avec une réserve ; les faits fournis et les références posées comme pistes de recherche restent admis.
- Les variables bloquantes (défectuosité, circonstances du signalement, appréciation du motif raisonnable) ne sont pas identifiées.
- Le mode dégradé n'est pas déclaré.

**Sources annoncées et réserves**

- Décret 85-603 du 10 juin 1985, article 5-1 — Motif raisonnable de danger grave et imminent, signalement au supérieur, défectuosité du système de protection, interdiction de sanction et de retenue, impossibilité d'ordonner la reprise si danger persiste (consulte_dans_dossier).
- Dossier réellement fourni : [Décret n°85-603 du 10 juin 1985 relatif à l'hygiène et à la sécurité du travail ainsi qu'à la médecine professionnelle et préventive dans la fonction publique territoriale](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006368812), passages 2-1, 5-1.

Liste exhaustive des identifiants et critères : [jeuBJSON](cases-b.json).

### B-03 — CDD successifs et CDI

**Question**

Un agent contractuel de catégorie B a été recruté six fois de suite par CDD pour accroissement temporaire d'activité sur un emploi non permanent, sur cinq ans et demi (collectivité de 450 agents, 12 octobre 2026). Certains contrats excèdent douze mois ; des interruptions entre contrats sont inférieures à un mois. L'agent demande par écrit sa CDIsation en invoquant ses années de service. Le DRH doit : qualifier le régime de chaque contrat, déterminer si et dans quelles conditions les services accomplis ouvrent droit à une CDIsation, et produire une réponse motivée à l'agent.

**Critères obligatoires — intégration**

- **B-03-i01** : Fondement légal distingué sur source : emploi non permanent pour accroissement temporaire (L332-23) vs contrat établi ou renouvelé pour pourvoir un emploi permanent (L332-8) ; CDIsation de droit (L332-10) subordonnée à un contrat relevant de L332-8, les services accomplis au titre de L332-23 étant comptabilisables pour la durée de six ans auprès du même employeur et dans la même catégorie hiérarchique.
- **B-03-i02** : Distinguer les dépassements individuels de douze mois déjà indiqués, contraires à la durée maximale, du contrôle des renouvellements sur dix-huit mois nécessitant la chronologie détaillée ; ne déduire ni irrégularité autonome des interruptions courtes ni CDIsation automatique des dépassements.
- **B-03-i03** : Réponse motivée à l'agent produite en version conditionnelle, précisant la position de la collectivité ; l'existence de voies de recours peut être mentionnée comme piste de vérification sans en certifier le détail procédural.

**Échecs — intégration**

- Une CDIsation de droit est affirmée sans vérifier les conditions de L332-10, notamment le contrat établi ou renouvelé sous L332-8, les six ans de services admissibles, le même employeur et la même catégorie hiérarchique.
- Les interruptions courtes sont automatiquement qualifiées d'irrégularités sans analyse des fenêtres de référence.
- La réponse à l'agent est absente.

**Critères obligatoires — dégradé**

- **B-03-d01** : Distinction emploi non permanent / emploi permanent posée sans certification des durées exactes ni des conditions de CDIsation.
- **B-03-d02** : Variables bloquantes identifiées : chronologie détaillée et dates de chaque contrat, fondement juridique de chaque contrat, durée de chaque interruption ; la catégorie B et la nature des recrutements pour accroissement temporaire sur emploi non permanent sont tenues pour acquises, les contrats étant demandés comme justificatifs.
- **B-03-d03** : Mode dégradé déclaré ; réponse à l'agent en version d'attente concise avec champs à compléter ; aucune CDIsation ni irrégularité certifiées sans vérification.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable, même avec une réserve ; les faits fournis et les références posées comme pistes de recherche restent admis.
- Les variables bloquantes (chronologie et dates des contrats, interruptions, fondement de chaque contrat) ne sont pas identifiées.
- Le mode dégradé n'est pas déclaré.

**Sources annoncées et réserves**

- CGFP L332-23 — Emploi non permanent pour accroissement temporaire, durée maximale douze mois, période de référence dix-huit mois, renouvellement (consulte_dans_dossier).
- CGFP L332-10 — Conditions de CDIsation de droit : emploi permanent, six ans, même employeur, même catégorie, continuité ≤ 4 mois ; prise en compte des services accomplis au titre de L332-23 (consulte_dans_dossier).
- Dossier réellement fourni : [Code général de la fonction publique](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000048778058), passages L332-8, L332-9, L332-10, L332-11, L332-12, L332-13, L332-23.
- Dossier réellement fourni : [Décret n°88-145 du 15 février 1988 relatif aux agents contractuels de la fonction publique territoriale](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051980613), passages 1.

Liste exhaustive des identifiants et critères : [jeuBJSON](cases-b.json).

### B-04 — Demande syndicale de négociation

**Question**

La DRH d'une collectivité de 420 agents (12 octobre 2026) prépare des lignes directrices de gestion (LDG) sur la promotion et la valorisation des parcours professionnels. Deux organisations syndicales représentatives réclament l'ouverture d'une négociation formelle préalable à toute consultation du CST, soutenant que les LDG relèvent d'un domaine de négociation obligatoire. La DRH doit arbitrer : procédure légale applicable aux LDG territoriales, existence ou non d'une obligation légale de négociation préalable, risques en cas de vice de procédure. Produire une note d'aide à la décision.

**Critères obligatoires — intégration**

- **B-04-i01** : Procédure légale des LDG territoriales précisée sur source : L413-1 (stratégie pluriannuelle, orientations en matière de promotion et de valorisation des parcours), L413-3 (LDG arrêtées par l'autorité compétente après avis du comité social compétent) et R413-31 (saisine pour avis du CST sur les projets de LDG).
- **B-04-i02** : Obligation légale de négociation préalable aux LDG : conclusion limitée aux passages effectivement reproduits (L222-3 8° : déroulement des carrières dans le champ de négociation) ; absence d'une obligation d'ouverture automatique démontrée sur source ou gap explicitement identifié si la source ne permet pas de conclure.
- **B-04-i03** : Note d'aide à la décision produite : distinction consultation CST / négociation posée, risque contentieux en cas de défaut de consultation CST identifié, recommandation conditionnelle sur la suite à donner à la demande syndicale selon les variables locales.

**Échecs — intégration**

- Une obligation légale de négociation préalable aux LDG est affirmée sans source consultée l'établissant.
- La compétence du CST sur les LDG est affirmée sans fondement textuel identifié.
- La note d'aide à la décision n'est pas produite.

**Critères obligatoires — dégradé**

- **B-04-d01** : Procédure des LDG FPT posée comme à vérifier ; aucune obligation de négociation ni son absence certifiées.
- **B-04-d02** : Variables bloquantes identifiées : existence d'un accord, protocole ou engagement local pris en instance. La représentativité des deux organisations syndicales est tenue pour acquise ; les suffrages peuvent constituer une information utile à une vérification ciblée, sans constituer un seuil ou une règle juridique en mode dégradé.
- **B-04-d03** : Mode dégradé déclaré ; note produite en version bornée ; aucune conclusion sur la validité ou l'annulation des LDG sans vérification.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable, même avec une réserve ; les faits fournis et les références posées comme pistes de recherche restent admis.
- Les variables bloquantes (accord, protocole ou engagement local) ne sont pas identifiées, la représentativité syndicale étant tenue pour acquise.
- Le mode dégradé n'est pas déclaré.

**Sources annoncées et réserves**

- CGFP L413-1, L413-2, L413-3 — L413-1 : contenu des LDG pour toutes FP ; L413-2 : volet mobilité réservé à l'État ; L413-3 : avis du comité social compétent (consulte_dans_dossier).
- CGFP R413-31, R253-7 (8°) — Consultation du CST territorial sur les projets de LDG promotion/valorisation (consulte_dans_dossier).
- CGFP L221-2, L222-3 (8°), L223-1 — Champ de la négociation collective incluant le déroulement des carrières ; conditions de validité d'un accord (50 % des suffrages) ; représentativité requise (consulte_dans_dossier).
- Dossier réellement fourni : [Code général de la fonction publique](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044426396), passages L413-1, L413-2, L413-3, L222-3, R413-31, R413-32, R413-33, R413-34, L224-1, L224-2, L224-3, L224-4, R253-7, L221-2, L223-1.

Liste exhaustive des identifiants et critères : [jeuBJSON](cases-b.json).

### B-05 — Recette du SIRH

**Question**

Collectivité FPT >350 agents, 12 octobre 2026. À l'issue d'une migration du SIRH vers un prestataire externe finalisée il y a trois semaines, la DRH constate des erreurs de correspondance entre données reprises et référentiels locaux : échelons mal appariés pour une trentaine d'agents, droits à formation non intégrés, accès non ouverts pour plusieurs gestionnaires. Le prestataire conteste une partie des anomalies. La DRH doit piloter la recette, arbitrer les corrections à la charge du prestataire ou de la collectivité, sécuriser le contrôle RGPD des données transmises, et décider des conditions d'ouverture officielle du système.

**Critères obligatoires — intégration**

- **B-05-i01** : Le répondant identifie les vérifications à conduire avant ouverture (cohérence des données reprises, droits d'accès, intégrité des référentiels) et les responsabilités contractuelles DRH/prestataire à établir à partir du contrat de sous-traitance, avec les textes vérifiés.
- **B-05-i02** : Le répondant précise les obligations RGPD applicables au prestataire en tant que sous-traitant (instructions documentées, garanties, informations et audits selon l'art. 28 §3 h, registre du sous-traitant selon l'art. 30 §2, sécurité selon l'art. 32, restitution ou suppression) et les contrôles que la DRH doit exercer, avec les articles vérifiés.
- **B-05-i03** : Le répondant propose une procédure de décision d'ouverture conditionnelle distinguant anomalies bloquantes et corrections différables, et propose une répartition des rôles (DRH, DSI, DPO, finances) à valider selon les habilitations locales et le contrat, sans abandonner la décision d'ouverture au prestataire.

**Échecs — intégration**

- Attribue sans justification locale la compétence finale d'ouverture à un acteur ou abandonne au prestataire le contrôle de la recette
- Omet les obligations RGPD du prestataire sous-traitant
- Ne distingue pas anomalies bloquantes et corrections différables

**Critères obligatoires — dégradé**

- **B-05-d01** : Le répondant signale qu'il ne peut certifier les obligations contractuelles exactes ni le périmètre des responsabilités du prestataire sans accès au contrat de sous-traitance, et indique les clauses à vérifier.
- **B-05-d02** : Le répondant identifie les données RGPD à vérifier (types de données transmises, destinataires, mesures de sécurité) comme conditions préalables à l'ouverture, sans certifier la conformité.
- **B-05-d03** : Le répondant propose une logique conditionnelle de recette (anomalies bloquantes à qualifier, seuil d'ouverture) sans certifier la procédure exacte ni les délais contractuels.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable, même avec une réserve ; les faits fournis et les références posées comme pistes de recherche restent admis.
- Ne collecte pas les variables nécessaires (contenu du contrat, types de données, liste des anomalies)
- Refuse toute logique conditionnelle d'ouverture

**Sources annoncées et réserves**

- RGPD art. 28, 30 §2 et 32 (dispositif EUR-Lex CELEX:02016R0679-20160504) — Instructions documentées, garanties, informations et audits (28 §3 h), registre du sous-traitant (30 §2), sécurité (32), restitution ou suppression (verifie_selon_complement_2026-10-14).
- RGPD art. 5, 25, 32 (dispositif EUR-Lex CELEX:02016R0679-20160504) — Principes de minimisation, privacy by design, sécurité du traitement applicables à la reprise de données (verifie_selon_complement_2026-10-14).
- Contrat de sous-traitance SIRH — Répartition des responsabilités en cas d'erreurs de reprise, délais de correction, conditions de recette (piece_locale).
- Source RGPD à relire : [PDF consolidé EUR-Lex archivé](../rapports/rgpd-2026-10-14/CELEX-02016R0679-20160504-FR-consulte-2026-10-14.pdf) ; identifiant requis `CELEX:02016R0679-20160504` ; [provenance et empreinte](../rapports/rgpd-2026-10-14/provenance.json), [articles et pages par cas](../rapports/rgpd-2026-10-14/articles-rgpd.json).

Liste exhaustive des identifiants et critères : [jeuBJSON](cases-b.json).

### B-06 — Newsletter et données

**Question**

Collectivité FPT >350 agents, 12 octobre 2026. La DRH souhaite lancer une newsletter mensuelle numérique via les adresses mail professionnelles des agents. Contenu prévu : statistiques anonymisées sur l'absentéisme, annonces de promotions nominatives, résultats d'enquêtes internes de satisfaction, informations syndicales résumées par la DRH. Le DPO alerte sur la nécessité d'établir une base légale pour les traitements impliquant des données personnelles et de vérifier les droits des agents. La DRH doit piloter la décision éditoriale et de gouvernance sans la déléguer au DPO. Produire un cadrage.

**Critères obligatoires — intégration**

- **B-06-i01** : Le répondant vérifie rubrique par rubrique si un traitement de données personnelles est effectivement en jeu (notamment pour les données présentées comme anonymisées) et, pour les rubriques concernées, justifie le fondement applicable lorsque les éléments fournis le permettent ; pour une rubrique nominative révélant l'appartenance syndicale, examine aussi l'art. 9 §1 RGPD ; sinon identifie les fondements à examiner et suspend précisément leur validation en indiquant le texte ou la documentation manquante.
- **B-06-i02** : Le répondant précise, pour les traitements impliquant des données personnelles, les obligations d'information des agents (RGPD art. 13 ou 14 selon que les données sont ou non collectées auprès de l'agent) et les droits applicables selon le fondement retenu, en distinguant le droit d'opposition (art. 21, dont §4) des autres droits.
- **B-06-i03** : Le répondant délimite les rôles du DPO et de la DRH et identifie le texte manquant sur la communication syndicale. L121-2 porte sur la neutralité et la laïcité de l'agent ; il ne suffit pas à fonder le régime de cette rubrique.

**Échecs — intégration**

- Certifie les bases légales RGPD sans source vérifiée pour chaque rubrique
- Confie la décision éditoriale ou de gouvernance au DPO
- Attribue la tenue du registre des traitements au DPO seul sans mentionner la responsabilité de la collectivité
- Ignore les risques liés à la rubrique informations syndicales

**Critères obligatoires — dégradé**

- **B-06-d01** : Le répondant signale qu'il ne peut certifier les bases légales précises ni les droits applicables à chaque rubrique sans vérification, et indique les textes à consulter par catégorie de contenu.
- **B-06-d02** : Le répondant recense les questions à soumettre au DPO sans lui attribuer le pouvoir décisionnel éditorial, et formule les points de vigilance à vérifier avant publication.
- **B-06-d03** : Le répondant propose un plan conditionnel de lancement intégrant l'avis DPO préalable et désigne la rubrique informations syndicales comme nécessitant une vérification spécifique, sans certifier les modalités admissibles.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable, même avec une réserve ; les faits fournis et les références posées comme pistes de recherche restent admis.
- Bloque le projet sans proposer de démarche conditionnelle
- Confond rôle consultatif du DPO et pouvoir décisionnel de la DRH

**Sources annoncées et réserves**

- RGPD art. 6, 9 §1, 13, 14 et 21 §4 (dispositif EUR-Lex CELEX:02016R0679-20160504) — Fondement des traitements ; appartenance syndicale pour une rubrique nominative (9 §1) ; information selon 13 ou 14 ; droit d'opposition dont 21 §4 (verifie_selon_complement_2026-10-14).
- RGPD art. 30, 38-39 (dispositif EUR-Lex CELEX:02016R0679-20160504) — Tenue du registre par le responsable du traitement ; missions du DPO sans pouvoir décisionnel (verifie_selon_complement_2026-10-14).
- CGFP L121-2 et texte régissant la communication syndicale dans les collectivités — L121-2 vise la neutralité et la laïcité de l'agent ; aucun article d'affichage ou de diffusion syndicale trouvé dans L213, L214, L215, partie législative du CGFP ; partie réglementaire non lue : abstention sur le régime de cette communication (abstention_partie_legislative_recherchee_reglementaire_non_lue).
- Source RGPD à relire : [PDF consolidé EUR-Lex archivé](../rapports/rgpd-2026-10-14/CELEX-02016R0679-20160504-FR-consulte-2026-10-14.pdf) ; identifiant requis `CELEX:02016R0679-20160504` ; [provenance et empreinte](../rapports/rgpd-2026-10-14/provenance.json), [articles et pages par cas](../rapports/rgpd-2026-10-14/articles-rgpd.json).
- Dossier réellement fourni : [Code général de la fonction publique](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044427911), passages L121-2, L121-6, L121-7.

Liste exhaustive des identifiants et critères : [jeuBJSON](cases-b.json).

### B-07 — Congé pour convenances personnelles

**Question**

Collectivité FPT >350 agents, 12 octobre 2026. Un agent contractuel en CDI de droit public, catégorie B, recruté sur emploi permanent depuis 7 ans, adresse une demande écrite de congé non rémunéré de 12 mois pour convenances personnelles en invoquant par analogie les droits à disponibilité reconnus aux fonctionnaires titulaires. La DRH doit déterminer si ce congé existe pour les contractuels en CDI territorial, sur quelle base légale, et quel est l'effet sur le contrat pendant l'absence. Produire une note de décision motivée à destination du DGS.

**Critères obligatoires — intégration**

- **B-07-i01** : Le répondant identifie le texte régissant les congés non rémunérés pour convenances personnelles des agents contractuels territoriaux en CDI et précise les conditions d'octroi effectivement documentées, sans extrapoler les conditions non vérifiées.
- **B-07-i02** : Le répondant établit explicitement que l'analogie avec la disponibilité fonctionnaire n'est pas automatique, en distinguant le régime propre aux contractuels du régime fonctionnaire documenté par les articles CGFP fournis (L514-1 à L514-8).
- **B-07-i03** : Le répondant présente l'effet juridique du congé sur le CDI et les conditions de réintégration uniquement à partir des passages vérifiés (décret 88-145, art. 33-34), suspend la qualification de l'état du CDI pendant l'absence si aucun passage ne l'établit, et identifie les gaps à fermer avant décision.

**Échecs — intégration**

- Applique directement le régime de disponibilité fonctionnaire sans distinguer le statut contractuel
- Annonce les conditions du congé sans source vérifiée
- Qualifie l'effet sur le CDI sans passage textuel établissant cette qualification

**Critères obligatoires — dégradé**

- **B-07-d01** : Le répondant indique qu'il ne peut certifier l'existence ni les conditions du congé pour convenances personnelles des contractuels CDI sans avoir consulté le texte applicable (notamment art. 17 décret 88-145), et précise ce texte à consulter.
- **B-07-d02** : Le répondant avertit que l'analogie avec la disponibilité fonctionnaire ne peut être appliquée sans vérification et signale le risque pour la collectivité d'un refus sans base légale ou d'un accord à tort.
- **B-07-d03** : Le répondant propose une démarche conditionnelle : si le congé existe, conditions et effets à vérifier ; si non, alternatives à explorer — sans certifier le résultat.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable, même avec une réserve ; les faits fournis et les références posées comme pistes de recherche restent admis.
- Ne signale pas le risque de confusion entre disponibilité fonctionnaire et congé contractuel
- Ne propose aucune démarche conditionnelle

**Sources annoncées et réserves**

- Décret 88-145 du 15 février 1988, art. 17 (fourni) — Congé non rémunéré pour convenances personnelles des agents en CDI : existence, conditions, durée maximale et renouvellement, modalités et délai de demande (verifie).
- Décret 88-145, art. 33-34 (fournis) — Conditions de réemploi, priorité, exclusions et portée CDI/CDD ; ne retenir un délai que pour le congé auquel le texte le rattache (verifie).
- CGFP L514-1 à L514-8 (fournis) — Régime de disponibilité fonctionnaire à comparer pour mesurer l'écart, non à transposer directement (verifie).
- Dossier réellement fourni : [Décret n°88-145 du 15 février 1988 relatif aux agents contractuels de la fonction publique territoriale](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000046185721), passages 17, 32, 33, 34.
- Dossier réellement fourni : [Code général de la fonction publique](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044425636), passages L514-1, L514-2, L514-3, L514-4, L514-5, L514-6, L514-7, L514-8.

Liste exhaustive des identifiants et critères : [jeuBJSON](cases-b.json).

### B-08 — Saisie sur rémunération

**Question**

Collectivité FPT >350 agents, 12 octobre 2026. La DRH reçoit une notification visant le traitement d'un adjoint administratif titulaire (catégorie C, indice brut 380, marié, sans enfant déclaré à charge). L'expéditeur demande à la collectivité, en tant que tiers saisi, de pratiquer des retenues mensuelles sur rémunération et de les reverser. La DRH doit qualifier le régime applicable, identifier l'assiette saisissable et les exclusions, appliquer le barème légal selon la situation familiale déclarée, informer l'agent de ses droits, et organiser le circuit de traitement avec le service financier. Produire une note de procédure interne.

**Critères obligatoires — intégration**

- **B-08-i01** : Le répondant vérifie l'identité de l'émetteur compétent (commissaire de justice répartiteur, régime en vigueur depuis le 1er juillet 2025, R212-3 CPCE) et le régime applicable aux employeurs publics, en citant les articles vérifiés.
- **B-08-i02** : Le répondant identifie les éléments de rémunération inclus dans l'assiette saisissable et les exclusions documentées par les textes fournis, applique le barème par tranches en précisant les données manquantes nécessaires au calcul final (rémunération nette précise, ressources du conjoint pour le correctif).
- **B-08-i03** : Le répondant précise les obligations déclaratives de la collectivité tiers saisi et les délais documentés par les articles fournis, demande un circuit coordonné respectant les rôles textuels (service employeur, comptable assignataire) et les habilitations locales, décrit le circuit de versement à partir des sources fournies en ne signalant que les lacunes réellement restantes, et prépare une information de l'agent limitée aux éléments documentés, notamment la juridiction de contestation indiquée dans l'acte selon R212-1-15, avec identification des compléments à vérifier.

**Échecs — intégration**

- Présente le reversement au greffe comme automatique sans vérifier le régime en vigueur depuis juillet 2025
- Annonce les quotités saisissables sans source vérifiée
- Omet les variables bloquantes au calcul (rémunération nette, ressources conjoint pour le correctif)
- Attribue sans justification une compétence exclusive à la DRH ou confond les obligations du service employeur et du comptable assignataire

**Critères obligatoires — dégradé**

- **B-08-d01** : Le répondant signale qu'il ne peut certifier ni le barème exact ni la liste exhaustive des exclusions sans vérification, indique les textes à consulter, et identifie les données manquantes (rémunération nette, ressources conjoint) comme variables bloquantes.
- **B-08-d02** : Le répondant avertit que l'identité du destinataire compétent (greffe ou commissaire de justice répartiteur) doit être vérifiée avant toute retenue et propose une démarche conditionnelle sans certifier le circuit.
- **B-08-d03** : Le répondant souligne l'urgence de qualifier la notification reçue et propose un plan conditionnel, incluant la préparation conditionnelle de l'information de l'agent, sans certifier les délais de traitement, les droits ni les sanctions applicables.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable, même avec une réserve ; les faits fournis et les références posées comme pistes de recherche restent admis.
- Ne collecte pas les variables manquantes pour le calcul
- Ignore l'urgence de qualifier la notification reçue

**Sources annoncées et réserves**

- CPCE R212-1-14, R212-2, R212-4, L212-8 (fournis) — Déclaration au commissaire de justice répartiteur ; régime particulier aux employeurs publics ; copie au comptable assignataire (verifie).
- Code du travail L3252-3, R3252-2, R3252-3 (fournis) — Assiette après déductions ; barème par tranches ; correctif par personne à charge sous condition de ressources et sur justification (verifie).
- CGFP L711-5 et code du travail L3252-3 — L711-5 rend applicable le code du travail ; L3252-3 exclut les indemnités insaisissables, remboursements de frais, allocations ou indemnités pour charges de famille ; SFT non nommé : son rattachement nominatif est une inférence, pas une exclusion textuelle nominative certifiée (verifie_selon_complement_2026-10-14).
- CPCE R212-3, R212-6 (fournis) ; L212-14 (fourni) — Circuit de versement par le comptable public et déclarations du service employeur ; sanctions du tiers saisi défaillant (L212-14) ; L212-12 à consulter uniquement si son contenu précis est nécessaire (verifie).
- Dossier réellement fourni : [Code des procédures civiles d'exécution](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000048447274), passages L212-1, L212-5, L212-8, L212-14, R212-1-4, R212-1-14, R212-1-15, R212-1-16, R212-1-17, R212-1-18, R212-1-19, R212-1-20, R212-2, R212-3, R212-4, R212-5, R212-6.
- Dossier réellement fourni : [Code du travail](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006902878), passages L3252-2, L3252-3, R3252-2, R3252-3, R3252-5.

Liste exhaustive des identifiants et critères : [jeuBJSON](cases-b.json).

### B-09 — Recrutement et grossesse

**Question**

Le 12 octobre 2026, dans une communauté d'agglomération de 410 agents (>350), une candidate contractuelle externe a été écartée d'une procédure de recrutement sur emploi permanent de catégorie B après que le jury a eu connaissance de sa grossesse lors de l'entretien. La DRH est alertée par un signalement de la candidate. Elle doit : qualifier la discrimination alléguée et les protections applicables à la candidate ; déterminer si des données relatives à la grossesse ont été collectées ou consignées dans le dossier de recrutement et analyser les obligations RGPD correspondantes ; identifier les mesures correctives sur la procédure de recrutement ; et préparer une communication interne aux membres du jury.

**Critères obligatoires — intégration**

- **B-09-i01** : Analyse l'allégation de discrimination liée à la grossesse au regard de L131-1 et L131-2 CGFP sans tenir le lien causal pour établi ; examine la portée de ces textes et de L131-12 et L135-4 pour une candidate externe et suspend la conclusion sur ses protections lorsque le fondement manque ; distingue la qualification de lanceur d'alerte selon l'art. 6 I de la loi 2016-1691 et la voie interne ouverte aux personnes candidates à un emploi par l'art. 8 I-A 1°, sans tenir la qualification de lanceur d'alerte pour acquise.
- **B-09-i02** : Vérifie les données effectivement traitées et leur qualification, les finalités, le fondement de l'article 6 RGPD et, si applicable, une exception de l'article 9 ; la qualification de la grossesse comme donnée de santé (art. 4 §15 et art. 9 §1) est à établir sur les faits ; distingue l'utilisation des données pour sélectionner des candidats d'une conservation limitée et sécurisée de preuves, en examinant l'art. 17 §3 e, sans conclure a priori à l'absence de fondement ni à une suppression obligatoire.
- **B-09-i03** : Propose des mesures correctives proportionnées aux faits : contrôle des motifs du rejet, réexamen impartial, adaptation éventuelle de la procédure ou du jury, préservation des preuves ; définit le contenu minimal de la communication interne aux membres du jury sur la pertinence des données collectées et l'absence de critères discriminatoires, sans imposer l'éviction automatique du jury.

**Échecs — intégration**

- Omet d'analyser l'allégation de discrimination liée à la grossesse et la portée des textes pour une candidate externe
- Analyse les données de grossesse sans vérifier les données effectivement traitées, leur qualification, les finalités et le fondement applicable (articles 5, 6 et 9 RGPD)
- Ne prévoit aucun examen de mesures correctives proportionnées sur la procédure de recrutement

**Critères obligatoires — dégradé**

- **B-09-d01** : Signale que la qualification de la discrimination et la portée des protections pour une candidate externe nécessitent de vérifier L131-1, L131-2, L131-12 et L135-4 CGFP et les conditions des articles 6 et 8 de la loi du 9 décembre 2016, posés comme pistes, avant toute décision.
- **B-09-d02** : Collecte les variables manquantes décisives : existence d'une mention écrite de la grossesse dans le dossier ou un compte rendu de jury, stade de la procédure au moment du signalement, existence d'un autre candidat déjà informé de sa sélection.
- **B-09-d03** : Prépare conditionnellement des mesures correctives proportionnées (contrôle des motifs, réexamen impartial, adaptation éventuelle de la procédure ou du jury, préservation des preuves), sans certifier qu'une solution précise s'impose sans vérification des faits.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable, même avec une réserve ; les faits fournis et les références posées comme pistes de recherche restent admis.
- Omet la trace écrite dans le dossier comme variable décisive à collecter.
- Omet de préparer des mesures correctives proportionnées ou affirme une obligation d'annulation totale de la procédure.

**Sources annoncées et réserves**

- CGFP L131-1, L131-2, L131-12, L135-4 — Interdiction des discriminations fondées sur le sexe et la grossesse ; champ des agents publics et conditions propres à chaque protection, portée à vérifier pour une candidate externe sans protection présumée applicable (verifie).
- RGPD art. 4 §15, 5, 6, 9 et 17 §3 e (dispositif EUR-Lex CELEX:02016R0679-20160504) — Qualification de la grossesse comme donnée de santé à établir sur les faits ; finalités, fondement et exceptions de l'art. 9, dont 9 §2 f ; conservation limitée et sécurisée de preuves et examen de l'art. 17 §3 e (verifie_selon_complement_2026-10-14).
- Loi 2016-1691 art. 6, 8, 10-1 — Qualification de l'alerte selon l'art. 6 I ; voie interne ouverte aux personnes candidates à un emploi (8 I-A 1°) ; interdiction des représailles, dont licenciement et mesures disciplinaires (10-1 II) ; textes en vigueur depuis le 01/09/2022 selon le complément (verifie_selon_complement_2026-10-14).
- Dossier réellement fourni : [Code général de la fonction publique](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044427698), passages L131-1, L131-2, L131-12, L131-13, L135-4.
- Source RGPD à relire : [PDF consolidé EUR-Lex archivé](../rapports/rgpd-2026-10-14/CELEX-02016R0679-20160504-FR-consulte-2026-10-14.pdf) ; identifiant requis `CELEX:02016R0679-20160504` ; [provenance et empreinte](../rapports/rgpd-2026-10-14/provenance.json), [articles et pages par cas](../rapports/rgpd-2026-10-14/articles-rgpd.json).

Liste exhaustive des identifiants et critères : [jeuBJSON](cases-b.json).

### B-10 — Transfert d’agents

**Question**

Le 12 octobre 2026, une communauté de communes de 380 agents (>350) absorbe par dissolution légale d'un syndicat intercommunal 42 agents : 28 titulaires (catégories A, B, C) et 14 contractuels de droit public (6 en CDI, 8 en CDD dont certains arrivent à terme dans les 6 mois suivant le transfert). Le transfert est effectif dans 90 jours. La DRH doit qualifier le régime juridique applicable à chaque catégorie d'agents à partir des textes pertinents, identifier les obligations de consultation du CST, évaluer l'impact sur la masse salariale et le SIRH, et produire un plan de conduite du changement RH.

**Critères obligatoires — intégration**

- **B-10-i01** : Identifie la base de la dissolution (CGCT L5212-33), sans en déduire le transfert des agents ; distingue la substitution vers un syndicat mixte (L5711-4) du mécanisme de reprise à déterminer à partir de l'acte de dissolution et des compétences concernées, puis applique le cadre de reprise établi aux titulaires et aux contractuels, ou suspend précisément cette conclusion ; ne mobilise L445-1 et L445-2 CGFP qu'après vérification de leurs conditions et de leur articulation avec le dispositif spécial, sans présenter la reprise comme automatique.
- **B-10-i02** : Identifie l'obligation de consultation du CST de la collectivité d'accueil sur les projets d'organisation des services (R253-7, 1° CGFP) ; examine si un CST du syndicat dissous est encore constitué et compétent avant la dissolution effective et doit également être consulté.
- **B-10-i03** : Pour les CDD arrivant à terme dans les 6 mois post-transfert, identifie les variables à vérifier (durée résiduelle, ancienneté, nature du besoin) pour décider entre non-renouvellement au terme et examen d'une proposition de renouvellement ou de CDI, sans certifier les conditions d'une CDIsation sans vérification des textes applicables à la collectivité d'accueil.
- **B-10-i04** : Prépare une estimation documentée de l'impact salarial et un plan opérationnel de reprise SIRH et d'accompagnement du changement, avec hypothèses, responsables et jalons adaptés au délai de 90 jours.

**Échecs — intégration**

- Affirme un régime de reprise distinct pour titulaires et contractuels sans l'avoir déduit de l'acte de dissolution et du cadre de reprise applicable
- Présente la reprise des contractuels comme automatique sans vérifier les conditions de L445-1 et L445-2
- Omet la consultation du CST de la collectivité d'accueil avant le transfert

**Critères obligatoires — dégradé**

- **B-10-d01** : Signale que les modalités exactes du transfert dépendent de la qualification de l'acte de dissolution et des compétences concernées ; conserve L5212-33, L5711-4, L5211-4-1 IV bis, L445-1 et L445-2 comme pistes à vérifier, sans affirmer le renvoi applicable ni le régime avant ces vérifications.
- **B-10-d02** : Collecte les variables manquantes décisives au traitement individuel : éléments d'ancienneté et de rémunération de chaque agent, durée résiduelle des CDD, grilles appliquées dans l'ancienne structure, existence d'un CST encore actif dans le syndicat dissous ; les statuts annoncés (titulaires, CDI, CDD) restent acquis.
- **B-10-d03** : Identifie l'impact SIRH et masse salariale comme axe à co-instruire avec DSI et finances et repère le circuit documentaire de validation et le décideur habilité pour les modalités de reprise statutaire ou contractuelle.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable, même avec une réserve ; les faits fournis et les références posées comme pistes de recherche restent admis.
- Omet la durée résiduelle des CDD comme variable décisive à collecter.
- Délègue aux finances ou à la DSI la décision sur le régime applicable ou omet de préparer l'estimation salariale et le plan de reprise utiles.

**Sources annoncées et réserves**

- CGCT L5212-33 et L5711-4 — Base de la dissolution (L5212-33), non du transfert des agents ; substitution vers un syndicat mixte (L5711-4) ; cadre de reprise à déterminer selon l'acte de dissolution et les compétences concernées, sans régime présumé (verifie).
- CGFP L445-1, L445-2 — Reprise d'activité dans un service public administratif ; proposition de contrat et clauses substantielles sous réserve des conditions générales d'emploi, à articuler avec le dispositif spécial après vérification (verifie).
- CGFP R253-7, 1° — Compétence du CST sur les projets d'organisation des services (verifie).
- Dossier réellement fourni : [Code général des collectivités territoriales](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038922544), passages L5212-33, L5211-4-1, L5211-25-1, L5211-26, L5711-4.
- Dossier réellement fourni : [Code général de la fonction publique](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044426064), passages L445-1, L445-2, L445-3, L253-5, R253-7.

Liste exhaustive des identifiants et critères : [jeuBJSON](cases-b.json).

### B-11 — Scoring de promotion

**Question**

Le 12 octobre 2026, la DRH d'une collectivité de 520 agents (>350) souhaite déployer un outil de scoring automatisé pour prioriser les candidatures internes aux tableaux d'avancement de grade. L'outil attribue un score à chaque agent éligible à partir des données du SIRH (ancienneté, évaluations, formations suivies). Le DPO signale un risque lié à l'article 22 du RGPD. Le CST demande à être consulté. La DRH doit piloter la gouvernance sans déléguer au DPO ni à la DSI la décision sur les critères d'avancement. Produire une note de cadrage juridique et de gouvernance.

**Critères obligatoires — intégration**

- **B-11-i01** : Analyse si l'outil relève de l'article 22 RGPD en examinant les effets réels du classement (exclusion effective de candidats du vivier, effets juridiques ou significatifs) et le degré réel d'intervention humaine sur chaque inscription finale au tableau ; examine les exceptions de l'art. 22 §2 a-c et les garanties du §3 ; ne présente pas une validation humaine formelle comme une obligation fondée sur l'article 22 lui-même.
- **B-11-i02** : Qualifie le projet pour identifier la base de consultation du CST applicable parmi R253-7, 1° (organisation des services), 11° (critères d'appréciation de la valeur professionnelle) ou 8° et 12° (LDG promotion et taux d'avancement), et précise que la consultation doit précéder la mise en production.
- **B-11-i03** : Délimite les rôles : l'AIPD est conduite par le responsable du traitement avant le traitement selon l'art. 35 §1 RGPD, et requise notamment dans l'hypothèse du §3 a ; le DPO conseille selon l'art. 35 §2 et l'art. 39 §1 c ; la DSI assure le déploiement technique ; la décision sur les critères de scoring et les inscriptions au tableau relève de l'autorité territoriale compétente selon les LDG et délégations locales, et non du DPO ou de la DSI.

**Échecs — intégration**

- Conclut sur la qualification art. 22 RGPD par la seule présence d'une validation humaine formelle sans examiner les effets réels du classement
- Attribue à la DRH seule la compétence exclusive des inscriptions au tableau sans identifier les LDG et délégations locales
- Omet la qualification du projet pour déterminer la base de consultation du CST applicable

**Critères obligatoires — dégradé**

- **B-11-d01** : Signale que la qualification de l'outil au regard de l'article 22 RGPD dépend du paramétrage réel et des effets effectifs du classement, et que cette qualification doit être établie avant tout déploiement, sans la certifier a priori.
- **B-11-d02** : Collecte les variables manquantes décisives : critères exacts de scoring retenus, degré d'intervention humaine dans la décision finale, LDG locales en vigueur, délégation de signature applicable aux inscriptions au tableau.
- **B-11-d03** : Prépare les informations sur les opérations, finalités, effets, personnes concernées, données et garanties permettant la vérification de la nécessité d'une AIPD ; cite l'article 35 RGPD comme piste sans certifier ses conditions ni l'obligation ou la dispense.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable, même avec une réserve ; les faits fournis et les références posées comme pistes de recherche restent admis.
- Omet le paramétrage exact, les effets réels, les LDG ou les délégations locales comme variables décisives à collecter.
- Omet d'identifier qui décide des inscriptions au tableau selon les LDG et délégations locales ou de préparer les informations utiles à la vérification de l'AIPD.

**Sources annoncées et réserves**

- RGPD art. 22 (dispositif EUR-Lex CELEX:02016R0679-20160504) — Décision fondée exclusivement sur traitement automatisé produisant des effets juridiques ou significatifs ; exceptions §2 a-c et garanties §3 ; la validation humaine formelle n'est pas fondée sur cet article lui-même (verifie_selon_complement_2026-10-14).
- CGFP R253-7, 1°, 8°, 11°, 12° — Compétence du CST sur organisation des services, LDG promotion, critères d'appréciation de la valeur professionnelle, taux d'avancement (verifie).
- RGPD art. 35 et 39 §1 c (dispositif EUR-Lex CELEX:02016R0679-20160504) — AIPD conduite par le responsable avant le traitement (35 §1), requise notamment au §3 a ; conseil du DPO (35 §2 et 39 §1 c) (verifie_selon_complement_2026-10-14).
- Source RGPD à relire : [PDF consolidé EUR-Lex archivé](../rapports/rgpd-2026-10-14/CELEX-02016R0679-20160504-FR-consulte-2026-10-14.pdf) ; identifiant requis `CELEX:02016R0679-20160504` ; [provenance et empreinte](../rapports/rgpd-2026-10-14/provenance.json), [articles et pages par cas](../rapports/rgpd-2026-10-14/articles-rgpd.json).
- Dossier réellement fourni : [Code général de la fonction publique](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044425506), passages L522-24, L522-27, L253-5, R253-7.

Liste exhaustive des identifiants et critères : [jeuBJSON](cases-b.json).

### B-12 — Insuffisance et signalement

**Question**

Le 12 octobre 2026, dans une collectivité de 480 agents (>350), un agent titulaire de catégorie B fait l'objet d'une procédure engagée depuis trois semaines en vue de son licenciement pour insuffisance professionnelle (L553-1 3° et L553-2 CGFP), conduite selon les formes de la procédure disciplinaire. Durant cette même période, il dépose auprès de la DRH un signalement de harcèlement moral dirigé contre son supérieur hiérarchique direct, auteur du rapport ayant fondé l'engagement de la procédure. L'agent invoque une protection contre les mesures défavorables et demande la suspension de la procédure en cours. La DRH doit déterminer si le signalement suspend la procédure, comment instruire les deux procédures sans confusion, et comment assurer la protection de chaque partie.

**Critères obligatoires — intégration**

- **B-12-i01** : Qualifie la procédure en cours comme licenciement pour insuffisance professionnelle (L553-1 3°, L553-2 CGFP) conduit selon les formes disciplinaires, en la distinguant d'une sanction disciplinaire, et analyse si le signalement de harcèlement peut légalement la suspendre en identifiant les textes applicables et les incertitudes à vérifier.
- **B-12-i02** : Identifie la protection contre les mesures défavorables prises en raison du signalement en la rattachant directement à L133-3 ; distingue la portée de L135-4, qui ne cite pas expressément le licenciement pour insuffisance. Analyse le conflit identifié et recommande une organisation impartiale de l'instruction.
- **B-12-i03** : Distingue les objets et décisions des deux procédures ; propose une organisation impartiale adaptée au conflit identifié, sans présenter des acteurs entièrement distincts comme une obligation générale ; identifie les vérifications locales nécessaires et assure confidentialité et examen des besoins de protection de chaque partie, appréciés selon leurs conditions, notamment L134-5.

**Échecs — intégration**

- Qualifie la procédure de sanction disciplinaire sans distinguer le licenciement pour insuffisance professionnelle conduit selon les formes disciplinaires
- Certifie que le signalement suspend ou ne suspend pas automatiquement la procédure sans identifier les textes applicables
- Instruit ou analyse les deux procédures comme une seule démarche fusionnée

**Critères obligatoires — dégradé**

- **B-12-d01** : Signale que la question de la suspension de la procédure de licenciement par le signalement de harcèlement est une question juridique à vérifier dans les textes et la jurisprudence administrative avant toute décision, sans certifier ni la suspension ni la non-suspension.
- **B-12-d02** : Collecte les variables manquantes décisives : stade exact de la procédure au moment du signalement, existence d'une procédure interne formalisée de recueil des signalements, modalités locales inconnues ; une copie du signalement peut être demandée pour en documenter le contenu, sans remettre en cause la qualification de harcèlement moral déjà annoncée.
- **B-12-d03** : Signale le risque de confusion des procédures comme enjeu de sécurité juridique majeur et recommande à titre conservatoire une organisation impartiale, sans certifier qu'une modalité précise est légalement obligatoire sans vérification.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable, même avec une réserve ; les faits fournis et les références posées comme pistes de recherche restent admis.
- Omet la protection de l'agent signalant (L133-3, L135-4) comme référence à vérifier, ou présuppose l'existence d'une procédure interne formalisée de signalement sans que le prompt l'indique.
- Omet de préparer une organisation impartiale conservatoire adaptée au conflit identifié.

**Sources annoncées et réserves**

- CGFP L553-1 3°, L553-2 — Licenciement pour insuffisance professionnelle prononcé selon la procédure disciplinaire ; distinction avec sanction disciplinaire (verifie).
- CGFP L133-2, L133-3, L134-5, L135-4, L135-6 — Harcèlement moral ; protection de l'agent signalant contre mesures défavorables selon leurs conditions ; protection fonctionnelle ; dispositif de recueil des signalements (verifie).
- Loi 2016-1691 art. 6, 8, 10-1 — Qualification de l'alerte selon l'art. 6 I ; voie interne ouverte aux personnes candidates à un emploi (8 I-A 1°) ; interdiction des représailles, dont licenciement et mesures disciplinaires (10-1 II) ; textes en vigueur depuis le 01/09/2022 selon le complément (verifie_selon_complement_2026-10-14).
- Dossier réellement fourni : [Code général de la fonction publique](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044425184), passages L553-1, L553-2, L133-1, L133-2, L133-3, L135-1, L135-4, L135-5, L135-6, L134-1, L134-5, R135-1, R135-2, R135-3, R135-4, R135-5, R135-6, R135-7, R135-8, R135-9, R135-10.

Liste exhaustive des identifiants et critères : [jeuBJSON](cases-b.json).
