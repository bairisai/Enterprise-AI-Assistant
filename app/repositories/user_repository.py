from app.models.requests import RegisterRequest


class UserRepository:
    def create_user(self, username: str) -> None:
        """Create a new user from the registration request."""
        pass

    def get_user_by_username(self, username: str) -> None:
        """Retrieve a user record by username."""
        pass

    def username_exists(self, username: str) -> bool:
        """Check whether a username already exists."""
        pass