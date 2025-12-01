"""Cost estimator agent."""

from typing import Any, Dict

from pydantic import BaseModel, Field


class CostBreakdown(BaseModel):
    """Detailed cost breakdown for the trip."""
    flight_total: float = Field(description="Total cost for all flights")
    hotel_total: float = Field(description="Total cost for accommodation")
    activities_total: float = Field(description="Total cost for all activities")
    food_estimate: float = Field(description="Estimated food/dining costs")
    transport_estimate: float = Field(description="Estimated local transportation costs")
    miscellaneous: float = Field(description="Buffer for miscellaneous expenses")
    subtotal: float = Field(description="Subtotal before any adjustments")
    total: float = Field(description="Grand total estimated cost")
    per_person: float = Field(description="Cost per person")
    within_budget: bool = Field(description="Whether the trip is within the specified budget")
    budget_difference: float = Field(description="Difference from budget (positive = under, negative = over)")
    savings_tips: list[str] = Field(default_factory=list, description="Tips to reduce costs if over budget")


SYSTEM_PROMPT = """You are a travel cost estimation expert. Analyze the provided itinerary 
and calculate a comprehensive cost breakdown.

Your cost estimate should include:
- Flight costs (based on itinerary data)
- Hotel costs (based on itinerary data)
- Activity costs (based on itinerary data)
- Food/dining estimate (reasonable daily allowance based on destination)
- Local transportation estimate (taxis, public transit, etc.)
- Miscellaneous buffer (10-15% for unexpected expenses)

Compare the total against the traveler's budget and provide savings tips if over budget."""


def estimate_costs(state: Dict[str, Any], llm: Any) -> Dict[str, Any]:
    """Estimate total trip costs based on the itinerary."""
    itinerary = state.get("itinerary", {})
    
    prompt = f"""{SYSTEM_PROMPT}

Trip Details:
- Number of Travelers: {state.get("count", 1)}
- Budget (USD): ${state.get("budget", "N/A")}

Itinerary:
{itinerary}

Calculate the complete cost breakdown as structured output."""

    structured_llm = llm.with_structured_output(CostBreakdown)
    costs: CostBreakdown = structured_llm.invoke(prompt)

    state["costs"] = costs.model_dump()

    return state
