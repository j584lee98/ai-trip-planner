from typing import Any

from langgraph.graph import StateGraph

from backend.agents.trip_planner import plan_trip
from backend.graphs.state import State


def create_graph(llm: Any):
    """Create a LangGraph graph for trip planning with multiple nodes.

    For now this is a minimal single-agent node, but the structure
    is ready for additional tools/agents (pricing, routes, etc.).
    """

    def planner_node(state: State) -> State:
        messages = state.get("messages", [])
        result = plan_trip(llm, query=messages[-1].content if messages else "", context=state)
        state["messages"].append({"role": "assistant", "content": result})
        return state

    graph = StateGraph(State)
    graph.add_node("planner", planner_node)
    graph.set_entry_point("planner")
    graph.set_finish_point("planner")

    compiled = graph.compile()
    return compiled
