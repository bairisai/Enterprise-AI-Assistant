
from app.models.responses import RegisterResponse


class AuthService:

    def register_user(self):
        return RegisterResponse(message="Registration service called successfully")