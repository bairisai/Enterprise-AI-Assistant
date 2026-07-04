class UserAlreadyExistsException(Exception):
    """Exception raised when a user already exists."""

    def __init__(self, message: str = "User already exists"):
        super().__init__(message)