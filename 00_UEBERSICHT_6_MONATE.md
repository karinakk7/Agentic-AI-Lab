# KI-Expertin in 6 Monaten – Übersicht & Betriebsanleitung

**Erstellt:** 13. September 2026
**Für:** Data Science / Wirtschaftsinformatik-Hintergrund, Vollzeitjob, 4 Lerntage pro Woche
**Prinzip:** 1%-Methode – klein, regelmäßig, praktisch, aufeinander aufbauend

---

## 0. Was sich gerade geändert hat (Stand 13.09.2026)

Damit du weißt, warum der Plan so aussieht, wie er aussieht – das sind die Dinge, die seit ca. 12 Monaten anders sind:

| Bereich | Stand heute | Konsequenz für den Plan |
|---|---|---|
| **Modelllandschaft** | Frontier: GPT-6 Astra, GPT-5.6 Sol/Terra, Claude Fable 5.1, Claude Opus 5, Gemini 3.1 Pro / 3.8 Flash, Grok 4.5. Open-Weights (MiniMax M2.5, GLM-5.x, Kimi K2.5, DeepSeek V4.1, Qwen3.8) haben beim Coding stark aufgeholt. API-Preise sind seit 2025 um grob 80 % gefallen. | Kein Modell gewinnt überall. **Model Routing** statt „Lieblingsmodell" ist die Kernkompetenz – ist in Monat 1 und Monat 4 eingebaut. |
| **RAG** | Naive RAG (embed → top-k → generieren) gilt als Prototyp, nicht als Architektur. Produktionsstandard: **Hybrid Search (dense + BM25, fusioniert per RRF) + Cross-Encoder-Reranker**. Darüber: Agentic RAG, GraphRAG, Adaptive RAG. | Monat 2 baut bewusst erst die Baseline und dann jede Verbesserung **messbar** obendrauf. Keine Tutorials aus 2023. |
| **MCP** | Die Spec **2026-07-28** ist da: stateless Protokoll-Kern, Extensions-Framework (Tasks, MCP Apps, Enterprise Managed Authorization), Multi-Round-Trip-Requests statt dauerhafter SSE-Streams, Abkehr von Dynamic Client Registration. **Roots, Sampling und Logging sind deprecated.** | Monat 5 arbeitet gegen die aktuelle Spec. Alle MCP-Tutorials von vor Sommer 2026 sind an entscheidenden Stellen veraltet – das ist explizit ein Lerntag. |
| **Agent-Frameworks** | Konvergenz: Praktisch jedes Framework spricht MCP für Tools. LangGraph (durable state, HITL), OpenAI Agents SDK (schlank), Claude Agent SDK (Code/Dateien), Microsoft Agent Framework (Azure/Enterprise), Pydantic AI, smolagents. | Du lernst **ein** Framework tief (LangGraph) und portierst einmal in ein zweites. Framework-Sammeln bringt nichts. |
| **Evaluation & Observability** | Ist erwachsen geworden und OpenTelemetry-basiert (`gen_ai.*` Semantic Conventions). Ragas (RAG), DeepEval (Agents, CI), Langfuse / Arize Phoenix / MLflow (Tracing). | Evaluation kommt in Monat 3 – **vor** den Agenten, nicht danach. Das ist Absicht. |
| **Security** | OWASP Top 10 for LLM Apps **2026**: Prompt Injection und Sensitive Information Disclosure weiter auf 1 und 2, **Excessive Agency von Platz 6 auf 3 gesprungen**. Dazu die eigene OWASP Top 10 for Agentic Applications (ASI01 Goal Hijack, ASI02 Tool Misuse, ASI03 Privilege Abuse …). | Security ist kein Anhang, sondern Woche 19–20 mit eigenem Angriffs-/Verteidigungs-Praxisteil. |
| **Microsoft** | „Azure AI Foundry" heißt inzwischen **Microsoft Foundry**; Foundry IQ ist die Knowledge-/RAG-Schicht, Foundry Agent Service + Microsoft Agent Framework die Agent-Schicht. | Relevant für dein Azure-Profil – aber konzeptionell, nicht als Klickstrecke. |

> **Hinweis zu Links:** Alle Links sind offizielle Quellen, die ich bei der Recherche am 13.09.2026 verwendet habe. KI-Dokumentationen werden häufig umstrukturiert. Wenn ein Deep-Link ins Leere läuft: über die Suche der jeweiligen Seite nach dem Modulnamen suchen. Ich habe bewusst überwiegend stabile Einstiegsseiten verlinkt statt fragiler Unterseiten.

---

## 1. Dein Wochenrhythmus

| Tag | Dauer | Was |
|---|---|---|
| **Montag** | 60 Min | Lerntag 1 + heise KI Update (im Training) → **Discover**: 1 Entwicklung notieren |
| **Dienstag** | 0 | frei |
| **Mittwoch** | 60 Min | Lerntag 2 + heise KI Update → **Understand**: 1 Technologie 10 Min recherchieren |
| **Donnerstag** | 60 Min | Lerntag 3 |
| **Freitag** | 15 Min | heise KI Update → **Wochenreflexion** (Template unten). Kein Lerntag. |
| **Samstag** | 60–90 Min | Build-Session (die längere, optionale Einheit) |
| **Sonntag** | 0 | **komplett frei** – nicht verhandelbar |

**Gesamt: ca. 4 Std. aktiv pro Woche + Podcast im Training.** Über 24 Wochen sind das rund 100 fokussierte Stunden – das entspricht grob einem guten Universitätsmodul, aber mit 100 % Praxisanteil im Bauen.

**Die Regeln der 1%-Methode für dich:**

1. **Minimum-Version ist erlaubt.** An einem schlechten Tag: nur die 20 Minuten „Lernen", Praxis verschieben. Kette nicht abreißen lassen schlägt Intensität.
2. **Nie zwei Tage hintereinander ausfallen lassen.** Ein Tag ist Leben, zwei Tage sind ein Trend.
3. **Jeder Lerntag endet mit einem Commit.** Auch wenn es nur eine Notiz in `notes/` ist. Der Commit ist der sichtbare Beweis des 1 %.
4. **Puffer ist eingeplant.** In jedem Monat ist der letzte Samstag Review + Test, kein neuer Stoff. Wenn du hinterherhinkst, ist das dein Aufholtag.
5. **Wenn eine Woche komplett ausfällt:** nicht aufholen, sondern einfach eine Woche nach hinten schieben. Der Plan ist eine Reihenfolge, kein Kalender.

---

## 2. Die Phasenlogik der 6 Monate

```
Monat 1  LLM Engineering      →  Du beherrschst die Schicht direkt am Modell
Monat 2  RAG                  →  Du bringst eigenes Wissen ins Modell
Monat 3  Evaluation + Agents  →  Du kannst MESSEN, ob es gut ist (bevor es komplex wird)
Monat 4  Agents & Orchestr.   →  Du baust Systeme, die selbst handeln
Monat 5  MCP + Security       →  Du baust die Werkzeugschicht – und sicherst sie ab
Monat 6  Production + Capstone→  Du baust und dokumentierst ein Enterprise-System
```

**Warum Evaluation schon in Monat 3 und nicht ganz am Ende (Abweichung von deiner Gliederung):** Der häufigste Fehler beim Agentenbau ist, dass man Komplexität hinzufügt, ohne messen zu können, ob sie hilft. Wenn du in Monat 4 Multi-Agent-Systeme baust, ohne eine Eval-Suite zu haben, optimierst du nach Bauchgefühl. Deshalb: erst messen lernen, dann komplex werden. Der Rest der Production-Themen (Observability-Tiefe, Cost, Caching, Governance) bleibt in Monat 6, wo er hingehört.

---

## 3. Deine 5 Projekte

Alle Projekte bauen aufeinander auf. Projekt 2 liefert den Retriever für Projekt 3; Projekt 4 liefert die Tools für den Capstone.

| # | Repo | Monat | Was es beweist |
|---|---|---|---|
| 1 | `llm-playground` | 1 | Du verstehst die Modellschicht: Prompting, Structured Outputs, Tool Calling, Kosten, Modellvergleich |
| 2 | `ai-knowledge-assistant` | 2–3 | Du baust produktionsnahe Retrieval-Systeme und **evaluierst sie** |
| 3 | `ai-research-agent` | 4 | Du baust Agenten mit State, Tools, HITL und Multi-Agent-Struktur |
| 4 | `mcp-toolbelt` | 5 | Du baust die Werkzeugschicht selbst – gegen die aktuelle Spec, mit Threat Model |
| ★ | `vendor-risk-copilot` | 6 | Capstone: Enterprise-System, das alles kombiniert |

### Capstone-Szenario: Vendor & Compliance Risk Copilot

Gewählt, weil es zu deinem Profil (Wirtschaftsinformatik + Business Analysis + Azure) passt und technisch alle Bausteine erzwingt:

> Ein Assistent für ein Einkaufs-/Compliance-Team. Er beantwortet Fragen zu Lieferantenverträgen und internen Richtlinien, prüft einen neuen Lieferanten gegen interne Policies, zieht externe Informationen (Web, Register) über Tools hinzu, erstellt einen strukturierten Risikobericht mit Quellenangaben – und eskaliert an einen Menschen, bevor er etwas Verbindliches ausgibt.

```
User
 ↓
Router (einfach → klein/günstig | komplex → Agent)
 ↓
Agent (LangGraph, durable state)
 ├→ RAG-Tool        (Verträge/Policies, hybrid + rerank, mit Zitaten)
 ├→ MCP-Server      (eigene Tools: SQL read-only, Dateisuche, Rechner)
 └→ External APIs   (Websuche)
 ↓
Guardrails (Input/Output-Filter, Schema-Validierung, Allow-Lists)
 ↓
Human-in-the-Loop (Freigabe vor finalem Bericht)
 ↓
Evaluation (CI-Gate) + Observability (Traces, Kosten, Latenz)
```

---

## 4. Deine News-Routine (max. 5 Quellen)

**Behalte den heise KI Update Podcast – aber gib jeder Folge eine Rolle:**

| Tag | Rolle | Zeitaufwand |
|---|---|---|
| **Montag** | **Discover** – nach dem Training 1 Satz in `radar.md`: Was ist die wichtigste Entwicklung? | 3 Min |
| **Mittwoch** | **Understand** – eine Technologie aus dem Radar auswählen, 10 Min Primärquelle lesen (nicht den Podcast, nicht LinkedIn – die offizielle Ankündigung) | 10 Min (Teil des Lerntags) |
| **Freitag** | **Reflect** – Wochenreflexion, Radar-Einträge auf Ampel setzen | 15 Min |

**Deine 5 Quellen – mehr brauchst du nicht:**

1. **heise KI Update** – Mo/Mi/Fr im Training. Deine Breitensicht, deutschsprachig, gut kuratiert.
2. **Anbieter-Primärquellen (1× pro Woche, 10 Min gebündelt):** OpenAI Changelog (`platform.openai.com/docs/changelog`), Anthropic Release Notes (`docs.claude.com`), Google DeepMind Blog, Microsoft Foundry Docs „What's new". → Nur das lesen, was ein Radar-Eintrag ausgelöst hat.
3. **Hugging Face** – `huggingface.co/blog` und Daily Papers. 1× pro Woche 10 Min. Dein Fenster in Open Source.
4. **Artificial Analysis** (`artificialanalysis.ai`) – 1× pro Monat. Benchmarks, Preise, Latenz an einem Ort. Deine Grundlage für Modellentscheidungen.
5. **Engineering-Blogs** – Anthropic Engineering (`anthropic.com/engineering`) und OpenAI Cookbook (`cookbook.openai.com`). 1× pro Monat. Das ist der Unterschied zwischen „kennt die News" und „weiß, wie man es baut".

**Bewusst nicht auf der Liste:** LinkedIn-KI-Influencer, Twitter/X-Threads, YouTube-„Breaking News"-Kanäle, tägliche Newsletter. Die kosten überproportional Zeit und liefern fast ausschließlich Sekundärinformation.

### Der Relevanzfilter: 3 Fragen + Ampel

Wenn dir eine neue Technologie begegnet, stelle **drei Fragen**:

1. **Ändert es, wie ich baue?** (Neue Fähigkeit vs. nur bessere Benchmark-Zahl)
2. **Betrifft es eine Schicht, in der ich arbeite?** (Modell / Retrieval / Orchestrierung / Tools / Betrieb)
3. **Könnte ich es in unter 60 Minuten selbst testen?**

**Ampel:**

- 🔴 **Rot** – 0 von 3 Ja. Nicht notieren, nicht merken. Beispiel: Ein Modell verbessert einen Benchmark um 1,2 Punkte.
- 🟡 **Gelb** – 1–2 von 3 Ja. Eine Zeile in `radar.md` mit Datum und Link. Nicht weiter verfolgen. Monatlich Radar durchgehen: Was steht nach 4 Wochen immer noch da und ist jetzt wichtiger geworden? Nur das kommt in Grün.
- 🟢 **Grün** – 3 von 3 Ja. **Nächste Samstags-Session einplanen.** Durchlaufe den vollen Loop:

```
Discover  → 1 Zeile: was und wo (Primärquelle)
Understand→ Welches Problem löst es? Was ist die Alternative ohne diese Technologie?
Test      → Kleinster Test, der eine Antwort gibt. 45 Min Deckel.
Evaluate  → Besser als mein bisheriger Ansatz? Woran gemessen? Kosten/Latenz?
Document  → 5 Sätze in notes/tech-radar/. Entscheidung: adoptieren / beobachten / verwerfen.
```

**Der wichtigste Teil ist „Evaluate":** Die meisten Menschen bleiben bei „Understand" stehen und verwechseln das mit Expertise. Nach 6 Monaten sollst du zu jeder Technologie sagen können: *„Ich habe es getestet, hier ist die Zahl, und deshalb nutze ich es (nicht)."*

---

## 5. Wöchentliche Review (Freitag, 15 Min)

Lege `reviews/woche-XX.md` an, Template:

```markdown
# Woche XX

## Gelernt (3–5 Punkte)
-

## Gebaut (1 Punkt – was läuft jetzt, das vorher nicht lief)
-

## Neue KI-Technologie (1 Punkt, aus dem Radar)
- Technologie:
- Ampel: 🔴 / 🟡 / 🟢
- Entscheidung:

## Noch unklar (1–3 Punkte)
-

## Nächste Woche – konkretes Ziel (1 Satz)
-

## Ehrlichkeits-Check
Lerntage geschafft: __ / 4
Wenn < 3: Was war der Grund, und was streiche ich nächste Woche?
```

Der letzte Abschnitt ist wichtiger als er aussieht. Wenn du zwei Wochen hintereinander unter 3 Tagen liegst, ist nicht deine Disziplin das Problem, sondern der Plan – dann kürze den Stoff, nicht den Schlaf.

---

## 6. MUST / SHOULD / NICE pro Monat

Das ist dein Prioritätenfilter. Wenn die Zeit knapp wird, streichst du **von unten nach oben**.

### Monat 1 – LLM Engineering
- **MUST:** Tokenisierung & Kostenrechnung, Prompt-Struktur, Structured Outputs (JSON Schema), Tool Calling + Tool-Loop, Modellauswahl nach Aufgabe
- **SHOULD:** Prompt Caching, Reasoning-Effort bewusst steuern, Streaming, Parameter (temperature/seed) verstehen
- **NICE TO KNOW – aktuell nicht priorisieren:** Fine-Tuning, Batch-APIs, multimodale Video-Inputs, Embedding-Modelle selbst trainieren

### Monat 2 – RAG
- **MUST:** Chunking-Strategien, Hybrid Search + RRF, Cross-Encoder-Reranking, Grounding mit Zitaten, Retrieval-Metriken (Recall@k, MRR, nDCG)
- **SHOULD:** Query-Rewriting/Multi-Query, Contextual Retrieval, Metadaten-Filter, Adaptive Routing (retrieval ja/nein)
- **NICE TO KNOW – aktuell nicht priorisieren:** GraphRAG produktiv bauen (Konzept reicht), eigene Embedding-Modelle finetunen, exotische Vector DBs vergleichen, ColBERT/Late Interaction

### Monat 3 – Evaluation & Agent-Grundlagen
- **MUST:** Faithfulness / Answer Relevancy / Context Precision & Recall, LLM-as-a-Judge inkl. seiner Schwächen, Testset-Aufbau, Agent-Loop from scratch, Workflow vs. Agent entscheiden
- **SHOULD:** Synthetische Testsets, Tracing-Grundlagen (OTel `gen_ai.*`), Eval im CI, Memory-Strategien
- **NICE TO KNOW – aktuell nicht priorisieren:** Human-Annotation-Workflows, Drift Detection, Eval-Plattform-Vergleiche im Detail

### Monat 4 – Agents & Orchestrierung
- **MUST:** LangGraph (State, Nodes, Conditional Edges, Checkpointer), Tool-Design, Fehlerbehandlung & Budget-Limits, Human-in-the-Loop, Supervisor-Pattern
- **SHOULD:** Framework-Vergleich mit Entscheidungsmatrix, Agent-Trajektorien bewerten, Model Routing zur Kostensenkung
- **NICE TO KNOW – aktuell nicht priorisieren:** A2A-Protokoll im Detail, Agent-Marktplätze, Swarm-/Blackboard-Architekturen, Voice-Agents

### Monat 5 – MCP & Security
- **MUST:** MCP-Architektur (Host/Client/Server, Tools/Resources/Prompts), eigener Server + eigener Client, Spec 2026-07-28 (stateless, Extensions, MRTR, Deprecations), OWASP LLM Top 10 2026, indirekte Prompt Injection praktisch, Guardrails, Least Privilege
- **SHOULD:** Elicitation, Tasks-Extension, MCP-Authorization, Red-Teaming mit promptfoo
- **NICE TO KNOW – aktuell nicht priorisieren:** MCP Apps UI-Extension, Enterprise Managed Authorization im Detail, eigenen MCP-Gateway bauen

### Monat 6 – Production & Capstone
- **MUST:** Architektur entwerfen und begründen, Eval-Suite als CI-Gate, Tracing + Kostenüberblick, Caching, Dokumentation, mündlich erklären können
- **SHOULD:** Semantic Caching, Model Routing produktiv, EU AI Act Grobeinordnung, Model Card, lokale LLMs mit Ollama
- **NICE TO KNOW – aktuell nicht priorisieren:** Eigenes Deployment auf Kubernetes, Quantisierung, GPU-Serving, Multi-Region-Setups

---

## 7. GitHub-Struktur (für jedes Projekt gleich)

```
projektname/
├── README.md
├── ARCHITECTURE.md          ← Mermaid-Diagramm + Komponentenbeschreibung
├── DECISIONS.md             ← ADRs: Entscheidung, Alternativen, Begründung, Datum
├── EVALUATION.md            ← Metriken, Testset, Ergebnisse, Baseline vs. jetzt
├── .env.example
├── requirements.txt
├── src/
│   ├── config.py
│   └── ...
├── eval/
│   ├── testset.jsonl
│   └── run_eval.py
├── notes/                   ← deine Lernnotizen, bewusst öffentlich
└── tests/
```

### README-Struktur (in dieser Reihenfolge)

```markdown
# Projektname
Ein-Satz-Beschreibung: was es tut und für wen.

## Demo
Screenshot oder GIF. Zuerst, nicht zuletzt.

## Problem
Welches konkrete Problem löst das? 3 Sätze.

## Architektur
Mermaid-Diagramm + 5 Sätze Datenfluss.

## Setup
Kopierbare Befehle. Getestet auf: ...

## Technische Entscheidungen
| Entscheidung | Alternative | Warum diese |
|---|---|---|

## Evaluation
Was gemessen, womit, Baseline → aktuell. Mit Tabelle.

## Limitations
Ehrlich. Das ist der Abschnitt, den erfahrene Leute zuerst lesen.

## Mögliche Verbesserungen
Priorisiert, mit geschätztem Aufwand.
```

**Der Abschnitt „Limitations" ist dein stärkstes Signal.** Ein Repo, das offen sagt „Reranking bringt bei kurzen Dokumenten nichts, bei unserem Testset +18 % MRR, aber +140 ms Latenz" zeigt mehr Expertise als jedes Zertifikat.

### Commit-Rhythmus

- Jeder Lerntag → mindestens 1 Commit (auch nur Notizen)
- Commit-Nachrichten im Stil `feat: hybrid retrieval mit RRF` / `docs: eval-ergebnisse woche 6` / `chore: notizen tag 23`
- Samstags → Push + kurze Ergänzung im README

---

## 8. Die 6 Monatstests

Am letzten Samstag jedes Monats. Jeweils ca. 60–90 Minuten. Die vollständigen Fragen, Aufgaben und Bewertungskriterien stehen am Ende der jeweiligen Monatsdatei.

| Monat | Leitfrage |
|---|---|
| 1 | Wann setzt du welches LLM ein – und was kostet das? |
| 2 | Warum funktioniert dein RAG-System schlecht und wie verbesserst du es? |
| 3 | Woran erkennst du objektiv, dass dein System besser geworden ist? Und: Wann braucht man einen Agent – und wann nicht? |
| 4 | Wie baust du einen Agenten, der nicht in einer Schleife Geld verbrennt? |
| 5 | Erkläre MCP nach der aktuellen Spec und baue einen sicheren Server. |
| 6 | Entwirf und verteidige eine vollständige Enterprise-AI-Architektur. |

**Die Regel für alle Tests:** Du bestehst nicht, wenn du die Antwort kennst. Du bestehst, wenn du sie **jemandem ohne KI-Hintergrund in 3 Minuten erklären** kannst und **die Zahl aus deinem eigenen Projekt** nennst, die deine Aussage belegt.

---

## 9. Setup vor Tag 1 (einmalig, ca. 45 Min – mach das an einem Sonntagabend)

```bash
mkdir ki-expertin && cd ki-expertin
git init
python -m venv .venv && source .venv/bin/activate
pip install python-dotenv httpx pydantic rich jupyter
```

**Accounts / Keys, die du brauchst (alle mit kostenlosem Kontingent oder geringen Kosten):**

- Anthropic API (`console.anthropic.com`) – Startguthaben
- OpenAI API (`platform.openai.com`) – geringes Guthaben aufladen, du wirst über 6 Monate wahrscheinlich unter 30 € bleiben
- Google AI Studio (`aistudio.google.com`) – großzügiges kostenloses Kontingent, gut für Experimente
- Hugging Face Account – kostenlos, für Modelle und Kurse
- GitHub Account – Repos öffentlich

**Kostenrealität, damit dich nichts überrascht:** Wenn du diszipliniert mit kleinen Modellen für Experimente arbeitest und nur für echte Vergleiche Frontier-Modelle nutzt, liegen die gesamten API-Kosten über 6 Monate erfahrungsgemäß im Bereich **20–50 €**. Das Kostenbewusstsein selbst ist Teil des Lernziels – du misst ab Tag 2 jeden Call.

**Ordner für deinen Kopf:**

```bash
mkdir -p notes/tech-radar reviews
touch radar.md
```

---

## 10. Die Dateien dieses Plans

- `00_UEBERSICHT_6_MONATE.md` ← du bist hier
- `MONAT_1_LLM_ENGINEERING.md` – Woche 1–4, Tag 1–16
- `MONAT_2_RAG.md` – Woche 5–8, Tag 17–32
- `MONAT_3_EVALUATION_UND_AGENTS.md` – Woche 9–12, Tag 33–48
- `MONAT_4_AGENTS_UND_ORCHESTRIERUNG.md` – Woche 13–16, Tag 49–64
- `MONAT_5_MCP_UND_SECURITY.md` – Woche 17–20, Tag 65–80
- `MONAT_6_PRODUCTION_UND_CAPSTONE.md` – Woche 21–24, Tag 81–96

Fang am nächsten Montag an. Nicht heute, nicht „wenn das Projekt auf der Arbeit ruhiger wird".
