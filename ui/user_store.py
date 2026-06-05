import hashlib
import hmac
import os
import re
import secrets
import sqlite3
from typing import Optional

from ui.database import _conn

_USERNAME_RE = re.compile(r"^[a-zA-Z0-9_]{3,32}$")
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def init_users_table() -> None:
    from ui.session_store import init_auth_sessions_table

    with _conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE COLLATE NOCASE,
                email TEXT,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        init_auth_sessions_table(conn)
        cols = {row[1] for row in conn.execute("PRAGMA table_info(conversations)").fetchall()}
        if "user_id" not in cols:
            conn.execute("ALTER TABLE conversations ADD COLUMN user_id INTEGER")


def _hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 120_000)
    return f"{salt}${digest.hex()}"


def _verify_password(password: str, stored: str) -> bool:
    try:
        salt, digest_hex = stored.split("$", 1)
    except ValueError:
        return False
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 120_000)
    return hmac.compare_digest(digest.hex(), digest_hex)


def validate_username(username: str) -> Optional[str]:
    name = username.strip()
    if not _USERNAME_RE.fullmatch(name):
        return "Username must be 3–32 characters (letters, numbers, underscore)."
    return None


def validate_password(password: str) -> Optional[str]:
    if len(password) < 8:
        return "Password must be at least 8 characters."
    return None


def validate_email(email: str) -> Optional[str]:
    clean = email.strip()
    if not clean:
        return None
    if not _EMAIL_RE.fullmatch(clean):
        return "Enter a valid email address."
    return None


def register_user(username: str, password: str, email: str = "") -> tuple[bool, str]:
    issue = validate_username(username) or validate_password(password)
    if issue:
        return False, issue
    email_issue = validate_email(email)
    if email_issue:
        return False, email_issue

    clean_email = email.strip().lower() or None
    try:
        with _conn() as conn:
            conn.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username.strip(), clean_email, _hash_password(password)),
            )
    except sqlite3.IntegrityError:
        return False, "That username is already taken."
    return True, "Account created. You can sign in now."


def authenticate_user(username: str, password: str) -> tuple[bool, Optional[int], str]:
    with _conn() as conn:
        row = conn.execute(
            "SELECT id, password_hash FROM users WHERE username = ? COLLATE NOCASE",
            (username.strip(),),
        ).fetchone()
    if not row:
        return False, None, "Invalid username or password."
    user_id, stored = row
    if not _verify_password(password, stored):
        return False, None, "Invalid username or password."
    return True, int(user_id), "Signed in successfully."


def reset_password(username: str, email: str, new_password: str) -> tuple[bool, str]:
    issue = validate_password(new_password)
    if issue:
        return False, issue
    if not email.strip():
        return False, "Enter the email used when you registered."

    with _conn() as conn:
        row = conn.execute(
            "SELECT id FROM users WHERE username = ? COLLATE NOCASE AND lower(email) = lower(?)",
            (username.strip(), email.strip()),
        ).fetchone()
        if not row:
            return False, "No account matches that username and email."
        conn.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (_hash_password(new_password), row[0]),
        )
    return True, "Password updated. Sign in with your new password."


def seed_admin_from_env() -> None:
    username = os.getenv("APP_LOGIN_USER", "").strip()
    password = os.getenv("APP_LOGIN_PASSWORD", "").strip()
    if not username or not password:
        return
    with _conn() as conn:
        count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if count:
        return
    register_user(username, password, email=os.getenv("APP_LOGIN_EMAIL", "").strip())
