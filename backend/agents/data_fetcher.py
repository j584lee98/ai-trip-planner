from typing import Any, Dict

from langchain.agents import create_agent

from backend.tools.amadeus import get_amadeus_tools


def fetch_data(state: Dict[str, Any], llm: Any) -> Dict[str, Any]:
    """Plan a trip or answer travel questions via Amadeus tools."""

    system_prompt = (
        "You are a travel assistant that uses Amadeus tools to "
        "answer questions about airports, flights, and itineraries. "
        "Be concise and base answers on tool results when possible."
    )

    agent = create_agent(
        llm,
        get_amadeus_tools(),
        system_prompt=system_prompt
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
    state["message"] = result["messages"][-1].content

    return state
