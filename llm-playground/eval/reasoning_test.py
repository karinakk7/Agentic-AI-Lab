"""Reasoning-Eval: Lohnt sich Extended Thinking für verschiedene Aufgabentypen?

Drei Tasks × 2 Modi (Standard / Extended Thinking) → 6 API-Calls.
Metriken: korrekt (ja/nein), Kosten (€-Cent), Latenz (ms).

Erwartetes Ergebnis:
  Task 1 (Extraktion):      Standard = korrekt, Thinking = korrekt + teurer → Overkill
  Task 2 (Mehrstufige Logik): Standard = ggf. falsch, Thinking = korrekt   → lohnt sich
  Task 3 (Planung):         Beide korrekt, Thinking marginal besser         → neutral
"""
from __future__ import annotations

import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from rich import box
from rich.console import Console
from rich.rule import Rule
from rich.table import Table

load_dotenv(Path(__file__).parent.parent / ".env")

MODEL = "claude-sonnet-5"
THINKING_BUDGET = 5_000   # Tokens die Claude zum Denken bekommt (min. 1024)
MAX_TOKENS_THINKING = 7_000  # muss > THINKING_BUDGET sein
MAX_TOKENS_STANDARD = 512

_USD_EUR = 0.92
_IN_PRICE_PER_M  = 2.00   # claude-sonnet-5 Input  $/1M
_OUT_PRICE_PER_M = 10.00  # claude-sonnet-5 Output $/1M


# ── Aufgaben-Definitionen ─────────────────────────────────────────────────────

TASKS = [
    {
        "name": "1 · Extraktion",
        "description": "Datum + Betrag aus Rechnungstext",
        "prompt": (
            "Extrahiere aus folgendem Rechnungstext (1) das Rechnungsdatum und "
            "(2) den Nettobetrag. Gib nur diese zwei Werte zurück, ohne weitere Erklärung.\n\n"
            "---\n"
            "Rechnung Nr. 2024-0923\n"
            "Ausgestellt: 15. März 2024\n"
            "Leistungszeitraum: 01.02.2024 – 29.02.2024\n\n"
            "Pos. 1: Beratungsleistung (20 h × 118,00 €) = 2.360,00 €\n"
            "Pos. 2: Reisekosten pauschal               =   487,50 €\n"
            "                       Nettobetrag         = 2.847,50 €\n"
            "                       USt. 19%            =   540,83 €\n"
            "                       Gesamtbetrag        = 3.388,33 €\n\n"
            "Zahlungsziel: 30. April 2024\n"
            "---"
        ),
        "check": lambda r: (
            ("15. März 2024" in r or "15.03.2024" in r)
            and "2.847,50" in r
        ),
        "expected": "15. März 2024 + 2.847,50 €",
    },
    {
        "name": "2 · Mehrstufige Logik",
        "description": "Rabattstaffel mit 3 Regeln + 2 Zusatzbedingungen",
        "prompt": (
            "Rabattstaffel der Bürobedarf GmbH:\n"
            "  Regel 1: Ab 10 Stück  → 5% Mengenrabatt\n"
            "  Regel 2: Ab 50 Stück  → 10% Mengenrabatt (ersetzt Regel 1)\n"
            "  Regel 3: Ab 100 Stück → 15% Mengenrabatt (ersetzt Regel 2)\n"
            "  Zusatz A: Stammkunden erhalten zusätzlich 3% auf den rabattierten Preis\n"
            "  Zusatz B: Bei erster Bestellung im Kalenderjahr gilt 2% Serviceaufschlag\n\n"
            "Fall: Frau Müller (Stammkundin seit 2019) bestellt 65 Einheiten. "
            "Es ist ihre dritte Bestellung in diesem Jahr. Listenpreis: 100,00 € pro Stück.\n\n"
            "Rechne Schritt für Schritt und nenne am Ende den Endpreis pro Stück."
        ),
        # Lösung: 65 Stk → Regel 2 → 10% → 90,00 €; Stammkunde +3% → 90,00 × 0,97 = 87,30 €
        # kein Serviceaufschlag (nicht erste Bestellung)
        "check": lambda r: "87,30" in r or "87.30" in r,
        "expected": "87,30 € pro Stück",
    },
    {
        "name": "3 · Planung",
        "description": "KI-Lösung auf Datenschutzkonformität prüfen",
        "prompt": (
            "Eine neue KI-Lösung soll in unserem Unternehmen eingesetzt werden. "
            "Welche konkreten Schritte brauche ich, um diese Lösung auf Datenschutzkonformität zu prüfen? "
            "Nenne die 5 wichtigsten Schritte als nummerierte Liste."
        ),
        # korrekt wenn ≥ 2 DSGVO-relevante Kernbegriffe erscheinen
        "check": lambda r: sum(
            kw in r.lower()
            for kw in [
                "dsgvo", "gdpr", "personenbezogen", "datenschutz",
                "auftragsverarbeit", "risikoanalyse", "dsfa", "tom",
                "verarbeitungsverzeichnis", "datenschutzbeauftragt",
            ]
        ) >= 2,
        "expected": "≥ 2 DSGVO-Kernbegriffe",
    },
]


# ── API-Aufruf ────────────────────────────────────────────────────────────────

@dataclass
class Result:
    task_name: str
    mode: str
    correct: bool
    cost_eur_cent: float  # in Cent für lesbare Tabelle
    latency_ms: int
    in_tok: int
    out_tok: int
    response_snippet: str


def _cost_eur(in_tok: int, out_tok: int) -> float:
    usd = (in_tok * _IN_PRICE_PER_M + out_tok * _OUT_PRICE_PER_M) / 1_000_000
    return round(usd * _USD_EUR * 100, 4)  # → Cent


def call_claude(prompt: str, use_thinking: bool) -> tuple[str, int, int, int]:
    """Gibt (text, in_tok, out_tok, latency_ms) zurück."""
    import anthropic

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    kwargs: dict = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
    }
    if use_thinking:
        kwargs["thinking"] = {"type": "enabled", "budget_tokens": THINKING_BUDGET}
        kwargs["max_tokens"] = MAX_TOKENS_THINKING
    else:
        kwargs["max_tokens"] = MAX_TOKENS_STANDARD

    t0 = time.monotonic()
    msg = client.messages.create(**kwargs)
    latency_ms = int((time.monotonic() - t0) * 1000)

    text = " ".join(b.text for b in msg.content if b.type == "text")
    return text, msg.usage.input_tokens, msg.usage.output_tokens, latency_ms


# ── Haupt-Logik ───────────────────────────────────────────────────────────────

def run_task(task: dict, use_thinking: bool, console: Console) -> Result:
    mode = "Extended Thinking" if use_thinking else "Standard"
    console.print(f"  [dim]→ {task['name']} [{mode}][/dim]", end=" ")
    try:
        text, in_tok, out_tok, latency_ms = call_claude(task["prompt"], use_thinking)
        correct = task["check"](text)
        snippet = text.replace("\n", " ")[:80]
        console.print("[green]✓[/green]" if correct else "[red]✗[/red]")
    except Exception as exc:
        console.print(f"[red]ERROR: {exc}[/red]")
        return Result(
            task_name=task["name"], mode=mode,
            correct=False, cost_eur_cent=0.0, latency_ms=0,
            in_tok=0, out_tok=0, response_snippet=f"ERROR: {exc}",
        )

    return Result(
        task_name=task["name"],
        mode=mode,
        correct=correct,
        cost_eur_cent=_cost_eur(in_tok, out_tok),
        latency_ms=latency_ms,
        in_tok=in_tok,
        out_tok=out_tok,
        response_snippet=snippet,
    )


def print_results(results: list[Result], console: Console) -> None:
    table = Table(
        title=f"Reasoning-Eval  |  Modell: {MODEL}  |  Thinking-Budget: {THINKING_BUDGET:,} Tokens",
        box=box.ROUNDED,
        header_style="bold cyan",
        show_lines=True,
    )
    table.add_column("Aufgabe",          style="bold",  no_wrap=True)
    table.add_column("Modus",            no_wrap=True)
    table.add_column("Korrekt",          justify="center")
    table.add_column("Kosten (¢)",       justify="right")
    table.add_column("Latenz (ms)",      justify="right")
    table.add_column("Tokens In/Out",    justify="right")
    table.add_column("Antwort (Auszug)", max_width=48)

    task_names = list(dict.fromkeys(r.task_name for r in results))

    for task_name in task_names:
        pair = [r for r in results if r.task_name == task_name]
        for r in pair:
            correct_icon = "[green]Ja ✓[/green]" if r.correct else "[red]Nein ✗[/red]"
            mode_style   = "[bold magenta]" if "Thinking" in r.mode else "[dim]"
            mode_end     = "[/bold magenta]" if "Thinking" in r.mode else "[/dim]"
            # Kostenvergleich innerhalb des Paares
            costs = [x.cost_eur_cent for x in pair if x.cost_eur_cent > 0]
            cost_color = "yellow" if (len(costs) == 2 and r.cost_eur_cent == max(costs)) else "white"
            table.add_row(
                r.task_name,
                f"{mode_style}{r.mode}{mode_end}",
                correct_icon,
                f"[{cost_color}]{r.cost_eur_cent:.4f}[/{cost_color}]",
                str(r.latency_ms),
                f"{r.in_tok} / {r.out_tok}",
                r.response_snippet,
            )

    console.print(table)

    # Interpretation
    console.print()
    console.print("[bold]Interpretation:[/bold]")
    for task_name in task_names:
        pair = [r for r in results if r.task_name == task_name]
        if len(pair) == 2:
            std  = next(r for r in pair if r.mode == "Standard")
            thk  = next(r for r in pair if r.mode == "Extended Thinking")
            extra_cost = thk.cost_eur_cent - std.cost_eur_cent
            if std.correct and thk.correct:
                verdict = f"[yellow]Thinking kostet +{extra_cost:.4f} ¢ extra, bringt keinen Vorteil[/yellow]"
            elif not std.correct and thk.correct:
                verdict = f"[green]Thinking macht den Unterschied (+{extra_cost:.4f} ¢ – lohnt sich)[/green]"
            elif std.correct and not thk.correct:
                verdict = "[red]Unerwartetes Ergebnis: Standard korrekt, Thinking nicht[/red]"
            else:
                verdict = "[red]Beide falsch – Prompt oder Erwartung prüfen[/red]"
            console.print(f"  {task_name}: {verdict}")


# ── Entry Point ───────────────────────────────────────────────────────────────

def main() -> None:
    console = Console()
    console.print(Rule("[bold blue]Reasoning-Eval – Extended Thinking vs. Standard"))
    console.print(
        f"[dim]Modell:[/dim] {MODEL}  |  "
        f"[dim]Thinking-Budget:[/dim] {THINKING_BUDGET:,} Tokens\n"
    )

    results: list[Result] = []
    for task in TASKS:
        console.print(f"\n[bold yellow]{task['name']}[/bold yellow]  [dim]{task['description']}[/dim]")
        console.print(f"  [dim]Erwartung: {task['expected']}[/dim]")
        for use_thinking in (False, True):
            result = run_task(task, use_thinking, console)
            results.append(result)
            if use_thinking:
                time.sleep(1)  # kurze Pause zwischen den Task-Paaren

    console.print()
    print_results(results, console)
    console.print("\n[dim]Calls geloggt in logs/calls.jsonl (nur Standard-Calls via llm_client)[/dim]")


if __name__ == "__main__":
    main()
