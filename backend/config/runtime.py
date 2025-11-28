from typing import Any

from langchain.messages import HumanMessage

from backend.config.graph import create_graph
from backend.config.state import State


def run_trip_planner_sync(llm: Any, query: str, extra_state: dict | None = None) -> str:
    """Convenience sync wrapper for Streamlit.

    Takes a user query and optional extra state, runs the compiled
    trip-planning graph, and returns the assistant's textual result.
    """

    graph = create_graph(llm)
    state: State = {
        "messages": [HumanMessage(content=query)]
    }
    if extra_state:
        state.update(extra_state)
    result: State = graph.invoke(state)
    output = result["messages"][-1].content if "messages" in result and result["messages"] else ""
    return output
