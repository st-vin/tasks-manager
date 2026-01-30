"""User service (use cases for User)."""

from typing import Optional

from repository import UserRepository
from repository.database import DatabaseError
from models import User


class UserService:
    """Use cases for User: get or create default user."""

    def __init__(self, user_repo: Optional[UserRepository] = None) -> None:
        self._repo = user_repo or UserRepository()

    def get_or_create_default_user(self) -> User:
        """
        Return the default user; create one if none exists.

        Returns:
            Default user (single-user app).

        Raises:
            DatabaseError: If repository fails.
        """
        default_id = "default_user"
        user = self._repo.get_by_id(default_id)
        if user is not None:
            return user
        user = User(
            user_id=default_id,
            name="User",
            email="user@local",
            is_student_mode=False,
        )
        self._repo.save(user)
        return user
