from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.requests import RegisterRequest
from app.models.responses import RegisterResponse
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService

router = APIRouter()


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    repository = UserRepository(db)
    return AuthService(repository)
@router.post("/register", response_model=RegisterResponse)
def register(request: RegisterRequest, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.register_user(request)