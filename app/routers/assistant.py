
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.requests import AskRequest
from app.models.responses import AskResponse
from app.services.assistant_service import AssistantService


router = APIRouter()

def get_assistant_service(db: Session = Depends(get_db)) -> AssistantService:
    return AssistantService(db)

@router.post("/assistant/ask", response_model=AskResponse)
def ask_assistant(request: AskRequest, assistant_service: AssistantService = Depends(get_assistant_service)):
    answer = assistant_service.ask(request.question)
    return AskResponse(answer=answer)
