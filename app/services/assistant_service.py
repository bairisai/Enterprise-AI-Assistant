from langchain_google_genai import ChatGoogleGenerativeAI
from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage

from app.ai.tools import make_check_user_exists_tool, get_current_date, search_documents
from app.ai.graph import build_agent_graph


class AssistantService:
    def __init__(self, db: Session):
        model = ChatGoogleGenerativeAI(model="gemini-flash-latest")
        tools = [make_check_user_exists_tool(db), get_current_date, search_documents]
        model_with_tools = model.bind_tools(tools)
        tools_by_name = {t.name: t for t in tools}

        self.graph = build_agent_graph(model_with_tools, tools_by_name)
    def ask(self, question: str) -> str:
        result = self.graph.invoke({"messages": [HumanMessage(question)]})
        final_message = result["messages"][-1]
        return self.extract_text(final_message)

        
    @staticmethod
    def extract_text(response) -> str:
        if isinstance(response.content, str):
            return response.content
        return "".join(
            part.get("text", "") for part in response.content if isinstance(part, dict)
        )