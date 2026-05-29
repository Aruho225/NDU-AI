import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent.parent / "chat_history.db"


def _conn() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    from ui.call_store import init_calls_table
    from ui.user_store import init_users_table

    with _conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
    init_users_table()
    init_calls_table()


def save_turn(question: str, answer: str, user_id: int) -> int:
    with _conn() as conn:
        cursor = conn.execute(
            "INSERT INTO conversations (question, answer, user_id) VALUES (?, ?, ?)",
            (question, answer, user_id),
        )
    return int(cursor.lastrowid)


def load_recent_turns(user_id: int, limit: int = 8) -> list[dict[str, str | int]]:
    with _conn() as conn:
        rows = conn.execute(
            """
            SELECT id, question, answer
            FROM conversations
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (user_id, limit),
        ).fetchall()
    return [{"id": row_id, "q": q, "a": a} for row_id, q, a in rows]


def rename_turn(turn_id: int, new_question: str) -> None:
    with _conn() as conn:
        conn.execute(
            "UPDATE conversations SET question = ? WHERE id = ?",
            (new_question, turn_id),
        )


def delete_turn(turn_id: int) -> None:
    with _conn() as conn:
        conn.execute("DELETE FROM conversations WHERE id = ?", (turn_id,))
