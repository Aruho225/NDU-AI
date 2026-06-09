import os
import re
from typing import Optional

from livekit import api
from livekit.protocol.agent_dispatch import RoomAgentDispatch
from livekit.protocol.connector_twilio import ConnectTwilioCallRequest

from ui.telephony_config import agent_name, livekit_configured


def room_name_for_call(call_sid: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9_-]", "", call_sid) or "unknown"
    return f"call-{safe}"


def call_sid_from_room(room_name: str) -> Optional[str]:
    if room_name.startswith("call-"):
        return room_name[5:] or None
    return None


async def connect_twilio_call(
    call_sid: str,
    direction: str,
    from_number: str = "",
    to_number: str = "",
) -> tuple[Optional[str], Optional[str]]:
    """
    Bridge a Twilio call into a LiveKit room via the Twilio Connector.
    Returns (connect_url for <Stream>, error_message).
    """
    if not livekit_configured():
        return None, "LiveKit is not configured (LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET)."

    if not call_sid:
        return None, "Missing CallSid."

    is_outbound = direction == "outbound"
    twilio_direction = (
        ConnectTwilioCallRequest.TWILIO_CALL_DIRECTION_OUTBOUND
        if is_outbound
        else ConnectTwilioCallRequest.TWILIO_CALL_DIRECTION_INBOUND
    )

    identity = from_number or to_number or call_sid
    room = room_name_for_call(call_sid)
    name = agent_name()

    lkapi = api.LiveKitAPI()
    try:
        response = await lkapi.connector.connect_twilio_call(
            ConnectTwilioCallRequest(
                twilio_call_direction=twilio_direction,
                room_name=room,
                participant_identity=identity,
                participant_name=identity,
                participant_metadata=call_sid,
                agents=[RoomAgentDispatch(agent_name=name)],
                destination_country=os.getenv("LIVEKIT_DESTINATION_COUNTRY", "US"),
            )
        )
        connect_url = (response.connect_url or "").strip()
        if not connect_url:
            return None, "LiveKit returned an empty connect URL."
        return connect_url, None
    except Exception as exc:
        return None, f"LiveKit connector failed: {exc}"
    finally:
        await lkapi.aclose()


def build_stream_twiml(connect_url: str, greeting: str = "") -> str:
    from twilio.twiml.voice_response import Connect, Start, Stream, VoiceResponse

    from ui.twilio_calls import get_webhook_base_url

    response = VoiceResponse()
    base = get_webhook_base_url()
    if base:
        start = Start()
        start.recording(
            recording_status_callback=f"{base}/twilio/voice/recording",
            recording_status_callback_method="POST",
            recording_channels="dual",
        )
        response.append(start)
    if greeting:
        response.say(greeting, voice="Polly.Joanna")
    connect = Connect()
    connect.stream(url=connect_url)
    response.append(connect)
    return str(response)
