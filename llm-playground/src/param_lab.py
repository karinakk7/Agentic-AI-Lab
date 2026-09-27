"""Parameter-Labor: Wie wirken temperature und top_p auf kreative vs. deterministische Tasks?

Jede Konfiguration wird 5× mit derselben Frage aufgerufen.
Metriken: Anzahl identischer Antworten, durchschnittliche Zeichenlänge.

Laufzeit: ~4 Min (50 Calls × 4 s Pause, Free-Tier Gemini: 15 Req/Min).
"""
from __future__ import annotations

import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from rich import box
from rich.console import Console
from rich.rule import Rule
from rich.table import Table

from llm_client import complete

MODEL = "gemini-3.8-flash"
RUNS = 5
SYSTEM = "Antworte kurz und präzise auf Deutsch."

TASKS = {
    "kreativ": "Erzeuge einen Produktnamen für eine Software zur Vertragsanalyse.",
    "deterministisch": (
        "Extrahiere das Rechnungsdatum aus diesem Text und gib nur das Datum zurück: "
        "'Rechnung Nr. 2024-0815, ausgestellt am 15. März 2024, fällig bis 30. April 2024.'"
    ),
}

# temperature und top_p werden bewusst getrennt variiert (nie beide gleichzeitig setzen)
CONFIGS: list[dict] = [
    {"label": "temp=0.0", "temperature": 0.0},
    {"label": "temp=0.7", "temperature": 0.7},
    {"label": "temp=1.2", "temperature": 1.2},
    {"label": "top_p=0.1", "top_p": 0.1},
    {"label": "top_p=0.9", "top_p": 0.9},
]


def run_config(task: str, cfg: dict, console: Console) -> dict:
    label = cfg["label"]
    params = {k: v for k, v in cfg.items() if k != "label"}
    answers: list[str] = []

    console.print(f"  [dim]{label}[/dim]", end=" ")
    for i in range(RUNS):
        if i > 0:
            time.sleep(4)  # Free-Tier Gemini: ~15 Req/Min → mind. 4 s Abstand
        try:
            r = complete(task, model=MODEL, system=SYSTEM, max_tokens=64, **params)
            answers.append(r.text.strip())
            console.print("[green]·[/green]", end="")
        except Exception as exc:
            answers.append(f"ERROR: {exc}")
            console.print("[red]✗[/red]", end="")
    console.print()

    counts = Counter(answers)
    most_common_n = counts.most_common(1)[0][1]
    avg_len = sum(len(a) for a in answers) / len(answers)

    return {
        "label": label,
        "identical": most_common_n,
        "avg_len": round(avg_len, 1),
        "answers": answers,
    }


def print_table(results: list[dict], task_name: str, console: Console) -> None:
    table = Table(
        title=f"Task: {task_name}",
        box=box.ROUNDED,
        header_style="bold cyan",
        show_lines=True,
    )
    table.add_column("Konfiguration", style="bold", no_wrap=True)
    table.add_column(f"Identisch (von {RUNS})", justify="center")
    table.add_column("Ø Länge (Zeichen)", justify="right")
    table.add_column("Beispielantworten", max_width=60)

    for r in results:
        identical_style = "green" if r["identical"] == RUNS else ("yellow" if r["identical"] >= 3 else "red")
        sample = " / ".join(dict.fromkeys(r["answers"]))  # dedupliziert, Reihenfolge erhalten
        table.add_row(
            r["label"],
            f"[{identical_style}]{r['identical']}[/{identical_style}]",
            str(r["avg_len"]),
            sample[:200],
        )
    console.print(table)


def main() -> None:
    console = Console()
    console.print(Rule("[bold blue]Parameter-Labor – temperature & top_p"))
    console.print(f"[dim]Modell:[/dim] {MODEL}  |  [dim]Runs pro Config:[/dim] {RUNS}\n")

    for task_name, task_prompt in TASKS.items():
        console.print(f"[bold yellow]Task:[/bold yellow] {task_name.upper()}")
        console.print(f"[dim]{task_prompt}[/dim]\n")

        results = []
        for i, cfg in enumerate(CONFIGS):
            if i > 0:
                time.sleep(6)  # Extra-Pause zwischen Configs
            result = run_config(task_prompt, cfg, console)
            results.append(result)

        console.print()
        print_table(results, task_name, console)
        console.print()

    console.print("[dim]Calls geloggt in logs/calls.jsonl[/dim]")


if __name__ == "__main__":
    main()
