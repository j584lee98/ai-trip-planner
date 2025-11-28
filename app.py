import streamlit as st

from backend.core.llm import create_llm
from backend.config.runtime import run_trip_planner_sync


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
        start = st.date_input("Start (Date)")
        end = st.date_input("End (Date)")
        budget = st.number_input("Budget (USD)", step=1)
        update = st.form_submit_button("Update")

    if update:
        st.session_state["details"] = {
            "origin": origin,
            "destination": destination,
            "start": str(start),
            "end": str(end),
            "budget": budget,
        }
        st.toast("Trip preferences saved", icon="✅")

col1, col2, col3 = st.columns(3, gap="medium")
generate = col1.button("Generate", use_container_width=True, type="primary")
download_json = col2.button("Download JSON", use_container_width=True, disabled=True)
download_pdf = col3.button("Download PDF", use_container_width=True, disabled=True)
