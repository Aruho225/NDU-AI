import json
from typing import Any, Optional

from ui.database import _conn

ACTIVE_CALL_STATUSES = frozenset(
    {
        "queued",
        "initiated",
        "ringing",
        "in-progress",
        "answered",
    }
)

_CALL_SELECT = """
    SELECT id, call_sid, user_id, direction, from_number, to_number, status,
           duration_seconds, recording_url, recording_sid, transcription,
           conversation_log, livekit_room, voice_mode, created_at, completed_at
    FROM calls
"""


def init_calls_table() -> None:
    with _conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS calls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                call_sid TEXT NOT NULL UNIQUE,
                user_id INTEGER,
                direction TEXT NOT NULL,
                from_number TEXT,
                to_number TEXT,
                status TEXT DEFAULT 'initiated',
                duration_seconds INTEGER DEFAULT 0,
                recording_url TEXT,
                recording_sid TEXT,
                transcription TEXT,
                conversation_log TEXT DEFAULT '[]',
                livekit_room TEXT,
                voice_mode TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                completed_at TEXT
            )
            """
        )
        cols = {row[1] for row in conn.execute("PRAGMA table_info(calls)").fetchall()}
        if "livekit_room" not in cols:
            conn.execute("ALTER TABLE calls ADD COLUMN livekit_room TEXT")
        if "voice_mode" not in cols:
            conn.execute("ALTER TABLE calls ADD COLUMN voice_mode TEXT")


def create_call(
    call_sid: str,
    direction: str,
    from_number: str,
    to_number: str,
    user_id: Optional[int] = None,
    voice_mode: Optional[str] = None,
    livekit_room: Optional[str] = None,
) -> int:
    with _conn() as conn:
        cursor = conn.execute(
            """
            INSERT INTO calls (
                call_sid, user_id, direction, from_number, to_number,
                status, voice_mode, livekit_room
            )
            VALUES (?, ?, ?, ?, ?, 'initiated', ?, ?)
            """,
            (call_sid, user_id, direction, from_number, to_number, voice_mode, livekit_room),
        )
    return int(cursor.lastrowid)


def get_call_by_sid(call_sid: str) -> Optional[dict[str, Any]]:
    with _conn() as conn:
        row = conn.execute(f"{_CALL_SELECT} WHERE call_sid = ?", (call_sid,)).fetchone()
    return _row_to_call(row) if row else None


def get_call(call_id: int) -> Optional[dict[str, Any]]:
    with _conn() as conn:
        row = conn.execute(f"{_CALL_SELECT} WHERE id = ?", (call_id,)).fetchone()
    return _row_to_call(row) if row else None


def update_call_status(call_sid: str, status: str, duration_seconds: int = 0) -> None:
    with _conn() as conn:
        if status in {"completed", "busy", "failed", "no-answer", "canceled"}:
            conn.execute(
                """
                UPDATE calls
                SET status = ?, duration_seconds = ?, completed_at = CURRENT_TIMESTAMP
                WHERE call_sid = ?
                """,
                (status, duration_seconds, call_sid),
            )
        else:
            conn.execute(
                "UPDATE calls SET status = ? WHERE call_sid = ?",
                (status, call_sid),
            )


def update_call_livekit_room(call_sid: str, room_name: str, voice_mode: str = "livekit") -> None:
    with _conn() as conn:
        conn.execute(
            "UPDATE calls SET livekit_room = ?, voice_mode = ? WHERE call_sid = ?",
            (room_name, voice_mode, call_sid),
        )


def update_call_recording(
    call_sid: str,
    recording_url: str,
    recording_sid: str,
    transcription: Optional[str] = None,
) -> None:
    with _conn() as conn:
        if transcription:
            conn.execute(
                """
                UPDATE calls
                SET recording_url = ?, recording_sid = ?, transcription = ?
                WHERE call_sid = ?
                """,
                (recording_url, recording_sid, transcription, call_sid),
            )
        else:
            conn.execute(
                """
                UPDATE calls SET recording_url = ?, recording_sid = ?
                WHERE call_sid = ?
                """,
                (recording_url, recording_sid, call_sid),
            )


def append_call_turn(call_sid: str, role: str, text: str) -> None:
    clean = text.strip()
    if not clean:
        return
    row = get_call_by_sid(call_sid)
    if not row:
        return
    log = row.get("conversation_log") or []
    if log and log[-1].get("role") == role:
        previous = (log[-1].get("text") or "").strip()
        if clean == previous:
            return
        if clean.startswith(previous) or len(clean) > len(previous):
            log[-1]["text"] = clean
        else:
            log.append({"role": role, "text": clean})
    else:
        log.append({"role": role, "text": clean})
    with _conn() as conn:
        conn.execute(
            "UPDATE calls SET conversation_log = ? WHERE call_sid = ?",
            (json.dumps(log), call_sid),
        )


def set_conversation_log(call_sid: str, conversation: list[dict[str, Any]]) -> None:
    if not call_sid:
        return
    with _conn() as conn:
        conn.execute(
            "UPDATE calls SET conversation_log = ? WHERE call_sid = ?",
            (json.dumps(conversation), call_sid),
        )


def update_call_transcription(call_sid: str, transcription: str) -> None:
    clean = transcription.strip()
    if not call_sid or not clean:
        return
    with _conn() as conn:
        conn.execute(
            "UPDATE calls SET transcription = ? WHERE call_sid = ?",
            (clean, call_sid),
        )


def is_call_active(status: str) -> bool:
    return (status or "").lower() in ACTIVE_CALL_STATUSES


def load_watchable_calls(user_id: Optional[int] = None, limit: int = 10) -> list[dict[str, Any]]:
    """Active calls plus recently completed calls still worth watching in the UI."""
    with _conn() as conn:
        if user_id is not None:
            rows = conn.execute(
                f"""
                {_CALL_SELECT}
                WHERE (user_id = ? OR direction = 'inbound')
                  AND (
                    lower(status) IN ('queued', 'initiated', 'ringing', 'in-progress', 'answered')
                    OR (
                      lower(status) = 'completed'
                      AND datetime(created_at) >= datetime('now', '-3 hours')
                    )
                  )
                ORDER BY id DESC
                LIMIT ?
                """,
                (user_id, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                f"""
                {_CALL_SELECT}
                WHERE lower(status) IN ('queued', 'initiated', 'ringing', 'in-progress', 'answered')
                   OR (
                     lower(status) = 'completed'
                     AND datetime(created_at) >= datetime('now', '-3 hours')
                   )
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
    return [_row_to_call(row) for row in rows]


def load_active_calls(user_id: Optional[int] = None, limit: int = 10) -> list[dict[str, Any]]:
    placeholders = ",".join("?" for _ in ACTIVE_CALL_STATUSES)
    statuses = tuple(ACTIVE_CALL_STATUSES)
    with _conn() as conn:
        if user_id is not None:
            rows = conn.execute(
                f"""
                {_CALL_SELECT}
                WHERE (user_id = ? OR direction = 'inbound')
                  AND lower(status) IN ({placeholders})
                ORDER BY id DESC
                LIMIT ?
                """,
                (user_id, *statuses, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                f"""
                {_CALL_SELECT}
                WHERE lower(status) IN ({placeholders})
                ORDER BY id DESC
                LIMIT ?
                """,
                (*statuses, limit),
            ).fetchall()
    return [_row_to_call(row) for row in rows]


def load_calls_in_range(
    user_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 500,
) -> list[dict[str, Any]]:
    """Load calls between start_date and end_date (YYYY-MM-DD), inclusive."""
    clauses = ["1=1"]
    params: list[Any] = []
    if user_id is not None:
        clauses.append("(user_id = ? OR direction = 'inbound')")
        params.append(user_id)
    if start_date:
        clauses.append("date(created_at) >= date(?)")
        params.append(start_date)
    if end_date:
        clauses.append("date(created_at) <= date(?)")
        params.append(end_date)
    where = " AND ".join(clauses)
    params.append(limit)
    with _conn() as conn:
        rows = conn.execute(
            f"{_CALL_SELECT} WHERE {where} ORDER BY id DESC LIMIT ?",
            tuple(params),
        ).fetchall()
    return [_row_to_call(row) for row in rows]


def load_recent_calls(user_id: Optional[int] = None, limit: int = 30) -> list[dict[str, Any]]:
    with _conn() as conn:
        if user_id is not None:
            rows = conn.execute(
                f"""
                {_CALL_SELECT}
                WHERE user_id = ? OR direction = 'inbound'
                ORDER BY id DESC
                LIMIT ?
                """,
                (user_id, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                f"{_CALL_SELECT} ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
    return [_row_to_call(row) for row in rows]


def delete_call(call_id: int) -> None:
    with _conn() as conn:
        conn.execute("DELETE FROM calls WHERE id = ?", (call_id,))


def _row_to_call(row: tuple) -> dict[str, Any]:
    if len(row) >= 16:
        (
            call_id,
            call_sid,
            user_id,
            direction,
            from_number,
            to_number,
            status,
            duration_seconds,
            recording_url,
            recording_sid,
            transcription,
            conversation_log,
            livekit_room,
            voice_mode,
            created_at,
            completed_at,
        ) = row[:16]
    else:
        (
            call_id,
            call_sid,
            user_id,
            direction,
            from_number,
            to_number,
            status,
            duration_seconds,
            recording_url,
            recording_sid,
            transcription,
            conversation_log,
            created_at,
            completed_at,
        ) = row
        livekit_room = ""
        voice_mode = ""

    try:
        log = json.loads(conversation_log or "[]")
    except json.JSONDecodeError:
        log = []
    return {
        "id": call_id,
        "call_sid": call_sid,
        "user_id": user_id,
        "direction": direction,
        "from_number": from_number or "",
        "to_number": to_number or "",
        "status": status or "unknown",
        "duration_seconds": duration_seconds or 0,
        "recording_url": recording_url or "",
        "recording_sid": recording_sid or "",
        "transcription": transcription or "",
        "conversation_log": log,
        "livekit_room": livekit_room or "",
        "voice_mode": voice_mode or "",
        "created_at": created_at or "",
        "completed_at": completed_at or "",
    }
