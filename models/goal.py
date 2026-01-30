"""Goal domain model."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from models.enums import GoalCategory, FrequencyType


@dataclass
class Goal:
    """
    Goal entity containing tasks and tracking streaks.

    Attributes:
        goal_id: Unique identifier.
        user_id: Owner user id.
        title: Goal title.
        description: Optional description.
        category: Goal category.
        color_hex: Hex color for UI (e.g. #4CAF50).
        frequency: How often the goal should be completed.
        created_at: Creation timestamp.
        is_archived: Whether the goal is archived.
        current_streak: Current streak count.
        longest_streak: Longest streak count.
    """

    goal_id: str
    user_id: str
    title: str
    description: str = ""
    category: GoalCategory = GoalCategory.OTHER
    color_hex: str = "#4CAF50"
    frequency: FrequencyType = FrequencyType.DAILY
    created_at: datetime = None
    is_archived: bool = False
    current_streak: int = 0
    longest_streak: int = 0

    def __post_init__(self) -> None:
        if self.created_at is None:
            self.created_at = datetime.now()

    def archive(self) -> None:
        """Mark the goal as archived."""
        self.is_archived = True

    def update_streak(self, new_current: int, new_longest: Optional[int] = None) -> None:
        """Update streak counts."""
        self.current_streak = new_current
        if new_longest is not None and new_longest > self.longest_streak:
            self.longest_streak = new_longest

    def calculate_completion_rate(self, completed: int, scheduled: int) -> float:
        """Calculate completion rate (0.0 to 1.0). Returns 0 if scheduled is 0."""
        if scheduled <= 0:
            return 0.0
        return min(1.0, completed / scheduled)
