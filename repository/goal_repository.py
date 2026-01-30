"""Goal repository for CRUD on Goal entity."""

from datetime import datetime
from typing import List, Optional

from repository.database import Database, DatabaseError, get_database
from models import Goal
from models.enums import GoalCategory, FrequencyType


class GoalRepository:
    """Data access for Goal entity."""

    def __init__(self, db: Optional[Database] = None) -> None:
        self._db = db or get_database()

    def get_by_id(self, goal_id: str) -> Optional[Goal]:
        """Return goal by id or None."""
        try:
            conn = self._db.connect()
            row = conn.execute(
                """SELECT goal_id, user_id, title, description, category, color_hex,
                          frequency_type, created_at, is_archived, current_streak, longest_streak
                   FROM goal WHERE goal_id = ?""",
                (goal_id,),
            ).fetchone()
            if row is None:
                return None
            return self._row_to_goal(row)
        except Exception as e:
            raise DatabaseError(f"get_by_id failed: {e}") from e

    def get_all_by_user(self, user_id: str, include_archived: bool = False) -> List[Goal]:
        """Return all goals for user, optionally including archived."""
        try:
            conn = self._db.connect()
            if include_archived:
                rows = conn.execute(
                    """SELECT goal_id, user_id, title, description, category, color_hex,
                              frequency_type, created_at, is_archived, current_streak, longest_streak
                       FROM goal WHERE user_id = ?""",
                    (user_id,),
                ).fetchall()
            else:
                rows = conn.execute(
                    """SELECT goal_id, user_id, title, description, category, color_hex,
                              frequency_type, created_at, is_archived, current_streak, longest_streak
                       FROM goal WHERE user_id = ? AND is_archived = 0""",
                    (user_id,),
                ).fetchall()
            return [self._row_to_goal(r) for r in rows]
        except Exception as e:
            raise DatabaseError(f"get_all_by_user failed: {e}") from e

    def save(self, goal: Goal) -> None:
        """Insert or replace goal."""
        try:
            conn = self._db.connect()
            conn.execute(
                """INSERT OR REPLACE INTO goal
                   (goal_id, user_id, title, description, category, color_hex, frequency_type,
                    created_at, is_archived, current_streak, longest_streak)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    goal.goal_id,
                    goal.user_id,
                    goal.title,
                    goal.description,
                    goal.category.value if hasattr(goal.category, "value") else str(goal.category),
                    goal.color_hex,
                    goal.frequency.value if hasattr(goal.frequency, "value") else str(goal.frequency),
                    goal.created_at.isoformat() if goal.created_at else None,
                    1 if goal.is_archived else 0,
                    goal.current_streak,
                    goal.longest_streak,
                ),
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"save goal failed: {e}") from e

    def delete(self, goal_id: str) -> None:
        """Delete goal by id."""
        try:
            conn = self._db.connect()
            conn.execute("DELETE FROM goal WHERE goal_id = ?", (goal_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"delete goal failed: {e}") from e

    def _row_to_goal(self, row) -> Goal:
        """Map DB row to Goal model."""
        return Goal(
            goal_id=row["goal_id"],
            user_id=row["user_id"],
            title=row["title"],
            description=row["description"] or "",
            category=GoalCategory(row["category"]) if row["category"] else GoalCategory.OTHER,
            color_hex=row["color_hex"] or "#4CAF50",
            frequency=FrequencyType(row["frequency_type"]) if row["frequency_type"] else FrequencyType.DAILY,
            created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else datetime.now(),
            is_archived=bool(row["is_archived"]),
            current_streak=row["current_streak"] or 0,
            longest_streak=row["longest_streak"] or 0,
        )
