# Datei-Integritätsüberprüfung (File Integrity Monitoring)

Ein einfaches Python-Skript zur Überwachung von Dateien in einem angegebenen Verzeichnis. Es erkennt neue, geänderte oder gelöschte Dateien anhand von SHA-256-Hashwerten.

## Funktionsweise

Dieses Tool:
- erstellt Hash-Werte für alle Dateien im angegebenen Verzeichnis (und Unterverzeichnissen),
- vergleicht sie mit vorherigen Hashwerten aus einer `hashes.json`-Datei,
- erkennt neue, geänderte oder gelöschte Dateien,
- speichert die aktuellen Hashes als neue Basislinie.

## Voraussetzungen

- Python 3.x
- Betriebssystem: Windows oder Linux
- Python-Standardbibliotheken: `os`, `hashlib`, `argparse`, `json`

## Installation

Kein Setup notwendig. Stelle nur sicher, dass Python installiert ist.

## Beispiel

Ein Beispiel zur Nutzung des Codes wäre wiefolgt:

'py "File integrity monitoring.py" --check "C:\Users\Benutzername\Dokumente\wichtiges"'
