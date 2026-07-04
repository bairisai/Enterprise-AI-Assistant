
from app.exceptions.auth_exceptions import UserAlreadyExistsException
from app.models.requests import RegisterRequest
from app.models.responses import RegisterResponse


class AuthService:

    def register_user(self, request: RegisterRequest) -> RegisterResponse:
        if request.username == "admin":
            raise UserAlreadyExistsException()
        return RegisterResponse(message="Registration service called successfully")