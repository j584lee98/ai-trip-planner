from typing import Any, Dict, Optional


class State(Dict[str, Any]):
    """Simple state container for trip planning graph."""
    origin: str
    destination: str
    people: int
    start: str
    end: str
    budget: float
    extra: Optional[str]
