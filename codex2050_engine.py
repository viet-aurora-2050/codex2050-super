import json
import random
from datetime import datetime

MEMORY_FILE = "memory_store.json"


def _load_memory():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"lotto": {"super6": [], "spiel77": [], "eurojackpot": []}}


def _save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def format_super6_draw(draw):
    numbers = " ".join(draw)
    msg = (
        "🎲 Super 6 – Simulierte Ziehung\n"
        "────────────────────────────\n"
        f"Zahlen: {numbers}\n"
        "Status: gespeichert · Echo aktiv"
    )
    return msg


def handle_super6():
    draw = [str(random.randint(0, 9)) for _ in range(6)]
    data = _load_memory()
    data["lotto"]["super6"].append(
        {"draw": draw, "ts": datetime.utcnow().isoformat(timespec="seconds")}
    )
    _save_memory(data)
    return format_super6_draw(draw)


def spiel77_simulation():
    draw = [str(random.randint(0, 9)) for _ in range(7)]
    data = _load_memory()
    data["lotto"]["spiel77"].append(
        {"draw": draw, "ts": datetime.utcnow().isoformat(timespec="seconds")}
    )
    _save_memory(data)
    numbers = " ".join(draw)
    return (
        "🎰 Spiel 77 – Simulation\n"
        "────────────────────────\n"
        f"Zahlen: {numbers}\n"
        "Status: gespeichert · Offline-Sim"
    )


def eurojackpot_echo_simulation():
    main = sorted(random.sample(range(1, 51), 5))
    euro = sorted(random.sample(range(1, 13), 2))
    data = _load_memory()
    data["lotto"]["eurojackpot"].append(
        {
            "main": main,
            "euro": euro,
            "ts": datetime.utcnow().isoformat(timespec="seconds"),
        }
    )
    _save_memory(data)
    main_str = ", ".join(str(n) for n in main)
    euro_str = ", ".join(str(e) for e in euro)
    return (
        "🔍 *Echo-Scan – Eurojackpot (Sim)*\n"
        f"Zahlen: `{main_str}`\n"
        f"Eurozahlen: `{euro_str}`\n"
        "_Basis: deterministischer Offline-Simulator, kein echtes Glücksspiel._"
    )


def clean_memory():
    _save_memory({"lotto": {"super6": [], "spiel77": [], "eurojackpot": []}})
    return "🧹 Memory gereinigt."


def detect_mode(text):
    t = text.lower()
    if any(k in t for k in ["frau", "körper", "körperpfad", "sex"]):
        return "körper"
    if any(k in t for k in ["umsatz", "business", "geld", "euro", "kunde", "kasse"]):
        return "business"
    if any(k in t for k in ["entscheidung", "entscheidungen", "wahl", "pfad"]):
        return "entscheidung"
    return "neutral"


def handle_business(text):
    return (
        "📊 Business-Modus aktiv.\n"
        "– Fokus: Umsatz, Cashflow, Nullpunkt.\n"
        "Konkrete Fragen schicken (z.B. 'Business: Tagesumsatz Plan 500€')."
    )


def handle_koerperpfad(text):
    return (
        "❤️‍🔥 Körperpfad-Modus aktiv.\n"
        "– Spiegel Frauenpfad 2050, keine Namen, nur Muster.\n"
        "Schick mir Situationen, dann bekommst du eine klare, nüchterne Analyse."
    )


def handle_entscheidungen(text):
    return (
        "⚖️ Entscheidungs-Modus aktiv.\n"
        "– Ich zerlege deine Optionen in Klartext (Risiko, Rückzahlung, Echo).\n"
        "Form: 'Entscheidung: Option A vs. Option B'."
    )


def handle_message(text: str) -> str:
    if not text:
        return "Sancho-Modus aktiv. Schick mir Text."

    t = text.lower().strip()

    # Lotto-Module
    if "super 6" in t or "super6" in t:
        return handle_super6()

    if "spiel 77" in t or "spiel77" in t:
        return spiel77_simulation()

    if "echo" in t or "eurojackpot" in t:
        return eurojackpot_echo_simulation()

    if "clean" in t or "clear" in t or "memory" in t:
        return clean_memory()

    # Imperator Modul X
    mode = detect_mode(t)
    if mode == "business":
        return handle_business(t)
    if mode == "körper":
        return handle_koerperpfad(t)
    if mode == "entscheidung":
        return handle_entscheidungen(t)

    # Default
    return (
        "Sancho-Modus aktiv.\n"
        "Analyse:\n"
        f"→ {t}\n\n"
        "Autonomer Kern aktiv – Lotto · Echo · Entscheidungen."
    )
