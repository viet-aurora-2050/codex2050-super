# AutonomousCore – Minimaler Autonomie-Layer v1.3.1
# Hier kannst du später komplexere Zustandslogik einbauen.

class AutonomousCore:
    def __init__(self):
        self.state = {
            "version": "v1.3.1-HYBRID-C",
            "messages_seen": 0,
        }

    def process(self, text: str):
        self.state["messages_seen"] += 1
        tag = "neutral"
        t = (text or "").lower()

        if "angst" in t or "stress" in t:
            tag = "schutz"
        elif "idee" in t or "plan" in t:
            tag = "strategie"
        elif "frau" in t or "pati" in t or "körper" in t:
            tag = "körperpfad"

        self.state["last_tag"] = tag
        self.state["last_text"] = text

        return {
            "tag": tag,
            "messages_seen": self.state["messages_seen"],
        }
