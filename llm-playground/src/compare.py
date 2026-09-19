"""Sendet dieselbe Frage an alle 3 Anbieter und zeigt eine Rich-Vergleichstabelle."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from rich import box
from rich.console import Console
from rich.table import Table

from llm_client import LLMResponse, complete

PROMPT = "Erkläre in zwei Sätzen, warum zu viele Tokens im Kontext teuer werden können."
SYSTEM = "Du bist ein prägnanter KI-Erklärer. Antworte auf Deutsch."

MODELS = [
    "claude-opus-5",
    "gpt-5.6-sol",
    "gemini-3.8-flash",
]


def main() -> None:
    console = Console()
    console.rule("[bold blue]LLM Provider Vergleich")
    console.print(f"[dim]Frage:[/dim] {PROMPT}\n")

    results: list[LLMResponse] = []
    for model in MODELS:
        console.print(f"[yellow]→ {model}[/yellow] …", end=" ")
        try:
            r = complete(PROMPT, model=model, system=SYSTEM, max_tokens=256)
            results.append(r)
            console.print("[green]✓[/green]")
        except Exception as exc:
            console.print(f"[red]✗ {exc}[/red]")

    if not results:
        console.print("\n[red]Keine erfolgreichen Antworten.[/red]")
        return

    table = Table(box=box.ROUNDED, header_style="bold cyan", show_lines=True)
    table.add_column("Modell", style="bold", no_wrap=True)
    table.add_column("Kosten (€)", justify="right")
    table.add_column("Latenz (ms)", justify="right")
    table.add_column("Tokens (in/out)", justify="right")
    table.add_column("Antwort", max_width=55)

    for r in results:
        table.add_row(
            r.model,
            f"{r.cost_eur:.5f}",
            str(r.latency_ms),
            f"{r.input_tokens} / {r.output_tokens}",
            r.text.strip().replace("\n", " "),
        )

    console.print()
    console.print(table)
    console.print(
        f"\n[dim]Calls geloggt in logs/calls.jsonl[/dim]"
    )


if __name__ == "__main__":
    main()
