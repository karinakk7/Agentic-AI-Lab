# Modelllandschaft September 2026

> Preisquellen: [artificialanalysis.ai](https://artificialanalysis.ai) · Stand: September 2026
> Legende: $/1M = US-Dollar pro 1 Million Tokens

| Modell | Anbieter | Input $/1M | Output $/1M | Kontext | Stärke laut Benchmark | Wofür ICH es einsetzen würde |
|---|---|---|---|---|---|---|
| Claude Opus 5 | Anthropic | 5|25 | 1M+ | Höchste Reasoning-Tiefe, Code, komplexe Analyse; Intelligence: 51 – absolute Frontier, sehr stark bei komplexem Reasoning & Coding | Komplexe Probleme, anspruchsvolles Coding, tiefgehende Analysen, schwierige Recherche|
| Claude Fable 5.1 | Anthropic |10 |50 | 1M+ | Balance Speed/Qualität, Coding, strukturierte Ausgaben; Intelligence: 53 – aktuell höchster Intelligence Score, Spitzenleistung bei komplexen Aufgaben | Hochwertiger Allrounder für anspruchsvolle Aufgaben, Coding, Analyse & lange Dokumente|
| GPT-6 Astra | OpenAI | 10| 50 | 1M+ | Multimodal, breite Benchmark-Führung; Intelligence: 53 – gemeinsam mit Fable 5.1 an der Spitze; besonders stark bei professionellen/agentischen Aufgaben |komplexes Reasoning, Multimodalität, Agenten & anspruchsvolle Workflows |
| GPT-5.6 Sol | OpenAI | 4| 20| 1M+| Effizienz, hoher Durchsatz; Intelligence: 47 – sehr starkes Frontier-Modell, gutes Verhältnis aus Leistung und Effizienz |Allround-Aufgaben, Schreiben, Analyse, Coding und tägliche Nutzung |
| Medium 3.5 Pro | Mistral |1.5 |7.5 | 256k |  | Günstige Standardaufgaben, Textverarbeitung, Coding & einfache Analyse|
| Gemini 3.8 Flash | Google | 0.75| 3.75| 1M+ | Schnell, günstig, gut für einfache Tasks | Schnelle und günstige Aufgaben, große Dokumentmengen, Zusammenfassungen & Extraktion|
| DeepSeek V4.1 | Open-Weights | 0.3|1.2 | 1M+| Coding, Mathematik, auf Augenhöhe mit Frontier; Intelligence: 40 – sehr stark für Open Weights; besonders gutes Preis-/Leistungsverhältnis |Coding, Mathematik, technische Aufgaben & günstige Inference |
| Qwen3.8 | Open-Weights (Alibaba) |0.5 |3 | 984k | Multilingual, günstig selbst zu hosten; Intelligence: 40 (Qwen3.8 2.4T A95B) – starkes Open-Weights-Modell, besonders interessant für günstige/selbst betriebene Anwendungen | Multilinguale Aufgaben, Self-Hosting, eigene AI-Anwendungen & günstige Inference | 

---

## Meine Einschätzung

Wenn ich heute ein Projekt starten müsste, würde ich mit GPT-5.6 Sol anfangen, weil es ein sehr gutes Verhältnis aus Qualität, Kosten und Geschwindigkeit bietet. Wechseln würde ich zu Claude Opus 5, wenn die Aufgaben deutlich komplexer werden und ich mehr Reasoning- oder Coding-Leistung brauche.

| Modell                     | „Wenn ich heute ein Projekt starten müsste …“                                                                                                                                                                                                                                   |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Claude Opus 5**          | … würde ich damit anfangen, wenn **Qualität und Reasoning wichtiger sind als Kosten**. Wechseln würde ich zu einem günstigeren Modell, wenn **die Aufgaben einfacher oder die Anzahl der Anfragen sehr hoch wird**.                                                             |
| **Claude Fable 5.1**       | … würde ich damit anfangen, wenn ich **einen sehr leistungsfähigen Allrounder für komplexe Aufgaben** brauche. Wechseln würde ich zu einem günstigeren Modell, wenn **die zusätzliche Qualität den höheren Preis nicht rechtfertigt**.                                          |
| **GPT-6 Astra**            | … würde ich damit anfangen, wenn ich **ein möglichst vielseitiges High-End-Modell für unterschiedliche Aufgaben** brauche. Wechseln würde ich zu einem spezialisierten oder günstigeren Modell, wenn **Kosten, Geschwindigkeit oder ein bestimmter Use Case wichtiger werden**. |
| **GPT-5.6 Sol**            | … würde ich damit anfangen, wenn ich **ein gutes Verhältnis aus Leistung, Geschwindigkeit und Kosten** möchte. Wechseln würde ich zu einem stärkeren Modell, wenn **komplexes Reasoning oder anspruchsvolles Coding zum Flaschenhals wird**.                                    |
| **Mistral Medium 3.5 Pro** | … würde ich damit anfangen, wenn **Kosten eine wichtige Rolle spielen, aber ich trotzdem ein leistungsfähiges Modell möchte**. Wechseln würde ich zu einem Frontier-Modell, wenn **komplexere Aufgaben die Qualitätsgrenze erreichen**.                                         |
| **Gemini 3.8 Flash**       | … würde ich damit anfangen, wenn **Geschwindigkeit, niedrige Kosten und große Kontextmengen** entscheidend sind. Wechseln würde ich zu einem stärkeren Modell, wenn **tieferes Reasoning benötigt wird**.                                                                       |
| **DeepSeek V4.1**          | … würde ich damit anfangen, wenn **Coding/Mathematik wichtig sind und ich ein sehr günstiges Open-Weight-Modell möchte**. Wechseln würde ich zu einem Frontier-Modell, wenn **maximale Qualität oder komplexere allgemeine Aufgaben gefragt sind**.                             |
| **Qwen3.8**                | … würde ich damit anfangen, wenn **Open Weights, Self-Hosting oder Multilingualität** wichtig sind. Wechseln würde ich zu einem proprietären Frontier-Modell, wenn **maximale Modellleistung wichtiger ist als Kontrolle und Hosting-Flexibilität**.                            |



---

## Notizen aus der Recherche



<!-- Hier stichpunktartig festhalten, was auf artificialanalysis.ai auffällt -->

## Reflexion
1. Welches Modell würdest du für die Klassifikation von 100.000 Support-Tickets wählen – und warum nicht das beste?

Ich würde Gemini 3.8 Flash bzw. generell ein schnelles, günstiges Modell wählen. Warum? 100.000 Tickets sind eine sehr große Anzahl an Requests. Für Klassifikation braucht man i.d.R kein maximales Reasoning. Hier geht's es darum Geschwindigkeit zu erhöhen und Kosten pro Reduktion zu verringern.
Wenn das Modell hingegen deutlich teurer ist, aber bei einfachen Klassifkationsaufgaben nur geringfügig besser abschneidet, ist es wirtschaftlich nicht Sinnvoll 

2. Was bedeutet ein 1-Mio-Token-Kontextfenster in Seiten Text, und was kostet es einmal zu füllen?

1 Token ~ 0.75 Wörter bei englischem Text d.h. 1.000.000 Tokens ~ 750.000 Wörter
$5 pro 1 Mio. Input-Tokens

Dann kostet das einmalige Einspeisen von 1 Mio. Tokens:

1.000.000 × $5 / 1.000.000 = $5
1 Mio. Tokens Kontext → $5 Input-Kosten


3. Welche Eigenschaft eines Modells kann ein Benchmark grundsätzlich nicht messen?
Wie gut das Modell in der realen Anwendung tatäschlich abschneidet

Benchmarks können beispielsweise Reasoning, Coding, Mathematik, Wissen oder bestimmte Aufgaben messen.

- Wie zuverlässig das Modell in deinem konkreten Workflow ist
- Wie gut es mit deinen echten Daten funktioniert
- Wie viele Fehler es im produktiven Betrieb macht
- Wie gut Nutzer die Antworten tatsächlich finden
- Wie gut es sich in deine Systeme und Prozesse integrieren lässt
- Wie hoch die tatsächlichen Kosten und Latenzen in deinem Setup sind
- Wie gut es mit ungewöhnlichen Edge Cases umgeht

Ein Benchmark misst eine definierte Testaufgabe – aber nicht automatisch den Business Value eines Modells.