import io
import os
from typing import Optional

from openai import OpenAI


TTS_MODEL = "gpt-4o-mini-tts"
TTS_VOICES = ["alloy", "verse", "sage", "aria"]


def transcribe_audio(audio_bytes: bytes, file_name: str) -> tuple[Optional[str], Optional[str]]:
    """Return (transcript, error)."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None, "OPENAI_API_KEY is missing. Add it to your .env file."

    if not audio_bytes:
        return None, "Audio file is empty. Upload a valid recording."

    audio_stream = io.BytesIO(audio_bytes)
    audio_stream.name = file_name or "voice_note.webm"

    try:
        client = OpenAI(api_key=api_key)
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_stream,
        )
        text = (transcription.text or "").strip()
        if not text:
            return None, "Could not detect speech clearly. Try a clearer recording."
        return text, None
    except Exception as exc:  # broad catch for UI stability
        return None, f"Transcription failed: {exc}"


def text_to_speech_bytes(text: str, voice: str = "alloy") -> tuple[Optional[bytes], Optional[str]]:
    """Return (audio_bytes_mp3, error)."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None, "OPENAI_API_KEY is missing. Add it to your .env file."

    if not text.strip():
        return None, "Assistant response is empty, nothing to read aloud."

    try:
        client = OpenAI(api_key=api_key)
        speech = client.audio.speech.create(
            model=TTS_MODEL,
            voice=voice,
            input=text.strip(),
            response_format="mp3",
        )
        audio_bytes = getattr(speech, "content", None)
        if not audio_bytes:
            return None, "TTS returned no audio."
        return audio_bytes, None
    except Exception as exc:  # broad catch for UI stability
        return None, f"Text-to-speech failed: {exc}"
