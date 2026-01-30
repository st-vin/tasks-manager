"""Task repository for CRUD on Task entity."""

from datetime import datetime
from typing import List, Optional

from repository.database import Database, DatabaseError, get_database
from models import Task
from models.enums import Priority, TaskType, TaskStatus


class TaskRepository:
    """Data access for Task entity."""

    def __init__(self, db: Optional[Database] = None) -> None:
        self._db = db or get_database()

    def get_by_id(self, task_id: str) -> Optional[Task]:
        """Return task by id or None."""
        try:
            conn = self._db.connect()
            row = conn.execute(
                """SELECT task_id, user_id, goal_id, title, description, due_date_time,
                          duration_minutes, priority, task_type, is_completed, completed_at,
                          status, progress_percent, created_at, updated_at
                   FROM task WHERE task_id = ?""",
                (task_id,),
            ).fetchone()
            if row is None:
                return None
            return self._row_to_task(row)
        except Exception as e:
            raise DatabaseError(f"get_by_id failed: {e}") from e

    def get_all_by_user(
        self,
        user_id: str,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        include_completed: bool = True,
        search_query: Optional[str] = None,
    ) -> List[Task]:
        """
        Return tasks for user, optionally filtered by date range and search.

        Args:
            user_id: Owner user id.
            from_date: Only tasks due on or after this date (date part).
            to_date: Only tasks due on or before this date (date part).
            include_completed: Include completed tasks.
            search_query: If set, filter by title/description containing this string (case-insensitive).
        """
        try:
            conn = self._db.connect()
            sql = """SELECT task_id, user_id, goal_id, title, description, due_date_time,
                            duration_minutes, priority, task_type, is_completed, completed_at,
                            status, progress_percent, created_at, updated_at
                     FROM task WHERE user_id = ?"""
            params: list = [user_id]
            if not include_completed:
                sql += " AND is_completed = 0"
            if from_date is not None:
                sql += " AND date(due_date_time) >= date(?)"
                params.append(from_date.strftime("%Y-%m-%d"))
            if to_date is not None:
                sql += " AND date(due_date_time) <= date(?)"
                params.append(to_date.strftime("%Y-%m-%d"))
            if search_query and search_query.strip():
                sql += " AND (title LIKE ? OR description LIKE ?)"
                q = f"%{search_query.strip()}%"
                params.extend([q, q])
            sql += " ORDER BY due_date_time IS NULL, due_date_time ASC, created_at ASC"
            rows = conn.execute(sql, params).fetchall()
            return [self._row_to_task(r) for r in rows]
        except Exception as e:
            raise DatabaseError(f"get_all_by_user failed: {e}") from e

    def save(self, task: Task) -> None:
        """Insert or replace task."""
        try:
            conn = self._db.connect()
            conn.execute(
                """INSERT OR REPLACE INTO task
                   (task_id, user_id, goal_id, title, description, due_date_time, duration_minutes,
                    priority, task_type, is_completed, completed_at, status, progress_percent, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    task.task_id,
                    task.user_id,
                    task.goal_id,
                    task.title,
                    task.description,
                    task.due_date_time.isoformat() if task.due_date_time else None,
                    task.duration_minutes,
                    task.priority.value if hasattr(task.priority, "value") else str(task.priority),
                    task.type.value if hasattr(task.type, "value") else str(task.type),
                    1 if task.is_completed else 0,
                    task.completed_at.isoformat() if task.completed_at else None,
                    task.status.value if hasattr(task.status, "value") else str(task.status),
                    task.progress_percent,
                    task.created_at.isoformat() if task.created_at else None,
                    task.updated_at.isoformat() if task.updated_at else datetime.now().isoformat(),
                ),
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"save task failed: {e}") from e

    def delete(self, task_id: str) -> None:
        """Delete task by id."""
        try:
            conn = self._db.connect()
            conn.execute("DELETE FROM task WHERE task_id = ?", (task_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise DatabaseError(f"delete task failed: {e}") from e

    def _row_to_task(self, row) -> Task:
        """Map DB row to Task model."""
        return Task(
            task_id=row["task_id"],
            user_id=row["user_id"],
            goal_id=row["goal_id"],
            title=row["title"],
            description=row["description"] or "",
            due_date_time=datetime.fromisoformat(row["due_date_time"]) if row["due_date_time"] else None,
            duration_minutes=row["duration_minutes"] or 0,
            priority=Priority(row["priority"]) if row["priority"] else Priority.MEDIUM,
            type=TaskType(row["task_type"]) if row["task_type"] else TaskType.FREE,
            is_completed=bool(row["is_completed"]),
            completed_at=datetime.fromisoformat(row["completed_at"]) if row["completed_at"] else None,
            status=TaskStatus(row["status"]) if row["status"] else TaskStatus.CREATED,
            progress_percent=row["progress_percent"] or 0,
            created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else None,
            updated_at=datetime.fromisoformat(row["updated_at"]) if row["updated_at"] else None,
        )
