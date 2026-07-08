from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.entities.user import User
from app.models.requests import LoginRequest, RegisterRequest
from app.models.responses import RegisterResponse, TokenResponse
from app.repositories.user_repository import UserRepository
from app.security.auth_dependency import get_current_user
from app.services.auth_service import AuthService

router = APIRouter()


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    repository = UserRepository(db)
    return AuthService(repository)
@router.post("/register", response_model=RegisterResponse)
def register(request: RegisterRequest, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.register_user(request)

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.login_user(request)

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "username": current_user.username, 
        "email": current_user.email
        }