# Mietwagenverwaltung

Lokale Python-Anwendung mit Terminalmenü zur Verwaltung von Fahrzeugen, Kunden,
Vermietungen und Rückgaben. Die drei ursprünglichen Pakete sind hier gemeinsam
enthalten, damit zum Ausprobieren kein Zugang zur FH-Paketregistry nötig ist.

**Hochschul-Teamprojekt · Python · Schichtenarchitektur · Protocols · Dataclasses · shelve**

## Starten

Python 3.12 oder neuer genügt; für den direkten Start werden keine zusätzlichen
Pakete installiert und keine Zugangsdaten benötigt.

```bash
python run.py
```

Die Daten liegen lokal in `data/` und werden nicht versioniert. Über
`python run.py --data-dir /pfad/zum/ordner` ist ein anderer Speicherort möglich.
Die Verwendung von shelve setzt vertrauenswürdige Datenbankdateien voraus.

## Architektur

| Paket | Aufgabe |
|---|---|
| `packages/ui` | Terminalmenü und UI-Schnittstelle |
| `packages/manager` | Geschäftsregeln für Vermietung und Rückgabe |
| `packages/storage` | Persistenz über shelve |

## Projektstand und eigener Beitrag

Die Mietwagenverwaltung entstand als Hochschul-Teamprojekt. Der eigene Beitrag in einer späteren Übungsvariante umfasste die Implementierung eines HTTP-Clients und eines API-Controllers zur Datenübertragung. Auf diese Variante bezieht sich die Projektbeschreibung im Lebenslauf.

**Dieses Repository enthält die frühere lokale Variante aus Praktikum 2, Aufgabe 2. Der HTTP-Client und der API-Controller der späteren Variante sind hier nicht enthalten.** Die lokale Version zeigt die Aufteilung in Benutzeroberfläche, Geschäftslogik und Speicherung.

## Herkunft und Prüfung

Hochschul-Teamprojekt der FH Münster. Projektstand ohne ursprüngliche GitLab-Historie; Autorenhinweise im Quellcode sind erhalten.

Für den lokalen Start wurden die Pakete zusammengeführt und kleinere Integrationsfehler korrigiert. Prüfergebnisse: [VALIDATION.md](VALIDATION.md).

Die Anwendung verwendet eine lokale Einzelbenutzerdatenbank und hat keine Weboberfläche.
