"""Task service (use cases: CRUD, complete, filter)."""

import uuid
from datetime import datetime
from typing import List, Optional

from repository import TaskRepository
from repository.database import DatabaseError
from models import Task
from models.enums import TaskStatus, TaskType, Priority


class TaskService:
    """
    Use cases for Task: Create, Read, Update, Delete, Complete, and list/filter.

    Follows sequence diagram: Controller calls Service, Service uses Repository.
    """

    def __init__(self, task_repo: Optional[TaskRepository] = None) -> None:
        self._repo = task_repo or TaskRepository()

    def get_by_id(self, task_id: str) -> Optional[Task]:
        """Return task by id or None."""
        try:
            return self._repo.get_by_id(task_id)
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"get_by_id failed: {e}") from e

    def get_tasks_for_user(
        self,
        user_id: str,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        include_completed: bool = True,
        search_query: Optional[str] = None,
    ) -> List[Task]:
        """
        Return tasks for user with optional date range and search filter.

        Args:
            user_id: Owner user id.
            from_date: Only tasks due on or after this date.
            to_date: Only tasks due on or before this date.
            include_completed: Include completed tasks.
            search_query: Filter by title/description containing this string.

        Returns:
            List of tasks ordered by due date.
        """
        try:
            return self._repo.get_all_by_user(
                user_id=user_id,
                from_date=from_date,
                to_date=to_date,
                include_completed=include_completed,
                search_query=search_query,
            )
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"get_tasks_for_user failed: {e}") from e

    def create_task(
        self,
        user_id: str,
        title: str,
        description: str = "",
        due_date_time: Optional[datetime] = None,
        duration_minutes: int = 0,
        priority: Priority = Priority.MEDIUM,
        goal_id: Optional[str] = None,
        task_type: TaskType = TaskType.FREE,
    ) -> Task:
        """
        Create a new task and persist it.

        Returns:
            Created task with assigned task_id.
        """
        task_id = str(uuid.uuid4())
        status = TaskStatus.UPCOMING if due_date_time else TaskStatus.PENDING
        if due_date_time:
            now = datetime.now()
            if due_date_time.date() == now.date():
                status = TaskStatus.TODAY
            elif due_date_time < now:
                status = TaskStatus.OVERDUE
        task = Task(
            task_id=task_id,
            user_id=user_id,
            goal_id=goal_id,
            title=title,
            description=description,
            due_date_time=due_date_time,
            duration_minutes=duration_minutes,
            priority=priority,
            type=task_type,
            status=status,
            progress_percent=0,
        )
        try:
            self._repo.save(task)
            return task
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"create_task failed: {e}") from e

    def update_task(
        self,
        task_id: str,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        due_date_time: Optional[datetime] = None,
        duration_minutes: Optional[int] = None,
        priority: Optional[Priority] = None,
        progress_percent: Optional[int] = None,
        status: Optional[TaskStatus] = None,
    ) -> Optional[Task]:
        """
        Update task by id. Only provided fields are updated.

        Returns:
            Updated task or None if not found.
        """
        task = self._repo.get_by_id(task_id)
        if task is None:
            return None
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if due_date_time is not None:
            task.due_date_time = due_date_time
        if duration_minutes is not None:
            task.duration_minutes = duration_minutes
        if priority is not None:
            task.priority = priority
        if progress_percent is not None:
            task.progress_percent = max(0, min(100, progress_percent))
        if status is not None:
            task.status = status
        task.updated_at = datetime.now()
        try:
            self._repo.save(task)
            return task
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"update_task failed: {e}") from e

    def complete_task(self, task_id: str) -> Optional[Task]:
        """
        Mark task as completed (execute completion flow per sequence diagram).

        Returns:
            Completed task or None if not found.
        """
        task = self._repo.get_by_id(task_id)
        if task is None:
            return None
        task.complete()
        try:
            self._repo.save(task)
            return task
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"complete_task failed: {e}") from e

    def cancel_task(self, task_id: str) -> Optional[Task]:
        """Mark task as cancelled/rejected. Returns updated task or None."""
        return self.update_task(task_id, status=TaskStatus.CANCELLED)

    def set_task_running(self, task_id: str) -> Optional[Task]:
        """Set task status to in_progress. Returns updated task or None."""
        return self.update_task(task_id, status=TaskStatus.IN_PROGRESS)

    def delete_task(self, task_id: str) -> bool:
        """Delete task by id. Returns True if deleted."""
        try:
            self._repo.delete(task_id)
            return True
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"delete_task failed: {e}") from e
