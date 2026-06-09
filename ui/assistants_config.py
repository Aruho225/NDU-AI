import os
from typing import Any

from ui.assistant_client import DEFAULT_MODEL
from ui.telephony_config import telephony_status, use_livekit_voice
from ui.twilio_calls import get_phone_number, get_webhook_base_url
from ui.voice_client import TTS_VOICES

ASSISTANT_ID = "ndu-main"

ASSISTANTS: list[dict[str, Any]] = [
    {
        "id": ASSISTANT_ID,
        "name": "NDU AI Assistant",
        "description": "Student support for admissions, fees, academics, portal help, and ICT.",
        "model": DEFAULT_MODEL,
        "voice_web": TTS_VOICES[0],
        "voice_phone": "Polly.Joanna (Twilio)",
        "stt_phone": "Twilio Speech · en-US",
        "channels": ["Web playground", "SMS", "Voice calls"],
        "tags": ["Admissions", "Fees", "Academics", "ICT"],
    },
]


def get_assistant(assistant_id: str = ASSISTANT_ID) -> dict[str, Any]:
    for item in ASSISTANTS:
        if item["id"] == assistant_id:
            return item
    return ASSISTANTS[0]


def assistant_runtime_status() -> dict[str, bool]:
    status = telephony_status()
    return {
        "openai": bool(status["openai"]),
        "twilio": bool(status["twilio"]),
        "webhook": bool(status["webhook_url"]),
        "livekit": bool(status["livekit"]),
        "deepgram": bool(status["deepgram"]),
        "realtime": bool(status["realtime_stt"]),
        "phone_assigned": bool(status["twilio"]) and bool(get_phone_number()),
        "voice_livekit": use_livekit_voice(),
    }
