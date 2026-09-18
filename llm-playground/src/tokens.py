# Anforderungen:
# 1. Funktion count_tokens(text, model) -> int
# 2. Funktion estimate_cost(input_tokens, output_tokens, model) -> float
#    (Preise aus notes/models.md in ein dict PRICING übernehmen)
# 3. Vergleichsfunktion: gleicher Inhalt auf Deutsch und Englisch

import tiktoken
from rich.console import Console
from rich.table import Table

# Preise aus notes/models.md – USD pro 1 Million Tokens
PRICING = {
    "gpt-5.6-sol":        {"input":  4.00, "output": 20.00},
    "gpt-6-astra":        {"input": 10.00, "output": 50.00},
    "gemini-3.8-flash":   {"input":  0.75, "output":  3.75},
    "mistral-medium-3.5": {"input":  1.50, "output":  7.50},
    "deepseek-v4.1":      {"input":  0.30, "output":  1.20},
    "qwen3.8":            {"input":  0.50, "output":  3.00},
}

EUR_PER_USD = 0.92


def count_tokens(text: str, model: str) -> int:
    """Zählt Tokens lokal mit tiktoken (kein API-Call)."""
    try:
        enc = tiktoken.encoding_for_model(model)
    except KeyError:
        # Neuere Modellnamen noch nicht in tiktoken – o200k_base als Näherung
        enc = tiktoken.get_encoding("o200k_base")
    return len(enc.encode(text))


def estimate_cost(input_tokens: int, output_tokens: int, model: str) -> dict:
    """Gibt {"usd": float, "eur": float} zurück."""
    if model not in PRICING:
        raise ValueError(f"'{model}' nicht in PRICING. Verfügbar: {list(PRICING)}")
    p = PRICING[model]
    usd = (input_tokens * p["input"] + output_tokens * p["output"]) / 1_000_000
    return {"usd": usd, "eur": usd * EUR_PER_USD}


def compare_languages(text_de: str, text_en: str, model: str) -> None:
    """Druckt Token-Vergleich DE vs. EN mit Kosten."""
    console = Console()

    tokens_de = count_tokens(text_de, model)
    tokens_en = count_tokens(text_en, model)
    aufschlag = (tokens_de - tokens_en) / tokens_en * 100

    cost_de = estimate_cost(tokens_de, 0, model)
    cost_en = estimate_cost(tokens_en, 0, model)

    console.print(
        f"\n[bold]Modell:[/bold] {model}\n"
        f"DE: {tokens_de} Tokens | EN: {tokens_en} Tokens | "
        f"Aufschlag: [yellow]{aufschlag:+.1f}%[/yellow]\n"
        f"Kosten DE: ${cost_de['usd']:.5f} (€{cost_de['eur']:.5f}) | "
        f"Kosten EN: ${cost_en['usd']:.5f} (€{cost_en['eur']:.5f})"
    )

    table = Table(title=f"Token-Vergleich – {model}")
    table.add_column("", style="bold")
    table.add_column("Tokens", justify="right")
    table.add_column("Input USD", justify="right")
    table.add_column("Input EUR", justify="right")

    table.add_row("Deutsch",  str(tokens_de), f"${cost_de['usd']:.5f}", f"€{cost_de['eur']:.5f}")
    table.add_row("Englisch", str(tokens_en), f"${cost_en['usd']:.5f}", f"€{cost_en['eur']:.5f}")
    table.add_row(
        "Aufschlag", f"{aufschlag:+.1f}%",
        f"{(cost_de['usd'] - cost_en['usd']) / cost_en['usd'] * 100:+.1f}%", "",
        style="yellow",
    )
    console.print(table)


# Testtext – ersetze durch eigenen Absatz aus deiner Arbeit (anonymisiert)
TEXT_DE = """
Die Risikoklassifizierung von Kreditanträgen erfolgt anhand eines mehrstufigen
Bewertungsverfahrens. Dabei werden bonitätsrelevante Merkmale wie Einkommenssituation,
Beschäftigungsverhältnis und bisherige Zahlungshistorie systematisch erfasst und
gewichtet. Das Ergebnis fließt in die interne Ratingnote ein, die als Grundlage
für die Kreditentscheidung und die Konditionengestaltung dient.
"""

TEXT_EN = """
The risk classification of loan applications is carried out using a multi-stage
assessment process. Creditworthiness-relevant characteristics such as income situation,
employment status, and previous payment history are systematically recorded and weighted.
The result feeds into the internal rating score, which serves as the basis for
the credit decision and the structuring of terms and conditions.
"""


if __name__ == "__main__":
    compare_languages(TEXT_DE, TEXT_EN, model="gpt-5.6-sol")
