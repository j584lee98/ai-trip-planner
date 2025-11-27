from typing import Any

from backend.graphs.trip_graph import create_trip_graph
from backend.graphs.state import TripState


def run_trip_planner_sync(llm: Any, query: str, extra_state: dict | None = None) -> str:
    """Convenience sync wrapper for Streamlit.

    Takes a user query and optional extra state, runs the compiled
    trip-planning graph, and returns the assistant's textual result.
    """

    graph = create_trip_graph(llm)
    state: TripState = {"query": query}
    if extra_state:
        state.update(extra_state)

    result_state = graph.invoke(state)
    return str(result_state.get("result", ""))
