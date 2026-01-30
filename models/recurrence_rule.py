"""Recurrence rule for recurring tasks."""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from models.enums import RecurrenceType, DayOfWeek


@dataclass
class RecurrenceRule:
    """
    Rule defining when a recurring task repeats.

    Attributes:
        type: Recurrence pattern (daily, weekly, etc.).
        interval: Interval (e.g. every 2 weeks).
        days_of_week: For weekly, which days (0=Mon, 6=Sun).
        end_date: Optional end date for recurrence.
        max_occurrences: Optional max number of occurrences.
    """

    type: RecurrenceType
    interval: int = 1
    days_of_week: Optional[List[DayOfWeek]] = None
    end_date: Optional[datetime] = None
    max_occurrences: Optional[int] = None

    def get_next_occurrence(self, from_dt: datetime) -> Optional[datetime]:
        """Compute next occurrence after from_dt. Simplified implementation."""
        if self.end_date and from_dt >= self.end_date:
            return None
        # Placeholder: full logic would depend on type/interval/days_of_week
        return from_dt

    def should_repeat(self, current_dt: datetime) -> bool:
        """Return True if recurrence should continue after current_dt."""
        if self.end_date and current_dt >= self.end_date:
            return False
        if self.max_occurrences is not None and self.max_occurrences <= 0:
            return False
        return True
