"""Persist LiveKit agent transcripts into the calls table."""

from __future__ import annotations

from typing import Any

from ui.call_store import (
    append_call_turn,
    create_call,
    get_call_by_sid,
    set_conversation_log,
    update_call_livekit_room,
    update_call_transcription,
)
from ui.call_sync import format_conversation_transcript
from ui.livekit_telephony import call_sid_from_room


def ensure_call_record(
    call_sid: str,
    direction: str = "inbound",
    from_number: str = "",
    to_number: str = "",
    room_name: str = "",
) -> None:
    if not call_sid:
        return
    if not get_call_by_sid(call_sid):
        create_call(
            call_sid=call_sid,
            direction=direction,
            from_number=from_number,
            to_number=to_number,
        )
    if room_name:
        update_call_livekit_room(call_sid, room_name)


def log_turn(room_name: str, role: str, text: str) -> None:
    call_sid = call_sid_from_room(room_name)
    if not call_sid:
        return
    mapped = "caller" if role in {"user", "caller"} else "assistant"
    append_call_turn(call_sid, mapped, text)


def _message_text(item: Any) -> str:
    if item is None:
        return ""
    if hasattr(item, "text_content") and item.text_content:
        return str(item.text_content).strip()
    if hasattr(item, "content") and item.content:
        parts: list[str] = []
        for block in item.content:
            if isinstance(block, str):
                parts.append(block)
            elif hasattr(block, "text") and block.text:
                parts.append(str(block.text))
        return " ".join(parts).strip()
    return ""


def persist_session_history(room_name: str, history: Any) -> None:
    call_sid = call_sid_from_room(room_name)
    if not call_sid or history is None:
        return

    items = getattr(history, "items", None)
    if items is None:
        return

    conversation: list[dict[str, str]] = []
    for item in items:
        item_type = getattr(item, "type", "")
        if item_type and item_type != "message":
            continue
        role = getattr(item, "role", "")
        text = _message_text(item)
        if not text:
            continue
        mapped = "caller" if role == "user" else "assistant"
        if conversation and conversation[-1]["role"] == mapped:
            previous = conversation[-1]["text"]
            if text.startswith(previous) or len(text) > len(previous):
                conversation[-1]["text"] = text
            elif text != previous:
                conversation.append({"role": mapped, "text": text})
        else:
            conversation.append({"role": mapped, "text": text})

    if not conversation:
        return

    set_conversation_log(call_sid, conversation)
    formatted = format_conversation_transcript(conversation)
    if formatted:
        update_call_transcription(call_sid, formatted)
