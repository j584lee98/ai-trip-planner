from typing import Any, Dict

from amadeus import Client

from langchain.agents import create_agent
from langchain_community.agent_toolkits.amadeus.toolkit import AmadeusToolkit
from langchain_community.agent_toolkits.amadeus import toolkit as amadeus_module

for attr in dir(amadeus_module):
    obj = getattr(amadeus_module, attr)
    if hasattr(obj, "model_rebuild"):
        try:
            obj.model_rebuild()
        except:
            pass


def _build_agent(llm: Any):
    """Create a tool-calling agent powered by Amadeus tools."""

    toolkit = AmadeusToolkit(llm=llm)
    tools = toolkit.get_tools()

    system_prompt = (
        "You are a travel assistant that uses Amadeus tools to "
        "answer questions about airports, flights, and itineraries. "
        "Be concise and base answers on tool results when possible."
    )

    agent = create_agent(
        llm,
        tools,
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
