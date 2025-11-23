# Codex2050 – Debug Edition v1.1

Dieses Repository enthält die stabile und überprüfbare Debug-Edition des Codex2050-Systems.  
Ziel: sofortige Reproduzierbarkeit, einfache Deployments (Render, GitHub) und klare Fehlerdiagnose.

## Inhalt
- Verbesserte Debug-Tabellen (`table_improved_1.csv`, `table_improved_2.csv`)
- Vollständiger Backend-Code:
  - `main.py`
  - `codex2050_engine.py`
  - `codex2050_modes.py`
- Deployment-Konfiguration:
  - `render.yaml`
  - `requirements.txt`

## Deployment auf Render
1. Neues Render-Projekt erstellen → “Web Service”.
2. GitHub-Repo verbinden.
3. Automatisch erkennt Render:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
4. Unter Environment Variables hinzufügen:
   - `TELEGRAM_TOKEN`
   - `WEBHOOK_URL`
5. Deploy klicken.

## Ordnerstruktur
```
codex2050/
├── main.py
├── codex2050_engine.py
├── codex2050_modes.py
├── table_improved_1.csv
├── table_improved_2.csv
├── requirements.txt
├── render.yaml
└── README_GitHub.md
```

## Versionierung
- **v1.1** – Debug Edition  
  Enthält Fehlercodes, Diagnosematrix, automatische Checks und Render-kompatible Struktur.

