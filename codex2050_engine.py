import json
import random

def format_super6_draw(draw):
    numbers = " ".join(draw)
    msg = (
        "🏦 Super 6 – Simulierte Ziehung\n"
        "──────────────────────────────\n"
        f"Zahlen: {numbers}\n"
        "Status: gespeichert · Echo aktiv"
    )
    return msg

def handle_super6():
    draw = [str(random.randint(0,9)) for _ in range(6)]
    try:
        with open("memory_store.json","r",encoding="utf-8") as f:
            data=json.load(f)
    except:
        data={"lotto":{"super6":[],"spiel77":[],"eurojackpot_echo":[]}}

    data["lotto"]["super6"].append(draw)
    with open("memory_store.json","w",encoding="utf-8") as f:
        json.dump(data,f,indent=4,ensure_ascii=False)
    return format_super6_draw(draw)

def handle_message(text):
    t=text.lower().strip()
    if "super6" in t or "super 6" in t:
        return handle_super6()
    return "Codex2050-Super aktiv."
