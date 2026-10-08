import sqlite3
from datetime import datetime, timezone
from typing import Optional
from src.exceptions import URLNotFoundException


class SQLiteRepository:
    def __init__(self, db_path: str = "urls.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path, timeout=20.0, check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL;")
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS urls (
                    short_code TEXT PRIMARY KEY,
                    original_url TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    clicks INTEGER DEFAULT 0
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS sequence (
                    id INTEGER PRIMARY KEY AUTOINCREMENT
                )
                """
            )
            conn.commit()

    def check_health(self) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1;")
            return cursor.fetchone() is not None

    def get_next_sequence_id(self) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO sequence DEFAULT VALUES;")
            conn.commit()
            return cursor.lastrowid

    def save(self, short_code: str, original_url: str) -> dict:
        created_at = datetime.now(timezone.utc).isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO urls (short_code, original_url, created_at, clicks)
                VALUES (?, ?, ?, 0)
                """,
                (short_code, original_url, created_at),
            )
            conn.commit()
        return {
            "short_code": short_code,
            "original_url": original_url,
            "created_at": created_at,
            "clicks": 0,
        }

    def get_by_code(self, short_code: str) -> Optional[dict]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT short_code, original_url, created_at, clicks "
                "FROM urls WHERE short_code = ?",
                (short_code,),
            )
            row = cursor.fetchone()
            if row:
                return {
                    "short_code": row[0],
                    "original_url": row[1],
                    "created_at": row[2],
                    "clicks": row[3],
                }
        return None

    def increment_clicks(self, short_code: str) -> str:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?",
                (short_code,),
            )
            if cursor.rowcount == 0:
                raise URLNotFoundException(f"URL code '{short_code}' not found.")
            conn.commit()
            cursor.execute(
                "SELECT original_url FROM urls WHERE short_code = ?",
                (short_code,),
            )
            return cursor.fetchone()[0]
