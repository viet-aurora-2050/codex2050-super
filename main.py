import os
import logging
import requests
from flask import Flask, request

from codex2050_engine import Codex2050Engine
from codex2050_modes import handle_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("codex2050")

TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    # Hart abbrechen, weil ohne Token macht der Dienst keinen Sinn
    raise RuntimeError("TELEGRAM_TOKEN ist nicht gesetzt.")

TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)
engine = Codex2050Engine()

# sehr einfache In-Memory-States pro Chat-ID
chat_states = {}

def get_state(chat_id: int):
    return chat_states.setdefault(chat_id, {})

@app.route("/", methods=["GET"])
def index():
    return "Codex2050 Render Bot – online (final3)."

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True, silent=True) or {}
    logger.info("Update: %s", data)

    message = data.get("message") or data.get("edited_message")
    if not message:
        return "no message"

    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    text = message.get("text", "")

    if chat_id is None:
        return "no chat"

    state = get_state(chat_id)
    try:
        reply = handle_message(text, engine, state)
    except Exception as e:
        logger.exception("Fehler in handle_message: %s", e)
        reply = "Ich hatte intern einen Fehler. Versuch es bitte noch einmal in einfachen Sätzen."

    send_message(chat_id, reply)
    return "ok"

def send_message(chat_id: int, text: str):
    try:
        resp = requests.post(
            TELEGRAM_API + "/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
            },
            timeout=10,
        )
        if resp.status_code != 200:
            logger.warning("sendMessage failed: %s %s", resp.status_code, resp.text)
    except Exception as e:
        logger.error("sendMessage exception: %s", e)

def set_webhook():
    url = os.environ.get("WEBHOOK_URL")
    if not url:
        logger.warning("WEBHOOK_URL ist nicht gesetzt – kein automatisches setWebhook.")
        return
    try:
        resp = requests.get(
            TELEGRAM_API + "/setWebhook",
            params={"url": url},
            timeout=10,
        )
        logger.info("setWebhook: %s %s", resp.status_code, resp.text)
    except Exception as e:
        logger.error("setWebhook exception: %s", e)

if __name__ == "__main__":
    # Beim direkten Start (z.B. lokal) einmalig Webhook setzen
    set_webhook()
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
