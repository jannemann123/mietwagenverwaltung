# Prüfung am 8. Oktober 2026

Python 3.12.14: `python -m unittest -v test_workflow` erfolgreich.
Der Test prüft Kundenanlage, Fahrzeuganlage, Verfügbarkeitsanzeige, Vermietung,
Sperre der Löschung vermieteter Fahrzeuge und betroffener Kunden, Rückgabe,
Persistenz nach Schließen/Öffnen sowie abschließendes Löschen.
Alle Python-Dateien konnten mit compileall kompiliert werden.

Der lokale Einstieg `run.py` umgeht die ursprüngliche private Paketregistry.
Die separat installierbaren Pakete mit ihrem ursprünglichen uv_build-Backend
wurden nicht veröffentlicht und nicht als Registry-Pakete getestet.
