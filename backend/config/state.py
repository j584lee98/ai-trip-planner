from typing import Any, Dict, Annotated
from langgraph.graph.message import add_messages


class State(Dict[str, Any]):
    """Simple state container for trip planning graph."""
    messages: Annotated[list, add_messages]