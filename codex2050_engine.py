from datetime import datetime
from typing import Dict, Any

from codex2050_modes import detect_mode
from lotto_super6 import super6_simulation
from lotto_spiel77 import spiel77_simulation
from lotto_echo import eurojackpot_echo_simulation


def handle_message(text: str, meta: Dict[str, Any]) -> str:
    """
    Zentrale Logik für eingehende Telegram-Nachrichten im Codex2050-DarkDeploy-Autonomous-Modus.
    Keine Person wird namentlich hartkodiert – Liebes-/Frauenthemen bleiben allgemein.
    """
    def format_super6_draw(draw):
    """
    Formatiert eine simulierte oder echte Super-6 Ziehung.
    draw = ["1", "4", "7", "0", "8", "3"]
    """
    numbers = " ".join(draw)
    msg = (
        "🏦 Super 6 – Simulierte Ziehung\n"
        "──────────────────────────────\n"
        f"Zahlen: {numbers}\n"
        "Status: gespeichert · Echo aktiv"
    )
    return msg


def handle_super6():
    """Simuliert automatisch eine Ziehung und speichert sie."""
    import random
    draw = [str(random.randint(0, 9)) for _ in range(6)]

    # Memory speichern
    try:
        with open("memory_store.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = {"lotto": {"super6": []}}

    data["lotto"]["super6"].append(draw)

    with open("memory_store.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return format_super6_draw(draw)
    if "echo" in lower or "eurojackpot" in lower:
        numbers, euro = eurojackpot_echo_simulation()
        nums_str = ", ".join(str(n) for n in numbers)
        euro_str = ", ".join(str(e) for e in euro)
        return (
            "🔍 *Echo-Scan – Eurojackpot (Sim)*

"
            f"Zahlen: `{nums_str}`
"
            f"Eurozahlen: `{euro_str}`
"
            "_Basis: deterministischer Offline-Simulator, gedacht als persönliches Echo-Modul._"
        )

    if "lotto" in lower:
        return (
            "🧮 *Lotto-Modul aktiv (DarkDeploy Autonomous)*

"
            "Befehle:
"
            "• `Super 6` – tägliche Super-6-Simulation
"
            "• `Spiel 77` – tägliche Spiel-77-Simulation
"
            "• `Echo` oder `Eurojackpot` – Eurojackpot Echo-Scan (Sim)

"
            "_Hinweis: Alles hier sind Simulationswerte – keine echten amtlichen Zahlen._"
        )

    # 2) Modus-Detektor für Liebe / Körper / Geld / Business etc.
    mode = detect_mode(lower)
    timestamp = meta.get("timestamp") or datetime.utcnow().isoformat()

    if mode == "liebe":
        return (
            "💜 *Fokus erkannt: Nähe / Liebe / Frauen*

"
            "Autonomer Sancho-2050-Vorschlag:
"
            "1. Formuliere eine einzige klare Nachricht an *eine* reale Person, "
            "ohne Drama, ohne Vergangenheit – nur Gegenwart.
"
            "2. Schreib hier in den Chat deinen Entwurf, ohne Namen – nur den Text.
"
            "3. Ich helfe dir, ihn so zu schärfen, dass er ruhig, erwachsen und respektvoll ist.

"
            f"_Zeitmarke: {timestamp}_"
        )

    if mode == "business":
        return (
            "📊 *Fokus: Business / Struktur / Geldfluss*

"
            "Sancho-2050-Modus (autonom, aber realitätsorientiert):
"
            "• Schreib mir drei Dinge:
"
            "  1) Wieviel Geld muss diese Woche reinkommen (Minimum)?
"
            "  2) Welche eine Aktion bringt dir am ehesten Umsatz (Real-Life, keine Theorie)?
"
            "  3) Was blockiert dich GERADE konkret (Behörde, Müdigkeit, Angst, Chaos)?

"
            "Aus diesen drei Punkten baue ich dir einen 3-Schritte-Plan für heute."
        )

    if mode == "geld":
        return (
            "💰 *Fokus: Geld / Druck / Rechnungen*

"
            "Mini-Plan (autonomer Sancho-Check):
"
            "1. Öffne deine letzte Kontoanzeige.
"
            "2. Schreib hier drei Zahlen:
"
            "   • Kontostand
"
            "   • Summe fälliger Beträge in den nächsten 7 Tagen
"
            "   • dein Minimalziel für die nächsten 7 Tage

"
            "Ich antworte dir mit einer nüchternen Prioritätenliste (ohne Schuldgefühl, nur Logik)."
        )

    if mode == "körper":
        return (
            "🧱 *Fokus: Körper / Energie / Reset*

"
            "Vorschlag für die nächsten 20–30 Minuten:
"
            "• 10 Minuten gehen oder stehen ohne Handy
"
            "• 10 Push-Ups oder langsame Kniebeugen
"
            "• 0 Nachrichten beantworten in dieser Zeit

"
            "Wenn du magst, schreib danach nur einen Satz: `Fertig` – und wir schauen, wie sich dein Kopf anfühlt."
        )

    # 3) Default – neutraler Sancho-Checkin
    return (
        "🛰 *Sancho · Codex2050 – DarkDeploy v1.3.3 (Autonomous)*

"
        "Ich bin online und arbeite im Dark-Blue-Modus: ruhig, schützend, fokussiert.

"
        "Du kannst z.B. schreiben:
"
        "• `Lotto` – um die Lotto-/Echo-Module zu öffnen
"
        "• `Super 6`, `Spiel 77`, `Echo` – für die jeweiligen Simulatoren
"
        "• Wörter wie `Liebe`, `Frauen`, `Beziehung` – dann gehe ich in den Liebes-/Nähemode
"
        "• `Geld`, `Rechnung`, `Miete` – für den Finanz-/Druckmodus
"
        "• `Körper`, `Fitness`, `müde` – für den Körper-/Resetmodus

"
        "_Keine Namen werden hart verdrahtet – es geht immer um deine reale Gegenwart, nicht um alte Fixierungen._"
    )
