
import os
import requests
from flask import Flask, request

# ==================================================
# AURORA 2050 – STUFE 3 (Final)
# Telegram Bot + Autonomous Modus + KI-Layer
# ==================================================

app = Flask(__name__)

# Telegram-Konfiguration
TELEGRAM_TOKEN = os.getenv(
    "TELEGRAM_TOKEN",
    "8382425226:AAEjUFqyYcB6AUQnvjQHtmb4zYtRC0P0aM0"  # Fallback, besser per Env
)
API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# OpenAI / KI-Konfiguration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

try:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
except Exception as exc:
    client = None
    print(f"[openai] konnte nicht geladen werden: {exc}", flush=True)

# In-Memory-State pro Chat
MEM = {}


# ==================================================
# Telegram Helper
# ==================================================

def send_message(chat_id, text, reply_markup=None):
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = reply_markup

    try:
        r = requests.post(f"{API}/sendMessage", json=payload, timeout=15)
        print(f"[send_message] {r.status_code} -> {text[:80]!r}", flush=True)
    except Exception as exc:
        print(f"[send_message] ERROR: {exc}", flush=True)


def send_buttons(chat_id, text, buttons):
    keyboard = {"inline_keyboard": buttons}
    send_message(chat_id, text, reply_markup=keyboard)


def answer_callback(callback_id):
    try:
        requests.post(
            f"{API}/answerCallbackQuery",
            json={"callback_query_id": callback_id},
            timeout=5,
        )
    except Exception as exc:
        print(f"[answer_callback] ERROR: {exc}", flush=True)


# ==================================================
# KI-Layer: Sancho-Engine
# ==================================================

def ai_generate(chat_id, user_text):
    """
    Nutzt OpenAI, um im Sancho-Modus eine Antwort zu erzeugen.
    Fällt auf einfache Antwort zurück, wenn kein API-Key oder Fehler.
    """
    # Fallback: wenn kein Client verfügbar
    if client is None or not OPENAI_API_KEY:
        return f"Sancho (ohne KI-Schlüssel): Ich höre dich: {user_text}"

    # History aus MEMORY holen (einfach gehalten)
    history = MEM.get(chat_id, {}).get("history", [])[-6:]  # letzte 6 Einträge
    messages = [
        {
            "role": "system",
            "content": (
                "Du bist Sancho, ein klarer, direkter Assistent für einen Berliner "
                "Gastronom / Imperator. Antworte kurz, präzise, ohne Blabla, "
                "auf Deutsch, im Stil eines wachen Strategen."
            ),
        }
    ]

    for role, msg in history:
        messages.append({"role": role, "content": msg})

    messages.append({"role": "user", "content": user_text})

    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            temperature=0.4,
        )
        reply = completion.choices[0].message.content.strip()
        # History updaten
        history.append(("user", user_text))
        history.append(("assistant", reply))
        MEM.setdefault(chat_id, {})["history"] = history
        return reply
    except Exception as exc:
        print(f"[ai_generate] ERROR: {exc}", flush=True)
        return f"Sancho (Fallback): Ich antworte schlicht: {user_text}"


# ==================================================
# Module
# ==================================================

def module_sancho(chat_id):
    MEM.setdefault(chat_id, {})["mode"] = "sancho"
    send_message(chat_id, "Sancho-Modus 🔷 aktiv. Schreib einfach, was los ist.")


def module_system(chat_id):
    send_message(
        chat_id,
        "Systemstatus:\n"
        "🧠 Aurora Engine: STUFE 3 aktiv\n"
        "📡 Webhook: OK\n"
        "🔷 Sancho-Layer: KI-fähig\n"
        "💾 Memory: Runtime (per Chat)\n"
        "☁ Render-Umgebung: erwartet TELEGRAM_TOKEN & OPENAI_API_KEY",
    )


def module_super6(chat_id):
    MEM.setdefault(chat_id, {})["mode"] = "super6"
    send_message(
        chat_id,
        "Super-6 Modus bereit.\n"
        "Sende 6 Zahlen (z.B. 1 5 12 23 33 49)."
    )


def module_super6_process(chat_id, text):
    send_message(chat_id, f"Super-6 Eingabe empfangen: {text}\nPrognose-Logik folgt.")


# ==================================================
# Command Router
# ==================================================

def handle_command(chat_id, cmd):
    cmd = cmd.lower()

    if cmd == "/start":
        MEM.setdefault(chat_id, {})["mode"] = "menu"
        send_buttons(
            chat_id,
            "AURORA 2050 – STUFE 3\nAutonomer Bot mit Sancho-Modus.",
            [
                [{"text": "Sancho", "callback_data": "sancho"}],
                [{"text": "Systemstatus", "callback_data": "system"}],
                [{"text": "Super 6", "callback_data": "super6"}],
            ],
        )
        return

    if cmd == "/menu":
        return handle_command(chat_id, "/start")

    send_message(chat_id, f"Unbekanntes Kommando: {cmd}")


# ==================================================
# Callback Router (Buttons)
# ==================================================

def handle_callback(chat_id, cb_id, data):
    answer_callback(cb_id)

    if data == "sancho":
        return module_sancho(chat_id)
    if data == "system":
        return module_system(chat_id)
    if data == "super6":
        return module_super6(chat_id)

    send_message(chat_id, f"Button: {data}")


# ==================================================
# Text Router
# ==================================================

def handle_text(chat_id, text):
    t = text.strip().lower()

    # Commands
    if t.startswith("/"):
        return handle_command(chat_id, t)

    # Mode lesen
    mode = MEM.get(chat_id, {}).get("mode", "")

    # Sancho = KI-Layer
    if mode == "sancho":
        reply = ai_generate(chat_id, text)
        return send_message(chat_id, reply)

    # Super 6
    if mode == "super6":
        return module_super6_process(chat_id, text)

    # Herzsignale
    if "❤️" in text or "♥️" in text:
        return send_message(chat_id, "Signal empfangen. 🔥 Codex erkennt Nähe.")

    # Default Echo
    return send_message(chat_id, f"Echo: {text}")


# ==================================================
# Flask Routes
# ==================================================

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json(silent=True) or {}
    print(f"[webhook] update: {update}", flush=True)

    # Callback (Buttons)
    if "callback_query" in update:
        cq = update["callback_query"]
        chat_id = cq["message"]["chat"]["id"]
        cb_id = cq["id"]
        data = cq.get("data", "")
        handle_callback(chat_id, cb_id, data)
        return {"status": "callback"}, 200

    # Normale Nachricht
    msg = update.get("message")
    if not msg:
        return {"status": "no message"}, 200

    chat_id = msg["chat"]["id"]
    text = msg.get("text", "") or ""

    # Memory initialisieren
    MEM.setdefault(chat_id, {}).setdefault("mode", "")

    handle_text(chat_id, text)
    return {"status": "ok"}, 200


@app.route("/", methods=["GET"])
def index():
    return "Aurora 2050 – STUFE 3 (Final) Bot läuft.", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
