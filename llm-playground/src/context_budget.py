"""
context_budget.py – Kontextbudget-Analyse für LLM-Szenarien

Eingabe:  Modell, Systemprompt, Retrieval-Chunks, Tool-Definitionen, Historie
Ausgabe:  Tabelle mit Tokenanteil je Komponente, Restbudget, Kosten pro Call
"""

from dataclasses import dataclass, field
from typing import Optional
import tiktoken
from rich.console import Console
from rich.table import Table
from rich import box
from rich.panel import Panel

# ── Modell-Konfigurationen ────────────────────────────────────────────────────
# context_window: maximale Tokens insgesamt
# input / output: Preis in USD pro 1 Mio. Tokens
MODELS = {
    "gpt-5.6-sol":  {"context_window": 128_000, "input":  4.00, "output": 20.00},
    "gpt-6-astra":  {"context_window": 200_000, "input": 10.00, "output": 50.00},
    "deepseek-v4.1":{"context_window": 128_000, "input":  0.30, "output":  1.20},
}

EUR_PER_USD = 0.92

# ── Token-Zählung ─────────────────────────────────────────────────────────────

def _tokenizer():
    """o200k_base als universelle Näherung für alle neueren Modelle."""
    return tiktoken.get_encoding("o200k_base")


def count(text: str) -> int:
    return len(_tokenizer().encode(text))


# ── Datenklassen ──────────────────────────────────────────────────────────────

@dataclass
class ToolDefinition:
    name: str
    description: str
    parameters: str = ""   # JSON-Schema als String

    def token_count(self) -> int:
        return count(f"{self.name} {self.description} {self.parameters}")


@dataclass
class HistoryMessage:
    role: str   # "user" | "assistant"
    content: str

    def token_count(self) -> int:
        # ~4 Tokens Overhead pro Nachricht (role-Header)
        return count(self.content) + 4


@dataclass
class ContextBudgetInput:
    model: str
    system_prompt: str
    user_query: str
    retrieval_chunks: list[str] = field(default_factory=list)
    tool_definitions: list[ToolDefinition] = field(default_factory=list)
    conversation_history: list[HistoryMessage] = field(default_factory=list)
    reserved_output_tokens: int = 1_000


# ── Berechnungslogik ──────────────────────────────────────────────────────────

@dataclass
class ComponentBreakdown:
    name: str
    tokens: int
    percent: float
    description: str


@dataclass
class BudgetResult:
    model: str
    context_window: int
    total_input_tokens: int
    remaining_tokens: int
    cost_usd: float
    cost_eur: float
    components: list[ComponentBreakdown]
    over_budget: bool


def compute_budget(inp: ContextBudgetInput) -> BudgetResult:
    if inp.model not in MODELS:
        raise ValueError(f"Unbekanntes Modell '{inp.model}'. Verfügbar: {list(MODELS)}")

    cfg = MODELS[inp.model]
    context_window = cfg["context_window"]

    # Token-Zählung je Komponente
    t_system   = count(inp.system_prompt)
    t_query    = count(inp.user_query)
    t_chunks   = sum(count(c) for c in inp.retrieval_chunks)
    t_tools    = sum(td.token_count() for td in inp.tool_definitions)
    t_history  = sum(m.token_count() for m in inp.conversation_history)
    t_output   = inp.reserved_output_tokens

    total_input = t_system + t_query + t_chunks + t_tools + t_history
    total_used  = total_input + t_output
    remaining   = context_window - total_used

    # Kosten auf Basis Input + Output-Reserve
    p = cfg
    cost_usd = (total_input * p["input"] + t_output * p["output"]) / 1_000_000
    cost_eur = cost_usd * EUR_PER_USD

    def pct(t: int) -> float:
        return t / context_window * 100

    components = [
        ComponentBreakdown("System-Prompt",      t_system,  pct(t_system),  "Instruktionen & Persona"),
        ComponentBreakdown("User-Anfrage",        t_query,   pct(t_query),   "Aktuelle Nutzerfrage"),
        ComponentBreakdown("Retrieval-Chunks",    t_chunks,  pct(t_chunks),  f"{len(inp.retrieval_chunks)} Chunks"),
        ComponentBreakdown("Tool-Definitionen",   t_tools,   pct(t_tools),   f"{len(inp.tool_definitions)} Tools"),
        ComponentBreakdown("Konversationshistorie",t_history, pct(t_history), f"{len(inp.conversation_history)} Nachrichten"),
        ComponentBreakdown("Output-Reserve",      t_output,  pct(t_output),  "Reserviert für Antwort"),
    ]

    return BudgetResult(
        model=inp.model,
        context_window=context_window,
        total_input_tokens=total_input,
        remaining_tokens=remaining,
        cost_usd=cost_usd,
        cost_eur=cost_eur,
        components=components,
        over_budget=remaining < 0,
    )


# ── Ausgabe ───────────────────────────────────────────────────────────────────

BAR_WIDTH = 20

def _bar(percent: float) -> str:
    filled = round(percent / 100 * BAR_WIDTH)
    return "█" * filled + "░" * (BAR_WIDTH - filled)


def print_budget(result: BudgetResult, title: str) -> None:
    console = Console()

    status_color = "red" if result.over_budget else "green"
    status_text  = "ÜBER BUDGET!" if result.over_budget else "OK"

    # Anteil am Fenster für Footer; Balken zeigen Anteil am genutzten Input
    total_used_for_bar = result.total_input_tokens + result.components[-1].tokens  # inkl. Output-Reserve

    table = Table(
        title=f"[bold]{title}[/bold]  |  Modell: {result.model}  |  Fenster: {result.context_window:,} Tokens",
        box=box.ROUNDED,
        show_footer=True,
    )
    table.add_column("Komponente",        style="bold", footer="GESAMT (Input)")
    table.add_column("Tokens",            justify="right", footer=f"{result.total_input_tokens:,}")
    table.add_column("% Fenster",         justify="right", footer=f"{result.total_input_tokens/result.context_window*100:.1f}%")
    table.add_column("% genutzter Input", justify="right", footer="100%")
    table.add_column("Anteil (von genutztem Input)", footer="")
    table.add_column("Beschreibung",      style="dim", footer="")

    for c in result.components:
        share_of_used = c.tokens / total_used_for_bar * 100 if total_used_for_bar > 0 else 0
        color = "yellow" if c.tokens > 0 else "dim"
        table.add_row(
            c.name,
            f"[{color}]{c.tokens:,}[/{color}]",
            f"[{color}]{c.percent:5.2f}%[/{color}]",
            f"[{color}]{share_of_used:5.1f}%[/{color}]",
            f"[{color}]{_bar(share_of_used)}[/{color}]",
            c.description,
        )

    console.print(table)
    console.print(
        f"  Restbudget: [{status_color}]{result.remaining_tokens:,} Tokens ({result.remaining_tokens / result.context_window * 100:.1f}%) — {status_text}[/{status_color}]"
        f"  |  Kosten/Call: [cyan]${result.cost_usd:.5f}[/cyan] (€{result.cost_eur:.5f})\n"
    )


# ── Szenarien ─────────────────────────────────────────────────────────────────

SYSTEM_PROMPT_CHATBOT = """\
Du bist ein hilfreicher Assistent. Beantworte Fragen klar und präzise auf Deutsch.
Halte deine Antworten knapp, es sei denn, der Nutzer bittet um Details.
"""

SYSTEM_PROMPT_RAG = """\
Du bist ein Wissensassistent. Dir werden Dokument-Auszüge bereitgestellt.
Beantworte ausschließlich auf Basis der gegebenen Informationen.
Zitiere relevante Stellen und weise auf fehlende Informationen hin.
Antworte immer auf Deutsch und strukturiere deine Antworten mit Absätzen.
"""

SYSTEM_PROMPT_AGENT = """\
Du bist ein autonomer Recherche-Agent. Du hast Zugriff auf mehrere Tools.
Arbeite schrittweise: Plane zunächst, dann führe aus, dann fasse zusammen.
Nutze Tools sparsam und zielgerichtet. Dokumentiere jeden Schritt kurz.
Bei Unsicherheit frage nach, bevor du weitermachst.
Antworte immer auf Deutsch. Formatiere Ergebnisse als strukturierten Report.
"""

USER_QUERY = "Kannst du mir eine Zusammenfassung der wichtigsten Punkte geben?"

def _make_rag_chunks(n: int, avg_tokens: int) -> list[str]:
    """Erzeugt n Platzhalter-Chunks mit je ~avg_tokens Tokens."""
    word = "Informationsinhalt "   # ~3 Tokens
    words_per_chunk = avg_tokens // 3
    chunk = word * words_per_chunk
    return [f"[Chunk {i+1}] {chunk}" for i in range(n)]


def _make_tool_definitions(n: int) -> list[ToolDefinition]:
    """Erzeugt n realistische Tool-Definitionen mit typischer Größe."""
    base_tools = [
        ToolDefinition(
            name="web_search",
            description="Führt eine Web-Suche durch und gibt die Top-Ergebnisse zurück.",
            parameters='{"query": {"type": "string", "description": "Suchanfrage"}, "max_results": {"type": "integer", "default": 5}}',
        ),
        ToolDefinition(
            name="read_document",
            description="Liest den Inhalt eines Dokuments aus dem Wissensspeicher.",
            parameters='{"document_id": {"type": "string"}, "start_page": {"type": "integer", "default": 1}, "end_page": {"type": "integer"}}',
        ),
        ToolDefinition(
            name="run_code",
            description="Führt Python-Code in einer isolierten Sandbox aus und gibt stdout zurück.",
            parameters='{"code": {"type": "string"}, "timeout_seconds": {"type": "integer", "default": 30}}',
        ),
        ToolDefinition(
            name="write_file",
            description="Schreibt Inhalt in eine Datei im Arbeitsverzeichnis des Agenten.",
            parameters='{"filename": {"type": "string"}, "content": {"type": "string"}, "mode": {"type": "string", "enum": ["write", "append"]}}',
        ),
        ToolDefinition(
            name="database_query",
            description="Führt eine SQL-Abfrage gegen die interne Datenbank aus.",
            parameters='{"sql": {"type": "string"}, "database": {"type": "string", "enum": ["prod", "staging"]}, "limit": {"type": "integer", "default": 100}}',
        ),
        ToolDefinition(
            name="send_email",
            description="Sendet eine E-Mail über den konfigurierten SMTP-Server.",
            parameters='{"to": {"type": "array", "items": {"type": "string"}}, "subject": {"type": "string"}, "body": {"type": "string"}, "cc": {"type": "array"}}',
        ),
        ToolDefinition(
            name="calendar_lookup",
            description="Sucht Termine im Unternehmenskalender für einen bestimmten Zeitraum.",
            parameters='{"start_date": {"type": "string"}, "end_date": {"type": "string"}, "user_id": {"type": "string"}}',
        ),
        ToolDefinition(
            name="fetch_api",
            description="Ruft eine externe REST-API ab und gibt die JSON-Antwort zurück.",
            parameters='{"url": {"type": "string"}, "method": {"type": "string", "enum": ["GET", "POST"]}, "headers": {"type": "object"}, "body": {"type": "object"}}',
        ),
        ToolDefinition(
            name="summarize_text",
            description="Erstellt eine kompakte Zusammenfassung eines langen Textes.",
            parameters='{"text": {"type": "string"}, "max_sentences": {"type": "integer", "default": 5}, "language": {"type": "string", "default": "de"}}',
        ),
        ToolDefinition(
            name="translate",
            description="Übersetzt einen Text in die angegebene Zielsprache.",
            parameters='{"text": {"type": "string"}, "target_language": {"type": "string"}, "source_language": {"type": "string", "default": "auto"}}',
        ),
        ToolDefinition(
            name="vector_search",
            description="Durchsucht den Vektorspeicher nach semantisch ähnlichen Dokumenten.",
            parameters='{"query": {"type": "string"}, "collection": {"type": "string"}, "top_k": {"type": "integer", "default": 10}, "threshold": {"type": "number"}}',
        ),
        ToolDefinition(
            name="create_report",
            description="Generiert einen formatierten PDF-Report aus strukturierten Daten.",
            parameters='{"title": {"type": "string"}, "sections": {"type": "array"}, "template": {"type": "string", "enum": ["standard", "executive", "technical"]}}',
        ),
    ]
    return base_tools[:n]


def _make_history(n_steps: int) -> list[HistoryMessage]:
    """Erzeugt n_steps Schritte (je 1 User + 1 Assistant = 2 Nachrichten)."""
    history = []
    for i in range(n_steps):
        history.append(HistoryMessage(
            role="user",
            content=f"Schritt {i+1}: Bitte analysiere den folgenden Aspekt und gib eine strukturierte Einschätzung.",
        ))
        history.append(HistoryMessage(
            role="assistant",
            content=(
                f"Ich habe Schritt {i+1} abgeschlossen. Hier sind meine Ergebnisse: "
                f"Die Analyse zeigt, dass mehrere Faktoren zu berücksichtigen sind. "
                f"Erstens wurden die Kerndaten ausgewertet. Zweitens wurden Querverbindungen identifiziert. "
                f"Drittens empfehle ich folgende nächste Maßnahmen basierend auf den Erkenntnissen."
            ),
        ))
    return history


def run_scenarios() -> None:
    console = Console()

    console.print(Panel.fit(
        "[bold cyan]Kontextbudget-Analyse[/bold cyan]\n"
        "Drei Szenarien zeigen, wie Token-Budget verteilt wird",
        border_style="cyan",
    ))

    # ── Szenario 1: Einfacher Chatbot ─────────────────────────────────────────
    scenario_1 = ContextBudgetInput(
        model="gpt-5.6-sol",
        system_prompt=SYSTEM_PROMPT_CHATBOT,
        user_query=USER_QUERY,
        retrieval_chunks=[],
        tool_definitions=[],
        conversation_history=[],
        reserved_output_tokens=500,
    )
    result_1 = compute_budget(scenario_1)
    print_budget(result_1, "Szenario 1 – Einfacher Chatbot (kein Retrieval)")

    # ── Szenario 2: RAG-Assistent ─────────────────────────────────────────────
    scenario_2 = ContextBudgetInput(
        model="gpt-5.6-sol",
        system_prompt=SYSTEM_PROMPT_RAG,
        user_query=USER_QUERY,
        retrieval_chunks=_make_rag_chunks(n=8, avg_tokens=500),
        tool_definitions=[],
        conversation_history=[],
        reserved_output_tokens=800,
    )
    result_2 = compute_budget(scenario_2)
    print_budget(result_2, "Szenario 2 – RAG-Assistent (8 Chunks × 500 Tokens)")

    # ── Szenario 3: Agent ─────────────────────────────────────────────────────
    scenario_3 = ContextBudgetInput(
        model="gpt-5.6-sol",
        system_prompt=SYSTEM_PROMPT_AGENT,
        user_query=USER_QUERY,
        retrieval_chunks=[],
        tool_definitions=_make_tool_definitions(n=12),
        conversation_history=_make_history(n_steps=20),
        reserved_output_tokens=1_500,
    )
    result_3 = compute_budget(scenario_3)
    print_budget(result_3, "Szenario 3 – Agent (12 Tools, 20 Schritte Historie)")

    # ── Vergleichszusammenfassung ──────────────────────────────────────────────
    summary = Table(title="Vergleich: Dominante Komponente je Szenario", box=box.SIMPLE_HEAD)
    summary.add_column("Szenario",         style="bold")
    summary.add_column("Größte Komponente",style="yellow")
    summary.add_column("deren Tokens",     justify="right")
    summary.add_column("Anteil am Fenster",justify="right")
    summary.add_column("Nutzeranfrage",    justify="right", style="dim")
    summary.add_column("Kosten/Call",      justify="right", style="cyan")

    for label, result in [
        ("1 – Chatbot",    result_1),
        ("2 – RAG",        result_2),
        ("3 – Agent",      result_3),
    ]:
        biggest = max(result.components, key=lambda c: c.tokens)
        user_comp = next(c for c in result.components if c.name == "User-Anfrage")
        summary.add_row(
            label,
            biggest.name,
            f"{biggest.tokens:,}",
            f"{biggest.percent:.1f}%",
            f"{user_comp.tokens} Tok ({user_comp.percent:.1f}%)",
            f"${result.cost_usd:.5f}",
        )

    console.print(summary)
    console.print(
        "\n[bold]Kernaussage:[/bold] Im Agenten-Szenario dominieren "
        "[yellow]Tool-Definitionen[/yellow] und [yellow]Konversationshistorie[/yellow] "
        "das Budget – [dim]nicht[/dim] die eigentliche Nutzeranfrage.\n"
    )


if __name__ == "__main__":
    run_scenarios()
