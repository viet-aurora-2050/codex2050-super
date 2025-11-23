from typing import Optional
from codex2050_engine import Codex2050Engine

def detect_mode_from_text(text: str) -> Optional[int]:
    t = text.strip().lower()
    if t in {"/start", "start"}:
        return None
    # Zahl oder "stufe x"
    for i in range(1, 7):
        if t == str(i) or t.replace("stufe", "").strip() == str(i):
            return i
    return None

def handle_message(text: str, engine: Codex2050Engine, state: dict) -> str:
    """
    Zentrale Routing-Funktion.
    `state` ist ein einfaches Dict pro Chat (persistiert NICHT serverseitig – reiner RAM).
    """
    t = (text or "").strip()

    # Start
    if t.startswith("/start"):
        state.clear()
        return (
            "Codex2050 Render‑Bot ist aktiv. 🔥\n\n"
            + engine.list_stufen()
        )

    # Stufe wechseln?
    mode = detect_mode_from_text(t)
    if mode is not None:
        state["mode"] = mode
        if mode == 1:
            state["awaiting_checkin"] = True
            return engine.handle_checkin(t)
        return engine.mode_reply(mode, t)

    # Kontextabhängige Antworten
    current_mode = state.get("mode")

    # Stufe 1: nach dem ersten Prompt die Antwort spiegeln
    if current_mode == 1 and state.get("awaiting_checkin"):
        state["awaiting_checkin"] = False
        return engine.reflect_checkin_answer(t)

    # Stufe 5: Archiv – Stichworte sortieren
    if current_mode == 5:
        parts = [p.strip() for p in t.split(",") if p.strip()]
        if not parts:
            return "Gib ein paar Stichworte, getrennt durch Kommas."
        parts_sorted = sorted(parts, key=lambda x: x.lower())
        bullet_list = "\n".join(f"- {p}" for p in parts_sorted)
        return "Archiv‑Eintrag:\n\n" + bullet_list

    # Default-Fallback: einfach erneut Stufenliste ausgeben
    return (
        "Ich habe dich verstanden, aber ordne es gerade keiner Stufe zu.\n\n"
        + engine.list_stufen()
    )
