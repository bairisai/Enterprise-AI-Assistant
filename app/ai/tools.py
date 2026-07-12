from datetime import datetime

from langchain_core.tools import tool
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository

def make_check_user_exists_tool(db: Session):
    """Factory function to create a tool that checks if a user exists in the database."""
    @tool
    def check_user_exists(username: str) -> str:
        """Checks whether a user with the given username exists in the system,
        and returns their username and email if found."""
        repository = UserRepository(db)
        user = repository.get_user_by_username(username)
        if user is None:
            return f"No user found with username '{username}'."
        return f"User found: username={user.username}, email={user.email}"
    return check_user_exists

@tool
def get_current_date() -> str:
    """Returns today's date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")