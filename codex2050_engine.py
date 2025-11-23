import datetime

class Codex2050Engine:
    """
    Kleine Text-Engine für deinen Codex2050-Bot.
    Nichts von hier berührt echte Konten, Geld oder externe Systeme.
    Es ist reine Textlogik.
    """

    def __init__(self):
        self.version = "final3"
        self.stufen = self._build_stufen()

    def _build_stufen(self):
        # Nur kurze, sichere Beschreibungen – keine Versprechen, kein Geld.
        return {
            1: {
                "name": "Stufe 1 – Check‑In",
                "desc": (
                    "Kurzer Status‑Check: Wie geht es dir, Körper / Geld / Kopf?\n"
                    "Ich antworte mit einer kompakten Spiegelung und 1 Mini‑Aufgabe."
                ),
            },
            2: {
                "name": "Stufe 2 – Dunkelblauer Zukunftsmodus",
                "desc": (
                    "Fokus auf Schutz, Ruhe, Schlaf, realistische Schritte.\n"
                    "Kein Druck, keine Überforderung – nur das Nötigste für heute."
                ),
            },
            3: {
                "name": "Stufe 3 – Imperator‑Pfad",
                "desc": (
                    "Erinnert dich an deinen Imperator‑Modus: Präsenz, Körper, Klarheit.\n"
                    "Antwort ist immer: Was ist der nächste kleine, würdige Schritt?"
                ),
            },
            4: {
                "name": "Stufe 4 – Lola x Iki",
                "desc": (
                    "Hier geht es nur um das Projekt / Restaurant.\n"
                    "Ich spiegel dir: Was heute real Umsatz, Stabilität oder Sichtbarkeit bringt."
                ),
            },
            5: {
                "name": "Stufe 5 – Codex / Archiv",
                "desc": (
                    "Reflexions‑Stufe: Ich helfe, Gedanken zu sortieren wie ein Archiv.\n"
                    "Keine Entscheidungen, nur Struktur und Klarheit."
                ),
            },
            6: {
                "name": "Stufe 6 – Kettenbrecher‑Modus",
                "desc": (
                    "Wenn du Kettenbrech‑Thema schreibst, reagiere ich direkt, klar, ohne Deko.\n"
                    "Ziel: Muster erkennen und mindestens eine konkrete Alternative formulieren."
                ),
            },
        }

    def list_stufen(self):
        lines = ["Aktive Stufen (Codex2050 – final3):"]
        for i in range(1, 7):
            s = self.stufen[i]
            lines.append(f"{i}. {s['name']}")
        lines.append("\nSchreib z.B. `Stufe 2` oder `2`, um in diesen Modus zu gehen.")
        return "\n".join(lines)

    def get_stufe_info(self, n: int) -> str:
        s = self.stufen.get(n)
        if not s:
            return "Diese Stufe gibt es nicht. Gültig sind 1–6."
        return f"{s['name']}\n\n{s['desc']}"

    def handle_checkin(self, text: str) -> str:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        return (
            "Stufe 1 – Check‑In\n"
            f"Zeitstempel: {now}\n\n"
            "Schreib mir in EINEM Satz:\n"
            "Körper / Geld / Kopf – je ein Wort.\n\n"
            "Ich antworte dann mit einer knappen Spiegelung + 1 Mini‑Aufgabe."
        )

    def reflect_checkin_answer(self, text: str) -> str:
        # sehr einfache Spiegelung ohne Psychotricks
        return (
            "Gesehen. Dein Satz war:\n"
            f"»{text.strip()}«\n\n"
            "Mini‑Aufgabe (heute, nicht perfekt, nur mini):\n"
            "➡  Triff EINE Entscheidung, die dir ein bisschen Druck nimmt "
            "oder ein bisschen Geld / Ruhe bringt."
        )

    def mode_reply(self, mode: int, text: str) -> str:
        # Hier nur sehr einfache, sichere Logik – kein Coaching, keine Heilsversprechen.
        if mode == 2:
            return (
                "Stufe 2 – Dunkelblauer Zukunftsmodus\n\n"
                "Heute zählt nur: Schlaf, Essen, 1 kleine Aufgabe.\n"
                "Schreib mir, was heute REALISTISCH das Wichtigste ist (max. 1–2 Sätze)."
            )
        if mode == 3:
            return (
                "Stufe 3 – Imperator‑Pfad\n\n"
                "Imperator heißt nicht Drama, sondern: kein Selbstverrat.\n"
                "Formuliere einen Satz: *Was lasse ich heute NICHT mehr mit mir machen?*"
            )
        if mode == 4:
            return (
                "Stufe 4 – Lola x Iki\n\n"
                "Schreib eine Sache, die heute direkt hilft: Gast, Post, Lieferant, Rechnung.\n"
                "Ich spiegele dir, was davon am klarsten / einfachsten ist."
            )
        if mode == 5:
            return (
                "Stufe 5 – Codex / Archiv\n\n"
                "Schreib Stichworte, die du archivieren willst (mit Kommas getrennt).\n"
                "Ich packe sie in eine sortierte Liste zurück."
            )
        if mode == 6:
            return (
                "Stufe 6 – Kettenbrecher\n\n"
                "Schreib mir das Ketten‑Thema in 1–3 Sätzen.\n"
                "Ich antworte mit: (1) Worin genau die Kette besteht, "
                "(2) einem möglichen Gegen‑Move."
            )
        return self.get_stufe_info(mode)
