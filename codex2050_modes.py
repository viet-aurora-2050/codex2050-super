# Codex2050 Modes – Simple Resolver v1.3.1

def resolve_mode(text: str) -> str:
    if not text:
        return "default"

    t = text.lower().strip()

    if "/start" in t or "start" == t:
        return "checkin"
    if "lola" in t or "iki" in t:
        return "lola-x-iki"
    if "geld" in t or "money" in t or "cash" in t:
        return "money"
    if "pati" in t or "liebe" in t or "love" in t:
        return "love"
    if "sancho" in t and "vision" in t:
        return "sancho-vision"
    if "dunkelblau" in t or "darkblue" in t:
        return "darkblue"
    if "kettenbrecher" in t:
        return "chains"

    return "default"
