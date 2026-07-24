from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from langchain_google_genai import ChatGoogleGenerativeAI

from app.ai.graph import build_agent_graph
from app.ai.tools import (
    make_check_user_exists_tool,
    get_current_date,
    search_documents,
)
from app.database.session import get_db
from app.models.requests import AskRequest
from app.models.responses import AskResponse
from app.services.assistant_service import AssistantService


router = APIRouter()


def get_assistant_service(
    db: Session = Depends(get_db),
) -> AssistantService:

    model = ChatGoogleGenerativeAI(
        model="gemini-flash-latest"
    )

    tools = [
        make_check_user_exists_tool(db),
        get_current_date,
        search_documents,
    ]

    model_with_tools = model.bind_tools(tools)

    tools_by_name = {
        tool.name: tool
        for tool in tools
    }

    graph = build_agent_graph(
        model_with_tools,
        tools_by_name,
    )

    return AssistantService(graph)

@router.post("/assistant/ask", response_model=AskResponse)
def ask_assistant(request: AskRequest, assistant_service: AssistantService = Depends(get_assistant_service)):
    answer = assistant_service.ask(request.question)
    return AskResponse(answer=answer)
