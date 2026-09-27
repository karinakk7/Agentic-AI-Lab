# Reasoning

## OpenAI

### Reasoning Models

* Reasoning models use **internal reasoning tokens** before producing a response.
* They are particularly useful for **complex problem solving, coding, scientific reasoning, and multi-step agentic workflows**.

### Reasoning Effort

The `reasoning.effort` parameter guides the model on **how much reasoning to use when performing a task**.

Available effort levels include:

* `none`
* `minimal`
* `low`
* `medium`
* `high`
* `xhigh`
* `max`

In general, **lower effort** favors speed and lower token usage, while **higher effort** allows the model to reason more extensively, potentially improving the quality and reliability of the response.

The default effort level is generally **`medium`**, depending on the model.

| Effort        | Best for                                                                                                                                                                                                                                                                            |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`none`**    | Latency-critical tasks that do not benefit from reasoning or multi-step tool calls. Common use cases include voice, fast information retrieval, and classification.                                                                                                                 |
| **`minimal`** | Very lightweight reasoning where some additional reasoning may be useful while keeping latency and token usage low.                                                                                                                                                                 |
| **`low`**     | Efficient reasoning with a modest latency increase. Suitable for tool use, planning, search, and multi-step decision making while optimizing for speed and cost. Common use cases include data analysis, drafting, execution-oriented coding, and customer support/chat assistants. |
| **`medium`**  | A balanced choice when quality and reliability matter and the task involves planning, complex reasoning, or judgment. Common use cases include agentic coding, research, and working with spreadsheets and slides.                                                                  |
| **`high`**    | Hard reasoning, complex debugging, deep planning, and high-value tasks where quality matters more than latency. Suitable for complex workflows, agentic coding, long-horizon research, and knowledge work.                                                                          |
| **`xhigh`**   | Deep research, asynchronous workflows, and agentic tasks requiring long runs. Should be used when evaluations show that the additional reasoning provides enough benefit to justify the extra latency and cost.                                                                     |
| **`max`**     | Maximum reasoning for the most complex tasks. If currently using `xhigh`, evaluate whether `max` provides a meaningful improvement in performance.                                                                                                                                  |

### Key Takeaway

> **More reasoning is not automatically better.** The appropriate reasoning effort depends on the complexity and requirements of the task. For simple tasks such as classification or information retrieval, low or no reasoning may be sufficient. Complex coding, research, planning, or agentic workflows may justify higher reasoning effort.

### Architecture Consideration

The key question is:

> **"Does this task actually require reasoning?"**

Using a higher reasoning effort can increase **token usage, latency, and cost**. Therefore, reasoning effort should be treated as an **architecture decision** rather than simply choosing the highest available setting.

## Claude

### Extended Thinking

* **Manual Extended Thinking** allows you to configure a fixed reasoning budget using `budget_tokens`.
* You have direct control over how much Claude can think. For each request, you specify a thinking configuration such as:

  ```json
  {
    "thinking": {
      "type": "enabled",
      "budget_tokens": 5000
    }
  }
  ```
* Claude uses the allocated thinking budget for internal reasoning before producing its final answer.
* `budget_tokens` must be **at least 1,024 tokens**. The API rejects smaller values.
* Normally, `budget_tokens` must be **less than `max_tokens`**, because thinking tokens count toward the token limit for the turn.
* **Exception:** With **interleaved thinking**, `budget_tokens` can exceed `max_tokens` because the thinking budget spans all thinking blocks within a single assistant turn.
* **No cache pre-warming:** Extended Thinking cannot be combined with `max_tokens: 0`, because thinking requires tokens to be allocated.

### Interleaved Thinking in Manual Mode

* With **interleaved thinking**, Claude can reason **between tool calls within a single assistant turn**.
* Claude can therefore analyze the result of one tool call, reason about it, and then decide which action or tool call to perform next.
* This enables more complex **multi-step agentic workflows**.

Example:

```text
User request
    ↓
Claude thinks
    ↓
Tool call
    ↓
Tool result
    ↓
Claude thinks again
    ↓
Next tool call
    ↓
Final answer
```

This is particularly useful when a task requires Claude to **iteratively use tools and adapt its reasoning based on intermediate results**.


### Turn strcture in manual mode
 Claude supports thinking in combination with tool use within a turn.
- Thinking can be enabled or disabled between turns.
- In **manual mode**, the final assistant turn of a thinking-enabled request must begin with a thinking block.
- **Adaptive thinking** does not have this requirement.
- Changing the thinking configuration between turns invalidates prompt caching, which can increase latency and cost.

**Architecture implication:** Thinking configuration should be chosen deliberately and kept stable where possible to preserve prompt-cache benefits.

### Prompt Caching in Manual Mode

* Changing `budget_tokens` between requests **invalidates the prompt-cache breakpoint** because the budget value is rendered into the prompt.
* Simply switching the **thinking mode** does not necessarily invalidate the cache; changing the `budget_tokens` value does.
* In practice, this means that changing the thinking budget can cause the cached prompt content to be reprocessed, increasing **latency and potentially costs**.

---

## Reflexionsfragen

### 1. Bei welcher Aufgabe hat Reasoning messbar geholfen? Um welchen Faktor stiegen die Kosten?

**Aufgabe 2 (Mehrstufige Logik)** ist der Kandidat, bei dem Extended Thinking den Unterschied machen sollte. Die Rabattstaffel erfordert drei aufeinanderfolgende Regelanwendungen: erst die richtige Mengenstufe wählen (65 Stück → 10 %), dann den Stammkundenrabatt korrekt auf den bereits rabattierten Preis anwenden (× 0,97), und schließlich den Serviceaufschlag ausschließen, weil es nicht die erste Bestellung des Jahres ist. Standard-Modelle neigen hier dazu, Schritte zu verschmelzen oder die Reihenfolge zu verwechseln.

**Kostenfaktor:** Mit `budget_tokens=5000` und Sonnet-5-Preisen ($2/$10 pro 1M Tokens) entstehen grob:

| Modus              | Tokens (In/Out)  | Kosten (ca.) |
| ------------------ | ---------------- | ------------ |
| Standard           | ~200 / ~150      | ~0,17 ¢      |
| Extended Thinking  | ~200 / ~5200     | ~4,94 ¢      |

Thinking-Tokens zählen als Output → **Faktor ~30×** für diesen kleinen Einzelcall.
Bei Aufgabe 1 (Extraktion) entstehen dieselben Mehrkosten ohne jeden Qualitätsgewinn – klassischer Fall von Overkill.

### 2. Warum ist ein Reasoning-Modell für eine Klassifikationsaufgabe mit 100.000 Datensätzen fast immer die falsche Wahl?

Drei unabhängige Gründe, die zusammen ein KO-Kriterium ergeben:

**Kosten skalieren linear.** Wenn ein Reasoning-Call ~30× teurer ist als ein Standard-Call, multipliziert sich das direkt mit der Datenmenge. Aus 10 € werden 300 € – für denselben Accuracy-Wert, weil Klassifikation kein mehrstufiges Schlussfolgern braucht.

**Latenz ist nicht parallelisierbar (genug).** Reasoning-Tokens erzeugen sequenzielle Wartezeit pro Request. Selbst mit maximaler Parallelisierung summiert sich das bei 100.000 Calls auf Stunden statt Minuten.

**Das Problem passt nicht zum Werkzeug.** Klassifikation mit einem klaren Label-Set ist eine Mustererkennung, keine Deduktionskette. Das Modell muss nicht „überlegen" – es muss aus Trainingsdaten interpolieren. Ein feinjustiertes kleines Modell oder ein Standard-Call mit strukturiertem Output (`response_format: json`) liefert hier denselben oder besseren Accuracy-Wert.

> Faustregel: Reasoning lohnt sich wenn der **Lösungsweg mehrstufig und nicht in den Trainingsdaten direkt abgebildet** ist. Bei Klassifikation ist der Weg trivial – nur das Ziel zählt.

### 3. Was ist der Unterschied zwischen Reasoning im Modell und Chain-of-Thought im Prompt?

| Merkmal               | Reasoning im Modell (Extended Thinking)              | Chain-of-Thought im Prompt                          |
| --------------------- | ---------------------------------------------------- | --------------------------------------------------- |
| **Wo passiert es?**   | Intern, in separaten Thinking-Blöcken               | Im sichtbaren Output, als Text vor der Antwort      |
| **Kontrolle**         | Modell entscheidet selbst, wie es denkt             | Du gibst die Denkstruktur vor („Schritt 1: …")      |
| **Kosten**            | Thinking-Tokens = Output-Preis, unsichtbar          | CoT-Text = reguläre Output-Tokens, sichtbar         |
| **Ausgabe**           | Thinking-Blöcke oft nicht im finalen Response       | Denkschritte erscheinen im Antworttext              |
| **Manipulierbarkeit** | Modell kann Anweisungen besser widerstehen          | CoT kann durch adversarielle Inputs beeinflusst werden |
| **Geeignet wenn**     | Aufgabe wirklich komplex, Budget vorhanden          | Aufgabe mittelkomplex, Transparenz gewünscht        |

**Kernunterschied in einem Satz:** CoT ist eine Prompt-Technik, die das Modell zur expliziten Verschriftlichung seiner Zwischenschritte auffordert – Reasoning ist eine Modell-Architektur-Funktion, bei der das Modell einen geschützten, separat abgerechneten Denkraum erhält, bevor es antwortet.

**Praktische Konsequenz:** CoT ist kostengünstiger und portabler (funktioniert mit jedem Modell), aber das Modell kann die Denkschritte auch „vortäuschen" – der Output und das tatsächliche interne Verhalten sind nicht garantiert konsistent. Extended Thinking schafft eine härtere Garantie, dass das Modell tatsächlich vor der Antwort plant.
