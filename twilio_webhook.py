import os

from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request, Response
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse

from ui.assistant_client import ask_assistant, validate_message

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


# Run with:
# uvicorn twilio_webhook:app --host 0.0.0.0 --port 8000
