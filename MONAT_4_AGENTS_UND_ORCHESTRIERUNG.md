# Monat 4 – AI Agents und Orchestrierung
**Woche 13–16 · Tag 49–64 · Projekt: `ai-research-agent`**

**Monatsziel:** Du beherrschst ein modernes Agent-Framework tief genug, um damit produktionsnahe Systeme zu bauen – mit persistentem Zustand, menschlicher Freigabe, Multi-Agent-Struktur und einem Kostenbudget, das nicht explodiert.

**Die Framework-Entscheidung:** Du lernst **LangGraph** als Hauptframework. Begründung: Es ist der Standard für zustandsbehaftete, unterbrechbare Workflows mit Human-in-the-Loop, es hat die reifste Persistenz-Schicht, und es hat die mit Abstand größte Verbreitung in Unternehmen. In Woche 14 portierst du **einmal** in ein zweites Framework – nicht, um es zu lernen, sondern um zu sehen, was framework-spezifisch und was universell ist.

**Wichtige Randnotiz aus der Recherche:** Alle aktuellen Frameworks sprechen inzwischen MCP für Tools, und viele unterstützen A2A für frameworkübergreifende Übergaben. Der Lock-in liegt heute nicht mehr im Protokoll, sondern in der Abstraktionsebene – eine Migration bedeutet, jede Agent- und Tool-Definition neu zu schreiben. Deshalb: eines richtig, nicht fünf oberflächlich.

---

# WOCHE 13 – LangGraph

**Wochenziel:** Du baust Graphen mit Zustand, Bedingungen, Persistenz und menschlicher Freigabe.
**Themen:** State, Nodes, Edges, Conditional Edges, Checkpointer, Interrupts
**Praxisergebnis:** Research Agent v1 – Suche, Lesen, Zusammenfassen mit Quellen.

---

## Tag 49 · Montag – LangGraph-Grundkonzepte

**Zeit:** 60 Minuten

### 🎯 Lernziel
Du verstehst State, Nodes und Edges und kannst einen linearen Graphen bauen.

### 📚 1. Lernen – 20 Min
**LangGraph – offizielle Dokumentation**
Link: https://www.langchain.com/langgraph (von dort in die Docs)
Dauer: 20 Min
Zu bearbeiten: Quickstart plus das Kapitel „State". Die Multi-Agent-Kapitel überspringst du noch.

Das mentale Modell: Ein Graph ist eine Zustandsmaschine. Der `State` ist ein typisiertes Dictionary, das durch den Graphen gereicht wird. Jeder Node ist eine Funktion `state → state_update`. Edges bestimmen, wer als Nächstes dran ist.

Der wichtige Punkt, den man leicht übersieht: **Reducer**. Wenn zwei Nodes dasselbe Feld schreiben, entscheidet der Reducer, ob überschrieben oder angehängt wird (`Annotated[list, operator.add]`). Das ist die Ursache der meisten Anfängerfehler.

Danach: heise KI Update → Discover.

### 💻 2. Praxis – 30 Min
```bash
cd ai-research-agent
pip install langgraph langchain-core langchain-anthropic langchain-openai
```

Erstelle `src/graph_basics.py` – drei Nodes, linear:

```python
from typing import Annotated, TypedDict
import operator

class State(TypedDict):
    frage: str
    suchbegriffe: list[str]
    ergebnisse: Annotated[list[str], operator.add]
    antwort: str

# Node 1: frage → suchbegriffe
# Node 2: suchbegriffe → ergebnisse
# Node 3: ergebnisse → antwort
```

Lass dir den Graphen als Mermaid ausgeben (`graph.get_graph().draw_mermaid()`) und speichere ihn für `ARCHITECTURE.md`.

Erwartetes Ergebnis: Ein laufender 3-Node-Graph plus Diagramm. Experimentiere: Was passiert ohne den `operator.add`-Reducer bei `ergebnisse`?

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Was ist ein Reducer und was passiert ohne ihn?
2. Warum ist der State typisiert, und was gewinnst du dadurch?
3. Wo steckt in diesem Graphen der Agent-Loop aus Tag 42 – und wo nicht?

**Dokumentieren:** `notes/tag49-langgraph.md`.

---

## Tag 50 · Mittwoch – Conditional Edges und Schleifen

**Zeit:** 60 Minuten

### 🎯 Lernziel
Dein Graph trifft Entscheidungen und kann kontrolliert in Schleifen laufen.

### 📚 1. Lernen – 15 Min
**LangGraph Docs – Conditional Edges, Cycles**
Dauer: 15 Min
Zu bearbeiten: `add_conditional_edges`, die Rolle von `END`, Rekursionslimit.

Danach 10 Min: heise KI Update → Understand.

### 💻 2. Praxis – 25 Min
Erweitere den Graphen um eine Qualitätsschleife:

```
suche → bewerte_ergebnisse → [ausreichend?]
                              ├─ ja  → antworte → END
                              └─ nein→ verfeinere_suche → suche  (max. 3×)
```

Die Bewertung nutzt Structured Output (`ausreichend: bool`, `was_fehlt: str`). Der Schleifenzähler liegt im State, **nicht** in einer globalen Variable.

Setze zusätzlich `recursion_limit` beim Aufruf und provoziere absichtlich einen Abbruch, um zu sehen, wie sich das verhält.

Erwartetes Ergebnis: Ein Graph, der sich selbst korrigiert und bei Erfolglosigkeit sauber abbricht statt endlos zu laufen.

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Warum gehört der Schleifenzähler in den State?
2. Was passiert beim Erreichen des Rekursionslimits – und wie fängst du das nutzerfreundlich ab?
3. Wo ist der Unterschied zwischen dieser Schleife und einer `while`-Schleife in `mini_agent.py`?

---

## Tag 51 · Donnerstag – Persistenz und Human-in-the-Loop

**Zeit:** 60 Minuten

### 🎯 Lernziel
Dein Graph überlebt einen Neustart und kann an definierter Stelle auf eine menschliche Freigabe warten.

### 📚 1. Lernen – 20 Min
**LangGraph Docs – Persistence, Checkpointers, Human-in-the-loop / interrupt**
Dauer: 20 Min
Zu bearbeiten: `SqliteSaver` / `MemorySaver`, `thread_id`, `interrupt()` und wie man mit einem Wert fortsetzt.

Warum das der eigentliche Grund für LangGraph ist: Ein Agent, der nach einem Absturz oder einem Deployment weiterlaufen kann, und einer, der vor einer folgenreichen Aktion anhält und fragt – das ist der Unterschied zwischen Demo und Produktivsystem. Und es adressiert direkt das Risiko, das OWASP 2026 auf Platz 3 gehoben hat: **Excessive Agency**.

### 💻 2. Praxis – 30 Min
1. `SqliteSaver` einbauen, `thread_id` pro Sitzung
2. Graph starten, nach zwei Schritten den Prozess **hart beenden**, neu starten, mit derselben `thread_id` fortsetzen
3. Einen `interrupt()` vor einem als „folgenreich" markierten Tool einbauen (z. B. `sende_bericht`)
4. Freigabe simulieren: Der Graph pausiert, du gibst frei, er läuft weiter

Erwartetes Ergebnis: Ein Agent, der nach Prozessneustart exakt dort weitermacht, und einer, der vor der kritischen Aktion anhält. Das filmst du als GIF fürs README.

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Was genau wird im Checkpoint gespeichert – und was nicht?
2. Bei welchen Tools würdest du in deinem Capstone zwingend `interrupt()` setzen?
3. Warum ist Human-in-the-Loop eine Sicherheitsmaßnahme und nicht nur ein Komfortmerkmal?

**Dokumentieren:** `notes/tag51-persistence.md`.

---

## Tag 52 · Samstag – Research Agent v1 (Build-Session)

**Zeit:** 90 Minuten

### 🎯 Lernziel
Ein funktionierender Rechercheagent, der mehrere Schritte ausführt und Quellen liefert.

### 📚 1. Lernen – 15 Min
**Hugging Face Agents Course – Einheit zu Tools und Ausführung**
Link: https://huggingface.co/learn/agents-course
Dauer: 15 Min
Zu bearbeiten: Die Übersicht der Agent-Bausteine als Auffrischung.

### 💻 2. Praxis – 65 Min
Baue `src/research_graph.py`:

```
START
  → plane        (Frage → 3–5 Teilfragen, Structured Output)
  → recherchiere (pro Teilfrage: web_search + wissensbasis_suche)
  → bewerte      (reichen die Belege? → Schleife zurück, max. 2×)
  → synthetisiere(strukturierter Bericht mit Zitaten)
  → END
```

Tools:
- `web_search` – nutze eine kostenlose Option: DuckDuckGo über `ddgs`, oder Tavily Free Tier
- `lies_url` – Seite abrufen und in Text umwandeln (`trafilatura` oder `httpx` + `readability`)
- `wissensbasis_suche` – dein Retrieval aus Projekt 2

Ausgabeschema:
```python
class Bericht(BaseModel):
    frage: str
    zusammenfassung: str
    befunde: list[Befund]        # aussage + quelle_url + zitat
    offene_punkte: list[str]
    konfidenz: Literal["hoch", "mittel", "niedrig"]
```

Testfrage: Etwas aus deinem Fachgebiet, dessen Antwort du selbst beurteilen kannst.

Erwartetes Ergebnis: Ein Bericht mit echten, klickbaren Quellen. Prüfe mindestens drei Zitate manuell nach.

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Wie viele deiner geprüften Zitate stimmten mit der Quelle überein?
2. Wie viele Schritte und wie viel Geld hat ein Durchlauf gekostet?
3. Welcher Node ist am fehleranfälligsten?

**Commit + Push.** Wochenreflexion `reviews/woche-13.md`.

---

# WOCHE 14 – Framework-Landschaft und Robustheit

**Wochenziel:** Du kannst Frameworks begründet auswählen und deinen Agenten gegen Fehler absichern.
**Themen:** Framework-Vergleich, Portierung, Fehlerbehandlung, Budgetgrenzen, strukturierte Endergebnisse
**Praxisergebnis:** Entscheidungsmatrix und ein abgesicherter Agent.

---

## Tag 53 · Montag – Die Framework-Landschaft 2026

**Zeit:** 60 Minuten

### 🎯 Lernziel
Du kannst sechs Frameworks nach ihrem jeweiligen Stärkebereich einordnen und eine begründete Auswahl treffen.

### 📚 1. Lernen – 25 Min
**Langfuse Blog – Vergleich von Open-Source-Agent-Frameworks** (Stand Juli 2026)
Link: https://langfuse.com/blog/2025-03-19-ai-agent-comparison
Dauer: 15 Min
Zu bearbeiten: Die Einordnung von LangGraph, DeepAgents, OpenAI Agents SDK, Claude Agent SDK, Google ADK, Pydantic AI, CrewAI, Microsoft Agent Framework, smolagents.

**Ergänzend, 10 Min:** LangChain-Übersicht der Frameworks
Link: https://www.langchain.com/resources/ai-agent-frameworks

Kurzeinordnung als Ausgangspunkt für deine eigene Matrix:

| Framework | Stärke | Wann du es wählst |
|---|---|---|
| **LangGraph** | Durable State, HITL, Checkpointing | Der Agent muss einen Absturz überleben oder unterbrechbar sein |
| **OpenAI Agents SDK** | Minimal, vier Primitive (Agents, Handoffs, Guardrails, Sessions) | Schneller Prototyp, OpenAI-nahes Umfeld |
| **Claude Agent SDK** | Code- und Dateimanipulation | Die Arbeit ist Software-/Dateiarbeit |
| **Microsoft Agent Framework** | Azure-Integration, Foundry Agent Service | Enterprise auf Azure – **für dein Profil besonders relevant** |
| **Pydantic AI** | Typsicherheit, FastAPI-Gefühl | Das Team lebt ohnehin in Pydantic |
| **smolagents** | Kleinster Weg zu einem Agent-Loop | Lernzwecke, einfache Einzelagenten |

Und die ehrliche Gegenposition, die in der Recherche mehrfach auftauchte: Jedes Framework fügt Vokabular, Fehlerquellen und Versionsabhängigkeiten hinzu. Manchmal lohnt sich das, oft nicht – der sinnvolle Ausgangspunkt ist das nackte Provider-SDK. Genau deshalb hast du in Monat 3 zuerst ohne Framework gebaut.

Danach: heise KI Update → Discover.

### 💻 2. Praxis – 25 Min
Erstelle `notes/framework-matrix.md` mit **deinen** Kriterien, gewichtet:

| Kriterium | Gewicht | LangGraph | OpenAI SDK | MS Agent FW | Pydantic AI |
|---|---|---|---|---|---|
| Durable State | | | | | |
| Human-in-the-Loop | | | | | |
| Azure-Integration | | | | | |
| Lernkurve | | | | | |
| Observability-Anbindung | | | | | |
| MCP-Unterstützung | | | | | |
| Team-Fit (dein Umfeld) | | | | | |

Die Gewichtung ist der eigentliche Inhalt – sie zwingt dich, deine Prioritäten explizit zu machen.

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Welches Framework gewinnt nach deiner Gewichtung – und weicht das von deiner Intuition ab?
2. Welches Kriterium hat die Entscheidung gekippt?
3. Wann würdest du ganz auf ein Framework verzichten?

---

## Tag 54 · Mittwoch – Portierung in ein zweites Framework

**Zeit:** 60 Minuten

### 🎯 Lernziel
Du erkennst, was am Agentenbau framework-spezifisch ist und was universell.

### 📚 1. Lernen – 15 Min
**OpenAI Agents SDK Docs** oder **Pydantic AI Docs** (wähle eines)
Links: https://openai.github.io/openai-agents-python/ · https://ai.pydantic.dev
Dauer: 15 Min
Zu bearbeiten: Quickstart und die Kernprimitive.

Danach 10 Min: heise KI Update → Understand.

### 💻 2. Praxis – 25 Min
Portiere **nur den Kern** deines Research Agents (planen → recherchieren → synthetisieren) ins zweite Framework. Ohne Persistenz, ohne HITL.

Miss: Zeilen Code, benötigte Zeit, welche Funktion fehlte oder war umständlicher.

Erwartetes Ergebnis: Vermutlich weniger Code, aber auch weniger Kontrolle. Trage das Ergebnis in deine Matrix ein.

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Welcher Teil deines Agenten war **identisch** in beiden Frameworks? (Antwort: die Tools und die Prompts – und genau das ist der Punkt.)
2. Was ging im zweiten Framework schneller, was fehlte?
3. Wie lange würde eine Migration eines echten Produktivsystems dauern?

**Dokumentieren:** `notes/tag54-portierung.md`.

---

## Tag 55 · Donnerstag – Robustheit: Timeouts, Retries, Budgets

**Zeit:** 60 Minuten

### 🎯 Lernziel
Dein Agent kann nicht mehr unbemerkt Geld verbrennen oder ewig hängen.

### 📚 1. Lernen – 15 Min
**OWASP GenAI Security Project – LLM06 Excessive Agency**
Link: https://genai.owasp.org
Dauer: 15 Min
Zu bearbeiten: Die Beschreibung des Risikos und die empfohlenen Gegenmaßnahmen.

Kontext: In der 2026er-Ausgabe der OWASP Top 10 für LLM-Anwendungen ist Excessive Agency von Platz 6 auf **Platz 3** gestiegen. Der Grund ist genau das, was du gerade baust: Agenten mit Tool-Zugriff, die eigenständig handeln. Was du heute einbaust, ist deshalb keine Fleißarbeit, sondern die Kernmaßnahme gegen das drittwichtigste Risiko der Kategorie.

### 💻 2. Praxis – 35 Min
Erstelle `src/guards.py` und wickle deinen Graphen darin ein:

```python
@dataclass
class Limits:
    max_steps: int = 15
    max_kosten_eur: float = 0.25
    max_laufzeit_s: int = 120
    max_tool_calls_pro_tool: dict[str, int] = ...   # z.B. web_search: 8
```

Umsetzung:
1. Nach jedem Node: Limits prüfen, bei Überschreitung geordnet in einen `abbruch`-Node
2. Tool-Aufrufe mit `timeout`
3. Retry mit exponentiellem Backoff bei transienten Fehlern (429, 5xx), **kein** Retry bei 4xx
4. Ein `budget_verbraucht`-Feld im State, das im Endergebnis mit ausgegeben wird

Test: Baue eine Aufgabe, die absichtlich in eine Schleife führt („Suche so lange, bis du absolute Gewissheit hast"). Der Agent muss sauber abbrechen und einen Teilbericht liefern.

Erwartetes Ergebnis: Ein Agent, der bei Abbruch einen brauchbaren Zwischenstand ausgibt statt einer Exception.

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Was passiert bei Budgetüberschreitung – Exception oder Teilergebnis? Warum ist das die bessere Wahl?
2. Warum retry-st du bei 429, aber nicht bei 400?
3. Welche Grenze ist in deinem Capstone-Szenario die kritischste?

---

## Tag 56 · Samstag – Strukturiertes Endergebnis und Fehlererkennung (Build-Session)

**Zeit:** 90 Minuten

### 🎯 Lernziel
Dein Agent liefert ein maschinenlesbares Ergebnis und erkennt selbst, wenn er unsicher ist.

### 📚 1. Lernen – 15 Min
Auffrischung Structured Outputs (Tag 8) – jetzt angewandt auf komplexe verschachtelte Ergebnisse.

### 💻 2. Praxis – 65 Min
**Teil A (35 Min):** Erweitere das `Bericht`-Schema:

```python
class Befund(BaseModel):
    aussage: str
    belege: list[Beleg]
    konfidenz: Literal["hoch", "mittel", "niedrig"]
    widerspruch_gefunden: bool

class Bericht(BaseModel):
    frage: str
    zusammenfassung: str
    befunde: list[Befund]
    quellen_gesamt: list[str]
    offene_punkte: list[str]
    nicht_beantwortbar_weil: str | None
    metadaten: Metadaten   # schritte, kosten_eur, dauer_s, modelle
```

**Teil B (30 Min): Fehlererkennung.** Baue einen `pruefe`-Node vor `END`:
1. Enthält jeder Befund mindestens einen Beleg? (programmatisch)
2. Kommt jedes Zitat wortwörtlich in der Quelle vor? (programmatisch – dein Verfahren aus Tag 27)
3. Widersprechen sich zwei Befunde? (LLM-Prüfung)

Bei Verstoß: Befund als `konfidenz: niedrig` markieren oder entfernen, und in `offene_punkte` vermerken.

Erwartetes Ergebnis: Ein Agent, der lieber „das konnte ich nicht belegen" sagt als etwas zu erfinden. Miss über 10 Läufe, wie oft der Prüf-Node eingreift.

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Wie oft griff die Zitatprüfung ein?
2. Warum ist programmatische Prüfung der LLM-Prüfung vorzuziehen, wo immer sie möglich ist?
3. Was ist der Unterschied zwischen „der Agent ist unsicher" und „der Agent sagt, er sei unsicher"?

**Commit + Push.** Wochenreflexion `reviews/woche-14.md`.

---

# WOCHE 15 – Multi-Agent-Systeme

**Wochenziel:** Du kennst die Multi-Agent-Muster und kannst begründen, wann Mehr-Agenten-Architektur hilft und wann sie nur Komplexität hinzufügt.
**Themen:** Supervisor, Handoffs, Parallelisierung, Evaluator-Optimizer, Agent-Evaluation
**Praxisergebnis:** Ein Supervisor-Graph mit Researcher, Critic und Writer.

---

## Tag 57 · Montag – Multi-Agent-Muster

**Zeit:** 60 Minuten

### 🎯 Lernziel
Du kennst vier Muster und die Bedingungen, unter denen sie sich lohnen.

### 📚 1. Lernen – 20 Min
**LangGraph Docs – Multi-Agent Systems**
Dauer: 20 Min
Zu bearbeiten: Supervisor, Network/Handoffs, Hierarchical.

Die vier Muster:
| Muster | Aufbau | Gut für | Preis |
|---|---|---|---|
| **Supervisor** | Ein Koordinator delegiert an Spezialisten | Klar trennbare Teilaufgaben | +1 LLM-Call pro Delegation |
| **Handoff** | Agenten reichen direkt weiter | Sequenzielle Spezialisierung | Kontextverlust an Übergaben |
| **Parallel** | Mehrere Agenten gleichzeitig, dann Zusammenführung | Unabhängige Teilfragen | Latenzgewinn, Kostenmultiplikation |
| **Evaluator-Optimizer** | Ein Agent produziert, einer kritisiert, Schleife | Qualität wichtiger als Kosten | 2–3× Kosten |

Die ehrliche Einordnung: Multi-Agent lohnt sich, wenn Teilaufgaben **echt unabhängig** sind oder **verschiedene Werkzeuge/Rollen** brauchen. Wenn ein Agent mit 8 Tools dieselbe Aufgabe löst, ist Multi-Agent meist teurer und fehleranfälliger.

Danach: heise KI Update → Discover.

### 💻 2. Praxis – 30 Min
Skizziere in `ARCHITECTURE.md` **drei** Varianten deines Research Agents:
- A: Einzelagent mit allen Tools (dein aktueller Stand)
- B: Supervisor + Researcher + Writer
- C: Supervisor + Researcher + Critic + Writer

Schätze für jede: Anzahl LLM-Calls pro Durchlauf, erwartete Kosten, erwartete Qualität. Das prüfst du an Tag 58/59 nach.

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Welches Muster passt zu „drei unabhängige Teilfragen parallel beantworten"?
2. Was ist das Hauptproblem bei Handoffs?
3. Nenne einen Fall, in dem Multi-Agent klar schlechter ist als ein guter Einzelagent.

---

## Tag 58 · Mittwoch – Supervisor-Graph bauen

**Zeit:** 60 Minuten

### 🎯 Lernziel
Du implementierst ein Supervisor-Muster mit sauberer Zustandstrennung.

### 📚 1. Lernen – 10 Min
**LangGraph Docs – Supervisor-Beispiel**
Dauer: 10 Min

Danach 10 Min: heise KI Update → Understand.

### 💻 2. Praxis – 30 Min
Erstelle `src/multi_agent.py`:

```
supervisor ──→ researcher (Tools: web_search, wissensbasis_suche, lies_url)
    ↑  ↓
    └── writer     (kein Tool-Zugriff, nur Formulierung)
```

Der Supervisor entscheidet per Structured Output:
```python
class Delegation(BaseModel):
    naechster: Literal["researcher", "writer", "fertig"]
    auftrag: str
    begruendung: str
```

Wichtig: **Trenne den Zustand.** Der Writer bekommt nicht den vollständigen Recherche-Verlauf, sondern nur die gesammelten Befunde. Das spart Tokens und verhindert, dass er Zwischenschritte in den Bericht schreibt.

Erwartetes Ergebnis: Ein laufender Supervisor-Graph. Vergleiche Kosten und Qualität gegen Variante A auf denselben 5 Testfragen.

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. War Variante B besser als A? Um welchen Preis?
2. Warum bekommt der Writer nicht den vollen Verlauf?
3. Wie verhinderst du, dass der Supervisor endlos hin- und herdelegiert?

---

## Tag 59 · Donnerstag – Der Critic und die Reflexionsschleife

**Zeit:** 60 Minuten

### 🎯 Lernziel
Du baust Evaluator-Optimizer ein und misst, ob Selbstkritik tatsächlich hilft.

### 📚 1. Lernen – 10 Min
Auffrischung: Dein Judge aus Tag 35 plus seine Verzerrungen. Der Critic ist ein Judge im Loop – dieselben Fallen gelten.

### 💻 2. Praxis – 40 Min
Füge einen `critic`-Node hinzu:

```python
class Kritik(BaseModel):
    unbelegte_aussagen: list[str]
    fehlende_aspekte: list[str]
    bewertung: int = Field(ge=1, le=5)
    ueberarbeitung_noetig: bool
```

Schleife: `writer → critic → [überarbeitung nötig?] → writer` mit **max. 2 Revisionen**.

Der entscheidende Test: Lauf 8 Testfragen dreimal durch – Variante A (Einzelagent), B (Supervisor), C (mit Critic). Bewerte die Berichte **blind**: Speichere sie ohne Kennzeichnung und bewerte sie erst danach nach einem festen Kriterienraster.

Erwartetes Ergebnis: Eine ehrliche Tabelle. Häufiger Befund: Der Critic verbessert Belegqualität spürbar, verschlechtert aber die Lesbarkeit, und kostet das Zwei- bis Dreifache.

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Hat der Critic gemessen etwas gebracht – und in welcher Dimension genau?
2. Warum hast du blind bewertet?
3. Ab welchem Kostenniveau würdest du auf den Critic verzichten?

**Dokumentieren:** `EVALUATION.md` mit dem A/B/C-Vergleich.

---

## Tag 60 · Samstag – Agent-Evaluation: Trajektorien bewerten (Build-Session)

**Zeit:** 90 Minuten

### 🎯 Lernziel
Du bewertest nicht nur das Ergebnis, sondern den **Weg** dorthin – Tool-Wahl, Schrittzahl, Effizienz.

### 📚 1. Lernen – 20 Min
**DeepEval Docs – Agent-Metriken**
Link: https://deepeval.com
Dauer: 20 Min
Zu bearbeiten: Tool Correctness, Task Completion, komponentenweise Evaluation.

Warum das anders ist als RAG-Evaluation: Zwei Agenten können dasselbe richtige Ergebnis liefern – einer in 3 Schritten für 2 Cent, einer in 14 Schritten für 30 Cent. Ergebnisorientierte Metriken sehen keinen Unterschied. Trajektorien-Metriken schon.

### 💻 2. Praxis – 60 Min
Erstelle `eval/agent_eval.py` mit vier Metriken:

```python
def tool_correctness(trajektorie, erwartete_tools) -> float
    # Wurden die richtigen Tools benutzt?
def schritt_effizienz(trajektorie, optimale_schritte) -> float
    # optimale_schritte / tatsaechliche_schritte, gedeckelt auf 1.0
def task_completion(bericht, ziel) -> float
    # LLM-Judge: Wurde das Ziel erreicht?
def belegdichte(bericht) -> float
    # Anteil der Aussagen mit verifiziertem Beleg
```

Baue `eval/agent_testset.jsonl` mit **12 Aufgaben**, jeweils mit `erwartete_tools` und `optimale_schritte` (die du selbst festlegst, indem du die Aufgabe gedanklich löst).

Lauf alle drei Varianten (A/B/C) durch und fülle die Tabelle:

| Variante | Tool Correctness | Schritt-Effizienz | Task Completion | Belegdichte | Ø Kosten |
|---|---|---|---|---|---|

Erwartetes Ergebnis: Die vollständige Vergleichstabelle in `EVALUATION.md`. Diese Tabelle ist der Kern deines Repo-Werts.

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Welche Variante hat die beste Kosten-Qualitäts-Relation?
2. Wo weicht die Trajektorien-Bewertung von der Ergebnis-Bewertung ab?
3. Welches Tool wurde am häufigsten unnötig aufgerufen – und wie beseitigst du das? (Tipp: Tag 43.)

**Commit + Push.** Wochenreflexion `reviews/woche-15.md`.

---

# WOCHE 16 – Kosten, Tracing, Abschluss

**Wochenziel:** Projekt 3 ist optimiert, beobachtbar und vorzeigbar.
**Themen:** Model Routing, Agent-Tracing, Dokumentation, Monatstest
**Praxisergebnis:** `ai-research-agent` öffentlich mit Demo und Zahlen.

---

## Tag 61 · Montag – Model Routing: der größte Kostenhebel

**Zeit:** 60 Minuten

### 🎯 Lernziel
Du senkst die Agent-Kosten deutlich, ohne die Qualität zu verlieren, indem du jedem Schritt das passende Modell zuweist.

### 📚 1. Lernen – 15 Min
Zurück zu `notes/models.md` (Tag 1) und deinem Vergleichslauf (Tag 12). Frage: Welcher Node in deinem Graphen braucht wirklich ein Frontier-Modell?

Typische Verteilung:
| Node | Modellklasse | Begründung |
|---|---|---|
| Supervisor/Routing | klein & schnell | Entscheidung zwischen 3 Optionen |
| Suchbegriffe generieren | klein | Textumformung |
| Bewertung „reicht das?" | mittel | braucht Urteilsvermögen |
| Synthese des Berichts | groß | Qualität sichtbar für den Nutzer |
| Critic | mittel bis groß | Fehlerfindung braucht Kompetenz |

Danach: heise KI Update → Discover.

### 💻 2. Praxis – 35 Min
Implementiere `src/routing.py`: Jeder Node bekommt sein Modell aus einer Konfiguration.

```python
MODELLE = {
    "supervisor": "klein",
    "plan": "klein",
    "bewerte": "mittel",
    "synthese": "gross",
    "critic": "mittel",
}
```

Lauf dein 12-Aufgaben-Testset zweimal: einmal alles mit dem großen Modell, einmal mit Routing. Vergleiche Kosten, Latenz und alle vier Agent-Metriken.

Erwartetes Ergebnis: Eine deutliche Kostenersparnis bei annähernd gleicher Qualität. Notiere den genauen Prozentsatz – das ist eine der überzeugendsten Zahlen, die du vorweisen kannst.

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Wie viel Prozent Kosten hast du gespart, und welche Metrik hat gelitten?
2. Bei welchem Node hat das kleine Modell Fehler gemacht? Wie hast du das gemerkt?
3. Was ist der Nachteil, verschiedene Anbieter in einem Graphen zu mischen?

---

## Tag 62 · Mittwoch – Agent-Tracing und Engpassanalyse

**Zeit:** 60 Minuten

### 🎯 Lernziel
Du siehst die vollständige Trajektorie eines Agenten in einer Oberfläche und findest Engpässe.

### 📚 1. Lernen – 10 Min
**Langfuse Docs – LangGraph-Integration**
Link: https://langfuse.com/docs
Dauer: 10 Min

Danach 10 Min: heise KI Update → Understand.

### 💻 2. Praxis – 30 Min
1. Langfuse-Callback für den gesamten Graphen aktivieren
2. 15 Durchläufe mit unterschiedlichen Aufgaben
3. In der UI analysieren:
   - Welcher Node kostet am meisten?
   - Bei welchen Aufgaben lief die Bewertungsschleife durch?
   - Wie hoch ist die Kostenspreizung zwischen billigstem und teuerstem Durchlauf?

Setze ein Tag pro Durchlauf (`variante=C`, `modell_routing=an`), damit du in der UI filtern kannst.

Erwartetes Ergebnis: Screenshots einer Trajektorie für das README plus eine Liste von drei konkreten Optimierungen.

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Wie groß ist die Kostenspreizung zwischen dem günstigsten und dem teuersten Durchlauf? Was heißt das für die Budgetplanung?
2. Welcher Node hat die höchste Varianz in der Laufzeit?
3. Welche Information brauchst du im Trace, die noch fehlt?

---

## Tag 63 · Donnerstag – Dokumentation Projekt 3

**Zeit:** 60 Minuten

### 🎯 Lernziel
Dein Repo erklärt sich selbst und zeigt deine Entscheidungen, nicht nur deinen Code.

### 📚 1. Lernen – 5 Min
Sieh dir zwei gut dokumentierte KI-Repos an und notiere, was sie gut machen.

### 💻 2. Praxis – 45 Min
1. **README:** Demo-GIF ganz oben (Agent arbeitet, HITL-Freigabe, Bericht erscheint)
2. **ARCHITECTURE.md:** Mermaid-Diagramm direkt aus LangGraph exportiert plus Beschreibung jedes Nodes
3. **DECISIONS.md** – mindestens 8 Einträge, darunter:
   - Warum LangGraph und nicht X
   - Warum Supervisor und nicht Einzelagent (oder umgekehrt – mit deinen Zahlen)
   - Warum Model Routing so konfiguriert
   - Warum max. 2 Revisionen
4. **EVALUATION.md:** die A/B/C-Tabelle und die Routing-Ersparnis
5. **LIMITATIONS:** ehrlich, mindestens 5 Punkte

### 🧠 3. Reflexion – 10 Min
**Kontrollfragen:**
1. Welche deiner Entscheidungen würdest du heute anders treffen?
2. Was ist die überzeugendste Zahl in deinem Repo?
3. Welche Limitation wäre für einen Produktiveinsatz der Blocker?

---

## Tag 64 · Samstag – Monatstest 4

**Zeit:** 90 Minuten

### 🧠 Monatstest 4

**Leitfrage: Wie baust du einen Agenten, der nicht in einer Schleife Geld verbrennt?**

Schriftlich in `notes/test-monat-4.md`:

1. Erkläre State, Node, Edge und Reducer in LangGraph – je ein Satz.
2. Was ist ein Checkpointer und welches Produktionsproblem löst er?
3. Nenne fünf Sicherungen gegen Excessive Agency – und ordne sie nach Wirksamkeit.
4. Wann setzt du `interrupt()` ein? Nenne drei konkrete Fälle aus deinem Arbeitsumfeld.
5. Nenne die vier Multi-Agent-Muster und je einen passenden Anwendungsfall.
6. Wann ist ein Einzelagent mit vielen Tools besser als ein Multi-Agent-System?
7. Warum reicht Ergebnis-Evaluation bei Agenten nicht? Nenne zwei Trajektorien-Metriken.
8. Wie senkst du Agent-Kosten um mehr als die Hälfte? Nenne drei Hebel mit geschätzter Wirkung.
9. Ein Agent liefert richtige Ergebnisse, braucht aber 14 statt 4 Schritte. Wie diagnostizierst du das?
10. Erkläre einer fachfremden Person in drei Sätzen, was dein Research Agent tut und wo seine Grenzen sind.

**Praktische Aufgabe (35 Min):**
Baue einen **Workflow** (kein Agent!), der dieselbe Aufgabe löst wie dein Research Agent bei den drei einfachsten Testfragen – mit fest verdrahteten Schritten. Miss Kosten, Latenz und Qualität gegen den Agenten. Schreibe fünf Sätze: Was ist das Ergebnis, und was folgt daraus für deine Architekturentscheidungen?

Diese Aufgabe ist bewusst unbequem. Sehr wahrscheinlich gewinnt der Workflow bei einfachen Fragen deutlich. Das zu wissen und zu akzeptieren ist Expertise.

**Bewertungskriterien:**

| Kriterium | Bestanden, wenn … |
|---|---|
| Sicherheitsdenken | Du nennst Grenzen (Schritte, Kosten, Zeit) als Erstes, nicht als Nachtrag |
| Kostenbewusstsein | Du kannst die Kosten eines Durchlaufs beziffern und aufschlüsseln |
| Angemessenheit | Die praktische Aufgabe führt dich zu einer differenzierten Aussage, nicht zu „Agenten sind besser" |
| Messung | Mindestens fünf Antworten enthalten eine eigene Zahl |

**Bevor du zu Monat 5 weitergehst, solltest du können:**
- Einen LangGraph mit Zustand, Bedingungen, Persistenz und HITL bauen
- Multi-Agent-Muster auswählen und begründen
- Agent-Trajektorien evaluieren
- Agent-Kosten durch Routing deutlich senken

**Wochenreflexion** `reviews/woche-16.md` + Monatsrückblick.
