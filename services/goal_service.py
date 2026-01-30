"""Goal service (use cases for Goal)."""

from typing import List, Optional

from repository import GoalRepository
from repository.database import DatabaseError
from models import Goal


class GoalService:
    """Use cases for Goal: CRUD and list by user."""

    def __init__(self, goal_repo: Optional[GoalRepository] = None) -> None:
        self._repo = goal_repo or GoalRepository()

    def get_by_id(self, goal_id: str) -> Optional[Goal]:
        """Return goal by id or None."""
        try:
            return self._repo.get_by_id(goal_id)
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"get_by_id failed: {e}") from e

    def get_all_for_user(self, user_id: str, include_archived: bool = False) -> List[Goal]:
        """Return all goals for user."""
        try:
            return self._repo.get_all_by_user(user_id, include_archived=include_archived)
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"get_all_for_user failed: {e}") from e

    def save_goal(self, goal: Goal) -> None:
        """Create or update goal."""
        try:
            self._repo.save(goal)
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"save_goal failed: {e}") from e

    def delete_goal(self, goal_id: str) -> None:
        """Delete goal by id."""
        try:
            self._repo.delete(goal_id)
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"delete_goal failed: {e}") from e
