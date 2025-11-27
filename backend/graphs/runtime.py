from typing import Any

from backend.graphs.graph import create_graph
from backend.graphs.state import State


def run_trip_planner_sync(llm: Any, query: str, extra_state: dict | None = None) -> str:
    """Convenience sync wrapper for Streamlit.

    Takes a user query and optional extra state, runs the compiled
    trip-planning graph, and returns the assistant's textual result.
    """

    import asyncio

    graph = create_graph(llm)
    state: State = {"query": query}
    if extra_state:
        state.update(extra_state)

    # The compiled graph exposes an async ``ainvoke`` API; since Streamlit
    # expects a synchronous call path here, we run it to completion using
    # ``asyncio.run`` and then pull the text result out of the final state.
    result_state: State = asyncio.run(graph.ainvoke(state))
    return str(result_state.get("result", ""))
