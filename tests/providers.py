"""Adaptateurs HTTP minimaux pour les campagnes LLM du dépôt."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from dataclasses import dataclass


RETRY_DELAYS = (2, 4, 8)
RETRYABLE_HTTP_STATUS = {408, 409, 429, 500, 502, 503, 504, 529}


class ApiCallError(RuntimeError):
    """Échec d'un appel après épuisement des tentatives."""
    def __init__(self,message,*,provider_trace=None):
        super().__init__(message)
        self.provider_trace=provider_trace


@dataclass
class Completion:
    text: str
    truncated: bool
    usage: dict
    response_id: str | None
    duration_ms: int
    provider_trace: str | None = None


def key_for_provider(provider: str) -> str:
    if provider in {"codex", "claude-cli"}:
        return ""  # L'authentification existante reste gérée par le CLI.
    env_name = {"anthropic": "ANTHROPIC_API_KEY", "openai": "OPENAI_API_KEY"}[provider]
    key = os.environ.get(env_name)
    if not key:
        raise ApiCallError(f"Définis {env_name} dans ton environnement.")
    return key


def _request(url: str, payload: dict, headers: dict) -> tuple[dict, int]:
    data = json.dumps(payload).encode("utf-8")
    last_error: ApiCallError | None = None
    started = time.monotonic()
    for attempt in range(len(RETRY_DELAYS) + 1):
        req = urllib.request.Request(url, data=data, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                body = json.loads(response.read())
                return body, round((time.monotonic() - started) * 1000)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode(errors="replace")[:500]
            last_error = ApiCallError(f"Erreur API HTTP {exc.code} : {detail}")
            if exc.code not in RETRYABLE_HTTP_STATUS or attempt >= len(RETRY_DELAYS):
                raise last_error
        except (urllib.error.URLError, TimeoutError) as exc:
            last_error = ApiCallError(f"Erreur réseau/timeout : {exc}")
            if attempt >= len(RETRY_DELAYS):
                raise last_error
        time.sleep(RETRY_DELAYS[attempt])
    raise last_error or ApiCallError("Échec API sans cause exploitable")


def _anthropic(
    key: str, model: str, system: str, user: str, max_tokens: int,
) -> Completion:
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "system": [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        "messages": [{"role": "user", "content": user}],
    }
    raw, duration = _request(
        "https://api.anthropic.com/v1/messages",
        payload,
        {
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
    )
    text = "".join(
        block.get("text", "")
        for block in raw.get("content", [])
        if block.get("type") == "text"
    )
    usage = raw.get("usage") or {}
    normalized_usage = {
        "input_tokens": usage.get("input_tokens"),
        "output_tokens": usage.get("output_tokens"),
        "cache_creation_input_tokens": usage.get("cache_creation_input_tokens"),
        "cache_read_input_tokens": usage.get("cache_read_input_tokens"),
    }
    return Completion(
        text=text,
        truncated=raw.get("stop_reason") == "max_tokens",
        usage=normalized_usage,
        response_id=raw.get("id"),
        duration_ms=duration,
    )


def _openai(
    key: str, model: str, system: str, user: str, max_tokens: int,
    reasoning_effort: str | None,
) -> Completion:
    payload = {
        "model": model,
        "instructions": system,
        "input": user,
        "max_output_tokens": max_tokens,
    }
    if reasoning_effort:
        payload["reasoning"] = {"effort": reasoning_effort}
    raw, duration = _request(
        "https://api.openai.com/v1/responses",
        payload,
        {"authorization": f"Bearer {key}", "content-type": "application/json"},
    )
    parts = []
    for output in raw.get("output", []):
        for content in output.get("content", []):
            if content.get("type") == "output_text":
                parts.append(content.get("text", ""))
    usage = raw.get("usage") or {}
    normalized_usage = {
        "input_tokens": usage.get("input_tokens"),
        "output_tokens": usage.get("output_tokens"),
        "total_tokens": usage.get("total_tokens"),
    }
    incomplete = raw.get("incomplete_details") or {}
    return Completion(
        text="".join(parts),
        truncated=raw.get("status") == "incomplete" and incomplete.get("reason") == "max_output_tokens",
        usage=normalized_usage,
        response_id=raw.get("id"),
        duration_ms=duration,
    )


def _codex(model: str, system: str, user: str, max_tokens: int,
           reasoning_effort: str | None) -> Completion:
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="drh-eval-") as isolated:
        command = ["codex", "exec", "--ignore-user-config", "--ephemeral",
            "--skip-git-repo-check", "--sandbox", "read-only", "--json",
            "--cd", isolated, "--model", model, "-c", 'web_search="disabled"']
        if reasoning_effort:
            command.extend(["-c", f'model_reasoning_effort="{reasoning_effort}"'])
        prompt = (
            "Évaluation isolée. Réponds à la question avec le corpus fourni. "
            "N'utilise aucun outil, fichier, skill installé, mémoire ni accès réseau. "
            "Tu n'as ni les autres cas ni leurs critères. "
            f"Vise une sortie de moins de {max_tokens} tokens (limite indicative du CLI).\n\n"
            f"<corpus>\n{system}\n</corpus>\n\n<question>\n{user}\n</question>"
        )
        try:
            result = subprocess.run(command, input=prompt, capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=300, check=False)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise ApiCallError(f"Exécution Codex impossible : {type(exc).__name__}") from exc
    if result.returncode:
        # Les logs ne sont pas incorporés dans une erreur publique : pas de secret accidentel.
        raise ApiCallError(f"Codex a échoué (code {result.returncode})")
    events = []
    for line in result.stdout.splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    messages, usage, response_id, finished = [], {}, None, False
    for event in events:
        if event.get("type") == "thread.started":
            response_id = event.get("thread_id")
        if event.get("type") in {"turn.failed", "error"}:
            raise ApiCallError("Échec de la session Codex")
        if event.get("type") == "item.completed":
            item = event.get("item", {})
            if item.get("type") == "agent_message":
                messages.append(item.get("text", ""))
            elif item.get("type") != "reasoning":
                raise ApiCallError("Outil inattendu : l'isolation de l'évaluation n'est pas respectée")
        if event.get("type") == "turn.completed":
            finished, usage = True, event.get("usage", {})
    if not finished or not messages or not messages[-1].strip():
        raise ApiCallError("Session Codex sans réponse finale complète")
    usage["output_token_limit_enforced"] = False
    return Completion(messages[-1], False, usage, response_id,
        round((time.monotonic() - started) * 1000), result.stdout)


def complete(
    provider: str,
    key: str,
    model: str,
    system: str,
    user: str,
    max_tokens: int,
    reasoning_effort: str | None = None,
) -> Completion:
    if provider == 'claude-cli':
        from claude_cli import complete_cli
        return complete_cli(model,system,user,max_tokens,reasoning_effort)
    if provider == "codex":
        return _codex(model, system, user, max_tokens, reasoning_effort)
    if provider == "anthropic":
        if reasoning_effort:
            raise ApiCallError(
                "--reasoning-effort n'est pas pris en charge par l'adaptateur Anthropic ; "
                "retire ce paramètre au lieu de le laisser silencieusement ignoré."
            )
        return _anthropic(key, model, system, user, max_tokens)
    if provider == "openai":
        return _openai(key, model, system, user, max_tokens, reasoning_effort)
    raise ApiCallError(f"Fournisseur non pris en charge : {provider}")
