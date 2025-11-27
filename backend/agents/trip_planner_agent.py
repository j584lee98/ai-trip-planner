from typing import Any, Dict


class TripPlannerAgent:
    """High-level agent responsible for orchestrating trip planning logic."""

    def __init__(self, llm: Any):
        self.llm = llm

    async def plan_trip(self, query: str, context: Dict[str, Any] | None = None) -> str:
        # Placeholder for more complex multi-step reasoning
        prompt = f"You are a helpful AI trip planner. User request: {query}"
        return await self.llm.ainvoke(prompt)
