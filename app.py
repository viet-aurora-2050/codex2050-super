import os
import json
from datetime import datetime
from flask import Flask, request, jsonify

from codex2050_engine import handle_message

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

def build_telegram_api_url(method: str) -> str:
    if not TELEGRAM_TOKEN:
        raise RuntimeError("TELEGRAM_TOKEN is not set in environment variables.")
    return f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/{method}"

def send_telegram_message(chat_id: int, text: str) -> None:
    import requests

    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
    }
    try:
        requests.post(build_telegram_api_url("sendMessage"), json=payload, timeout=10)
    except Exception as e:
        print(f"[{datetime.utcnow().isoformat()}] send_telegram_message error:", e, flush=True)


@app.route("/", methods=["GET"])
def index() -> str:
    return "Codex2050 v1.3.3 – DarkDeploy Autonomous – service OK"


@app.route("/webhook", methods=["POST"])
def telegram_webhook():
    update = request.get_json(force=True, silent=True) or {}
    print("Incoming update:", json.dumps(update, ensure_ascii=False), flush=True)

    message = update.get("message") or update.get("edited_message")
    if not message:
        return jsonify({"ok": True})

    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    text = message.get("text") or ""

    if not chat_id:
        return jsonify({"ok": True})

    reply = handle_message(text=text, meta={"chat_id": chat_id, "timestamp": datetime.utcnow().isoformat()})
    if reply:
        send_telegram_message(chat_id, reply)

    return jsonify({"ok": True})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
