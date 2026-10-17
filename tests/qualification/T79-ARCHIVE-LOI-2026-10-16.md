# T79 — consultation Claude de la loi 2016-1691, 16 octobre 2026

Préparation locale depuis `019bce2`. Aucune poussée, aucun gel, appel modèle ou campagne. La signature T77 reste différée au runtime final. La pièce fournie est archivée à l’identique avec son horodatage de copie ; les cas A/B et profils sont inchangés.

## Pièce et provenance exacte

[Pièce fournie par Jo](../rapports/loi-2016-1691-2026-10-16/loi-2016-1691-consultation-claude-2026-10-16.json) ; [provenance et diagnostic](../rapports/loi-2016-1691-2026-10-16/provenance.json).

SHA-256 brut attendu et recalculé après copie : `78da546dd2d3785c4a75f925e3cb28cbc34bc0638fd2623c4acc53f17cc7550c`. Le fichier est copié octet pour octet, sans réécriture JSON. Le hash confirme l’identité de la pièce reçue et archivée.

Selon la pièce et le message deJo : Claude a consulté l’API Légifrance par le MCP (serveur 578fe7d7-583a-429a-b9b8-dc00d39ac090), fonction `get_article`, puis recopié le texte depuis la réponse de l’outil. La consultation est rapportée «2026-10-16T10:13Z», avec des appels juste avant l’horodatage 10:13:29Z. L’instant exact de chaque appel n’est pas fourni ; il reste inconnu. L’horodatage d’archivage local est distinct.

La réponse brute API et la réponse d’outil originale ne figurent pas dans cette pièce. `content_trust=untrusted_source_data` est la valeur rapportée de l’outil. Les champs `verified=true`, `legal_status=VIGUEUR`, `applicable_at_as_of_date=true`, version 01/09/2022→01/01/2999 et date de référence 16/10/2026 sont conservés comme métadonnées de cette consultation rapportée. Aucune nouvelle interrogation primaire par Codex ni comparaison indépendante avec les octets originaux.

| Cas visé | Article | Identifiant fourni | Statut documentaire |
|---|---|---|---|
| B-09 |6|`LEGIARTI000045391750`| Texte et métadonnées recopiés par Claude, archive locale contrôlée |
| B-09 |10-1|`LEGIARTI000045389749`| Idem |
| B-12 |10-1|`LEGIARTI000045389749`| Idem |

Les trois identifiants sont déjà requis dans ces cas : aucun ajout/retrait. La fenêtre de version indiquée dans la pièce inclut sa date de consultation et la date des scénarios 12/10/2026 ; c’est un contrôle de cohérence interne, pas une nouvelle vérification de vigueur.

## Compatibilité avec le harnais : réserve maintenue

Le format reçu est `consultation-legifrance-claude/1`. Le harnais attend une enveloppe `consultations` contenant des traces par cas, avec requête, réponse archivée, empreinte, date et extrait contrôlables. Passage direct de la pièce à `live_sources.verify_trace` : refus vérifié, avec `URL officielle HTTPS absente`, `date de consultation invalide`, `'raw_response_file'`. Ces diagnostics décrivent des différences d’enveloppe ; ils ne suffisent pas à expliquer la limite de preuve.

| Élément | Disponible | Ce qui manque pour le contrôle existant |
|---|---|---|
| Identifiant / numéro / texte / version | Champs recopiés présents pour 6 et 10-1 | Réponse source originale permettant de comparer l’extrait aux champs officiels contrôlés par le validateur |
| Horodatage | Minute de consultation et borne rapportées en texte libre | Champ de trace exploitable avec fuseau et précision déclarée ; ne pas inventer un instant exact par appel |
| Requête / endpoint | Nom de fonction MCP `get_article` | Paramètres effectivement transmis, endpoint et métadonnées de contexte/version ; le transport HTTP exact n’est pas enregistré |
| Archive source | Octets exacts de la transcription, hash vérifié | Réponse source originale conservée et hashée. Compresser la transcription ne restaure pas cette réponse |
| Format d’article accepté | Le collecteur existant utilise `/consult/legiPart` | Sa réponse JSON et sa requête avec `textId` et date, puis les champs `id`, `num`, `etat`, `dateDebut`, `dateFin`, contenu et renvois nécessaires. Une réponse `get_article` originale exigerait un adaptateur spécifique relu et testé si son schéma diffère |
| Liaisons cas | B-09/6, B-09/10-1, B-12/10-1 identifiées | Trois traces valides liées à une archive source ; aucune inscription d’une transcription dans `evidence.json` de campagne |

Les noms de champs et l’enveloppe peuvent être adaptés ; la réponse d’origine absente ne peut pas être reconstruite. Créer un faux conteneur PISTE avec `etat`, `dateDebut`, `dateFin`, `num`, `content` et requête déduits de la transcription reviendrait à fabriquer l’objet servant à vérifier sa propre copie. Cela n’est pas effectué.

Le validateur, le schéma de preuve, `campaign.py`, les sources requises et les seuils sont conservés. Le support PDF T75 reste fondé sur le document officiel archivé lui-même et son index figé. Ajouter une voie acceptant une transcription Claude sur son seul hash changerait la nature de la preuve acceptée ; aucune telle voie n’est introduite.

## Pièce complémentaire à obtenir

Voie déjà supportée : récupérer via le collecteur existant la réponse API consolidée de la loi pour les articles 6 et 10-1, conserver requête/date/réponse JSON avant transcription, l’archiver en gzip avec son hash, puis produire les 3 liaisons. Aucun identifiant de texte `textId` n’est inventé ici.

Autre élément utile : export original de l’appel MCP et de sa réponse complète, avec paramètres, horodatage réel et contenu structuré non recopié. Selon son schéma, un adaptateur documenté et testé pourrait alors être évalué ; la pièce présente ne remplit pas cette condition.

La consultation primaire par Claude est désormais documentée dans une archive locale vérifiée. La compatibilité de preuve de campagne reste ouverte pour ces 3 liaisons. Les anciennes mentions de textes absents décrivent l’état antérieur à cette réception ; les octets source de l’API restent absents.

## Contrôles

Le 16/10/2026 : **137/137 tests déterministes en cp1252 et 137/137 en UTF-8**, sans échec ni test ignoré ; cohérence et `build_bundle.py --check` réussis dans les deux environnements. Seul avertissement préexistant : tag v0.7.0 absent. Empreintes A/B/profils inchangées et concordantes avec `suites.file_sha`. Pièce copiée à l’identique, hash recalculé concordant. Validateur, schéma, campagne et support PDF identiques à 019bce2 ; registre de suites inchangé. Aucun gel, appel modèle ou tentative de campagne.

## Empreintes inchangées

- A : `c7958f40a2938e67bc62a2f9b579b39f9f59d790dcce0eb70944b9db78b1141c`.
- B : `8e7c303417e91fc7415606ba478e1f87553506674ef39157f9e6bb7008447262`.
- Profils : `65301665ed0e9b1b2d1b613f2e4ba4baf5e4ae36dc7e65fb12de3610e7cc4c29`.
- PDF : `e5984442f70f842034f9b5cb39bf3d6137630252260830c07b0449f354faa718`.

## Vérifié / rapporté

Vérifié : identité de la pièce source et copie, schéma et champs présents, cohérence interne des dates, identifiants déjà requis et refus par le harnais actuel. Rapporté par Jo/Claude : consultation MCP, contenu officiel, statut et version. Inconnus : octets de la réponse source, requête transport exacte et instant exact par appel. Aucun gel ni qualification déclarés.
