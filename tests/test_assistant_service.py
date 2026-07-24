from unittest.mock import Mock

from langchain_core.messages import AIMessage, HumanMessage

from app.services.assistant_service import AssistantService


def test_ask_returns_generated_response():
    fake_graph = Mock()
    fake_graph.invoke.return_value = {
        "messages": [
            AIMessage(content="Hello from Gemini")
        ]
    }

    service = AssistantService(fake_graph)

    answer = service.ask("Hello")

    assert answer == "Hello from Gemini"

    fake_graph.invoke.assert_called_once()

    args, _ = fake_graph.invoke.call_args
    state = args[0]

    assert "messages" in state
    assert len(state["messages"]) == 1

    message = state["messages"][0]

    assert isinstance(message, HumanMessage)
    assert message.content == "Hello"


def test_extract_text_returns_string_content():
    response = AIMessage(content="Simple response")

    result = AssistantService.extract_text(response)

    assert result == "Simple response"


def test_extract_text_joins_multimodal_text_parts():
    response = AIMessage(
        content=[
            {"text": "Hello "},
            {"text": "World"},
            {"type": "image"},
            {"text": "!"},
        ]
    )

    result = AssistantService.extract_text(response)

    assert result == "Hello World!"