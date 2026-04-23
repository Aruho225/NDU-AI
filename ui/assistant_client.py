import os
from typing import Optional

from openai import OpenAI

from prompts import NDEJJE_UNIVERSITY_SYSTEM_PROMPT


DEFAULT_MODEL = "gpt-4o-mini"


def ask_assistant(user_message: str, model: str = DEFAULT_MODEL) -> str:
    """Send one text message to the assistant model."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "OPENAI_API_KEY is missing. Add it to your .env file and restart the app."

    client = OpenAI(api_key=api_key)
    try:
        response = client.responses.create(
            model=model,
            input=[
                {"role": "system", "content": NDEJJE_UNIVERSITY_SYSTEM_PROMPT.strip()},
                {"role": "user", "content": user_message.strip()},
            ],
            temperature=0.4,
        )
        return (response.output_text or "").strip() or "No response generated."
    except Exception as exc:  # broad catch for UI stability
        return f"Request failed: {exc}"


def validate_message(user_message: str) -> Optional[str]:
    if not user_message.strip():
        return "Please enter a question first."
    if len(user_message) > 2000:
        return "Message is too long. Keep it under 2000 characters."
    return None
