import os

from dotenv import load_dotenv

from livekit import agents
from livekit.agents import Agent, AgentSession, RoomInputOptions
from livekit.plugins import cartesia, deepgram, noise_cancellation, openai, silero

from agent_language import OPENING_GREETING_INSTRUCTIONS, build_agent_instructions
from ui.call_transcript import ensure_call_record, log_turn, persist_session_history
from ui.livekit_telephony import call_sid_from_room, room_name_for_call
from ui.telephony_config import agent_name

load_dotenv()


class NdejjeUniversityAssistant(Agent):
    def __init__(self, caller_language: str | None = None) -> None:
        super().__init__(instructions=build_agent_instructions(caller_language))


def _attach_transcript_logging(session: AgentSession, room_name: str) -> None:
    caller_language: str | None = None

    @session.on("user_input_transcribed")
    def on_user_transcribed(event) -> None:
        nonlocal caller_language

        text = (getattr(event, "transcript", "") or "").strip()
        is_final = getattr(event, "is_final", False)
        lang = getattr(event, "language", None)
        lang_code = str(lang).strip() if lang else None

        if is_final and lang_code and lang_code != caller_language:
            caller_language = lang_code
            session.update_agent(NdejjeUniversityAssistant(caller_language=caller_language))

        if not text:
            return
        if is_final:
            log_turn(room_name, "caller", text)

    @session.on("conversation_item_added")
    def on_item_added(event) -> None:
        item = getattr(event, "item", None)
        if item is None:
            return
        role = getattr(item, "role", "") or ""
        text = ""
        if hasattr(item, "text_content") and item.text_content:
            text = item.text_content
        elif hasattr(item, "content") and item.content:
            parts = []
            for block in item.content:
                if isinstance(block, str):
                    parts.append(block)
                elif hasattr(block, "text"):
                    parts.append(block.text)
            text = " ".join(parts)
        clean = (text or "").strip()
        if not clean:
            return
        if role in {"assistant", "agent"}:
            log_turn(room_name, "assistant", clean)
        elif role == "user":
            log_turn(room_name, "caller", clean)


async def entrypoint(ctx: agents.JobContext):
    room_name = ctx.room.name or ""
    call_sid = call_sid_from_room(room_name) or ""

    if call_sid:
        from ui.call_store import get_call_by_sid

        row = get_call_by_sid(call_sid) or {}
        ensure_call_record(
            call_sid=call_sid,
            direction=row.get("direction") or "inbound",
            from_number=row.get("from_number") or "",
            to_number=row.get("to_number") or "",
            room_name=room_name or room_name_for_call(call_sid),
        )

    use_telephony_nc = bool(call_sid) or os.getenv("LIVEKIT_TELEPHONY_NC", "1") == "1"
    nc = noise_cancellation.BVCTelephony() if use_telephony_nc else noise_cancellation.BVC()

    session = AgentSession(
        stt=deepgram.STT(model="nova-3", language="multi"),
        llm=openai.LLM(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini")),
        tts=cartesia.TTS(
            model="sonic-2",
            voice=os.getenv(
                "CARTESIA_VOICE_ID",
                "f786b574-daa5-4673-aa0c-cbe3e8534c02",
            ),
        ),
        vad=silero.VAD.load(),
        turn_handling={"turn_detection": "stt"},
    )

    _attach_transcript_logging(session, room_name)

    @session.on("close")
    def on_session_close(_event) -> None:
        persist_session_history(room_name, session.history)

    await session.start(
        room=ctx.room,
        agent=NdejjeUniversityAssistant(),
        room_input_options=RoomInputOptions(noise_cancellation=nc),
    )

    await ctx.connect()

    await session.generate_reply(
        instructions=OPENING_GREETING_INSTRUCTIONS,
        allow_interruptions=False,
    )


if __name__ == "__main__":
    agents.cli.run_app(
        agents.WorkerOptions(
            entrypoint_fnc=entrypoint,
            agent_name=agent_name(),
        )
    )
