from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
load_dotenv()


@tool
def get_current_date() -> str:
    """Returns today's date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")


# @tool
# def calculate_percentage(value: float, percentage: float) -> float:
#     """Calculates what a given percentage of a value is. For example, 15 percent of 200."""
#     return (percentage / 100) * value


model = ChatGoogleGenerativeAI(model="gemini-flash-latest")
tools = [get_current_date]  # , calculate_percentage]
model_with_tools = model.bind_tools(tools)
tools_by_name = {t.name: t for t in tools}

def run_with_tools(question: str) -> str:
    messages = [HumanMessage(question)]

    ai_response = model_with_tools.invoke(messages)
    messages.append(ai_response)

    if not ai_response.tool_calls:
        # No tool needed — the first response IS the final answer
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

print(run_with_tools("What is 37.6842 percent of 9384.17?"))