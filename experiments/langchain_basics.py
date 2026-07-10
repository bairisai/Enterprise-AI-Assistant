from dotenv import load_dotenv
load_dotenv()
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from datetime import datetime
from langchain_core.messages import HumanMessage

@tool
def get_current_date() -> str:
    """Returns today's date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")

def extract_text(response) -> str:
    """Extracts text from the model's response."""
    if isinstance(response.content, str):
        return response.content
    return "".join(
        part.get("text", "") for part in response.content if isinstance(part, dict)
    )
# prompt = ChatPromptTemplate.from_template(
#     "You are a helpful assistant. Answer the following question: {question}"
# )

model = ChatGoogleGenerativeAI(model = "gemini-flash-latest")

# output_parser = StrOutputParser()

# chain = prompt | model | output_parser

# result = chain.invoke({"question": "name three prime numbers greater than 20?"})

# print(get_current_date.name)
# print(get_current_date.description)

model_with_tools = model.bind_tools([get_current_date])

tools_by_name = {"get_current_date": get_current_date}

messages = [HumanMessage("What is today's date?")]

ai_response = model_with_tools.invoke(messages)
messages.append(ai_response)

for tool_call in ai_response.tool_calls:
    selected_tool = tools_by_name[tool_call["name"]]
    tool_result = selected_tool.invoke(tool_call)
    messages.append(tool_result)
final_response = model_with_tools.invoke(messages)
print(extract_text(final_response))