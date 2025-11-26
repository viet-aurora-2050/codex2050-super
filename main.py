import os
from flask import Flask, request
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

app = Flask(__name__)

API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"


# --- BASIC SEND FUNCTION ---
def send_message(chat_id, text):
    requests.post(
        f"{API}/sendMessage",
        json={"chat_id": chat_id, "text": text}
    )


# --- WEBHOOK ENDPOINT ---
@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()

    if not update:
        return {"status": "no update"}, 200

    # Extract message
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        # Simple response
        reply = f"🜏 Sancho aktiv.\nEcho: {text}"
        send_message(chat_id, reply)

    return {"status": "ok"}, 200


# --- ROOT ---
@app.route("/", methods=["GET"])
def index():
    return "Codex2050 Autonomous Mode v1.3 + Memory – Webhook OK", 200


# --- APP EXPORT FOR RENDER ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
