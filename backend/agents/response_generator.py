"""Response generator agent."""

from typing import Any, Dict

from backend.config.state import MAX_BUDGET_RETRIES


SYSTEM_PROMPT = """You are a travel content writer. Generate a beautifully formatted markdown 
response presenting the complete trip plan to the user.

Your response should be:
- Well-organized with clear sections and headers
- Easy to read with bullet points and tables where appropriate
- Engaging and informative
- Include all relevant details from the itinerary and cost breakdown

Structure your response with these sections:
1. Trip Overview (destination, dates, travelers)
2. Flight Details (outbound and return with times and costs)
3. Accommodation (hotel details with amenities)
4. Day-by-Day Itinerary (each day with activities, times, and costs)
5. Cost Summary (breakdown table and total)
6. Budget Status (whether within budget, tips if over)
7. Travel Tips (destination-specific advice)

Use markdown formatting:
- Headers (##, ###)
- Tables for costs and schedules
- Bullet points for lists
- Bold for emphasis
- Emojis for visual appeal (✈️, 🏨, 🎯, 💰, etc.)"""


def generate_response(state: Dict[str, Any], llm: Any) -> Dict[str, Any]:
    """Generate a formatted markdown response from the itinerary and costs."""
    costs = state.get("costs", {})
    retry_count = state.get("retry_count", 0)
    within_budget = costs.get("within_budget", True)
    
    budget_note = ""
    if not within_budget and retry_count >= MAX_BUDGET_RETRIES:
        budget_note = f"""
NOTE: After {MAX_BUDGET_RETRIES} attempts, the itinerary still exceeds the budget.
Include a clear section explaining this and provide actionable suggestions for the user
to either increase their budget or make further compromises."""

    prompt = f"""{SYSTEM_PROMPT}
{budget_note}

Trip Details:
- Origin: {state.get("origin", "N/A")}
- Destination: {state.get("destination", "N/A")}
- Number of Travelers: {state.get("count", "N/A")}
- Start Date: {state.get("start", "N/A")}
- End Date: {state.get("end", "N/A")}
- Budget (USD): ${state.get("budget", "N/A")}
- Additional Notes: {state.get("extra", "None")}

Itinerary:
{state.get("itinerary", {})}

Cost Breakdown:
{costs}

Generate a complete, beautifully formatted markdown response."""

    response = llm.invoke(prompt)
    state["message"] = response.content

    return state
