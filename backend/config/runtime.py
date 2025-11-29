from typing import Any

from backend.config.graph import create_graph
from backend.config.state import State


def invoke_graph(llm: Any, state: State) -> dict:
    """Convenience sync wrapper for Streamlit.

    Takes a user query and optional extra state, runs the compiled
    trip-planning graph, and returns the assistant's textual result.
    """

    graph = create_graph(llm)

    result: State = graph.invoke(state)
    return result
