from langchain_google_genai import ChatGoogleGenerativeAI
from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage

from app.ai.tools import make_check_user_exists_tool


class AssistantService:
    def __init__(self, db: Session):
        self.model = ChatGoogleGenerativeAI(model="gemini-flash-latest")
        self.tools = [make_check_user_exists_tool(db)]  # , calculate_percentage]
        self.model_with_tools = self.model.bind_tools(self.tools)
        self.tools_by_name = {t.name: t for t in self.tools}
    def ask(self, question: str) -> str:
        messages = [HumanMessage(question)]
        ai_response = self.model_with_tools.invoke(messages)
        messages.append(ai_response)

        if not ai_response.tool_calls:
            # No tool needed — the first response IS the final answer
            return self.extract_text(ai_response)

        for tool_call in ai_response.tool_calls:
            selected_tool = self.tools_by_name[tool_call["name"]]
            tool_result = selected_tool.invoke(tool_call)
            messages.append(tool_result)

        final_response = self.model_with_tools.invoke(messages)
        return self.extract_text(final_response)
    @staticmethod
    def extract_text(response) -> str:
        if isinstance(response.content, str):
            return response.content
        return "".join(
            part.get("text", "") for part in response.content if isinstance(part, dict)
        )