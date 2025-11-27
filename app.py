import os
import json
import logging

import requests
from flask import Flask, request

from codex2050_engine import handle_message

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN environment variable is not set")

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"


def send_message(chat_id: int, text: str) -> None:
    """Schickt eine Antwort an Telegram."""
    if len(text) > 3900:
        text = text[:3900] + "\n…[gekürzt]"
    try:
        requests.post(
            f"{TELEGRAM_API}/sendMessage",
            json={"chat_id": chat_id, "text": text},
            timeout=10,
        )
    except Exception as e:
        app.logger.error(f"send_message error: {e}")


@app.route("/", methods=["GET"])
def index():
    """Healthcheck – wird z.B. von Render aufgerufen."""
    return "Codex2050 Render Bot online", 200


@app.route("/", methods=["POST"])
def webhook():
    """Telegram Webhook Endpoint."""
    update = request.get_json(force=True, silent=True) or {}
    app.logger.info("Update: %s", json.dumps(update))

    message = update.get("message") or update.get("edited_message") or {}
    text = message.get("text") or ""
    chat = message.get("chat") or {}
    chat_id = chat.get("id")

    # Nichts Sinnvolles drin → einfach OK sagen
    if not chat_id or not text:
        return "no message", 200

    # Deine Engine
    try:
        reply = handle_message(text)
    except Exception as e:
        app.logger.error(f"handle_message error: {e}")
        reply = "⚠️ Interner Fehler im Codex2050-Engine-Modul."

    if reply:
        send_message(chat_id, reply)

    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
