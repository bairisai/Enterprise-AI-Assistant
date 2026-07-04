from fastapi import APIRouter

from app.models.requests import RegisterRequest
from app.models.responses import RegisterResponse
from app.services.auth_service import AuthService

router = APIRouter()
auth_service = AuthService()

@router.post("/register", response_model=RegisterResponse)
def test_register_request(request: RegisterRequest): 
    return auth_service.register_user(request)