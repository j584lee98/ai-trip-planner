"""Itinerary planner agent."""

from typing import Any, Dict

from pydantic import BaseModel, Field


class Activity(BaseModel):
    """A single activity in the itinerary."""
    time: str = Field(description="Start time of the activity (e.g., '09:00')")
    name: str = Field(description="Name of the activity")
    location: str = Field(description="Location of the activity")
    duration: str = Field(description="Duration of the activity (e.g., '2 hours')")
    cost: float = Field(description="Estimated cost in USD")
    notes: str = Field(default="", description="Additional notes")


class DayPlan(BaseModel):
    """Plan for a single day."""
    date: str = Field(description="Date in YYYY-MM-DD format")
    activities: list[Activity] = Field(description="List of activities for the day")


class Flight(BaseModel):
    """Flight information."""
    departure_time: str = Field(description="Departure time")
    arrival_time: str = Field(description="Arrival time")
    airline: str = Field(description="Airline name")
    flight_number: str = Field(description="Flight number")
    origin: str = Field(description="Origin airport code")
    destination: str = Field(description="Destination airport code")
    cost_per_person: float = Field(description="Cost per person in USD")


class Hotel(BaseModel):
    """Hotel information."""
    name: str = Field(description="Hotel name")
    address: str = Field(description="Hotel address")
    check_in: str = Field(description="Check-in date")
    check_out: str = Field(description="Check-out date")
    cost_per_night: float = Field(description="Cost per night in USD")
    amenities: list[str] = Field(default_factory=list, description="List of amenities")


class Itinerary(BaseModel):
    """Complete trip itinerary."""
    outbound_flight: Flight = Field(description="Outbound flight details")
    return_flight: Flight = Field(description="Return flight details")
    hotel: Hotel = Field(description="Hotel details")
    daily_plans: list[DayPlan] = Field(description="Day-by-day itinerary")


SYSTEM_PROMPT = """You are an expert travel itinerary planner. Based on the trip details and 
available travel data, create a detailed day-by-day itinerary.

Your itinerary should include:
- Outbound and return flight details with times and costs
- Hotel accommodation with check-in/check-out dates and nightly rates
- Daily activities with specific times, locations, durations, and estimated costs
- Consider the traveler's budget and preferences from additional notes

Make the itinerary realistic and well-paced, allowing for travel time between activities.
Include a mix of popular attractions and local experiences."""

REVISION_PROMPT = """The previous itinerary exceeded the budget. Please create a MORE BUDGET-FRIENDLY 
itinerary by:
- Choosing cheaper flight options (economy class, budget airlines, flexible dates)
- Selecting more affordable accommodations (3-star hotels, hostels, vacation rentals)
- Reducing expensive activities or replacing with free/low-cost alternatives
- Focusing on essential experiences within the budget constraint

Previous cost breakdown showed:
{previous_costs}

You MUST keep the total cost under ${budget}."""


def plan_itinerary(state: Dict[str, Any], llm: Any) -> Dict[str, Any]:
    """Create a detailed itinerary based on trip details and fetched data."""
    retry_count = state.get("retry_count", 0)
    previous_costs = state.get("costs", {})
    
    base_prompt = f"""{SYSTEM_PROMPT}

Trip Details:
- Origin: {state.get("origin", "N/A")}
- Destination: {state.get("destination", "N/A")}
- Number of Travelers: {state.get("count", "N/A")}
- Start Date: {state.get("start", "N/A")}
- End Date: {state.get("end", "N/A")}
- Budget (USD): ${state.get("budget", "N/A")}
- Additional Notes: {state.get("extra", "None")}

Available Travel Data:
{state.get("message", "No data available")}"""

    if retry_count > 0 and previous_costs:
        revision_context = REVISION_PROMPT.format(
            previous_costs=previous_costs,
            budget=state.get("budget", "N/A")
        )
        prompt = f"{base_prompt}\n\n{revision_context}\n\nCreate a revised, budget-friendly itinerary as structured output."
    else:
        prompt = f"{base_prompt}\n\nCreate a complete itinerary as structured output."

    structured_llm = llm.with_structured_output(Itinerary)
    itinerary: Itinerary = structured_llm.invoke(prompt)

    state["itinerary"] = itinerary.model_dump()

    return state
