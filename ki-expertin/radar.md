# My Personalized notes: 
# Week 1

heise KI Update – Mo/Mi/Fr im Training. Deine Breitensicht, deutschsprachig, gut kuratiert. Zusätzlich: Matt Wolfe – AI News (YouTube), wöchentliches englischsprachiges Update zu den wichtigsten KI-Entwicklungen.
Anbieter-Primärquellen (1× pro Woche, 10 Min gebündelt): OpenAI Changelog (platform.openai.com/docs/changelog), Anthropic Release Notes (docs.claude.com), Google DeepMind Blog, Microsoft Foundry Docs „What's new". → Nur das lesen, was ein Radar-Eintrag ausgelöst hat.
Hugging Face – huggingface.co/blog und Daily Papers. 
Artificial Analysis (artificialanalysis.ai) 
Engineering-Blogs – Anthropic Engineering (anthropic.com/engineering) und OpenAI Cookbook (cookbook.openai.com).

## KI Heise Update 14.09
- Entschleunigung der KI-Entwicklung: Zunehmende Diskussionen darüber, die Entwicklung von KI stärker zu regulieren und zu verlangsamen.

- Claude: Berichte über Sicherheitsvorfälle, bei denen KI-Modelle Ziel von Angriffen oder Manipulationsversuchen wurden.

- Ray-Ban AI-Brillen: Gesichtserkennung ist technisch möglich. Das Aufnahme-Warnlicht ist bei Tageslicht nur schwer erkennbar, was Datenschutzbedenken aufwirft. Zudem stellt sich die Frage nach der Haftung im Rahmen der DSGVO.

- Apple und Siri-Daten: Apple nutzt persönliche Siri-Daten für das Training von KI-Funktionen. Zudem wird diskutiert, dass die Apple Watch dauerhaft mithören könnte, um parallel Transkripte zu erstellen.

- Urheberrechtskontroverse in der Mathematik: Streit um wissenschaftliche Urheberschaft, da ein noch unveröffentlichtes KI-Modell als Grundlage für mathematische Forschung gedient haben soll. Mehrere Mathematiker arbeiteten gleichzeitig an ähnlichen Forschungsrichtungen, was die Zuordnung von Ideen erschwert.

- Gemini für Windows: Google bringt Gemini als eigenständige Desktop-App für Windows. Die Anwendung fungiert sowohl als Chatbot als auch als KI-Agent und integriert zudem Gemini Nano für lokale KI-Funktionen auf dem Gerät.

## Microsoft- What's new?
### Foundry Agent Service

1. Der Artikel erklärt, wie sich die Kosten von Optimierungsjobs im Foundry Agent Service abschätzen und nachvollziehen lassen.

* Vor dem Start werden Kostenprognosen für Prompt-Agents angezeigt (Minimum, Schätzung und Maximum).

* Die Schätzung basiert unter anderem auf der Anzahl der Kandidaten und den Zeilen des Evaluierungsdatensatzes.

* Nach dem Lauf werden die tatsächlich verbrauchten Tokens und die realen Kosten für Prompt- und Hosted-Agents angezeigt.

* Die Prognosen dienen nur der Planung, da die endgültigen Kosten je nach tatsächlichem Tokenverbrauch und Ablauf der Optimierung abweichen können.



2. Der Artikel beschreibt den Lebenszyklus eines Azure Autopiloten – von der Bereitstellung bis zur Stilllegung – sowie die Verantwortlichkeiten der beteiligten Rollen.

* Der Lebenszyklus umfasst die Bereitstellung der Infrastruktur, das Erstellen und Veröffentlichen von Blueprints, deren Freigabe und Konfiguration, das Starten von Instanzen, den Betrieb sowie das Offboarding.

* Wichtige Rollen sind Azure-Administrator, Entwickler, Tenant-Administrator und Manager.

* Der Artikel unterscheidet zwischen Verantwortlichkeit (Accountability) und Governance, also wer handeln darf und wer dazu verpflichtet ist.

* Je nach Einsatzszenario (Gruppe, Unternehmen oder persönlich) unterscheiden sich die benötigten Rollen.

* Der Tenant-Administrator übernimmt außerdem die laufende Verwaltung der Blueprints und die Überwachung aller Autopilot-Instanzen.


3. Der Artikel gibt einen Überblick über Autopilots in Microsoft Foundry – spezielle KI-Agenten, die mit einer eigenen Identität arbeiten und Microsoft-365-Aktionen unabhängig von einem angemeldeten Nutzer ausführen können.

* Autopilots besitzen sowohl eine Agentenidentität als auch ein eigenes Benutzerkonto.

* Im Gegensatz zu normalen Agenten können sie eigenständig und proaktiv in Microsoft 365 arbeiten.

* Sie werden über Blueprints erstellt, wodurch Berechtigungen und Governance gezielt gesteuert werden können.

* Es gibt drei Varianten: Gruppen-, unternehmensweite und persönliche Autopilots, jeweils für unterschiedliche Einsatzbereiche.

### Quelle: Matt Wolfe AI News

## Meta Muse 
Hier ist eine detaillierte und strukturierte Übersicht über alle bekannten Informationen, technischen Grundlagen und spezifischen Funktionalitäten von Meta Muse.

### 🌐 Was ist Meta Muse?
Meta Muse ist ein am 8. September 2026 vorgestellter, hochentwickelter [persönlicher KI-Agent von Meta Platforms](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/). Im Gegensatz zu klassischen, reaktiven Chatbots (wie ChatGPT oder älteren Versionen von Meta AI) ist Muse ein autonomer Agent. Das bedeutet, das System versteht komplexe, langfristige Ziele, bricht diese eigenständig in Zwischenschritte herunter und führt sie im Hintergrund aus, selbst wenn der Nutzer die App geschlossen hat.

### 🛠️ Technische Kern-Infrastruktur

* 
* Modellbasis: Der Agent wird von Muse Spark angetrieben, einem speziell für agentische Workflows optimierten Sprachmodell. Es beherrscht das sogenannte Zero-Shot-Tool-Calling – es kann also instinktiv entscheiden, wann es welche Software-Werkzeuge einsetzen muss.
* Interner Browser: Muse nutzt einen eigenen, isolierten Webbrowser (Headless Browser) in der Cloud. Dadurch kann die KI auch Webseiten bedienen, die keine offizielle Programmierschnittstelle (API) besitzen, um Formulare auszufüllen oder Daten zu recherchieren.
* Entwicklungs-Codename: Das Projekt wurde von den Meta Superintelligence Labs unter dem internen Codenamen „Hatch“ entwickelt.
* 


### 🎛️ Die Funktionalitäten im Detail
Die Fähigkeiten von Meta Muse lassen sich in vier zentrale Anwendungsbereiche unterteilen:
### 1. Autonomes Aufgabenmanagement & Assistenz

* 
* Proaktives Handeln: Muse wartet nicht nur auf Befehle. Wenn Sie beispielsweise ein Kochvideo auf Instagram als „Reel“ speichern, kann Muse dieses im Hintergrund analysieren, das Rezept extrahieren und die Zutaten selbstständig auf Ihre Einkaufsliste setzen.
* Langzeit-Ziele (Long-running Goals): Sie können Aufgaben stellen wie: „Plane meinen einwöchigen Urlaub in Tokio für nächsten Frühling mit einem Budget von 2.500 €.“ Muse arbeitet über Tage hinweg daran, sucht Flüge, erstellt Routen und aktualisiert die Pläne, wenn sich Preise ändern.
* Kalender- und E-Mail-Vollmacht: Muse kann Ihren Posteingang sortieren, Entwürfe schreiben und Termine mit Dritten koordinieren, indem es direkt mit den digitalen Assistenten anderer Personen interagiert.
* 

#### 2. Live-Dashboards & Daten-Integration

* 
* Zentralisierte Übersichten: Muse aggregiert Daten aus verschiedensten Lebensbereichen und bereitet sie visuell auf der Plattform muse.ai auf.
* Finanz-Tracking: Durch die Verknüpfung mit Bankkonten erstellt die KI Ausgabenanalysen und Budgetprognosen.
* Gesundheit & Fitness: Muse verbindet sich mit Fitness-Trackern (z. B. Apple Health) und korreliert Ihre Schlaf- und Aktivitätsdaten mit Ihren Kalendereinträgen, um Optimierungsvorschläge für Ihren Alltag zu machen.
* 

### 3. Nahtlose Ökosystem- und Hardware-Integration

* 
* Messenger-Bots: Der Agent ist tief in WhatsApp, Instagram Direct und den Facebook Messenger integriert. Sie können Muse dort wie einen normalen Kontakt anschreiben oder in Gruppen-Chats erwähnen, um Aufgaben zu delegieren.
* Wearables: Muse ist für die zukünftige Tiefenintegration in Metas Smart Glasses (Ray-Ban Meta) vorbereitet, um über Sprachbefehle und die verbaute Kamera Kontext aus der echten Welt zu verarbeiten.
* 

### 4. Sicheres Bezahlen im Web

* 
* E-Commerce-Abwicklung: Muse kann eigenständig Online-Käufe (z. B. auf Shopify-Plattformen oder Amazon) durchführen, Hotelbuchungen abschließen oder Lieferungen in Auftrag geben.
* 


### 🔒 Sicherheitsarchitektur & Datenschutz
Da Muse für seine Aufgaben tiefgehende Berechtigungen benötigt, hat Meta ein striktes Sicherheitsmodell implementiert:

* 
* Isolierte Umgebung (Muse Secure VM): Jeder Nutzer erhält eine eigene, isolierte Linux-Umgebung in der Cloud. Bis Ende des Jahres wird dies auf Confidential VMs (vertrauliche Computer-Infrastruktur) umgestellt. Dabei werden die Daten im Arbeitsspeicher so verschlüsselt, dass nicht einmal Meta selbst die Passwörter oder Eingaben des Nutzers einsehen kann.
* Der „Sentinel“-Wächter: Ein komplett separates, unabhängiges KI-Sicherheitssystem läuft parallel auf der Maschine. Sentinel überwacht jede ausgehende Internetverbindung von Muse und blockiert die Aktion sofort, falls der Agent versucht, sensible Daten unautorisiert zu übertragen.
* Virtuelle Kreditkarten: Finanztransaktionen werden niemals mit der echten Kreditkarte des Nutzers durchgeführt. Muse nutzt in Kooperation mit Stripe Link dynamisch generierte Einmalkarten, die exakt auf den Cent-Betrag des jeweiligen Kaufs limitiert sind.
* Human-in-the-Loop (Freigabezwang): Für kritische Aktionen – wie das endgültige Absenden einer geschäftlichen E-Mail oder das Auslösen einer kostenpflichtigen Buchung – fordert das System zwingend eine finale Push-Bestätigung des Nutzers an.
* 

### 💰 Verfügbarkeit und Preisstufen
Das System befindet sich in der schrittweisen Einführungsphase in den USA (für Nutzer ab 18 Jahren). Zur Aktivierung der Hintergrund-Features muss eine Zahlungsmethode hinterlegt werden. Es gibt drei Preisstufen:

| Tarifstufe | Monatliche Kosten | Fokus / Einsatzzweck |
|---|---|---|
| Free Tier | Kostenlos | Grundlegende Alltagsassistenz, gedeckelt durch ein monatliches Nutzungslimit (Usage Meter). |
| Power Tier | ca. $20 | Für Power-User; höhere Priorität bei der Verarbeitung und erweitertes Datenvolumen. |
| Maximum Tier | ca. $100 | Maximale Rechenleistung; unbegrenzte, komplexe Hintergrundprozesse im Rahmen des Meta One-Abos. |

Hinweis: Ein genaues Veröffentlichungsdatum für Europa oder Deutschland ist aufgrund der strengeren Datenschutzvorgaben (DSGVO / AI Act) derzeit noch nicht offiziell angekündigt.


## GPT Image 2.5 
GPT Image 2.5 (auch bekannt als ChatGPT Bilder 2.5) ist das am 8. September 2026 von OpenAI veröffentlichte KI-Bildmodell der neuesten Generation. Es löst GPT Image 2.0 ab und zeichnet sich vor allem durch enorme Geschwindigkeitsvorteile, verbesserte Kontrollen und ein tieferes, logisches Bildverständnis aus. [1, 2, 3] 
Hier ist die detaillierte Übersicht über alle Informationen und Funktionalitäten:
### 🌐 Was ist GPT Image 2.5?
Es handelt sich um ein autoregressives "Denk-Modell" für Bilder. Im Gegensatz zu reinen Diffusionsmodellen (wie älteren Midjourney-Versionen) nutzt es die LLM-Architektur der GPT-Familie, um Prompts logisch zu analysieren, Layouts exakt zu planen und Fehler vor der finalen Ausgabe selbstständig zu korrigieren. Das Modell generiert weltweit bereits über 3 Milliarden Bilder pro Woche. [3, 4, 5, 6, 7, 8] 
### 🎛️ Die zwei API-Modellvarianten
Für Entwickler stellt OpenAI das System über die API in zwei spezialisierten Modell-IDs bereit: [3, 9] 

* 
* GPT-Image-2.5 Flare: Das auf maximale Geschwindigkeit optimierte Modell. Es liefert hochwertige Bilder mit einer um 50 % reduzierten Latenz im Vergleich zur Vorgängerversion (2- bis 4-mal schneller als GPT Image 2). [1, 9, 10] 
* GPT-Image-2.5 Sunburst: Das Premium-Modell für maximale Präzision. Es bietet noch schärfere Details, feineres Licht-Rendering und ist die erste Wahl für komplexe, werbereife Kampagnen-Assets. [4, 9, 11] 
* 

### 🎨 Die wichtigsten Funktionalitäten im Detail
### 1. Sketch-to-Image (Skizze zu Bild)
Nutzer können direkt in der ChatGPT-Oberfläche auf einem digitalen Zeichenpad eine grobe Skizze anfertigen. GPT Image 2.5 nimmt diese visuelle Vorlage und verwandelt sie in Kombination mit einem Text-Prompt in ein detailreiches, professionelles Kunstwerk oder Rendering. [7, 12] 
### 2. Transparente Hintergründe (Native Alpha-Kanäle)
Das Modell beherrscht das native Generieren und Freistellen von Objekten. Selbst extrem komplexe, feine Strukturen (wie die Tentakel einer Qualle oder Insektenflügel) können direkt mit transparentem Hintergrund ausgegeben werden. Dies erleichtert das direkte Layering in Photoshop oder Webdesigns ungemein. [9, 12] 
### 3. Konsistente Bildbearbeitung über mehrere Runden

* 
* Lokale Anpassungen: Über eine Kommentar- und Auswahlfunktion können gezielt Bildelemente verändert werden, während der Rest des Bildes pixelgenau identisch bleibt. [12] 
* Charakter- & Stil-Konsistenz: Das Modell behält das Aussehen von Personen (Subjekten) und Markenprodukten aus Referenzfotos extrem präzise bei, selbst wenn sich die Szene, die Kameraposition oder der Hintergrund in der nächsten Generierungsrunde komplett ändern. [2, 10] 
* 

### 4. Integrierte "Research-Before-Generation"-Logik
Exklusiv in der ChatGPT-Oberfläche (nicht via API) führt das System bei historisch, wissenschaftlich oder datentechnisch komplexen Prompts vorab eine Websuche durch. Dadurch gelingt es GPT Image 2.5, hochpräzise Infografiken, Diagramme oder historische Szenen fehlerfrei und faktisch korrekt darzustellen. [12] 
### 5. Überlegene Textdarstellung (Typografie)
Das Modell kann geschriebenen Text fehlerfrei in Bilder einbetten. Dies umfasst neben dem lateinischen Alphabet nun auch nicht-lateinische Schriften (wie Kyrillisch, Arabisch oder Kanji) ohne die typischen KI-Buchstabenfehler. [6] 
### 🔀 Der direkte Vergleich: Meta Muse Image vs. GPT Image 2.5
Da Meta zeitnah sein eigenes Meta Muse Image-Modell auf den Markt gebracht hat, konkurrieren beide Systeme stark: [6, 13] 

| Feature / Kriterium | GPT Image 2.5 (OpenAI) | Meta Muse Image (Meta) |
|---|---|---|
| Architektur | Autoregressives LLM-Modell | Agentisches Modell (nutzt Sub-Agenten) |
| Hauptstärken | Sketch-Feature, Transparenz, Multi-Turn-Edits | Live-Daten-Infografiken, Generierung von funktionierenden QR-Codes |
| API-Kompatibilität | Nativ über OpenAI API | Vollständig OpenAI-API-kompatibel (einfacher Wechsel der Base-URL) |
| Preismodell (API) | Token-basiertes / Metered Pricing | Aggressives Flatrate-Pricing (z.B. $0.01 pauschal pro Bild) |

### 💰 Verfügbarkeit

* 
* Plattformen: GPT Image 2.5 ist vollständig integriert in ChatGPT (alle Tarife), Codex sowie in Drittanbieter-Tools wie Adobe Firefly und Runway.
* Preise: In den ChatGPT-Abos (Plus, Team, Enterprise) ist die Nutzung inbegriffen (unter Berücksichtigung der jeweiligen Nachrichtenlimits). Über die API wird nach verbrauchten Bild-Einheiten abgerechnet. [1, 3, 6, 14] 
* 


## Deepseek V  4.1-Flash 
DeepSeek V4.1-Flash ist das am 10. September 2026 vom chinesischen KI-Labor DeepSeek veröffentlichte, hocheffiziente Open-Weight-Modell der neuesten Generation. Das Modell bricht mit klassischen LLM-Strukturen und nutzt eine radikal neue, asymmetrische Architektur, die extrem hohe Geschwindigkeiten (bis zu 220+ Tokens pro Sekunde) mit unschlagbar günstigen Betriebskosten für KI-Agenten kombiniert. [1, 2, 3, 4] 
Weil es in Tests sogar das größere V4-Pro-Modell schlug, hat [DeepSeek](https://www.deepseek.com/en/news/deepseek-v4-1-flash/) das Pro-Modell vorerst eingestellt und leitet alle API-Anfragen automatisch zu den deutlich günstigeren Flash-Preisen auf V4.1-Flash um. [5] 
### 🏗️ Die asymmetrische Architektur im Detail
Das Modell basiert auf einem 552-Milliarden-Parameter Mixture-of-Experts (MoE) Backbone, arbeitet aber durch clevere Kniffe so ressourcenschonend wie ein winziges Modell: [2, 3] 

* 
* Asymmetrisches Causal Encoder-Decoder (CED): Bei der Eingabe (Prefill) werden nur 8 Milliarden Parameter aktiv. Erst bei der Ausgabe (Decode) schaltet das Modell auf 16 Milliarden aktive Parameter hoch. Das spart massiv Rechenleistung beim Einlesen riesiger Code-Repositories. [1, 6] 
* Radikale KV-Cache-Verkleinerung (CSA2): Dank Compressed Sparse Attention 2 verbraucht der Zwischenspeicher für Kontexte nur noch 890 Bytes pro Token – das ist ein Viertel (1/4) des HBM-Speicherbedarfs und ein Achtel (1/8) des SSD-Speicherbedarfs des Vorgängers. Für komplexe Agenten-Workflows, die permanent auf dem Kontext aufbauen, ist das der größte Kostensenker. [1, 7] 
* Engram Conditional Memory: Ein zusätzlicher, spärlich angesprochener Wissensspeicher von 196 Milliarden Parametern liefert tiefes Faktenwissen, ohne die Inferenzgeschwindigkeit zu drosseln. [3, 7] 
* 

### 🎛️ Die wichtigsten Funktionalitäten & Features## 1. Natives Multimodal-Verständnis (Vision)
Es ist kein separates "Vision-Exp"-Modell mehr nötig. V4.1-Flash verarbeitet Text und Bilder nativ über einen einzigen API-Endpunkt. Es glänzt beim Erkennen, Zählen und logischen Analysieren von Objekten in Bildern sowie beim Generieren von Code für komplexe visuelle Anwendungen (z. B. Echtzeit-3D-Globen). [3, 5, 8] 
### 2. Der "Reasoning Effort" Dial (Denk-Regler)
Nutzer und Entwickler können die Intensität des logischen Nachdenkens über einen Parameter von 1 bis 100 steuern. [3] 

* 
* Niedriger Wert: Blitzschnelle, intuitive Antworten für einfache Aufgaben.
* Maximaler Wert (100): Das Modell nimmt sich Zeit für tiefe mathematische Beweise, Code-Verifizierungen und logische Ketten (Continuous Reasoning). [3, 9] 
* 

### 3. Massiver Fokus auf "Agent Coding" & Software-Agenten
Das Modell wurde im Post-Training (mittels großskalierbarem Reinforcement Learning) gezielt darauf getrimmt, als autonomer Programmier-Subagent (z. B. im DeepSeek Harness oder OpenCode) zu arbeiten. In Benchmarks wie DeepSWE (Lösen realer GitHub-Issues) springt es von 54,4 % auf phänomenale 74,2 % und zieht damit mit teuren Flaggschiff-Modellen wie Claude 5.0 Opus gleich. [2, 3, 8] 
### 4. Riesiges Kontextfenster
Unterstützt bis zu 1 Million Token Kontext bei einer maximalen Ausgabe von 384.000 Token am Stück. [2, 3] 
### 💰 API-Preise und Lizenz
DeepSeek behält seine aggressive Preiskampf-Strategie bei und rechnet nach Peak- (Hauptverkehrszeit) und Off-Peak-Stunden (Nebenzeiten) ab: [3] 

| Abrechnungseinheit (pro 1 Mio. Token) | Off-Peak (Mondschein-Tarif) | Peak (Hauptzeit) |
|---|---|---|
| Input (Cache Hit – bereits eingelesen) | $0,003 | $0,006 |
| Input (Cache Miss – neu eingelesen) | $0,15 | $0,30 |
| Output (Generierte Tokens) | $0,60 | $1,20 |


* 
* Open-Source & Verfügbarkeit: Die Modellgewichte sind unter der freien MIT-Lizenz auf Hugging Face veröffentlicht. Über die offizielle API ist das Modell einheitlich unter dem Namen deepseek-flash erreichbar. 

# Week 2
## Claude Combines Modes
- Die Zusammenführung von Chat- und Cowork-Modus zu einer einheitlichen Oberfläche („One Claude“) bringt weitreichende neue Funktionen mit sich. Claude entscheidet nun vollautomatisch im Hintergrund, ob für ein Problem ein einfacher Chat ausreicht oder im Hintergrund rechenintensive Agenten-Werkzeuge gestartet werden müssen. [1, 2, 3] 
Die wichtigsten Funktionalitäten, Beta-Tools und System-Features im Überblick:
### 1. Die neuen All-in-One Beta-Werkzeuge (Docs, Slides & Design)
Direkt innerhalb einer laufenden Konversation können nun Medieninhalte erstellt, live editiert und kollaborativ bearbeitet werden: 

* Claude Docs: Ermöglicht das kollaborative Erstellen und Formatieren von Dokumenten (z. B. One-Pager oder Berichte). Texte lassen sich direkt im Dokument manuell anpassen, oder man markiert Zeilen, um Claude via Kommentar um Änderungen zu bitten. Der Export ist nativ nach Google Docs oder Microsoft Word möglich. 
* Claude Slides: Erstellt visuelle Präsentationen und Slide-Decks direkt aus Gesprächsverläufen, Notizen oder Transkripten. Diese können direkt in Claude präsentiert, kommentiert oder als PowerPoint-Präsentation / PDF exportiert werden. 
* Claude Design: Das visuelle Designtool (text-to-prototype) ist komplett in die Workspace-Oberfläche integriert. Damit lassen sich UI/UX-Elemente, Design-Systeme und interaktive Webseiten-Prototypen erzeugen. Elemente können auf einem digitalen Artboard direkt per Maus ausgewählt, verschoben oder editiert werden. 
*

### 2. Autonome Hintergrund-Agenten (Ehemals Cowork-Modus)
Wenn eine Aufgabe komplexer ist (z. B. „Organisiere meinen gesamten Download-Ordner“ oder „Schreibe einen Report aus 20 PDFs“), schaltet Claude unbemerkt in den Hintergrund-Modus: 

* Hintergrund-Ausführung: Claude analysiert die Anfrage, erstellt einen Arbeitsplan und spaltet komplexe Aufgaben in parallele Teilaufgaben auf. Der Nutzer kann das Laptop zuklappen oder den Chat verlassen; Claude arbeitet im Hintergrund weiter und liefert die fertigen Dateien. [2, 4] 
* Code- und Befehlsausführung: Claude besitzt eine isolierte Server-Umgebung (Sandbox), in der KI-Modelle echten Code ausführen, Datenanalysen betreiben und Shell-Befehle nutzen können, um z. B. funktionale Excel-Tabellen mit echten Formeln zu generieren. 
* Connectors & Skills: Über die Einstellungen lassen sich Schnittstellen zu Drittanbieter-Tools (z. B. Google Drive, Gmail, Calendar, HubSpot oder Notion) einrichten. Arbeitsabläufe können als wiederverwendbare „Skills“ abgespeichert und via Vorwärtsstrich (z. B. /mein-skill) oder über automatisierte Zeitpläne (Schedules) gestartet werden. [4, 6, 7] 
* 

### 3. Exklusive Features der Desktop-App
Zwar funktioniert das neue Claude im Webbrowser, bestimmte Systemzugriffe setzen jedoch die Claude Desktop-App (für macOS/Windows) voraus: 

*
* Local File Access: Claude kann direkt auf freigegebene, lokale Ordner auf dem Computer zugreifen, um Dateien massenhaft zu sortieren, umzubenennen oder Rechnungen zu verarbeiten.
* Computer Use & Browser Use: Claude ist in der Lage, den Bildschirm via Screenshots zu analysieren, Benutzeroberflächen zu verstehen und Maus- sowie Tastaturbefehle auszuführen. In der Desktop-App ist zudem ein eigener integrierter Browser verbaut, mit dem Claude eigenständig im Web recherchiert.
* Action Logging: Für maximale Sicherheit wird jede eigenständige Aktion der KI in einem detaillierten Protokoll (Log) festgehalten, sodass Nutzer genau prüfen können, was Claude auf dem System getan hat. [4, 8, 9, 10] 
* 

### Verfügbarkeit
Das neue vereinheitlichte Interface mit den Beta-Tools (Docs, Slides, Design) wird stufenweise ausgerollt: [3] 

* 
* Zuerst: Nutzer der kostenpflichtigen Abos (Claude Pro und Claude Max) im Web, auf dem Desktop und Mobilgeräten.
* Folgend: Die Rollouts für die Abo-Modelle Team sowie schrittweise für die Free-User schließen sich zeitnah an. [2, 3] 
* 


## Claude Projects
Anthropic hat Claude Projects grundlegend überarbeitet. Das Feature wandelt sich von einem statischen Dateiordner zu einer dynamischen, konversationsbasierten Steuerzentrale für autonome Multi-Agenten-Workflows („From folder to conversation“). [1, 2] 
Die wichtigsten Kernfunktionen und Updates im Überblick:
## 1. Das neue Multi-Agenten-Prinzip (Der "Orchestration Hub")
Bisher waren Projekte primär dafür da, Dateien (Knowledge Base) und spezifische Anweisungen (Custom Instructions) für eine Chat-Sitzung zu speichern. Mit der am 17. September 2026 gestarteten Beta-Version fungiert das Projekt als zentraler Koordinator: [1, 3, 4, 5, 6] 

* 
* Delegieren statt Einzelsitzungen: Du gibst in einem Projekt ein übergeordnetes Ziel vor (z. B. „Migriere diese API und teste alle Endpunkte“). [1, 6] 
* Parallele Arbeitsstränge (Threads): Claude zerlegt die Aufgabe selbstständig in logische Teilbereiche. Das System startet im Hintergrund mehrere parallele Cloud-Sitzungen (Claude Code Sessions), die jeweils auf einer eigenen Kopie (Git-Branch) des Codes arbeiten. [3, 6, 7, 8] 
* Automatische Konfliktlösung: Sollten zwei parallele KI-Sitzungen denselben Code modifizieren, führt Claude die Änderungen zusammen und löst Überschneidungen wie bei einem echten Entwickler-Merge-Konflikt auf. [7, 8] 
* Asynchrones Arbeiten: Sobald der Arbeitsplan steht, kannst du deinen Laptop zuklappen oder den Fortschritt von unterwegs auf dem Smartphone überwachen. Die Agenten arbeiten autonom in der Cloud weiter. [1, 7, 8] 
* 

## 2. Das geteilte Projekt-Gedächtnis (Shared Memory)
Innerhalb eines Projekts gibt es nun ein dauerhaftes, dynamisches Gedächtnis, das über alle separaten Chats und Sub-Agenten hinweg synchronisiert bleibt. [7, 9] 

* 
* Kontext-Kontinuität: Wenn du in einem Thread erwähnst, dass ein Release auf Freitag verschoben wurde, weiß das System dieses Detail auch in allen parallel laufenden oder zukünftigen Unterhaltungen des Projekts.
* Lernfähiger Arbeitsstil: Claude merkt sich deine Präferenzen. Du kannst festlegen, wie detailliert Status-Updates sein sollen oder wie häufig die KI eigenständig neue Threads eröffnen darf.
* Zentrale Bibliothek: Alle hochgeladenen Dokumente sowie die von Claude generierten Ergebnisse (wie Code-Dateien, Docs oder Slides) fließen in eine gemeinsame Projekt-Bibliothek ein. [8, 9] 
* 

## 3. Klassische Grundlagen (Bleiben weiterhin aktiv)
Für reguläre Büro- oder Kreativ-Workflows bietet das bewährte Fundament der Projekte nach wie vor feste Strukturen:

* 
* Knowledge Base: Projekte erlauben das einmalige Hochladen einer Wissensdatenbank (z. B. PDFs, Word-Dokumente, CSV, JSON). Claude greift gezielt darauf zu, ohne dass der Nutzer die Daten bei jedem neuen Chat manuell anhängen muss.
* Custom Instructions: Du kannst projektspezifische Verhaltensregeln definieren (z. B. „Schreibe immer im formellen Corporate-Design-Stil“ oder „Nutze für Code-Kommentare ausschließlich Englisch“).
* Team-Kollaboration: In den Team- und Enterprise-Tarifen können ganze Arbeitsbereiche geteilt werden, sodass Kollegen in denselben Projekten mit denselben Dokumenten arbeiten. 
* 

## Verfügbarkeit und Limits

* 
* Derzeitige Beta: Die überarbeiteten, agenten-basierten Projekte rollen zuerst stufenweise für ausgewählte Claude Pro- und Max-Abonnenten aus, die Cloud-Sitzungen in Claude Code nutzen.
* Geplanter Rollout: Der vollständige Release für alle Pro- und Max-User (inklusive Web- und Desktop-Oberfläche) sowie für die Tarife Team und Enterprise folgt im Anschluss.
* Kostenlose Nutzer: Free-User behalten weiterhin Zugriff auf die klassische Variante der Projekte, um eigenständige Arbeitsbereiche zu organisieren (maximal 5 Projekte gleichzeitig). [1, 6, 8, 13, 14] 
* 

Hinweis von Anthropic: Da das System im Hintergrund mehrere Agenten-Sitzungen gleichzeitig öffnet und verarbeitet, verbrauchen die parallelen Threads das gemeinsame Nachrichtenkontingent deines Tarifs deutlich schneller als normale Chats. 
Möchtest du wissen, wie du die Knowledge Base optimal strukturierst, um das Token-Limit nicht zu sprengen, oder interessierst du dich dafür, wie du dich auf die Waitlist für die neuen Multi-Agenten-Projekte setzen lassen kannst?


## Gemini Notebook Update
## New Siri AI
## Qwen 3.8 Omni-Flash
## Union Alpha Model