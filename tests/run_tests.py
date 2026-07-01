#!/usr/bin/env python3
"""
Harness de test du skill drh-fpt — sous-agents à contexte vierge.

Principe : chaque cas est traité par un appel API indépendant dont le SEUL
contexte est le bundle du skill (system) + le cas (user). Le modèle ne connaît
ni l'historique de conception, ni les réponses attendues : c'est un évaluateur
neutre. Un second appel (juge), tout aussi vierge, note la réponse contre la
grille d'attendus.

Usage :
    export ANTHROPIC_API_KEY=sk-...
    python run_tests.py                 # répond aux cas
    python run_tests.py --judge         # répond + évalue (LLM-as-judge)
    python run_tests.py --model claude-opus-4-8 --judge

Sorties : tests/resultats/<id>.md (réponse) et <id>-eval.json (évaluation),
tests/resultats/_bilan.json (bilan global).
"""
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
import argparse

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


def bundle_sha256_prefix(bundle_text: str, length: int = 12) -> str:
    return hashlib.sha256(bundle_text.encode("utf-8")).hexdigest()[:length]


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
    "AFFIRMATION FAUSSE ou inventée (référence, montant, jurisprudence). "
    "Termine par un score global sur 5 et un verdict global REUSSITE ou ECHEC. "
    "Réponds UNIQUEMENT en JSON : "
    '{"criteres":[{"critere":"...","statut":"SATISFAIT|PARTIEL|ABSENT","note":"..."}],'
    '"erreurs":["..."],"score_sur_5":N,"verdict":"REUSSITE|ECHEC","synthese":"..."}\n\n'
    "RÈGLES TRANSVERSES (s'appliquent quels que soient les critères ci-dessus) :\n"
    "1. Toute référence, montant ou jurisprudence qui semble INVENTÉ(E) (non "
    "vérifiable, incohérent avec le droit de la FPT, ou présenté avec une "
    "précision suspecte sans réserve) → verdict ECHEC, quel que soit le score "
    "par ailleurs.\n"
    "2. Toute valeur d'INDEXATION VOLATILE (point d'indice, taux de cotisation, "
    "plancher PSC...) donnée DE MÉMOIRE, sans réserve de vérification → le "
    "critère « données volatiles » (ou équivalent) est en ÉCHEC.\n"
    "3. Un PLAFOND RÉGLEMENTAIRE cité avec sa source DATÉE et accompagné de "
    "« à confirmer » (ou formulation équivalente de réserve) est ACCEPTABLE — "
    "ne pas le compter comme une erreur inventée.\n"
    "4. Si le cas fourni précise un champ 'echec_si' (liste de conditions "
    "d'échec spécifiques au cas), applique-le en plus des règles ci-dessus : "
    "si l'une des conditions est manifestement remplie par la réponse, le "
    "verdict global est ECHEC."
)


def judge(key: str, model: str, prompt: str, answer: str, attendus: list, echec_si: list | None = None) -> dict:
    crit = "\n".join(f"- {a}" for a in attendus)
    echec_si_block = ""
    if echec_si:
        echec_si_block = "\n\nCONDITIONS D'ÉCHEC SPÉCIFIQUES AU CAS (echec_si) :\n" + "\n".join(
            f"- {c}" for c in echec_si
        )
    user = (
        f"QUESTION POSÉE :\n{prompt}\n\n"
        f"RÉPONSE À ÉVALUER :\n{answer}\n\n"
        f"CRITÈRES ATTENDUS :\n{crit}"
        f"{echec_si_block}\n\n"
        "Évalue selon les consignes. JSON uniquement."
    )
    response = call_api(key, model, JUDGE_SYSTEM, user, max_tokens=MAX_TOKENS_JUGE)
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"modèle répondant (défaut {DEFAULT_MODEL})")
    ap.add_argument(
        "--judge-model", default=DEFAULT_JUDGE_MODEL,
        help=f"modèle juge (défaut {DEFAULT_JUDGE_MODEL})",
    )
    ap.add_argument("--judge", action="store_true", help="activer l'évaluation")
    args = ap.parse_args()

    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("Définis ANTHROPIC_API_KEY dans ton environnement.")

    bundle_path = find_bundle()
    system = bundle_path.read_text(encoding="utf-8")
    cases = json.loads((HERE / "cas-de-test.json").read_text(encoding="utf-8"))
    RESULTS.mkdir(exist_ok=True)

    scores = []
    non_evalues = 0
    cas_bilan = []

    for c in cases:
        print(f"\n=== {c['id']} — {c['branche']} ===")
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

        (RESULTS / f"{c['id']}.md").write_text(
            f"# {c['branche']}\n\n## Question\n{c['prompt']}\n\n## Réponse (contexte vierge)\n{answer}\n",
            encoding="utf-8",
        )
        print(f"Réponse enregistrée ({len(answer)} caractères).{' [TRONQUÉE]' if tronque else ''}")

        entry = {
            "id": c["id"],
            "branche": c["branche"],
            "statut": statut_cas,
            "tronque": tronque,
        }

        if args.judge:
            try:
                ev = judge(
                    key, args.judge_model, c["prompt"], answer, c["attendus"],
                    echec_si=c.get("echec_si"),
                )
            except ApiCallError as e:
                print(f"  ERREUR (juge) : {e}")
                entry["statut"] = "erreur"
                entry["erreur"] = str(e)
                cas_bilan.append(entry)
                continue

            (RESULTS / f"{c['id']}-eval.json").write_text(
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
            entry["tronque"] = entry["tronque"] or ev.get("tronque", False)
            print(f"Score : {s}/5 — verdict {verdict} — {ev.get('synthese', '')[:100]}")

        cas_bilan.append(entry)

    if args.judge:
        moy = sum(scores) / len(scores) if scores else None
        if moy is not None:
            print(f"\n=== BILAN : {moy:.1f}/5 sur {len(scores)} cas évalués ({non_evalues} non évalués) ===")
        else:
            print(f"\n=== BILAN : aucun score exploitable ({non_evalues} non évalués) ===")

        bundle_text = system
        bilan = {
            "cas": cas_bilan,
            "scores": scores,
            "moyenne_sur_5": moy,
            "non_evalues": non_evalues,
            "version_skill": read_skill_version(),
            "modele": args.model,
            "modele_juge": args.judge_model,
            "date": datetime.now(timezone.utc).isoformat(),
            "sha256_bundle": bundle_sha256_prefix(bundle_text),
        }
        (RESULTS / "_bilan.json").write_text(
            json.dumps(bilan, ensure_ascii=False, indent=2), encoding="utf-8"
        )


if __name__ == "__main__":
    main()
