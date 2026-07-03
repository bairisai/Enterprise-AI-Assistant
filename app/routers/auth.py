from fastapi import APIRouter

from app.models.requests import RegisterRequest
from app.services.auth_service import AuthService

router = APIRouter()
auth_service = AuthService()

@router.post("/register")
def test_register_request(request: RegisterRequest):
    response = auth_service.register_user()
    return response