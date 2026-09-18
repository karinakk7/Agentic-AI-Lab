# Monat 3 – Evaluation, Observability und die Agent-Grundlagen
**Woche 9–12 · Tag 33–48 · Projekt: `ai-knowledge-assistant` abschließen, Agent-Fundament legen**

**Monatsziel:** Du kannst objektiv messen, ob ein KI-System besser geworden ist – und du hast einen Agenten von Hand gebaut, bevor du ein Framework anfasst.

**Warum Evaluation vor Agenten:** Ein Agent hat mehr Freiheitsgrade als jedes andere KI-System. Ohne Messinstrumente optimierst du ihn nach Gefühl und merkst Verschlechterungen erst in der Produktion. Die Reihenfolge in diesem Plan ist bewusst anders als in den meisten Kursen – und sie ist der Grund, warum du in Monat 4 schneller vorankommst.

---

# WOCHE 9 – RAG-Evaluation

**Wochenziel:** Du hast eine automatisierte Eval-Suite mit den Standardmetriken und kennst deren Grenzen.
**Themen:** Faithfulness, Answer Relevancy, Context Precision/Recall, Ragas, LLM-as-a-Judge
**Praxisergebnis:** `eval/` mit Ragas-Lauf, eigenem Judge und Fehleranalyse.

---

## Tag 33 · Montag – Die vier Metriken, die zählen

**Zeit:** 60 Minuten

### 🎯 Lernziel
Du kannst die vier RAG-Kernmetriken definieren und sagen, welche welchen Fehlertyp aufdeckt.

### 📚 1. Lernen – 20 Min
**Ragas Documentation – Core Concepts / Metrics**
Link: https://docs.ragas.io
Dauer: 20 Min
Zu bearbeiten: Die Metrikbeschreibungen für **Faithfulness**, **Answer Relevancy**, **Context Precision**, **Context Recall**. Noch nicht installieren.

Die entscheidende Struktur:

| Metrik | Misst | Braucht Ground Truth? | Deckt auf |
|---|---|---|---|
| Context Recall | Wurde alles Relevante gefunden? | ja | Retriever findet zu wenig |
| Context Precision | Steht Relevantes weit oben? | ja | Ranking ist schlecht |
| Faithfulness | Steht die Antwort in den Auszügen? | nein | Halluzination |
| Answer Relevancy | Beantwortet die Antwort die Frage? | nein | Thema verfehlt |

Die beiden oberen messen den **Retriever**, die beiden unteren den **Generator**. Damit hast du die Diagnosestruktur aus Monat 2 formalisiert.

Danach: heise KI Update → Discover.

### 💻 2. Praxis – 30 Min
Bevor du ein Werkzeug einsetzt: Bewerte **10 Antworten deines Systems von Hand** auf allen vier Metriken (Skala 0–1). Notiere in `eval/manual_baseline.csv`.

Das dauert lange und ist Absicht: Du sollst wissen, wie sich diese Metriken anfühlen, bevor eine Bibliothek dir eine Zahl liefert, die du nicht hinterfragst.

Erwartetes Ergebnis: 10 × 4 = 40 manuelle Bewertungen plus eine Notiz zu jedem Fall, bei dem du selbst unsicher warst.

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Bei welcher Metrik warst du dir am unsichersten? Was sagt das über automatisierte Bewertung derselben Metrik aus?
2. Eine Antwort ist faithful, aber nicht relevant. Wie sieht so ein Fall konkret aus?
3. Warum brauchen Context Recall und Precision Ground Truth, Faithfulness aber nicht?

**Dokumentieren:** `notes/tag33-metriken.md`.

---

## Tag 34 · Mittwoch – Ragas praktisch einsetzen

**Zeit:** 60 Minuten

### 🎯 Lernziel
Du hast einen automatisierten Eval-Lauf, dessen Ergebnisse du gegen deine manuelle Bewertung prüfst.

### 📚 1. Lernen – 10 Min
**Ragas – Getting Started**
Link: https://docs.ragas.io
Dauer: 10 Min
Zu bearbeiten: Installation, Datenformat, `evaluate()`.

Danach 10 Min: heise KI Update → Understand.

### 💻 2. Praxis – 30 Min
```bash
pip install ragas datasets
```

Erstelle `eval/run_ragas.py`. Datenformat:

```python
{"question": ..., "answer": ..., "contexts": [...], "ground_truth": ...}
```

Lauf über dieselben 10 Fragen, die du gestern manuell bewertet hast.

**Der eigentliche Punkt der Übung:** Vergleiche Ragas-Werte mit deinen manuellen. Wo weichen sie ab? Bei welchen Fällen liegt Ragas falsch – und bei welchen lagst **du** falsch?

Anschließend über das volle 30-Fragen-Set laufen lassen.

Erwartetes Ergebnis: Vier Metrikwerte für dein System plus eine Abweichungsanalyse. Kostenhinweis: Ragas nutzt ein LLM als Bewerter – nimm ein günstiges Modell und beachte die Kosten.

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Wie stark korrelierten Ragas-Werte mit deinen? Bei welcher Metrik am wenigsten?
2. Was kostet ein vollständiger Eval-Lauf – und wie oft kannst du ihn dir leisten?
3. Warum ist ein Eval-Lauf mit demselben Modell, das auch generiert, problematisch?

**Dokumentieren:** `EVALUATION.md` erweitern.

---

## Tag 35 · Donnerstag – LLM-as-a-Judge selbst bauen

**Zeit:** 60 Minuten

### 🎯 Lernziel
Du baust einen eigenen Judge und kennst seine drei bekannten Verzerrungen.

### 📚 1. Lernen – 15 Min
**DeepEval Docs – LLM-as-a-Judge / G-Eval**
Link: https://deepeval.com
Dauer: 15 Min
Zu bearbeiten: Wie ein Judge-Prompt strukturiert wird und wie Bewertungskriterien explizit gemacht werden.

Die drei Verzerrungen, die du kennen musst:
- **Position bias** – bei Paarvergleichen wird die erste Antwort bevorzugt
- **Verbosity bias** – längere Antworten werden besser bewertet
- **Self-preference** – ein Modell bevorzugt Texte, die es selbst erzeugt hat

### 💻 2. Praxis – 35 Min
Erstelle `eval/judge.py`:

```python
class Bewertung(BaseModel):
    faithfulness: int = Field(ge=1, le=5)
    begruendung_faithfulness: str
    vollstaendigkeit: int = Field(ge=1, le=5)
    begruendung_vollstaendigkeit: str
```

Wichtige Bauprinzipien:
1. **Kriterien explizit im Prompt**, nicht „bewerte die Qualität"
2. **Begründung vor Zahl** erzwingen (die Reihenfolge im Schema ist relevant)
3. Skala 1–5 mit beschriebenen Ankerpunkten, nicht 1–10 ohne Beschreibung

Dann teste die **Verbosity-Verzerrung** empirisch: Nimm 5 gute kurze Antworten, lass ein Modell sie ohne Informationsgewinn auf die doppelte Länge aufblähen, und bewerte beide Varianten mit deinem Judge.

Erwartetes Ergebnis: Vermutlich bekommen die längeren Antworten bessere Noten, obwohl sie nicht besser sind. Diese Zahl ist Gold wert – sie zeigt, dass du Judges nicht blind vertraust.

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Um wie viel besser wurden die aufgeblähten Antworten bewertet?
2. Wie könntest du Verbosity-Verzerrung im Prompt gegensteuern?
3. Wann ist ein Judge unverzichtbar, wann reicht eine regelbasierte Prüfung?

**Dokumentieren:** `notes/tag35-judge.md` mit den Verzerrungsmesswerten.

---

## Tag 36 · Samstag – Synthetisches Testset und Fehleranalyse (Build-Session)

**Zeit:** 90 Minuten

### 🎯 Lernziel
Du skalierst dein Testset und leitest aus den schlechtesten Fällen konkrete Verbesserungen ab.

### 📚 1. Lernen – 20 Min
**Ragas – Testset Generation**
Link: https://docs.ragas.io
Dauer: 20 Min
Zu bearbeiten: Wie aus einem Dokumentenkorpus Fragen unterschiedlicher Komplexität generiert werden (einfach, mehrstufig, konditional).

Warum relevant: Dein handgebautes 30-Fragen-Set ist qualitativ hochwertig, aber zu klein für belastbare Aussagen. Synthetische Sets ergänzen – sie ersetzen das handgebaute nicht.

### 💻 2. Praxis – 60 Min
**Teil A (25 Min):** Generiere 50 synthetische Fragen aus deinem Korpus. Prüfe **stichprobenartig 10 davon** manuell – wie viele sind sinnvoll? Notiere die Ausschussquote.

**Teil B (35 Min): Fehleranalyse.** Lauf die Evaluation über alle 80 Fragen (30 handgebaut + 50 synthetisch). Sortiere nach Gesamtscore und nimm dir die **10 schlechtesten** vor.

Für jeden Fall trägst du in `eval/fehleranalyse.md` ein:

| # | Frage | Was ging schief | Kategorie | Hypothese | Fix |
|---|---|---|---|---|---|

Kategorien: `retrieval_miss` · `ranking` · `chunking` · `generation` · `frage_schlecht` · `ground_truth_falsch`

Erwartetes Ergebnis: Eine Verteilung der Fehlerkategorien. Typischerweise sind 2–3 Kategorien für über die Hälfte der Fehler verantwortlich – genau dort investierst du.

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Welche Fehlerkategorie dominiert? Was ist die billigste Gegenmaßnahme dafür?
2. Wie viele „Fehler" waren in Wahrheit schlechte Testfragen? Was heißt das für synthetische Sets?
3. Was wäre die teuerste Maßnahme, die du dir jetzt sparst, weil die Analyse sie nicht rechtfertigt?

**Commit + Push.** Wochenreflexion `reviews/woche-09.md`.

---

# WOCHE 10 – Observability und datengetriebene Iteration

**Wochenziel:** Du siehst, was dein System intern tut, und leitest daraus Verbesserungen ab.
**Themen:** Tracing, OpenTelemetry GenAI Conventions, Langfuse, Eval im CI
**Praxisergebnis:** Instrumentierte Pipeline, CI-Gate, Projekt 2 abgeschlossen.

---

## Tag 37 · Montag – Tracing verstehen und Langfuse aufsetzen

**Zeit:** 60 Minuten

### 🎯 Lernziel
Du verstehst Spans, Traces und die `gen_ai.*`-Konventionen und hast eine lokale Tracing-Instanz.

### 📚 1. Lernen – 20 Min
**Langfuse Docs – Get Started + Tracing Data Model**
Link: https://langfuse.com/docs
Dauer: 20 Min
Zu bearbeiten: Das Datenmodell (Trace → Span → Generation) und Self-Hosting per Docker.

Kontext: Die Branche hat sich auf **OpenTelemetry** als Standard geeinigt, mit den GenAI Semantic Conventions im `gen_ai.*`-Namespace. Das bedeutet für dich: Deine Instrumentierung ist portabel – du kannst später von Langfuse zu Phoenix, MLflow oder einem anderen Backend wechseln, ohne alles neu zu schreiben. Langfuse ist Open Source, self-hostbar und für den Einstieg am unkompliziertesten.

Danach: heise KI Update → Discover.

### 💻 2. Praxis – 30 Min
```bash
git clone https://github.com/langfuse/langfuse
cd langfuse && docker compose up -d
# UI auf http://localhost:3000, Projekt anlegen, Keys kopieren
pip install langfuse
```

Instrumentiere zunächst nur **einen** Call deiner Pipeline und sieh ihn dir in der UI an. Verstehe, wo Kosten, Latenz und Prompt/Completion landen.

Erwartetes Ergebnis: Ein sichtbarer Trace. Screenshot für dein README.

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Was ist der Unterschied zwischen einem Trace und einem Span?
2. Warum ist OpenTelemetry-Kompatibilität ein Auswahlkriterium und kein Nebenaspekt?
3. Welche Information willst du im Trace sehen, die standardmäßig nicht drin ist?

---

## Tag 38 · Mittwoch – Die gesamte Pipeline instrumentieren

**Zeit:** 60 Minuten

### 🎯 Lernziel
Jede Stufe deiner RAG-Pipeline ist einzeln sichtbar, mit Latenz und Kosten.

### 📚 1. Lernen – 10 Min
**Langfuse Docs – Decorators / Nested Spans**
Link: https://langfuse.com/docs
Dauer: 10 Min

Danach 10 Min: heise KI Update → Understand.

### 💻 2. Praxis – 30 Min
Setze Spans um: `route` → `query_transform` → `retrieve_dense` → `retrieve_sparse` → `fuse` → `rerank` → `generate` → `verify`.

Pro Span als Attribut mitgeben: Dauer, Anzahl Ergebnisse, Modell, Tokens, Kosten. Beim Retrieval-Span zusätzlich die Chunk-IDs.

Lauf 20 Anfragen durch und sieh dir in der UI an: Welche Stufe verbraucht die meiste Zeit? Welche das meiste Geld?

Erwartetes Ergebnis: Ein Latenz-Profil. Fast immer überraschend – meist ist es nicht die Stufe, die man erwartet.

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Welche Stufe war der Latenz-Engpass? Entsprach das deiner Erwartung?
2. Welche Stufe verursacht die meisten Kosten?
3. Welche Information fehlt dir im Trace, um einen Fehlerfall nachzuvollziehen?

**Dokumentieren:** `notes/tag38-tracing.md` mit dem Latenz-Profil.

---

## Tag 39 · Donnerstag – Aus Traces Hypothesen ableiten

**Zeit:** 60 Minuten

### 🎯 Lernziel
Du arbeitest datengetrieben statt nach Bauchgefühl: Hypothese → Experiment → Messung → Entscheidung.

### 📚 1. Lernen – 10 Min
Kein neues Material. Lies stattdessen deine eigene `eval/fehleranalyse.md` und dein Latenz-Profil noch einmal durch.

### 💻 2. Praxis – 40 Min
Formuliere **drei Hypothesen** im Format:

> „Wenn ich ___ ändere, dann steigt ___ um mindestens ___, weil ___. Das kostet mich ___."

Beispiele, die sich aus typischen Analysen ergeben:
- „Wenn ich Top-k von 5 auf 8 erhöhe, steigt Context Recall um 5 Punkte, kostet aber 60 % mehr Input-Tokens."
- „Wenn ich die Chunk-Größe von 500 auf 300 senke, steigt Precision, aber mehrteilige Fragen werden schlechter."
- „Wenn ich den Reranker nur bei `komplex`-Routing einsetze, sinken die Kosten um 30 % bei unverändertem Recall."

Teste **alle drei** gegen dein 80-Fragen-Set. Trage die Ergebnisse ein und entscheide für jede: übernehmen / verwerfen.

Erwartetes Ergebnis: Mindestens eine Hypothese wird widerlegt. Das ist der wertvollste Teil – dokumentiere ihn ausdrücklich in `DECISIONS.md`.

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Welche Hypothese wurde widerlegt? Warum hattest du sie trotzdem für plausibel gehalten?
2. Was wäre passiert, wenn du die Änderung ohne Messung übernommen hättest?
3. Wie viele Anfragen braucht dein Testset, damit ein Unterschied von 2 Punkten belastbar ist?

---

## Tag 40 · Samstag – Eval als CI-Gate, Projekt 2 abschließen (Build-Session)

**Zeit:** 90 Minuten

### 🎯 Lernziel
Deine Evaluation läuft automatisch bei jedem Push und blockiert Verschlechterungen.

### 📚 1. Lernen – 20 Min
**DeepEval – pytest-Integration** und **GitHub Actions – Workflow-Grundlagen**
Links: https://deepeval.com · https://docs.github.com/actions
Dauer: 20 Min
Zu bearbeiten: `assert_test()` bzw. Schwellenwertprüfungen, und ein minimaler Workflow mit Secrets.

### 💻 2. Praxis – 60 Min
**Teil A (30 Min):** `tests/test_quality.py`:

```python
def test_faithfulness_schwelle():
    ergebnis = run_eval(testset="eval/testset_klein.jsonl")
    assert ergebnis["faithfulness"] >= 0.85

def test_recall_schwelle():
    assert ergebnis["context_recall"] >= 0.80

def test_ablehnung_funktioniert():
    # Die 3 "nicht beantwortbar"-Fragen MÜSSEN abgelehnt werden
    assert ergebnis["korrekte_ablehnungen"] == 3
```

Wichtig: Für CI nimmst du ein **kleines Testset (10–15 Fragen)**, damit der Lauf schnell und billig ist. Das große Set läufst du manuell vor größeren Änderungen.

**Teil B (30 Min):** `.github/workflows/eval.yml` – bei Push auf `main` die Tests laufen lassen, API-Keys als Secrets.

Erwartetes Ergebnis: Ein grünes Badge im README. Teste das Gate, indem du absichtlich eine Verschlechterung einbaust (Reranking ausschalten) und siehst, wie CI rot wird.

**Projekt 2 abschließen:** README finalisieren, `EVALUATION.md` mit allen fünf Versionen, `LIMITATIONS` ehrlich ausfüllen, Repo pinnen.

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Welche Schwelle hast du gewählt und warum genau diese Zahl?
2. Was kostet ein CI-Lauf? Wie oft pro Tag ist das tragbar?
3. Warum ist ein Test „Ablehnung funktioniert" wichtiger als ein Test auf durchschnittliche Qualität?

**Commit + Push.** Wochenreflexion `reviews/woche-10.md`.

---

# WOCHE 11 – Agent-Grundlagen ohne Framework

**Wochenziel:** Du baust einen Agenten von Hand und kannst begründen, wann man gar keinen braucht.
**Themen:** Workflow vs. Agent, Agent-Loop, Tool-Design, Planungsmuster
**Praxisergebnis:** `mini_agent.py` und eine Entscheidungsregel „Agent ja/nein".

---

## Tag 41 · Montag – Workflow oder Agent? Die wichtigste Entscheidung

**Zeit:** 60 Minuten

### 🎯 Lernziel
Du kannst begründen, wann ein deterministischer Workflow besser ist als ein Agent – und das ist häufiger der Fall, als der Markt suggeriert.

### 📚 1. Lernen – 25 Min
**Anthropic Engineering – Building effective agents**
Link: https://www.anthropic.com/engineering
Dauer: 25 Min
Zu bearbeiten: Vollständig. Besonders die Unterscheidung zwischen **Workflows** (vordefinierte Pfade) und **Agenten** (Modell steuert den Ablauf selbst) sowie die Muster Prompt Chaining, Routing, Parallelization, Orchestrator-Workers, Evaluator-Optimizer.

Warum dieser Artikel trotz seines Alters: Er ist die klarste Darstellung der Muster, die 2026 immer noch die Grundlage jedes Agent-Frameworks bilden. LangGraph, das OpenAI Agents SDK und das Microsoft Agent Framework implementieren im Kern genau diese Muster. Wer sie kennt, lernt jedes Framework in einem Tag.

Danach: heise KI Update → Discover.

### 💻 2. Praxis – 25 Min
Erstelle `notes/agent-entscheidung.md` – deine eigene Entscheidungsregel:

```
Braucht diese Aufgabe einen Agenten?

1. Sind die Schritte im Voraus bekannt?          → ja: Workflow
2. Ist die Schrittzahl vorhersehbar?             → ja: Workflow
3. Muss das System auf Zwischenergebnisse
   reagieren und den Plan ändern?                → ja: Agent-Kandidat
4. Ist ein Fehler teuer/irreversibel?            → Human-in-the-Loop zwingend
5. Rechtfertigt der Nutzen das 5–20-fache
   an Tokens gegenüber einem Workflow?           → wenn nein: Workflow
```

Wende sie auf **fünf Szenarien** an – drei aus deinem Arbeitsumfeld, zwei erfundene. Begründe jede Entscheidung in zwei Sätzen.

Erwartetes Ergebnis: Wahrscheinlich brauchen drei bis vier der fünf keinen Agenten. Dieses Ergebnis ehrlich aufzuschreiben ist ein Expertisemerkmal.

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Welches deiner fünf Szenarien braucht wirklich einen Agenten – und welches Kriterium gab den Ausschlag?
2. Was kostet ein Agent gegenüber einem Workflow ungefähr, in Tokens gerechnet?
3. Was ist der Unterschied zwischen Routing (Workflow-Muster) und einem Agenten, der ein Tool wählt?

---

## Tag 42 · Mittwoch – Agent-Loop from scratch

**Zeit:** 60 Minuten

### 🎯 Lernziel
Du schreibst einen vollständigen Agenten in unter 100 Zeilen und weißt danach, was jedes Framework für dich versteckt.

### 📚 1. Lernen – 10 Min
Kein neues Material. Sieh dir stattdessen deinen `tool_loop.py` aus Tag 9/10 an. Der Agent ist dieser Loop **plus Zustand plus Zielprüfung**.

Danach 10 Min: heise KI Update → Understand.

### 💻 2. Praxis – 30 Min
Erstelle im neuen Repo `ai-research-agent` die Datei `src/mini_agent.py`:

```python
def agent(ziel: str, tools: dict, max_steps: int = 10, budget_eur: float = 0.10):
    verlauf = [{"role": "user", "content": ziel}]
    kosten = 0.0
    for schritt in range(max_steps):
        antwort = llm(verlauf, tools=tool_schemas(tools))
        kosten += antwort.cost_eur
        if kosten > budget_eur:
            return abbruch("Budget überschritten", verlauf)
        if antwort.tool_calls:
            for tc in antwort.tool_calls:
                ergebnis = sicher_ausfuehren(tools, tc)   # Fehler als Text zurück
                verlauf.append(tool_result(tc.id, ergebnis))
        else:
            return erfolg(antwort.text, verlauf, kosten, schritt)
    return abbruch("max_steps erreicht", verlauf)
```

Vier Tools: `web_search` (erstmal fest kodierte Ergebnisse), `lese_datei`, `rechne`, `notiere`.

Testaufgabe: „Finde heraus, welche drei Punkte in Dokument X zur Haftung stehen, und fasse sie zusammen."

Erwartetes Ergebnis: Ein laufender Agent mit sichtbarem Schritt-für-Schritt-Protokoll.

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Wie viele Schritte brauchte dein Agent? Wie viele wären nötig gewesen?
2. Was ist die Abbruchbedingung – und warum ist „bis das Modell aufhört" allein gefährlich?
3. Wo in diesem Loop würdest du einen menschlichen Freigabeschritt einbauen?

**Dokumentieren:** `notes/tag42-agentloop.md` mit dem vollständigen Protokoll eines Durchlaufs.

---

## Tag 43 · Donnerstag – Tool-Design als Kernkompetenz

**Zeit:** 60 Minuten

### 🎯 Lernziel
Du gestaltest Tools so, dass das Modell sie richtig einsetzt – und du siehst, wie stark die Beschreibung das Verhalten steuert.

### 📚 1. Lernen – 15 Min
**Anthropic Engineering – Writing effective tools for agents**
Link: https://www.anthropic.com/engineering
Dauer: 15 Min
Zu bearbeiten: Benennung, Beschreibungen, Parameter-Granularität, Fehlerrückgaben.

Kernprinzipien:
- Ein Tool pro Aufgabe, nicht ein Universal-Tool mit `action`-Parameter
- Die Beschreibung erklärt **wann** man es benutzt, nicht nur **was** es tut
- Fehler kommen als hilfreicher Text zurück, nicht als Exception
- Rückgaben sind kompakt (Tokens!) und in einem für das Modell lesbaren Format

### 💻 2. Praxis – 35 Min
Experiment in `src/tool_design_lab.py`:

Definiere dasselbe Tool dreimal unterschiedlich:
- **A:** `def suche(q)` mit Docstring „Sucht etwas."
- **B:** `def dokument_suche(anfrage: str, max_ergebnisse: int = 5)` mit ausführlichem Docstring inkl. „Nutze dieses Tool, wenn die Frage sich auf interne Dokumente bezieht. Nicht für allgemeines Wissen."
- **C:** wie B, plus zwei Anwendungsbeispiele im Docstring

Lauf 8 Testaufgaben pro Variante. Miss: Wie oft wurde das Tool korrekt gewählt? Wie oft mit sinnvollen Parametern?

Erwartetes Ergebnis: Eine klare Abstufung A < B < C. Die Zahl belegt: Tool-Beschreibungen sind Prompts.

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Wie groß war der Unterschied zwischen A und C in Prozent korrekter Tool-Wahl?
2. Was passiert, wenn zwei Tools sich in ihrer Beschreibung überschneiden?
3. Warum ist ein Universal-Tool mit `action`-Parameter fast immer die schlechtere Wahl?

**Dokumentieren:** `notes/tag43-tooldesign.md` + eine persönliche Tool-Checkliste.

---

## Tag 44 · Samstag – Planungsmuster: ReAct vs. Plan-and-Execute (Build-Session)

**Zeit:** 90 Minuten

### 🎯 Lernziel
Du kennst zwei Planungsmuster, hast beide implementiert und kannst ihre Kosten vergleichen.

### 📚 1. Lernen – 20 Min
Recherchiere beide Muster:

- **ReAct:** Denken → Handeln → Beobachten, Schritt für Schritt. Flexibel, reagiert auf Zwischenergebnisse, kann aber im Kreis laufen.
- **Plan-and-Execute:** Erst vollständigen Plan erstellen, dann abarbeiten, optional nachplanen. Vorhersehbarer, günstiger (weniger LLM-Calls), aber starrer bei Überraschungen.

### 💻 2. Praxis – 60 Min
Implementiere beide in `src/patterns.py` auf derselben Aufgabe:

> „Vergleiche die Kündigungsregelungen in Dokument A und Dokument B und nenne die drei wichtigsten Unterschiede."

Miss für beide über **5 Durchläufe**:

| Muster | Ø Schritte | Ø LLM-Calls | Ø Kosten | Ø Latenz | Erfolgsquote |
|---|---|---|---|---|---|

Erwartetes Ergebnis: Plan-and-Execute ist meist günstiger und schneller; ReAct ist robuster, wenn ein Tool unerwartet versagt. Teste das, indem du in einem Durchlauf ein Tool absichtlich fehlschlagen lässt.

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Welches Muster war günstiger, welches robuster? Um welchen Faktor?
2. Wie verhielt sich Plan-and-Execute beim Tool-Fehler?
3. Für welchen Anwendungsfall aus deinem Job würdest du welches Muster wählen?

**Commit + Push.** Wochenreflexion `reviews/woche-11.md`.

---

# WOCHE 12 – Memory, Context Engineering, Agentic RAG

**Wochenziel:** Dein Agent behält den Überblick über lange Läufe und nutzt dein RAG-System als Werkzeug.
**Themen:** Memory-Arten, Context Compaction, Sub-Agents, Agentic RAG
**Praxisergebnis:** Agent mit Memory, der deine Wissensbasis selbstständig befragt und sich korrigiert.

---

## Tag 45 · Montag – Memory: drei Arten, drei Zwecke

**Zeit:** 60 Minuten

### 🎯 Lernziel
Du unterscheidest Kurzzeit-, Arbeits- und Langzeitgedächtnis und implementierst eine Kompaktierungsstrategie.

### 📚 1. Lernen – 20 Min
**Hugging Face Agents Course – Modul zu Memory**
Link: https://huggingface.co/learn/agents-course
Dauer: 20 Min
Zu bearbeiten: Das Kapitel zu Agent-Memory und Zustandsverwaltung.

Die drei Arten:
| Art | Lebensdauer | Umsetzung | Typischer Fehler |
|---|---|---|---|
| Kurzzeit | eine Konversation | Nachrichtenverlauf | wächst unkontrolliert |
| Arbeit/Scratchpad | eine Aufgabe | Datei oder Variable | wird nicht gelesen |
| Langzeit | über Sitzungen | Vektorspeicher / DB | wird zu unspezifisch abgerufen |

Danach: heise KI Update → Discover.

### 💻 2. Praxis – 30 Min
Erweitere `mini_agent.py` um `src/memory.py`:

1. **Kurzzeit mit Kompaktierung:** Wenn der Verlauf 60 % des Kontextfensters überschreitet, fasse die ältesten Schritte per LLM zu einem Absatz zusammen und ersetze sie.
2. **Scratchpad:** Ein `findings.md`, in das der Agent per Tool `notiere(erkenntnis)` schreibt und das er per `lies_notizen()` wieder lesen kann.

Test: Eine Aufgabe, die 12+ Schritte braucht. Beobachte, ob der Agent nach der Kompaktierung noch weiß, was er vorher herausgefunden hat.

Erwartetes Ergebnis: Ein Agent, der lange Läufe übersteht. Miss die Tokenersparnis durch die Kompaktierung.

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Hat der Agent nach der Kompaktierung Information verloren? Welche?
2. Warum ist ein externes Scratchpad oft besser als alles im Kontext zu halten?
3. Bei welcher Schwelle würdest du kompaktieren – und was ist der Nachteil bei zu früher Kompaktierung?

---

## Tag 46 · Mittwoch – Context Engineering für Agenten

**Zeit:** 60 Minuten

### 🎯 Lernziel
Du kennst die Techniken, mit denen 2026 Agentenkontext strukturiert wird: Skills, Sub-Agents, Hooks.

### 📚 1. Lernen – 20 Min
**Hugging Face Context Course** (6 Einheiten zu Context Engineering für Code-Agenten, kostenlos)
Link: https://huggingface.co/learn
Dauer: 20 Min
Zu bearbeiten: Einheit 1 (Agent Skills) und die Übersicht der übrigen Einheiten. Die MCP-Einheit hebst du dir für Monat 5 auf.

Warum relevant: Dieser Kurs ist aus dem Frühjahr 2026 und behandelt genau die Verschiebung, die stattgefunden hat – von „wie formuliere ich den Prompt" zu „wie strukturiere ich Wissen so, dass ein Agent es findet, wenn er es braucht". Das ist derzeit die am höchsten bewertete Fähigkeit beim Agentenbau.

Danach 10 Min: heise KI Update → Understand.

### 💻 2. Praxis – 20 Min
Wende das Prinzip auf deinen Agenten an: Statt alle Anweisungen in einen großen Systemprompt zu packen, lege `skills/` an:

```
skills/
├── dokumentanalyse.md    ← wann und wie Dokumente analysiert werden
├── vergleich.md          ← Vorgehen bei Vergleichsaufgaben
└── berichterstellung.md  ← Ausgabeformat für Berichte
```

Der Agent bekommt im Systemprompt nur die **Namen und Einzeiler-Beschreibungen**, und ein Tool `lade_skill(name)`, mit dem er die Details bei Bedarf nachlädt.

Miss: Systemprompt-Länge vorher vs. nachher, und ob die Aufgabenqualität gleich bleibt.

Erwartetes Ergebnis: Deutlich kürzerer Basiskontext bei gleicher Leistung – das skaliert auf 20 Skills, ein Monolith-Prompt nicht.

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Um wie viel ist dein Basiskontext geschrumpft?
2. Wann lädt der Agent den falschen Skill – und woran liegt das? (Zurück zu Tag 43: Beschreibungen.)
3. Was ist der Zusammenhang zwischen dieser Technik und dem, was du in Monat 5 mit MCP machst?

---

## Tag 47 · Donnerstag – Agentic RAG: Retrieval im Loop

**Zeit:** 60 Minuten

### 🎯 Lernziel
Dein Agent entscheidet selbst, wann und wie oft er sucht – und erkennt, wenn die Ergebnisse nicht reichen.

### 📚 1. Lernen – 15 Min
Recherchiere **Self-RAG** und **CRAG** (Corrective RAG). Kernidee beider: Nach dem Retrieval bewertet das System selbst, ob die Auszüge ausreichen, und sucht gegebenenfalls neu – mit umformulierter Anfrage oder anderer Quelle.

Dazu der Kontrast zum klassischen RAG: Dort ist Retrieval **vor** der Generierung fest verdrahtet. Im agentischen Fall ist es ein Werkzeug **innerhalb** der Schleife.

### 💻 2. Praxis – 35 Min
Binde dein Projekt-2-Retrieval als Tool ein:

```python
def wissensbasis_suche(anfrage: str, k: int = 5) -> str:
    """Durchsucht die interne Dokumentensammlung (Verträge, Richtlinien).
    Nutze dieses Tool für alle Fragen zu internen Regelungen.
    Gibt Auszüge mit Quellenangabe zurück."""
```

Ergänze eine Selbstprüfung: Nach jedem Retrieval bewertet der Agent per Structured Output, ob die Auszüge zur Beantwortung reichen (`ausreichend: bool`, `fehlt: str`). Wenn nicht, formuliert er die Anfrage um und sucht erneut – **maximal 3 Mal**.

Test: Fünf Fragen, davon zwei, deren Antwort zwei verschiedene Suchen braucht.

Erwartetes Ergebnis: Bei den mehrteiligen Fragen sucht der Agent mehrfach und findet mehr als die einmalige Pipeline. Vergleiche Kosten gegen die klassische Pipeline aus Monat 2.

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Wie viel besser waren die Antworten auf die mehrteiligen Fragen – und um welchen Faktor teurer?
2. Wann lief die Selbstkorrektur ins Leere (drei Suchen, trotzdem nichts)?
3. Warum brauchst du zwingend eine Obergrenze für die Suchschleife?

---

## Tag 48 · Samstag – Monatstest 3 und Konsolidierung

**Zeit:** 90 Minuten

### 💻 Teil 1 – Aufräumen (30 Min)
- `ai-research-agent` Repo-Struktur anlegen (README-Gerüst, ARCHITECTURE, DECISIONS)
- `mini_agent.py` mit Memory, Skills und Agentic RAG committen
- Langfuse-Tracing auch für den Agenten aktivieren

### 🧠 Teil 2 – Monatstest 3 (60 Min)

**Leitfrage A: Woran erkennst du objektiv, dass dein System besser geworden ist?**
**Leitfrage B: Wann braucht man einen Agenten – und wann nicht?**

Schriftlich in `notes/test-monat-3.md`:

1. Definiere Faithfulness, Answer Relevancy, Context Precision und Context Recall – je ein Satz, ohne nachzuschlagen.
2. Welche zwei Metriken messen den Retriever, welche den Generator?
3. Nenne drei Verzerrungen von LLM-as-a-Judge und je eine Gegenmaßnahme.
4. Dein Faithfulness-Wert ist 0,92, die Nutzer beschweren sich trotzdem. Nenne drei mögliche Ursachen.
5. Wann ist ein Workflow einem Agenten überlegen? Nenne fünf Kriterien.
6. Beschreibe den Agent-Loop in fünf Sätzen, ohne ein Framework zu erwähnen.
7. Nenne drei Sicherungen, die jeder produktive Agent braucht.
8. Was ist der Unterschied zwischen Kurzzeit-, Arbeits- und Langzeitgedächtnis – mit je einem konkreten Beispiel?
9. Warum ist die Tool-Beschreibung wichtiger als die Tool-Implementierung?
10. Erkläre Agentic RAG gegenüber klassischem RAG und nenne den Preis.

**Praktische Aufgabe (25 Min):**
Ein Kollege zeigt dir einen Agenten, der eine feste Abfolge von vier Schritten ausführt und dafür ein Frontier-Modell mit Reasoning nutzt. Schreibe eine halbe Seite Code-Review: Was würdest du ändern, in welcher Reihenfolge, und welche Ersparnis schätzt du?

**Bewertungskriterien:**

| Kriterium | Bestanden, wenn … |
|---|---|
| Messkultur | Du kannst zu jeder Metrik sagen, welchen Fehlertyp sie aufdeckt |
| Skepsis | Du nennst mindestens zwei Gründe, einer Eval-Zahl nicht zu trauen |
| Zurückhaltung | Bei der praktischen Aufgabe empfiehlst du, den Agenten durch einen Workflow zu ersetzen |
| Eigene Zahlen | Mindestens vier Antworten enthalten einen Messwert aus deinen Projekten |

**Bevor du zu Monat 4 weitergehst, solltest du können:**
- Eine Eval-Suite aufsetzen und ihre Ergebnisse kritisch einordnen
- Einen Agent-Loop ohne Framework schreiben
- Begründen, wann kein Agent nötig ist
- Traces lesen und daraus Hypothesen ableiten

**Halbzeit-Rückblick:** Du bist bei Tag 48 von 96. Schreib eine halbe Seite: Was kannst du heute, was du vor drei Monaten nicht konntest? Was ist immer noch unklar? Das ist auch die Rohfassung für ein LinkedIn-Update, falls du eines machen willst.

**Wochenreflexion** `reviews/woche-12.md`.
