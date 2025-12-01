"""Data fetcher agent for travel information."""

from typing import Any, Dict

from langchain.agents import create_agent

from backend.tools.amadeus import get_amadeus_tools


SYSTEM_PROMPT = """You are a travel assistant that uses Amadeus tools to 
find information about airports, flights, hotels, and activities.
Be concise and base answers on tool results when possible."""


def fetch_data(state: Dict[str, Any], llm: Any) -> Dict[str, Any]:
    """Fetch travel data using Amadeus tools."""
    agent = create_agent(
        llm,
        get_amadeus_tools(),
        system_prompt=SYSTEM_PROMPT
    )

    query = f"""These are the trip details provided so far:
    Origin: {state.get("origin", "N/A")}
    Destination: {state.get("destination", "N/A")}
    Number of Travelers: {state.get("count", "N/A")}
    Start Date: {state.get("start", "N/A")}
    End Date: {state.get("end", "N/A")}
    Budget (USD): ${state.get("budget", "N/A")}
    Additional Notes: {state.get("extra", "None")}

    Based on these details, provide multiple options for
    flights, accommodation, and activities.
    """

    result = agent.invoke(
        {"messages": [{"role": "user", "content": query}]}
    )
    state["travel_data"] = result["messages"][-1].content

    return state
