import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

from app.database.session import SessionLocal
from app.repositories.user_repository import UserRepository

@tool
def check_user_exists(username: str) -> str:
    """Checks whether a user with the given username exists in the system,
    and returns their username and email if found."""
    db = SessionLocal()
    try:
        repository = UserRepository(db)
        user = repository.get_user_by_username(username)
        if user is None:
            return f"No user found with username '{username}'."
        return f"User found: username={user.username}, email={user.email}"
    finally:
        db.close()

model = ChatGoogleGenerativeAI(model="gemini-flash-latest")
tools = [check_user_exists]
model_with_tools = model.bind_tools(tools)
tools_by_name = {t.name: t for t in tools}


def run_with_tools(question: str) -> str:
    messages = [HumanMessage(question)]
    ai_response = model_with_tools.invoke(messages)
    messages.append(ai_response)

    if not ai_response.tool_calls:
        return extract_text(ai_response)

    for tool_call in ai_response.tool_calls:
        selected_tool = tools_by_name[tool_call["name"]]
        tool_result = selected_tool.invoke(tool_call)
        messages.append(tool_result)

    final_response = model_with_tools.invoke(messages)
    return extract_text(final_response)


def extract_text(response) -> str:
    if isinstance(response.content, str):
        return response.content
    return "".join(
        part.get("text", "") for part in response.content if isinstance(part, dict)
    )


print(run_with_tools("Does a user called bairi exist in the system?"))
print(run_with_tools("Is there a user named randomnonexistentuser123?"))