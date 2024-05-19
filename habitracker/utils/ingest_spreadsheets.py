import os
import pandas as pd
from datetime import datetime, timedelta
from openpyxl import load_workbook

from utilities import HabiTracker, DatabaseError

def ingest_xlsx_files(directory: str, db_name: str = "habitrack.db"):
    # Initialize the HabiTracker instance
    tracker = HabiTracker(db_name)
    tracker.initialize_database()
    tracker.create_necessary_tables()

    # List all xlsx files in the specified directory
    xlsx_files = [f for f in os.listdir(directory) if f.endswith('.xlsx')]

    for file in xlsx_files:
        file_path = os.path.join(directory, file)
        workbook = load_workbook(filename=file_path)
        sheet = workbook.active

        # Iterate through rows 2 to 31
        for row in range(2, 32):
            day = sheet[f'A{row}'].value
            if day is None:
                continue

            # Extract columns B-E and calculate the total
            total_entries = sum(
                sheet[f'{col}{row}'].value or 0 for col in ['B', 'C', 'D', 'E']
            )

            # Insert entries into the database
            for _ in range(total_entries):
                tracker.record_habit_entry("smoke weed")

    # Close the database connection
    tracker.close_connection()

if __name__ == "__main__":
    ingest_xlsx_files(".")