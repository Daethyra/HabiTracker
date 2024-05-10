import streamlit as st
import datetime
import sqlite3
import logging

from utils import create_and_connect_db, record_habit

st.set_page_config(
    page_title="HabiTrack: Visualize Your Usage", page_icon="🔁"
)

st.title(":orange[HabiTrack]")

# Create the database connection
db_conn = create_and_connect_db()
if not db_conn:
    logging.error("Failed to create or connect to the database.")
    st.error("Failed to create or connect to the database.")
    st.stop()

# Input box for the habit name
habit_name = st.text_input("Enter the name of the habit you want to track:")

# Button to record the habit
if st.button("Record"):
    record_habit(db_conn, habit_name)
    st.success(f"Recorded habit: {habit_name}")

# Define the database cursor

# Query the database for specific habits within the last four weeks

# Display the results in a heatmap