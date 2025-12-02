"""Runtime utilities for invoking the trip planning graph."""

from typing import Any, Generator

from backend.config.graph import create_graph
from backend.config.state import State


# Mapping of node names to user-friendly descriptions
NODE_DESCRIPTIONS = {
    "details_validator": "🔍 Validating trip details...",
    "data_fetcher": "🌐 Fetching flight and hotel data...",
    "itinerary_planner": "📅 Planning your itinerary...",
    "cost_estimator": "💰 Estimating costs...",
    "response_generator": "✍️ Generating your trip plan...",
}


def invoke_graph(llm: Any, state: State) -> dict:
    """Convenience sync wrapper for Streamlit.

    Takes a user query and optional extra state, runs the compiled
    trip-planning graph, and returns the assistant's textual result.
    """

    graph = create_graph(llm)

    result: State = graph.invoke(state)
    return result


def stream_graph(llm: Any, state: State) -> Generator[tuple[str, State], None, None]:
    """Stream graph execution, yielding (node_name, state) for each step.
    
    This allows showing progress updates as each node executes.
    """
    graph = create_graph(llm)
    
    for event in graph.stream(state):
        # event is a dict with node_name as key and output state as value
        for node_name, node_output in event.items():
            yield node_name, node_output
