# Codex2050 – Autonomous Hybrid C Entry v1.3.1
# Flask + Telegram Webhook + Engine + AutonomousCore

import os
import json
import requests
from flask import Flask, request

from codex2050_engine import CodexEngine
from codex2050_modes import resolve_mode
from autonomous_core import AutonomousCore

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    print("⚠️ TELEGRAM_TOKEN ist nicht gesetzt – Bot kann nicht antworten.")
TG_SEND = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

engine = CodexEngine()
auto_core = AutonomousCore()


@app.route("/", methods=["GET"])
def home():
    return "Codex2050 v1.3.1 – Autonomous Hybrid C – Webhook OK", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True)

    if not data or "message" not in data:
        return {"status": "ignored"}, 200

    msg = data["message"]
    chat_id = msg["chat"]["id"]
    text = msg.get("text", "") or ""

    # 1) Autonomous-Layer
    auto_state = auto_core.process(text)

    # 2) Modus ermitteln
    mode = resolve_mode(text)

    # 3) Engine-Antwort
    reply = engine.generate_response(text, mode=mode, auto=auto_state)

    if TELEGRAM_TOKEN:
        try:
            requests.post(TG_SEND, json={
                "chat_id": chat_id,
                "text": reply
            }, timeout=5)
        except Exception as e:
            print("Send-Error:", e)

    return {"status": "sent"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
