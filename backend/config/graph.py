"""LangGraph workflow definition for trip planning."""

from typing import Any

from langgraph.graph import END, START, StateGraph

from backend.agents.details_validator import validate_trip_details
from backend.agents.data_fetcher import fetch_data
from backend.agents.itinerary_planner import plan_itinerary
from backend.agents.cost_estimator import estimate_costs
from backend.agents.response_generator import generate_response
from backend.config.state import State, MAX_BUDGET_RETRIES


def create_graph(llm: Any):
    """Create a LangGraph graph for trip planning with multiple nodes."""

    def details_validator(state: State) -> State:
        state["node"] = "details_validator"
        state["retry_count"] = 0
        return validate_trip_details(state, llm)

    def details_validator_router(state: State) -> str:
        """Route to data_fetcher if valid, otherwise end the graph."""
        if state.get("is_valid"):
            return "data_fetcher"
        return END

    def data_fetcher_node(state: State) -> State:
        state["node"] = "data_fetcher"
        return fetch_data(state, llm)

    def itinerary_planner_node(state: State) -> State:
        state["node"] = "itinerary_planner"
        return plan_itinerary(state, llm)

    def cost_estimator_node(state: State) -> State:
        state["node"] = "cost_estimator"
        return estimate_costs(state, llm)

    def cost_estimator_router(state: State) -> str:
        """Route back to itinerary_planner if over budget and retries remain."""
        costs = state.get("costs", {})
        retry_count = state.get("retry_count", 0)
        
        if costs.get("within_budget", True):
            return "response_generator"
        
        if retry_count < MAX_BUDGET_RETRIES:
            state["retry_count"] = retry_count + 1
            return "itinerary_planner"
        
        return "response_generator"

    def response_generator_node(state: State) -> State:
        state["node"] = "response_generator"
        return generate_response(state, llm)

    graph = StateGraph(State)

    graph.add_node("details_validator", details_validator)
    graph.add_node("data_fetcher", data_fetcher_node)
    graph.add_node("itinerary_planner", itinerary_planner_node)
    graph.add_node("cost_estimator", cost_estimator_node)
    graph.add_node("response_generator", response_generator_node)

    graph.add_edge(START, "details_validator")
    graph.add_conditional_edges("details_validator", details_validator_router)
    graph.add_edge("data_fetcher", "itinerary_planner")
    graph.add_edge("itinerary_planner", "cost_estimator")
    graph.add_conditional_edges("cost_estimator", cost_estimator_router)
    graph.add_edge("response_generator", END)

    compiled = graph.compile()
    return compiled
