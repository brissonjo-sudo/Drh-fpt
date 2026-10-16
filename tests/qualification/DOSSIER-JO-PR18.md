# PR18 — Dossier de validation des jeux A et B

**État : à relire par Jo. Aucun gel, aucun cas de qualification exécuté.**

## Décision attendue

Valider les 24 questions, leurs critères/échecs dans les deux modes et les quatre profils ci-dessous. Le plan approuvé exige cette validation concrète avant tout gel. Une remarque peut conduire à corriger le dossier avant son approbation.

Après accord : A est exécuté une fois sur chaque profil. Un changement après ouverture consomme A ; B reste la réserve, utilisable uniquement après échec de A. Un échec de B termine ce cycle sans qualification.

Seuil fixé avant lancement : 100 % des critères obligatoires, aucune erreur juridique confirmée. Jo arbitre les jugements contestés avec motifs et sources ; un doute non tranché bloque. Le style est indicatif. Les scores bruts et décisions humaines restent séparés.

## Profils proposés

| Répondant | Juge | Modes | Contexte |
|---|---|---|---|
| Codex `gpt-6.1-sol`, high | Claude `claude-opus-5-5`, high | intégration + dégradé | assemblage sélectif |
| Claude Code `claude-opus-5-5`, high | Codex `gpt-6.1-sol`, high | intégration + dégradé | activation native des skills |

Versions effectives relevées le **14/10/2026 à 21:10 UTC (23:10 à Paris)**, par les résolveurs du harnais (`suites.cli_versions` et `claude_cli.executable`) : Codex `codex-cli 0.162.0-alpha.17.2` ; Claude `2.1.288 (Claude Code)`. [Configuration complète](profiles-v1.json). Aucun remplacement silencieux. Ces versions sont à recontrôler avant tout gel.

### Mise à jour des profils Claude — 14 octobre 2026 (T70)

Décision de Jo, depuis `7b5450c` : répondant natif `claude-opus-5-5` et juge Claude `claude-opus-5-5` dans les quatre profils ; Codex `gpt-6.1-sol`, efforts `high`, modes et contextes inchangés. Les constantes `DEFAULT_MODEL` et `DEFAULT_JUDGE_MODEL` de `tests/campaign.py`, utilisées par `--model` et `--judge-model` lorsqu'ils sont omis, valent toutes deux `claude-opus-5-5`. Le parseur accepte ces chaînes sans imposer de modèle différent. Les quatre profils de qualification exigent toujours les modèles et fournisseurs explicites du tableau, sans substitution.

Révision demandée par Jo depuis `e2cf46b` : juge Opus 5.5 dans les deux profils Codex ; profils natifs inchangés (juge `gpt-6.1-sol`) ; répondant et juge par défaut tous deux Opus 5.5. Cette préparation remplace la proposition de poussée T70 ; `e2cf46b` ne doit pas être poussé comme tête du candidat. Aucun gel.

Exécutables effectivement résolus sur ce poste : Claude `C:\Users\Krn\.local\bin\claude.exe` ; Codex `C:\Users\Krn\AppData\Local\OpenAI\Codex\bin\2e5e00daee91c61d\codex.exe`. La commande PowerShell `claude --version` renvoie elle aussi `2.1.288 (Claude Code)` lors du contrôle ; le `2.1.133` signalé par Jo n'est pas reproduit dans cet environnement. Le `2.1.277` des anciens profils est remplacé par la version constatée, sans installation ni mise à jour de CLI pendant ce tour.

**Acceptation effective d’Opus 5.5 : non vérifiée.** Lors de la préparation initiale de T70, deux sondes minimales (Opus 5.5 et Sonnet 5.5) ont été préparées hors `campaign.py`, sans charger les jeux A/B ni appeler `suites.claim_launch`. Pour les deux identifiants, `claude_cli.complete_cli` s'arrête dans la vérification OAuth préalable : « OAuth expiré ou moins d'une heure restante ». Aucun sous-processus d'inférence n'est lancé, aucun appel modèle ni créneau de qualification consommé ; aucun fallback et aucun contournement de ce garde-fou. Reconnexion par le flux normal puis sondes isolées à revalider avant gel. La [documentation officielle des modèles](https://code.claude.com/docs/en/model-config) et la [référence CLI](https://code.claude.com/docs/en/cli-reference), consultées le 14/10/2026 après indisponibilité de Context7 (quota), documentent les identifiants exacts et `--model` ; elles ne prouvent pas l'accès effectif de ce compte.

Contrôles locaux du remplacement de T70 du 14/10/2026, relancés après alignement des profils et des deux constantes depuis `e2cf46b` : **125/125 tests déterministes en cp1252**, puis les mêmes **125/125 en UTF-8** ; cohérence et `build_bundle.py --check` réussis dans les deux environnements. Avertissement conservé : tag `v0.7.0` absent, contrôle de l’incrément de version ignoré. Empreinte brute des profils recalculée après écriture et comparée à `suites.file_sha` ; empreintes des jeux A/B inchangées et recontrôlées. Ces contrôles ne prouvent pas l’accès aux modèles ; aucun gel ni qualification réelle.

Les octets de `cases-a.json` et `cases-b.json`, dont `final_revision_model` (provenance historique), sont inchangés. Les preuves et rapports historiques ne sont pas réécrits. Les paragraphes datés des corrections juridiques décrivent leur propre périmètre antérieur ; la présente décision modifie uniquement les profils courants, leurs valeurs par défaut et ce dossier. Aucun gel ni campagne n'est exécuté.

En intégration native, les deux skills sont demandés explicitement et les documents officiels sont préconsultés. Tous les fragments et fichiers obligatoires doivent être effectivement reçus intégralement. Cela ne teste ni la recherche autonome via le serveur juridique ni la co-activation automatique sans demande explicite.

En dégradé : pas de compagnon ni de source. Les faits fournis restent utilisables ; les règles, compétences, durées, plafonds et procédures ne peuvent être certifiés, même avec réserve. Une réponse doit préparer utilement la vérification et la décision conditionnelle.


## Préparation du 15 octobre 2026 — T71 (partielle, sans gel)

Depuis `11ead2c`, le parseur Claude accepte les plugins dont l'identifiant (`source` lorsqu'il est présent, sinon `name` ou la chaîne reçue) se termine par `@builtin`. Ils sont conservés dans la trace brute et dans `usage.plugins` / `usage.builtin_plugins`. Les autres plugins restent refusés hors du seul plugin candidat exigé pour le runtime natif ; ce candidat et son catalogue restent obligatoires. Deux tests supplémentaires couvrent builtin seuls acceptés, conservation de la trace, runtime natif et rejet d'un plugin non builtin même mêlé aux builtin.

Sonde réelle du 15/10 à 00:17 Paris (14/10 22:17 UTC) : Claude Code 2.1.288, effort high, invite triviale, garde-fou OAuth accepté ; réponse OK, modèle renvoyé `claude-opus-5-5`, trois plugins builtin consignés, aucun outil/MCP ni cas A/B. La trace corrigée est acceptée par le harnais.

**Isolation Codex non résolue.** Sur `codex-cli 0.162.0-alpha.17.2`, les deux essais locaux ont laissé dans stderr le chargement refusé du skill global `C:\Users\Krn\.agents\skills\recherche-juridique\SKILL.md` (description manquante). `--enable skip_host_skill_discovery`, listé under development par le CLI mais non décrit dans les pages publiques consultées, n'isole pas `codex exec` et émet en plus un avertissement rejeté par l'adaptateur. Le diagnostic prompt-input n'a pas permis de distinguer les deux situations et n'est pas une preuve d'isolation. La désactivation par chemin `skills.config` / `enabled=false`, appliquée uniquement par `-c` selon la documentation publique, permet la réponse OK mais ne supprime pas l'erreur de chargement. Ces deux essais sont retirés du candidat ; l'adaptateur Codex est inchangé. Aucun mécanisme documenté efficace n'a été établi sur cette version ; la preuve demandée d'un stderr sans chargement de skill n'est pas obtenue. Aucun fichier ou réglage utilisateur n'est modifié.

Les événements Codex réellement reçus contiennent thread.started, turn.started, item.completed et turn.completed ; aucun champ attestant le modèle. Mention proposée à Jo : **« gpt-6.1-sol : modèle demandé, non attesté »**. Cette proposition n'est pas une validation implicite de l'identité ni une qualification. Aucune valeur d'attestation n'est fabriquée dans le harnais.

Sources techniques consultées le 15/10 : [référence CLI](https://learn.chatgpt.com/docs/developer-commands?surface=cli), [configuration](https://learn.chatgpt.com/docs/config-file/config-reference), [skills](https://learn.chatgpt.com/docs/build-skills), aide/features du CLI installé. Context7 tenté en premier, quota épuisé. La documentation distingue l'absence de config utilisateur et la découverte des skills ; la désactivation documentée d'un skill ne constitue pas ici une preuve d'absence de chargement.

Contrôles relancés : les **125 tests existants + 2 nouveaux**, soit **127/127 en cp1252**, puis les mêmes **127/127 en UTF-8** ; cohérence et bundle réussis dans les deux encodages. Avertissement conservé : tag v0.7.0 absent, contrôle de l'incrément ignoré. Empreintes brutes des profils et jeux A/B recontrôlées et inchangées ; provenance historique conservée.

Trois appels réels triviaux au total (un Claude, deux essais Codex), hors campagne et sans cas de qualification. Registres JSON et résultats comparés avant/après : contenus et horodatages inchangés. Le skill global n'est ni réparé ni modifié. Zéro tentative de qualification consommée, aucun gel, aucun push. La correction Claude est prête à relire ; l'isolation Codex reste un blocage avant qualification.


## Décisions de Jo du 15 octobre 2026 — préparation T72

**Identité Codex acceptée par Jo : « gpt-6.1-sol : modèle demandé, non attesté ».** Cette mention accompagne chaque nouvelle trace Codex (répondant, juge et échec/timeout), dans un en-tête `harness.model_identity` attribué explicitement à `local_harness`. `requested_model` porte le modèle demandé, `returned_model` reste nul et `attestation` vaut `requested_unattested`. L'en-tête contient l'empreinte SHA-256 des événements fournisseur ; ceux-ci sont conservés après l'en-tête, sans modification. Les métriques portent aussi cette mention. Il s'agit d'une annotation décidée par Jo, pas d'une identité certifiée par le fournisseur. Aucune trace ni preuve historique n'est réécrite.

**Isolation Codex : quarantaine temporaire retenue**, exclusivement dans la fenêtre de campagne et après accord explicite de Jo à ce moment. [Procédure préparée](PROCEDURE-QUARANTAINE-CODEX.md) : contrôle des chemins et empreintes, déplacement hors `.agents/skills` dans un dossier daté, sonde triviale sans chargement de skill dans stderr, campagne seulement si tous les prérequis sont validés, puis restauration avec comparaison des empreintes même si la sonde ou la campagne échoue.

Contrôles T72 : les mêmes **127/127 tests en cp1252**, puis **127/127 en UTF-8**, cohérence et bundle réussis. Syntaxe des quatre blocs PowerShell et du code Python de sonde vérifiée sans exécution. Les tests couvrent l’en-tête d’identité sur succès, timeout et échec, la préservation des événements fournisseur et la compatibilité du contrôle de traces ; aucune sonde réelle relancée dans ce tour.

Cette procédure n'est pas exécutée lors de la préparation T72. Le dossier global reste en place et intact ; aucune sonde d'isolation après déplacement n'est prétendue réalisée. Le choix opératoire est arrêté, mais sa preuve reste à établir au moment autorisé. Aucun gel ni autorisation implicite de campagne. Les seuils, 24 cas, modèles/efforts et empreintes brutes des jeux/profils restent inchangés.


## Relecture des 24 cas du 15 octobre 2026 — préparation T73

Source du premier lot : [rapport fourni par Jo](../rapports/relecture-24-cas-2026-10-15.md), SHA-256 `d6594cfafb4c53c439c44522d15ba47dc49e96df10917f27e7a0f4f99f53346f`. La section finale « Points juridiques vérifiés » prime sur les propositions antérieures ; il s'agit de vérifications rapportées par Claude et ses agents, pas de nouvelles consultations par Codex. Aucun article, identifiant ou règle n'est ajouté de mémoire.

Les cinq corrections transverses sont appliquées avant les corrections A/B : hypothèse distincte de certification, attendus composites scindés avec identifiants stables et suffixes pour les nouveaux items, source vérifiée citée plutôt que présence dans le dossier, articles présents dans l'énoncé évalués pour leur articulation, et « vérifié » défini comme une preuve de consultation exploitable en intégration. Le mode dégradé n'exige aucune référence précise. Les seuils restent100% des critères obligatoires, zéro erreur juridique confirmée, doute non arbitré bloquant ; la scission change le nombre de critères à relire, pas le seuil.

En particulier : B-10 conserve L445-1/2 pour les contractuels et attend une conclusion suspendue sur les titulaires sans mécanisme établi ; le CST de la communauté de380agents est propre. B-02 utilise R253-58 à63 avec la réserve explicite R253-61 et exclut les articles5-2/5-3 abrogés du décret85-603. B-04 est borné à la partie législative lue. A-07 retient la variante deux ans deCDI après six ans deCDD. A-10 n'impose pas une différence statutaire sans source ni un échec « charte/accord ». A-11 n'exige aucune autorité médicale nommée non établie par les textes du rapport.

**Énoncés A-10/B-10 intégrés après validation de Jo du 15/10/2026** : [texte approuvé et provenance](PROPOSITIONS-A10-B10-2026-10-15.md). A-10 est repris tel que proposé. B-10 décrit désormais un syndicat mixte dont la communauté est membre avec plusieurs communes, et la reprise des compétences et de l'activité du syndicat. L'adhésion, l'arrêté et la date d'effet sont des faits du scénario validés par Jo. Cette validation ciblée ne vaut pas approbation globale des 24 cas ni gel. [Liste « non traité »](NON-TRAITE-RELECTURE-2026-10-15.md) maintenue pour les autres réserves.

Empreintes brutes A/B recalculées après écriture, reportées ci-dessous et comparées à `suites.file_sha`. Profils et `author_provenance`/`final_revision_model` inchangés. Sources et traces historiques conservées ; aucun modèle, gel, campagne, déplacement du skill global ou push dans ce tour.

Contrôles locaux du premier candidat T73 (`a38507e`) du 15/10/2026 :127tests déterministes réussis sous cp1252 et127sous UTF-8 ; encodage effectif confirmé pour chaque exécution. Cohérence et `build_bundle.py --check` réussis dans les deux environnements. Cinq avertissements non bloquants de cohérence : quatre chemins de documentation absents du bloc Structure du README (dont la procédure de quarantaine préexistante), et tag `v0.7.0` absent de cette copie. Aucun appel modèle réel ; seules les fixtures temporaires des tests ont exercé le harnais. Les registres et profils de qualification restent inchangés ; aucun gel ni tentative consommée.

### Complément T73 — intégration des énoncés validés le 15 octobre 2026

Depuis `a38507e`, Jo valide A-10 tel que proposé et B-10 avec les deux corrections de formulation ci-dessus. Le nouvel identifiant `LEGIARTI000044190730` (CGCT L5711-1), explicitement fourni par Jo et relu par Claude selon son message, est ajouté aux sources requises de B-10 ; l'attendu B-10-i01 articule cette qualification avec L5212-33. Aucune nouvelle consultation primaire par Codex, aucune référence de mémoire et aucun article cité dans l'énoncé B-10. Les autres critères, seuils, profils et provenances historiques sont conservés. Les quatre chemins manquants sont ajoutés au seul bloc Structure du README.

Les empreintes brutes A/B sont recalculées après intégration, reportées à la section Empreintes exactes et comparées à `suites.file_sha`. La poussée du nouveau candidat reste soumise à validation séparée ; aucun gel ni campagne.

Contrôles après intégration des énoncés, le 15/10/2026 : **127/127 tests en cp1252**, puis **127/127 en UTF-8** ; encodages effectifs confirmés. Cohérence et `build_bundle.py --check` réussis dans les deux environnements. Les quatre avertissements README sont corrigés ; seul demeure l'avertissement préexistant sur le tag `v0.7.0` absent de cette copie, avec contrôle d'incrément de version ignoré. Les empreintes brutes A/B sont vérifiées par recalcul et par `suites.file_sha`. Aucun appel modèle réel, aucun registre de qualification modifié, aucune tentative consommée. Les preuves historiques restent intactes.


## Réconciliation documentaire T74 — 15 octobre 2026

Préparation locale depuis `0a483f6`, sans poussée ni gel. [Écarts et décisions](RECONCILIATION-SOURCES-2026-10-15.md) ; [registre exhaustif des attendus et identifiants](reconciliation-sources-2026-10-15.json).

Huit identifiants déjà visés par les sources/attendus sont ajoutés : A-07 L332-9/10/11, A-10 R433-1 (CGFP, sans confusion avec l'article homonyme du CPCE), B-02 R253-58/59/62/63. Numéro, identifiant, texte et version sont retrouvés dans les codes complets archivés ; cette lecture locale du 15/10 ne devient pas une nouvelle consultation primaire. Leurs liaisons historiques de cas restent à préparer avant qualification.

Selon la correspondance explicitement donnée dans le complément du rapport Claude du 14/10 : article 8 de la loi 2016-1691 retiré des sources obligatoires de B-09 (piste facultative conservée) ; articles 6 et 8 retirés de B-12, dont le périmètre est limité à 10-1 II depuis T73. Les réponses primaires de ces articles ne figurent pas dans les archives examinées. Le chemin CLI PISTE n'a pas d'identifiants disponibles dans ce contexte ; la récupération web des trois fiches a renvoyé 403. La correspondance figurait déjà dans le rapport : T74 corrige la réserve T73 « mapping non fourni ». Elle reste attribuée au rapport, sans certification indépendante nouvelle.

Les 299 traces historiques examinées, dont 234 liées aux jeux A/B, ne présentent pas d'écart structurel selon le vérificateur existant (empreintes, requêtes, extraits et versions). Elles dépassent toutes la fenêtre de fraîcheur de 24 heures à la date de cet audit. Les dates ne sont pas réécrites. Les cinq liaisons PDF/CELEX sont documentées et hashées, mais leur prise en charge par le harnais reste T75. Aucune trace de qualification n'est fabriquée.

Les 24 énoncés, 132 attendus d'intégration, 73 attendus dégradés et clauses d'échec sont inchangés depuis T73. Seuls les identifiants et la description de source facultative B-09 sont réconciliés. Profils, preuves et provenance historique intacts. Le caractère complet d'une liste d'identifiants ne certifie pas les conséquences juridiques ; les réserves du registre restent à arbitrer par Jo. Aucun gel, tentative ou campagne.

## Ajustements de fin de relecture T76 — 16 octobre 2026

Préparation locale depuis `c8885eb`, sur instructions ciblées de Jo. [Corrections et inventaire à arbitrer](FIN-RELECTURE-2026-10-16.md) ; [registre des 239 liaisons restantes](inventaire-sources-fin-relecture-2026-10-16.json). Les cinq autres ajustements de formulation sont appliqués ; R253-61 n’est ni exigé ni sanctionné, la substitution de B-10 reste conditionnelle, et le doublon A-01-i03-f est supprimé.

D74-4 : sept liaisons retirées seulement (B-10 L5211-4-1, L5211-25-1, L5211-26, L445-3, L253-5 ; A-10 R432-3 ; A-11 article 24 du décret85-603). L’article 24 du décret87-602 en A-02 est conservé. Les listes « Dossier réellement fourni » ci-dessous décrivent les archives historiques ; elles ne sont pas la liste des sources encore requises. La liste courante fait foi dans les JSON A/B et le registre T76 ; aucune preuve n’est supprimée.

État courant : **24 cas, 131 critères d’intégration, 73 dégradés, 239 liaisons requises et 214 identifiants uniques**. Le constat T74 de132critères est historique. Les49liaisons sans attendu propre retrouvé et 65 rattachements implicites sont listés sans retrait. L’absence d’un numéro dans un critère n’est pas assimilée à l’absence de lien juridique. Les classements de sens restent à arbitrer ; ils ne modifient pas les seuils. Profils, provenance de rédaction et preuves historiques inchangés. Réserves, T29 et préparation PDF/CELEX T75 maintenues. Aucun gel.

Le 16/10/2026 : **127/127 tests déterministes en cp1252**, puis **127/127 en UTF-8**, sans échec ni test ignoré ; encodages effectifs contrôlés. Cohérence et `build_bundle.py --check` réussis dans les deux environnements. Seul avertissement : tag `v0.7.0` absent de la copie, contrôle d’incrément ignoré. Empreintes brutes A/B/profils comparées à `suites.file_sha` et au dossier ; profils et registre `suites.json` inchangés, contenus et horodatages contrôlés. Aucun appel modèle réel, aucun gel ni tentative consommée.

## Préparation runtime T75 — 16 octobre 2026

Jo a relu T77 et différé sa signature jusqu’au commit runtime final. [Bilan T75](T75-PDF-CELEX-2026-10-16.md) : validation dédiée du PDF/CELEX figé et de son index, cinq traces de lecture locale datées réellement, tests de refus après altération. La lecture d’archive est distinguée de la consultation primaire rapportée du 14/10, heure inconnue ; aucune prétention à une nouvelle consultation EUR-Lex ni à la vigueur actuelle. Les anciens paragraphes disant PDF non compatible décrivent l’état historique antérieur à T75.

Pour la loi 2016-1691, les deux identifiants fournis sont repris comme pistes attribuées à Claude, mais aucune nouvelle preuve primaire obtenue : identifiants PISTE absents du contexte normal du CLI utilisé, puis HTTP 403 sur les pages officielles. Les 3 liaisons B-09/B-12 restent à documenter par récupération primaire. Aucun texte, statut ou trace valide fabriqué. Les 20 liaisons historiques et la fraîcheur des autres sources restent à préparer.

Jeux A/B, profils, PDF, index et archives historiques inchangés. Conservation des 49 liaisons sans attendu propre et 65 rattachements implicites confirmée par Jo ; aucun retrait. Aucun sceau ni campagne. Un nouvel acte non signé accompagnera le candidat runtime.

Le16/10/2026 : **137/137 tests déterministes en cp1252 et 137/137 en UTF-8**, soit 127 existants et 10 nouveaux tests PDF, sans échec ni test ignoré. Cohérence et `build_bundle.py --check` réussis dans les deux environnements ; seul avertissement préexistant : tag v0.7.0 absent. A/B/profils/PDF etindex restent inchangés ; hashes bruts A/B/profils concordants avec `suites.file_sha`. Le registre `suites.json` reste inchangé, aucun sceau, tentative ou appel modèle.

## Pièce de consultation Claude reçue le 16 octobre 2026 — T79

[Pièce archivée et diagnostic du format](T79-ARCHIVE-LOI-2026-10-16.md). SHA-256 brut de la pièce fournie par Jo : `78da546dd2d3785c4a75f925e3cb28cbc34bc0638fd2623c4acc53f17cc7550c`, copie à l’identique recontrôlée. Articles 6 et 10-1 récupérés par Claude via MCP `get_article`, en vigueur au 16/10/2026, version 01/09/2022 selon la consultation rapportée ; texte recopié depuis la réponse de l’outil, octets API originaux non disponibles. Horodatage rapporté conservé verbatim, sans heure exacte inventée par appel.

Les textes et métadonnées sont maintenant présents dans cette pièce pour les 3 liaisons B-09/6, B-09/10-1, B-12/10-1. Le harnais ne peut pas comparer la transcription à la réponse source originale absente : aucune trace de campagne n’est fabriquée, aucun contrôle assoupli, aucune exemption. Demande complémentaire précise dans le rapport : réponse API consolidée et requête archivées via le collecteur, ou export MCP original à évaluer avec son schéma. Les anciens constats d’absence de texte restent historiques.

Empreintes A/B/profils/PDF inchangées, sources requises conservées. Signature différée au runtime final ; acte actualisé non signé. Aucun gel ni campagne.

Le 16/10/2026 : **137/137 tests déterministes en cp1252 et 137/137 en UTF-8**, sans échec ni test ignoré ; cohérence et `build_bundle.py --check` réussis dans les deux environnements. Seul avertissement préexistant : tag v0.7.0 absent. Empreintes A/B/profils inchangées et concordantes avec `suites.file_sha`. Pièce copiée à l’identique, hash recalculé concordant. Validateur, schéma, campagne et support PDF identiques à 019bce2 ; registre de suites inchangé. Aucun gel, appel modèle ou tentative de campagne.

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

- Jeu A : `c7958f40a2938e67bc62a2f9b579b39f9f59d790dcce0eb70944b9db78b1141c`
- Jeu B : `8e7c303417e91fc7415606ba478e1f87553506674ef39157f9e6bb7008447262`
- Profils : `65301665ed0e9b1b2d1b613f2e4ba4baf5e4ae36dc7e65fb12de3610e7cc4c29`
- Archive primaire : `467bd64c3537f98e0793412f581aef496520edb3767a40736118f7a0666eb090`

Le commit exact est joint à la demande d’approbation après publication du candidat propre. Aucun sceau humain n’est créé à ce stade.

## Jeu A — actif

### A-01 — Cumul d’activités

**Question**

Un agent territorial titulaire occupe un emploi permanent à temps non complet (quotité 60 %) dans une collectivité de 400 agents. Il déclare à son autorité territoriale qu'il envisage d'exercer, à compter du 1er décembre 2026, en dehors de ses heures de service, une activité de consultant indépendant à titre lucratif. L'autorité territoriale s'interroge sur la légalité de cette situation et sur les conditions dans lesquelles elle peut s'y opposer. Date : 12 octobre 2026. Produire une note d'analyse sur le cadre applicable et une décision motivée sur l'opposition ou l'autorisation.

**Critères obligatoires — intégration**

- **A-01-i01** : L123-5 est identifié comme base de la dérogation : un agent occupant un emploi permanent à temps non complet avec une durée ≤70 % de la durée légale peut exercer une activité privée lucrative ; la compatibilité avec l'interdiction générale de L123-1 est explicitée.
- **A-01-i02** : L'obligation déclarative (L123-6, R123-6) est distinguée de l'autorisation préalable : la déclaration porte sur l'activité envisagée. Son caractère préalable est explicité comme une déduction de R123-6, sans exiger que le texte utilise ce mot.
- **A-01-i03** : Identifie et applique aux faits le motif d'opposition tenant à l'intérêt du service (R123-2).
- **A-01-i03-b** : Identifie et applique aux faits le motif d'opposition tenant aux informations inexactes (R123-2).
- **A-01-i03-c** : Identifie et applique aux faits le motif d'opposition tenant à l'incompatibilité déontologique (R123-2).
- **A-01-i03-d** : Distingue l'absence de motif d'opposition établi d'une compatibilité démontrée.
- **A-01-i03-e** : Fournit une position motivée sur les éléments acquis ou, si nécessaire, un projet conditionnel précisant les seules informations manquantes.

**Échecs — intégration**

- L123-5 n'est pas identifié ou le régime de l'activité accessoire autorisée (L123-7) est appliqué à la place.
- L'obligation déclarative est présentée comme une obligation d'autorisation préalable.
- Les motifs d'opposition (R123-2) ne sont pas distingués ou un motif non prévu est certifié.
- Aucune décision motivée ni projet de décision conditionnel n'est produit.

**Critères obligatoires — dégradé**

- **A-01-d01** : La quotité de 60 % est prise comme acquise ; les informations manquantes sont listées : fonctions exercées par l'agent, nature et compatibilité de l'activité avec les fonctions, existence d'un conflit d'intérêts ou d'un lien avec les missions.
- **A-01-d02** : Aucune règle juridique n'est certifiée : le cadre est présenté sous forme de questions à instruire (régime applicable, obligation déclarative ou d'autorisation, motifs d'opposition) sans conclure sur la licéité.
- **A-01-d03** : Un projet de décision conditionnel est proposé avec champs à compléter ; toute certification non vérifiée est un échec.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable ou certifiée ; nommer un régime, une distinction ou une référence comme hypothèse à vérifier n'est pas une certification. Les faits fournis restent acquis.
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

- **A-02-d01** : Les variables bloquantes sont identifiées : certificat médical transmis avec quotité/durée/modalités prescrites, avis du médecin agréé formalisé, existence de fonctions à conditions de santé particulières, droits à congé restants et perspective de réintégration.
- **A-02-d02** : Sans source, aucune procédure juridique n'est certifiée : compétences, délais et rôle du conseil médical sont présentés comme des points à vérifier avant tout engagement.
- **A-02-d03** : Une organisation de reprise conditionnelle est proposée ; les points non vérifiés (primes, rôle éventuel de la médecine préventive à rechercher) sont explicitement signalés comme à confirmer.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable ou certifiée ; nommer un régime, une distinction ou une référence comme hypothèse à vérifier n'est pas une certification. Les faits fournis restent acquis.
- Les variables manquantes (certificat médical transmis, avis agréé formalisé, fonctions à conditions de santé particulières, droits à congé restants et perspective de réintégration) ne sont pas identifiées.
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

Une commune de 600 agents doit pourvoir un emploi permanent vacant de responsable de la cybersécurité (catégorie A). La vacance a été publiée il y a quatre mois ; la procédure de recrutement d'un fonctionnaire n'a pas abouti, comme documenté par le service RH. La direction hésite entre L332-8 2° (recrutement contractuel permanent) et L332-14 (vacance temporaire dans l'attente d'un fonctionnaire). La recherche d'un fonctionnaire se poursuit. La délibération créant l'emploi n'est pas jointe ; sa mention de la possibilité de recruter un contractuel reste à établir. Date : 12 octobre 2026. Produire une note d'aide à la décision comparant les deux fondements et recommandant le choix.

**Critères obligatoires — intégration**

- **A-03-i01** : Identifie sur une source vérifiée citée la justification par les besoins ou la nature des fonctions requise pour L332-8 2°.
- **A-03-i01-b** : Identifie le constat d'infructuosité documenté préalable à l'examen des candidatures non fonctionnaires (R332-9) pour L332-8 2°.
- **A-03-i01-c** : Identifie L332-14 comme une occupation temporaire dans l'attente d'un fonctionnaire.
- **A-03-i01-d** : Identifie la publicité de la vacance relevant de L313-4 pour L332-14.
- **A-03-i01-e** : Motive le choix entre une occupation contractuelle durable justifiée par les besoins ou la nature des fonctions et une occupation temporaire dans l'attente d'un fonctionnaire, sans rendre les démarches légalement exclusives.
- **A-03-i02** : Les durées maximales sont précisées avec bases vérifiées : L332-9 (3 ans renouvelable jusqu'à 6 ans, reconduction expresse pour CDI au-delà, conditions de décompte L332-10) pour L332-8 2° ; L332-14 (1 an, prolongeable jusqu'à 2 ans si procédure fonctionnaire demeurée infructueuse) ; la prolongation de L332-14 est conditionnée à l'échec avéré du recrutement.
- **A-03-i03** : Distingue les pièces établissant la publicité applicable au fondement retenu.
- **A-03-i03-b** : Demande la pièce retraçant le constat préalable d'infructuosité requis pour L332-8 2°.
- **A-03-i03-c** : Documente l'attente d'un fonctionnaire et, en cas de prolongation de L332-14, l'échec de son recrutement.
- **A-03-i03-d** : Demande la justification des besoins ou de la nature des fonctions pour L332-8 2°.
- **A-03-i03-e** : Vérifie si la délibération créant l'emploi prévoit le recrutement d'un contractuel (L313-1) ; faute de pièce, suspend précisément la conclusion sur cette condition.
- **A-03-i03-f** : Prévoit le fondement légal du contrat à partir d'une source vérifiée citée (R331-6 à R331-11).
- **A-03-i03-g** : Pour L332-14, prévoit le motif précis du contrat à partir d'une source vérifiée citée.
- **A-03-i03-h** : Pour L332-14, prévoit le descriptif du poste annexé, sans exiger une énumération exhaustive de clauses non établies.

**Échecs — intégration**

- La distinction entre L332-8 2° et L332-14 n'est pas opérée ou un seul fondement est traité.
- Le constat d'infructuosité documenté (R332-9) est omis.
- Les durées maximales et la condition de prolongation de L332-14 sont ignorées.
- Les mentions contractuelles obligatoires sont certifiées sans source vérifiée citée.

**Critères obligatoires — dégradé**

- **A-03-d01** : La poursuite de la recherche d'un fonctionnaire et l'infructuosité documentée sont prises comme acquises ; leurs pièces sont demandées pour la seule traçabilité. Les informations manquantes sont identifiées : justification des besoins ou de la nature des fonctions, durée prévisible du besoin, délibération créant l'emploi et mention de la possibilité de recruter un contractuel.
- **A-03-d02** : Sans source, aucun régime légal n'est certifié : les deux fondements sont présentés comme des scénarios à instruire, conditions et durées posées comme points à vérifier.
- **A-03-d03** : Une note conditionnelle est produite listant les pièces à réunir selon le scénario retenu, avec indication explicite des points à confirmer avant signature.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable ou certifiée ; nommer un régime, une distinction ou une référence comme hypothèse à vérifier n'est pas une certification. Les faits fournis restent acquis.
- Les informations manquantes (justification des besoins ou de la nature des fonctions, durée prévisible du besoin, délibération créant l'emploi et possibilité d'un recrutement contractuel) ne sont pas identifiées.
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

- **A-04-d01** : L'unanimité du vote défavorable et le caractère délibératoire de la question sont pris comme acquis ; les vérifications portent sur les modalités de séance non décrites : composition et quorum de la première séance. Le recueil éventuel de l'avis du collège employeur peut être mentionné ; son omission n'est pas bloquante en mode dégradé.
- **A-04-d02** : Sans source, aucun délai ni règle de quorum n'est certifié : la procédure de réexamen est présentée comme un point à vérifier ; toute certification non vérifiée est un échec.
- **A-04-d03** : Un plan conditionnel est proposé avec les étapes séquencées ; l'unanimité et le caractère délibératoire étant acquis, les réserves portent sur les modalités de séance non décrites.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable ou certifiée ; nommer un régime, une distinction ou une référence comme hypothèse à vérifier n'est pas une certification. Les faits fournis restent acquis.
- Les modalités de séance non décrites (composition et quorum de la première séance) ne sont pas identifiées ; l'avis du collège employeur reste facultatif dans ce mode.
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

12 octobre 2026, collectivité FPT de 480 agents. Lors de la préparation du budget primitif N+1, la DRH constate que le SIRH présente des écarts d'indice entre la base RH et les bulletins de paie des 18 derniers mois pour une vingtaine d'agents, à la suite d'erreurs de saisie d'échelon lors d'une mise à jour logicielle. Les arrêtés individuels sont conformes ; seules les données de paie sont erronées. Ces écarts génèrent des trop-versés et des sous-versés. Produire un mémo de pilotage : audit et quantification des écarts, obligations de régularisation et délais applicables, impact sur la prévision de masse salariale N+1, alertes coordonnées finances et DSI.

**Critères obligatoires — intégration**

- **A-05-i01** : Distinction des régimes : trop-versé (répétition de l'indu au profit de la collectivité, soumise à prescription biennale, loi 2000-321 art. 37-1, avec exceptions aux alinéas suivants) et sous-versé (créance de l'agent, prescription quadriennale loi 68-1250 art. 1, avec causes d'interruption art. 2).
- **A-05-i02** : Pour les trop-versés : délai de deux ans à compter du premier jour du mois suivant le versement erroné (art. 37-1 al. 1) ; exceptions aux alinéas 2 et 3 vérifiées selon la cause de l'erreur ; modalités de récupération sur paie et information préalable renvoyées à vérification des textes non fournis.
- **A-05-i03** : Rôle de la DSI limité à la correction technique avec traçabilité ; instruction et coordination par la DRH ; validation et décision de régularisation par l'autorité compétente, dont l'identification relève de la collectivité.
- **A-05-i04** : Impact budgétaire intégré à la note de prévision de masse salariale N+1, distinguant la charge récurrente corrigée et le one-shot de régularisation.

**Échecs — intégration**

- Confond le régime du trop-versé et celui du sous-versé
- Certifie des modalités de récupération sur paie non étayées par une source vérifiée citée
- Attribue à la DRH ou à la DSI le pouvoir de décider de la régularisation
- Omet l'impact sur la prévision de masse salariale N+1

**Critères obligatoires — dégradé**

- **A-05-d01** : Recensement des variables manquantes (montants par agent et par versement, dates exactes des versements et pièces permettant de reconstituer les écarts, en utilisant la période et la cause déjà fournies) sans certifier aucun délai, taux ou modalité de récupération.
- **A-05-d02** : Présentation conditionnelle des deux régimes trop-versé/sous-versé, en renvoyant délais et modalités à vérification avant tout acte.
- **A-05-d03** : Plan d'action structuré (audit SIRH → questions de contrôle → notification individuelle → régularisation → note finances) utilisable dès vérification des règles.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable ou certifiée ; nommer un régime, une distinction ou une référence comme hypothèse à vérifier n'est pas une certification. Les faits fournis restent acquis.
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

- **A-06-i01** : Analyse la finalité et la nécessité de l'annuaire pour chaque catégorie de donnée ; ne retient pas l'intérêt légitime et, s'il l'évoque, l'écarte pour les traitements relevant des missions publiques (art. 6 §1 al. 2 RGPD). Examine les bases envisageables des coordonnées professionnelles et leur fondement ; conclut conditionnellement ou suspend précisément le choix si ce fondement manque. Qualifie la base de la photo selon sa nécessité à la finalité retenue.
- **A-06-i02** : Pour les refus de photo, distingue retrait du consentement (art. 7) et opposition selon les conditions de l'article 21 si la base est une mission d'intérêt public. Propose une alternative (initiales ou avatar neutre) ; ne présente ni obligation de publier la photo ni sanction du refus sans base vérifiée.
- **A-06-i03** : Prévoit dans l'information préalable l'identité et les coordonnées du responsable du traitement.
- **A-06-i03-b** : Prévoit dans l'information préalable la finalité et la base légale.
- **A-06-i03-c** : Prévoit les destinataires des données (RGPD art. 13 §1 e).
- **A-06-i03-d** : Prévoit la durée de conservation ou, lorsque ce n'est pas possible, les critères utilisés pour la déterminer.
- **A-06-i03-e** : Prévoit l'information sur les droits d'accès, de rectification et d'effacement.
- **A-06-i03-f** : Prévoit l'information sur le droit d'opposition (RGPD art. 13 §2 b).
- **A-06-i03-g** : Prévoit les coordonnées du DPO.
- **A-06-i03-h** : Si le consentement est retenu comme base, prévoit l'information sur le droit de retrait.
- **A-06-i03-i** : Prévoit le droit de réclamation (RGPD art. 13 §2 d).
- **A-06-i03-j** : Si la donnée n'est pas collectée auprès de l'agent, examine l'information relevant de l'article 14.
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

- Une règle juridique non vérifiée est présentée comme applicable ou certifiée ; nommer un régime, une distinction ou une référence comme hypothèse à vérifier n'est pas une certification. Les faits fournis restent acquis.
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

12 octobre 2026, collectivité FPT de 480 agents. Un agent contractuel en CDI de droit public recruté sur le fondement de l'article L332-8 2° du CGFP pour un emploi de chargé de mission numérique (catégorie A) est en CDI depuis deux ans, après six ans de CDD sur cet emploi. Il demande par écrit une révision de sa rémunération en invoquant l'évolution significative de ses missions, l'expertise acquise et la comparaison avec la grille indiciaire des attachés. Produire une note d'analyse et un projet d'avenant conditionnel : règles de fixation et de réévaluation de la rémunération d'un CDI contractuel, qualification des changements de fonctions, procédure et éléments à documenter.

**Critères obligatoires — intégration**

- **A-07-i01** : Règles applicables : CGFP L713-1 (fonctions, qualification requise, expérience) ; décret 88-145 art. 1-2 (réévaluation au moins tous les trois ans pour les CDI, notamment au vu des entretiens ou de l'évolution des fonctions) ; premier contrôle : date de la dernière réévaluation effectuée ; distinction entre réévaluation périodique et augmentation discrétionnaire.
- **A-07-i02** : Qualification des changements allégués : distinction évolution normale de l'emploi et éventuelle modification substantielle dont la qualification et les suites restent à vérifier ; les critères précis et formalités applicables (R331-12, R331-13) doivent être vérifiés sur les textes non fournis.
- **A-07-i03** : Procédure à documenter : décision de l'autorité territoriale ; préparation conditionnelle du projet demandé sous réserve de vérification des conditions et formalités applicables, les exigences de transmission et de contrôle ultérieur devant être vérifiées avant toute formalisation.
- **A-07-i04** : Éléments admissibles pour instruire la demande : fonctions exercées, qualification détenue, expérience acquise, comparaison indicative avec la grille FPT sans en faire une obligation ; aucun plafond ou plancher non sourcé certifié.

**Échecs — intégration**

- Applique mécaniquement la grille statutaire des attachés à un contractuel CDI
- Omet la réévaluation périodique prévue pour les CDI et le contrôle de sa dernière occurrence
- Certifie des formalités de procédure (contrôle de légalité, conditions d'avenant) non étayées par une source vérifiée citée
- Confond les règles de rémunération des fonctionnaires et des contractuels

**Critères obligatoires — dégradé**

- **A-07-d01** : Identification des variables manquantes (rémunération actuelle, date de dernière réévaluation, description précise des nouvelles missions) sans certifier aucun plafond, plancher ou formalité.
- **A-07-d02** : Présentation conditionnelle du besoin de formalisation si changement substantiel, en indiquant que qualification et formalités doivent être vérifiées avant tout acte.
- **A-07-d03** : Trame d'avenant conditionnel avec clauses à compléter, sans fixer de montant ni certifier des règles de procédure non vérifiées.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable ou certifiée ; nommer un régime, une distinction ou une référence comme hypothèse à vérifier n'est pas une certification. Les faits fournis restent acquis.
- Refuse de fournir une trame d'avenant faute de textes consultés
- Redemande le fondement contractuel L332-8 2° ou la durée déjà fournis

**Sources annoncées et réserves**

- CGFP L713-1 — Fixation de la rémunération contractuelle : fonctions, qualification, expérience (verifie).
- Décret 88-145, art. 1-2 — Réévaluation au moins tous les trois ans pour les CDI, entretiens professionnels, évolution des fonctions (verifie).
- CGFP R331-12 et R331-13 — Critères de modification substantielle du contrat et formalités requises (a_consulter).
- Décret 88-145 art. 39-3 — Motifs de licenciement, dont le refus d'une modification substantielle du contrat (4°) (a_consulter).
- CGFP L332-9, L332-10 et L332-11 — Historique du CDI à articuler avec les services antérieurs et les conditions de L332-10 ; possibilité de CDI anticipé d'un commun accord selon L332-11. La variante du scénario retient deux ans de CDI après six ans de CDD. (verifie_selon_relecture_2026-10-15).

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
- **A-08-d04** : Trame de traçabilité de la communication (bordereau ou équivalent) utilisable après vérification du contenu communicable, sans certifier ce contenu.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable ou certifiée ; nommer un régime, une distinction ou une référence comme hypothèse à vérifier n'est pas une certification. Les faits fournis restent acquis.
- Refuse de structurer la procédure ou de fournir une trame de traçabilité (bordereau ou équivalent) faute de textes consultés
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
- **A-09-i02** : Examine la poursuite de la procédure pendant le CLM sur une source vérifiée citée : CE 13 juillet 2022, n°461914, point 19. Précise que ce point vise le congé de maladie en général, ni le CLM en particulier ni les droits de la défense ; n'étend pas sa portée au-delà de ce qu'il établit.
- **A-09-i03** : Identifie les garanties de défense exigées : communication intégrale du dossier (L532-4), délai suffisant pour organiser la défense (décret 89-677 art. 4), droit à assistance ; si le conseil de discipline intervient, vérifier la convocation au moins quinze jours avant sa réunion (art. 6) ; précise comment l'état de santé peut affecter concrètement l'exercice de ces droits et quel risque contentieux en résulte.

**Échecs — intégration**

- Affirme que le CLM suspend ou interdit la procédure.
- Confond la prescription initiale (délai pour engager) avec la question d'un délai courant après engagement.
- Omet les garanties de défense applicables (L532-4, décret 89-677 art. 4 ; art. 6 lorsque le conseil de discipline intervient).

**Critères obligatoires — dégradé**

- **A-09-d01** : Signale que la règle sur la continuation d'une procédure disciplinaire pendant un CLM doit être vérifiée avant tout acte, sans certifier de position.
- **A-09-d02** : Collecte les variables absentes : date de connaissance effective des faits par l'administration, stade de la procédure au moment du CLM, type de sanction envisagée.
- **A-09-d03** : Prépare conditionnellement les modalités permettant l'exercice de la défense (report, représentation, observations écrites), sous réserve des vérifications ciblées sur la capacité de l'agent, sans certifier un interlocuteur compétent ni bloquer indéfiniment ou clore la procédure.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable ou certifiée ; nommer un régime, une distinction ou une référence comme hypothèse à vérifier n'est pas une certification. Les faits fournis restent acquis.
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

Collectivité FPT de 420 agents, 12 octobre 2026. La DRH souhaite instaurer le télétravail de manière pérenne pour les postes éligibles. Elle doit identifier l'acte applicable et l'instance à consulter selon la portée du projet ; examiner les conditions d'accès des titulaires et des contractuels ; traiter séparément la demande d'un agent reconnu en situation de handicap concernant une dérogation au quota standard et des aménagements sur son lieu de télétravail ; organiser le suivi des jours dans le SIRH et examiner les questions RGPD associées ; préparer la communication interne. Produire un plan de déploiement en signalant les points que les sources disponibles ne permettent pas de trancher.

**Critères obligatoires — intégration**

- **A-10-i01** : Identifie la délibération de l'organe délibérant et l'instance à consulter selon l'objet et la portée du projet, en articulant R432-1 2°, L253-6 et R253-80 ; ne pénalise pas une réponse qui cite L253-6. Distingue cet acte d'un accord collectif et qualifie les options proposées à la DRH.
- **A-10-i02** : Examine le régime visant l'agent public, sans imposer une différence entre titulaires et contractuels pour l'accès au télétravail : L430-1, R431-1 et R433-1 ne les distinguent pas. Cite la base si elle figure dans les sources disponibles et est vérifiée, sinon signale son absence ; les conditions d'éligibilité de R432-3 à R432-8 restent à vérifier.
- **A-10-i03** : Traite séparément la demande de dérogation au quota (R431-6 1° : conditions et durée maximale) et la demande d'aménagement du lieu de télétravail (R433-3, L131-8 : sous réserve de charges non disproportionnées) ; conclut si l'obligation d'aménagement est automatique ou conditionnelle.
- **A-10-i04** : Propose un suivi opérationnel des jours dans le SIRH et une communication d'accompagnement ; identifie les traitements et les questions RGPD à vérifier, sans certifier les obligations dont les sources sont absentes.

**Échecs — intégration**

- Retient une instance incompatible avec la portée du projet au regard de R432-1, R253-7 et R253-80.
- Assimile dérogation quota et aménagement de poste handicap sans distinguer leur régime.

**Critères obligatoires — dégradé**

- **A-10-d01** : Signale que l'acte et l'instance doivent être qualifiés selon la composition locale du CST et la portée du projet avant d'annoncer une procédure précise.
- **A-10-d02** : Collecte les variables absentes : existence d'une formation spécialisée CST, accord collectif local éventuel, outil SIRH disponible, état de la délibération cadre.
- **A-10-d03** : Traite l'agent handicapé en deux questions distinctes (dérogation quota / aménagement) et signale l'incertitude sur l'étendue de chaque obligation sans les affirmer comme absolues.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable ou certifiée ; nommer un régime, une distinction ou une référence comme hypothèse à vérifier n'est pas une certification. Les faits fournis restent acquis.
- Ne pose pas la question du régime applicable aux contractuels.
- Omet de collecter l'existence d'une formation spécialisée CST ou d'un accord local.

**Sources annoncées et réserves**

- CGFP R432-1 2°, R431-5, R431-6 1° — Délibération FPT, avis formation spécialisée ou CST, quota et dérogation pour handicap ou état de santé (verifie).
- CGFP R253-7 et R253-80 — Compétence du CST seul lorsque le projet relève aussi de ses attributions (verifie).
- CGFP R433-3 et L131-8 — Aménagements du lieu de télétravail pour agent handicapé, sous réserve de charges non disproportionnées (verifie).
- CGFP L430-1, R431-1 et R433-1 — Les articles visent l'agent public sans distinguer titulaires et contractuels ; R432-3 à R432-8 (éligibilité) non lus selon le rapport. (verifie_selon_relecture_2026-10-15).

- Dossier réellement fourni : [Code général de la fonction publique](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044426132), passages L430-1, L131-8, L251-9, R253-7, R253-80, R431-1, R431-2, R431-3, R431-4, R431-5, R431-6, R432-1, R432-2, R432-3, R433-3.

Liste exhaustive des identifiants et critères : [jeuAJSON](cases-a.json).

### A-11 — Suppression d’emploi et RQTH

**Question**

Collectivité FPT >350 agents, 12 octobre 2026. Un rédacteur principal de 2e classe, reconnu RQTH et bénéficiaire depuis 18 mois d'un aménagement de poste formalisé (horaires adaptés, matériel ergonomique), est concerné par une suppression d'emploi envisagée dans le cadre d'une réorganisation ; le projet de délibération n'a pas encore été soumis au CST. Aucune inaptitude médicale n'a été constatée. La DRH doit : conduire la procédure de suppression d'emploi (CGFP L542-1 à L542-7) ; vérifier si des obligations spécifiques s'appliquent au titre de la qualité de BOE avant, pendant ou après la suppression ; organiser la recherche d'un poste compatible avec les restrictions fonctionnelles formalisées ; identifier qui valide la compatibilité du nouveau poste. Produire une note de procédure articulant ces régimes.

**Critères obligatoires — intégration**

- **A-11-i01** : Articule recherche de reclassement dès que la suppression est envisagée (L542-1), rapport et avis du CST (L542-2), puis suites conditionnelles selon les emplois pouvant être offerts (L542-5) ; distingue maintien en surnombre (L542-4) et prise en charge (L542-7) ; si les conséquences financières sont évoquées, les rattache à la prise en charge (L542-15).
- **A-11-i02** : Vérifie si les textes disponibles établissent des obligations spécifiques à l'employeur au titre de la qualité de BOE lors de la suppression d'emploi, distinctes de la procédure ordinaire (L131-8) ; indique précisément les limites de ce que le corpus permet d'affirmer.
- **A-11-i03** : Signale que la validation de la compatibilité médicale du poste relève d'un avis médical dont le cadre reste à vérifier ; ne nomme pas une autorité non établie par les sources. Distingue ce point d'une procédure d'inaptitude médicale, non en cause ici.

**Échecs — intégration**

- Traite la suppression d'emploi d'un BOE identiquement à celle d'un agent ordinaire sans mentionner la question des obligations spécifiques.
- Confond reclassement pour inaptitude médicale (conseil médical) et reclassement pour suppression d'emploi.
- Cite une référence au livre III du CGFP pour la suppression d'emploi (articles concernés sont au livre V).

**Critères obligatoires — dégradé**

- **A-11-d01** : Signale que des obligations spécifiques BOE en cas de suppression d'emploi doivent être vérifiées avant d'en affirmer l'existence, sans les certifier.
- **A-11-d02** : Collecte les variables absentes : date envisagée de suppression, postes vacants disponibles dans le grade, état des recherches de reclassement déjà engagées.
- **A-11-d03** : Distingue la suppression d'emploi de la procédure liée à une inaptitude médicale et prépare deux options conditionnelles selon les postes disponibles, sans certifier de délais ni exiger une référence précise.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable ou certifiée ; nommer un régime, une distinction ou une référence comme hypothèse à vérifier n'est pas une certification. Les faits fournis restent acquis.
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
- **A-12-i04** : Propose pour les 8 postes critiques un dispositif de transmission des savoirs, avec outils et calendrier compatibles avec les dates de départ confirmées et l'emploi budgétaire disponible.

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

- Une règle juridique non vérifiée est présentée comme applicable ou certifiée ; nommer un régime, une distinction ou une référence comme hypothèse à vérifier n'est pas une certification. Les faits fournis restent acquis.
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

Un attaché hors classe titulaire exerce dans une commune de 25 000 habitants depuis trois ans. Il demande sa mutation vers une commune de 450 agents (12 octobre 2026). Le service RH de la collectivité d'accueil a établi que le plafond statutaire de 10 % des attachés en activité et en détachement au 31 décembre N-1 est déjà atteint pour les promotions au grade hors classe de l'année en cours. Le DRH doit déterminer si la mutation peut néanmoins être acceptée et quelle incidence elle aura sur les promotions futures. Produire une note d'aide à la décision.

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

- Une règle juridique non vérifiée est présentée comme applicable ou certifiée ; nommer un régime, une distinction ou une référence comme hypothèse à vérifier n'est pas une certification. Les faits fournis restent acquis.
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

Un adjoint technique territorial titulaire (collectivité de 450 agents, 12 octobre 2026) quitte son poste en invoquant un droit de retrait : il signale une défectuosité du système de protection d'une machine présentant selon lui un danger grave et imminent pour sa santé. Son supérieur hiérarchique estime le danger non avéré et demande à la DRH d'ordonner la reprise immédiate et, en cas de refus, d'opérer une retenue sur traitement. La DRH doit déterminer : les conditions d'un retrait légitime, si une retenue est possible, et comment instruire la situation. Produire une note de procédure.

**Critères obligatoires — intégration**

- **B-02-i01** : Distingue le signalement d'un danger grave et imminent ou d'une défectuosité des conditions du droit de retrait.
- **B-02-i01-b** : Identifie le motif raisonnable de penser à un danger grave et imminent requis par l'article 5-1 du décret 85-603 pour la protection contre sanction et retenue.
- **B-02-i01-c** : Ne présente pas la seule défectuosité comme suffisante pour établir le droit de retrait.
- **B-02-i01-d** : Précise que l'exercice du retrait ne crée pas pour autrui une nouvelle situation de danger grave et imminent.
- **B-02-i02** : Interdiction de retenue sur traitement et d'aucune sanction lorsque le motif raisonnable est établi, identifiée sur source ; impossibilité pour l'autorité territoriale d'ordonner la reprise si le danger persiste qualifiée.
- **B-02-i03** : Note de procédure produite : instruction conditionnelle (vérifier la défectuosité, apprécier le motif raisonnable avant toute retenue ou sanction, constituer les pièces) ; décision sur la reprise subordonnée au résultat de cette vérification.
- **B-02-i04** : Si la procédure d'alerte et d'instruction est décrite, la rattache aux articles R253-58 à R253-63 CGFP selon les conditions effectivement établies ; n'exige ni ne retient les articles 5-2/5-3 abrogés du décret 85-603. R253-61 n'est ni exigé ni sanctionné.

**Échecs — intégration**

- La retenue sur traitement est présentée comme applicable sans examen du motif raisonnable.
- Les conditions du droit de retrait (motif raisonnable de penser à un danger grave et imminent) ne sont pas identifiées.
- La note de procédure n'est pas produite.

**Critères obligatoires — dégradé**

- **B-02-d01** : Existence d'un droit de retrait dans la FPT territoriale posée comme à vérifier sur source ; aucune condition ni protection certifiées.
- **B-02-d02** : Identifie les éléments permettant d'apprécier le bien-fondé du retrait : nature et réalité de la défectuosité, circonstances du signalement déjà mentionné, éléments disponibles documentant la situation, position du supérieur et vérification technique de l'équipement.
- **B-02-d03** : Mode dégradé déclaré ; aucune conclusion sur la légitimité du retrait ni sur la retenue sans vérification de la source.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable ou certifiée ; nommer un régime, une distinction ou une référence comme hypothèse à vérifier n'est pas une certification. Les faits fournis restent acquis.
- Les éléments permettant d'apprécier le bien-fondé du retrait (défectuosité, circonstances du signalement, éléments techniques et position du supérieur) ne sont pas identifiés.
- Le mode dégradé n'est pas déclaré.

**Sources annoncées et réserves**

- Décret 85-603 du 10 juin 1985, article 5-1 — Motif raisonnable de danger grave et imminent, signalement au supérieur, défectuosité du système de protection, interdiction de sanction et de retenue, impossibilité d'ordonner la reprise si danger persiste (consulte_dans_dossier).
- CGFP R253-58 à R253-63, sous réserve de R253-61 non vérifié — Registre spécial ; enquête immédiate R253-60 ; réunion sous 24 heures et inspecteur du travail R253-62 ; rapport et réponse motivée sous 15 jours R253-63, selon le rapport. R253-61 non vérifié ; R253-64/65 non vérifiés. Ne pas exiger les articles 5-2/5-3 du décret 85-603, abrogés depuis le 01/01/2023, ni l'article 68 du décret 2021-571 abrogé depuis le 01/02/2025. (verifie_selon_relecture_2026-10-15).

- Dossier réellement fourni : [Décret n°85-603 du 10 juin 1985 relatif à l'hygiène et à la sécurité du travail ainsi qu'à la médecine professionnelle et préventive dans la fonction publique territoriale](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006368812), passages 2-1, 5-1.

Liste exhaustive des identifiants et critères : [jeuBJSON](cases-b.json).

### B-03 — CDD successifs et CDI

**Question**

Un agent contractuel de catégorie B a été recruté six fois de suite par CDD pour accroissement temporaire d'activité sur un emploi non permanent, sur cinq ans et demi (collectivité de 450 agents, 12 octobre 2026). Certains contrats excèdent douze mois ; des interruptions entre contrats sont inférieures à un mois. L'agent demande par écrit sa CDIsation en invoquant ses années de service. Le DRH doit : qualifier le régime de chaque contrat, déterminer si et dans quelles conditions les services accomplis ouvrent droit à une CDIsation, et produire une réponse motivée à l'agent.

**Critères obligatoires — intégration**

- **B-03-i01** : Fondement légal distingué sur source : emploi non permanent pour accroissement temporaire (L332-23) vs contrat établi ou renouvelé pour pourvoir un emploi permanent (L332-8) ; CDIsation de droit (L332-10) subordonnée à un contrat relevant de L332-8, les services accomplis au titre de L332-23 étant comptabilisables pour la durée de six ans auprès du même employeur et dans la même catégorie hiérarchique.
- **B-03-i02** : Distinguer les dépassements individuels de douze mois déjà indiqués, contraires à la durée maximale, du contrôle des renouvellements sur dix-huit mois nécessitant la chronologie détaillée ; ne déduire ni irrégularité autonome des interruptions courtes ni CDIsation automatique des dépassements.
- **B-03-i03** : Produit une réponse motivée ferme sur les conditions établies (moins de six ans de services et aucun contrat relevant de L332-8) et conditionnelle sur la chronologie restant à reconstituer. Les voies de recours peuvent être mentionnées comme piste à vérifier sans en certifier le détail procédural.

**Échecs — intégration**

- Une CDIsation de droit est affirmée sans vérifier les conditions de L332-10, notamment le contrat établi ou renouvelé sous L332-8, les six ans de services admissibles, le même employeur et la même catégorie hiérarchique.
- Les interruptions courtes sont automatiquement qualifiées d'irrégularités sans analyse des fenêtres de référence.
- La réponse à l'agent est absente.

**Critères obligatoires — dégradé**

- **B-03-d01** : Distinction emploi non permanent / emploi permanent posée sans certification des durées exactes ni des conditions de CDIsation.
- **B-03-d02** : Variables bloquantes identifiées : chronologie détaillée et dates de chaque contrat, fondement juridique de chaque contrat, durée de chaque interruption ; la catégorie B et la nature des recrutements pour accroissement temporaire sur emploi non permanent sont tenues pour acquises, les contrats étant demandés comme justificatifs.
- **B-03-d03** : Mode dégradé déclaré ; réponse à l'agent en version d'attente concise avec champs à compléter ; aucune CDIsation ni irrégularité certifiées sans vérification.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable ou certifiée ; nommer un régime, une distinction ou une référence comme hypothèse à vérifier n'est pas une certification. Les faits fournis restent acquis.
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
- **B-04-i02** : Distingue domaine ouvert à la négociation et obligation d'ouvrir ou de répondre à une demande : dans la partie législative L221-1 à L223-1, aucune telle obligation préalable aux LDG n'est démontrée. Borne la conclusion à cette partie ; la partie réglementaire non trouvée reste à vérifier.
- **B-04-i03** : Note d'aide à la décision produite : distinction consultation CST / négociation posée, risque contentieux en cas de défaut de consultation CST identifié, recommandation conditionnelle sur la suite à donner à la demande syndicale selon les variables locales.

**Échecs — intégration**

- Une obligation légale de négociation préalable aux LDG est affirmée sans source consultée l'établissant.
- La compétence du CST sur les LDG est affirmée sans fondement textuel identifié.
- La note d'aide à la décision n'est pas produite.

**Critères obligatoires — dégradé**

- **B-04-d01** : Procédure des LDG FPT posée comme à vérifier ; aucune obligation de négociation ni son absence certifiées.
- **B-04-d02** : Identifie l'existence éventuelle d'un accord, protocole ou engagement local pris en instance. La représentativité des deux organisations est acquise dans l'énoncé ; elle n'est pas une variable manquante décisive pour conclure sur une obligation juridique non vérifiée.
- **B-04-d03** : Mode dégradé déclaré ; note produite en version bornée ; aucune conclusion sur la validité ou l'annulation des LDG sans vérification.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable ou certifiée ; nommer un régime, une distinction ou une référence comme hypothèse à vérifier n'est pas une certification. Les faits fournis restent acquis.
- Les variables bloquantes (accord, protocole ou engagement local) ne sont pas identifiées, la représentativité syndicale étant tenue pour acquise.
- Le mode dégradé n'est pas déclaré.

**Sources annoncées et réserves**

- CGFP L413-1, L413-2, L413-3 — L413-1 : contenu des LDG pour toutes FP ; L413-2 : volet mobilité réservé à l'État ; L413-3 : avis du comité social compétent (consulte_dans_dossier).
- CGFP R413-31, R253-7 (8°) — Consultation du CST territorial sur les projets de LDG promotion/valorisation (consulte_dans_dossier).
- CGFP L221-2, L222-3 (8°), L223-1 — Champ de la négociation collective incluant le déroulement des carrières ; conditions de validité d'un accord (50 % des suffrages) ; représentativité requise (consulte_dans_dossier).
- CGFP L221-1 à L223-1 (partie législative) — Aucune obligation d'ouvrir ou de répondre à une demande de négociation démontrée dans les articles lus selon le rapport. L221-3 : représentativité par au moins un siège au CST ; L223-1 : 50 % pour la validité d'un accord signé, pas pour imposer son ouverture. Partie réglementaire R221/R222 non trouvée : réserve maintenue. (verifie_selon_relecture_2026-10-15).

- Dossier réellement fourni : [Code général de la fonction publique](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044426396), passages L413-1, L413-2, L413-3, L222-3, R413-31, R413-32, R413-33, R413-34, L224-1, L224-2, L224-3, L224-4, R253-7, L221-2, L223-1.

Liste exhaustive des identifiants et critères : [jeuBJSON](cases-b.json).

### B-05 — Recette du SIRH

**Question**

Collectivité FPT >350 agents, 12 octobre 2026. À l'issue d'une migration du SIRH vers un prestataire externe finalisée il y a trois semaines, la DRH constate des erreurs de correspondance entre données reprises et référentiels locaux : échelons mal appariés pour une trentaine d'agents, droits à formation non intégrés, accès non ouverts pour plusieurs gestionnaires. Le prestataire conteste une partie des anomalies. La DRH doit piloter la recette, arbitrer les corrections à la charge du prestataire ou de la collectivité, sécuriser le contrôle RGPD des données transmises, et décider des conditions d'ouverture officielle du système. Produire une note de décision.

**Critères obligatoires — intégration**

- **B-05-i01** : Identifie les vérifications avant ouverture (cohérence des données, droits d'accès, intégrité des référentiels) et les responsabilités à établir à partir du contrat, sans présumer la répartition DRH/prestataire.
- **B-05-i02** : Le répondant précise les obligations RGPD applicables au prestataire en tant que sous-traitant (instructions documentées, garanties, informations et audits selon l'art. 28 §3 h, registre du sous-traitant selon l'art. 30 §2, sécurité selon l'art. 32, restitution ou suppression) et les contrôles que la DRH doit exercer, avec les articles vérifiés.
- **B-05-i03** : Le répondant propose une procédure de décision d'ouverture conditionnelle distinguant anomalies bloquantes et corrections différables, et propose une répartition des rôles (DRH, DSI, DPO, finances) à valider selon les habilitations locales et le contrat, sans abandonner la décision d'ouverture au prestataire. Traite l'effet sur la paie des échelons erronés parmi les éléments de la décision d'ouverture.

**Échecs — intégration**

- Abandonne au prestataire la décision d'ouverture ou le contrôle de la recette
- Omet les obligations RGPD du prestataire sous-traitant
- Ne distingue pas anomalies bloquantes et corrections différables

**Critères obligatoires — dégradé**

- **B-05-d01** : Le répondant signale qu'il ne peut certifier les obligations contractuelles exactes ni le périmètre des responsabilités du prestataire sans accès au contrat de sous-traitance, et indique les clauses à vérifier.
- **B-05-d02** : Le répondant identifie les données RGPD à vérifier (types de données transmises, destinataires, mesures de sécurité) comme conditions préalables à l'ouverture, sans certifier la conformité.
- **B-05-d03** : Le répondant propose une logique conditionnelle de recette (anomalies bloquantes à qualifier, seuil d'ouverture) sans certifier la procédure exacte ni les délais contractuels.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable ou certifiée ; nommer un régime, une distinction ou une référence comme hypothèse à vérifier n'est pas une certification. Les faits fournis restent acquis.
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

- **B-06-i01** : Vérifie rubrique par rubrique si des données personnelles sont effectivement traitées, notamment pour les données présentées comme anonymisées. Pour les rubriques concernées, justifie le fondement lorsque les éléments le permettent ou suspend précisément sa validation. Si une rubrique permet d'identifier l'appartenance syndicale de personnes nommées, examine l'article 9 §1 ; sinon, l'absence de ce développement n'est pas un échec.
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

- Une règle juridique non vérifiée est présentée comme applicable ou certifiée ; nommer un régime, une distinction ou une référence comme hypothèse à vérifier n'est pas une certification. Les faits fournis restent acquis.
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

- **B-07-d01** : Indique qu'il ne peut certifier l'existence ni les conditions du congé pour convenances personnelles des contractuels CDI sans consulter le texte applicable ; identifie le texte à rechercher sans exigence d'article numéroté.
- **B-07-d02** : Le répondant avertit que l'analogie avec la disponibilité fonctionnaire ne peut être appliquée sans vérification et signale le risque pour la collectivité d'un refus sans base légale ou d'un accord à tort.
- **B-07-d03** : Le répondant propose une démarche conditionnelle : si le congé existe, conditions et effets à vérifier ; si non, alternatives à explorer — sans certifier le résultat.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable ou certifiée ; nommer un régime, une distinction ou une référence comme hypothèse à vérifier n'est pas une certification. Les faits fournis restent acquis.
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
- **B-08-i02** : Le répondant identifie les éléments de rémunération inclus dans l'assiette saisissable et les exclusions documentées par les sources vérifiées citées, applique le barème par tranches en précisant les données manquantes nécessaires au calcul final (rémunération nette précise, ressources du conjoint pour le correctif).
- **B-08-i03** : Précise les obligations déclaratives de la collectivité tiers saisi sur les sources vérifiées citées.
- **B-08-i03-b** : Précise les délais déclaratifs documentés, en identifiant les seuls compléments restant à vérifier.
- **B-08-i03-c** : Organise le circuit de traitement en respectant les rôles textuels du service employeur et du comptable assignataire.
- **B-08-i03-d** : Identifie les habilitations locales à vérifier pour le circuit coordonné.
- **B-08-i03-e** : Décrit le circuit de versement sur les sources vérifiées citées, sans inventer de lacune documentaire.
- **B-08-i03-f** : Prépare l'information de l'agent sur les éléments documentés, notamment la juridiction de contestation indiquée dans l'acte selon R212-1-15, et identifie les compléments à vérifier.

**Échecs — intégration**

- Présente le reversement au greffe comme automatique sans vérifier le régime en vigueur depuis juillet 2025
- Annonce les quotités saisissables sans source vérifiée
- Omet les variables bloquantes au calcul (rémunération nette, ressources conjoint pour le correctif)
- Attribue sans justification une compétence exclusive à la DRH ou confond les obligations du service employeur et du comptable assignataire

**Critères obligatoires — dégradé**

- **B-08-d01** : Le répondant signale qu'il ne peut certifier ni le barème exact ni la liste exhaustive des exclusions sans vérification, indique les textes à consulter, et identifie les données manquantes (rémunération nette, ressources conjoint) comme variables bloquantes.
- **B-08-d02** : Avertit que l'identité du destinataire compétent doit être vérifiée avant toute retenue ; le commissaire de justice répartiteur peut être nommé comme piste à vérifier, sans certifier le circuit.
- **B-08-d03** : Le répondant souligne l'urgence de qualifier la notification reçue et propose un plan conditionnel, incluant la préparation conditionnelle de l'information de l'agent, sans certifier les délais de traitement, les droits ni les sanctions applicables.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable ou certifiée ; nommer un régime, une distinction ou une référence comme hypothèse à vérifier n'est pas une certification. Les faits fournis restent acquis.
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

- **B-09-i01** : Analyse l'allégation de discrimination liée à la grossesse au regard de L131-1 et L131-2 CGFP sans tenir le lien causal pour établi.
- **B-09-i01-b** : Examine la portée de L131-1, L131-2, L131-12 et L135-4 pour une candidate externe et suspend la conclusion sur ses protections lorsque le fondement manque.
- **B-09-i01-c** : Si la loi 2016-1691 est mobilisée, distingue sa qualification de lanceur d'alerte sans la tenir pour acquise ; citer l'article 8 I-A 1° n'est pas obligatoire.
- **B-09-i02** : Vérifie quelles données sont effectivement collectées ou consignées dans la procédure de recrutement.
- **B-09-i02-b** : Établit sur les faits la qualification des données relatives à la grossesse, notamment au regard de l'article 4 §15 et de l'article 9 §1.
- **B-09-i02-c** : Analyse les finalités et les principes de l'article 5 RGPD pour les traitements effectivement établis.
- **B-09-i02-d** : Examine le fondement applicable au regard de l'article 6 RGPD.
- **B-09-i02-e** : Si l'article 9 s'applique, examine l'exception pertinente sans la présumer.
- **B-09-i02-f** : Distingue l'utilisation pour sélectionner les candidats de la conservation limitée et sécurisée de preuves.
- **B-09-i02-g** : Examine l'article 17 §3 e pour ces preuves, sans conclure a priori à une absence de fondement ni à une suppression obligatoire.
- **B-09-i03** : Propose des mesures correctives proportionnées aux faits : contrôle des motifs du rejet, réexamen impartial, adaptation éventuelle de la procédure ou du jury, préservation des preuves ; définit le contenu minimal de la communication interne aux membres du jury sur la pertinence des données collectées et l'absence de critères discriminatoires, sans imposer l'éviction automatique du jury.

**Échecs — intégration**

- Omet d'analyser l'allégation de discrimination liée à la grossesse et la portée des textes pour une candidate externe
- Analyse les données de grossesse sans vérifier les données effectivement traitées, leur qualification, les finalités et le fondement applicable (articles 5, 6 et 9 RGPD)
- Ne prévoit aucun examen de mesures correctives proportionnées sur la procédure de recrutement

**Critères obligatoires — dégradé**

- **B-09-d01** : Signale que la qualification de la discrimination et la portée des protections pour une candidate externe nécessitent de vérifier leurs fondements et conditions avant toute décision, sans exigence de référence précise.
- **B-09-d02** : Collecte les variables manquantes décisives : existence d'une mention écrite de la grossesse dans le dossier ou un compte rendu de jury, stade de la procédure au moment du signalement, existence d'un autre candidat déjà informé de sa sélection.
- **B-09-d03** : Prépare conditionnellement des mesures correctives proportionnées (contrôle des motifs, réexamen impartial, adaptation éventuelle de la procédure ou du jury, préservation des preuves), sans certifier qu'une solution précise s'impose sans vérification des faits.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable ou certifiée ; nommer un régime, une distinction ou une référence comme hypothèse à vérifier n'est pas une certification. Les faits fournis restent acquis.
- Omet la trace écrite dans le dossier comme variable décisive à collecter.
- Omet de préparer des mesures correctives proportionnées ou affirme une obligation d'annulation totale de la procédure.

**Sources annoncées et réserves**

- CGFP L131-1, L131-2, L131-12, L135-4 — Interdiction des discriminations fondées sur le sexe et la grossesse ; champ des agents publics et conditions propres à chaque protection, portée à vérifier pour une candidate externe sans protection présumée applicable (verifie).
- RGPD art. 4 §15, 5, 6, 9 et 17 §3 e (dispositif EUR-Lex CELEX:02016R0679-20160504) — Qualification de la grossesse comme donnée de santé à établir sur les faits ; finalités, fondement et exceptions de l'art. 9, dont 9 §2 f ; conservation limitée et sécurisée de preuves et examen de l'art. 17 §3 e (verifie_selon_complement_2026-10-14).
- Loi 2016-1691 art. 6 I et 10-1 II ; art. 8 en contexte facultatif — Si la loi est mobilisée, ne pas tenir la qualification de l'alerte pour acquise : conditions de l'article 6 I et protection contre les représailles de l'article 10-1 II. L'article 8 I-A 1° est une piste de contexte facultative, pas une référence obligatoire au barème ni une source requise pour ce cas. Mapping et lecture rapportés par Claude le 14/10 ; réponses primaires correspondantes absentes des archives locales examinées. (verifie_selon_complement_2026-10-14).

- Dossier réellement fourni : [Code général de la fonction publique](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044427698), passages L131-1, L131-2, L131-12, L131-13, L135-4.
- Source RGPD à relire : [PDF consolidé EUR-Lex archivé](../rapports/rgpd-2026-10-14/CELEX-02016R0679-20160504-FR-consulte-2026-10-14.pdf) ; identifiant requis `CELEX:02016R0679-20160504` ; [provenance et empreinte](../rapports/rgpd-2026-10-14/provenance.json), [articles et pages par cas](../rapports/rgpd-2026-10-14/articles-rgpd.json).

Liste exhaustive des identifiants et critères : [jeuBJSON](cases-b.json).

### B-10 — Transfert d’agents

**Question**

Le 12 octobre 2026, une communauté de communes de 380 agents, membre, avec plusieurs communes, d'un syndicat mixte, prépare la reprise des compétences et de l'activité du syndicat. Un arrêté préfectoral de dissolution identifie les compétences reprises et prévoit une prise d'effet dans 90 jours. L'activité concerne 42 agents : 28 titulaires (catégories A, B, C) et 14 contractuels de droit public (6 CDI, 8 CDD, dont certains arrivent à terme dans les six mois suivant la reprise). Le dossier ne précise pas le mécanisme individuel applicable aux titulaires. La DRH doit examiner séparément leur situation et celle des contractuels, identifier les consultations nécessaires, estimer l'impact salarial et préparer la reprise SIRH et l'accompagnement. Produire un plan motivé ; suspendre précisément toute conclusion que les pièces ou sources ne permettent pas d'établir.

**Critères obligatoires — intégration**

- **B-10-i01** : Identifie le syndicat mixte composé de communes et d'EPCI et articule le renvoi de L5711-1 aux règles des syndicats de communes avec L5212-33 pour la dissolution, sans en déduire un transfert automatique des agents.
- **B-10-i01-b** : Si une substitution vers un syndicat mixte est évoquée, distingue L5711-4 du mécanisme de reprise à établir à partir de l'arrêté et des compétences concernées.
- **B-10-i01-c** : Pour les 14 contractuels de droit public, examine L445-1 et L445-2 : reprise de l'activité d'une personne morale de droit public par une autre personne publique, conditions et proposition de contrat, sans présenter la reprise des contrats comme automatique.
- **B-10-i01-d** : Pour les 28 titulaires, établit le mécanisme applicable à partir de l'arrêté de dissolution ou suspend précisément cette conclusion ; ne présente pas leur transfert à l'EPCI comme automatique.
- **B-10-i02** : Identifie la consultation du CST propre de la communauté de communes, dont les 380 agents excèdent le seuil de 50 agents de L251-5, sur le projet d'organisation des services (R253-7 1°). Examine séparément si un CST du syndicat est encore constitué et compétent avant sa dissolution et doit être consulté.
- **B-10-i03** : Pour les CDD arrivant à terme dans les 6 mois post-transfert, identifie les variables à vérifier (durée résiduelle, ancienneté, nature du besoin) pour décider entre non-renouvellement au terme et examen d'une proposition de renouvellement ou de CDI, sans certifier les conditions d'une CDIsation sans vérification des textes applicables à la collectivité d'accueil.
- **B-10-i04** : Prépare une estimation documentée de l'impact salarial et un plan opérationnel de reprise SIRH et d'accompagnement du changement, avec hypothèses, responsables et jalons adaptés au délai de 90 jours.

**Échecs — intégration**

- Présente le transfert des titulaires à l'EPCI comme acquis sans mécanisme établi par l'arrêté de dissolution et le cadre applicable.
- Présente la reprise des contractuels comme automatique sans vérifier les conditions de L445-1 et L445-2
- Omet la consultation du CST de la collectivité d'accueil avant le transfert

**Critères obligatoires — dégradé**

- **B-10-d01** : Signale que les modalités de reprise sont à établir à partir de l'arrêté de dissolution et des compétences reprises ; distingue les questions concernant titulaires et contractuels sans certifier leur régime, ni exiger de référence numérotée.
- **B-10-d02** : Collecte les variables manquantes décisives au traitement individuel : éléments d'ancienneté et de rémunération de chaque agent, durée résiduelle des CDD, grilles appliquées dans l'ancienne structure, existence d'un CST encore actif dans le syndicat dissous ; les statuts annoncés (titulaires, CDI, CDD) restent acquis.
- **B-10-d03** : Identifie l'impact SIRH et masse salariale comme axe à co-instruire avec DSI et finances et repère le circuit documentaire de validation et le décideur habilité pour les modalités de reprise statutaire ou contractuelle.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable ou certifiée ; nommer un régime, une distinction ou une référence comme hypothèse à vérifier n'est pas une certification. Les faits fournis restent acquis.
- Omet la durée résiduelle des CDD comme variable décisive à collecter.
- Délègue aux finances ou à la DSI la décision sur le régime applicable ou omet de préparer l'estimation salariale et le plan de reprise utiles.

**Sources annoncées et réserves**

- CGCT L5212-33 et L5711-4 — Base de la dissolution (L5212-33), non du transfert des agents ; substitution vers un syndicat mixte (L5711-4) ; cadre de reprise à déterminer selon l'acte de dissolution et les compétences concernées, sans régime présumé (verifie).
- CGFP L445-1, L445-2 — L445-1 vise la reprise de l'activité d'une personne morale de droit public par une autre personne publique pour les contractuels de droit public ; L445-1/2 sont conservés pour les 14 contractuels. Leur champ ne permet pas d'en déduire le transfert automatique des titulaires. (verifie_selon_relecture_2026-10-15).
- CGFP R253-7, 1° — Compétence du CST sur les projets d'organisation des services (verifie).
- CGFP L251-5 — Seuil de 50 agents pour le CST propre ; la communauté de communes de 380 agents dispose de son CST propre selon la section finale du rapport. (verifie_selon_relecture_2026-10-15).
- CGCT L5711-1 — Syndicat de communes et d'EPCI : syndicat mixte soumis aux règles des syndicats de communes, selon la référence relue par Claude et fournie par Jo pour corriger le scénario B-10. (relu_par_Claude_selon_decision_Jo_2026-10-15).

- Dossier réellement fourni : [Code général des collectivités territoriales](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000038922544), passages L5212-33, L5211-4-1, L5211-25-1, L5211-26, L5711-4.
- Dossier réellement fourni : [Code général de la fonction publique](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044426064), passages L445-1, L445-2, L445-3, L253-5, R253-7.

Liste exhaustive des identifiants et critères : [jeuBJSON](cases-b.json).

### B-11 — Scoring de promotion

**Question**

Le 12 octobre 2026, la DRH d'une collectivité de 520 agents (>350) souhaite déployer un outil de scoring automatisé pour prioriser l’examen des agents éligibles aux tableaux d'avancement de grade. L'outil attribue un score à chaque agent éligible à partir des données du SIRH (ancienneté, évaluations, formations suivies). Le DPO signale un risque lié à l'article 22 du RGPD. Le CST demande à être consulté. La DRH doit piloter la gouvernance sans déléguer au DPO ni à la DSI la décision sur les critères d'avancement. Produire une note de cadrage juridique et de gouvernance.

**Critères obligatoires — intégration**

- **B-11-i01** : Examine les effets réels du classement, dont l'exclusion effective du vivier et les effets juridiques ou significatifs, pour apprécier l'article 22 RGPD.
- **B-11-i01-b** : Examine le degré réel d'intervention humaine sur chaque inscription finale au tableau.
- **B-11-i01-c** : Examine les exceptions de l'article 22 §2 a-c.
- **B-11-i01-d** : Examine les garanties de l'article 22 §3.
- **B-11-i01-e** : Ne présente pas une validation humaine formelle comme une obligation fondée sur l'article 22 lui-même.
- **B-11-i02** : Qualifie le projet pour identifier la base de consultation du CST applicable parmi R253-7, 1° (organisation des services), 11° (critères d'appréciation de la valeur professionnelle) ou 8° et 12° (LDG promotion et taux d'avancement), et précise que la consultation doit précéder la mise en production.
- **B-11-i03** : Rattache la conduite de l'AIPD au responsable du traitement (art. 35 §1 RGPD).
- **B-11-i03-b** : Situe l'AIPD avant le traitement et examine son exigibilité, notamment dans l'hypothèse de l'article 35 §3 a.
- **B-11-i03-c** : Rattache au DPO une mission de conseil (art. 35 §2 et 39 §1 c).
- **B-11-i03-d** : Rattache à la DSI le déploiement technique.
- **B-11-i03-e** : Rattache la décision sur les critères de scoring et les inscriptions à l'autorité territoriale compétente, selon les LDG et délégations locales, sans l'attribuer au DPO ou à la DSI.

**Échecs — intégration**

- Conclut sur la qualification art. 22 RGPD par la seule présence d'une validation humaine formelle sans examiner les effets réels du classement
- Attribue à la DRH seule la compétence exclusive des inscriptions au tableau sans identifier les LDG et délégations locales
- Omet la qualification du projet pour déterminer la base de consultation du CST applicable

**Critères obligatoires — dégradé**

- **B-11-d01** : Signale que la qualification de l'outil au regard de l'article 22 RGPD dépend du paramétrage réel et des effets effectifs du classement, et que cette qualification doit être établie avant tout déploiement, sans la certifier a priori.
- **B-11-d02** : Collecte les variables manquantes décisives : critères exacts de scoring retenus, degré d'intervention humaine dans la décision finale, LDG locales en vigueur, délégation de signature applicable aux inscriptions au tableau.
- **B-11-d03** : Prépare les informations sur les opérations, finalités, effets, personnes concernées, données et garanties permettant de vérifier la nécessité d'une AIPD ; nomme cette démarche comme piste, sans certifier ses conditions ni l'obligation ou la dispense et sans référence numérotée exigée.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable ou certifiée ; nommer un régime, une distinction ou une référence comme hypothèse à vérifier n'est pas une certification. Les faits fournis restent acquis.
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

Le 12 octobre 2026, dans une collectivité de 480 agents (>350), un agent titulaire de catégorie B fait l'objet d'une procédure engagée depuis trois semaines en vue de son licenciement pour insuffisance professionnelle conduite selon les formes de la procédure disciplinaire. Durant cette même période, il dépose auprès de la DRH un signalement de harcèlement moral dirigé contre son supérieur hiérarchique direct, auteur du rapport ayant fondé l'engagement de la procédure. L'agent invoque une protection contre les mesures défavorables et demande la suspension de la procédure en cours. La DRH doit déterminer si le signalement suspend la procédure, comment instruire les deux procédures sans confusion, et comment assurer la protection de chaque partie.

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
- **B-12-d02** : Collecte les variables manquantes décisives : stade exact de la procédure au moment du signalement, existence d'une procédure interne formalisée de recueil, modalités locales inconnues. Une copie du signalement peut être demandée pour en documenter le contenu, sans contester qu'il allègue un harcèlement moral.
- **B-12-d03** : Signale le risque de confusion des procédures comme enjeu de sécurité juridique majeur et recommande à titre conservatoire une organisation impartiale, sans certifier qu'une modalité précise est légalement obligatoire sans vérification.

**Échecs — dégradé**

- Une règle juridique non vérifiée est présentée comme applicable ou certifiée ; nommer un régime, une distinction ou une référence comme hypothèse à vérifier n'est pas une certification. Les faits fournis restent acquis.
- Omet la protection de l'agent signalant comme question à vérifier, ou présuppose l'existence d'une procédure interne formalisée de signalement non indiquée.
- Omet de préparer une organisation impartiale conservatoire adaptée au conflit identifié.

**Sources annoncées et réserves**

- CGFP L553-1 3°, L553-2 — Licenciement pour insuffisance professionnelle prononcé selon la procédure disciplinaire ; distinction avec sanction disciplinaire (verifie).
- CGFP L133-2, L133-3, L134-5, L135-4, L135-6 — Harcèlement moral ; protection de l'agent signalant contre mesures défavorables selon leurs conditions ; protection fonctionnelle ; dispositif de recueil des signalements (verifie).
- Loi 2016-1691 art. 10-1 II — Interdiction des représailles selon l'article 10-1 II ; la source liée à cette loi est limitée à cette disposition dans ce cas, conformément au rapport. (verifie_selon_relecture_2026-10-15).

- Dossier réellement fourni : [Code général de la fonction publique](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044425184), passages L553-1, L553-2, L133-1, L133-2, L133-3, L135-1, L135-4, L135-5, L135-6, L134-1, L134-5, R135-1, R135-2, R135-3, R135-4, R135-5, R135-6, R135-7, R135-8, R135-9, R135-10.

Liste exhaustive des identifiants et critères : [jeuBJSON](cases-b.json).
