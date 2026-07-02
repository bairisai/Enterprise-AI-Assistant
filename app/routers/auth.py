from fastapi import APIRouter

from app.models.requests import RegisterRequest

router = APIRouter()

@router.post("/register")
def test_register_request(request: RegisterRequest):
    print(f"Received registration request: {request}")