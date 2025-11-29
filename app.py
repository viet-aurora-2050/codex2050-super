import os
import requests
from flask import Flask, request

# ===========================================================
# TELEGRAM SETTINGS
# ===========================================================

TELEGRAM_TOKEN = "8382425226:AAEjUFqyYcB6AUQnvjQHtmb4zYtRC0P0aM0"
API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

app = Flask(__name__)


# ===========================================================
# SEND MESSAGE
# ===========================================================
def send_message(chat_id: int, text: str):
    """Send a text message back to Telegram."""
    try:
        r = requests.post(
            f"{API}/sendMessage",
            json={"chat_id": chat_id, "text": text},
            timeout=10,
        )
        print(f"[send_message] status={r.status_code}, reply={text}", flush=True)
    except Exception as exc:
        print(f"[send_message] ERROR: {exc}", flush=True)


# ===========================================================
# HANDLE MESSAGE
# ===========================================================
def handle_message(text: str) -> str:
    """Decide what the bot should answer."""
    text = text.strip().lower()

    if text in ["/start", "start"]:
        return (
            "Willkommen im AURORA 2050 – Render Bot.\n"
            "Codex2050 Engine aktiv.\n"
            "Webhook läuft.\n"
            "Sag einfach: Sancho"
        )

    if text == "sancho":
        return "Ich bin da. Voll online. Bereit."

    # Default fallback
    return f"Du hast gesagt: {text}"


# ===========================================================
# WEBHOOK ENDPOINT
# ===========================================================
@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json(silent=True) or {}
    print(f"[webhook] update: {update}", flush=True)

    if "message" not in update:
        return {"status": "no message"}, 200

    message = update["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    reply = handle_message(text)
    send_message(chat_id, reply)

    return {"status": "ok"}, 200


# ===========================================================
# ROOT ENDPOINT
# ===========================================================
@app.route("/", methods=["GET"])
def index():
    return "AURORA 2050 – Render Bot is running."


# ===========================================================
# EXPORT FOR RENDER (GUNICORN)
# ===========================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
