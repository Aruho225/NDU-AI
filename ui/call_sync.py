"""Sync call status, recordings, and transcripts from Twilio into the local store."""

from __future__ import annotations

from typing import Any, Optional

from ui.call_store import (
    get_call_by_sid,
    update_call_recording,
    update_call_status,
    update_call_transcription,
)
from ui.twilio_calls import get_account_sid, get_auth_token, transcribe_recording, twilio_configured


def format_conversation_transcript(conversation: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for turn in conversation:
        role = turn.get("role", "caller")
        text = (turn.get("text") or "").strip()
        if not text:
            continue
        label = "Caller" if role == "caller" else "NDU AI Assistant"
        lines.append(f"{label}: {text}")
    return "\n\n".join(lines)


def _twilio_recording_url(uri: str) -> str:
    clean = (uri or "").strip()
    if not clean:
        return ""
    if clean.startswith("http"):
        return clean.rsplit(".", 1)[0] if clean.endswith(".json") else clean
    return f"https://api.twilio.com{clean.replace('.json', '')}"


def sync_call_from_twilio(call_sid: str) -> bool:
    """Refresh status, duration, recording URL, and transcript for one call."""
    if not call_sid or not twilio_configured():
        return False

    row = get_call_by_sid(call_sid)
    if not row:
        return False

    from twilio.rest import Client

    client = Client(get_account_sid(), get_auth_token())
    try:
        remote = client.calls(call_sid).fetch()
    except Exception:
        return False

    status = (remote.status or row.get("status") or "unknown").lower()
    duration = int(remote.duration or row.get("duration_seconds") or 0)
    update_call_status(call_sid, status, duration)

    row = get_call_by_sid(call_sid) or row
    if not row.get("recording_url"):
        try:
            recordings = client.recordings.list(call_sid=call_sid, limit=3)
        except Exception:
            recordings = []
        for recording in recordings:
            if (recording.status or "").lower() != "completed":
                continue
            url = _twilio_recording_url(recording.uri or "")
            if not url:
                continue
            transcription = row.get("transcription") or ""
            if not transcription and row.get("voice_mode") != "livekit":
                text, _error = transcribe_recording(url)
                if text:
                    transcription = text
            update_call_recording(call_sid, url, recording.sid or "", transcription or None)
            row = get_call_by_sid(call_sid) or row
            break

    conversation = row.get("conversation_log") or []
    formatted = format_conversation_transcript(conversation)
    if formatted and not (row.get("transcription") or "").strip():
        update_call_transcription(call_sid, formatted)

    return True


def sync_calls(calls: list[dict[str, Any]], limit: int = 12) -> int:
    synced = 0
    for row in calls[:limit]:
        sid = row.get("call_sid") or ""
        needs_sync = (
            not row.get("recording_url")
            or row.get("status") in {"initiated", "ringing", "in-progress", "answered", "queued"}
            or not (row.get("transcription") or "").strip()
        )
        if sid and needs_sync and sync_call_from_twilio(sid):
            synced += 1
    return synced
