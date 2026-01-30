"""Presenter: connects UI to Service Layer (MVP)."""

from datetime import datetime, date, timedelta
from typing import Callable, List, Optional

from models import Task, User
from models.enums import Priority, TaskStatus, TaskType
from services import TaskService, UserService, GoalService
from repository.database import DatabaseError


class TaskPresenter:
    """
    Presenter/Controller: handles user actions and updates the view.

    View calls presenter methods; presenter calls services and then refresh_view(tasks).
    """

    def __init__(
        self,
        task_service: Optional[TaskService] = None,
        user_service: Optional[UserService] = None,
        goal_service: Optional[GoalService] = None,
    ) -> None:
        self._task_service = task_service or TaskService()
        self._user_service = user_service or UserService()
        self._goal_service = goal_service or GoalService()
        self._user: Optional[User] = None
        self._refresh_view: Optional[Callable[[List[Task]], None]] = None
        self._on_error: Optional[Callable[[str], None]] = None
        self._last_date: Optional[date] = None
        self._last_search: Optional[str] = None

    def set_refresh_view(self, callback: Callable[[List[Task]], None]) -> None:
        """Set callback to refresh the task list UI with new tasks."""
        self._refresh_view = callback

    def set_on_error(self, callback: Callable[[str], None]) -> None:
        """Set callback to show error messages."""
        self._on_error = callback

    def get_user(self) -> User:
        """Return current user (creates default if needed)."""
        if self._user is None:
            self._user = self._user_service.get_or_create_default_user()
        return self._user

    def load_tasks(
        self,
        selected_date: Optional[date] = None,
        search_query: Optional[str] = None,
    ) -> None:
        """
        Load tasks for the given date and search query, then refresh the view.
        Stores date/query for subsequent refresh (e.g. after create/update/delete).

        Args:
            selected_date: Filter tasks by due date (day). If None, uses last or today.
            search_query: Filter by title/description. If None, uses last or empty.
        """
        if selected_date is not None:
            self._last_date = selected_date
        if search_query is not None:
            self._last_search = search_query
        date_use = self._last_date or date.today()
        query_use = self._last_search if self._last_search is not None else ""
        user = self.get_user()
        try:
            from_dt = datetime(date_use.year, date_use.month, date_use.day)
            to_dt = datetime(date_use.year, date_use.month, date_use.day, 23, 59, 59)
            tasks = self._task_service.get_tasks_for_user(
                user_id=user.user_id,
                from_date=from_dt,
                to_date=to_dt,
                include_completed=True,
                search_query=query_use.strip() or None,
            )
            if self._refresh_view:
                self._refresh_view(tasks)
        except DatabaseError as e:
            if self._on_error:
                self._on_error(str(e))

    def complete_task(self, task_id: str) -> None:
        """Mark task complete and refresh."""
        try:
            self._task_service.complete_task(task_id)
            self.load_tasks(self._last_date, self._last_search or "")
        except DatabaseError as e:
            if self._on_error:
                self._on_error(str(e))

    def delete_task(self, task_id: str) -> None:
        """Delete task and refresh."""
        try:
            self._task_service.delete_task(task_id)
            self.load_tasks(self._last_date, self._last_search or "")
        except DatabaseError as e:
            if self._on_error:
                self._on_error(str(e))

    def create_task(
        self,
        title: str,
        description: str = "",
        due_date: Optional[datetime] = None,
        duration_minutes: int = 0,
        priority: Priority = Priority.MEDIUM,
        task_type: TaskType = TaskType.FREE,
        goal_id: Optional[str] = None,
    ) -> Optional[Task]:
        """Create task and refresh. Returns created task or None on error."""
        user = self.get_user()
        try:
            task = self._task_service.create_task(
                user_id=user.user_id,
                title=title,
                description=description,
                due_date_time=due_date,
                duration_minutes=duration_minutes,
                priority=priority,
                task_type=task_type,
                goal_id=goal_id,
            )
            self.load_tasks(self._last_date, self._last_search or "")
            return task
        except DatabaseError as e:
            if self._on_error:
                self._on_error(str(e))
            return None

    def update_task(
        self,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        due_date: Optional[datetime] = None,
        duration_minutes: Optional[int] = None,
        priority: Optional[Priority] = None,
        progress_percent: Optional[int] = None,
    ) -> Optional[Task]:
        """Update task and refresh. Returns updated task or None."""
        try:
            task = self._task_service.update_task(
                task_id,
                title=title,
                description=description,
                due_date_time=due_date,
                duration_minutes=duration_minutes,
                priority=priority,
                progress_percent=progress_percent,
            )
            self.load_tasks(self._last_date, self._last_search or "")
            return task
        except DatabaseError as e:
            if self._on_error:
                self._on_error(str(e))
            return None

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Return task by id (for edit dialog)."""
        try:
            return self._task_service.get_by_id(task_id)
        except DatabaseError as e:
            if self._on_error:
                self._on_error(str(e))
            return None

    def get_upcoming_tasks(self, limit: int = 10) -> List[Task]:
        """Return upcoming tasks (next 7 days) for home dashboard."""
        user = self.get_user()
        today = date.today()
        to_date = today + timedelta(days=7)
        try:
            from_dt = datetime(today.year, today.month, today.day)
            to_dt = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59)
            tasks = self._task_service.get_tasks_for_user(
                user_id=user.user_id,
                from_date=from_dt,
                to_date=to_dt,
                include_completed=False,
                search_query=None,
            )
            return tasks[:limit]
        except DatabaseError as e:
            if self._on_error:
                self._on_error(str(e))
            return []

    def get_completion_rate_today(self) -> int:
        """Return completion rate for today (0-100). Tasks due today: completed/total."""
        user = self.get_user()
        today = date.today()
        try:
            from_dt = datetime(today.year, today.month, today.day)
            to_dt = datetime(today.year, today.month, today.day, 23, 59, 59)
            tasks = self._task_service.get_tasks_for_user(
                user_id=user.user_id,
                from_date=from_dt,
                to_date=to_dt,
                include_completed=True,
                search_query=None,
            )
            total = len(tasks)
            if total == 0:
                return 0
            completed = sum(1 for t in tasks if t.is_completed)
            return int(round(100 * completed / total))
        except DatabaseError as e:
            if self._on_error:
                self._on_error(str(e))
            return 0

    def get_active_streaks(self) -> int:
        """Return total active streaks (sum of current_streak for active goals)."""
        user = self.get_user()
        try:
            goals = self._goal_service.get_all_for_user(user.user_id, include_archived=False)
            return sum(g.current_streak for g in goals)
        except DatabaseError as e:
            if self._on_error:
                self._on_error(str(e))
            return 0
