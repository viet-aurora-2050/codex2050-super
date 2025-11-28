import os
import logging
import requests
from flask import Flask, request, jsonify

from codex2050_engine import handle_message
import config

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


def send_telegram_message(chat_id, text):
    token = config.TELEGRAM_TOKEN
    if not token or token == "YOUR_TELEGRAM_TOKEN_HERE":
        app.logger.error("TELEGRAM_TOKEN nicht gesetzt.")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(
            url,
            json={"chat_id": chat_id, "text": text},
            timeout=10,
        )
    except Exception as e:
        app.logger.error(f"send_telegram_message error: {e}")


@app.route("/", methods=["GET"])
def index():
    return "Codex2050 Super v4 – Imperator Kernel aktiv.", 200


@app.route("/webhook", methods=["POST"])
def telegram_webhook():
    update = request.get_json(force=True, silent=True) or {}
    app.logger.info(f"Update: {update}")
    message = update.get("message") or update.get("edited_message") or {}
    chat = message.get("chat", {})
    chat_id = chat.get("id")
    text = message.get("text", "")

    if not chat_id:
        return jsonify({"ok": True})

    reply = handle_message(text)
    send_telegram_message(chat_id, reply)
    return jsonify({"ok": True})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
