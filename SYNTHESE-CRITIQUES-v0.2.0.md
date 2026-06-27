# Synthèse des critiques externes & feuille de route v0.2.0

> Trace de décision. Trois IA (Gemini, ChatGPT, « Vibe ») ont challengé le
> skill `drh-fpt` v0.1.0. Ce document trie leurs retours (retenu / nuancé /
> écarté), intègre deux **vérifications juridiques sur sources officielles**,
> et fixe le plan d'application.

Date : 2026-06-26 · Cible : `drh-fpt` v0.2.0

---

## 1. Méthode de tri

Chaque retour est classé :
- ✅ **Retenu** — juste et utile, à intégrer.
- 🟡 **Nuancé** — idée valable mais formulation ou justification à corriger.
- ❌ **Écarté** — faux, inadapté, ou contre-productif (motif indiqué).

Principe directeur : **une critique externe n'est pas une autorité**. Deux des
trois retours contiennent des erreurs de droit. Les points juridiques
contestés ont été vérifiés sur Légifrance avant arbitrage.

---

## 2. Vérifications juridiques sur sources officielles

### 2.1 RIFSEEP & police municipale — Gemini ❌, skill à actualiser

**Gemini affirmait** : « le décret 2024-611 a ouvert le RIFSEEP à la police
municipale en remplacement de l'ISMF ». **Faux sur les deux points.**

Faits vérifiés (Légifrance, décret n° 2024-614 du 26 juin 2024 ; analyses CIG /
CDG) :
- La police municipale **n'est pas** intégrée au RIFSEEP. Le ministère y a
  explicitement renoncé.
- Le décret **n° 2024-614** (et non 2024-611) crée un **régime propre** :
  l'**Indemnité Spéciale de Fonction et d'Engagement (ISFE)**, en deux parts
  (part fixe + part variable liée à l'engagement), fondée sur l'article
  **L. 714-13 du CGFP**.
- L'ISFE **remplace** les anciens régimes (décrets 97-702, 2000-45, 2006-1397),
  abrogés au 1er janvier 2025. Elle est exclusive d'autres primes, sauf IHTS,
  travail de nuit/dimanche/jours fériés, astreintes et NBI. Clause de
  sauvegarde du montant antérieur.

**Décision** : la branche carrière-paie avait **raison** sur l'exclusion du
RIFSEEP, mais sa formulation (« relève encore d'un régime indemnitaire
propre ») est **obsolète**. → Nommer l'ISFE et le décret 2024-614. La
correction proposée par Gemini est **écartée** (elle aurait introduit une
erreur de droit).

### 2.2 Échelle des sanctions disciplinaires — Vibe 🟡 (idée retenue, contenu corrigé)

**Vibe proposait** un tableau plaçant l'exclusion ≤ 3 jours au 2e groupe avec
CAP compétente. **Périmé.**

Faits vérifiés (Légifrance, CGFP art. L533-1 à L533-3) :

| Groupe | Sanctions | Conseil de discipline |
|--------|-----------|------------------------|
| **1er** | Avertissement ; blâme ; **exclusion temporaire ≤ 3 jours** | **Non** |
| **2e** | Radiation du tableau d'avancement ; abaissement d'échelon ; exclusion 4–15 jours | **Oui** |
| **3e** | Rétrogradation ; exclusion 16 jours – 2 ans | **Oui** |
| **4e** | Mise à la retraite d'office ; révocation | **Oui** |

Pouvoir disciplinaire : autorité territoriale (art. L532-1 CGFP), pas
l'assemblée. Pas de liste légale des fautes (art. L530-1).

**Décision** : l'idée d'un tableau est **retenue** ; le contenu de Vibe est
**corrigé** par le tableau ci-dessus.

---

## 3. Tri des retours juridiques

| # | Point | Source | Verdict | Action |
|---|-------|--------|---------|--------|
| J1 | PM hors RIFSEEP → régime propre ISFE (décret 2024-614) | Gemini/Vibe | ✅ (vérifié) | Actualiser carrière-paie |
| J2 | Tableau des sanctions + conseil de discipline dès 2e groupe | Vibe | ✅ (corrigé) | Ajouter tableau vérifié |
| J3 | Ne pas citer le décret 2014-513 (texte État) comme source FPT directe ; viser le décret **n° 91-875** + délibération locale | Gemini | ✅ | Corriger la source RIFSEEP |
| J4 | CNRACL : seuil 28 h = emplois à **temps non complet**, ≠ temps partiel (un agent à temps partiel reste CNRACL) | Gemini | ✅ | Clarifier |
| J5 | CAP toujours saisissable **par l'agent** (révision du CREP, refus de télétravail/temps partiel/CPF) | Gemini/Vibe | ✅ | Compléter le bloc CAP |
| J6 | « Quasi automatique » (avancement d'échelon) → « de plein droit sous réserve des dispositions statutaires » | ChatGPT | ✅ | Reformuler |
| J7 | Principe de parité : éviter la synthèse « pas plus favorable que l'État » | ChatGPT/Gemini | ✅ | Nuancer |
| J8 | Positions statutaires : enrichir, **mais** la loi 2019 a réduit la liste — vérifier l'exactitude (ne pas copier Vibe aveuglément) | Vibe | 🟡 | Enrichir avec vérif |
| J9 | Compléments métier : GIPA, IHTS, SFT en garde alternée, rupture conventionnelle, fin de fonctions, retraite CNRACL, **contrôle de légalité** (transmission des actes) | Gemini/Vibe/ChatGPT | ✅ | Compléter carrière-paie |
| J10 | Garde-fou filières spécifiques (PM, SPP, OPH) : signaler vérification renforcée | Vibe | 🟡 (signaler, pas exclure) | Ajouter garde-fou |

---

## 4. Tri des retours d'architecture & conception LLM

| # | Point | Source | Verdict | Action |
|---|-------|--------|---------|--------|
| A1 | **Matrice métier/juridique explicite** (type de question → vérification obligatoire) à la place du déclencheur narratif | ChatGPT | ✅ (fort) | Ajouter au SKILL.md |
| A2 | Embarquer un **noyau de vérification auto-suffisant** dans le skill DRH, et garder le renvoi à `recherche-juridique` pour l'approfondissement | ChatGPT/Gemini/Vibe | ✅ (reformulé) | Renforcer le socle |
| A3 | **Gabarit de branche normalisé** + orientation décisionnelle (question → variables à lever → décision → vérification → livrable) | ChatGPT/Vibe | ✅ | Refondre le gabarit |
| A4 | Rubrique **Calculs** (annoncer hypothèses, demander données manquantes, séparer connu/estimé) | ChatGPT/Vibe | ✅ | Ajouter au gabarit |
| A5 | **Règle de résolution des conflits de normes** (hiérarchie des normes + lex specialis + rôle de la jurisprudence) | ChatGPT/Vibe | ✅ (reformulé) | Ajouter au socle |
| A6 | Liste des **données volatiles à toujours vérifier** (valeur du point, plafonds, SMIC, GIPA) **sans figer les valeurs** | Vibe | 🟡 | Créer la liste, pas un cache |
| A7 | Posture **« conseil / ingénierie juridique alternative »** : proposer une voie légale plutôt qu'un refus sec | Gemini | ✅ (valeur ajoutée) | Ajouter au SKILL.md |
| A8 | **Niveau de confiance gradué** (stable / à vérifier / jurisprudence récente / abstention) | ChatGPT | ✅ (léger) | Ajouter au gabarit |
| A9 | Classer les **livrables par niveau** (décision / organisation / pilotage / communication) + éléments obligatoires (voies de recours) | ChatGPT/Vibe | ✅ | Structurer assets/ |
| A10 | Clarifier le mécanisme `JOURNAL.md` : écriture via outil (Claude Code / filesystem) **ou** bloc à copier-coller | Gemini/Vibe | 🟡 | Préciser §7 |
| A11 | Alléger le frontmatter (moins d'acronymes) sans tomber dans le sous-déclenchement | Gemini/ChatGPT | 🟡 | Ajuster la description |
| A12 | Sortir la note méta (« ce fichier fixe le gabarit ») de la branche fonctionnelle | Gemini/ChatGPT | ✅ (mineur) | Déplacer |
| A13 | Métadonnées : `compatibilite` + dépendance versionnée `recherche-juridique` | ChatGPT | ✅ (léger) | Compléter le frontmatter |

---

## 5. Retours écartés (avec motif)

- **« Réintégrer la PM au RIFSEEP »** (Gemini) — ❌ faux, vérifié (§2.1).
- **« Le skill ne peut pas écrire dans JOURNAL.md, il oublie tout »**
  (Gemini/Vibe) — ❌ trop absolu. Dans l'environnement de travail (Claude Code +
  dépôt Git), l'écriture de fichiers est possible. On **clarifie** le mécanisme
  (A10), on ne supprime pas la boucle d'apprentissage.
- **« La dépendance à `recherche-juridique` est fictive/brisée »** (Gemini) —
  ❌ inexact si les deux skills sont chargés (cas réel ici). On **renforce**
  néanmoins un noyau de vérification autonome (A2) pour la robustesse.
- **Cache local de valeurs** (point d'indice « 5,0279 € », plafonds…) (Vibe) —
  ❌ anti-pattern : figer une valeur périssable dans un skill statique
  **reproduit** le risque d'obsolescence qu'on veut éviter. Remplacé par une
  **liste de données volatiles à vérifier** (A6). La valeur citée par Vibe est
  d'ailleurs probablement déjà datée — preuve par l'exemple.
- **Hiérarchie de conflit de Vibe** plaçant la jurisprudence « sous » le décret
  — ❌ faux (le juge contrôle et peut annuler le décret). Reformulée en A5.
- **« Désigner un juriste mainteneur, revue par pair sous 48 h, `ALERTS.md` »**
  (Vibe) — ❌ sur-process pour un outil personnel. Conservé : une **procédure
  de mise à jour d'urgence légère** hors revue annuelle.

---

## 6. Plan d'application v0.2.0 (priorisé)

### P1 — Corrections juridiques (bloquant / majeur)
Fichier `references/carriere-paie.md` (+ `socle-sources-verification.md`) :
1. RIFSEEP PM → **ISFE / décret 2024-614** (J1).
2. Source RIFSEEP → **décret 91-875 + délibération**, pas le 2014-513 seul (J3).
3. CNRACL → distinguer **temps non complet** et temps partiel (J4).
4. **Tableau des sanctions** vérifié + conseil de discipline dès 2e groupe (J2).
5. **Saisine de la CAP par l'agent** (J5).
6. Nuancer **parité** (J7) et « **de plein droit sous réserve** » (J6).

### P2 — Architecture & fiabilité (conception LLM)
Fichier `SKILL.md` + gabarit de branche :
7. **Matrice métier/juridique** (A1).
8. **Noyau de vérification embarqué** + renvoi `recherche-juridique` (A2).
9. **Gabarit de branche décisionnel** normalisé (A3).
10. Rubrique **Calculs** (A4).
11. **Règle de conflits de normes** correcte (A5).
12. **Données volatiles à vérifier** sans valeurs (A6).
13. Posture **conseil / alternative légale** (A7).
14. **Niveau de confiance** gradué (A8).
15. **Garde-fou filières spécifiques** (J10).
16. Clarifier le mécanisme **JOURNAL** (A10).

### P3 — Compléments & finitions
17. Compléments métier carrière-paie : GIPA, IHTS, SFT garde alternée, rupture
    conventionnelle, fin de fonctions, retraite, **contrôle de légalité** (J9).
18. Positions statutaires enrichies, avec vérification (J8).
19. **Classement + validation des livrables** dans `assets/` (A9).
20. Alléger le **frontmatter** (A11) + sortir la note méta (A12).
21. Métadonnées **dépendance versionnée** (A13).
22. Procédure de **mise à jour d'urgence** légère.

### Puis
23. Dérouler les **5 branches restantes** sur le gabarit décisionnel amélioré.

---

## 7. Enseignement transversal

L'exercice valide le principe fondateur du skill : **la vérification prime sur
l'assurance**. Deux IA ont énoncé des erreurs de droit avec aplomb (RIFSEEP PM,
tableau des sanctions, cache de valeurs). Le réflexe « source officielle avant
conclusion » a permis de les écarter. C'est exactement le comportement que le
skill doit produire en production.
