"""User repository for CRUD on User entity."""

from datetime import datetime
from typing import Optional

from repository.database import Database, DatabaseError, get_database
from models import User
from models.user import NotificationPreferences


class UserRepository:
    """Data access for User and preferences."""

    def __init__(self, db: Optional[Database] = None) -> None:
        self._db = db or get_database()

    def get_by_id(self, user_id: str) -> Optional[User]:
        """Return user by id or None if not found."""
        try:
            conn = self._db.connect()
            row = conn.execute(
                "SELECT user_id, name, email, is_student_mode, created_at FROM user WHERE user_id = ?",
                (user_id,),
            ).fetchone()
            if row is None:
                return None
            prefs = self._get_preferences(conn, user_id)
            return User(
                user_id=row["user_id"],
                name=row["name"],
                email=row["email"],
                is_student_mode=bool(row["is_student_mode"]),
                preferences=prefs,
                created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else datetime.now(),
            )
        except Exception as e:
            raise DatabaseError(f"get_by_id failed: {e}") from e

    def _get_preferences(self, conn, user_id: str) -> NotificationPreferences:
        """Load preferences for user."""
        row = conn.execute(
            "SELECT notifications_enabled, default_reminder_minutes FROM user_preferences WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        if row is None:
            return NotificationPreferences()
        return NotificationPreferences(
            enabled=bool(row["notifications_enabled"]),
            default_reminder_minutes=row["default_reminder_minutes"] or 15,
        )

    def save(self, user: User) -> None:
        """Insert or replace user and preferences."""
        try:
            conn = self._db.connect()
            conn.execute(
                """INSERT OR REPLACE INTO user (user_id, name, email, is_student_mode, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    user.user_id,
                    user.name,
                    user.email,
                    1 if user.is_student_mode else 0,
                    user.created_at.isoformat() if user.created_at else None,
                    datetime.now().isoformat(),
                ),
            )
            conn.execute(
                """INSERT OR REPLACE INTO user_preferences (pref_id, user_id, notifications_enabled, default_reminder_minutes)
                   VALUES (?, ?, ?, ?)""",
                (
                    f"pref_{user.user_id}",
                    user.user_id,
                    1 if user.preferences.enabled else 0,
                    user.preferences.default_reminder_minutes,
                ),
            )
            conn.commit()
        except Exception as e:
            try:
                conn.rollback()
            except NameError:
                pass
            raise DatabaseError(f"save user failed: {e}") from e
