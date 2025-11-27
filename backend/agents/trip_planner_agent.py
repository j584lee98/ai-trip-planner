from typing import Any, Dict

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.agents.output_parsers import ReActJsonSingleInputOutputParser
from langchain.tools.render import render_text_description_and_args
from langchain_community.agent_toolkits.amadeus.toolkit import AmadeusToolkit
from langchain_core.prompts import ChatPromptTemplate


class TripPlannerAgent:
    """Trip planner that uses the Amadeus Toolkit under the hood.

    This wraps an AgentExecutor configured with Amadeus tools so that
    higher-level graph code can just call `plan_trip` with a natural
    language query.
    """

    def __init__(self, llm: Any):
        self.llm = llm
        self._agent_executor = self._build_agent_executor()

    def _build_agent_executor(self) -> AgentExecutor:
        """Create an agent powered by Amadeus tools.

        Assumes the following env vars are set (see Amadeus docs):
        - AMADEUS_CLIENT_ID
        - AMADEUS_CLIENT_SECRET
        Optionally:
        - AMADEUS_HOSTNAME ("test" or "production")
        """

        toolkit = AmadeusToolkit(llm=self.llm)
        tools = toolkit.get_tools()

        system_prompt = (
            "You are a travel assistant that uses Amadeus tools to "
            "answer questions about airports, flights, and itineraries. "
            "Be concise and base answers on tool results when possible."
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        agent = create_tool_calling_agent(
            self.llm,
            tools,
            prompt,
            tools_renderer=render_text_description_and_args,
            output_parser=ReActJsonSingleInputOutputParser(),
        )

        return AgentExecutor(agent=agent, tools=tools, verbose=False)

    async def plan_trip(self, query: str, context: Dict[str, Any] | None = None) -> str:
        """Plan a trip or answer travel questions via Amadeus tools."""

        payload: Dict[str, Any] = {"input": query}
        if context:
            payload["context"] = context

        result = await self._agent_executor.ainvoke(payload)
        return str(result.get("output", ""))
