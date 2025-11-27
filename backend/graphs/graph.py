from typing import Any

from langgraph.graph import StateGraph

from backend.agents.trip_planner_agent import TripPlannerAgent
from backend.graphs.state import TripState


def create_graph(llm: Any):
    """Create a LangGraph graph for trip planning with multiple nodes.

    For now this is a minimal single-agent node, but the structure
    is ready for additional tools/agents (pricing, routes, etc.).
    """

    async def planner_node(state: TripState) -> TripState:
        agent = TripPlannerAgent(llm)
        query = state.get("query", "")
        result = await agent.plan_trip(query, context=state)
        return {**state, "result": result}

    graph = StateGraph(TripState)
    graph.add_node("planner", planner_node)
    graph.set_entry_point("planner")
    graph.set_finish_point("planner")

    compiled = graph.compile()
    return compiled
