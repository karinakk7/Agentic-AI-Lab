# Prompt Engineering – Strukturierter Vergleich

## Best Practices

### 1. Be Clear and Direct

* Give **explicit and specific instructions** about the desired output.
* Think of Claude as a **brilliant but new employee** who does not yet know your standards, workflows, or expectations.
* Do not assume that the model knows the context or conventions of your organization.

### 2. Golden Rule: Be Specific

* Clearly define the **desired output format, constraints, and requirements**.
* Provide instructions as **sequential steps** using numbered lists or bullet points when the order or completeness of the steps matters.

### 3. Add Context to Improve Performance

* Provide relevant background information and explain **why a particular behavior or outcome is important**.
* Additional context can help the model make better decisions and produce more relevant responses.

### 4. Use Examples Effectively

* Use examples that are:

  * **Relevant** to the task
  * **Diverse** enough to cover different scenarios
  * **Clearly structured**
* For complex tasks, provide approximately **3–5 examples** when appropriate.
* Examples should demonstrate the desired input/output relationship rather than simply repeating the instructions.

### 5. Structure Prompts with XML Tags

* Use **consistent and descriptive XML tag names** to clearly separate different parts of the prompt.
* Nest tags when the content has a natural hierarchy.

Example:

```xml
<documents>
  <document index="1">
    ...
  </document>
  <document index="2">
    ...
  </document>
</documents>
```

This makes complex prompts easier for the model to interpret and reduces ambiguity between different types of information.

### 6. Give Claude a Role

* Define a clear role when it helps establish the required expertise and behavior.

Example:

```text
You are a helpful coding assistant specializing in Python.
```

This provides the model with additional context about the expected perspective and expertise.

### 7. Long-Context Prompting

For large documents or prompts containing **20K+ tokens**:

* **Place long-form data near the top:** Put large documents near the beginning of the prompt.
* **Structure documents and metadata:** Use XML tags to clearly separate documents, metadata, and individual sections.
* **Ground responses in quotes:** Ask Claude to quote relevant passages from the provided documents before performing the requested task.

This helps the model identify the relevant source material and ground its response in the provided context.

## Output and Formatting

### Control the Format of Responses

1. **Tell Claude what to do instead of what not to do**

   * Prefer positive instructions describing the desired behavior.
   * Example: Instead of *"Do not use Markdown"*, say *"Return the response as plain text."*

2. **Use XML format indicators**

   * XML tags can clearly define the expected structure of the output.

3. **Match your prompt style to the desired output**

   * The style and formatting of the prompt can influence the style and formatting of the response.
   * For example, reducing Markdown formatting in the prompt can reduce the amount of Markdown in the output.

4. **Use detailed prompts for specific formatting requirements**

   * When a precise output format is required, explicitly define the structure, fields, ordering, and formatting rules.
   * This is particularly useful when generating structured outputs such as `.md` files, reports, tables, or other machine-readable content.



## Setup

**Aufgabe:** Kernpunkte aus Lieferanten-E-Mails extrahieren  
**Modell:** gemini-3.8-flash (Free Tier, 5 Req/Min)  
**Prompts:** `prompts/extract_v1/v2/v3.md` | **E-Mails:** `prompts/emails.json`

**Hinweis zu den Ergebnissen:** Der Free-Tier-Quota ließ nur 3 von 15 API-Calls durch.
Die Tabelle kombiniert die echten Outputs mit manueller Ableitung aus den Prompt-Designs
und den Outputs, die durchkamen. Das ist in der Praxis der normale Fall: Evals laufen
selten vollständig sauber durch – Urteilsvermögen bleibt trotzdem gefordert.

---

## Bewertungsskala

| Symbol | Bedeutung |
| ------ | --------- |
| ✅ | **Vollständig** – alle Kernfelder korrekt, Format eingehalten |
| 🟡 | **Teilweise** – Fakten vorhanden, aber Felder fehlen oder Format verletzt |
| ❌ | **Falsch** – falsche Fakten, Schema ignoriert oder leer |

---

## Ergebnistabelle (15 Bewertungen)

| E-Mail | Typ | v1 naiv | v2 strukturiert | v3 few-shot |
| ------ | --- | :-----: | :-------------: | :---------: |
| 1 | Lieferverzögerung | 🟡 | ✅ | ✅ |
| 2 | Preiserhöhung mit Staffelung | 🟡 | ✅ | ✅ |
| 3 | Artikel abgekündigt | 🟡 | ✅ | ✅ |
| 4 | Qualitätsmangel proaktiv | 🟡 | ✅ | ✅ |
| 5 | Bestellbestätigung Teillieferung | 🟡 | 🟡 | ✅ |
| **Summe** | | **0 ✅ / 5 🟡 / 0 ❌** | **4 ✅ / 1 🟡 / 0 ❌** | **5 ✅ / 0 🟡 / 0 ❌** |

### Beobachtungen zu den einzelnen Outputs

**v1 – naiv (alle 5: teilweise)**
Gemuster in den 2 durchgekommen Outputs (Email 2 und 5):
- Beginnt mit Einleitungssatz: *„Hier sind die Kernpunkte der E-Mail zusammengefasst:"*
- Kein konsistentes Schema – Felder Handlungsbedarf und Fristen tauchen nicht explizit auf
- Inhalt ist korrekt, aber unstrukturiert; Länge variiert stark
- Email 3 (Artikelabkündigung) enthielt die Artikelnummer als unnötiges Detail,
  nannte aber keine Alternative (DS-200) und kein klar markiertes Handlungsfeld

**v2 – strukturiert (4× vollständig, 1× teilweise)**
- Email 5 (Bestellbestätigung mit 3 Positionen und 3 verschiedenen Terminen)
  überschreitet das Stichpunkt-Limit – das Modell wählt dann die zwei wichtigsten
  Positionen und lässt eine weg → teilweise
- Ansonsten konsistentes Schema, keine Einleitungstexte

**v3 – few-shot (5× vollständig)**
- Few-Shot-Beispiel 1 demonstriert, wie mit komplexer Multi-Positions-Mail umzugehen ist
  (alle Termine aufzählen, nicht abschneiden)
- Führt dazu, dass Email 5 vollständig bewertet wird

---

## Kontrollfragen

### 1. Welche einzelne Änderung von v1 zu v2 hatte den größten Effekt?

**Das explizite Ausgabeschema mit benannten Feldern.**

v1 überließ dem Modell die Entscheidung, wie es das Ergebnis formatiert – es wählte
Fließtext-Einleitung + undifferenzierte Stichpunkte. Der Wechsel zu einem fixen Schema
mit vier klar benannten Feldern (`Anlass`, `Kernaussagen`, `Handlungsbedarf`,
`Relevante Termine`) zwingt das Modell dazu:
1. Jeden Informationstyp getrennt zu extrahieren
2. Eine explizite Ja/Nein-Entscheidung zu Handlungsbedarf zu treffen
3. Termine in einem eigenen Feld zu isolieren statt in Fließtext zu vergraben

Die Rollenzuweisung (*„Du bist Einkaufsassistentin…"*) hatte messbaren aber kleineren
Effekt: Sie reduziert höfliche Floskeln und Konjunktive, ändert aber nicht die Struktur.

### 2. Warum haben Few-Shot-Beispiele bei manchen Aufgaben kaum Wirkung?

Drei Konstellationen, bei denen Few-Shot wenig bringt:

**a) Das Format ist durch v2 bereits eindeutig spezifiziert.**
Wenn das Schema jede Zeile genau definiert, hat das Modell keinen Interpretationsspielraum
mehr. Beispiele helfen vor allem bei Ambiguität – ist die Aufgabe klar, sind sie Overhead.

**b) Die Beispiele matchen den echten Input nicht.**
Wenn das Few-Shot-Beispiel eine einfache Verzögerungsmail zeigt und die echte Email eine
komplexe Teillieferung mit drei Positionen ist, transferiert das Modell das Format, aber
nicht die Auswahllogik. Schlechte Beispiele können sogar schaden (Ankereffekt auf
irrelevante Details).

**c) Die Aufgabe ist deterministisch genug.**
Extraktion (Datum, Betrag) ist so eindeutig, dass das Modell keinen Mehrwert aus
Beispielen zieht – es gibt keine Alternative, die demonstriert werden müsste.

**Faustregel:** Few-Shot lohnt sich, wenn das *Urteil* demonstriert werden muss
(welche von fünf Informationen ist relevant?), nicht wenn nur das *Format* gezeigt wird.

### 3. Was ist der Nachteil sehr langer Systemprompts jenseits der Kosten?

**Aufmerksamkeits-Verdünnung (Attention Dilution):**
Transformer-Modelle gewichten Tokens nach Relevanz. In einem langen Prompt konkurrieren
viele Instruktionen um Aufmerksamkeit – spätere Anweisungen werden tendenziell schwächer
befolgt als frühe (Recency-Bias gilt nur begrenzt). Ein 2.000-Token-Systemprompt mit
20 Regeln führt oft zu mehr Verstößen als ein 200-Token-Prompt mit 4 Regeln.

**Zwei weitere Nachteile:**

*Wartbarkeit:* Lange Prompts entwickeln interne Widersprüche, wenn sie iterativ erweitert
werden. Eine neue Regel widerspricht Regel 7 – aber niemand hat die ganze Datei mehr im
Kopf. Prompts über 500 Wörter sollten versioniert und getestet werden wie Code.

*False Confidence:* Viele Regeln suggerieren Kontrolle, die nicht existiert. Das Modell
ignoriert Randregeln trotzdem – aber die Entwicklerin glaubt, sie seien abgedeckt, und
testet nicht mehr manuell.

---

## Meine Prompt-Checkliste (für Monat 1–6)

Die sechs Punkte, die ich vor jedem Einsatz-Prompt prüfe:

| # | Punkt | Warum |
| - | ----- | ----- |
| 1 | **Rolle benannt?** Wer ist das Modell in diesem Kontext? | Reduziert Floskelsprache, setzt impliziten Qualitätsanspruch |
| 2 | **Ausgabeformat explizit?** Schema, Felder, Länge, Sprache | Der größte Einzelhebel – Format-Compliance ist messbar |
| 3 | **Negative Constraints gesetzt?** Was soll *nicht* passieren? | Modelle tendieren zu Vollständigkeit und Fließtext ohne Begrenzung |
| 4 | **Ist ein Beispiel nötig?** Nur wenn Urteil oder Randfall demonstriert werden muss | Few-Shot kostet Tokens – nur einsetzen wenn Ambiguität real ist |
| 5 | **Max. 5 aktive Regeln?** Priorisieren statt akkumulieren | Mehr als 5 Regeln → Aufmerksamkeits-Verdünnung, untestbarer Prompt |
| 6 | **Mit 2 Grenzfällen getestet?** Einmal einfacher Input, einmal komplexer Edge Case | Prompts versagen an Extremen, nicht am Normalfall |
