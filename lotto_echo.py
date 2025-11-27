import random
from datetime import date


def eurojackpot_echo_simulation():
    """
    Offline-Echo-Simulator für Eurojackpot:
    5 aus 50 + 2 aus 12, deterministisch pro Tag.
    KEIN echter Ziehungsdienst.
    """
    today = date.today().isoformat()
    rnd = random.Random()
    rnd.seed(f"eurojackpot-{today}")

    main_numbers = sorted(rnd.sample(range(1, 51), 5))
    euro_numbers = sorted(rnd.sample(range(1, 13), 2))
    return main_numbers, euro_numbers
