import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent.parent / "chat_history.db"


def _conn() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
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


def save_turn(question: str, answer: str) -> int:
    with _conn() as conn:
        cursor = conn.execute(
            "INSERT INTO conversations (question, answer) VALUES (?, ?)",
            (question, answer),
        )
    return int(cursor.lastrowid)


def load_recent_turns(limit: int = 8) -> list[dict[str, str | int]]:
    with _conn() as conn:
        rows = conn.execute(
            """
            SELECT id, question, answer
            FROM conversations
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
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
