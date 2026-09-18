## Tag 2

**Kontrollfragen:**
1. Wie hoch war dein deutscher Token-Aufschlag – und was bedeutet das für ein System mit 50.000 deutschen Anfragen pro Monat?
2. Warum kosten Output-Tokens fast immer mehr als Input-Tokens?
3. Welche zwei Textarten produzieren besonders viele Tokens pro Zeichen?

1. Dein deutscher Token-Aufschlag und 50.000 Anfragen

Dein Ergebnis: DE 92 | EN 69 → +33,3% Aufschlag

Annahme: eine Anfrage = 500 Tokens auf Englisch → auf Deutsch ~665 Tokens
Extra-Tokens pro Anfrage: 165 Tokens
Extra-Tokens pro Monat: 165 × 50.000 = 8,25 Mio. extra Tokens

Modell	Mehrkosten/Monat
gemini-3.8-flash ($0.75/1M)	+$6
gpt-5.6-sol ($4/1M)	+$33
claude-opus-5 ($5/1M)	+$41
Konsequenz: Je teurer das Modell, desto mehr lohnt es sich, deutsche Prompts kurz zu halten oder auf Englisch zu prompten und nur das Ergebnis zu übersetzen.



2. Warum kosten Output-Tokens mehr als Input-Tokens?

- Input-Tokens werden parallel verarbeitet — das Modell liest alles auf einmal.

- Output-Tokens werden sequenziell erzeugt — ein Token nach dem anderen, jedes Mal ein vollständiger Modell-Durchlauf. Das kostet deutlich mehr GPU-Rechenzeit. Deshalb sind Output-Preise oft 3–5× höher als Input-Preise.

3. Zwei Textarten mit besonders vielen Tokens pro Zeichen

- Nicht-lateinische Schriften (Chinesisch, Japanisch, Arabisch, Koreanisch) — BPE-Tokenizer wurden hauptsächlich auf englischem Text trainiert, daher zerfallen z.B. chinesische Zeichen in viele Subword-Tokens
- Code — Sonderzeichen wie {, }, =>, Einrückungen und Symbole bekommen oft je einen eigenen Token, obwohl sie nur 1–2 Zeichen lang sind