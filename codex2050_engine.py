
import json
import random
from datetime import datetime

MEMORY_PATH = "memory_store.json"


# -------- Utility memory helpers --------

def _load_memory() -> dict:
    try:
        with open(MEMORY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"lotto": {"super6": [], "spiel77": []}}
    except json.JSONDecodeError:
        return {"lotto": {"super6": [], "spiel77": []}}


def _save_memory(data: dict) -> None:
    with open(MEMORY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def clean_memory() -> str:
    data = {"lotto": {"super6": [], "spiel77": []}}
    _save_memory(data)
    return "🧹 Memory gereinigt."


# -------- Super 6 simulation --------

def _format_super6_draw(draw):
    numbers = " ".join(draw)
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    msg = (
        "🎲 Super-6:\n"
        f"{numbers}\n"
        f"⏱ {ts}\n"
        "📦 Status: gespeichert · Echo aktiv"
    )
    return msg


def handle_super6() -> str:
    draw = [str(random.randint(0, 9)) for _ in range(6)]

    data = _load_memory()
    data.setdefault("lotto", {}).setdefault("super6", [])
    data["lotto"]["super6"].append(draw)
    _save_memory(data)

    return _format_super6_draw(draw)


# -------- Spiel 77 simulation (simpler) --------

def _format_spiel77_draw(draw):
    numbers = " ".join(draw)
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    return (
        "🎰 Spiel 77 – Simulation\n"
        f"Zahlen: {numbers}\n"
        f"⏱ {ts}\n"
        "📦 Status: gespeichert"
    )


def handle_spiel77() -> str:
    draw = [str(random.randint(0, 9)) for _ in range(7)]

    data = _load_memory()
    data.setdefault("lotto", {}).setdefault("spiel77", [])
    data["lotto"]["spiel77"].append(draw)
    _save_memory(data)

    return _format_spiel77_draw(draw)


# -------- Eurojackpot Echo-Scan (placeholder) --------

def eurojackpot_echo() -> str:
    numbers = sorted(random.sample(range(1, 51), 5))
    euro = sorted(random.sample(range(1, 13), 2))
    nums_str = ", ".join(str(n) for n in numbers)
    euro_str = ", ".join(str(e) for e in euro)
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    return (
        "🔍 *Echo-Scan – Eurojackpot (Sim)*\n"
        f"Zahlen: {nums_str}\n"
        f"Eurozahlen: {euro_str}\n"
        f"⏱ {ts}\n"
        "_Basis: deterministischer Offline-Simulator, kein echter Tippschein._"
    )


# -------- Imperator-Kernel X v4.2 – text router --------

def handle_message(text: str) -> str:
    """Route incoming Telegram text to the right module."""
    t = (text or "").strip().lower()

    # Hard reset
    if t in {"clean", "reset", "memory", "🧹"}:
        return clean_memory()

    # Super 6
    if any(key in t for key in ["super6", "super 6", "s6"]):
        return handle_super6()

    # Spiel 77
    if any(key in t for key in ["spiel77", "spiel 77", "77"]):
        return handle_spiel77()

    # Eurojackpot echo
    if any(key in t for key in ["echo", "eurojackpot", "ej"]):
        return eurojackpot_echo()

    # Lotto / overview
    if "lotto" in t:
        return (
            "🧠 Sancho-Modus aktiv.\n"
            "Analyse:\n"
            "→ lotto\n\n"
            "Autonomer Kern aktiv – Lotto · Echo · Entscheidungen.\n"
            "\n"
            "Befehle:\n"
            "• super 6  → tägliche Super-6-Simulation\n"
            "• spiel 77 → tägliche Spiel-77-Simulation\n"
            "• echo     → Eurojackpot Echo-Scan\n"
            "• clean    → Memory-Cleaner\n"
        )

    # Auto / Imperator-Modus
    if "auto" in t or "sancho" in t:
        return (
            "Sancho-Modus aktiv.\n"
            "Analyse:\n"
            f"→ {t or 'auto'}\n\n"
            "Autonomer Kern aktiv – Lotto · Echo · Entscheidungen."
        )

    # Default
    return (
        "Codex2050 Kernel Ultra aktiv.\n"
        "Schreibe zum Beispiel:\n"
        "• super 6\n"
        "• spiel 77\n"
        "• echo\n"
        "• lotto\n"
        "• clean\n"
    )
