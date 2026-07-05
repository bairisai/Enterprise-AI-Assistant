
from app.exceptions.auth_exceptions import UserAlreadyExistsException
from app.models.requests import RegisterRequest
from app.models.responses import RegisterResponse
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register_user(self, request: RegisterRequest) -> RegisterResponse:
        if self.repository.username_exists(request.username):
            raise UserAlreadyExistsException()

        self.repository.create_user(username=request.username)
        return RegisterResponse(message="Registration service called successfully")