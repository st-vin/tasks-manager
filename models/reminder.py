"""Reminder domain model."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from models.enums import ReminderType


@dataclass
class Reminder:
    """
    Reminder for a task.

    Attributes:
        reminder_id: Unique identifier.
        task_id: Associated task id.
        reminder_time: When to fire.
        minutes_before: Minutes before task due time (alternative).
        is_sent: Whether the reminder was already sent.
        type: Reminder channel (push, email, in_app).
    """

    reminder_id: str
    task_id: str
    reminder_time: datetime
    minutes_before: int = 0
    is_sent: bool = False
    type: ReminderType = ReminderType.IN_APP

    def schedule(self) -> None:
        """Schedule the reminder (delegates to scheduler in service layer)."""
        pass  # No-op in model; service layer handles scheduling

    def cancel(self) -> None:
        """Mark as cancelled / unschedule."""
        self.is_sent = True  # or a dedicated cancelled flag
