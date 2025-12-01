"""Amadeus API tools for flight and travel data."""

from langchain_community.agent_toolkits.amadeus import toolkit as amadeus_module
from langchain_community.agent_toolkits.amadeus.toolkit import AmadeusToolkit

# Rebuild Pydantic models to avoid validation issues
for _attr in dir(amadeus_module):
    _obj = getattr(amadeus_module, _attr)
    if hasattr(_obj, "model_rebuild"):
        try:
            _obj.model_rebuild()
        except Exception:
            pass


def get_amadeus_tools():
    """Return a list of tools provided by the Amadeus toolkit."""
    toolkit = AmadeusToolkit()
    return toolkit.get_tools()
