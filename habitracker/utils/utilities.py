import logging
import sqlite3
from datetime import datetime
from typing import Optional

import streamlit as st

# Set up logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s"
)


class DatabaseError(Exception):
    """Custom exception for database-related errors."""

    pass


class HabiTracker:
    def __init__(self, db_name: str = "habitrack.db"):
        self.db_name = db_name
        self.conn = None

    def initialize_database(self) -> None:
        """
        Initializes the SQLite database.

        Creates a new database if it doesn't exist, or connects to an existing one.
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            logging.info(f"Connected to existing database: {self.db_name}")
        except sqlite3.Error as e:
            raise DatabaseError(f"Error connecting to database: {e}") from e

    def create_necessary_tables(self) -> None:
        """
        Creates the necessary tables in the database. This should be run once after initializing the database.

        This method creates the 'habits' and 'habit_entries' tables if they don't already exist.
        """
        if not self.conn:
            raise DatabaseError("Database connection not established")

        try:
            # Create the habits table
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS habits (
                    habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_name TEXT UNIQUE NOT NULL,
                    habit_description TEXT
                )
                """
            )
            logging.info("Successfully checked 'habits' table exists")

            # Create the habit_entries table
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS habit_entries (
                    entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER NOT NULL,
                    entry_timestamp TIMESTAMP NOT NULL,
                    FOREIGN KEY (habit_id) REFERENCES habits(habit_id)
                )
                """
            )
            logging.info("Successfully checked 'habit_entries' table exists")
        except sqlite3.Error as e:
            raise DatabaseError(f"Error creating tables: {e}") from e

    def create_habit(
        self, habit_name: str, habit_description: Optional[str] = None
    ) -> None:
        """
        Create a new habit in the database.

        Args:
            habit_name (str): The name of the habit to create.
            habit_description (Optional[str]): An optional description of the habit.

        Raises:
            DatabaseError: If an error occurs while creating the habit.
            ValueError: If the habit_name is an empty string or contains only whitespace characters.

        Example:
            tracker = HabitTracker()
            tracker.initialize_database()
            tracker.create_necessary_tables()
            tracker.create_habit("Smoking", "A bad habit")
        """
        if not self.conn:
            raise DatabaseError("Database connection not established")

        # Check if the habit_name is valid
        if not habit_name or habit_name.isspace():
            raise ValueError(
                "Habit name cannot be empty or contain only whitespace characters"
            )

        try:
            self.conn.execute(
                "INSERT INTO habits (habit_name, habit_description) VALUES (?, ?)",
                (habit_name.strip(), habit_description),
            )
            self.conn.commit()
            logging.info(f"Successfully created habit: {habit_name}")
        except sqlite3.IntegrityError as e:
            # Handle the case where the habit already exists
            if "UNIQUE constraint failed: habits.habit_name" in str(e):
                logging.info(f"Habit '{habit_name}' already exists")
            else:
                raise DatabaseError(f"Error creating habit: {e}") from e
        except sqlite3.Error as e:
            raise DatabaseError(f"Error creating habit: {e}") from e

    def record_habit_entry(self, habit_name: str) -> None:
        """
        Record a new habit entry in the database.

        Args:
            habit_name (str): The name of the habit to record.

        Raises:
            DatabaseError: If an error occurs while recording the habit entry.

        Example:
            tracker = HabitTracker()
            tracker.initialize_database()
            tracker.create_necessary_tables()
            tracker.create_habit("Smoking", "A bad habit")
            tracker.record_habit_entry("Smoking")
        """
        if not self.conn:
            raise DatabaseError("Database connection not established")

        try:
            with self.conn:
                # Get the habit_id for the given habit_name
                habit_id = self.conn.execute(
                    "SELECT habit_id FROM habits WHERE habit_name = ?",
                    (habit_name,)
                ).fetchone()[0]

                # Insert a new entry into the habit_entries table
                self.conn.execute(
                    "INSERT INTO habit_entries (habit_id, entry_timestamp) VALUES (?, ?)",
                    (habit_id, datetime.now())
                )
            logging.info(f"Successfully recorded entry for habit: {habit_name}")
        except sqlite3.Error as e:
            raise DatabaseError(f"Error recording habit entry: {e}") from e


# Display the past 4 weeks in a markdown table
def display_habit_history(conn: sqlite3.Connection, habit_name: str) -> None:
    """
    Display the past 4 weeks of habit entries in a markdown table.

    Args:
        conn (sqlite3.Connection): The database connection object.
        habit_name (str): The name of the habit to display entries for.

    Raises:
        DatabaseError: If an error occurs while querying the database.
    """
    if not conn:
        conn = sqlite3.connect(self.db_name)

    try:
        st.markdown("<h3>Habits in the last four weeks:</h3>", unsafe_allow_html=True)
        st.markdown("| Habit Name | Last Entry |", unsafe_allow_html=True)
        for row in query_result:
            st.markdown(
                f"| {row[0]} | {row[1].strftime('%Y-%m-%d %H:%M:%S')} |",
                unsafe_allow_html=True,
            )
    except Exception as e:
        st.error(f"Error querying database: {e}")
