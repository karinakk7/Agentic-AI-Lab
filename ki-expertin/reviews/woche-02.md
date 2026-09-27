# Structured Outputs mit Schema-Garantie (Build-Session)


## OpenAI – Structured Model Outputs

* **JSON** is a common format for exchanging data between applications.
* **Structured Outputs** is an OpenAI feature that ensures the model's response follows a **predefined JSON schema**.
* This makes the output more reliable and easier for applications to process.

### Benefits

* **Reliable type safety:** The returned data follows the expected types and structure.
* **Explicit refusals:** The model can clearly indicate when it cannot fulfill a request.
* **Similar prompting:** The same general prompting techniques can still be used together with Structured Outputs.

### Defining a Schema

You can define object schemas using tools such as:

* `pydantic.BaseModel`
* JSON Schema objects

Structured Outputs can be used in two main ways:

* **Function calling:** Useful when the model needs to interact with functions, tools, or other application functionality.
* **`response_format` / `text.format`:** Useful when the model should return a structured response directly to the application or user.

### Structured Outputs vs. JSON Mode

Both **JSON Mode** and **Structured Outputs** can ensure that the model returns valid JSON.

The important difference is:

> **JSON Mode ensures valid JSON, while Structured Outputs also ensures that the JSON follows the defined schema.**

Therefore, Structured Outputs should generally be preferred over JSON Mode when schema adherence is important.

### How to Use Structured Outputs with `text.format`

1. **Define the schema**
2. **Provide the schema in the API request**
3. **Handle edge cases**, such as refusals or unexpected situations

### Refusals with Structured Outputs

OpenAI may refuse to fulfill a request because of safety reasons.

A refusal does not necessarily follow the schema that you provided. Your application therefore needs to be prepared for this case.

For user-generated input, you should define in the prompt what should happen when the input cannot produce a valid result.

For example, you can instruct the model to return **empty parameters or fields** in certain cases.

If the model produces incorrect results:

* Improve the instructions
* Add relevant examples
* Break complex tasks into smaller subtasks

Also avoid **schema divergence**, meaning that the schema used by your application and the schema expected by the model should stay consistent. Using the native SDK helpers can help prevent these inconsistencies.

### Streaming

**Streaming** means processing the model's response or function-call arguments **while they are being generated**, instead of waiting for the complete response.

This is useful when you want to:

* Display structured data step by step
* Process function-call arguments as soon as they are available
* Reduce perceived waiting time for the user

OpenAI recommends using the **SDKs** to handle streaming with Structured Outputs.

### Supported Schemas

Structured Outputs supports a **subset of the JSON Schema specification**.

Common supported types include:

* `string`
* `number`
* `integer`
* `boolean`
* `object`
* `array`
* `enum`
* `anyOf`

**Key idea:** Structured Outputs gives you **schema-conformant JSON**, making model responses much easier and safer for applications to process.
### JSON Mode

JSON Mode is a more basic version of Structured Outputs. It ensures that the model returns **valid JSON**, but it does **not** guarantee that the response follows a specific JSON schema.

**Example:**
The model will return valid JSON, but fields, values, or the exact structure may still differ from what your application expects.
## Anthropic – Strict Tool Use

Strict Tool Use ensures that Claude's **tool inputs comply with a defined JSON Schema**.

By setting `strict: true`, Anthropic uses **grammar-constrained sampling** to restrict the model's output to values that are valid according to the schema.

Strict Tool Use is useful when you need to:

* Validate tool parameters
* Build reliable **agentic workflows**
* Ensure **type-safe function calls**
* Handle complex tools with nested properties

### Why Strict Tool Use Matters for Agents

Without strict mode, Claude may:

* Return values with incompatible types
* Omit required fields
* Produce tool inputs that do not match the expected structure

This can cause **runtime errors** and break downstream functions.

With Strict Tool Use:

* Functions receive correctly typed arguments consistently.
* Tool calls do not need to be repeatedly validated and repaired.
* Agents become more reliable and easier to operate at scale.

### How It Works

1. **Define your tool schema**
   Create a JSON Schema for the tool's `input_schema`.

2. **Enable strict mode**
   Add `strict: true` as a top-level property of the tool definition.

3. **Handle the tool call**
   The `input` field in the resulting `tool_use` block must follow the defined `input_schema`.

Example:

```json
{
  "name": "get_weather",
  "description": "Get the current weather for a location.",
  "strict": true,
  "input_schema": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string"
      }
    },
    "required": ["location"],
    "additionalProperties": false
  }
}
```

**Key idea:** `strict: true` makes tool calls **schema-conformant by construction**, reducing parsing errors and the need for validation and retry logic.

### Data Retention

* Strict Tool Use compiles the tool `input_schema` into a grammar.
* The compiled tool schema is **temporarily cached for up to 24 hours since its last use**.
* **Prompts and responses are not retained beyond the API response.**
* Strict Tool Use is **HIPAA eligible**, but **PHI must not be included in tool schema definitions**.
* The schema cache is stored separately from message content and does not have the same PHI protections as prompts and responses.
* Therefore, PHI should not appear in:

  * property names
  * `enum` values
  * `const` values
  * `pattern` regular expressions

**Key idea:** Keep sensitive health information in the **prompt/response content**, not in the **tool schema**, because the schema is temporarily cached.


## Praxis
Schema → API: _build_tool() calls Lieferantenrisiko.model_json_schema() and wraps it as an Anthropic tool definition. Using tool_choice={"type": "tool", "name": "..."} forces the model to always fill the schema — no prose, no markdown fences, just JSON.

Repair-Loop (extract()): After the first call, model_validate(raw) checks the result. On ValidationError, the full Pydantic error message is sent back as a tool_result and the model gets one more chance. The conversation history carries enough context that the model can fix the specific field(s) that failed.

8 Vertragsauszüge cover the full risk spectrum:

#	Lieferant	Erwartete Stufe
1	Metallbau Schröder	niedrig
2	Präzisionsteile Vogel	hoch (Insolvenz)
3	Eastern Components	mittel (Geopolitik)
4	ChemSupply Osteuropa	hoch (Compliance)
5	Büromaterial Zentral	niedrig, kein Vertragsbeginn → null
6	Schnelltransport Mayer	mittel (Konzentration)
7	Industrieservice Braun	hoch (Vertragsende)
8	Kunststoffwerk Bergmann	mittel (Qualität)
Fall #5 testet bewusst vertragsbeginn: null — prüft, ob das Modell None korrekt ausgibt statt zu halluzinieren.

Halluzinations-Auswertung: Die letzten Zeilen der Ausgabe listen alle zitate pro Lieferant auf — den Abgleich mit dem Quelltext machst du manuell. Das ist deine erste echte Halluzinationsmessung.

## Reflexion

### 1. Wie viele Ausgaben waren schema-valide, aber inhaltlich falsch? Was sagt das über Structured Outputs als Qualitätsmaßnahme?

**Schema-Validität löst das Parsing-Problem, nicht das Halluzinationsproblem.**

Ein Modell kann jedes definierte Feld mit einem **erfundenen, aber formal korrekt strukturierten Inhalt** füllen. Structured Outputs stellt daher sicher, dass die Antwort dem vorgegebenen Schema entspricht, garantiert aber nicht deren inhaltliche Richtigkeit.

Die **Zitate-Pflicht** ist deshalb besonders wichtig: Sie macht mögliche Halluzinationen sichtbar, da die Aussagen direkt mit dem zugrunde liegenden Quelltext überprüft werden können.

### 2. Warum sind `Literal`-Typen für Kategorien besser als freier Text mit der Anweisung „Wähle eines von drei“?

`Literal` wirkt auf zwei Ebenen:

1. Im Schema wird daraus ein **`enum`**, wodurch nur die vorgegebenen Werte zulässig sind.
2. **Pydantic** validiert die Antwort nach dem API-Aufruf und lehnt Abweichungen strikt ab.

Bei freiem Text könnten dagegen beispielsweise `"Mittel"`, `"mittel-hoch"` oder `"medium"` zurückgegeben werden. Semantisch können sie dasselbe bedeuten, für nachgelagerten Code sind sie jedoch unterschiedliche Werte und können zu Fehlern führen.

### 3. Wann ist ein Repair-Loop teurer als ein besserer Prompt?

Ein Repair-Loop kann teurer werden, wenn **Fehler regelmäßig auftreten** oder immer wieder auf dieselbe Ursache zurückzuführen sind.

Als Faustregel kann eine **Fehlerrate von etwa 10 %** ein Hinweis sein, dass der Prompt verbessert werden sollte. Wenn derselbe Fehler systematisch auftritt, liegt die Ursache eher beim **Prompt oder Schema als beim einzelnen Input**.

Bei seltenen Grenzfällen kann ein Repair-Loop dagegen sinnvoller sein: Statt den Prompt unnötig komplex zu machen, wird nur bei fehlerhaften Ausgaben ein zusätzlicher API-Aufruf durchgeführt.
