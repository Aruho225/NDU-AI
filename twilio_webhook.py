import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse

from ui.assistant_client import ask_assistant, validate_message
from ui.telephony_config import telephony_status, use_livekit_voice
from ui.twilio_calls import get_webhook_base_url
from ui.twilio_voice import (
    handle_gather,
    handle_inbound_voice,
    handle_outbound_voice,
    handle_recording,
    handle_status,
)

load_dotenv()
app = FastAPI(title="NDU Twilio Webhook")
logger = logging.getLogger("ndu.twilio")


@app.on_event("startup")
async def _sync_twilio_phone_on_startup() -> None:
    from ui.twilio_phone_setup import sync_phone_webhooks

    result = sync_phone_webhooks()
    if result.get("updated"):
        logger.info("Twilio inbound webhooks synced: %s", result.get("message"))
    elif result.get("ok"):
        logger.info("Twilio phone webhooks OK for %s", result.get("phone"))
    else:
        logger.warning("Twilio phone webhook sync skipped: %s", result.get("message") or result.get("error"))


def _candidate_request_urls(request: Request) -> list[str]:
    """URLs Twilio may have signed — ngrok/proxy headers often break a single guess."""
    path = request.url.path
    query = request.url.query
    suffix = path + (f"?{query}" if query else "")

    urls: list[str] = []
    base = get_webhook_base_url()
    if base:
        urls.append(f"{base.rstrip('/')}{suffix}")

    proto = request.headers.get("X-Forwarded-Proto", request.url.scheme)
    host = request.headers.get("X-Forwarded-Host") or request.headers.get("Host") or request.url.netloc
    urls.append(f"{proto}://{host}{suffix}")

    # De-dupe while preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for url in urls:
        if url not in seen:
            seen.add(url)
            unique.append(url)
    return unique


def _signature_valid_for_data(request: Request, form_data: dict[str, str]) -> bool:
    auth_token = os.getenv("TWILIO_AUTH_TOKEN", "").strip()
    signature = request.headers.get("X-Twilio-Signature", "").strip()
    if not auth_token:
        return True
    if not signature:
        return False
    validator = RequestValidator(auth_token)
    for url in _candidate_request_urls(request):
        if validator.validate(url, form_data, signature):
            return True
    logger.warning(
        "Twilio signature rejected for %s (tried %s)",
        request.url.path,
        ", ".join(_candidate_request_urls(request)),
    )
    return False


async def _read_form(request: Request) -> dict[str, str]:
    form = await request.form()
    return {key: str(value) for key, value in form.items()}


async def _validate_twilio_request(request: Request) -> tuple[bool, dict[str, str]]:
    form_data = await _read_form(request)
    return _signature_valid_for_data(request, form_data), form_data


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/telephony/status")
def telephony_status_endpoint() -> dict:
    from ui.twilio_phone_setup import get_phone_webhook_status

    status = telephony_status()
    status["livekit_voice_active"] = use_livekit_voice()
    status["phone_webhooks"] = get_phone_webhook_status()
    return status


@app.post("/telephony/sync-phone")
def sync_phone_webhooks_endpoint() -> dict:
    from ui.twilio_phone_setup import sync_phone_webhooks

    return sync_phone_webhooks(force=True)


@app.post("/twilio/webhook")
async def inbound_message(request: Request) -> Response:
    valid, form = await _validate_twilio_request(request)
    if not valid:
        twiml = MessagingResponse()
        twiml.message("Request rejected: invalid Twilio signature.")
        return Response(content=str(twiml), media_type="application/xml", status_code=403)

    Body = form.get("Body", "")
    From = form.get("From", "")
    issue = validate_message(Body)
    if issue:
        reply = issue
    else:
        prefix = f"User {From}: " if From else ""
        reply = ask_assistant(f"{prefix}{Body.strip()}")

    twiml = MessagingResponse()
    twiml.message(reply)
    return Response(content=str(twiml), media_type="application/xml")


@app.post("/twilio/voice/inbound")
async def voice_inbound(request: Request) -> Response:
    valid, form = await _validate_twilio_request(request)
    CallSid = form.get("CallSid", "")
    From = form.get("From", "")
    To = form.get("To", "")
    if not valid:
        logger.warning("Inbound voice rejected: invalid Twilio signature (CallSid=%s)", CallSid)
        return Response(content="Forbidden", status_code=403)
    logger.info("Inbound voice CallSid=%s From=%s To=%s", CallSid, From, To)
    twiml = await handle_inbound_voice(CallSid, From, To)
    return Response(content=twiml, media_type="application/xml")


@app.post("/twilio/voice/outbound")
async def voice_outbound(request: Request) -> Response:
    valid, form = await _validate_twilio_request(request)
    if not valid:
        return Response(content="Forbidden", status_code=403)
    twiml = await handle_outbound_voice(
        form.get("CallSid", ""),
        form.get("From", ""),
        form.get("To", ""),
    )
    return Response(content=twiml, media_type="application/xml")


@app.post("/twilio/voice/gather")
async def voice_gather(request: Request) -> Response:
    valid, form = await _validate_twilio_request(request)
    if not valid:
        return Response(content="Forbidden", status_code=403)
    twiml = handle_gather(form.get("CallSid", ""), form.get("SpeechResult", ""))
    return Response(content=twiml, media_type="application/xml")


@app.post("/twilio/voice/continue")
async def voice_continue(request: Request) -> Response:
    valid, _form = await _validate_twilio_request(request)
    if not valid:
        return Response(content="Forbidden", status_code=403)
    from ui.twilio_voice import build_continue_prompt

    return Response(content=build_continue_prompt(), media_type="application/xml")


@app.post("/twilio/voice/status")
async def voice_status(request: Request) -> Response:
    valid, form = await _validate_twilio_request(request)
    if not valid:
        return Response(content="Forbidden", status_code=403)
    try:
        duration = int(form.get("CallDuration", "0") or "0")
    except ValueError:
        duration = 0
    handle_status(form.get("CallSid", ""), form.get("CallStatus", ""), duration)
    return Response(content="ok", media_type="text/plain")


@app.post("/twilio/voice/recording")
async def voice_recording(request: Request) -> Response:
    valid, form = await _validate_twilio_request(request)
    if not valid:
        return Response(content="Forbidden", status_code=403)
    handle_recording(form.get("CallSid", ""), form.get("RecordingUrl", ""), form.get("RecordingSid", ""))
    return Response(content="ok", media_type="text/plain")


# Run:
#   uvicorn twilio_webhook:app --host 0.0.0.0 --port 8000
#
# Twilio console (VOICE_MODE=twiml):
#   Voice webhook POST -> {TWILIO_WEBHOOK_BASE_URL}/twilio/voice/inbound
#   Messaging POST     -> {TWILIO_WEBHOOK_BASE_URL}/twilio/webhook
#
# Twilio console (VOICE_MODE=livekit, recommended):
#   Same voice webhook URLs — calls bridge to LiveKit via Media Streams.
#   Also run: python agent.py dev
