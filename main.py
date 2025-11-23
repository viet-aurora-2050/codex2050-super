
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
    raise RuntimeError("TELEGRAM_TOKEN ist nicht gesetzt.")

TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)
engine = Codex2050Engine()

chat_states = {}

def send_message(chat_id, text):
    requests.post(f"{TELEGRAM_API}/sendMessage", json={"chat_id": chat_id, "text": text})

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json(force=True)
    msg = update.get("message", {}) or {}
    chat_id = msg.get("chat", {}).get("id")
    text = msg.get("text") or ""
    state = chat_states.setdefault(chat_id, {})
    reply = handle_message(text, state, engine)
    if reply:
        send_message(chat_id, reply)
    return "OK", 200

@app.route("/")
def index():
    return "Codex2050 Full Deploy OK"
