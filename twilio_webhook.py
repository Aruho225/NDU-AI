import os

from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request, Response
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse

from ui.assistant_client import ask_assistant, validate_message
from ui.twilio_voice import (
    handle_gather,
    handle_inbound_voice,
    handle_outbound_voice,
    handle_recording,
    handle_status,
)

load_dotenv()
app = FastAPI(title="NDU Twilio Webhook")


async def _signature_valid(request: Request) -> bool:
    auth_token = os.getenv("TWILIO_AUTH_TOKEN", "").strip()
    signature = request.headers.get("X-Twilio-Signature", "").strip()
    if not auth_token:
        return True
    if not signature:
        return False
    form_data = await request.form()
    validator = RequestValidator(auth_token)
    return validator.validate(str(request.url), dict(form_data), signature)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/twilio/webhook")
async def inbound_message(
    request: Request,
    Body: str = Form(default=""),
    From: str = Form(default=""),
) -> Response:
    if not await _signature_valid(request):
        twiml = MessagingResponse()
        twiml.message("Request rejected: invalid Twilio signature.")
        return Response(content=str(twiml), media_type="application/xml", status_code=403)

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
async def voice_inbound(
    request: Request,
    CallSid: str = Form(default=""),
    From: str = Form(default=""),
    To: str = Form(default=""),
) -> Response:
    if not await _signature_valid(request):
        return Response(content="Forbidden", status_code=403)
    twiml = handle_inbound_voice(CallSid, From, To)
    return Response(content=twiml, media_type="application/xml")


@app.post("/twilio/voice/outbound")
async def voice_outbound(
    request: Request,
    CallSid: str = Form(default=""),
    From: str = Form(default=""),
    To: str = Form(default=""),
) -> Response:
    if not await _signature_valid(request):
        return Response(content="Forbidden", status_code=403)
    twiml = handle_outbound_voice(CallSid, From, To)
    return Response(content=twiml, media_type="application/xml")


@app.post("/twilio/voice/gather")
async def voice_gather(
    request: Request,
    CallSid: str = Form(default=""),
    SpeechResult: str = Form(default=""),
) -> Response:
    if not await _signature_valid(request):
        return Response(content="Forbidden", status_code=403)
    twiml = handle_gather(CallSid, SpeechResult)
    return Response(content=twiml, media_type="application/xml")


@app.post("/twilio/voice/continue")
async def voice_continue(request: Request) -> Response:
    if not await _signature_valid(request):
        return Response(content="Forbidden", status_code=403)
    from ui.twilio_voice import build_continue_prompt

    return Response(content=build_continue_prompt(), media_type="application/xml")


@app.post("/twilio/voice/status")
async def voice_status(
    request: Request,
    CallSid: str = Form(default=""),
    CallStatus: str = Form(default=""),
    CallDuration: str = Form(default="0"),
) -> Response:
    if not await _signature_valid(request):
        return Response(content="Forbidden", status_code=403)
    try:
        duration = int(CallDuration or "0")
    except ValueError:
        duration = 0
    handle_status(CallSid, CallStatus, duration)
    return Response(content="ok", media_type="text/plain")


@app.post("/twilio/voice/recording")
async def voice_recording(
    request: Request,
    CallSid: str = Form(default=""),
    RecordingUrl: str = Form(default=""),
    RecordingSid: str = Form(default=""),
) -> Response:
    if not await _signature_valid(request):
        return Response(content="Forbidden", status_code=403)
    handle_recording(CallSid, RecordingUrl, RecordingSid)
    return Response(content="ok", media_type="text/plain")


# Run with:
# uvicorn twilio_webhook:app --host 0.0.0.0 --port 8000
#
# Twilio console setup:
# - Phone number Voice webhook (POST): {TWILIO_WEBHOOK_BASE_URL}/twilio/voice/inbound
# - Run a second ngrok tunnel for port 8000 if Streamlit uses a different URL
