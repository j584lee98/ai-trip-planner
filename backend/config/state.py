"""State schema for the trip planning graph."""

from typing import Any, Dict, Optional


MAX_BUDGET_RETRIES = 3


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
    travel_data: Optional[str]
    itinerary: Optional[Dict[str, Any]]
    costs: Optional[Dict[str, Any]]
    retry_count: int
