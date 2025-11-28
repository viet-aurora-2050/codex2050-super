
# Codex2050 Kernel Ultra – Telegram Bot

Minimaler Render/Telegram-Bot:

- `/webhook` empfängt Telegram-Updates
- `codex2050_engine.py` enthält:
  - Super‑6 Simulation + Memory
  - Spiel‑77 Simulation
  - Eurojackpot Echo‑Scan (Sim)
  - Memory‑Cleaner
  - Imperator‑Kernel‑Router `handle_message`

## Deployment (Render)

1. Neues Web Service auf Render erstellen, Repo/ZIP Inhalt hochladen.
2. Environment Variable setzen:

   - `TELEGRAM_TOKEN` = dein Bot‑Token vom BotFather.

3. Render startet mit:

   ```bash
   gunicorn app:app
   ```

4. Webhook in Telegram setzen:

   ```text
   https://api.telegram.org/bot<DEIN_TOKEN>/setWebhook?url=https://DEIN-SERVICE.onrender.com/webhook
   ```

Danach kannst du dem Bot in Telegram schreiben:

- `super 6`
- `spiel 77`
- `echo`
- `lotto`
- `clean`
- `auto`
