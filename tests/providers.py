"""Adaptateurs HTTP minimaux pour les campagnes LLM du dépôt."""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass


RETRY_DELAYS = (2, 4, 8)
RETRYABLE_HTTP_STATUS = {408, 409, 429, 500, 502, 503, 504, 529}


class ApiCallError(RuntimeError):
    """Échec d'un appel après épuisement des tentatives."""


@dataclass
class Completion:
    text: str
    truncated: bool
    usage: dict
    response_id: str | None
    duration_ms: int


def key_for_provider(provider: str) -> str:
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


def complete(
    provider: str,
    key: str,
    model: str,
    system: str,
    user: str,
    max_tokens: int,
    reasoning_effort: str | None = None,
) -> Completion:
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
