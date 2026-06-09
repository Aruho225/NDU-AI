import os

from ui.twilio_calls import get_webhook_base_url, twilio_configured


def voice_mode() -> str:
    """twiml = Twilio Gather + Polly | livekit = LiveKit agent + Deepgram realtime."""
    mode = os.getenv("VOICE_MODE", "livekit").strip().lower()
    return mode if mode in {"twiml", "livekit"} else "livekit"


def livekit_configured() -> bool:
    return bool(
        os.getenv("LIVEKIT_URL", "").strip()
        and os.getenv("LIVEKIT_API_KEY", "").strip()
        and os.getenv("LIVEKIT_API_SECRET", "").strip()
    )


def deepgram_configured() -> bool:
    return bool(os.getenv("DEEPGRAM_API_KEY", "").strip())


def openai_configured() -> bool:
    return bool(os.getenv("OPENAI_API_KEY", "").strip())


def cartesia_configured() -> bool:
    return bool(os.getenv("CARTESIA_API_KEY", "").strip())


def agent_name() -> str:
    return os.getenv("LIVEKIT_AGENT_NAME", "ndu-assistant").strip() or "ndu-assistant"


def use_livekit_voice() -> bool:
    return voice_mode() == "livekit" and livekit_configured()


def telephony_status() -> dict[str, bool | str]:
    lk = livekit_configured()
    tw = twilio_configured()
    base = get_webhook_base_url()
    mode = voice_mode()
    active = use_livekit_voice() if mode == "livekit" else tw and bool(base)
    return {
        "voice_mode": mode,
        "twilio": tw,
        "webhook_url": bool(base),
        "livekit": lk,
        "deepgram": deepgram_configured(),
        "openai": openai_configured(),
        "cartesia": cartesia_configured(),
        "agent_name": agent_name(),
        "voice_pipeline_ready": active and (lk or mode == "twiml"),
        "realtime_stt": use_livekit_voice() and deepgram_configured(),
    }
