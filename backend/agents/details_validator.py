"""Trip details validation agent."""

from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel, Field


MAX_TRIP_DURATION_DAYS = 14


class Validation(BaseModel):
    """Structured output for trip details validation."""
    is_valid: bool = Field(description="Whether the trip details are valid")
    message: str = Field(description="Reasons for invalid fields, if any")


def validate_trip_details(state: Dict[str, Any], llm: Any) -> Dict[str, Any]:
    """Validate trip details using an LLM with structured output."""
    
    # Pre-check trip duration before LLM call
    try:
        start_date = datetime.strptime(state.get("start", ""), "%Y-%m-%d")
        end_date = datetime.strptime(state.get("end", ""), "%Y-%m-%d")
        trip_duration = (end_date - start_date).days
        
        if trip_duration > MAX_TRIP_DURATION_DAYS:
            state["is_valid"] = False
            state["message"] = f"Trip duration exceeds the maximum allowed limit of {MAX_TRIP_DURATION_DAYS} days. Please shorten your trip to 2 weeks or less."
            return state
    except ValueError:
        pass  # Let LLM handle invalid date formats
    
    prompt = f"""You are a trip details validator. Review the following trip details and check for any issues.
    Trip Details:
    - Origin: {state.get("origin", "N/A")}
    - Destination: {state.get("destination", "N/A")}
    - Number of Travelers: {state.get("count", "N/A")}
    - Start Date: {state.get("start", "N/A")}
    - End Date: {state.get("end", "N/A")}
    - Budget (USD): ${state.get("budget", "N/A")}
    - Additional Notes: {state.get("extra", "None")}

    Please validate the following:
    1. Dates are in valid YYYY-MM-DD format
    2. End date is on or after start date
    3. Start date is not in the past (today is {datetime.now().strftime("%Y-%m-%d")})
    4. Trip duration does not exceed {MAX_TRIP_DURATION_DAYS} days (2 weeks)
    5. Origin and destination are different valid locations
    6. Number of travelers is reasonable (1-10)
    7. Budget is realistic for the trip duration and number of travelers

    Return your validation result as structured output."""
    
    structured_llm = llm.with_structured_output(Validation)
    validation: Validation = structured_llm.invoke(prompt)
    
    state.update(validation.model_dump())
    
    return state
