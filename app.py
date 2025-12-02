"""Streamlit application for AI Trip Planner."""

import json

import streamlit as st

from backend.config.runtime import stream_graph, NODE_DESCRIPTIONS
from backend.core.llm import create_llm


MAX_TRIP_DAYS = 14

st.set_page_config(
    page_title="AI Trip Planner",
    page_icon="✈️"
)

if "llm" not in st.session_state:
    st.session_state["llm"] = create_llm(
        st.secrets["MODEL_NAME"],
        st.secrets["OPENAI_API_KEY"]
    )

st.title("AI Trip Planner")

st.text(f"Powered by {st.secrets['MODEL_NAME']}")

with st.sidebar:
    st.header("Trip Details")
    with st.form("trip_form"):
        origin = st.text_input("Origin", placeholder="e.g., New York")
        destination = st.text_input("Destination", placeholder="e.g., London")
        count = st.number_input("Travelers", min_value=1, max_value=10, step=1, format="%d")
        start = st.date_input("Start Date")
        end = st.date_input("End Date")
        budget = st.number_input("Budget (USD)", min_value=100, step=100, format="%d")
        extra = st.text_area("Preferences", placeholder="e.g., no layovers, boutique hotels, outdoor activities...")
        
        update = st.form_submit_button("Save Trip Details", use_container_width=True)

    if update:
        if origin and destination and count and start and end and budget:
            trip_duration = (end - start).days
            if end < start:
                st.toast("End date cannot be before start date", icon="⚠️")
            elif trip_duration > MAX_TRIP_DAYS:
                st.toast(f"Trip cannot exceed {MAX_TRIP_DAYS} days", icon="⚠️")
            elif origin.lower() == destination.lower():
                st.toast("Origin and destination must be different", icon="⚠️")
            else:
                st.session_state["details"] = {
                    "origin": origin,
                    "destination": destination,
                    "count": count,
                    "start": str(start),
                    "end": str(end),
                    "budget": budget,
                    "extra": extra
                }
                st.session_state["result"] = None
                st.toast("Trip details saved!", icon="✅")
        else:
            st.toast("Please fill in all required fields", icon="⚠️")


col1, col2, col3 = st.columns(3, gap="medium")
has_details = st.session_state.get("details") is not None
generate = col1.button("Generate Plan", use_container_width=True, type="primary", disabled=not has_details)

result = st.session_state.get("result")
itinerary_data = result.get("itinerary") if result else None
costs_data = result.get("costs") if result else None

col2.download_button(
    label="📥 Itinerary",
    data=json.dumps(itinerary_data, indent=2) if itinerary_data else "",
    file_name="trip_itinerary.json",
    mime="application/json",
    use_container_width=True,
    disabled=not itinerary_data
)

col3.download_button(
    label="📥 Cost Breakdown",
    data=json.dumps(costs_data, indent=2) if costs_data else "",
    file_name="cost_breakdown.json",
    mime="application/json",
    use_container_width=True,
    disabled=not costs_data
)

if generate:
    if st.session_state.get("details"):
        status_container = st.status("Planning your trip...", expanded=True)
        res = None
        
        with status_container:
            for node_name, node_output in stream_graph(
                st.session_state["llm"],
                st.session_state["details"]
            ):
                description = NODE_DESCRIPTIONS.get(node_name, f"Processing {node_name}...")
                st.write(description)
                res = node_output
        
        if res:
            st.session_state["result"] = res
            status_container.update(label="Trip planning complete!", state="complete", expanded=False)
            st.rerun()
    else:
        st.error("Please update trip details in the sidebar before generating a plan.")

# Display stored result if available
if st.session_state.get("result") and not generate:
    res = st.session_state["result"]
    if res.get("node") == "details_validator":
        st.error(res.get("message", "Trip details validation failed. Please check your inputs."))
    else:
        st.markdown(res.get("message", ""))
