"""Orchestration reproductible des campagnes répondant + juge DRH-FPT."""

from __future__ import annotations

import argparse
import suites
import hashlib
import json
import re
import subprocess
import tempfile
import sys
import uuid
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RESULTS = HERE / "resultats"
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(HERE))

import context_loader  # noqa: E402
import live_sources  # noqa: E402
from providers import ApiCallError, Completion, complete, key_for_provider  # noqa: E402


DEFAULT_MODEL = "claude-opus-5-5"
DEFAULT_JUDGE_MODEL = "claude-opus-5-5"
MAX_TOKENS_REPONDANT = 4000
MAX_TOKENS_JUGE = 3000
EXPECTED_CASES_PER_MODE = 30
VALID_CRITERION_STATUSES = {"SATISFAIT", "PARTIEL", "ABSENT"}
VALID_GLOBAL_VERDICTS = {"REUSSITE", "ECHEC"}
VALID_ARCHITECTURE_VERDICTS = {"REUSSITE", "ECHEC", "NON_APPLICABLE"}


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def find_bundle() -> Path:
    for candidate in (ROOT / "drh-fpt-bundle-pour-LLM.md", HERE / "drh-fpt-bundle-pour-LLM.md"):
        if candidate.is_file():
            return candidate
    raise SystemExit("Bundle DRH introuvable")


def read_version_from_text(text: str) -> str:
    match = re.search(r"^\s*version:\s*(\S+)\s*$", text, re.MULTILINE)
    return match.group(1) if match else "inconnue"


def read_skill_version() -> str:
    return read_version_from_text((ROOT / "SKILL.md").read_text(encoding="utf-8"))


def git_provenance(path: Path) -> dict:
    base = path if path.is_dir() else path.parent

    def run(*args: str) -> str | None:
        try:
            result = subprocess.run(
                ["git", "-C", str(base), *args], capture_output=True, text=True,
                encoding="utf-8", check=False,
            )
        except OSError:
            return None
        return result.stdout.strip() if result.returncode == 0 else None

    root = run("rev-parse", "--show-toplevel")
    if not root:
        return {"racine_git": None, "commit": None, "dirty": None}
    status = run("status", "--porcelain")
    return {
        "racine_git": root,
        "commit": run("rev-parse", "HEAD"),
        "dirty": bool(status) if status is not None else None,
    }


def load_markdown_tree(raw_path: str, skill_name: str) -> tuple[str, Path, list[str]]:
    path = Path(raw_path).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"Chemin introuvable : {path}")
    if path.is_file():
        return path.read_text(encoding="utf-8"), path, [str(path)]
    candidates = (path, path / "skill", path / "skills" / skill_name)
    root = next((item for item in candidates if (item / "SKILL.md").is_file()), None)
    if root is None:
        raise SystemExit(f"Aucun SKILL.md de {skill_name} trouvé sous {path}")
    files = [root / "SKILL.md"]
    references = root / "references"
    if references.exists():
        files.extend(sorted(references.rglob("*.md")))
    chunks = []
    for file in files:
        chunks.append(f"\n\n<!-- SOURCE : {file.relative_to(root).as_posix()} -->\n\n")
        chunks.append(file.read_text(encoding="utf-8"))
    return "".join(chunks), root, [str(file) for file in files]


def load_legal_skill(raw_path: str) -> tuple[str, Path, list[str]]:
    return load_markdown_tree(raw_path, "recherche-juridique")


def load_source_pack(raw_path: str | None) -> tuple[str, Path | None, list[str]]:
    if not raw_path:
        return "", None, []
    path = Path(raw_path).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"Dossier de sources introuvable : {path}")
    files = [path] if path.is_file() else sorted(path.rglob("*.md"))
    if not files:
        raise SystemExit("Le dossier de sources ne contient aucun fichier Markdown")
    chunks = []
    for file in files:
        rel = file.name if path.is_file() else file.relative_to(path).as_posix()
        chunks.extend((f"\n\n<!-- SOURCE FIGÉE : {rel} -->\n\n", file.read_text(encoding="utf-8")))
    return "".join(chunks), path, [str(file) for file in files]


def build_system_context(
    drh_context: str,
    legal_bundle: str | None,
    mode: str,
    source_pack: str = "",
    evidence_mode: str = "rules",
    evidence: list[dict] | None = None,
) -> str:
    parts = []
    if mode == "integration":
        if legal_bundle is None:
            raise ValueError("Le compagnon juridique manque en mode integration")
        parts.extend(
            (
                "\n\n<!-- SKILL COMPAGNON : RECHERCHE JURIDIQUE -->\n",
                legal_bundle,
                "\n\n<!-- MODE -->\nLes deux skills sont co-activés. ",
                "DRH FPT qualifie, décide et livre ; recherche-juridique vérifie les sources.\n",
            )
        )
    else:
        parts.append(
            "\n\n<!-- MODE -->\nLe skill recherche-juridique est indisponible. "
            "Annonce le mode dégradé et applique l'abstention requise.\n"
        )
    if evidence_mode == "snapshot":
        parts.extend(
            (
                "\n\n<!-- DOSSIER DE SOURCES FIGÉES -->\n",
                "Ces documents servent à une évaluation reproductible et ne prouvent pas le droit actuel.\n",
                source_pack,
            )
        )
    elif evidence_mode == "live":
        parts.append(
            "\n\n<!-- PREUVE DE CONSULTATION -->\nToute affirmation présentée comme vérifiée "
            "doit correspondre à une trace de consultation officielle fournie à la campagne.\n"
        )
        parts.append(live_sources.source_context(evidence or []))
    # Les matériaux de vérification précèdent le contrat de restitution :
    # aucune duplication, aucun attendu de cas dans le contexte répondant.
    parts.extend(("\n\n<!-- SKILL MÉTIER : DRH FPT -->\n",drh_context))
    return "".join(parts)


def normalized_expectations(case: dict) -> list[dict]:
    expected = case.get("attendus")
    if not isinstance(expected, list) or not expected:
        raise ValueError(f"{case.get('id', 'cas inconnu')} : attendus absents")
    normalized = []
    for index, item in enumerate(expected, start=1):
        if not isinstance(item, dict):
            raise ValueError(
                f"{case.get('id', 'cas inconnu')} : attendu {index} sans identifiant stable"
            )
        criterion_id = item.get("id")
        text = item.get("texte")
        if not isinstance(criterion_id, str) or not criterion_id.strip():
            raise ValueError(f"{case.get('id')} : identifiant d'attendu vide")
        if not isinstance(text, str) or not text.strip():
            raise ValueError(f"{case.get('id')} : texte d'attendu vide")
        normalized.append({"id": criterion_id.strip(), "texte": text.strip()})
    ids = [item["id"] for item in normalized]
    if len(ids) != len(set(ids)):
        raise ValueError(f"{case.get('id')} : identifiants d'attendus dupliqués")
    return normalized


JUDGE_SYSTEM = """Tu évalues une réponse DRH FPT. Réponds uniquement en JSON.
Pour chaque critère fourni, recopie exactement son id et son texte, puis donne
SATISFAIT, PARTIEL ou ABSENT avec une justification non vide. N'ajoute et
n'omet aucun critère. Toute affirmation juridique fausse confirmée fait échouer
la fiabilité juridique et le verdict global. Une référence seulement suspecte
reste non tranchée. Une affirmation présentée comme vérifiée sans trace
exploitable n'est pas une vérification. Une réussite d'architecture ne compense
jamais une erreur juridique.

Évalue le sens de chaque critère, sans ajouter d'exigence. Accepte les
équivalences métier (par exemple statut particulier et décret statutaire du
cadre d'emplois). Respecte les alternatives « ou » et les conditions « si ».
Une mention « peut mentionner » est facultative : si elle est absente, ou si
la condition d'un critère ne se réalise pas, indique SATISFAIT avec la note
« non applicable » et sa raison. Une mention facultative effectivement donnée
reste soumise au contrôle de justesse. Une demande de collecte de pièces ou
un tableau explicite à renseigner suffit à demander des données ; aucune
forme interrogative particulière n'est exigée. Contrôle les précautions
adaptées au traitement décrit sans exiger un exposé juridique supplémentaire.
Une source officielle réellement fournie et vérifiée n'a pas à être annoncée
comme non consultée ; les réserves portent sur les points non vérifiés.
Recopie les libellés des critères à l'identique, même s'ils sont longs.
Consigne toute question juridique non tranchée dans incertitudes (liste de
phrases non vides, vide seulement si aucun doute résiduel). Une incertitude
non arbitrée bloque la qualification. Les scores de style sont indicatifs.
Ne transforme pas un soupçon juridique en erreur confirmée sans contrôler le
champ de la source et les décisions du dossier. En mode dégradé, les sources
OU les pièces à consulter suffisent si le critère le prévoit ; ne réclame pas
de références numérotées. Tout énoncé ferme non vérifié reste sanctionné.

Schéma :
{"criteres":[{"id":"...","critere":"...","statut":"SATISFAIT|PARTIEL|ABSENT","note":"..."}],
"erreurs":[],"incertitudes":[],"score_architecture_sur_5":0,"verdict_architecture":"REUSSITE|ECHEC|NON_APPLICABLE",
"score_fiabilite_juridique_sur_5":0,"verdict_fiabilite_juridique":"REUSSITE|ECHEC",
"score_sur_5":0,"verdict":"REUSSITE|ECHEC","synthese":"..."}
"""


def judge_prompt(case: dict, answer: str, evidence: list[dict] | None = None) -> str:
    expected = normalized_expectations(case)
    blocks = [
        f"QUESTION :\n{case['prompt']}",
        f"RÉPONSE :\n{answer}",
        "CRITÈRES :\n" + "\n".join(f"- [{x['id']}] {x['texte']}" for x in expected),
        f"TYPE : {case.get('type', 'standard')}",
        f"MODE ÉVALUÉ : {case.get('mode_evaluation', 'integration')} — "
        "En mode dégradé, contrôler les réserves et l'abstention. Ne pas exiger une consultation "
        "absente ni une décision ou un acte que les critères de ce mode interdisent.",
    ]
    if case.get("echec_si"):
        blocks.append("CONDITIONS D'ÉCHEC :\n" + "\n".join(f"- {x}" for x in case["echec_si"]))
    if evidence:
        blocks.append("TRACES DE CONSULTATION :\n" + json.dumps(evidence, ensure_ascii=False, indent=2))
    return "\n\n".join(blocks) + "\n\nJSON uniquement."


def parse_judge_completion(completion: Completion) -> dict:
    raw = completion.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        result = json.loads(raw)
        if not isinstance(result, dict):
            raise ValueError("Le jugement JSON n'est pas un objet")
    except (json.JSONDecodeError, ValueError):
        result = {"verdict": None, "synthese": "Réponse du juge non parsable", "raw": raw}
    result["tronque"] = completion.truncated
    result["metriques"] = {
        "duration_ms": completion.duration_ms,
        "usage": completion.usage,
        "response_id": completion.response_id,
    }
    return result


def validate_judge_result(result: dict, case: dict, *, semantic: bool = True) -> list[str]:
    problems: list[str] = []
    expected = normalized_expectations(case)
    expected_by_id = {item["id"]: item["texte"] for item in expected}
    criteria = result.get("criteres")
    if result.get("tronque"):
        problems.append("évaluation du juge tronquée")
    if not isinstance(criteria, list):
        problems.append("critères absents ou mal formés")
    else:
        received_ids = [item.get("id") for item in criteria
                        if isinstance(item, dict) and isinstance(item.get("id"), str)]
        if len(received_ids) != len(criteria):
            problems.append("au moins un critère est mal formé")
        if len(received_ids) != len(set(received_ids)):
            problems.append("identifiants de critères dupliqués")
        missing = sorted(set(expected_by_id) - set(received_ids))
        unknown = sorted(set(received_ids) - set(expected_by_id))
        if missing:
            problems.append("critères attendus absents : " + ", ".join(missing))
        if unknown:
            problems.append("critères inconnus : " + ", ".join(unknown))
        for criterion in criteria:
            if not isinstance(criterion, dict):
                continue
            criterion_id = criterion.get("id")
            if not isinstance(criterion_id, str):
                continue
            if criterion_id in expected_by_id and criterion.get("critere") != expected_by_id[criterion_id]:
                problems.append(f"{criterion_id} : libellé différent de l'attendu")
            status = criterion.get("statut")
            if not isinstance(status, str) or status not in VALID_CRITERION_STATUSES:
                problems.append(f"{criterion_id} : statut invalide")
            elif semantic and status != "SATISFAIT":
                problems.append(f"{criterion_id} : critère non entièrement satisfait")
            note = criterion.get("note")
            if not isinstance(note, str) or not note.strip():
                problems.append(f"{criterion_id} : justification vide")

    errors = result.get("erreurs")
    if not isinstance(errors, list):
        problems.append("champ erreurs absent ou mal formé")
    elif semantic and errors:
        problems.append("le juge a détecté au moins une erreur")

    verdict = result.get("verdict")
    legal = result.get("verdict_fiabilite_juridique")
    architecture = result.get("verdict_architecture")
    if not isinstance(verdict, str) or verdict not in VALID_GLOBAL_VERDICTS:
        problems.append("verdict global absent ou invalide")
    elif semantic and verdict != "REUSSITE":
        problems.append("verdict global en échec")
    if not isinstance(legal, str) or legal not in VALID_GLOBAL_VERDICTS:
        problems.append("verdict juridique absent ou invalide")
    elif semantic and legal != "REUSSITE":
        problems.append("fiabilité juridique en échec")
    if not isinstance(architecture, str) or architecture not in VALID_ARCHITECTURE_VERDICTS:
        problems.append("verdict d'architecture absent ou invalide")
    elif semantic and architecture == "ECHEC":
        problems.append("architecture en échec")
    elif semantic and case.get("type") == "architectural" and architecture != "REUSSITE":
        problems.append("cas architectural sans réussite d'architecture")
    for field in ("score_sur_5", "score_architecture_sur_5", "score_fiabilite_juridique_sur_5"):
        value = result.get(field)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 5:
            problems.append(f"{field} absent ou hors de l'intervalle 0–5")
    synthesis = result.get("synthese")
    if not isinstance(synthesis, str) or not synthesis.strip():
        problems.append("synthèse absente ou vide")
    if errors and (verdict == "REUSSITE" or legal == "REUSSITE"):
        problems.append("verdict incohérent avec les erreurs détectées")
    return problems


def load_evidence(path: str | None) -> tuple[list[dict], str | None]:
    if not path:
        return [], None
    evidence_path = Path(path).expanduser().resolve()
    data = json.loads(evidence_path.read_text(encoding="utf-8"))
    consultations = data.get("consultations") if isinstance(data, dict) else None
    if not isinstance(consultations, list):
        raise SystemExit("Le fichier de preuve doit contenir une liste consultations")
    return consultations, hashlib.sha256(evidence_path.read_bytes()).hexdigest()


def validate_evidence(consultations: list[dict], cases: list[dict], mode: str, evidence_mode: str,
                      evidence_root: Path | None = None, as_of: datetime | None = None) -> list[str]:
    if evidence_mode != "live":
        return []
    problems = []
    required_ids = {
        case["id"] for case in cases
        if mode == "integration" and case.get("preuve_requise", case.get("type") != "echec_attendu")
    }
    by_case: dict[str, list[dict]] = {}
    fields = ("case_id", "source_url", "consulted_at", "version_or_date", "supporting_excerpt", "conclusion_supported")
    for index, item in enumerate(consultations, start=1):
        if not isinstance(item, dict):
            problems.append(f"trace {index} mal formée")
            continue
        missing = [field for field in fields if not isinstance(item.get(field), str) or not item[field].strip()]
        if missing:
            problems.append(f"trace {index} : champs vides {', '.join(missing)}")
        case_id = item.get("case_id")
        if not isinstance(case_id, str):
            problems.append(f"trace {index} : identifiant de cas invalide")
            continue
        if case_id not in {case["id"] for case in cases}:
            problems.append(f"trace {index} : cas inconnu ou inactif {case_id}")
            continue
        for issue in live_sources.verify_trace(item, evidence_root or HERE, as_of=as_of):
            problems.append(f"trace {index} : {issue}")
        by_case.setdefault(case_id, []).append(item)
    missing_cases = sorted(required_ids - set(by_case))
    if missing_cases:
        problems.append("cas sans preuve de consultation : " + ", ".join(missing_cases))
    if mode=='integration':
        for case in cases:
            required=case.get('required_source_ids',[])
            if not isinstance(required,list) or any(not isinstance(x,str) or not x.strip() for x in required):
                problems.append(case['id']+' : liste des sources requises invalide');continue
            actual={trace.get('source_id') for trace in by_case.get(case['id'],[])}
            missing=sorted(set(required)-actual)
            if missing:problems.append(case['id']+' : sources requises non consultées : '+', '.join(missing))
    return problems


def case_for_mode(case: dict, mode: str) -> dict:
    result = {**case, "mode_evaluation": mode}
    if mode == "degraded" and "attendus_degraded" in case:
        result["attendus"] = case["attendus_degraded"]
        result["echec_si"] = case["echec_si_degraded"]
    return result


def active_cases(all_cases: list[dict], mode: str, selected: list[str]) -> list[dict]:
    cases = [case for case in all_cases if mode in case.get("modes", ["integration", "degraded"])]
    if selected:
        wanted = set(selected)
        cases = [case for case in cases if case["id"] in wanted]
        missing = wanted - {case["id"] for case in cases}
        if missing:
            raise SystemExit("Cas inconnus ou inactifs : " + ", ".join(sorted(missing)))
    return [case_for_mode(case, mode) for case in cases]


def campaign_signature(provenance: dict) -> dict:
    keys = (
        "mode", "provider_repondant", "modele_repondant", "effort_repondant",
        "context_mode", "evidence_mode", "sha256_cas", "sha256_compagnon", "sha256_source_pack",
        "case_ids", "evidence_sha256",
        "drh_fpt", "recherche_juridique", "context_sha256_by_case", "suite", "suite_registry_sha256", "suite_seal_sha256",
        "execution_profile", "native_runtime_sha256_by_case", "cli_versions",
    )
    return {key: provenance.get(key) for key in keys}


def resolve_campaign(raw: str) -> Path:
    candidate = Path(raw)
    if candidate.is_dir():
        return candidate.resolve()
    candidate = RESULTS / raw
    if candidate.is_dir():
        return candidate.resolve()
    raise SystemExit(f"Campagne introuvable : {raw}")


def response_path(campaign: Path, case_id: str) -> Path:
    return campaign / f"{case_id}-response.json"


def read_answer(campaign: Path, case_id: str) -> tuple[str, dict]:
    structured = response_path(campaign, case_id)
    if structured.is_file():
        data = json.loads(structured.read_text(encoding="utf-8"))
        return data["answer"], data
    legacy = campaign / f"{case_id}.md"
    if legacy.is_file():
        text = legacy.read_text(encoding="utf-8")
        marker = "## Réponse (contexte vierge)\n"
        if marker in text:
            return text.split(marker, 1)[1].rstrip(), {"legacy": True}
    raise FileNotFoundError(f"Réponse absente pour {case_id}")


def write_answer(campaign: Path, case: dict, answer: str, completion: Completion, metadata: dict) -> None:
    if completion.provider_trace is not None:
        trace_file = campaign / f"{case['id']}-respondant.jsonl"
        trace_file.write_bytes(completion.provider_trace.encode("utf-8"))
        metadata["provider_trace_sha256"] = sha256_text(completion.provider_trace)
    payload = {
        "id": case["id"], "branche": case["branche"], "answer": answer,
        "truncated": completion.truncated, "metrics": {
            "duration_ms": completion.duration_ms, "usage": completion.usage,
            "response_id": completion.response_id,
        }, **metadata,
    }
    response_path(campaign, case["id"]).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (campaign / f"{case['id']}.md").write_text(
        f"# {case['branche']}\n\n## Question\n{case['prompt']}\n\n"
        f"## Réponse (contexte vierge)\n{answer}\n", encoding="utf-8",
    )


def validate_strict_campaign(provenance: dict, cases: list[dict], results: list[dict], subset: bool = False, *, semantic: bool = True) -> list[str]:
    problems = []
    if subset:
        problems.append("une sélection de cas est diagnostique et ne constitue pas une campagne complète")
    else:
        try:
            suite = suites.load_suite(provenance.get('suite','developpement'))
            expected = suite['expected_per_mode']
            if len(cases) != expected:
                problems.append(f"{len(cases)} cas actifs au lieu de {expected}")
            if suite['qualification']:
                families={'codex':'openai','openai':'openai','anthropic':'anthropic','claude-cli':'anthropic'}
                if families.get(provenance.get('provider_repondant')) == families.get(provenance.get('provider_juge')):
                    problems.append('qualification : familles répondant et juge identiques')
                if provenance.get('suite_seal_sha256') != suite['seal_sha256']:
                    problems.append('qualification : gel différent ou absent')
        except (ValueError,OSError):
            problems.append('suite inconnue, non approuvée ou gel invalide')
    if (
        provenance.get("provider_juge")
        and provenance.get("modele_juge")
        and provenance.get("provider_repondant") == provenance.get("provider_juge")
        and provenance.get("modele_repondant") == provenance.get("modele_juge")
    ):
        problems.append("le juge strict doit utiliser un modèle distinct du répondant")
    if provenance.get("mode") == "integration" and provenance.get("evidence_mode") != "live":
        problems.append("une campagne stricte d'intégration exige evidence_mode=live")
    ids = [entry.get("id") for entry in results]
    if len(ids) != len(set(ids)):
        problems.append("identifiants de cas dupliqués dans le bilan")
    missing = sorted({case["id"] for case in cases} - set(ids))
    if missing:
        problems.append("cas sans résultat : " + ", ".join(missing))
    for skill in ("drh_fpt", "recherche_juridique"):
        item = provenance.get(skill) or {}
        if skill == "recherche_juridique" and provenance.get("mode") != "integration":
            continue
        if not item.get("commit"):
            problems.append(f"SHA Git {skill} absent")
        if item.get("dirty") is not False:
            problems.append(f"dépôt {skill} non propre ou état indéterminé")
    for entry in results:
        case_id = entry.get("id", "inconnu")
        if entry.get("statut") != "ok":
            problems.append(f"{case_id} : erreur d'exécution")
        if entry.get("tronque"):
            problems.append(f"{case_id} : réponse ou jugement tronqué")
        if semantic:
            for issue in entry.get("validation", ["évaluation absente"]):
                problems.append(f"{case_id} : {issue}")
    return problems


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('--suite', default='developpement')
    parser.add_argument('--execution-profile', choices=('assembled','claude-native'), default='assembled')
    parser.add_argument("--provider", choices=("anthropic", "openai", "codex", "claude-cli"), default="anthropic")
    parser.add_argument("--judge-provider", choices=("anthropic", "openai", "codex", "claude-cli"))
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--judge-model", default=DEFAULT_JUDGE_MODEL)
    parser.add_argument("--reasoning-effort")
    parser.add_argument("--judge-reasoning-effort")
    parser.add_argument("--judge", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--mode", choices=("integration", "degraded"), default="integration")
    parser.add_argument("--legal-skill")
    parser.add_argument("--workers", type=int, choices=range(1, 5), default=1)
    parser.add_argument("--case", action="append", default=[])
    parser.add_argument("--resume")
    parser.add_argument("--judge-only")
    parser.add_argument("--context-mode", choices=("full", "selective"), default="full")
    parser.add_argument("--evidence-mode", choices=("rules", "snapshot", "live"), default="rules")
    parser.add_argument("--source-pack")
    parser.add_argument("--evidence-file")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.judge_only:
        args.judge = True
    if args.strict and not args.judge:
        raise SystemExit("--strict exige --judge")
    if args.resume and args.judge_only:
        raise SystemExit("Utilise --resume ou --judge-only, pas les deux")
    if args.evidence_mode == "snapshot" and not args.source_pack:
        raise SystemExit("--evidence-mode snapshot exige --source-pack")
    if args.evidence_mode == "live" and not args.evidence_file:
        raise SystemExit("--evidence-mode live exige --evidence-file")
    if args.mode == "degraded" and args.evidence_mode == "live":
        raise SystemExit("Le mode dégradé ne peut pas déclarer une vérification live")
    selected = [item for group in args.case for item in group.split(",") if item]
    if args.execution_profile=='claude-native' and args.provider!='claude-cli':
        raise SystemExit('Le profil natif exige claude-cli')
    try:
        suite = suites.load_suite(args.suite)
    except (ValueError,OSError) as exc:
        raise SystemExit(str(exc)) from exc
    if suite['qualification'] and (selected or args.resume or args.judge_only):
        raise SystemExit('Qualification : sélection et relance interdites')
    if suite['qualification'] and args.mode=='integration' and args.evidence_mode!='live':
        raise SystemExit('Qualification intégration : evidence_mode=live requis avant réservation et génération')
    if suite['qualification']:
        state=git_provenance(ROOT)
        if state.get('dirty') is not False or (not suite.get('reserve_for') and state.get('commit')!=suite['runtime_commit']):
            raise SystemExit('Qualification : commit gelé propre requis avant tout appel')
    all_cases = suite['cases']
    cases = active_cases(all_cases, args.mode, selected)
    for case in cases:
        normalized_expectations(case)
        if args.context_mode == "selective":
            context_loader.files_for_case(case)

    legal_bundle = None
    legal_path = None
    legal_sources: list[str] = []
    if args.mode == "integration":
        if not args.legal_skill and not (args.resume or args.judge_only):
            raise SystemExit("--legal-skill est obligatoire en mode integration")
        if args.legal_skill:
            legal_bundle, legal_path, legal_sources = load_legal_skill(args.legal_skill)
    source_pack, source_pack_path, source_pack_files = load_source_pack(args.source_pack)
    evidence, evidence_sha = load_evidence(args.evidence_file)
    evidence_problems = validate_evidence(evidence, active_cases(all_cases, args.mode, []), args.mode,
        args.evidence_mode, Path(args.evidence_file).resolve().parent if args.evidence_file else None)
    if evidence_problems:
        raise SystemExit("Preuves invalides avant génération :\n" + "\n".join(evidence_problems))

    full_bundle_path = find_bundle()
    full_bundle = full_bundle_path.read_text(encoding="utf-8")
    cases_sha = sha256_text(Path(suite['cases_path']).read_text(encoding="utf-8"))
    judge_provider = args.judge_provider or args.provider
    if suite['qualification']:
        families={'codex':'openai','openai':'openai','claude-cli':'anthropic','anthropic':'anthropic'}
        if not args.strict or not args.judge or families[args.provider]==families[judge_provider]:
            raise SystemExit('Qualification : strict, juge et familles distinctes requis')
        if args.provider=='claude-cli' and args.execution_profile!='claude-native':
            raise SystemExit('Qualification Claude : profil natif requis')
        if args.provider not in {'codex','claude-cli'} or judge_provider not in {'codex','claude-cli'}:
            raise SystemExit('Qualification : CLI Codex et Claude exacts requis')
    now = datetime.now(timezone.utc)
    contexts = {}
    native_signatures={}
    for case in cases:
        if args.context_mode == "selective":
            drh_context, loaded_files = context_loader.build_case_context(case)
        else:
            drh_context, loaded_files = full_bundle, [str(full_bundle_path)]
        case_evidence = [item for item in evidence if item.get("case_id") == case["id"]]
        system = build_system_context(drh_context, legal_bundle, args.mode, source_pack,
            args.evidence_mode, case_evidence)
        contexts[case["id"]] = (system, context_loader.context_metrics(drh_context, loaded_files), case_evidence)
        if args.execution_profile=='claude-native':
            import native_runtime
            with tempfile.TemporaryDirectory(prefix='drh-native-preflight-') as temporary:
                runtime=native_runtime.stage(Path(temporary)/'project',ROOT,args.mode,case['id'],case_evidence,legal_path,
                    proof_required=case.get('preuve_requise',case.get('type')!='echec_attendu'))
                native_signatures[case['id']]=native_runtime.signature(runtime)
    base_provenance = {
        'suite': args.suite,
        'suite_registry_sha256': suite['registry_sha256'],
        'suite_seal_sha256': suite['seal_sha256'],
        'execution_profile': args.execution_profile,
        'native_runtime_sha256_by_case': native_signatures,
        "mode": args.mode,
        "provider_repondant": args.provider,
        "modele_repondant": args.model,
        "effort_repondant": args.reasoning_effort,
        "provider_juge": judge_provider if args.judge else None,
        "modele_juge": args.judge_model if args.judge else None,
        "effort_juge": args.judge_reasoning_effort if args.judge else None,
        "context_mode": args.context_mode,
        "evidence_mode": args.evidence_mode,
        "sha256_cas": cases_sha,
        "sha256_compagnon": sha256_text(legal_bundle or "") if legal_bundle else None,
        "sha256_source_pack": sha256_text(source_pack) if source_pack else None,
        "case_ids": [case["id"] for case in cases],
        "evidence_sha256": evidence_sha,
        "evidence_file": str(Path(args.evidence_file).resolve()) if args.evidence_file else None,
        "drh_fpt": {"version": read_skill_version(), "bundle": str(full_bundle_path),
            "sha256_bundle": sha256_text(full_bundle), **git_provenance(ROOT)},
        "recherche_juridique": ({"version": read_version_from_text(legal_bundle or ""),
            "chemin": str(legal_path), "sources_chargees": legal_sources,
            **git_provenance(legal_path or ROOT)} if args.mode == "integration" else {}),
        "context_sha256_by_case": {key: sha256_text(value[0]) for key, value in contexts.items()},
        "judge_context_sha256_by_case": {key:sha256_text(value[0]) for key,value in contexts.items()},
    }
    if suite['qualification']:
        base_provenance['cli_versions']=suites.cli_versions()
        slot=('claude-native' if args.execution_profile=='claude-native' else args.provider)+':'+args.mode
        suites.validate_profile(suite,slot,base_provenance)
    if args.execution_profile=='claude-native':
        base_provenance['context_sha256_by_case']={c['id']:sha256_text(native_runtime.prompt(c,args.mode)+native_signatures[c['id']]) for c in cases}

    resumed_from = args.resume or args.judge_only
    if resumed_from:
        campaign = resolve_campaign(resumed_from)
        provenance = json.loads((campaign / "_provenance.json").read_text(encoding="utf-8"))
        if args.mode == "integration" and legal_bundle is None:
            raise SystemExit("Une reprise en intégration exige --legal-skill pour reconstruire le contexte")
        if campaign_signature(provenance) != campaign_signature(base_provenance):
            raise SystemExit("Configuration incompatible avec la campagne existante")
    else:
        campaign_id = f"{now.strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
        campaign = RESULTS / campaign_id
        campaign.mkdir(parents=True, exist_ok=False)
        provenance = {
            "campagne_id": campaign_id,
            "date_debut_utc": now.isoformat(),
            **base_provenance,
            "drh_fpt": {
                "version": read_skill_version(), "bundle": str(full_bundle_path),
                "sha256_bundle": sha256_text(full_bundle), **git_provenance(ROOT),
            },
            "recherche_juridique": (
                {
                    "version": read_version_from_text(legal_bundle or ""), "chemin": str(legal_path),
                    "sources_chargees": legal_sources, **git_provenance(legal_path or ROOT),
                } if args.mode == "integration" else {}
            ),
            "source_pack": {"chemin": str(source_pack_path) if source_pack_path else None, "fichiers": source_pack_files},
            "evidence_sha256": evidence_sha,
            "nombre_cas_actifs": len(cases),
            "selection_diagnostique": bool(selected),
        }
        (campaign / "_provenance.json").write_text(
            json.dumps(provenance, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    if suite['qualification']:
        suites.claim_launch(suite,RESULTS/'qualification-launches.json',
            ('claude-native' if args.execution_profile=='claude-native' else args.provider)+':'+args.mode,
            provenance['campagne_id'],provenance['drh_fpt']['commit'])

    respondent_key = None if args.judge_only else key_for_provider(args.provider)
    judge_key = key_for_provider(judge_provider) if args.judge else None
    evaluation_id = None
    evaluation_dir = None
    if args.judge:
        evaluation_id = f"{now.strftime('%Y%m%dT%H%M%SZ')}-{judge_provider}-{uuid.uuid4().hex[:6]}"
        evaluation_dir = campaign / "evaluations" / evaluation_id
        evaluation_dir.mkdir(parents=True, exist_ok=False)

    def execute_case(case):
        case_id = case["id"]
        print(f"{args.mode} {case_id} : génération / évaluation", flush=True)
        system, context_meta, case_evidence = contexts[case_id]
        entry = {"id": case_id, "branche": case["branche"], "statut": "ok", "validation": []}
        try:
            answer, response_meta = read_answer(campaign, case_id)
            if not (args.resume or args.judge_only):
                raise FileNotFoundError
        except FileNotFoundError:
            if args.judge_only:
                entry.update({"statut": "erreur", "erreur": "réponse absente"})
                return entry
            try:
                native_meta={}
                if args.execution_profile=='claude-native':
                    import claude_cli
                    with tempfile.TemporaryDirectory(prefix='drh-native-case-') as temporary:
                        runtime=native_runtime.stage(Path(temporary)/'project',ROOT,args.mode,case_id,case_evidence,legal_path,
                            proof_required=case.get('preuve_requise',case.get('type')!='echec_attendu'))
                        if native_runtime.signature(runtime)!=native_signatures[case_id]:
                            raise ApiCallError('Runtime natif différent du précontrôle')
                        archive_directory=campaign/'runtime'/case_id
                        if archive_directory.exists():
                            archive_directory=campaign/'runtime'/(case_id+'-attempts')/uuid.uuid4().hex
                        native_runtime.archive(runtime,archive_directory)
                        completion=claude_cli.complete_cli(args.model,'',native_runtime.prompt(case,args.mode),
                            MAX_TOKENS_REPONDANT,args.reasoning_effort,runtime=runtime)
                        native_meta={'native_runtime_sha256':native_signatures[case_id],
                                     'native_runtime_directory':archive_directory.relative_to(campaign).as_posix(),
                                     'execution_profile':'claude-native'}
                else:
                    completion = complete(
                        args.provider, respondent_key or "", args.model, system, case["prompt"],
                        MAX_TOKENS_REPONDANT, args.reasoning_effort,
                    )
            except (ApiCallError,ValueError,OSError) as exc:
                entry.update({"statut": "erreur", "erreur": str(exc)})
                if getattr(exc,'provider_trace',None):
                    failure_path=campaign/f'{case_id}-respondant-failed.jsonl'
                    if failure_path.exists():failure_path=campaign/f'{case_id}-respondant-failed-{uuid.uuid4().hex}.jsonl'
                    failure_path.write_bytes(exc.provider_trace.encode('utf8'))
                    entry['failed_trace_sha256']=sha256_text(exc.provider_trace)
                    entry['failed_trace_file']=failure_path.name
                return entry
            answer = completion.text
            response_meta = {"truncated": completion.truncated, "metrics": {"usage": completion.usage}}
            metadata={"context":context_meta}
            if native_meta:
                metadata={'judge_context':context_meta,'context':{'profile':'claude-native',
                    'runtime_sha256':native_signatures[case_id],'loaded_files':completion.usage.get('loaded_files',[])}}
            write_answer(campaign, case, answer, completion, {**metadata,**native_meta})

        entry["tronque"] = bool(response_meta.get("truncated"))
        entry["respondant_metrics"] = response_meta.get("metrics", {})
        if args.judge and evaluation_dir is not None:
            case_evidence = [item for item in evidence if item.get("case_id") == case_id]
            try:
                completion = complete(
                    judge_provider, judge_key or "", args.judge_model,
                    JUDGE_SYSTEM + "\n\nCORPUS DE CAMPAGNE :\n" + system,
                    judge_prompt(case, answer, case_evidence), MAX_TOKENS_JUGE,
                    args.judge_reasoning_effort,
                )
                evaluation = parse_judge_completion(completion)
            except ApiCallError as exc:
                entry.update({"statut": "erreur", "erreur": str(exc)})
                if exc.provider_trace:
                    (evaluation_dir/f'{case_id}-juge-failed.jsonl').write_bytes(exc.provider_trace.encode('utf8'))
                    entry['failed_judge_trace_sha256']=sha256_text(exc.provider_trace)
                return entry
            (evaluation_dir / f"{case_id}-eval.json").write_text(
                json.dumps(evaluation, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            if completion.provider_trace is not None:
                (evaluation_dir / f"{case_id}-juge.jsonl").write_bytes(completion.provider_trace.encode("utf-8"))
                entry["juge_trace_sha256"] = sha256_text(completion.provider_trace)
            entry["validation"] = validate_judge_result(evaluation, case)
            entry["tronque"] = entry["tronque"] or evaluation.get("tronque", False)
            entry["score_sur_5"] = evaluation.get("score_sur_5")
            entry["verdict"] = evaluation.get("verdict")
            entry["juge_metrics"] = evaluation.get("metriques", {})
        return entry

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        results = list(executor.map(execute_case, cases))

    evaluation_provenance = {
        **provenance,
        "provider_juge": judge_provider if args.judge else None,
        "modele_juge": args.judge_model if args.judge else None,
        "effort_juge": args.judge_reasoning_effort if args.judge else None,
    }
    strict_problems = list(evidence_problems)
    if args.strict:
        strict_problems.extend(
            validate_strict_campaign(evaluation_provenance, cases, results, subset=bool(selected))
        )
    input_tokens = sum(
        (entry.get("respondant_metrics", {}).get("usage", {}).get("input_tokens") or 0)
        + (entry.get("juge_metrics", {}).get("usage", {}).get("input_tokens") or 0)
        for entry in results
    )
    output_tokens = sum(
        (entry.get("respondant_metrics", {}).get("usage", {}).get("output_tokens") or 0)
        + (entry.get("juge_metrics", {}).get("usage", {}).get("output_tokens") or 0)
        for entry in results
    )
    report = {
        "campagne_id": provenance["campagne_id"], "evaluation_id": evaluation_id,
        "provenance_evaluation": evaluation_provenance,
        "date_fin_utc": datetime.now(timezone.utc).isoformat(), "cas": results,
        "metriques": {"input_tokens": input_tokens, "output_tokens": output_tokens},
        "cout": None,
        "note_cout": "Aucun coût calculé sans grille tarifaire datée et vérifiée.",
        "gate_strict": {"active": args.strict, "reussite": args.strict and not strict_problems, "motifs_echec": strict_problems},
    }
    destination = evaluation_dir / "_bilan.json" if evaluation_dir else campaign / "_bilan.json"
    if destination.exists():
        history=campaign/'report-history';history.mkdir(exist_ok=True)
        (history/(uuid.uuid4().hex+'.json')).write_bytes(destination.read_bytes())
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Campagne : {campaign}")
    if evaluation_dir:
        print(f"Évaluation : {evaluation_dir}")
    print(f"Cas : {len(cases)} — entrée {input_tokens} tokens — sortie {output_tokens} tokens")
    if args.strict:
        print("Gate strict : " + ("RÉUSSITE" if not strict_problems else "ÉCHEC"))
        for problem in strict_problems:
            print(f"- {problem}")
    return 1 if strict_problems or any(entry.get('statut')!='ok' for entry in results) else 0
