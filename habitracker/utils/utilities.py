import sqlite3
import logging
import datetime
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s")


def create_and_connect_db(db_name: str = "habitrack.db") -> Optional[sqlite3.Connection]:
    """
    Creates a SQLite database and connects to it.

    Args:
        db_name (str): The name of the database file. Defaults to 'habitrack.db'.

    Returns:
        Optional[sqlite3.Connection]: A connection to the database, or None if an error occurs.
    """
    try:
        # Check if the database connection already exists
        with sqlite3.connect(db_name) as conn:
            logging.info(f"Connected to existing database: {db_name}")
            return conn
    except sqlite3.Error as e:
        logging.error(f"Error connecting to database: {e}")

    try:
        # Create the database if it doesn't exist
        with sqlite3.connect(db_name) as conn:
            logging.info(f"Created new database: {db_name}")

            try:
                # Create the habits table
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS habits (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        habit_name TEXT,
                        timestamp TEXT
                    )
                """
                )
                logging.info("Created 'habits' table")
            except sqlite3.Error as e:
                logging.error(f"Error creating 'habits' table: {e}")

            return conn
    except sqlite3.Error as e:
        logging.error(f"Error creating database: {e}")
        return None


# Function to record a habit event
def record_habit(conn: sqlite3.Connection, habit_name: str) -> None:
    """
    Record a habit event in the database.

    Args:
        conn (sqlite3.Connection): The database connection.
        habit_name (str): The name of the habit to record.

    Returns:
        None
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Recording habit: {habit_name}, timestamp: {timestamp}")

    conn.execute(
        "INSERT INTO habits (habit_name, timestamp) VALUES (?, ?)",
        (habit_name, timestamp),
    )
    conn.commit()
    logging.info(f"Successfully recorded habit: {habit_name}, timestamp: {timestamp}")
