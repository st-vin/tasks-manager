"""User domain model."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class NotificationPreferences:
    """User notification preferences."""

    enabled: bool = True
    sound: Optional[str] = None
    quiet_hours_start: Optional[int] = None  # hour 0-23
    quiet_hours_end: Optional[int] = None
    default_reminder_minutes: int = 15


@dataclass
class User:
    """
    User entity owning goals and tasks.

    Attributes:
        user_id: Unique identifier.
        name: Display name.
        email: Email address.
        is_student_mode: Whether student-specific features are enabled.
        preferences: Notification and UI preferences.
        created_at: Creation timestamp.
    """

    user_id: str
    name: str
    email: str
    is_student_mode: bool = False
    preferences: NotificationPreferences = field(default_factory=NotificationPreferences)
    created_at: datetime = field(default_factory=datetime.now)

    def toggle_student_mode(self) -> None:
        """Toggle student mode on/off."""
        self.is_student_mode = not self.is_student_mode

    def update_preferences(self, **kwargs: Any) -> None:
        """Update notification preferences with given keyword arguments."""
        for key, value in kwargs.items():
            if hasattr(self.preferences, key):
                setattr(self.preferences, key, value)
