import json
from typing import Any, Optional

from ui.database import _conn


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
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                completed_at TEXT
            )
            """
        )


def create_call(
    call_sid: str,
    direction: str,
    from_number: str,
    to_number: str,
    user_id: Optional[int] = None,
) -> int:
    with _conn() as conn:
        cursor = conn.execute(
            """
            INSERT INTO calls (call_sid, user_id, direction, from_number, to_number, status)
            VALUES (?, ?, ?, ?, ?, 'initiated')
            """,
            (call_sid, user_id, direction, from_number, to_number),
        )
    return int(cursor.lastrowid)


def get_call_by_sid(call_sid: str) -> Optional[dict[str, Any]]:
    with _conn() as conn:
        row = conn.execute(
            """
            SELECT id, call_sid, user_id, direction, from_number, to_number, status,
                   duration_seconds, recording_url, recording_sid, transcription,
                   conversation_log, created_at, completed_at
            FROM calls WHERE call_sid = ?
            """,
            (call_sid,),
        ).fetchone()
    return _row_to_call(row) if row else None


def get_call(call_id: int) -> Optional[dict[str, Any]]:
    with _conn() as conn:
        row = conn.execute(
            """
            SELECT id, call_sid, user_id, direction, from_number, to_number, status,
                   duration_seconds, recording_url, recording_sid, transcription,
                   conversation_log, created_at, completed_at
            FROM calls WHERE id = ?
            """,
            (call_id,),
        ).fetchone()
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
    log.append({"role": role, "text": clean})
    with _conn() as conn:
        conn.execute(
            "UPDATE calls SET conversation_log = ? WHERE call_sid = ?",
            (json.dumps(log), call_sid),
        )


def load_recent_calls(user_id: Optional[int] = None, limit: int = 30) -> list[dict[str, Any]]:
    with _conn() as conn:
        if user_id is not None:
            rows = conn.execute(
                """
                SELECT id, call_sid, user_id, direction, from_number, to_number, status,
                       duration_seconds, recording_url, recording_sid, transcription,
                       conversation_log, created_at, completed_at
                FROM calls
                WHERE user_id = ? OR direction = 'inbound'
                ORDER BY id DESC
                LIMIT ?
                """,
                (user_id, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT id, call_sid, user_id, direction, from_number, to_number, status,
                       duration_seconds, recording_url, recording_sid, transcription,
                       conversation_log, created_at, completed_at
                FROM calls
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
    return [_row_to_call(row) for row in rows]


def delete_call(call_id: int) -> None:
    with _conn() as conn:
        conn.execute("DELETE FROM calls WHERE id = ?", (call_id,))


def _row_to_call(row: tuple) -> dict[str, Any]:
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
        "created_at": created_at or "",
        "completed_at": completed_at or "",
    }
