import logging
import sqlite3
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
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
    df["entry_timestamp"] = pd.to_datetime(df["entry_timestamp"])
    df["date"] = df["entry_timestamp"].dt.date

    # Filter data for the last 6 weeks
    end_date = datetime.now().date()
    start_date = end_date - timedelta(weeks=6)
    df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

    # Generate a complete date range
    all_dates = pd.date_range(start=start_date, end=end_date).date
    all_dates_df = pd.DataFrame(all_dates, columns=["date"])

    # Group by date and count occurrences
    heatmap_data = df.groupby("date").size().reset_index(name="count")

    # Merge with the complete date range to fill missing dates with zero counts
    heatmap_data = all_dates_df.merge(heatmap_data, on="date", how="left").fillna(0)

    # Pivot the data to create a matrix suitable for a heatmap
    heatmap_data = heatmap_data.pivot_table(
        index="date", values="count", aggfunc="sum"
    ).fillna(0)

    # Create a calendar heatmap
    fig, ax = plt.subplots(figsize=(10, 6))

    if visualize_option == "Specific Habit" and habit_to_visualize == "smoke weed":
        # Custom color scale for "smoke weed"
        cmap = sns.color_palette(
            ["#9fc5e8", "#93c47d", "#f44336", "#990a00"], as_cmap=True
        )
        bounds = [0, 1, 2, 5, 6]
        norm = plt.Normalize(vmin=0, vmax=6)
    else:
        # Custom color scale for the main heatmap
        cmap = sns.color_palette(
            ["#9fc5e8", "#93c47d", "#f44336", "#990a00"], as_cmap=True
        )
        bounds = [0, 5, 10, 15, 20]
        norm = plt.Normalize(vmin=0, vmax=20)

    sns.heatmap(
        heatmap_data.T, cmap=cmap, norm=norm, cbar=True, ax=ax, annot=True, fmt="g"
    )
    ax.set_title(
        f"Heatmap for {habit_to_visualize if visualize_option == 'Specific Habit' else 'All Habits'}"
    )
    st.pyplot(fig)
else:
    st.write("No data to visualize.")