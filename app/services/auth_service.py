import bcrypt
from app.entities.user import User
from app.exceptions.auth_exceptions import UserAlreadyExistsException
from app.models.requests import RegisterRequest
from app.models.responses import RegisterResponse
from app.repositories.user_repository import UserRepository




class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register_user(self, request: RegisterRequest) -> RegisterResponse:
        if self.repository.username_exists(request.username):
            raise UserAlreadyExistsException(f"User with username '{request.username}' already exists")

        user = User(
            username=request.username,
            email=request.email,
            hashed_password=self.hash_password(request.password),
        )
        self.repository.create_user(user)
        return RegisterResponse(message="User registered successfully")
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod   
    def verify_password(password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))