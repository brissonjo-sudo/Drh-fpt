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
    python run_tests.py                 # répond aux 6 cas
    python run_tests.py --judge         # répond + évalue (LLM-as-judge)
    python run_tests.py --model claude-opus-4-8 --judge

Sorties : tests/resultats/<id>.md (réponse) et <id>-eval.json (évaluation).
"""
import os, sys, json, argparse, urllib.request, urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RESULTS = HERE / "resultats"
API_URL = "https://api.anthropic.com/v1/messages"


def find_bundle() -> Path:
    for c in (ROOT / "drh-fpt-bundle-pour-LLM.md", HERE / "drh-fpt-bundle-pour-LLM.md"):
        if c.exists():
            return c
    sys.exit("Bundle introuvable : place drh-fpt-bundle-pour-LLM.md à la racine du dépôt.")


def call_api(key: str, model: str, system: str, user: str, max_tokens: int = 2000) -> str:
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode(),
        headers={
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"Erreur API ({e.code}) : {e.read().decode()[:300]}")
    return "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")


JUDGE_SYSTEM = (
    "Tu es un évaluateur juridique rigoureux en droit de la fonction publique "
    "territoriale. On te donne une question, une réponse à évaluer, et une liste "
    "de critères attendus. Pour chaque critère, indique s'il est SATISFAIT, "
    "PARTIEL ou ABSENT, avec une justification d'une phrase. Repère aussi toute "
    "AFFIRMATION FAUSSE ou inventée (référence, montant, jurisprudence). "
    "Termine par un score global sur 5. Réponds UNIQUEMENT en JSON : "
    '{"criteres":[{"critere":"...","statut":"SATISFAIT|PARTIEL|ABSENT","note":"..."}],'
    '"erreurs":["..."],"score_sur_5":N,"synthese":"..."}'
)


def judge(key: str, model: str, prompt: str, answer: str, attendus: list) -> dict:
    crit = "\n".join(f"- {a}" for a in attendus)
    user = (
        f"QUESTION POSÉE :\n{prompt}\n\n"
        f"RÉPONSE À ÉVALUER :\n{answer}\n\n"
        f"CRITÈRES ATTENDUS :\n{crit}\n\n"
        "Évalue selon les consignes. JSON uniquement."
    )
    raw = call_api(key, model, JUDGE_SYSTEM, user, max_tokens=1500)
    raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"score_sur_5": None, "synthese": "Réponse du juge non parsable", "raw": raw}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="claude-sonnet-4-6", help="modèle répondant")
    ap.add_argument("--judge-model", default="claude-opus-4-8", help="modèle juge")
    ap.add_argument("--judge", action="store_true", help="activer l'évaluation")
    args = ap.parse_args()

    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("Définis ANTHROPIC_API_KEY dans ton environnement.")

    system = find_bundle().read_text(encoding="utf-8")
    cases = json.loads((HERE / "cas-de-test.json").read_text(encoding="utf-8"))
    RESULTS.mkdir(exist_ok=True)

    scores = []
    for c in cases:
        print(f"\n=== {c['id']} — {c['branche']} ===")
        # Sous-agent vierge : ne voit que le skill (system) + le cas (user)
        answer = call_api(key, args.model, system, c["prompt"])
        (RESULTS / f"{c['id']}.md").write_text(
            f"# {c['branche']}\n\n## Question\n{c['prompt']}\n\n## Réponse (contexte vierge)\n{answer}\n",
            encoding="utf-8",
        )
        print(f"Réponse enregistrée ({len(answer)} caractères).")

        if args.judge:
            ev = judge(key, args.judge_model, c["prompt"], answer, c["attendus"])
            (RESULTS / f"{c['id']}-eval.json").write_text(
                json.dumps(ev, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            s = ev.get("score_sur_5")
            scores.append(s if isinstance(s, (int, float)) else 0)
            print(f"Score : {s}/5 — {ev.get('synthese','')[:100]}")

    if args.judge and scores:
        moy = sum(scores) / len(scores)
        print(f"\n=== BILAN : {moy:.1f}/5 sur {len(scores)} cas ===")
        (RESULTS / "_bilan.json").write_text(
            json.dumps({"scores": scores, "moyenne_sur_5": moy}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
