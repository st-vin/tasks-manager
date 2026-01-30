"""Enumerations for the Task Management domain model."""

from enum import Enum, auto
from typing import Optional


class Priority(str, Enum):
    """Task priority levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskType(str, Enum):
    """Type of task (free, goal-linked, assignment, exam, study session)."""

    FREE = "free"
    GOAL = "goal"
    ASSIGNMENT = "assignment"
    EXAM = "exam"
    STUDY_SESSION = "study_session"


class TaskStatus(str, Enum):
    """Task lifecycle status (aligned with State Diagram)."""

    CREATED = "created"
    SCHEDULED = "scheduled"
    PENDING = "pending"
    UPCOMING = "upcoming"
    TODAY = "today"
    OVERDUE = "overdue"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    SNOOZED = "snoozed"
    REJECTED = "rejected"  # UI synonym for cancelled


class RecurrenceType(str, Enum):
    """Recurrence pattern for recurring tasks."""

    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class DayOfWeek(int, Enum):
    """Day of week (0=Monday, 6=Sunday)."""

    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class ReminderType(str, Enum):
    """Reminder notification type."""

    PUSH = "push"
    EMAIL = "email"
    IN_APP = "in_app"


class GoalCategory(str, Enum):
    """Goal category for grouping."""

    HEALTH = "health"
    WORK = "work"
    LEARNING = "learning"
    PERSONAL = "personal"
    OTHER = "other"


class FrequencyType(str, Enum):
    """Goal frequency (how often to complete)."""

    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
