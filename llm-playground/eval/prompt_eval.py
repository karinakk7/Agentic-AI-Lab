"""Prompt-Eval: Vergleich von drei Prompt-Versionen gegen 5 Lieferanten-E-Mails.

15 API-Calls (3 Prompts × 5 E-Mails) → Outputs werden gedruckt und in
eval/prompt_results.json gespeichert, damit die manuelle Bewertung in
notes/tag07-prompts.md vorgenommen werden kann.

Ausführen:
    cd llm-playground
    python eval/prompt_eval.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src"))

load_dotenv(ROOT / ".env")

from llm_client import complete  # noqa: E402

MODEL = "gemini-3.8-flash"
MAX_TOKENS = 512
PROMPTS_DIR = ROOT / "prompts"
OUTPUT_FILE = Path(__file__).parent / "prompt_results.json"

PROMPT_FILES = ["extract_v1.md", "extract_v2.md", "extract_v3.md"]


def load_prompt(filename: str) -> str:
    return (PROMPTS_DIR / filename).read_text(encoding="utf-8")


def load_emails() -> list[dict]:
    return json.loads((PROMPTS_DIR / "emails.json").read_text(encoding="utf-8"))


def run_combination(prompt_template: str, email: dict, retries: int = 3) -> dict:
    prompt = prompt_template.replace("{{email}}", email["body"])
    for attempt in range(retries):
        try:
            r = complete(prompt, model=MODEL, system="", max_tokens=MAX_TOKENS)
            return {
                "email_id": email["id"],
                "email_label": email["label"],
                "output": r.text.strip(),
                "cost_eur": r.cost_eur,
                "latency_ms": r.latency_ms,
                "in_tok": r.input_tokens,
                "out_tok": r.output_tokens,
            }
        except Exception as exc:
            msg = str(exc)
            # Rate-limit: warte die vom Server angegebene Zeit + Puffer
            if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                wait = 30
                time.sleep(wait)
            elif "503" in msg or "UNAVAILABLE" in msg:
                time.sleep(10)
            else:
                raise
    raise RuntimeError(f"Alle {retries} Versuche fehlgeschlagen")


def main() -> None:
    console = Console()
    console.print(Rule("[bold blue]Prompt-Eval – 3 Versionen × 5 E-Mails"))
    console.print(f"[dim]Modell: {MODEL}  |  15 Calls[/dim]\n")

    prompts = {f: load_prompt(f) for f in PROMPT_FILES}
    emails = load_emails()

    results: dict[str, list[dict]] = {}
    total_cost = 0.0

    for pname, ptemplate in prompts.items():
        version = pname.replace(".md", "")
        console.print(f"\n[bold yellow]── {version.upper()} ──[/bold yellow]")
        results[version] = []

        for i, email in enumerate(emails):
            if i > 0:
                time.sleep(13)  # Gemini Free-Tier: 5 Req/Min → mind. 12 s Abstand
            console.print(f"  [dim]Email {email['id']}: {email['label']}[/dim]", end=" ")
            try:
                entry = run_combination(ptemplate, email)
                results[version].append(entry)
                total_cost += entry["cost_eur"]
                console.print(f"[green]✓[/green] {entry['latency_ms']} ms / {entry['cost_eur']:.5f} €")

                console.print(Panel(
                    entry["output"],
                    title=f"[dim]{version} · Email {email['id']}[/dim]",
                    border_style="dim",
                    padding=(0, 1),
                ))
            except Exception as exc:
                console.print(f"[red]ERROR: {exc}[/red]")
                results[version].append({
                    "email_id": email["id"],
                    "email_label": email["label"],
                    "output": f"ERROR: {exc}",
                    "cost_eur": 0.0,
                    "latency_ms": 0,
                    "in_tok": 0,
                    "out_tok": 0,
                })

        time.sleep(15)  # Pause zwischen Prompt-Versionen

    OUTPUT_FILE.write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    console.print(f"\n[bold]Gesamtkosten:[/bold] {total_cost:.4f} €")
    console.print(f"[dim]Outputs gespeichert in: {OUTPUT_FILE}[/dim]")
    console.print("[dim]→ Jetzt manuell bewerten und notes/tag07-prompts.md füllen[/dim]")


if __name__ == "__main__":
    main()
