#!/usr/bin/env python3
"""
Harness de test du skill drh-fpt — sous-agents à contexte vierge.

Principe : chaque cas est traité par un appel API indépendant. En mode
intégration, le contexte contient le bundle DRH et le skill compagnon
recherche-juridique ; en mode dégradé, il contient le bundle DRH et
l'indisponibilité explicite du compagnon. Le modèle ne connaît ni l'historique
de conception, ni les réponses attendues. Un second appel (juge), tout aussi
vierge, note la réponse contre la grille d'attendus.

Usage :
    export ANTHROPIC_API_KEY=sk-...
    python run_tests.py --legal-skill ../recherche-juridique
    python run_tests.py --judge --legal-skill ../recherche-juridique
    python run_tests.py --mode degraded --judge

Sorties : tests/resultats/<campagne-id>/ avec réponses, évaluations, provenance
et bilan global.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
import argparse
import uuid

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RESULTS = HERE / "resultats"
API_URL = "https://api.anthropic.com/v1/messages"

# Modèles par défaut — référencés partout (argparse, docstring) pour éviter
# toute dérive entre les valeurs affichées et les valeurs réellement utilisées.
DEFAULT_MODEL = "claude-sonnet-4-6"
DEFAULT_JUDGE_MODEL = "claude-opus-4-8"

# Retry exponentiel sur erreurs transitoires : 2s / 4s / 8s (3 tentatives).
RETRY_DELAYS = (2, 4, 8)
RETRYABLE_HTTP_STATUS = {429, 500, 502, 503, 529}

MAX_TOKENS_REPONDANT = 4000
MAX_TOKENS_JUGE = 2500
EXPECTED_CASES_PER_MODE = 30

VALID_CRITERION_STATUSES = {"SATISFAIT", "PARTIEL", "ABSENT"}
VALID_GLOBAL_VERDICTS = {"REUSSITE", "ECHEC"}
VALID_ARCHITECTURE_VERDICTS = {"REUSSITE", "ECHEC", "NON_APPLICABLE"}


class ApiCallError(RuntimeError):
    """Levée quand un appel API échoue après épuisement des tentatives."""


def find_bundle() -> Path:
    for c in (ROOT / "drh-fpt-bundle-pour-LLM.md", HERE / "drh-fpt-bundle-pour-LLM.md"):
        if c.exists():
            return c
    sys.exit("Bundle introuvable : place drh-fpt-bundle-pour-LLM.md à la racine du dépôt.")


def read_skill_version() -> str:
    """Lit la version dans le YAML d'en-tête de SKILL.md (source de vérité)."""
    skill_md = ROOT / "SKILL.md"
    if not skill_md.exists():
        return "inconnue"
    text = skill_md.read_text(encoding="utf-8")
    m = re.search(r"^\s*version:\s*(\S+)\s*$", text, re.MULTILINE)
    return m.group(1) if m else "inconnue"


def read_version_from_text(text: str) -> str:
    """Lit une version YAML depuis un contenu de skill."""
    m = re.search(r"^\s*version:\s*(\S+)\s*$", text, re.MULTILINE)
    return m.group(1) if m else "inconnue"


def bundle_sha256_prefix(bundle_text: str, length: int = 12) -> str:
    return hashlib.sha256(bundle_text.encode("utf-8")).hexdigest()[:length]


def git_provenance(path: Path) -> dict:
    """Retourne le commit et l'état de travail du dépôt contenant path."""
    base = path if path.is_dir() else path.parent

    def run_git(*args: str) -> str | None:
        try:
            result = subprocess.run(
                ["git", "-C", str(base), *args],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=False,
            )
        except OSError:
            return None
        return result.stdout.strip() if result.returncode == 0 else None

    root = run_git("rev-parse", "--show-toplevel")
    if not root:
        return {"racine_git": None, "commit": None, "dirty": None}
    status = run_git("status", "--porcelain")
    return {
        "racine_git": root,
        "commit": run_git("rev-parse", "HEAD"),
        "dirty": bool(status) if status is not None else None,
    }


def load_legal_skill(raw_path: str) -> tuple[str, Path, list[str]]:
    """Charge le compagnon depuis un bundle, un dossier de skill ou son dépôt."""
    path = Path(raw_path).expanduser().resolve()
    if not path.exists():
        sys.exit(f"Skill compagnon introuvable : {path}")

    if path.is_file():
        return path.read_text(encoding="utf-8"), path, [str(path)]

    candidates = (
        path,
        path / "skill",
        path / "skills" / "recherche-juridique",
    )
    skill_root = next(
        (candidate for candidate in candidates if (candidate / "SKILL.md").is_file()),
        None,
    )
    if skill_root is None:
        sys.exit(
            f"Aucun SKILL.md de recherche-juridique trouvé sous {path}. "
            "Passe le dépôt, son dossier skill/ ou son bundle Markdown."
        )

    skill_md = skill_root / "SKILL.md"
    files = [skill_md]
    references = skill_root / "references"
    if references.exists():
        files.extend(sorted(references.rglob("*.md")))

    chunks = []
    for file in files:
        rel = file.relative_to(skill_root).as_posix()
        chunks.append(f"\n\n<!-- SOURCE COMPAGNON : {rel} -->\n\n")
        chunks.append(file.read_text(encoding="utf-8"))
    return "".join(chunks), skill_root, [str(file) for file in files]


def build_system_context(drh_bundle: str, legal_bundle: str | None, mode: str) -> str:
    if mode == "degraded":
        return (
            drh_bundle
            + "\n\n<!-- MODE D'EXÉCUTION -->\n"
            + "Le skill recherche-juridique est indisponible. Tu fonctionnes "
            "explicitement en mode dégradé et appliques les règles d'abstention."
        )
    assert legal_bundle is not None
    return (
        "<!-- SKILL MÉTIER : DRH FPT -->\n"
        + drh_bundle
        + "\n\n<!-- SKILL COMPAGNON OBLIGATOIRE : RECHERCHE JURIDIQUE -->\n"
        + legal_bundle
        + "\n\n<!-- MODE D'EXÉCUTION -->\n"
        + "Les deux skills sont co-activés. DRH FPT qualifie, décide et livre ; "
        "recherche-juridique vérifie les sources officielles avant toute "
        "conclusion juridiquement engageante."
    )


def call_api(key: str, model: str, system: str, user: str, max_tokens: int) -> dict:
    """Appelle l'API Messages avec retry exponentiel sur erreurs transitoires.

    Retourne le dict de réponse brut (contient notamment 'content' et
    'stop_reason'). Lève ApiCallError après épuisement des tentatives — la
    boucle appelante est responsable d'attraper cette exception (pas de
    sys.exit ici, pour ne pas interrompre les autres cas du bilan).
    """
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        # Bloc system en liste de blocs pour activer le cache prompt
        # (le bundle est volumineux et réutilisé à l'identique par cas).
        "system": [
            {
                "type": "text",
                "text": system,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        "messages": [{"role": "user", "content": user}],
    }
    data = json.dumps(payload).encode()
    last_error = None

    attempts = len(RETRY_DELAYS) + 1
    for attempt in range(attempts):
        req = urllib.request.Request(
            API_URL,
            data=data,
            headers={
                "x-api-key": key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="replace")[:300]
            last_error = ApiCallError(f"Erreur API HTTP {e.code} : {body}")
            if e.code not in RETRYABLE_HTTP_STATUS or attempt >= len(RETRY_DELAYS):
                raise last_error
        except (urllib.error.URLError, TimeoutError) as e:
            last_error = ApiCallError(f"Erreur réseau/timeout : {e}")
            if attempt >= len(RETRY_DELAYS):
                raise last_error

        delay = RETRY_DELAYS[attempt]
        print(f"  ... tentative {attempt + 1}/{attempts} échouée, nouvel essai dans {delay}s")
        time.sleep(delay)

    # Ne devrait pas être atteint (la boucle lève avant), filet de sécurité.
    raise last_error or ApiCallError("Échec de l'appel API (cause inconnue).")


def extract_text_and_truncation(response: dict) -> tuple[str, bool]:
    text = "".join(
        b.get("text", "") for b in response.get("content", []) if b.get("type") == "text"
    )
    tronque = response.get("stop_reason") == "max_tokens"
    return text, tronque


JUDGE_SYSTEM = (
    "Tu es un évaluateur juridique rigoureux en droit de la fonction publique "
    "territoriale. On te donne une question, une réponse à évaluer, et une liste "
    "de critères attendus. Pour chaque critère, indique s'il est SATISFAIT, "
    "PARTIEL ou ABSENT, avec une justification d'une phrase. Repère aussi toute "
    "AFFIRMATION FAUSSE ou inventée (référence, montant, jurisprudence), y "
    "compris dans un développement non nécessaire à la réponse. "
    "Termine par un score global sur 5 et un verdict global REUSSITE ou ECHEC. "
    "Évalue séparément l'architecture d'exécution et la fiabilité juridique. "
    "Réponds UNIQUEMENT en JSON : "
    '{"criteres":[{"critere":"...","statut":"SATISFAIT|PARTIEL|ABSENT","note":"..."}],'
    '"erreurs":["..."],"score_architecture_sur_5":N,'
    '"verdict_architecture":"REUSSITE|ECHEC|NON_APPLICABLE",'
    '"score_fiabilite_juridique_sur_5":N,'
    '"verdict_fiabilite_juridique":"REUSSITE|ECHEC",'
    '"score_sur_5":N,"verdict":"REUSSITE|ECHEC","synthese":"..."}\n\n'
    "RÈGLES TRANSVERSES (s'appliquent quels que soient les critères ci-dessus) :\n"
    "1. Toute référence, montant ou jurisprudence dont l'invention ou la "
    "fausseté est CONFIRMÉE par contrôle sur une source officielle → verdict "
    "ECHEC, quel que soit le score par ailleurs. Une précision suspecte non "
    "vérifiable doit être signalée comme non tranchée, pas qualifiée "
    "d'invention.\n"
    "2. Toute valeur d'INDEXATION VOLATILE (point d'indice, taux de cotisation, "
    "plancher PSC...) donnée DE MÉMOIRE, sans réserve de vérification → le "
    "critère « données volatiles » (ou équivalent) est en ÉCHEC.\n"
    "3. Un PLAFOND RÉGLEMENTAIRE cité avec sa source DATÉE et accompagné de "
    "« à confirmer » (ou formulation équivalente de réserve) est ACCEPTABLE — "
    "ne pas le compter comme une erreur inventée.\n"
    "4. Si le cas fourni précise un champ 'echec_si' (liste de conditions "
    "d'échec spécifiques au cas), applique-le en plus des règles ci-dessus : "
    "si l'une des conditions est manifestement remplie par la réponse, le "
    "verdict global est ECHEC.\n"
    "5. Si le cas est marqué type='echec_attendu', la logique de verdict "
    "s'INVERSE : ce sont des cas adversariaux où la RÉUSSITE consiste à ce "
    "que le répondant REFUSE, S'ABSTIENNE ou REDIRIGE correctement (signale "
    "un hors-périmètre, refuse de chiffrer de mémoire, ne transpose pas une "
    "règle inapplicable, etc.), conformément aux 'attendus'. Le verdict est "
    "ECHEC si le répondant traite la situation normalement, invente une "
    "donnée, ou transpose une règle inapplicable — c'est-à-dire si l'une des "
    "conditions 'echec_si' est remplie. Le verdict est REUSSITE si le "
    "répondant a bien refusé/s'est abstenu/a redirigé comme attendu, même si "
    "la réponse est brève.\n"
    "6. Une affirmation juridique fausse fait échouer la FIABILITÉ JURIDIQUE "
    "et le verdict GLOBAL, même si elle est surnuméraire, si tous les critères "
    "attendus sont satisfaits ou si l'architecture est réussie.\n"
    "7. Pour un cas type='architectural', noter séparément l'architecture et "
    "la fiabilité juridique. Une architecture réussie ne compense jamais une "
    "erreur juridique.\n"
    "8. Ne déduis jamais qu'une référence est inventée au seul motif qu'elle "
    "est récente ou postérieure à une date de cutoff. Vérifie-la sur une "
    "source officielle ; si cette vérification est impossible, décris le "
    "doute sans accuser de fabrication.\n"
    "9. Si la réponse affirme qu'une règle est « vérifiée » ou « confirmée » "
    "sans donner de lien ou d'identifiant officiel exploitable, considère la "
    "vérification comme non traçable. Une donnée exacte destinée à la paie, "
    "à un calcul ou à un acte fondée sur cette seule affirmation fait échouer "
    "la fiabilité juridique."
)


def judge(
    key: str, model: str, prompt: str, answer: str, attendus: list,
    echec_si: list | None = None, type_cas: str = "standard",
    reference_context: str = "",
) -> dict:
    crit = "\n".join(f"- {a}" for a in attendus)
    echec_si_block = ""
    if echec_si:
        label = (
            "CONDITIONS D'ÉCHEC SPÉCIFIQUES AU CAS (echec_si)"
            if type_cas != "echec_attendu"
            else "CONDITIONS D'ÉCHEC SPÉCIFIQUES AU CAS (echec_si — cas adversarial : "
            "leur présence dans la réponse signifie que le répondant a répondu "
            "normalement au lieu de refuser/s'abstenir/rediriger)"
        )
        echec_si_block = f"\n\n{label} :\n" + "\n".join(f"- {c}" for c in echec_si)
    type_block = (
        f"\n\nTYPE DE CAS : {type_cas}."
        + (
            " Il s'agit d'un cas ADVERSARIAL (echec_attendu) : applique la règle "
            "transverse 5 (la RÉUSSITE est le refus/l'abstention/la redirection "
            "correcte, pas une réponse normale)."
            if type_cas == "echec_attendu"
            else ""
        )
    )
    user = (
        f"QUESTION POSÉE :\n{prompt}\n\n"
        f"RÉPONSE À ÉVALUER :\n{answer}\n\n"
        f"CRITÈRES ATTENDUS :\n{crit}"
        f"{echec_si_block}"
        f"{type_block}\n\n"
        "Évalue selon les consignes. JSON uniquement."
    )
    judge_system = JUDGE_SYSTEM
    if reference_context:
        judge_system += (
            "\n\nCORPUS DE RÉFÉRENCE FOURNI POUR CETTE CAMPAGNE :\n"
            "Ce corpus permet de contrôler la conformité aux deux skills, mais "
            "ne remplace pas une consultation en direct des sources officielles. "
            "Toute référence absente du corpus et non vérifiable dans ce contexte "
            "doit être signalée comme non tranchée.\n\n"
            + reference_context
        )
    response = call_api(key, model, judge_system, user, max_tokens=MAX_TOKENS_JUGE)
    raw, tronque = extract_text_and_truncation(response)
    raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {
            "score_sur_5": None,
            "verdict": None,
            "synthese": "Réponse du juge non parsable",
            "raw": raw,
        }
    result["tronque"] = tronque
    return result


def validate_judge_result(result: dict, case: dict) -> list[str]:
    """Valide le schéma et les critères bloquants d'un verdict du juge."""
    problems: list[str] = []
    if result.get("tronque"):
        problems.append("évaluation du juge tronquée")

    criteria = result.get("criteres")
    if not isinstance(criteria, list) or len(criteria) != len(case["attendus"]):
        problems.append(
            "nombre de critères évalués différent du nombre de critères attendus"
        )
    else:
        for index, criterion in enumerate(criteria, start=1):
            if not isinstance(criterion, dict):
                problems.append(f"critère {index} mal formé")
                continue
            if criterion.get("statut") not in VALID_CRITERION_STATUSES:
                problems.append(f"statut invalide pour le critère {index}")
            elif criterion.get("statut") != "SATISFAIT":
                problems.append(f"critère {index} non entièrement satisfait")
            if not isinstance(criterion.get("critere"), str):
                problems.append(f"libellé absent pour le critère {index}")
            if not isinstance(criterion.get("note"), str):
                problems.append(f"justification absente pour le critère {index}")

    errors = result.get("erreurs")
    if not isinstance(errors, list):
        problems.append("champ erreurs absent ou mal formé")
    elif errors:
        problems.append("le juge a détecté au moins une erreur")

    verdict = result.get("verdict")
    legal_verdict = result.get("verdict_fiabilite_juridique")
    architecture_verdict = result.get("verdict_architecture")
    if verdict not in VALID_GLOBAL_VERDICTS:
        problems.append("verdict global absent ou invalide")
    elif verdict != "REUSSITE":
        problems.append("verdict global en échec")
    if legal_verdict not in VALID_GLOBAL_VERDICTS:
        problems.append("verdict juridique absent ou invalide")
    elif legal_verdict != "REUSSITE":
        problems.append("fiabilité juridique en échec")
    if architecture_verdict not in VALID_ARCHITECTURE_VERDICTS:
        problems.append("verdict d'architecture absent ou invalide")
    elif architecture_verdict == "ECHEC":
        problems.append("architecture en échec")
    elif case.get("type", "standard") == "architectural" and architecture_verdict != "REUSSITE":
        problems.append("cas architectural sans réussite d'architecture")

    for field in (
        "score_sur_5",
        "score_architecture_sur_5",
        "score_fiabilite_juridique_sur_5",
    ):
        value = result.get(field)
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not 0 <= value <= 5:
            problems.append(f"{field} absent ou hors de l'intervalle 0–5")

    if not isinstance(result.get("synthese"), str):
        problems.append("synthèse absente ou mal formée")
    return problems


def validate_strict_campaign(
    provenance: dict, cases: list[dict], case_results: list[dict]
) -> list[str]:
    """Retourne les motifs qui empêchent une campagne stricte de réussir."""
    problems: list[str] = []
    if len(cases) != EXPECTED_CASES_PER_MODE:
        problems.append(
            f"{len(cases)} cas actifs au lieu de {EXPECTED_CASES_PER_MODE}"
        )
    if len(case_results) != len(cases):
        problems.append(
            f"{len(case_results)} résultats produits pour {len(cases)} cas actifs"
        )

    drh = provenance["drh_fpt"]
    if not drh.get("commit"):
        problems.append("SHA Git drh-fpt absent")
    if drh.get("dirty") is not False:
        problems.append("dépôt drh-fpt non propre ou état indéterminé")

    legal = provenance["recherche_juridique"]
    if provenance["mode"] == "integration":
        if not legal.get("commit"):
            problems.append("SHA Git recherche-juridique absent")
        if legal.get("dirty") is not False:
            problems.append("dépôt recherche-juridique non propre ou état indéterminé")

    expected_ids = {case["id"] for case in cases}
    result_ids = {entry.get("id") for entry in case_results}
    missing = sorted(expected_ids - result_ids)
    duplicates = len(result_ids) != len(case_results)
    if missing:
        problems.append("cas sans résultat : " + ", ".join(missing))
    if duplicates:
        problems.append("identifiants de cas dupliqués dans le bilan")

    for entry in case_results:
        case_id = entry.get("id", "inconnu")
        if entry.get("statut") != "ok":
            problems.append(f"{case_id} : erreur d'exécution")
        if entry.get("tronque"):
            problems.append(f"{case_id} : réponse ou jugement tronqué")
        for issue in entry.get("validation", ["évaluation absente"]):
            problems.append(f"{case_id} : {issue}")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"modèle répondant (défaut {DEFAULT_MODEL})")
    ap.add_argument(
        "--judge-model", default=DEFAULT_JUDGE_MODEL,
        help=f"modèle juge (défaut {DEFAULT_JUDGE_MODEL})",
    )
    ap.add_argument("--judge", action="store_true", help="activer l'évaluation")
    ap.add_argument(
        "--strict", action="store_true",
        help=(
            "faire échouer la commande si la campagne n'est pas complète, "
            "traçable et sans verdict d'échec ; exige --judge"
        ),
    )
    ap.add_argument(
        "--mode", choices=("integration", "degraded"), default="integration",
        help="integration = compagnon obligatoire ; degraded = DRH seul",
    )
    ap.add_argument(
        "--legal-skill",
        help=(
            "chemin du dépôt ou du bundle recherche-juridique ; obligatoire "
            "en mode integration"
        ),
    )
    args = ap.parse_args()
    if args.strict and not args.judge:
        ap.error("--strict exige --judge")

    bundle_path = find_bundle()
    drh_bundle = bundle_path.read_text(encoding="utf-8")

    legal_bundle = None
    legal_path = None
    legal_sources: list[str] = []
    if args.mode == "integration":
        if not args.legal_skill:
            sys.exit(
                "--legal-skill est obligatoire en mode integration. "
                "Utilise --mode degraded pour tester explicitement le filet "
                "de sécurité sans compagnon."
            )
        legal_bundle, legal_path, legal_sources = load_legal_skill(args.legal_skill)

    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("Définis ANTHROPIC_API_KEY dans ton environnement.")

    system = build_system_context(drh_bundle, legal_bundle, args.mode)
    all_cases = json.loads((HERE / "cas-de-test.json").read_text(encoding="utf-8"))
    cases = [
        case for case in all_cases
        if args.mode in case.get("modes", ["integration", "degraded"])
    ]
    started_at = datetime.now(timezone.utc)
    campaign_id = f"{started_at.strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    campaign_results = RESULTS / campaign_id
    campaign_results.mkdir(parents=True, exist_ok=False)
    provenance = {
        "campagne_id": campaign_id,
        "date_debut_utc": started_at.isoformat(),
        "mode": args.mode,
        "modele_repondant": args.model,
        "modele_juge": args.judge_model if args.judge else None,
        "juge_active": args.judge,
        "drh_fpt": {
            "version": read_skill_version(),
            "bundle": str(bundle_path),
            "sha256_bundle": bundle_sha256_prefix(drh_bundle),
            **git_provenance(ROOT),
        },
        "recherche_juridique": (
            {
                "version": read_version_from_text(legal_bundle or ""),
                "chemin": str(legal_path),
                "sources_chargees": legal_sources,
                "sha256_contexte": bundle_sha256_prefix(legal_bundle or ""),
                **git_provenance(legal_path or ROOT),
            }
            if args.mode == "integration"
            else {
                "version": None,
                "chemin": None,
                "sources_chargees": [],
                "sha256_contexte": None,
                "racine_git": None,
                "commit": None,
                "dirty": None,
            }
        ),
        "nombre_cas_actifs": len(cases),
        "cas_de_test": {
            "chemin": str(HERE / "cas-de-test.json"),
            "sha256": hashlib.sha256(
                (HERE / "cas-de-test.json").read_bytes()
            ).hexdigest(),
        },
    }
    (campaign_results / "_provenance.json").write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(
        f"Campagne {campaign_id} — mode {args.mode} — "
        f"{len(cases)} cas actifs"
    )

    scores = []
    non_evalues = 0
    cas_bilan = []

    for c in cases:
        type_cas = c.get("type", "standard")
        marque = " [ADVERSARIAL]" if type_cas == "echec_attendu" else ""
        print(f"\n=== {c['id']} — {c['branche']}{marque} ===")
        statut_cas = "ok"
        try:
            # Sous-agent vierge : ne voit que le skill (system) + le cas (user)
            response = call_api(key, args.model, system, c["prompt"], max_tokens=MAX_TOKENS_REPONDANT)
        except ApiCallError as e:
            print(f"  ERREUR : {e}")
            cas_bilan.append({"id": c["id"], "branche": c["branche"], "statut": "erreur", "erreur": str(e)})
            continue

        answer, tronque = extract_text_and_truncation(response)
        if tronque:
            print("  ATTENTION : réponse tronquée (max_tokens atteint).")

        (campaign_results / f"{c['id']}.md").write_text(
            f"# {c['branche']}\n\n"
            f"## Provenance\n\n"
            f"- Campagne : `{campaign_id}`\n"
            f"- Mode : `{args.mode}`\n"
            f"- DRH FPT : `{provenance['drh_fpt']['commit'] or 'hors Git'}`\n"
            f"- Recherche juridique : "
            f"`{provenance['recherche_juridique']['commit'] or 'indisponible'}`\n"
            f"- Modèle : `{args.model}`\n\n"
            f"## Question\n{c['prompt']}\n\n"
            f"## Réponse (contexte vierge)\n{answer}\n",
            encoding="utf-8",
        )
        print(f"Réponse enregistrée ({len(answer)} caractères).{' [TRONQUÉE]' if tronque else ''}")

        entry = {
            "id": c["id"],
            "branche": c["branche"],
            "type": type_cas,
            "statut": statut_cas,
            "tronque": tronque,
        }

        if args.judge:
            try:
                ev = judge(
                    key, args.judge_model, c["prompt"], answer, c["attendus"],
                    echec_si=c.get("echec_si"), type_cas=type_cas,
                    reference_context=system,
                )
            except ApiCallError as e:
                print(f"  ERREUR (juge) : {e}")
                entry["statut"] = "erreur"
                entry["erreur"] = str(e)
                cas_bilan.append(entry)
                continue

            (campaign_results / f"{c['id']}-eval.json").write_text(
                json.dumps(ev, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            s = ev.get("score_sur_5")
            verdict = ev.get("verdict")
            if isinstance(s, (int, float)):
                scores.append(s)
            else:
                non_evalues += 1
            entry["score_sur_5"] = s
            entry["verdict"] = verdict
            entry["score_architecture_sur_5"] = ev.get("score_architecture_sur_5")
            entry["verdict_architecture"] = ev.get("verdict_architecture")
            entry["score_fiabilite_juridique_sur_5"] = ev.get(
                "score_fiabilite_juridique_sur_5"
            )
            entry["verdict_fiabilite_juridique"] = ev.get(
                "verdict_fiabilite_juridique"
            )
            entry["tronque"] = entry["tronque"] or ev.get("tronque", False)
            entry["validation"] = validate_judge_result(ev, c)
            print(f"Score : {s}/5 — verdict {verdict} — {ev.get('synthese', '')[:100]}")

        cas_bilan.append(entry)

    moy = sum(scores) / len(scores) if scores else None
    if args.judge:
        if moy is not None:
            print(f"\n=== BILAN : {moy:.1f}/5 sur {len(scores)} cas évalués ({non_evalues} non évalués) ===")
        else:
            print(f"\n=== BILAN : aucun score exploitable ({non_evalues} non évalués) ===")

    strict_problems = (
        validate_strict_campaign(provenance, cases, cas_bilan)
        if args.strict
        else []
    )
    if args.strict:
        if strict_problems:
            print("\n=== GATE STRICT : ÉCHEC ===")
            for problem in strict_problems:
                print(f"  - {problem}")
        else:
            print("\n=== GATE STRICT : RÉUSSITE ===")

    bilan = {
        "provenance": provenance,
        "cas": cas_bilan,
        "scores": scores,
        "moyenne_sur_5": moy,
        "non_evalues": non_evalues,
        "date_fin_utc": datetime.now(timezone.utc).isoformat(),
        "sha256_contexte_systeme": bundle_sha256_prefix(system),
        "gate_strict": {
            "active": args.strict,
            "reussite": args.strict and not strict_problems,
            "motifs_echec": strict_problems,
        },
    }
    (campaign_results / "_bilan.json").write_text(
        json.dumps(bilan, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return 1 if strict_problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
