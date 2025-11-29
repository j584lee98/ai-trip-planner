import streamlit as st

from backend.core.llm import create_llm
from backend.config.runtime import invoke_graph


st.set_page_config(
    page_title="AI Trip Planner",
    page_icon="✈️"
)

if "llm" not in st.session_state:
    st.session_state["llm"] = create_llm(
        st.secrets["MODEL_NAME"],
        st.secrets["OPENAI_API_KEY"]
    )

st.session_state["generated"] = False

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
        extra = st.text_area("Additional Information", placeholder="Preferred airlines, hotels, etc.")
        
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
download_json = col2.button("Download JSON", use_container_width=True, disabled=True)
download_pdf = col3.button("Download PDF", use_container_width=True, disabled=True)

if generate:
    if st.session_state.get("details"):
        with st.spinner("Planning your trip..."):
            res = invoke_graph(
                st.session_state["llm"],
                st.session_state["details"]
            )
            if res.get("node") == "validator":
                st.error(res.get("message", "Trip details validation failed. Please check your inputs."))
            else:
                st.write(res.get("message", "Trip plan generated successfully!"))
    else:
        st.error("Please update trip details in the sidebar before generating a plan.")
