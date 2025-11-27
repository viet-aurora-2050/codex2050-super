import json
import random
from datetime import datetime, date, timedelta
from typing import Any, Dict, List, Optional

# -----------------------------------------
#  Basis – Memory-Store Handling
# -----------------------------------------

MEMORY_FILE = "memory_store.json"


def _default_memory() -> Dict[str, Any]:
    """Erzeugt eine frische Memory-Struktur."""
    return {
        "version": "1.3.4-render-autonomous",
        "notes": [
            "Platzhalter für zukünftige Persistenzdaten.",
            "Lotto-Echos, Fokus-Logs, einfache Autonomous-States.",
        ],
        "lotto": {
            "super6": [],          # Liste von Ziehungen
            "spiel77": [],         # Liste von Ziehungen
            "eurojackpot_echo": [] # Liste von Echo-Scans
        },
        "meta": {
            "last_cleanup": None
        }
    }


def load_memory() -> Dict[str, Any]:
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return _default_memory()
    except json.JSONDecodeError:
        # Falls kaputt: sanft neu starten
        return _default_memory()


def save_memory(data: Dict[str, Any]) -> None:
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# -----------------------------------------
#  Lotto – Super 6
# -----------------------------------------

def simulate_super6_draw() -> List[str]:
    """Erzeugt eine 6-stellige Super-6 Zahl (0–9 je Stelle)."""
    return [str(random.randint(0, 9)) for _ in range(6)]


def format_super6_draw(draw: List[str], draw_date: date, source: str) -> str:
    numbers = " ".join(draw)
    date_str = draw_date.strftime("%d.%m.%Y")
    msg = (
        "🏦 Super 6 – Simulierte Ziehung\n"
        "———————————————\n"
        f"Datum: {date_str}\n"
        f"Zahlen: {numbers}\n"
        f"Status: gespeichert · Echo aktiv\n"
        f"Quelle: {source}"
    )
    return msg


def super6_daily_auto() -> str:
    """
    'Auto-Cron' für Super 6:
    – Wenn heute schon eine Ziehung existiert → wiederverwenden
    – Sonst neue Ziehung erzeugen, speichern und ausgeben
    """
    data = load_memory()
    today = date.today()
    today_str = today.isoformat()

    history: List[Dict[str, Any]] = data["lotto"]["super6"]

    existing = next(
        (entry for entry in history if entry.get("date") == today_str),
        None,
    )

    if existing is None:
        draw = simulate_super6_draw()
        entry = {
            "date": today_str,
            "numbers": draw,
            "created_at": datetime.utcnow().isoformat() + "Z",
        }
        history.append(entry)
        data["lotto"]["super6"] = history
        save_memory(data)
        return format_super6_draw(draw, today, "Neu · Auto-Cron")
    else:
        draw = existing.get("numbers", simulate_super6_draw())
        return format_super6_draw(draw, today, "Heute bereits simuliert")


# -----------------------------------------
#  Lotto – Spiel 77
# -----------------------------------------

def simulate_spiel77() -> str:
    """Erzeugt eine 7-stellige Spiel-77 Nummer."""
    return "".join(str(random.randint(0, 9)) for _ in range(7))


def handle_spiel77() -> str:
    data = load_memory()
    today = date.today()
    today_str = today.isoformat()

    number = simulate_spiel77()
    entry = {
        "date": today_str,
        "number": number,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    data["lotto"]["spiel77"].append(entry)
    save_memory(data)

    return (
        "🎲 Spiel 77 – Simulierte Ziehung\n"
        "———————————————\n"
        f"Datum: {today.strftime('%d.%m.%Y')}\n"
        f"Nummer: {number}\n"
        "Status: gespeichert"
    )


# -----------------------------------------
#  Lotto – Eurojackpot Echo-Scan
# -----------------------------------------

def eurojackpot_echo_simulation() -> Dict[str, Any]:
    """
    Sehr einfache Echo-Simulation:
    – 5 Hauptzahlen 1..50
    – 2 Eurozahlen 1..12
    """
    main = sorted(random.sample(range(1, 51), 5))
    euro = sorted(random.sample(range(1, 13), 2))
    return {"main": main, "euro": euro}


def handle_eurojackpot_echo() -> str:
    data = load_memory()
    today = date.today()
    today_str = today.isoformat()

    result = eurojackpot_echo_simulation()
    entry = {
        "date": today_str,
        "result": result,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    data["lotto"]["eurojackpot_echo"].append(entry)
    save_memory(data)

    nums_str = ", ".join(str(n) for n in result["main"])
    euro_str = ", ".join(str(e) for e in result["euro"])

    return (
        "🔍 Echo-Scan – Eurojackpot (Simulation)\n"
        "———————————————\n"
        f"Zahlen: {nums_str}\n"
        f"Eurozahlen: {euro_str}\n"
        "Basis: deterministischer Offline-Simulator (Codex2050-Style)"
    )


# -----------------------------------------
#  Memory-Cleaner
# -----------------------------------------

def clean_memory(keep_days: int = 30) -> str:
    """
    Schneidet alte Lotto-Einträge ab.
    – keep_days: wie viele Tage Historie behalten
    """
    cutoff = date.today() - timedelta(days=keep_days)
    cutoff_str = cutoff.isoformat()

    data = load_memory()
    lotto = data.get("lotto", {})

    def _filter(entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [e for e in entries if e.get("date", "") >= cutoff_str]

    before_super6 = len(lotto.get("super6", []))
    before_77 = len(lotto.get("spiel77", []))
    before_euro = len(lotto.get("eurojackpot_echo", []))

    lotto["super6"] = _filter(lotto.get("super6", []))
    lotto["spiel77"] = _filter(lotto.get("spiel77", []))
    lotto["eurojackpot_echo"] = _filter(lotto.get("eurojackpot_echo", []))

    data["lotto"] = lotto
    data["meta"]["last_cleanup"] = datetime.utcnow().isoformat() + "Z"
    save_memory(data)

    after_super6 = len(lotto["super6"])
    after_77 = len(lotto["spiel77"])
    after_euro = len(lotto["eurojackpot_echo"])

    return (
        "🧹 Memory-Cleaner ausgeführt.\n"
        f"Super 6: {before_super6} → {after_super6}\n"
        f"Spiel 77: {before_77} → {after_77}\n"
        f"Eurojackpot Echo: {before_euro} → {after_euro}\n"
        f"Historie behalten: {keep_days} Tage"
    )


# -----------------------------------------
#  Einfacher Autonomous-Mode v2.0
#  (Business / Körperpfad / Entscheidungen)
# -----------------------------------------

try:
    # Optional: nutzt dein separates Mode-Modul, wenn vorhanden
    from codex2050_modes import detect_mode  # type: ignore
except Exception:
    def detect_mode(text: str) -> Optional[str]:
        """Fallback: sehr einfache Mode-Erkennung über Keywords."""
        t = text.lower()
        if any(k in t for k in ["liebe", "frau", "körper", "sex"]):
            return "body_love"
        if any(k in t for k in ["umsatz", "restaurant", "kunden", "miete", "vertrag"]):
            return "business"
        if any(k in t for k in ["entscheidung", "entscheiden", "weg", "pfad"]):
            return "decision"
        return None


def autonomous_response(text: str) -> Optional[str]:
    """
    Liefert eine einfache, textbasierte Antwort je nach Modus.
    Wird nur genutzt, wenn kein Lotto-Befehl gegriffen hat.
    """
    mode = detect_mode(text)
    if mode is None:
        return None

    if mode == "business":
        return (
            "📊 Autonomous-Mode: Business\n"
            "Fokus: ruhiger Cash-Flow, keine Hektik.\n"
            "– Nächster Schritt: eine konkrete Aufgabe heute fertig machen,\n"
            "  die direkt Geld oder Stabilität bringt (z.B. Bestellung, Mail, Post).\n"
        )

    if mode == "body_love":
        return (
            "🫀 Autonomous-Mode: Körper / Nähe\n"
            "Dein System priorisiert echte Begegnung statt Kopfkino.\n"
            "– Nächster Schritt: eine reale, kleine Handlung,\n"
            "  die deinen Körper beruhigt (Schlaf, Essen, kurzer Spaziergang)\n"
            "  und erst DANACH Kontakt oder Chat."
        )

    if mode == "decision":
        return (
            "⚖️ Autonomous-Mode: Entscheidung\n"
            "Wichtige Frage: Was bringt dir in 7 Tagen spürbare Entlastung?\n"
            "– Triff die Entscheidung, die diesen Effekt am klarsten auslöst.\n"
            "Keine Opfer-Romantik – nur Rückführung von Energie."
        )

    # Unbekannter Mode-Typ
    return None


# -----------------------------------------
#  Zentrale Router-Funktion für Telegram
# -----------------------------------------

def handle_message(text: str) -> str:
    """
    Zentrale Eingabe für alle Bot-Nachrichten (Webhook).
    Gibt immer einen String zurück.
    """
    t = text.strip()
    lower = t.lower()

    # 1) Hard Commands /start /help
    if lower.startswith("/start"):
        return (
            "🟦 Codex2050 Super – Render Bot\n"
            "Autonomous Engine v2.0 ist aktiv.\n\n"
            "Befehle:\n"
            "• super6  → tägliche Super-6 Ziehung (Auto-Cron)\n"
            "• spiel77 → Spiel-77 Simulation\n"
            "• echo    → Eurojackpot Echo-Scan\n"
            "• clean   → Memory-Cleaner (alte Einträge kürzen)\n"
            "Sonst: freie Texte → einfacher Autonomous-Modus\n"
        )

    if lower.startswith("/help"):
        return (
            "ℹ️ Hilfe – Codex2050 Super\n"
            "Sende z.B.:\n"
            "• super6\n"
            "• spiel77\n"
            "• echo\n"
            "• clean\n"
            "oder einen freien Text zu Business / Körper / Entscheidung."
        )

    # 2) Lotto – Super6 (inkl. Auto-Cron)
    if "super6" in lower or "super 6" in lower:
        return super6_daily_auto()

    # 3) Lotto – Spiel 77
    if "spiel77" in lower or "spiel 77" in lower or lower == "77":
        return handle_spiel77()

    # 4) Lotto – Eurojackpot Echo-Scan
    if "echo" in lower or "eurojackpot" in lower or "euro" in lower:
        return handle_eurojackpot_echo()

    # 5) Memory-Cleaner
    if "clean" in lower or "cleanup" in lower or "cleaner" in lower:
        return clean_memory(keep_days=30)

    # 6) Autonomous-Mode (Business / Körperpfad / Entscheidung)
    auto = autonomous_response(text)
    if auto is not None:
        return auto

    # 7) Fallback
    return (
        "Codex2050–Super aktiv.\n"
        "Sende `super6`, `spiel77`, `echo`, `clean` oder einen freien Text."
    )
