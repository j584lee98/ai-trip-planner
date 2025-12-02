"""Streamlit application for AI Trip Planner."""

import json

import streamlit as st

from backend.config.runtime import stream_graph, NODE_DESCRIPTIONS
from backend.core.llm import create_llm


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

with st.sidebar:
    st.header("Trip Details")
    with st.form("trip_form"):
        origin = st.text_input("Origin (Location)", placeholder="e.g., New York")
        destination = st.text_input("Destination (Location)", placeholder="e.g., London")
        count = st.number_input("Number of Travelers", min_value=1, max_value=10, step=1, format="%d")
        start = st.date_input("Start (Date)")
        end = st.date_input("End (Date)")
        budget = st.number_input("Budget (USD)", min_value=1, step=1, format="%d")
        extra = st.text_area("Additional Information", placeholder="Preferred airlines/hotels, no layovers, indoor activities only, etc.")
        
        update = st.form_submit_button("Update")

    if update:
        if origin and destination and count and start and end and budget:
            if end >= start:
                st.session_state["details"] = {
                    "origin": origin,
                    "destination": destination,
                    "count": count,
                    "start": str(start),
                    "end": str(end),
                    "budget": budget,
                    "extra": extra
                }
                st.success("Trip preferences saved")
            else:
                st.error("End date cannot be before start date")
        else:
            st.error("Please fill in all trip details")

col1, col2, col3 = st.columns(3, gap="medium")
generate = col1.button("Generate", use_container_width=True, type="primary")

result = st.session_state.get("result")
itinerary_data = result.get("itinerary") if result else None
costs_data = result.get("costs") if result else None

col2.download_button(
    label="Trip Itinerary",
    data=json.dumps(itinerary_data, indent=2) if itinerary_data else "",
    file_name="trip_itinerary.json",
    mime="application/json",
    use_container_width=True,
    disabled=not itinerary_data
)

col3.download_button(
    label="Cost Breakdown",
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
            
            if res.get("node") == "details_validator":
                st.error(res.get("message", "Trip details validation failed. Please check your inputs."))
            else:
                st.markdown(res.get("message", "Trip plan generated successfully!"))
    else:
        st.error("Please update trip details in the sidebar before generating a plan.")

# Display stored result if available
if st.session_state.get("result") and not generate:
    res = st.session_state["result"]
    if res.get("node") == "details_validator":
        st.error(res.get("message", "Trip details validation failed. Please check your inputs."))
    else:
        st.markdown(res.get("message", ""))
