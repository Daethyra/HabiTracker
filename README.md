# HabiTracker

To timestamp your usage and gather data over time...

## Project Goals

The application must:
- Maintain a userbase and their data
    - User "Records"
        - Habit Names
        - Event Timestamps

The application should:
- Allow the users to retroactively change their stats
- Have a centered graph for visualizing the user's "Records"

Application Flow:
- Login
- Selectbox OR Input: Habit Name
- Click button to 'Record an Event'

## Roadmap

1. Create a function that takes 'Habit Name' as input; Creates a timestamped 'Record' in a database
2. Create a button to Record Events
3. Create a graph that displays the current user's "Records"
4. Create a table that displays the current user's "Records"
5. Plan a sidebar feature that allows the user to change their "Records"

## Project Vocabulary

| Word          | Definition                                                  |
|---------------|--------------------------------------------------------------|
| Habit         | A behavior or habit that is learned over time.             |
| Event         | A row in the database table representing a habit event. |
| Habit Name    | A column in the database table representing a habit name.    |
