import os

from twilio.twiml.voice_response import Gather, Start, VoiceResponse

from ui.assistant_client import ask_assistant, validate_message
from ui.call_store import append_call_turn, create_call, get_call_by_sid, update_call_recording, update_call_status
from ui.twilio_calls import get_webhook_base_url, transcribe_recording


def _base_url() -> str:
    return get_webhook_base_url()


def _say_text(text: str, max_len: int = 1200) -> str:
    clean = " ".join(text.split())
    if len(clean) <= max_len:
        return clean
    trimmed = clean[:max_len].rsplit(" ", 1)[0]
    return f"{trimmed}. Ask a follow up question if you need more details."


def build_call_flow() -> str:
    base = _base_url()
    response = VoiceResponse()
    start = Start()
    start.recording(
        recording_status_callback=f"{base}/twilio/voice/recording",
        recording_status_callback_method="POST",
    )
    response.append(start)
    response.say(
        "Welcome to N D U AI Assistant. I can help with admissions, fees, academics, and portal support.",
        voice="Polly.Joanna",
    )
    gather = Gather(
        input="speech",
        action=f"{base}/twilio/voice/gather",
        method="POST",
        speech_timeout="auto",
        language="en-US",
        timeout=5,
    )
    gather.say("Please ask your question after the tone.", voice="Polly.Joanna")
    response.append(gather)
    response.redirect(f"{base}/twilio/voice/continue", method="POST")
    return str(response)


def build_continue_prompt() -> str:
    base = _base_url()
    response = VoiceResponse()
    gather = Gather(
        input="speech",
        action=f"{base}/twilio/voice/gather",
        method="POST",
        speech_timeout="auto",
        language="en-US",
        timeout=5,
    )
    gather.say("Do you have another question?", voice="Polly.Joanna")
    response.append(gather)
    response.say("Thank you for calling N D U. Goodbye.", voice="Polly.Joanna")
    response.hangup()
    return str(response)


def handle_inbound_voice(call_sid: str, from_number: str, to_number: str) -> str:
    if not get_call_by_sid(call_sid):
        create_call(
            call_sid=call_sid,
            direction="inbound",
            from_number=from_number,
            to_number=to_number,
        )
    return build_call_flow()


def handle_outbound_voice(call_sid: str, from_number: str, to_number: str) -> str:
    if not get_call_by_sid(call_sid):
        create_call(
            call_sid=call_sid,
            direction="outbound",
            from_number=from_number,
            to_number=to_number,
        )
    return build_call_flow()


def handle_gather(call_sid: str, speech_result: str) -> str:
    response = VoiceResponse()
    question = (speech_result or "").strip()

    if not question:
        response.say("I did not catch that. Please try again.", voice="Polly.Joanna")
        response.redirect(f"{_base_url()}/twilio/voice/continue", method="POST")
        return str(response)

    append_call_turn(call_sid, "caller", question)

    issue = validate_message(question)
    if issue:
        answer = issue
    else:
        answer = ask_assistant(question)

    append_call_turn(call_sid, "assistant", answer)
    response.say(_say_text(answer), voice="Polly.Joanna")

    gather = Gather(
        input="speech",
        action=f"{_base_url()}/twilio/voice/gather",
        method="POST",
        speech_timeout="auto",
        language="en-US",
        timeout=4,
    )
    gather.say("Anything else I can help with?", voice="Polly.Joanna")
    response.append(gather)
    response.say("Thank you for calling N D U. Goodbye.", voice="Polly.Joanna")
    response.hangup()
    return str(response)


def handle_status(call_sid: str, status: str, duration: int) -> None:
    if not call_sid:
        return
    if not get_call_by_sid(call_sid):
        create_call(call_sid=call_sid, direction="inbound", from_number="", to_number="")
    update_call_status(call_sid, status.lower(), duration)


def handle_recording(call_sid: str, recording_url: str, recording_sid: str) -> None:
    if not call_sid or not recording_url:
        return
    row = get_call_by_sid(call_sid)
    if not row:
        return

    transcription = row.get("transcription") or ""
    if not transcription and recording_url:
        text, _error = transcribe_recording(recording_url)
        if text:
            transcription = text

    update_call_recording(call_sid, recording_url, recording_sid, transcription or None)
