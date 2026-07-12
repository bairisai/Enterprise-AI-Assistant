from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def make_call_model_node(model_with_tools):
    def call_model(state: AgentState) -> dict:
        response = model_with_tools.invoke(state["messages"])
        return {"messages": [response]}
    return call_model

def make_run_tools_node(tools_by_name: dict[str, BaseTool]):
    def run_tools(state: AgentState) -> dict:
        last_message = state["messages"][-1]
        tool_results = []
        for tool_call in last_message.tool_calls:
            selected_tool = tools_by_name[tool_call["name"]]
            result = selected_tool.invoke(tool_call)
            tool_results.append(result)
        return {"messages": tool_results}
    return run_tools

def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "run_tools"
    return END

def build_agent_graph(model_with_tools, tools_by_name):
    graph = StateGraph(AgentState)
    graph.add_node("call_model", make_call_model_node(model_with_tools))
    graph.add_node("run_tools", make_run_tools_node(tools_by_name))

    graph.set_entry_point("call_model")

    graph.add_conditional_edges("call_model", should_continue, {"run_tools": "run_tools", END: END})

    graph.add_edge("run_tools", "call_model")

    return graph.compile()