class UserAlreadyExistsException(Exception):
    """Exception raised when a user already exists."""

    def __init__(self, message: str = "User already exists"):
        super().__init__(message)

class InvalidCredentialsException(Exception):
    """Exception raised when the provided credentials are invalid."""
    
    def __init__(self, message: str = "Invalid username or password"):
        super().__init__(message)
    
class InvalidTokenException(Exception):
    """Exception raised when a token is invalid or expired."""

    def __init__(self, message: str = "Invalid or expired token"):
        super().__init__(message)