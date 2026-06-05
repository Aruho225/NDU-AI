import os
from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    openai,
    cartesia,
    deepgram,
    noise_cancellation,
    silero,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from prompt_loader import load_greeting_prompt, load_system_prompt

load_dotenv()


class NdejjeUniversityAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=load_system_prompt())


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt=deepgram.STT(
            model="nova-3",
            language="multi"
        ),
        llm=openai.LLM(
            model="gpt-4o-mini"
        ),
        tts=cartesia.TTS(
            model="sonic-2",
            voice="f786b574-daa5-4673-aa0c-cbe3e8534c02"
        ),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=NdejjeUniversityAssistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()

    await session.generate_reply(instructions=load_greeting_prompt())


if __name__ == "__main__":
    agents.cli.run_app(
        agents.WorkerOptions(entrypoint_fnc=entrypoint)
    )