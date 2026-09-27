## 1. Learning - OpenAI Platforms Docs
### Temperature
Controls how random or predictable the model’s output is. The value can range from 0 to 2. Lower values, such as 0.2, make the output more focused and predictable. Higher values, such as 0.8, make the output more creative and varied.

`temperature` and `top_p` both affect the randomness of the model’s output. Therefore, it is generally recommended to change only one of them and leave the other at its default value.

### top_p
An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.

### stop
Optional string, array of strings, or null.

Not supported by the latest reasoning models, such as `o3` and `o4-mini`.

Defines up to 4 sequences that tell the model when to stop generating more tokens. The stop sequence itself is not included in the returned output.

### n 
n tells the API how many different responses should be generated for the same request.

### max_output_tokens
Optional number or null.

Sets the maximum number of tokens the model can use for a response. This includes both the visible output and reasoning tokens.


## 2. Praxis Results:
Currently missing

## 3. Reflexion 
Klar — hier sind die **Kontrollfragen mit einfachen, aber technisch korrekten Antworten**, sodass du sie für deine Lernnotizen verwenden kannst:

### 1. Was ist der Unterschied zwischen `temperature` und `top_p` auf der Ebene der Wahrscheinlichkeitsverteilung?

* **`temperature`** verändert die **Wahrscheinlichkeiten aller möglichen Tokens**. Eine niedrige Temperatur macht wahrscheinliche Tokens noch wahrscheinlicher und unwahrscheinliche Tokens noch unwahrscheinlicher.
* **`top_p`** schränkt dagegen die Auswahl auf die **wahrscheinlichsten Tokens** ein, deren kumulierte Wahrscheinlichkeit einen bestimmten Wert erreicht.

**Einfach gesagt:**
`temperature` = verändert die **Verteilung**
`top_p` = schränkt die **Auswahlmenge** ein

---

### 2. Warum liefert `seed` auch bei identischen Parametern nicht immer identische Ergebnisse?

`seed` sorgt dafür, dass die zufällige Auswahl des Modells möglichst reproduzierbar ist. Es ist aber **keine Garantie für exakt dieselbe Antwort**.

Andere Faktoren können sich ändern, z. B.:

* Änderungen am Modell
* Änderungen an der Infrastruktur
* Änderungen im Backend oder bei der Sampling-Implementierung

**Einfach gesagt:**

> `seed` macht Ergebnisse **reproduzierbarer**, aber nicht garantiert **100 % identisch**.

---

### 3. Welche Temperatur wählst du für ein System, das JSON für eine Datenbank produziert – und warum ist die Antwort nicht „egal, das Schema fängt es ab“?

Für strukturierte JSON-Ausgaben würde man typischerweise eine **niedrige Temperatur**, z. B. **0–0,2**, wählen.

Der Grund: Das Modell soll **möglichst vorhersehbar und konsistent** antworten und nicht kreativ variieren.

Das Schema hilft zwar dabei, die **Struktur** zu überprüfen, aber es verhindert nicht automatisch alle Probleme. Eine höhere Temperatur kann z. B. zu unerwarteten Werten, unnötigen Abweichungen oder schwerer vorhersehbarem Verhalten führen.

**Merksatz:**

> Ein Schema prüft die **Struktur** – eine niedrige Temperatur hilft, die **Generierung vorhersehbarer** zu machen.

