"""Task domain model."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from models.enums import Priority, TaskType, TaskStatus
from models.recurrence_rule import RecurrenceRule


@dataclass
class Task:
    """
    Task entity (core unit of work).

    Attributes:
        task_id: Unique identifier.
        goal_id: Optional linked goal id.
        user_id: Owner user id.
        title: Task title.
        description: Optional description.
        due_date_time: When the task is due.
        duration_minutes: Estimated duration.
        priority: Priority level.
        recurrence: Optional recurrence rule.
        is_completed: Whether the task is completed.
        completed_at: When it was completed (if any).
        type: Task type (free, goal, assignment, etc.).
        status: Lifecycle status (upcoming, in_progress, completed, etc.).
        progress_percent: 0-100 for UI progress bar.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
    """

    task_id: str
    user_id: str
    title: str
    description: str = ""
    due_date_time: Optional[datetime] = None
    duration_minutes: int = 0
    priority: Priority = Priority.MEDIUM
    recurrence: Optional[RecurrenceRule] = None
    is_completed: bool = False
    completed_at: Optional[datetime] = None
    type: TaskType = TaskType.FREE
    goal_id: Optional[str] = None
    status: TaskStatus = TaskStatus.CREATED
    progress_percent: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        now = datetime.now()
        if self.created_at is None:
            self.created_at = now
        if self.updated_at is None:
            self.updated_at = now

    def complete(self) -> None:
        """Mark the task as completed and set completed_at."""
        self.is_completed = True
        self.completed_at = datetime.now()
        self.status = TaskStatus.COMPLETED
        self.progress_percent = 100
        self.updated_at = datetime.now()

    def snooze(self, until: datetime) -> None:
        """Snooze the task until the given time."""
        self.status = TaskStatus.SNOOZED
        self.due_date_time = until
        self.updated_at = datetime.now()

    def generate_next_instance(self) -> Optional["Task"]:
        """Generate the next instance for recurring tasks. Returns None if not recurring."""
        if not self.recurrence or not self.recurrence.should_repeat(
            self.due_date_time or datetime.now()
        ):
            return None
        next_dt = self.recurrence.get_next_occurrence(
            self.due_date_time or datetime.now()
        )
        if not next_dt:
            return None
        # Create a copy with new id and due date (simplified; id would come from repo)
        return Task(
            task_id="",  # Repository assigns new id
            user_id=self.user_id,
            goal_id=self.goal_id,
            title=self.title,
            description=self.description,
            due_date_time=next_dt,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            recurrence=self.recurrence,
            type=self.type,
        )
