from flask import Flask, request
import requests
import config
from codex2050_engine import handle_message

app = Flask(__name__)

TOKEN = config.TELEGRAM_TOKEN
API = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def send(chat_id, text):
    requests.post(API, json={"chat_id": chat_id, "text": text})


@app.route("/", methods=["GET"])
def index():
    return "Codex2050 Super v3.0 · Sancho-Core aktiv", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if not data:
        return "no data", 200

    msg = data.get("message", {})
    text = msg.get("text", "")
    chat_id = msg.get("chat", {}).get("id")

    if text and chat_id:
        reply = handle_message(text)
        send(chat_id, reply)

    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
