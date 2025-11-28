from typing import Any, Dict

from langchain.agents import create_agent

from backend.tools.amadeus import get_amadeus_tools


def _build_agent(llm: Any):
    """Create a tool-calling agent powered by Amadeus tools."""

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

    return agent


def plan_trip(llm: Any, query: str, context: Dict[str, Any] | None = None) -> str:
    """Plan a trip or answer travel questions via Amadeus tools."""

    agent = _build_agent(llm)

    payload: Dict[str, Any] = {"input": query}
    if context:
        payload["context"] = context

    result = agent.invoke(
        {"messages": [{"role": "user", "content": query}]}
    )

    messages = result.get("messages", [])
    return messages[-1].content
