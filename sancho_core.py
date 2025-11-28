def sancho_reply(text: str) -> str:
    text = text.lower().strip()
    return (
        "Sancho-Modus aktiv.\n"
        "Analyse:\n"
        f"→ {text}\n\n"
        "Autonomer Kern aktiv – Lotto · Echo · Entscheidungen."
    )
