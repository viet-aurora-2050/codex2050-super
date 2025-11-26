# Codex2050 – Autonomous Hybrid C v1.3.1-HYBRID-C

Dieses Paket ist eine bereinigte, lauffähige Version des Codex2050-Telegram-Bots
für Render.com – inklusive:

- Flask-App (`app.py`)
- Engine (`codex2050_engine.py`)
- Modus-Routing (`codex2050_modes.py`)
- Autonomous-Core (`autonomous_core.py`)
- Memory-Store (`memory_store.json`)
- `render.yaml` & `Procfile` für Deployment
- `requirements.txt` mit minimalen, stabilen Abhängigkeiten

## Deployment (Kurzfassung)

1. Repo auf GitHub hochladen (Inhalt dieses ZIPs als Root).
2. Render-Service mit diesem Repo verbinden.
3. In Render `TELEGRAM_TOKEN` als Environment Variable setzen.
4. Deploy auslösen.
5. Telegram-WebHook setzen:

   `https://api.telegram.org/bot<DEIN_TOKEN>/setWebhook?url=https://codex2050-super.onrender.com/webhook`

Danach antwortet der Bot auf Nachrichten mit einer Codex2050-Antwort,
inklusive einfachem Autonomous-Tagging (z. B. Schutz / Strategie / Körperpfad).
