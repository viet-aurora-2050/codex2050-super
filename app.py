
import os
from flask import Flask, request
import requests

from codex2050_engine import handle_message

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN not set in environment")

API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

app = Flask(__name__)


def send_message(chat_id: int, text: str) -> None:
    """Send a text message back to Telegram."""
    try:
        requests.post(
            f"{API}/sendMessage",
            json={"chat_id": chat_id, "text": text},
            timeout=10,
        )
    except Exception as exc:
        # We just log to stdout; Render will capture logs
        print(f"[send_message] error: {exc}", flush=True)


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
    return "Codex2050 Kernel Ultra – Render online", 200


# Export for gunicorn
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
