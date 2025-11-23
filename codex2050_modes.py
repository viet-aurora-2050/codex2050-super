
from typing import Optional
from codex2050_engine import Codex2050Engine


def detect_mode_from_text(text: str) -> Optional[int]:
    """
    Versucht, aus einem Text eine Stufe (1–6) zu erkennen.
    Erlaubt z.B.:
    - "1"
    - "Stufe 2"
    - "stufe 3"
    """
    t = (text or "").strip().lower()

    # /start und "start" nie als Modus interpretieren
    if t in {"/start", "start"}:
        return None

    for i in range(1, 7):
        # "1" oder "stufe 1"
        if t == str(i) or t.replace("stufe", "").strip() == str(i):
            return i

    return None


def handle_message(text: str, engine: Codex2050Engine, state: dict) -> str:
    """
    Zentrale Routing-Funktion.
    `state` ist ein einfaches Dict pro Chat-ID, das in main.py
    aus einem globalen Dict geholt wird.
    """
    t = (text or "").strip()

    # -------------------------
    # 1) RESET – GANZ OBEN
    # -------------------------
    if t.lower().startswith("/reset") or t.lower() == "reset":
        state.clear()
        return (
            "🔄 Reset durchgeführt. Alle Zwischenschritte für diesen Chat wurden gelöscht.

"
            "Aktive Stufen (Codex2050 – final3):
"
            "1. Stufe 1 – Check-In
"
            "2. Stufe 2 – Dunkelblauer Zukunftsmodus
"
            "3. Stufe 3 – Imperator-Pfad
"
            "4. Stufe 4 – Lola x Iki
"
            "5. Stufe 5 – Codex / Archiv
"
            "6. Stufe 6 – Kettenbrecher-Modus

"
            "Schreib z.B. `Stufe 2` oder `2`, um in diesen Modus zu gehen."
        )

    # -------------------------
    # 2) START
    # -------------------------
    if t.lower().startswith("/start"):
        state.clear()
        # engine.list_stufen() gibt bereits eine Stufenliste zurück
        try:
            stufen_text = engine.list_stufen()
        except Exception:
            stufen_text = (
                "Aktive Stufen (Codex2050 – final3):\n"
                "1. Stufe 1 – Check-In\n"
                "2. Stufe 2 – Dunkelblauer Zukunftsmodus\n"
                "3. Stufe 3 – Imperator-Pfad\n"
                "4. Stufe 4 – Lola x Iki\n"
                "5. Stufe 5 – Codex / Archiv\n"
                "6. Stufe 6 – Kettenbrecher-Modus"
            )

        return "Codex2050 Render-Bot ist aktiv. 🔥\n\n" + stufen_text

    # -------------------------
    # 3) STUFE WECHSELN?
    # -------------------------
    mode = detect_mode_from_text(t)
    if mode is not None:
        state["mode"] = mode

        # Spezielle Logik für Stufe 1 (Check-In mit Folgefrage)
        if mode == 1:
            state["awaiting_checkin"] = True
            try:
                return engine.handle_checkin(t)
            except Exception:
                return (
                    "Stufe 1 – Check-In\n\n"
                    "Schreib kurz, wie es dir geht (1–2 Sätze)."
                )

        # Alle anderen Stufen: kurze Erklärung
        try:
            return engine.mode_reply(mode, t)
        except Exception:
            # Fallback, falls ältere Engine-Version keine mode_reply hat
            if mode == 2:
                return (
                    "Stufe 2 – Dunkelblauer Zukunftsmodus\n\n"
                    "Heute zählt nur: Schlaf, Essen, eine kleine Aufgabe. "
                    "Schreib mir, was realistisch das Wichtigste ist (1–2 Sätze)."
                )
            if mode == 3:
                return (
                    "Stufe 3 – Imperator-Pfad\n\n"
                    "Schreib eine Sache, bei der du heute führen / entscheiden willst. "
                    "Ich spiegel dir Risiko vs. Ruhe."
                )
            if mode == 4:
                return (
                    "Stufe 4 – Lola x Iki\n\n"
                    "Schreib eine Sache, die heute direkt hilft: Gast, Post, Lieferant, Rechnung. "
                    "Ich zeige dir, was davon am klarsten / einfachsten ist."
                )
            if mode == 5:
                return (
                    "Stufe 5 – Codex / Archiv\n\n"
                    "Schreib Stichworte, die du archivieren willst (mit Kommas getrennt). "
                    "Ich sortiere sie für dich."
                )
            if mode == 6:
                return (
                    "Stufe 6 – Kettenbrecher-Modus\n\n"
                    "Schreib das Ketten-Thema in 1–3 Sätzen. "
                    "Ich helfe dir, den nächsten kleinen Gegen-Move zu sehen."
                )
            return "Stufe geändert, aber diese Engine-Version kennt keine Details zu dieser Stufe."

    # -------------------------
    # 4) KONTEXTABHÄNGIGE ANTWORTEN
    # -------------------------
    current_mode = state.get("mode")

    # Stufe 1 – Check-In (Follow-up)
    if current_mode == 1 and state.get("awaiting_checkin"):
        state["awaiting_checkin"] = False
        try:
            return engine.handle_checkin(t)
        except Exception:
            return (
                "Danke für dein Check-In.\n"
                "Ich habe es gespeichert – jetzt kleine nächste Handlung: "
                "Was ist heute der minimal wichtige Schritt?"
            )

    # Stufe 2 – Dunkelblauer Zukunftsmodus
    if current_mode == 2:
        try:
            return engine.handle_dunkelblau(t)
        except Exception:
            return (
                "Dunkelblauer Zukunftsmodus:\n"
                "Such dir genau EINE Sache aus, die heute machbar ist. "
                "Schreib sie in einem Satz."
            )

    # Stufe 3 – Imperator-Pfad
    if current_mode == 3:
        try:
            return engine.handle_imperator(t)
        except Exception:
            return (
                "Imperator-Pfad:\n"
                "Schreib: (1) Situation, (2) deine Wahrheit, (3) dein nächster Schritt."
            )

    # Stufe 4 – Lola x Iki
    if current_mode == 4:
        try:
            return engine.handle_lola(t)
        except Exception:
            return (
                "Lola x Iki – Betriebsmodus:\n"
                "Nenn mir kurz eine konkrete Aufgabe (Gast, Rechnung, Lieferant, Social)."
            )

    # Stufe 5 – Codex / Archiv
    if current_mode == 5:
        parts = [p.strip() for p in t.split(",") if p.strip()]
        if not parts:
            return "Gib ein paar Stichworte, getrennt durch Kommas."
        parts_sorted = sorted(parts, key=lambda x: x.lower())
        bullet_list = "\n".join(f"- {p}" for p in parts_sorted)
        return "Archiv‑Eintrag:\n\n" + bullet_list

    # Stufe 6 – Kettenbrecher-Modus
    if current_mode == 6:
        try:
            return engine.handle_kettenbrecher(t)
        except Exception:
            return (
                "Kettenbrecher-Modus:\n"
                "Schreib mir das Muster / die Kette kurz auf – ich formuliere dir eine Gegen-Bewegung."
            )

    # -------------------------
    # 5) DEFAULT-FALLBACK
    # -------------------------
    try:
        stufen_text = engine.list_stufen()
    except Exception:
        stufen_text = (
            "Aktive Stufen (Codex2050 – final3):\n"
            "1. Stufe 1 – Check-In\n"
            "2. Stufe 2 – Dunkelblauer Zukunftsmodus\n"
            "3. Stufe 3 – Imperator-Pfad\n"
            "4. Stufe 4 – Lola x Iki\n"
            "5. Stufe 5 – Codex / Archiv\n"
            "6. Stufe 6 – Kettenbrecher-Modus"
        )

    return (
        "Ich habe dich verstanden, aber ordne es gerade keiner Stufe zu.\n\n"
        + stufen_text
    )
