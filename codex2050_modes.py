from typing import Optional


def detect_mode(text: str) -> Optional[str]:
    """
    Sehr einfacher Modus-Detektor.
    Keine festen Personennamen – nur Themenfelder.
    """
    t = text.lower()

    # Liebe / Frauen / Beziehung
    if any(k in t for k in ["liebe", "frau", "frauen", "beziehung", "nähe", "alleine", "einsam", "herz", "crush"]):
        return "liebe"

    # Business / Arbeit / Restaurant / Projekt
    if any(k in t for k in ["business", "firma", "restaurant", "projekt", "umsatz", "kunden", "vertrag", "mieter", "miete"]):
        return "business"

    # Geld / Rechnungen / Schulden
    if any(k in t for k in ["geld", "rechnung", "miete", "schulden", "konto", "dispo", "mahnung"]):
        return "geld"

    # Körper / Fitness / Müdigkeit
    if any(k in t for k in ["körper", "müde", "erschöpft", "fitness", "sport", "krank", "energie"]):
        return "körper"

    return None
