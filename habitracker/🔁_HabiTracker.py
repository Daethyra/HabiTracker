import streamlit as st
import datetime
import sqlite3
import logging

from utils import HabiTracker, DatabaseError, display_habit_history

# Configure the app
st.set_page_config(page_title="HabiTrack: Visualize Your Usage", page_icon="🔁")
st.title(":orange[HabiTrack]")

# NOTE: https://discuss.streamlit.io/t/hide-button-b-with-button-a-without-clicking-twice/42835/2?u=daethyra
# Hide the setup button after setup is complete #
# Manually boot up database
if "conn" not in st.session_state:

        if st.button("Boot up database"):
            try:
                
                # Instantiate the HabitTracker class
                tracker = HabiTracker()
                
                # Store the connection in the session state
                st.session_state["conn"] = tracker
                
                # Initialize the database
                st.session_state.conn.initialize_database()
                
                # Create the necessary tables
                st.session_state.conn.create_necessary_tables()

                # Set the setup flag to True
                st.session_state.setup_complete = True
                
            except Exception as e:
                st.error(f"Database Operation Failed!: {e}")
    
        else:
            st.stop()

# Input box for the habit name
habit_name = st.text_input("Enter the name of the habit you want to track:")
# Optional input box for habit description
habit_description = st.text_input("Optionally, describe the habit:")

# Create columns to put buttons in
col1, col2, col3 = st.columns(spec=[1, 1, 1])  # three columns with equal width

# Button to RECORD the habit
if col1.button(
        label="Record",
        key="record_button",
        help="Record a habit entry.",
    ):
    try:
        tracker.record_habit_entry(habit_name)
    except Exception as e:
        st.error(f"Failed to record habit entry: {e}")

# Button to CREATE new habit
if col2.button(
        label="Create New Habit",
        key="create_habit_button",
        help="Create a new habit in the database.",
    ):
    try:
        tracker.create_habit(habit_name, habit_description if habit_description else None)
    except Exception as e:
        st.error(f"Failed to create habit: {e}")

# Button to SEARCH
if not col3.button(
    label="Search",
    key="search_button",
    help="Search for habits in the last four weeks.",
):
    st.stop()

###
st.divider()

# Display the past 4 weeks in a markdown table
display_habit_history(tracker.conn, habit_name)

# Display the results in a heatmap


