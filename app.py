"""
app.py — Streamlit UI for the Text-to-SQL Assistant (polished version)

Same pipeline as the basic version — this file only changes how it's
presented:
    1. st.chat_message() for a real chat interface (instead of one input box)
    2. st.dataframe() to show results as a proper table
    3. A sidebar listing the database schema, for context during a demo

No pipeline logic lives here. Everything SQL/LLM-related still comes
from src/data_loader.py and src/model_runner.py.

Run with:
    streamlit run app.py
"""

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from src.data_loader import load_config, connect_db, get_schema, get_schema_string
from src.model_runner import text_to_sql_pipeline

# -----------------------------------------------------------
# STEP 1: One-time setup (cached across reruns)
# -----------------------------------------------------------

@st.cache_resource
def get_pipeline_resources():
    load_dotenv()
    client = OpenAI()

    config = load_config()
    conn, cursor = connect_db(config["db_path"])
    schema = get_schema(cursor)
    schema_string = get_schema_string(cursor)

    return client, config, cursor, schema, schema_string


client, config, cursor, schema, schema_string = get_pipeline_resources()

st.set_page_config(page_title="Text-to-SQL Assistant", page_icon="🎵", layout="wide")

# -----------------------------------------------------------
# STEP 2: Sidebar — shows the database schema for context
# -----------------------------------------------------------

with st.sidebar:
    st.header("📋 Database Schema")
    st.caption("Chinook digital music store — 11 tables")
    for table, columns in schema.items():
        with st.expander(table):
            for col_name, col_type in columns:
                st.text(f"{col_name} ({col_type})")

# -----------------------------------------------------------
# STEP 3: Chat history (kept in session_state so it persists
# across reruns within the same browser session)
# -----------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🎵 Chinook Text-to-SQL Assistant")
st.write("Ask a question about the database in plain English.")

# Replay previous turns
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            st.code(msg["sql"], language="sql")
            if isinstance(msg["results"], list):
                st.dataframe(pd.DataFrame(msg["results"]), use_container_width=True)
            else:
                st.write(msg["results"])
        else:
            st.write(msg["content"])

# -----------------------------------------------------------
# STEP 4: Handle a new question
# -----------------------------------------------------------

user_question = st.chat_input("e.g. Which artist has the most albums?")

if user_question:
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.write(user_question)

    with st.chat_message("assistant"):
        with st.spinner("Generating SQL and running query..."):
            result = text_to_sql_pipeline(
                cursor,
                client,
                config["model"],
                schema_string,
                user_question,
                config["max_retries"],
            )

        st.code(result["sql"], language="sql")

        if result["results"] == "BLOCKED: unsafe SQL rejected":
            st.error("This query was blocked by the safety scrubber (not a read-only SELECT).")
        elif result["results"] is None:
            st.error("The query failed and could not be corrected after multiple attempts.")
        else:
            st.dataframe(pd.DataFrame(result["results"]), use_container_width=True)

    st.session_state.messages.append({
        "role": "assistant",
        "sql": result["sql"],
        "results": result["results"],
    })
