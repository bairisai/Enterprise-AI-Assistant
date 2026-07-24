from unittest.mock import Mock
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from app.ai.graph import build_agent_graph, make_call_model_node, should_continue, make_run_tools_node
from langgraph.graph import END

def test_call_model_node_returns_model_response():
    mock_model = Mock()

    model_response = AIMessage(content="Hello from Gemini")
    mock_model.invoke.return_value = model_response

    call_model = make_call_model_node(mock_model)

    state = {
        "messages" : [
            HumanMessage(content="Hi")
        ]
    }
    result = call_model(state)

    mock_model.invoke.assert_called_once_with(state["messages"])

    assert result["messages"][0] is model_response

    assert result == {
        "messages" : [model_response]
    }



def test_should_continue_returns_run_tools_when_tool_calls_exist():
    state = {
        "messages": [
            AIMessage(
                content="I'll use a tool.",
                tool_calls=[
                    {
                        "name": "get_current_date",
                        "args": {},
                        "id": "tool-call-1",
                    }
                ],
            )
        ]
    }

    result = should_continue(state)

    assert result == "run_tools"

def test_should_continue_returns_end_when_no_tool_calls_exist():
    state = {
        "messages" : [
            AIMessage(
                content="No tools needed."
            )
        ]
    }
    result = should_continue(state)

    assert result == END


def test_run_tools_node_executes_requested_tool():
    mock_tool = Mock()

    tool_result = ToolMessage(
        content="Today's date is 2026-07-24",
        tool_call_id="tool-call-1",
    )

    mock_tool.invoke.return_value = tool_result

    tools_by_name = {
        "get_current_date": mock_tool
    }

    run_tools = make_run_tools_node(tools_by_name)

    tool_call = {
        "name": "get_current_date",
        "args": {},
        "id": "tool-call-1",
    }

    state = {
        "messages": [
            AIMessage(
                content="",
                tool_calls=[tool_call],
            )
        ]
    }

    result = run_tools(state)

    called_tool_call = mock_tool.invoke.call_args.args[0]

    assert called_tool_call["name"] == "get_current_date"
    assert called_tool_call["args"] == {}
    assert called_tool_call["id"] == "tool-call-1"

    assert result == {
        "messages": [tool_result]
    }
def test_run_tools_node_executes_multiple_tools():
    first_tool = Mock()
    second_tool = Mock()

    first_result = ToolMessage(
        content="first",
        tool_call_id="tool-1",
    )

    second_result = ToolMessage(
        content="second",
        tool_call_id="tool-2",
    )

    first_tool.invoke.return_value = first_result
    second_tool.invoke.return_value = second_result

    tools = {
        "tool_one": first_tool,
        "tool_two": second_tool,
    }

    run_tools = make_run_tools_node(tools)

    first_call = {
        "name": "tool_one",
        "args": {},
        "id": "tool-1",
    }

    second_call = {
        "name": "tool_two",
        "args": {},
        "id": "tool-2",
    }

    state = {
        "messages": [
            AIMessage(
                content="",
                tool_calls=[
                    first_call,
                    second_call,
                ],
            )
        ]
    }

    result = run_tools(state)

    first_called = first_tool.invoke.call_args.args[0]
    second_called = second_tool.invoke.call_args.args[0]

    assert first_called["name"] == "tool_one"
    assert second_called["name"] == "tool_two"

    assert result == {
        "messages": [
            first_result,
            second_result,
        ]
    }

def test_build_agent_graph_returns_compiled_graph():
    mock_model = Mock()

    model_response = AIMessage(content="Finished")
    model_response.tool_calls = []

    mock_model.invoke.return_value = model_response

    graph = build_agent_graph(
        model_with_tools=mock_model,
        tools_by_name={},
    )

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content="Hello")
            ]
        }
    )

    mock_model.invoke.assert_called_once()

    assert result["messages"][-1].content == "Finished"