"""Persistent login sessions stored server-side with opaque browser tokens."""

from __future__ import annotations

import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional

from ui.database import _conn

COOKIE_NAME = "ndu_auth"
DEFAULT_SESSION_DAYS = 30


def session_ttl_days() -> int:
    raw = os.getenv("APP_SESSION_DAYS", str(DEFAULT_SESSION_DAYS)).strip()
    try:
        days = int(raw)
    except ValueError:
        return DEFAULT_SESSION_DAYS
    return max(1, min(days, 90))


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def init_sessions_table() -> None:
    with _conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS auth_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                token_hash TEXT NOT NULL UNIQUE,
                user_id INTEGER NOT NULL,
                expires_at TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def _purge_expired() -> None:
    now = datetime.now(timezone.utc).replace(tzinfo=None).isoformat(timespec="seconds")
    with _conn() as conn:
        conn.execute("DELETE FROM auth_sessions WHERE expires_at <= ?", (now,))


def create_session_token(user_id: int, days: Optional[int] = None) -> str:
    init_sessions_table()
    _purge_expired()
    ttl_days = days if days is not None else session_ttl_days()
    token = secrets.token_urlsafe(32)
    expires = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=ttl_days)
    with _conn() as conn:
        conn.execute(
            """
            INSERT INTO auth_sessions (token_hash, user_id, expires_at)
            VALUES (?, ?, ?)
            """,
            (_hash_token(token), int(user_id), expires.isoformat(timespec="seconds")),
        )
    return token


def resolve_session_token(token: str) -> Optional[dict[str, int | str]]:
    clean = (token or "").strip()
    if not clean:
        return None

    init_sessions_table()
    _purge_expired()
    now = datetime.now(timezone.utc).replace(tzinfo=None).isoformat(timespec="seconds")
    with _conn() as conn:
        row = conn.execute(
            """
            SELECT u.id, u.username
            FROM auth_sessions s
            JOIN users u ON u.id = s.user_id
            WHERE s.token_hash = ? AND s.expires_at > ?
            """,
            (_hash_token(clean), now),
        ).fetchone()
    if not row:
        return None
    return {"user_id": int(row[0]), "username": str(row[1])}


def revoke_session_token(token: str) -> None:
    clean = (token or "").strip()
    if not clean:
        return
    with _conn() as conn:
        conn.execute("DELETE FROM auth_sessions WHERE token_hash = ?", (_hash_token(clean),))
