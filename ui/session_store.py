import hashlib
import secrets
import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Optional


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _token_hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def init_auth_sessions_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS auth_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token_hash TEXT NOT NULL UNIQUE,
            expires_at TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    )


def create_session_token(user_id: int, days: int = 30) -> str:
    from ui.database import _conn

    token = secrets.token_urlsafe(32)
    expires = (_utc_now() + timedelta(days=days)).isoformat()
    with _conn() as conn:
        conn.execute(
            "INSERT INTO auth_sessions (user_id, token_hash, expires_at) VALUES (?, ?, ?)",
            (user_id, _token_hash(token), expires),
        )
    return token


def resolve_session_token(token: str) -> Optional[dict[str, object]]:
    from ui.database import _conn

    if not token.strip():
        return None
    digest = _token_hash(token.strip())
    with _conn() as conn:
        row = conn.execute(
            """
            SELECT s.user_id, u.username, s.expires_at
            FROM auth_sessions s
            JOIN users u ON u.id = s.user_id
            WHERE s.token_hash = ?
            """,
            (digest,),
        ).fetchone()
    if not row:
        return None
    expires = datetime.fromisoformat(row[2])
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)
    if expires < _utc_now():
        revoke_session_token(token)
        return None
    return {"user_id": int(row[0]), "username": str(row[1])}


def revoke_session_token(token: str) -> None:
    from ui.database import _conn

    digest = _token_hash(token.strip())
    with _conn() as conn:
        conn.execute("DELETE FROM auth_sessions WHERE token_hash = ?", (digest,))
