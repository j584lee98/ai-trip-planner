from typing import Any

from langgraph.graph import StateGraph, START, END

from backend.agents.validator import validate_trip_details
from backend.agents.data_fetcher import fetch_data
from backend.config.state import State


def create_graph(llm: Any):
    """Create a LangGraph graph for trip planning with multiple nodes.

    For now this is a minimal single-agent node, but the structure
    is ready for additional tools/agents (pricing, routes, etc.).
    """

    def validator(state: State) -> State:
        state["node"] = "validator"
        return validate_trip_details(state, llm)

    def validator_router(state: State) -> str:
        """Route to data_fetcher if valid, otherwise end the graph."""
        if state.get("is_valid"):
            return "data_fetcher"
        return END

    def data_fetcher_node(state: State) -> State:
        state["node"] = "data_fetcher"
        return fetch_data(state, llm)

    graph = StateGraph(State)

    graph.add_node("validator", validator)
    graph.add_node("data_fetcher", data_fetcher_node)

    graph.add_edge(START, "validator")
    graph.add_conditional_edges("validator", validator_router)
    graph.add_edge("data_fetcher", END)

    compiled = graph.compile()
    return compiled
