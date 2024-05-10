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
st.success("Initializing database...")

# Initialize the database
try:
    tracker.initialize_database()
    st.success("Database connection initialized!")
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

# Create columns to put buttons in
col1, col2, col3 = st.columns(spec=[1, 1, 1])  # three columns with equal width

# Button to RECORD the habit
with col1:
    if st.button("Record", key="record_button", help="Record a habit entry."):
        try:
            tracker.record_habit_entry(habit_name)
        except DatabaseError as e:
            st.error(f"Habit name already exists: {e}")

# Button to CREATE new habit
with col2:
    if st.button("Create New Habit", key="create_habit_button", help="Create a new habit in the database."):
        try:
            tracker.create_habit(habit_name)
        except DatabaseError as e:
            st.error(f"Habit name already exists: {e}")

# Button to SEARCH
if col3.button("Search", key="search_button", help="Search for habits in the last four weeks."):
    try:
        query_result = tracker.conn.execute(
            "SELECT habits.habit_name, habit_entries.entry_timestamp "
            "FROM habits INNER JOIN habit_entries "
            "ON habits.habit_id = habit_entries.habit_id "
            "WHERE habit_entries.entry_timestamp > datetime('now','start of previous 4 weeks') "
            "AND habits.habit_name LIKE '%' || ? || '%'",
            (habit_name,)
        ).fetchall()

        st.markdown("<h3>Habits in the last four weeks:</h3>", unsafe_allow_html=True)
        st.markdown("| Habit Name | Last Entry |", unsafe_allow_html=True)
        for row in query_result:
            st.markdown(
                f"| {row[0]} | {row[1].strftime('%Y-%m-%d %H:%M:%S')} |",
                unsafe_allow_html=True,
            )
    except sqlite3.Error as e:
        st.error(f"Error querying database: {e}")



# Display the results in a heatmap

###
st.divider()

