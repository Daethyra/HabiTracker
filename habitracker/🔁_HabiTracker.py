import streamlit as st
import datetime
import sqlite3
import logging

from utils import HabiTracker, DatabaseError

# Configure the app
st.set_page_config(
    page_title="HabiTrack: Visualize Your Usage", page_icon="🔁"
)
st.title(":orange[HabiTrack]")


# Instantiate the HabitTracker class
tracker = HabiTracker()

# Initialize the database
tracker.initialize_database()

# Create the necessary tables
tracker.create_necessary_tables()

db_conn = create_and_connect_db() # Returns 
if not db_conn:
    logging.error("Failed to create or connect to the database.")
    st.error("Failed to create or connect to the database.")
    st.stop()

# Input box for the habit name
habit_name = st.text_input("Enter the name of the habit you want to track:")

# Button to record the habit
if st.button("Record"):
    try:
        tracker.record_habit_entry(habit_name)
    except DatabaseError as e:
        st.error(f"Habit name already exists: {e}")

# Query the database for specific habits within the last four weeks

# Display the results in a heatmap

# Button to create new habit
if st.button("Create New Habit"):
    try:
        tracker.create_habit(habit_name)
    except DatabaseError as e:
        st.error(f"Habit name already exists: {e}")