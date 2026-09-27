# Review Woche 2 – Structured Outputs & Repair-Loop

## Kontrollfragen

---

### 1. Wie viele Ausgaben waren schema-valide, aber inhaltlich falsch? Was sagt das über Structured Outputs als Qualitätsmaßnahme?

Bei meinem Testlauf waren alle 8 Ausgaben schema-valide – aber das ist gerade der Punkt.
Schema-Validität beantwortet nur: *Ist das JSON korrekt formatiert und entspricht es den Feldtypen?*
Sie beantwortet nicht: *Stimmt der Inhalt mit dem Quelltext überein?*

In meinem Lauf gab es mindestens zwei inhaltlich fragwürdige Stellen:

- Bei Vertragsauszug 5 (Büromaterial Zentral) fehlte der Vertragsbeginn im Text. Das Modell
  hat `vertragsbeginn: null` korrekt zurückgegeben – gut. Aber die `begruendung` enthielt
  Formulierungen, die so nicht im Text standen. Schema-valide, inhaltlich ausgedacht.
- Bei Vertragsauszug 3 (Eastern Components) hat das Modell in einem `zitat` „70 %" zitiert –
  das stand tatsächlich im Text. In einem anderen Zitat aber war die Formulierung eine
  Paraphrase, kein wörtliches Zitat.

**Fazit:** Structured Outputs lösen das *Parsing-Problem*, nicht das *Halluzinations-Problem*.
Das Modell kann jedes Feld mit plausiblem, aber erfundenem Inhalt füllen und trotzdem 100 %
schema-valide sein. Structured Outputs sind eine notwendige, aber keine hinreichende
Qualitätsmaßnahme. Sie machen Ausgaben maschinell verarbeitbar – die inhaltliche Richtigkeit
muss durch Prompting (Few-Shot, Chain-of-Thought, Retrieval) oder durch externe Prüfung
(genau das, wofür `zitate` gedacht sind) sichergestellt werden.

---

### 2. Warum sind `Literal`-Typen für Kategorien besser als freier Text mit der Anweisung „wähle eines von drei"?

Weil der Unterschied auf zwei Ebenen wirkt: **vor** dem Modell und **nach** dem Modell.

**Vor dem Modell (im Schema):** Pydantics `model_json_schema()` übersetzt
`Literal["niedrig", "mittel", "hoch"]` in `"enum": ["niedrig", "mittel", "hoch"]`.
Dieses Enum landet in der Tool-Definition, die Anthropic auf Token-Ebene erzwingt.
Das Modell kann physisch nicht „mittel-hoch", „eher mittel" oder das englische „medium"
ausgeben – der Constraint sitzt im Decoder, nicht im Prompt.

**Nach dem Modell (Validierung):** Pydantic wirft bei jeder Abweichung einen `ValidationError`.
Bei freiem Text wäre `risikostufe = "Mittel"` (Großschreibung) oder `"niedrig bis mittel"`
syntaktisch kein Fehler – und würde im Code stillschweigend zu einem falschen Ergebnis führen.

**Zusätzlich:** Der Prompt wird kürzer. Ich muss nicht schreiben „Wähle genau einen der drei
Werte: niedrig, mittel, hoch. Keine anderen Formulierungen." – das Schema sagt das bereits.
Weniger Prompt-Text bedeutet weniger Spielraum für Fehler und weniger Input-Tokens.

Die Faustregel: Wenn eine Kategorie im Downstream-Code ausgewertet wird (if/switch/match),
immer `Literal` oder Enum – nie freien Text.

---

### 3. Wann ist ein Repair-Loop teurer als ein besserer Prompt?

Der Repair-Loop kostet bei jedem ausgelösten Fehler:
- **2× API-Calls** (Original + Repair) mit der vollen Konversationsgeschichte
- **2× Latenz** – der Nutzer wartet auf zwei sequenzielle Round-Trips
- Für lange Kontexte: **quadratische Tokenkosten**, weil die Repair-Anfrage die gesamte
  bisherige Konversation trägt

Ein besserer Prompt kostet einmalig Entwicklungszeit, danach nichts.

Der Repair-Loop wird teurer, wenn:

1. **Die Fehlerrate hoch ist (>20–30 %).** Wenn jeder dritte Call repariert werden muss,
   zahle ich im Schnitt 1,3× die normalen Kosten. Bei 50 % Fehlerrate kostet derselbe
   Durchsatz fast doppelt so viel. Ein besserer Prompt, der Fehler auf <5 % senkt, amortisiert
   sich nach wenigen hundert Calls.

2. **Der Fehler systematisch ist.** Wenn immer dasselbe Feld scheitert (z. B. das Modell
   gibt `begruendung` regelmäßig zu lang zurück), ist der Prompt die Ursache – der
   Repair-Loop behandelt das Symptom. Hier ist ein klarerer Constraint im Prompt
   oder ein Few-Shot-Beispiel die richtige Antwort.

3. **Latenz kritisch ist.** In einem synchronen User-Flow (Nutzer wartet auf Antwort)
   kann ein zweiter sequenzieller Call die empfundene Qualität stärker senken als ein
   gelegentliches Parsing-Problem.

Der Repair-Loop macht Sinn, wenn:

- Fehler **selten und unvorhersehbar** sind (ungewöhnliche Inputs, Grenzfälle)
- Die Alternative ein sehr langer oder komplexer Prompt wäre, der Kosten und
  Latenz ohnehin erhöht
- Das Scheitern ansonsten einen **harten Crash** bedeutet, den der Nutzer direkt sieht

**Meine Heuristik:** Unter 5 % Fehlerrate → Repair-Loop behalten, Prompt nicht anfassen.
Über 10 % bei ähnlichen Inputs → Prompt zuerst verbessern, Repair-Loop als letzte Absicherung.
