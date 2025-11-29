
# AURORA 2050 – STUFE 11: CODEX-GEHIRN AKTIV
# Integrierter Master-Kopf aus Codex-Stufen 4–10

from stufe4_codex_memory import CODEX_MEM
from stufe5_user_profiles import USER_PROFILES
from stufe6_signal_detector import SIGNAL_WORDS
from stufe7_market_module import MARKT
from stufe8_emotion_engine import EMOTIONS
from stufe9_strategy_matrix import STRATEGY_LEVEL
from stufe10_codex_manifest import CODEX_KERNEL

def codex_gehirn_response(chat_id, text):
    response = []

    # 1. Signale prüfen
    if any(signal in text.lower() for signal in SIGNAL_WORDS):
        response.append("⚡ Codex-Signal erkannt. Zugriff bestätigt.")

    # 2. Emotionale Spiegelung
    for emoji, msg in EMOTIONS.items():
        if emoji in text:
            response.append(f"[EMOTION] {msg}")

    # 3. Marktsystem
    if "markt" in text.lower():
        response.append(MARKT(text))

    # 4. Nutzerprofil prüfen
    profile = USER_PROFILES.get(chat_id, {"status": "neu"})
    response.append(f"🧬 Profilstatus: {profile['status']}")

    # 5. Strategie & Manifest
    response.append(f"🎯 Strategie-Level: {STRATEGY_LEVEL}")
    response.append(f"🔐 Codex Manifest: {CODEX_KERNEL}")

    return "\n".join(response)
