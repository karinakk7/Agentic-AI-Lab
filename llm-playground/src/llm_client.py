from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# USD → EUR (fixed rate, September 2026)
_USD_TO_EUR = 0.92

# (input $/1M, output $/1M) — Quellen: models.md / artificialanalysis.ai
_PRICING: dict[str, tuple[float, float]] = {
    "claude-opus-5":          (5.00, 25.00),
    "claude-fable-5-1":       (10.00, 50.00),
    "claude-sonnet-5":        (2.00, 10.00),
    "gpt-6-astra":            (10.00, 50.00),
    "gpt-5.6-sol":            (4.00, 20.00),
    "mistral-medium-3.5-pro": (1.50, 7.50),
    "gemini-3.8-flash":       (0.75, 3.75),
}


@dataclass
class LLMResponse:
    text: str
    model: str
    input_tokens: int
    output_tokens: int
    cost_eur: float
    latency_ms: int


def _cost_eur(model: str, in_tok: int, out_tok: int) -> float:
    in_p, out_p = _PRICING.get(model, (0.0, 0.0))
    usd = (in_tok * in_p + out_tok * out_p) / 1_000_000
    return round(usd * _USD_TO_EUR, 6)


def _log(entry: dict) -> None:
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    with open(log_dir / "calls.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ── Provider implementations ────────────────────────────────────────────────

def _anthropic(prompt: str, model: str, system: str, **kwargs) -> LLMResponse:
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    t0 = time.monotonic()
    msg = client.messages.create(
        model=model,
        max_tokens=kwargs.get("max_tokens", 1024),
        system=system if system else anthropic.NOT_GIVEN,
        messages=[{"role": "user", "content": prompt}],
    )
    latency_ms = int((time.monotonic() - t0) * 1000)
    in_tok, out_tok = msg.usage.input_tokens, msg.usage.output_tokens
    return LLMResponse(
        text=msg.content[0].text,
        model=model,
        input_tokens=in_tok,
        output_tokens=out_tok,
        cost_eur=_cost_eur(model, in_tok, out_tok),
        latency_ms=latency_ms,
    )


def _openai(prompt: str, model: str, system: str, **kwargs) -> LLMResponse:
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    t0 = time.monotonic()
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=kwargs.get("max_tokens", 1024),
    )
    latency_ms = int((time.monotonic() - t0) * 1000)
    in_tok, out_tok = resp.usage.prompt_tokens, resp.usage.completion_tokens
    return LLMResponse(
        text=resp.choices[0].message.content,
        model=model,
        input_tokens=in_tok,
        output_tokens=out_tok,
        cost_eur=_cost_eur(model, in_tok, out_tok),
        latency_ms=latency_ms,
    )


def _mistral(prompt: str, model: str, system: str, **kwargs) -> LLMResponse:
    from mistralai import Mistral
    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    t0 = time.monotonic()
    resp = client.chat.complete(
        model=model,
        messages=messages,
        max_tokens=kwargs.get("max_tokens", 1024),
    )
    latency_ms = int((time.monotonic() - t0) * 1000)
    in_tok, out_tok = resp.usage.prompt_tokens, resp.usage.completion_tokens
    return LLMResponse(
        text=resp.choices[0].message.content,
        model=model,
        input_tokens=in_tok,
        output_tokens=out_tok,
        cost_eur=_cost_eur(model, in_tok, out_tok),
        latency_ms=latency_ms,
    )


# ── Router ───────────────────────────────────────────────────────────────────

_ROUTERS: dict[str, callable] = {
    "claude":   _anthropic,
    "gpt":      _openai,
    "mistral":  _mistral,
    "mixtral":  _mistral,
}


def complete(prompt: str, model: str, system: str = "", **kwargs) -> LLMResponse:
    """Routet anhand des Modellnamens zum passenden Provider-SDK."""
    for prefix, fn in _ROUTERS.items():
        if model.startswith(prefix):
            response = fn(prompt, model, system, **kwargs)
            _log({
                "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "model": response.model,
                "prompt_chars": len(prompt),
                "input_tokens": response.input_tokens,
                "output_tokens": response.output_tokens,
                "cost_eur": response.cost_eur,
                "latency_ms": response.latency_ms,
            })
            return response
    raise ValueError(
        f"Unbekanntes Modell: {model!r}. Erlaubte Prefixe: {list(_ROUTERS)}"
    )
