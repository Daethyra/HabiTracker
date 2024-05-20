import logging
from datetime import datetime
from typing import List, Optional

import streamlit as st
from sqlalchemy.exc import IntegrityError

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")


class DatabaseError(Exception):
    """Custom exception for database-related errors."""

    pass


class HabiTracker:
    def __init__(self):
        self.conn = st.connection("habitrack_db", type="sql")

    def create_necessary_tables(self) -> None:
        """
        Creates the necessary tables in the database. This should be run once after initializing the database.

        Raises:
            DatabaseError: If there is an error creating the tables.
        """
        try:
            with self.conn.session as s:
                s.execute(
                    """
                    CREATE TABLE IF NOT EXISTS habits (
                        habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        habit_name TEXT UNIQUE NOT NULL,
                        habit_description TEXT
                    )
                    """
                )
                logging.info("Successfully checked 'habits' table exists")

                s.execute(
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
                s.commit()
        except Exception as e:
            raise DatabaseError(f"Error creating tables: {e}") from e

    def create_habit(
        self, habit_name: str, habit_description: Optional[str] = None
    ) -> None:
        """
        Create a new habit in the database.

        Parameters:
        habit_name (str): The name of the habit.
        habit_description (str, optional): The description of the habit. Defaults to None.

        Returns:
        None
        """
        if not habit_name or habit_name.isspace():
            raise ValueError(
                "Habit name cannot be empty or contain only whitespace characters"
            )

        try:
            with self.conn.session as s:
                s.execute(
                    "INSERT INTO habits (habit_name, habit_description) VALUES (:habit_name, :habit_description)",
                    params={
                        "habit_name": habit_name.strip(),
                        "habit_description": habit_description,
                    },
                )
                s.commit()
                logging.info(f"Successfully created habit: {habit_name}")
                st.success(f"Successfully created habit: {habit_name}")

        except IntegrityError as e:
            if "UNIQUE constraint failed: habits.habit_name" in str(e):
                logging.info(f"Habit '{habit_name}' already exists")
                st.warning(f"Habit '{habit_name}' already exists")
            else:
                raise DatabaseError(f"Error creating habit: {e}") from e
        except Exception as e:
            raise DatabaseError(f"Error creating habit: {e}") from e

    def record_habit_entry(
        self, habit_name: str, entry_timestamp: Optional[datetime] = None
    ) -> None:
        """
        Record a new habit entry in the database.

        Args:
            habit_name (str): The name of the habit.
            entry_timestamp (datetime, optional): The timestamp of the habit entry. Defaults to None.

        Returns:
            None

        Raises:
            DatabaseError: If there is an error recording the habit entry.
        """
        try:
            with self.conn.session as s:
                habit_id = s.execute(
                    "SELECT habit_id FROM habits WHERE habit_name = :habit_name",
                    params={"habit_name": habit_name},
                ).fetchone()[0]

                if entry_timestamp is None:
                    entry_timestamp = datetime.now()

                s.execute(
                    "INSERT INTO habit_entries (habit_id, entry_timestamp) VALUES (:habit_id, :entry_timestamp)",
                    params={"habit_id": habit_id, "entry_timestamp": entry_timestamp},
                )
                s.commit()
                logging.info(f"Successfully recorded entry for habit: {habit_name}")
                st.success(
                    f"Successfully recorded entry for habit: {habit_name.upper()} at ({entry_timestamp})"
                )

        except Exception as e:
            raise DatabaseError(f"Error recording habit entry: {e}") from e

    def get_habits(self) -> List[str]:
        """
        Retrieves the list of habits from the database.

        Returns:
        List[str]: A list of habit names.
        """
        try:
            habits = self.conn.query(
                "SELECT habit_name FROM habits", show_spinner=True
            ).to_dict(orient="records")
            return [habit["habit_name"] for habit in habits]
        except Exception as e:
            raise DatabaseError(f"Error retrieving habits: {e}") from e

    def get_habit_entries(self, habit_name: str = None) -> List[str]:
        """
        Retrieves the habit entries from the database.

        Args:
            habit_name (str, optional): The name of the habit. Defaults to None.

        Returns:
            List[str]: A list of entry timestamps for the habit.

        Raises:
            DatabaseError: If there is an error retrieving the habit entries.
        """
        try:
            if habit_name:
                habit_id = self.conn.query(
                    "SELECT habit_id FROM habits WHERE habit_name = :habit_name",
                    params={"habit_name": habit_name},
                    show_spinner=True,
                ).to_dict(orient="records")[0]["habit_id"]
                entries = self.conn.query(
                    "SELECT entry_timestamp FROM habit_entries WHERE habit_id = :habit_id",
                    params={"habit_id": habit_id},
                    show_spinner=True,
                ).to_dict(orient="records")
            else:
                entries = self.conn.query(
                    "SELECT entry_timestamp FROM habit_entries", show_spinner=True
                ).to_dict(orient="records")
            return [entry["entry_timestamp"] for entry in entries]
        except Exception as e:
            raise DatabaseError(f"Error retrieving habit entries: {e}") from e
