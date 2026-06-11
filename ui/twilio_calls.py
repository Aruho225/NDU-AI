import base64
import io
import os
import re
import urllib.error
import urllib.request
from typing import Optional

PHONE_RE = re.compile(r"^\+[1-9]\d{6,14}$")
_ENV_LOADED = False


def _refresh_env() -> None:
    """Reload .env so long-running Streamlit picks up credential changes."""
    global _ENV_LOADED
    from dotenv import load_dotenv

    load_dotenv(override=True)
    _ENV_LOADED = True


def get_account_sid() -> str:
    if not _ENV_LOADED:
        _refresh_env()
    return os.getenv("TWILIO_ACCOUNT_SID", "").strip()


def get_auth_token() -> str:
    if not _ENV_LOADED:
        _refresh_env()
    return os.getenv("TWILIO_AUTH_TOKEN", "").strip()


def get_phone_number() -> str:
    number = os.getenv("TWILIO_PHONE_NUMBER", "").strip()
    if not number:
        number = os.getenv("twilio_phone_number", "").strip()
    return re.sub(r"\s+", "", number)


def get_webhook_base_url() -> str:
    return os.getenv("TWILIO_WEBHOOK_BASE_URL", "").strip().rstrip("/")


def twilio_configured() -> bool:
    return bool(get_account_sid() and get_auth_token() and get_phone_number())


def normalize_phone(number: str) -> str:
    clean = re.sub(r"[\s\-().]", "", number.strip())
    if clean and not clean.startswith("+"):
        clean = f"+{clean}"
    return clean


def validate_phone(number: str) -> Optional[str]:
    clean = normalize_phone(number)
    if not PHONE_RE.match(clean):
        return "Enter a valid phone number in E.164 format (e.g. +256700000000)."
    return None


def place_outbound_call(to_number: str, user_id: int) -> tuple[bool, str, Optional[str]]:
    _refresh_env()
    if not twilio_configured():
        return False, "Twilio is not configured. Add TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER to .env.", None

    base_url = get_webhook_base_url()
    if not base_url:
        return False, "Set TWILIO_WEBHOOK_BASE_URL to your public FastAPI URL (e.g. ngrok tunnel to port 8000).", None

    issue = validate_phone(to_number)
    if issue:
        return False, issue, None

    clean_to = normalize_phone(to_number)
    from_number = get_phone_number()

    try:
        from twilio.rest import Client

        client = Client(get_account_sid(), get_auth_token())
        call = client.calls.create(
            to=clean_to,
            from_=from_number,
            url=f"{base_url}/twilio/voice/outbound",
            status_callback=f"{base_url}/twilio/voice/status",
            status_callback_event=["initiated", "ringing", "answered", "completed"],
            status_callback_method="POST",
            record=True,
            recording_status_callback=f"{base_url}/twilio/voice/recording",
            recording_status_callback_method="POST",
        )
        from ui.call_store import create_call
        from ui.livekit_telephony import room_name_for_call
        from ui.telephony_config import voice_mode

        mode = voice_mode()
        create_call(
            call_sid=call.sid,
            direction="outbound",
            from_number=from_number,
            to_number=clean_to,
            user_id=user_id,
            voice_mode=mode,
            livekit_room=room_name_for_call(call.sid) if mode == "livekit" else None,
        )
        return True, f"Outbound call started to {clean_to}.", call.sid
    except Exception as exc:
        return False, f"Could not start call: {exc}", None


def fetch_recording_bytes(recording_url: str) -> tuple[Optional[bytes], Optional[str]]:
    if not recording_url:
        return None, "No recording URL saved for this call."

    sid = get_account_sid()
    token = get_auth_token()
    if not sid or not token:
        return None, "Twilio credentials missing."

    url = recording_url if recording_url.endswith(".mp3") else f"{recording_url}.mp3"
    req = urllib.request.Request(url)
    credentials = base64.b64encode(f"{sid}:{token}".encode()).decode()
    req.add_header("Authorization", f"Basic {credentials}")

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read(), None
    except urllib.error.HTTPError as exc:
        return None, f"Could not fetch recording ({exc.code})."
    except Exception as exc:
        return None, f"Could not fetch recording: {exc}"


def transcribe_recording(recording_url: str) -> tuple[Optional[str], Optional[str]]:
    audio_bytes, error = fetch_recording_bytes(recording_url)
    if error or not audio_bytes:
        return None, error or "Recording is empty."

    from ui.voice_client import transcribe_audio

    return transcribe_audio(audio_bytes, "call_recording.mp3")
