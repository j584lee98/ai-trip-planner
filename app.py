import streamlit as st

from backend.core.llm import create_llm
from backend.graphs.runtime import run_trip_planner_sync


st.title("AI Trip Planner")

if "llm" not in st.session_state:
    st.session_state["llm"] = create_llm(
        st.secrets["MODEL_NAME"],
        st.secrets["OPENAI_API_KEY"]
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    llm = st.session_state["llm"]
    response_text = run_trip_planner_sync(llm, prompt)

    with st.chat_message("assistant"):
        st.markdown(response_text)

    st.session_state.messages.append({"role": "assistant", "content": response_text})
