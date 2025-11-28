from typing import Any

from amadeus import Client
from langchain_community.agent_toolkits.amadeus.toolkit import AmadeusToolkit
from langchain_community.agent_toolkits.amadeus import toolkit as amadeus_module


for attr in dir(amadeus_module):
    obj = getattr(amadeus_module, attr)
    if hasattr(obj, "model_rebuild"):
        try:
            obj.model_rebuild()
        except:
            pass


def get_amadeus_tools():
    """Return a list of tools provided by the Amadeus toolkit."""
    toolkit = AmadeusToolkit()
    return toolkit.get_tools()
