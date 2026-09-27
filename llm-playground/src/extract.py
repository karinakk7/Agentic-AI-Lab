"""
Strukturierte Extraktion von Lieferantenrisiken aus Vertragsauszügen.

Workflow:
  1. JSON-Schema aus Pydantic-Modell -> Anthropic Tool Definition
  2. API-Aufruf mit erzwungenem Tool-Use -> garantiertes JSON
  3. Pydantic-Validierung; bei Fehler: einmaliger Repair-Loop
  4. Batch-Test gegen 8 Vertragsauszuege + Auswertung
"""
from __future__ import annotations

import os
from datetime import date
from typing import Literal

import anthropic
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError

load_dotenv()

MODEL = "claude-sonnet-5"


class Lieferantenrisiko(BaseModel):
    lieferant: str
    vertragsbeginn: date | None
    vertragswert_eur: float | None
    risikostufe: Literal["niedrig", "mittel", "hoch"]
    begruendung: str = Field(max_length=300)
    zitate: list[str] = Field(description="Woertliche Belegstellen aus dem Text")


# ── 8 Vertragsauszuege ───────────────────────────────────────────────────────

VERTRAGSAUSZUEGE = [
    {
        "id": 1,
        "label": "Niedrig: Etablierter Langzeitlieferant",
        "text": """
Lieferantenrahmenvertrag Nr. LV-2023-0012
Lieferant: Metallbau Schroeder GmbH & Co. KG
Vertragsbeginn: 01.03.2023
Vertragswert: 240.000 EUR/Jahr

Der Lieferant beliefert uns seit ueber 12 Jahren zuverlaessig mit Stahlprofilen.
Reklamationsquote liegt unter 0,3 %. Keine Lieferverzoegerungen in den letzten 24 Monaten.
Bonitaet geprueft (Creditreform Score 178 - sehr gut). Zweiter zugelassener Lieferant fuer
dieselben Artikel vorhanden (Stahl Express AG).
""",
    },
    {
        "id": 2,
        "label": "Hoch: Sole-Supplier, Insolvenzrisiko",
        "text": """
Einzelbezugsvertrag Nr. EB-2024-0044
Lieferant: Praezisionsteile Vogel GmbH
Vertragsbeginn: 15.06.2024
Vertragswert: 1.850.000 EUR

Ausschliesslicher Lieferant fuer Steuerungsplatinen Typ CP-77. Kein alternatives
Bezugsprodukt am Markt verfuegbar (Eigenentwicklung Vogel GmbH). Creditreform-Auskunft
vom 02.09.2024: Score 312 - erhoehtes Ausfallrisiko. Laufende Insolvenzpruefung durch
Glaeubigerbank bestaetigt. Lieferzeiten zuletzt von 6 auf 14 Wochen gestiegen.
""",
    },
    {
        "id": 3,
        "label": "Mittel: Geopolitisches Beschaffungsrisiko",
        "text": """
Importvertrag Nr. IV-2024-0091
Lieferant: Eastern Components Ltd. (Taiwan)
Vertragsbeginn: 01.01.2024
Vertragswert: 620.000 EUR

Lieferant produziert ausschliesslich in Hsinchu, Taiwan. 70 % der bezogenen
Halbleiterbauelemente kommen von diesem Standort. Geopolitische Spannungen in der
Strasse von Taiwan haben sich laut Auswaertigem Amt seit Q1/2024 verschaerft.
Alternativer EU-Lieferant in Qualifizierung, Abschluss fruehestens Q2/2025.
""",
    },
    {
        "id": 4,
        "label": "Hoch: Compliance-Verstoss",
        "text": """
Rahmenliefervertrag Nr. RL-2023-0077
Lieferant: ChemSupply Osteuropa s.r.o.
Vertragsbeginn: 15.04.2023
Vertragswert: 430.000 EUR

Audit vom 18.07.2024: Schwerwiegende Abweichungen bei Arbeitssicherheitsvorschriften
(3 kritische Findings). Keine ISO-14001-Rezertifizierung seit Januar 2024 (Zertifikat
abgelaufen). Lieferant wurde mit Maengelanzeige MA-2024-031 belegt; Nachbesserungsfrist
bis 31.10.2024. Bei Nichteinhaltung greift Sonderkuendigungsrecht gem. § 12 Abs. 3 des
Vertrages.
""",
    },
    {
        "id": 5,
        "label": "Niedrig: Standardware, viele Alternativen",
        "text": """
Abrufvertrag Nr. AV-2024-0003
Lieferant: Bueromaterial Zentral AG
Vertragswert: 18.500 EUR/Jahr

Vertrag fuer Standardverbrauchsmaterial (Papier, Druckertoner, Kleinteile).
Produkte sind bei mindestens 8 weiteren Lieferanten sofort verfuegbar. Wechselkosten
minimal. Laufzeit: 12 Monate, monatlich kuendbar. Keine Kritikalitaet fuer Produktion.
Kein Vertragsbeginn im Dokument angegeben.
""",
    },
    {
        "id": 6,
        "label": "Mittel: Konzentration bei einem Logistikdienstleister",
        "text": """
Logistikrahmenvertrag Nr. LG-2022-0009
Lieferant: Schnelltransport Mayer GmbH
Vertragsbeginn: 01.07.2022
Vertragswert: 890.000 EUR/Jahr

80 % aller eingehenden Expresslieferungen werden ueber Mayer GmbH abgewickelt.
Puenktlichkeitsquote: 94 % (Zielwert: 97 %). Letzte Eskalation: Ausfall eines
zentralen Hubs in Frankfurt (September 2023, Dauer: 4 Tage). Ausweichlieferant
DHL Freight ist vertraglich gebunden, jedoch kapazitaetsmaessig nur fuer ca. 40 %
des Volumens geeignet.
""",
    },
    {
        "id": 7,
        "label": "Hoch: Vertragsende ohne Anschlussregelung",
        "text": """
Wartungsvertrag Nr. WV-2019-0033
Lieferant: Industrieservice Braun AG
Vertragsbeginn: 01.01.2020
Vertragswert: 560.000 EUR/Jahr

Vertrag laeuft zum 31.12.2024 aus. Bisherige Verhandlungen fuer Folgevertrag ohne
Ergebnis (Stand: Oktober 2024). Braun AG haelt exklusives Know-how fuer Wartung der
Pruefanlage PA-3000; keine alternative Servicefirma zugelassen. Ausfall der Pruefanlage
wuerde Produktion an Standort 2 fuer ca. 3 Wochen stilllegen.
Verhandlungsposition des Lieferanten stark.
""",
    },
    {
        "id": 8,
        "label": "Mittel: Qualitaetsprobleme, aktiver Verbesserungsprozess",
        "text": """
Liefervertrag Nr. LV-2024-0055
Lieferant: Kunststoffwerk Bergmann GmbH
Vertragsbeginn: 01.02.2024
Vertragswert: 310.000 EUR

Reklamationsquote im ersten Halbjahr 2024: 4,2 % (Zielwert < 1 %). Ursache:
Anlaufschwierigkeiten nach Werksverlagerung im Januar 2024. Lieferant hat
CAPA-Massnahmen eingeleitet (Corrective Action Report CA-2024-07); erste
Verbesserungen sichtbar (Q2: 5,8 % -> Q3: 4,2 %). Eskalationsgespraech mit
Geschaeftsfuehrung am 14.09.2024. Monatliches Monitoring vereinbart.
""",
    },
]

# ── Extraktion ────────────────────────────────────────────────────────────────

SYSTEM = (
    "Du bist ein Risikomanagement-Assistent. Extrahiere die strukturierten Risikodaten "
    "aus dem Vertragsauszug. Nutze ausschliesslich das bereitgestellte Tool. "
    "Fuer `zitate` kopiere woertliche Textstellen, die deine Risikoeinstufung belegen."
)


def _build_tool() -> dict:
    """Wandelt das Pydantic-Schema in eine Anthropic-Tool-Definition um."""
    return {
        "name": "extract_lieferantenrisiko",
        "description": "Extrahiert strukturierte Risikodaten aus einem Lieferantenvertragsauszug.",
        "input_schema": Lieferantenrisiko.model_json_schema(),
    }


def extract(text: str, client: anthropic.Anthropic) -> Lieferantenrisiko:
    """Extrahiert Lieferantenrisiko aus Text. Max. 1 Repair-Versuch bei Validierungsfehler."""
    tool = _build_tool()
    messages: list[dict] = [{"role": "user", "content": text}]

    def _call(msgs: list[dict]) -> tuple[str, dict]:
        resp = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM,
            tools=[tool],
            tool_choice={"type": "tool", "name": "extract_lieferantenrisiko"},
            messages=msgs,
        )
        tu = next(b for b in resp.content if b.type == "tool_use")
        return tu.id, tu.input

    tool_id, raw = _call(messages)

    try:
        return Lieferantenrisiko.model_validate(raw)
    except ValidationError as err:
        # Repair-Loop: Pydantic-Fehlertext zurueckschicken, einmal neu versuchen
        repair_msgs = messages + [
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "tool_use",
                        "id": tool_id,
                        "name": "extract_lieferantenrisiko",
                        "input": raw,
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_id,
                        "content": f"Validierungsfehler: {err}. Bitte korrigiere die Ausgabe.",
                    }
                ],
            },
        ]
        _, raw2 = _call(repair_msgs)
        return Lieferantenrisiko.model_validate(raw2)


# ── Runner ────────────────────────────────────────────────────────────────────

def main() -> None:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    results: list[dict] = []
    valid = 0

    for v in VERTRAGSAUSZUEGE:
        print(f"\n[{v['id']}/8] {v['label']}")
        try:
            risiko = extract(v["text"], client)
            valid += 1
            results.append({"id": v["id"], "status": "OK", "risiko": risiko})
            print(f"  OK  Lieferant:   {risiko.lieferant}")
            print(f"  OK  Risikostufe: {risiko.risikostufe}")
            print(f"  OK  Begruendung: {risiko.begruendung[:80]}...")
            if risiko.zitate:
                print(f"  OK  Zitate ({len(risiko.zitate)}): {risiko.zitate[0][:70]!r}")
            else:
                print("  !!  Keine Zitate geliefert")
        except Exception as exc:
            results.append({"id": v["id"], "status": "FEHLER", "error": str(exc)})
            print(f"  FEHLER: {exc}")

    print(f"\n{'='*60}")
    print(f"Ergebnis: {valid}/8 schema-valide Ausgaben")
    print(f"{'='*60}")

    print("\nHalluzinations-Check (manuell pruefen):")
    print("Steht jedes Zitat woertlich im Vertragsauszug?\n")
    for r in results:
        if r["status"] == "OK":
            risiko: Lieferantenrisiko = r["risiko"]
            print(f"[{r['id']}] {risiko.lieferant} ({risiko.risikostufe}):")
            for z in risiko.zitate:
                print(f"    - {z!r}")


if __name__ == "__main__":
    main()
