import os

from twilio.twiml.voice_response import Gather, Start, VoiceResponse

from ui.assistant_client import ask_assistant, validate_message
from ui.call_store import append_call_turn, create_call, get_call_by_sid, update_call_recording, update_call_status
from ui.livekit_telephony import build_stream_twiml, connect_twilio_call, room_name_for_call
from ui.telephony_config import use_livekit_voice, voice_mode
from ui.twilio_calls import get_webhook_base_url, transcribe_recording


def _base_url() -> str:
    return get_webhook_base_url()


def _say_text(text: str, max_len: int = 1200) -> str:
    clean = " ".join(text.split())
    if len(clean) <= max_len:
        return clean
    trimmed = clean[:max_len].rsplit(" ", 1)[0]
    return f"{trimmed}. Ask a follow up question if you need more details."


def _ensure_call(
    call_sid: str,
    direction: str,
    from_number: str,
    to_number: str,
) -> None:
    if get_call_by_sid(call_sid):
        return
    mode = voice_mode()
    room = room_name_for_call(call_sid) if mode == "livekit" else None
    create_call(
        call_sid=call_sid,
        direction=direction,
        from_number=from_number,
        to_number=to_number,
        voice_mode=mode,
        livekit_room=room,
    )


async def _livekit_voice_twiml(
    call_sid: str,
    direction: str,
    from_number: str,
    to_number: str,
) -> str:
    connect_url, error = await connect_twilio_call(call_sid, direction, from_number, to_number)
    if error or not connect_url:
        # Fall back to TwiML pipeline so calls still work if LiveKit is misconfigured.
        return build_call_flow()

    # Agent delivers the full greeting after the LiveKit session starts.
    return build_stream_twiml(connect_url)


def _status_callback_attrs(base: str) -> dict[str, str]:
    if not base:
        return {}
    return {
        "status_callback": f"{base}/twilio/voice/status",
        "status_callback_method": "POST",
    }


def build_call_flow() -> str:
    base = _base_url()
    response = VoiceResponse(**_status_callback_attrs(base))
    start = Start()
    start.recording(
        recording_status_callback=f"{base}/twilio/voice/recording",
        recording_status_callback_method="POST",
        recording_channels="dual",
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
        speech_model="phone_call",
        enhanced=True,
        language="en-US",
        timeout=6,
        hints="admissions, fees, tuition, registration, portal, results, intake, Ndejje",
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
        speech_model="phone_call",
        enhanced=True,
        language="en-US",
        timeout=5,
        hints="admissions, fees, tuition, registration, portal",
    )
    gather.say("Do you have another question?", voice="Polly.Joanna")
    response.append(gather)
    response.say("Thank you for calling N D U. Goodbye.", voice="Polly.Joanna")
    response.hangup()
    return str(response)


async def handle_inbound_voice(call_sid: str, from_number: str, to_number: str) -> str:
    _ensure_call(call_sid, "inbound", from_number, to_number)
    if use_livekit_voice():
        return await _livekit_voice_twiml(call_sid, "inbound", from_number, to_number)
    return build_call_flow()


async def handle_outbound_voice(call_sid: str, from_number: str, to_number: str) -> str:
    _ensure_call(call_sid, "outbound", from_number, to_number)
    if use_livekit_voice():
        return await _livekit_voice_twiml(call_sid, "outbound", from_number, to_number)
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
        speech_model="phone_call",
        enhanced=True,
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
    if not transcription:
        from ui.call_sync import format_conversation_transcript

        conversation_text = format_conversation_transcript(row.get("conversation_log") or [])
        if conversation_text:
            transcription = conversation_text
        elif row.get("voice_mode") != "livekit" and os.getenv("OPENAI_API_KEY", "").strip():
            text, _error = transcribe_recording(recording_url)
            if text:
                transcription = text

    update_call_recording(call_sid, recording_url, recording_sid, transcription or None)
