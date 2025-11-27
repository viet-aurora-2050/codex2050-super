# Codex2050 – DarkDeploy v1.3.3 (Autonomous · Render · Telegram)

Dieses Paket enthält eine fokussierte Version des Codex2050-Bots:

- Flask + gunicorn für Render
- Telegram-WebHook (`/webhook`)
- Lotto-Module (Super 6 / Spiel 77 / Eurojackpot Echo) als Offline-Simulator
- Themenbasierte Moduslogik:
  - Liebe / Nähe / Frauen (ohne feste Namen)
  - Business / Restaurant / Projekte
  - Geld / Druck / Rechnungen
  - Körper / Energie / Müdigkeit

## Deployment (Kurzfassung)

1. Inhalt dieses Zips als neues GitHub-Repo hochladen (Root = diese Dateien).
2. Render-Webservice erstellen und mit dem Repo verbinden.
3. In Render eine Environment-Variable setzen: `TELEGRAM_TOKEN = <dein Bot-Token>`.
4. Deploy auslösen.
5. Telegram-WebHook setzen:

   `https://api.telegram.org/bot<DEIN_TOKEN>/setWebhook?url=https://<dein-render-service>.onrender.com/webhook`

Danach antwortet der Bot im Sancho·2050-Stil:

- mit neutralem Dark-Blue-Fokus,
- ohne hartkodierte Personennamen,
- mit konkreten Mikro-Schritten für echte Welt (Geld, Körper, Business, Nähe),
- plus Lotto-/Echo-Simulation als eigenes Modul.
