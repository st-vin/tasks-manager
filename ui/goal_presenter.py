"""Goal presenter: connects Goals UI to GoalService."""

from typing import Callable, List, Optional

from models import Goal, User
from models.enums import GoalCategory, FrequencyType
from services import GoalService, UserService
from repository.database import DatabaseError


class GoalPresenter:
    """Presenter for Goals screen: list active/archived, create, archive."""

    def __init__(
        self,
        goal_service: Optional[GoalService] = None,
        user_service: Optional[UserService] = None,
    ) -> None:
        self._goal_service = goal_service or GoalService()
        self._user_service = user_service or UserService()
        self._user: Optional[User] = None
        self._refresh_view: Optional[Callable[[List[Goal]], None]] = None
        self._on_error: Optional[Callable[[str], None]] = None
        self._show_active = True  # Active tab vs Archived

    def set_refresh_view(self, callback: Callable[[List[Goal]], None]) -> None:
        self._refresh_view = callback

    def set_on_error(self, callback: Callable[[str], None]) -> None:
        self._on_error = callback

    def get_user(self) -> User:
        if self._user is None:
            self._user = self._user_service.get_or_create_default_user()
        return self._user

    def load_goals(self, active_only: bool = True) -> None:
        """Load goals and refresh view. active_only=True = active only; False = archived only."""
        self._show_active = active_only
        user = self.get_user()
        try:
            goals = self._goal_service.get_all_for_user(
                user.user_id,
                include_archived=True,
            )
            if active_only:
                goals = [g for g in goals if not g.is_archived]
            else:
                goals = [g for g in goals if g.is_archived]
            if self._refresh_view:
                self._refresh_view(goals)
        except DatabaseError as e:
            if self._on_error:
                self._on_error(str(e))

    def get_active_goals_count(self) -> int:
        """Count of active (non-archived) goals."""
        user = self.get_user()
        try:
            goals = self._goal_service.get_all_for_user(user.user_id, include_archived=False)
            return len(goals)
        except DatabaseError:
            return 0

    def get_total_streaks(self) -> int:
        """Sum of current_streak across active goals."""
        user = self.get_user()
        try:
            goals = self._goal_service.get_all_for_user(user.user_id, include_archived=False)
            return sum(g.current_streak for g in goals)
        except DatabaseError:
            return 0

    def create_goal(
        self,
        title: str,
        description: str = "",
        color_hex: str = "#4CAF50",
        category: GoalCategory = GoalCategory.OTHER,
        frequency: FrequencyType = FrequencyType.DAILY,
    ) -> Optional[Goal]:
        """Create goal and refresh list."""
        import uuid
        user = self.get_user()
        goal = Goal(
            goal_id=str(uuid.uuid4()),
            user_id=user.user_id,
            title=title,
            description=description,
            color_hex=color_hex,
            category=category,
            frequency=frequency,
        )
        try:
            self._goal_service.save_goal(goal)
            self.load_goals(self._show_active)
            return goal
        except DatabaseError as e:
            if self._on_error:
                self._on_error(str(e))
            return None

    def archive_goal(self, goal_id: str) -> None:
        goal = self._goal_service.get_by_id(goal_id)
        if goal:
            goal.archive()
            try:
                self._goal_service.save_goal(goal)
                self.load_goals(self._show_active)
            except DatabaseError as e:
                if self._on_error:
                    self._on_error(str(e))

    def delete_goal(self, goal_id: str) -> None:
        try:
            self._goal_service.delete_goal(goal_id)
            self.load_goals(self._show_active)
        except DatabaseError as e:
            if self._on_error:
                self._on_error(str(e))
