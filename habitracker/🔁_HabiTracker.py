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
st.toast("Initializing database...")

# Initialize the database
try:
    tracker.initialize_database()
    st.toast("Database connection initialized!")
except Exception as e:
    # Directly print result
    st.error(f"{e}")

# Create the necessary tables
try:
    tracker.create_necessary_tables()
except Exception as e:
    st.error(f"Failed to create necessary tables: {e}")

# Check if the database connection was successful
if not tracker.conn:
    logging.error("Failed to create or connect to the database.")
    st.error("Failed to create or connect to the database.")
    st.stop()

# Input box for the habit name
habit_name = st.text_input("Enter the name of the habit you want to track:")
# Optional input box for habit description
habit_description = st.text_input("Optionally, describe the habit:")

# Button to RECORD the habit
if st.button("Record"):
    try:
        tracker.record_habit_entry(habit_name)
    except DatabaseError as e:
        st.error(f"Habit name already exists: {e}")

# Button to CREATE new habit
if st.sidebar.button(
    label="Create New Habit",
    key="new_habit_button",
    help="Create a new habit in the database.",
    ):
    try:
        tracker.create_habit(habit_name)
    except DatabaseError as e:
        st.error(f"Habit name already exists: {e}")

# Query the database for specific habits within the last four weeks

# Display the results in a heatmap

###
st.divider()

# Optional input box for habit description
habit_description = st.text_input("Optionally, describe the habit:")

# Button to CREATE new habit
if st.button("Create New Habit"):
    try:
        tracker.create_habit(habit_name)
    except DatabaseError as e:
        st.error(f"Habit name already exists: {e}")