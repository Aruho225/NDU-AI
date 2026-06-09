"""Language detection helpers for the LiveKit voice agent."""

from __future__ import annotations

from prompts import LANGUAGE_POLICY, NDEJJE_UNIVERSITY_SYSTEM_PROMPT

_LANGUAGE_NAMES: dict[str, str] = {
    "en": "English",
    "en-US": "English",
    "en-GB": "English",
    "lg": "Luganda",
    "sw": "Swahili",
    "fr": "French",
    "es": "Spanish",
    "ar": "Arabic",
    "pt": "Portuguese",
    "de": "German",
    "zh": "Chinese",
    "hi": "Hindi",
    "ru": "Russian",
    "so": "Somali",
    "rw": "Kinyarwanda",
    "ny": "Chichewa",
    "am": "Amharic",
}


def language_label(code: str | None) -> str | None:
    if not code:
        return None
    clean = code.strip()
    if not clean:
        return None
    base = clean.split("-")[0].lower()
    return _LANGUAGE_NAMES.get(clean, _LANGUAGE_NAMES.get(base, clean))


def build_agent_instructions(caller_language: str | None = None) -> str:
    parts = [NDEJJE_UNIVERSITY_SYSTEM_PROMPT.strip(), LANGUAGE_POLICY.strip()]
    label = language_label(caller_language)
    if label:
        parts.append(
            f"Active caller language: {label} (detected from speech). "
            f"Respond only in {label} unless the caller clearly switches language."
        )
    return "\n\n".join(parts)


OPENING_GREETING_INSTRUCTIONS = """
Deliver your phone greeting now, before the caller asks anything.

Required content (spoken naturally, not as a list):
1. Warm hello and welcome to Ndejje University.
2. Introduce yourself as the NDU AI Assistant.
3. Briefly mention you help with admissions, fees, academics, portal support, and ICT.
4. Invite the caller to ask their question.

Style:
- Sound warm, professional, and concise (about 20–35 seconds when spoken).
- Use short sentences suitable for a phone call.
- Default to English for this opening greeting.
- Do not ask multiple questions; one simple invitation to speak is enough.
"""
