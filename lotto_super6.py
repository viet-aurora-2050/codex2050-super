import random
from datetime import date


def super6_simulation() -> str:
    """
    Offline-Simulator für Super 6:
    deterministische 6-stellige Zahl pro Tag.
    KEIN echter Ziehungsdienst.
    """
    today = date.today().isoformat()
    rnd = random.Random()
    rnd.seed(f"super6-{today}")
    digits = [str(rnd.randint(0, 9)) for _ in range(6)]
    return "".join(digits)
