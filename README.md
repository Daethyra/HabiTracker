# HabiTracker: Track Your Usage and Gather Data Over Time

#### Project Vocabulary
| Word | Definition |
|---------------|--------------------------------------------------------------|
| Habit | A behavior to be recorded. |
| Use (Noun) | A timestamped action. An instance of using something. A partaking. |
| Event | A row in the database table representing a 'Use.' |

## Project Goals
The application must:
- Maintain a database of habit data
  - Habit Names
  - Event Timestamps (Hour, Minute, Second)

The application should have:
- Selectbox or Inputbox for selecting/adding Habits
- Button to record an event
- A centered heat map for visualizing the user's "Records"
- Ability to visualize:
  - All Habits' data
  - A specific Habit's data

### User Interaction Flow:
1. Select or Add a Habit
   - Selectbox: Existing Habit Name
   - Inputbox: New Habit Name (Creates a new habit in the *Habits* table)
2. Click button to 'Record an Event'
   - Adds entry to database, recording the current timestamp

## Database Specifications
**Habits Table**:
- `habit_id` (Primary Key Auto-Increment)
- `habit_name` (e.g., "smoking a half-bowl of weed", "riding a bike for 30 minutes")
- `habit_description` (optional description of the habit)

**HabitEntries Table**:
- `entry_id` (Primary Key Auto-Increment)
- `habit_id` (Foreign Key referencing Habits table)
- `entry_timestamp` (Timestamp of when the entry was recorded, down to the second)

### Example SQL Queries for Database Interactions
- **Count** the number of times a habit has been used in the past day
```SQL
SELECT COUNT(*) AS hit_count
FROM HabitEntries
WHERE habit_id = (
    SELECT habit_id
    FROM Habits
    WHERE habit_name = 'Smoke a Bowl'
) AND entry_timestamp BETWEEN '2023-05-07 00:00:00' AND '2023-05-07 23:59:59';