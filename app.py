import os
import requests
from flask import Flask, request

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

app = Flask(__name__)

def send_message(chat_id: int, text: str):
    try:
        print(f"[send] → {text}", flush=True)
        requests.post(
            f"{API}/sendMessage",
            json={"chat_id": chat_id, "text": text},
            timeout=10,
        )
    except Exception as exc:
        print(f"[send_message] error: {exc}", flush=True)

# ————————————————————————————————
# ZENTRUM: Antwort-Logik (jetzt wirklich vorhanden)
# ————————————————————————————————

def handle_message(text: str) -> str:
    t = text.lower().strip()

    if t == "sancho":
        return "Ich bin da. Codex2050 aktiv."
    if t == "/start":
        return "AURORA 2050 – Render Bot Modul.\nWebhook online."
    if t == "ping":
        return "pong 🛰️"

    return f"Echo: {text}"

# ————————————————————————————————

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json(silent=True) or {}
    print(f"[webhook] update: {update}", flush=True)

    message = update.get("message") or update.get("edited_message")
    if not message:
        return {"status": "no message"}, 200

    chat_id = message["chat"]["id"]
    text = message.get("text", "") or ""

    reply = handle_message(text)
    send_message(chat_id, reply)

    return {"status": "ok"}, 200

@app.route("/", methods=["GET"])
def index():
    return "Codex2050 Render Bot läuft."

# gunicorn export
app = app
