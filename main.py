
import os
import logging
import requests
from flask import Flask, request
from codex2050_engine import Codex2050Engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("codex2050")

TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN ist nicht gesetzt.")

TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)
engine = Codex2050Engine()

def send_message(chat_id, text):
    url = f"{TELEGRAM_API}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        r = requests.post(url, json=payload, timeout=10)
        if r.status_code != 200:
            logger.warning(f"sendMessage failed: {r.text}")
    except Exception as e:
        logger.error(f"send_message error: {e}")

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json(force=True)
    logger.info(f"Update: {update}")
    try:
        message = update.get("message", {}) or {}
        chat_id = message.get("chat", {}).get("id")
        response_text = engine.process(update)
        if response_text:
            send_message(chat_id, response_text)
    except Exception as e:
        logger.error(f"Webhook error: {e}")
    return "OK", 200

@app.route("/", methods=["GET"])
def index():
    return "Codex2050 Autonomous Mode v1.3 + Memory – Webhook OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
