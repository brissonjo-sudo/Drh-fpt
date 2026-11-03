# Agent Microsoft 365 Copilot — DRH-FPT

Adaptation du skill `drh-fpt` (v0.7.0) en agent **Microsoft 365 Copilot**,
créé avec **Agent Builder** (« Créer un agent » dans Copilot), sans code.

| Élément | Fichier | Limite Agent Builder |
|---------|---------|----------------------|
| Instructions | [instructions.md](instructions.md) | 8 000 caractères (≈ 6 850 utilisés) |
| Connaissances | `connaissances/DRH-FPT-01…16-*.docx` (générés) | 20 fichiers téléversés (16 utilisés) |
| Sites web | 4 sites officiels, listés ci-dessous | 4 adresses, 2 niveaux maximum |

Variante locale : placer des instructions personnalisées dans
`copilot/<collectivité>/instructions.md`. Ce dossier n'est pas versionné et
`--check` en contrôle aussi la taille.

Limites relevées sur la documentation Microsoft Learn le 27/10/2026
(*Add knowledge sources to an agent in Agent Builder* ; *Write effective
instructions for declarative agents*).

## 1. Générer les fiches de connaissance

Agent Builder n'accepte pas le `.md` : les références sont converties en `.docx`.

```bash
python scripts/build_copilot.py
```

Le script contrôle aussi la taille des instructions et l'absence de mentions
propres à Claude (`--check` pour contrôler sans générer). Les `.docx` sont
régénérables et ne sont pas versionnés. Relancer le script après chaque
évolution du skill, puis remplacer les fichiers dans l'agent.

| Fiche | Contenu |
|-------|---------|
| 01 | Contrat d'exécution (chaîne qualifier → sécuriser) |
| 02 | Sources et vérification |
| 03 | Paramètres de la collectivité et fiche profil |
| 04 | Gabarits : décision, délibération, courrier, note, procédure |
| 05 | Carrière et paie : règles communes |
| 06 | Statut, carrière et discipline |
| 07 | Rémunération, régime indemnitaire et paie |
| 08 | Temps de travail et fin de fonctions |
| 09 | QVT et santé |
| 10 | Recrutement et formation |
| 11 | CST et dialogue social |
| 12 | SI RH et masse salariale |
| 13 | Communication interne |
| 14 | Agents contractuels |
| 15 | Garanties, déontologie et signalements |
| 16 | Restitution proportionnée |

Exclus, comme dans le bundle : méta-gabarit des branches, registre de
maintenance des plafonds, tests.

## 2. Créer l'agent

Dans Microsoft 365 Copilot : **Nouvel agent** → **Passer à la configuration**
(onglet *Configurer*), puis renseigner les champs ci-dessous.

### Nom
```
DRH-FPT
```

### Description
```
Assistant RH pour les collectivités territoriales de plus de 350 agents : carrière, paie, régime indemnitaire, santé et QVT, recrutement, instances, contractuels, déontologie. Vérifie chaque règle sur les sources officielles avant de conclure et produit notes, projets d'arrêté, délibérations et courriers.
```

### Instructions
Copier **tout** le contenu de [instructions.md](instructions.md).

### Connaissances
- **Téléverser** les 16 fichiers de `copilot/connaissances/`.
- Ajouter les 4 sites suivants (bouton *Entrer une URL*) :

```
https://www.legifrance.gouv.fr
https://www.collectivites-locales.gouv.fr
https://www.fonction-publique.gouv.fr
https://www.service-public.fr
```

Variante : remplacer `service-public.fr` par le site de votre centre de gestion.

### Réglages
| Réglage | Valeur | Raison |
|---------|--------|--------|
| Rechercher sur tous les sites web | **Désactivé** | Limiter la vérification aux sites officiels |
| Utiliser uniquement les sources spécifiées | **Activé** | Privilégier les fiches et les sites officiels |
| Référencer les personnes de l'organisation | **Désactivé** | Éviter d'exposer des données d'agents |
| Interpréteur de code | Facultatif | Utile pour projeter une masse salariale |
| Générateur d'images | Désactivé | Sans usage |

### Amorces de conversation
| Titre | Message |
|-------|---------|
| Profil collectivité | Aide-moi à établir le profil de ma collectivité pour calibrer tes réponses. |
| Avancement de grade | Un adjoint administratif principal de 2e classe à 80 % peut-il avancer de grade cette année ? |
| Sanction disciplinaire | Quelle procédure pour exclure temporairement un fonctionnaire 5 jours ? |
| Régime indemnitaire | Je veux instaurer le régime indemnitaire de mes agents de police municipale. Que puis-je verser et comment procéder ? |
| Recruter un contractuel | Puis-je recruter un contractuel sur un emploi permanent vacant de catégorie B, et à quelles conditions ? |
| Note au DGS | Rédige une note d'aide à la décision sur la participation employeur à la protection sociale complémentaire. |

## 3. Recette (onglet *Essayer*)

Poser ces questions, issues de `tests/cas-de-test.json`, avant tout partage.

| Cas | Question (résumé) | Comportement attendu |
|-----|-------------------|----------------------|
| 01 | Avancement de grade à 80 % et affiliation CNRACL | Variables demandées (grade, ancienneté, LDG, ratios) ; source officielle citée |
| 09 | Exclusion temporaire de 5 jours | Procédure vérifiée ; motivation, recours, transmission au contrôle de légalité |
| 07 | Régime indemnitaire de la police municipale | Pas de RIFSEEP : régime propre de la filière, vérifié avant chiffre |
| 11 | DRH d'une collectivité à statut particulier (corps propres) | Statut particulier signalé, textes propres recherchés |
| 15 | Valeur exacte du point d'indice pour un arrêté | Valeur donnée **avec lien officiel**, sinon abstention, jamais de mémoire |
| 13 | Commune de 40 agents et CST | Hors périmètre annoncé, orientation sans dérouler la procédure |
| 14 | CHU de 900 agents | Fonction publique hospitalière : hors périmètre |
| 17 | Présomption de démission (droit privé) | Distinction avec l'abandon de poste en FPT |

Points à surveiller : un chiffre sans lien officiel, un nom de fiche cité dans
la réponse, ou l'absence du niveau de confiance en fin de réponse.

## 4. Différences avec la version Claude

- **Pas de skill compagnon `recherche-juridique`** : la vérification passe par
  la recherche web de Copilot, limitée aux 4 sites. Elle ne garantit pas
  l'ouverture de la version consolidée d'un texte : le cas 15 sert de témoin.
- **Fiches = connaissances, pas instructions** : Copilot peut ignorer ou
  filtrer les consignes contenues dans les fichiers (protection contre
  l'injection de prompt). Les règles de comportement essentielles sont donc
  toutes dans les instructions.
- **Recherche par extraits** : Copilot ne lit pas une fiche en entier mais en
  extrait des passages. Les fiches portent un numéro « DRH-FPT nn » repris
  dans les instructions pour guider la recherche.
- **Pas de journal ni de mémoire de fichier** : le profil de la collectivité
  se recolle en début de conversation.
- **Partage** : toute personne ayant accès à l'agent a accès au contenu des
  fichiers téléversés. Ne pas y ajouter de documents nominatifs.

## 5. Les 4 emplacements libres

Les 4 fichiers restants peuvent accueillir des documents propres à votre
collectivité, non nominatifs : délibération RIFSEEP, règlement du temps de
travail, lignes directrices de gestion, règlement de formation. Les
instructions demandent déjà de distinguer le socle national du choix local.

## 6. Évolution possible : skills Copilot (préversion)

Microsoft propose en préversion (programme *Frontier*) des **skills** pour les
agents, au format `SKILL.md` + fichiers, très proche du skill Claude
(instructions de skill jusqu'à 20 000 caractères, 8 skills par agent, archive
`.zip`). Si votre tenant y a accès, une version plus fidèle pourrait découper
le skill en plusieurs skills Copilot. Limite actuelle : un agent ne peut pas
combiner skills et fichiers téléversés.
