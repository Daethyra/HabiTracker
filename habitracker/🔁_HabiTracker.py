import logging
import sqlite3
from datetime import datetime, timedelta

import calplot
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from matplotlib.colors import ListedColormap
from utils import DatabaseError, HabiTracker

# Configure the app
st.set_page_config(page_title="HabiTrack: Visualize Your Usage", page_icon="🔁")
st.title(":orange[HabiTrack]")
st.subheader("Track Your Usage and Gather Data Over Time")

# Initialize the HabiTracker
tracker = HabiTracker()
tracker.initialize_database()
tracker.create_necessary_tables()

# Add or Select a Habit
habit_names = tracker.get_habits()
habit_names.append("Add New Habit")
selected_habit = st.selectbox("Select a Habit", habit_names)

if selected_habit == "Add New Habit":
    new_habit_name = st.text_input("Enter New Habit Name")
    new_habit_description = st.text_area("Enter Habit Description (Optional)")
    if st.button("Create Habit"):
        tracker.create_habit(new_habit_name, new_habit_description)
else:
    if st.button("Record Event"):
        tracker.record_habit_entry(selected_habit)

# Visualize Data
st.header("Visualize Habit Data")
visualize_option = st.selectbox(
    "Choose Visualization", ["All Habits", "Specific Habit"]
)

if visualize_option == "Specific Habit":
    habit_to_visualize = st.selectbox("Select Habit to Visualize", habit_names[:-1])
    entries = tracker.get_habit_entries(habit_to_visualize)
else:
    entries = tracker.get_habit_entries()

if entries:
    df = pd.DataFrame(entries, columns=["entry_timestamp"])

    # Convert entry_timestamp to datetime, handling any errors gracefully
    df["entry_timestamp"] = pd.to_datetime(df["entry_timestamp"], errors="coerce")
    df["date"] = df["entry_timestamp"].dt.date

    # Drop rows with invalid timestamps
    df.dropna(subset=["entry_timestamp"], inplace=True)

    # Group by date and count occurrences
    heatmap_data = df.groupby("date").size().reset_index(name="count")

    # Ensure the date column is a datetime type and set it as the index
    heatmap_data["date"] = pd.to_datetime(heatmap_data["date"])
    heatmap_data.set_index("date", inplace=True)

    # Create a calendar heatmap using calplot
    if visualize_option == "Specific Habit" and habit_to_visualize == "smoke weed":
        # Custom color scale for "smoke weed"
        cmap = ListedColormap(["#9fc5e8", "#93c47d", "#f44336", "#990a00"])
        vmin, vmax = 0, 6
    else:
        # Custom color scale for the main heatmap
        cmap = ListedColormap(["#9fc5e8", "#93c47d", "#f44336", "#990a00"])
        vmin, vmax = 0, 20

    fig, ax = calplot.calplot(
        heatmap_data["count"],
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        colorbar=True,
        suptitle=f"Heatmap for {habit_to_visualize if visualize_option == 'Specific Habit' else 'All Habits'}",
        figsize=(10, 6),
    )
    st.pyplot(fig)
else:
    st.write("No data to visualize.")
