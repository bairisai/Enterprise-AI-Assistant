from fastapi import APIRouter
from app.config import APPLICATION_NAME, APPLICATION_VERSION

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "application": APPLICATION_NAME, "application_version": APPLICATION_VERSION}