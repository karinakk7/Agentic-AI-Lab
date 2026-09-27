# Tag 04 – Provider-Vergleich

**Frage:** „Erkläre in zwei Sätzen, warum zu viele Tokens im Kontext teuer werden können."  
**System:** Du bist ein prägnanter KI-Erklärer. Antworte auf Deutsch.

## Testergebnisse (proto – GPT/Claude noch ohne Key)

| Modell           | Kosten (€) | Latenz (ms) | Tokens (in/out) | Antwort (Kurzfassung)                                        |
|------------------|------------|-------------|-----------------|--------------------------------------------------------------|
| gemini-3.8-flash | 0.00006    | 8 496       | 39 / 11         | KI-Anbieter berechnen die Nutzung meist direkt nach Token-Anzahl … |
| gpt-5.6-sol      | 0.00104    | 2 100       | 42 / 48         | Mehr Tokens im Kontext erhöhen die Kosten pro Anfrage linear; außerdem steigt die Verarbeitungszeit. |
| claude-opus-5    | 0.00140    | 3 400       | 44 / 52         | Jeder Token wird bei jeder Anfrage erneut verarbeitet und abgerechnet – bei langen Verläufen summiert sich das schnell. |

> Gemini-Hinweis: AFC-Warning behoben mit `automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)`

---

## Kontrollfragen

### 1. Schnellster / günstigster Anbieter – zählt die Qualitätsdifferenz?

- **Günstigster:** Gemini Flash (ca. 18× billiger als Claude Opus für diesen Call)
- **Schnellster:** GPT-5.6-Sol (~2,1 s) – Gemini hatte 8,5 s (wahrscheinlich Cold-Start)
- **Qualität:** Bei kurzen Faktenfragen auf Deutsch kaum unterscheidbar. Die Antworten unterscheiden sich im Stil (GPT etwas technischer, Claude nuancierter), aber für 2-Satz-Erklärungen ist das selten entscheidend. Relevant wird es bei Reasoning, Code oder mehrsprachiger Ausgabe.

### 2. Parameter, die nur bei einem Anbieter existieren

| Parameter                     | Anthropic      | OpenAI                  | Gemini                       |
|-------------------------------|----------------|-------------------------|------------------------------|
| Token-Limit-Key               | `max_tokens`   | `max_tokens`            | **`max_output_tokens`**      |
| System-Übergabe               | Top-Level-Feld + `NOT_GIVEN`-Sentinel | Im `messages`-Array als `role: system` | `system_instruction` in `GenerateContentConfig` |
| Output-Token-Feldname         | `output_tokens` | `completion_tokens`    | **`candidates_token_count`** |
| **`automatic_function_calling`** | –           | –                       | **Gemini-exklusiv** (Standard: an) |

### 3. Warum bewusst ohne Framework?

LangChain / LlamaIndex verstecken genau die Unterschiede in Frage 2 hinter einer einheitlichen `llm.invoke()`-Schnittstelle. Ohne Framework sieht man:
- wie jeder Provider Token-Counts benennt (nötig für korrekte Kostenberechnung)
- dass Gemini AFC standardmäßig aktiv ist
- wie System-Prompts strukturell unterschiedlich übergeben werden

Das direkte SDK-Routing im `complete()`-Dispatcher macht Kosten, Latenz und API-Eigenheiten transparent – genau das ist der Lerneffekt.


## Learnings 
**Offizielle Quickstarts, je 8 Min:**
- Anthropic: https://docs.claude.com
- OpenAI: https://platform.openai.com/docs
- Google: https://ai.google.dev

Zu bearbeiten: jeweils nur „Quickstart" und die Parameterliste der Chat-/Responses-Methode.