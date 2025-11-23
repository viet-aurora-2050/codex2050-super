
import logging
from datetime import datetime

logger = logging.getLogger("codex2050-engine")


class Codex2050Engine:
    """
    Einfache 2050-Engine mit Chat-Memory.

    Pro chat_id wird ein State gehalten:
      - mode:      "default", "dark_blue", "work"
      - last_goal: letzter formuliertes Ziel / Fokus
      - last_msg:  letzte Nachricht des Users (debug / Kontext)
      - created_at / updated_at: Timestamps
    """

    def __init__(self):
        # chat_id -> state-dict
        self.memory = {}

    # ----------------- intern: State-Handling -----------------

    def _get_state(self, chat_id: int) -> dict:
        if chat_id not in self.memory:
            self.memory[chat_id] = {
                "mode": "default",
                "last_goal": None,
                "last_msg": None,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
        return self.memory[chat_id]

    def _update_state(self, chat_id: int, **kwargs):
        state = self._get_state(chat_id)
        state.update(kwargs)
        state["updated_at"] = datetime.utcnow()
        self.memory[chat_id] = state

    # ----------------- Public API -----------------

    def process(self, update: dict) -> str:
        """
        Haupteinstiegspunkt. Bekommt den Telegram-Update-JSON.
        Gibt einen Text zurück, der an den User geschickt wird.
        """

        message = update.get("message", {}) or {}
        chat = message.get("chat", {}) or {}
        chat_id = chat.get("id")

        if chat_id is None:
            logger.warning("Update ohne chat_id erhalten.")
            return "Ich habe dich gehört, aber mir fehlt die Chat-ID. (Systemfehler)."

        text = (message.get("text") or "").strip()
        state = self._get_state(chat_id)

        logger.info(f"[{chat_id}] Eingehender Text: {text!r}, State: {state}")

        # 1) Systemkommandos zuerst behandeln
        if text.startswith("/"):
            return self._handle_command(chat_id, text, state)

        # 2) Modus-Wechsel anhand von Keywords
        lowered = text.lower()
        if "dunkelblau" in lowered or "stufe 2" in lowered:
            self._update_state(chat_id, mode="dark_blue")
            return (
                "Dunkelblauer Zukunftsmodus ist aktiv.\n\n"
                "Regel heute: Schlaf, Essen, eine kleine Aufgabe.\n"
                "Schreib mir in einem Satz, was heute wirklich das Wichtigste ist."
            )

        if "arbeit" in lowered or "lola" in lowered:
            self._update_state(chat_id, mode="work")
            return (
                "Arbeitsmodus aktiv (Lola x Iki / Geld / Struktur).\n"
                "Formuliere eine konkrete Aufgabe in einem Satz, z.B.:\n"
                "„Offene Rechnung mit X klären“ oder „Post an Hausverwaltung beantworten“."
            )

        # 3) Instinkt-/Energie-Schutz
        if any(
            key in lowered
            for key in [
                "kein bock",
                "keine energie",
                "müde",
                "überfordert",
                "leer",
                "kaputt",
            ]
        ):
            self._update_state(chat_id, last_msg=text)
            return (
                "Dein Instinkt sagt gerade: Stopp / keine Energie.\n\n"
                "Dann gilt heute: Dunkelblauer Modus light.\n"
                "➡ 1. Etwas essen oder trinken.\n"
                "➡ 2. Kurz hinlegen / atmen.\n"
                "➡ 3. Erst danach eine Mini-Aufgabe. Nicht mehr.\n\n"
                "Wenn du magst, schreib mir die kleinste Aufgabe, die du noch akzeptieren kannst "
                "(ein Satz)."
            )

        # 4) je nach Modus unterschiedlich antworten
        mode = state.get("mode", "default")
        if mode == "dark_blue":
            return self._handle_dark_blue(chat_id, text, state)
        elif mode == "work":
            return self._handle_work(chat_id, text, state)
        else:
            return self._handle_default(chat_id, text, state)

    # ----------------- Kommandos -----------------

    def _handle_command(self, chat_id: int, text: str, state: dict) -> str:
        cmd = text.split()[0].lower()

        if cmd == "/start":
            return (
                "Codex2050 Autonomous-Modus ist aktiv.\n\n"
                "Du kannst einfach schreiben, was heute für dich wichtig ist "
                "(z.B. „Mit Pati klären“, „Hausverwaltung“, „Schlaf nachholen“).\n\n"
                "Wenn du Ruhe brauchst, schreib „dunkelblau“.\n"
                "Wenn es um Arbeit/Geld geht, schreib „Lola“ oder „Arbeit“.\n"
                "Mit /reset kannst du den heutigen State zurücksetzen."
            )

        if cmd == "/reset":
            if chat_id in self.memory:
                del self.memory[chat_id]
            return (
                "State für diesen Chat wurde zurückgesetzt.\n"
                "Neuer Start. Was ist JETZT gerade das Wichtigste (ein Satz)?"
            )

        if cmd == "/state":
            st = self._get_state(chat_id)
            return (
                "Aktueller Codex2050-State:\n"
                f"- Modus: {st.get('mode')}\n"
                f"- Letztes Ziel: {st.get('last_goal')}\n"
                f"- Zuletzt aktualisiert: {st.get('updated_at')}\n"
            )

        return "Befehl kenne ich nicht. Wichtiger ist: Was brauchst du jetzt konkret?"

    # ----------------- Default-Handling -----------------

    def _handle_default(self, chat_id: int, text: str, state: dict) -> str:
        last_goal = state.get("last_goal")

        if not last_goal:
            self._update_state(chat_id, last_goal=text, last_msg=text)
            return (
                f"Okay. Ich nehme das als deinen aktuellen Fokus:\n\n"
                f"→ {text}\n\n"
                "Schreib mir jetzt den nächsten kleinsten Schritt dazu "
                "(eine konkrete Handlung, die max. 10–20 Minuten braucht)."
            )

        self._update_state(chat_id, last_msg=text)

        if any(word in text.lower() for word in ["erledigt", "geschafft", "fertig", "done"]):
            return (
                f"Gut. Fortschritt am Ziel:\n→ {last_goal}\n\n"
                "Wenn du willst, definieren wir jetzt eine neue Mini-Aufgabe dazu, "
                "oder du setzt ein neues Ziel mit einem Satz."
            )

        return (
            f"Fokus bleibt:\n→ {last_goal}\n\n"
            f"Dein letzter Input dazu:\n→ {text}\n\n"
            "Formuliere JETZT bitte eine konkrete Aktion daraus "
            "(z.B. „X anrufen“, „Mail an Y schreiben“, „Dokument Z öffnen“)."
        )

    # ----------------- Dark-Blue-Handling -----------------

    def _handle_dark_blue(self, chat_id: int, text: str, state: dict) -> str:
        last_goal = state.get("last_goal")

        if not last_goal:
            self._update_state(chat_id, last_goal=text, last_msg=text)
            return (
                "Alles klar. Ich setze das leise als deinen heutigen Fokus:\n"
                f"→ {text}\n\n"
                "Mehr musst du heute nicht beweisen.\n"
                "Wenn du magst, schreib mir eine einzige Mini-Aktion dazu "
                "(max. 5–10 Minuten), ansonsten reicht es, dass du es benannt hast."
            )

        self._update_state(chat_id, last_msg=text)
        if any(word in text.lower() for word in ["erledigt", "geschafft", "done", "fertig"]):
            return (
                f"Fein. Für den dunkelblauen Modus reicht das vollkommen.\n"
                f"Fokus war:\n→ {last_goal}\n\n"
                "Jetzt ist offiziell Pause. Essen, warmes Trinken, Körper runterfahren.\n"
                "Wenn später noch Energie da ist, melde dich – sonst ist es für heute genug."
            )

        return (
            f"Wir bleiben im Schutzmodus.\n\n"
            f"Aktueller Fokus:\n→ {last_goal}\n\n"
            "Frag dich ehrlich: Schaffst du HEUTE eine einzige kleine Aktion dafür?\n"
            "Wenn ja, schreib sie mir in einem Satz. Wenn nein, schreib einfach „keine Energie“, "
            "dann verschiebe ich es systemisch auf später."
        )

    # ----------------- Work-Handling -----------------

    def _handle_work(self, chat_id: int, text: str, state: dict) -> str:
        last_goal = state.get("last_goal")

        if not last_goal:
            self._update_state(chat_id, last_goal=text, last_msg=text)
            return (
                "Arbeitsmodus aktiv.\n"
                f"Ich setze das als aktuelle Hauptaufgabe:\n→ {text}\n\n"
                "Was ist der erste konkrete Schritt dafür? (z.B. „Mail an X schreiben“, "
                "„Zettel Y suchen“, „Person Z anrufen“)."
            )

        self._update_state(chat_id, last_msg=text)

        if any(word in text.lower() for word in ["erledigt", "geschickt", "abgeschickt", "bezahlt"]):
            return (
                f"Gut. Nüchtern betrachtet:\n"
                f"→ Aufgabe `{last_goal}` hat Bewegung.\n\n"
                "Such dir jetzt die nächste kleine Geld-/Lola-Aufgabe oder sag mir, "
                "wenn heute Schluss ist mit Arbeit."
            )

        return (
            f"Work-Fokus bleibt:\n→ {last_goal}\n\n"
            f"Dein letzter Input:\n→ {text}\n\n"
            "Ich empfehle dir, die Aufgabe jetzt in einen 10–20-Minuten-Block zu pressen.\n"
            "Schreib mir EINE Aktion, die du direkt danach machen kannst. Nicht planen – ausführen."
        )
