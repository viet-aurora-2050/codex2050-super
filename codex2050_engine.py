import json
import random
import os
from sancho_core import sancho_reply

MEMORY = "memory_store.json"


def load():
    if not os.path.exists(MEMORY):
        return {"super6": [], "spiel77": [], "echo": []}
    with open(MEMORY, "r", encoding="utf-8") as f:
        return json.load(f)


def save(data):
    with open(MEMORY, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def super6():
    d = [str(random.randint(0,9)) for _ in range(6)]
    db = load()
    db["super6"].append(d)
    save(db)
    return "🎲 Super-6:\n" + " ".join(d)


def spiel77():
    d = [str(random.randint(0,9)) for _ in range(7)]
    db = load()
    db["spiel77"].append(d)
    save(db)
    return "🎰 Spiel-77:\n" + " ".join(d)


def echo():
    d = random.sample(range(1,51),5)
    e = random.sample(range(1,11),2)
    return (
        "📡 Echo-Scan (Simulation)\n"
        f"Zahlen: {d}\nEurozahlen: {e}"
    )


def clean():
    save({"super6": [], "spiel77": [], "echo": []})
    return "🧹 Memory gereinigt."


def handle_message(text: str) -> str:
    t = text.lower().strip()

    if "super" in t:
        return super6()

    if "77" in t:
        return spiel77()

    if "echo" in t or "euro" in t:
        return echo()

    if "clean" in t or "reset" in t:
        return clean()

    return sancho_reply(text)
