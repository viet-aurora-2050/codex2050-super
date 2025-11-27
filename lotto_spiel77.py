import random
from datetime import date


def spiel77_simulation() -> str:
    """
    Offline-Simulator für Spiel 77:
    deterministische 7-stellige Zahl pro Tag.
    KEIN echter Ziehungsdienst.
    """
    today = date.today().isoformat()
    rnd = random.Random()
    rnd.seed(f"spiel77-{today}")
    digits = [str(rnd.randint(0, 9)) for _ in range(7)]
    return "".join(digits)
