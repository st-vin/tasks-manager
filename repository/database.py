"""SQLite database initialization and schema (ER Diagram compliant)."""

import sqlite3
from pathlib import Path
from typing import Optional

# Default DB path: same directory as this file, or cwd for PyInstaller bundle
def _default_db_path() -> Path:
    """Return path to tasks.db next to the application."""
    base = Path(__file__).resolve().parent.parent
    return base / "tasks.db"


class DatabaseError(Exception):
    """Raised when database operations fail (missing/corrupt file or query error)."""

    pass


class Database:
    """
    SQLite database wrapper with schema creation and error handling.

    Handles missing or corrupt database by recreating schema.
    """

    def __init__(self, path: Optional[Path] = None) -> None:
        """
        Initialize database connection path.

        Args:
            path: Path to SQLite file. If None, uses default tasks.db in project root.
        """
        self._path = path or _default_db_path()
        self._conn: Optional[sqlite3.Connection] = None

    def connect(self) -> sqlite3.Connection:
        """
        Get or create a connection. Creates schema if needed.

        Returns:
            SQLite connection.

        Raises:
            DatabaseError: If connection or schema creation fails.
        """
        if self._conn is not None:
            return self._conn
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._conn = sqlite3.connect(str(self._path), detect_types=sqlite3.PARSE_DECLTYPES)
            self._conn.row_factory = sqlite3.Row
            self._create_schema()
            return self._conn
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to connect to database: {e}") from e

    def _create_schema(self) -> None:
        """Create tables per ER diagram. Idempotent (CREATE TABLE IF NOT EXISTS)."""
        conn = self._conn
        if conn is None:
            return
        try:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS user (
                    user_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    is_student_mode INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT,
                    updated_at TEXT
                );

                CREATE TABLE IF NOT EXISTS user_preferences (
                    pref_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL REFERENCES user(user_id),
                    notifications_enabled INTEGER DEFAULT 1,
                    default_reminder_minutes INTEGER DEFAULT 15
                );

                CREATE TABLE IF NOT EXISTS goal (
                    goal_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL REFERENCES user(user_id),
                    title TEXT NOT NULL,
                    description TEXT,
                    category TEXT,
                    color_hex TEXT,
                    frequency_type TEXT,
                    created_at TEXT,
                    is_archived INTEGER DEFAULT 0,
                    current_streak INTEGER DEFAULT 0,
                    longest_streak INTEGER DEFAULT 0
                );

                CREATE TABLE IF NOT EXISTS task (
                    task_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL REFERENCES user(user_id),
                    goal_id TEXT,
                    title TEXT NOT NULL,
                    description TEXT,
                    due_date_time TEXT,
                    duration_minutes INTEGER DEFAULT 0,
                    priority TEXT,
                    task_type TEXT,
                    is_completed INTEGER NOT NULL DEFAULT 0,
                    completed_at TEXT,
                    status TEXT,
                    progress_percent INTEGER DEFAULT 0,
                    created_at TEXT,
                    updated_at TEXT
                );

                CREATE INDEX IF NOT EXISTS idx_task_user ON task(user_id);
                CREATE INDEX IF NOT EXISTS idx_task_due ON task(due_date_time);
                CREATE INDEX IF NOT EXISTS idx_task_goal ON task(goal_id);
                CREATE INDEX IF NOT EXISTS idx_goal_user ON goal(user_id);
            """)
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()
            raise DatabaseError(f"Failed to create schema: {e}") from e

    def close(self) -> None:
        """Close the connection if open."""
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def __enter__(self) -> "Database":
        self.connect()
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


_db: Optional[Database] = None


def get_database(path: Optional[Path] = None) -> Database:
    """Return singleton Database instance."""
    global _db
    if _db is None:
        _db = Database(path)
    return _db
