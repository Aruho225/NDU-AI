"""App navigation modes (Vapi-style console)."""

ASSISTANT = "Assistant"
DASHBOARD = "Dashboard"
PLAYGROUND = "Playground"
CONVERSATION = "Conversation"
PHONE_NUMBERS = "Phone Numbers"
CALLS = "Calls"
CALL_DETAIL = "Call Detail"
SETTINGS = "Settings"

DEFAULT_MODE = ASSISTANT

_LEGACY_MAP = {
    "Ask Page": PLAYGROUND,
    "Answer Page": CONVERSATION,
    "Inbound Calls Page": CALLS,
    "Outbound Calls Page": CALLS,
    "Call Detail Page": CALL_DETAIL,
}


def normalize_mode(mode: str) -> str:
    return _LEGACY_MAP.get(mode, mode)
