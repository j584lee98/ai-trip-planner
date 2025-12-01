from typing import Any, Dict, Optional


class State(Dict[str, Any]):
    """Simple state container for trip planning graph."""
    origin: str
    destination: str
    count: int
    start: str
    end: str
    budget: float
    extra: Optional[str]

    node: str
    message: str
    is_valid: bool
    itinerary: Optional[Dict[str, Any]]
    costs: Optional[Dict[str, Any]]
