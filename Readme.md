# Habit Tracker App

## Overview

The Habit Tracker App helps users create, manage, and track their habits. Users can register, log in, and interact with their habits through various functionalities provided by the app.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Required Python packages listed in `requirements.txt`

### Installation

1. Clone the repository:
    ```bash
    git clone git@github.com:Lukasa10/habit_tracking_app.git
    cd habit_tracking_app
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv .hta_venv
    source .hta_venv/bin/activate  # On Windows use `.hta_venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Program

To run the Habit Tracker App, execute the following command:

```bash
python main.py
```

This will initialize the habit_tracker.db instantly

### Using the App

#### Register:

- When you run the program, choose option `1` to register a new user.
- Enter a username and password when prompted.

#### Log In:

- After registering, restart the program and choose option `2` to log in.
- Enter the username and password you used during registration.

#### Log Out:

- After you are finish using the application you can exit by choosing option `3`

#### Main Menu:

After logging in, you will be presented with the main menu. Here are the available options:
1. **Add Habit**: Add a new habit by entering the title, description, and frequency (Daily, Weekly, Monthly).
2. **Edit Habit**: Edit an existing habit by entering the habit ID and the new details.
3. **Delete Habit**: Delete a habit by entering its ID.
4. **List Habits**: View a list of all your habits.
5. **Complete Reminder**: Mark a reminder as completed by entering its number.
6. **Analytical Progress**: View analytical progress, such as monthly completion rate and longest streak.
7. **Logout**: Log out from the application.

## Testing

### Unit Testing with `unittest`

To run the unit tests using `unittest`, execute the following command:

```bash
python -m unittest tests.test_habit_functions
```
### Integration Testing with `pytest`

To run the tests using `pytest` and see the detailed output, execute the following command:

```bash
pytest -v --maxfail=1 -s tests/test_habit_tracker_flow.py
```
the test will print out the expected value and the printout value of the test.

### Test Cases Covered

- **Registration and Login**:
  - Validates that new users can be registered and existing users can log in.
  - Prints the expected and actual user ID, ensuring the registration works correctly.
  
- **Habit Management**:
  - **Adding a Habit**: Tests for adding a new habit and validates the habit ID and title.
  - **Completing a Habit**: Tests for marking a habit as completed and validates the streak and completion count.
  - **Resetting a Habit Streak**: Tests for resetting the streak of a habit and validates the streak value.
  
- **Streak Computation**:
  - **Longest Streak**: Ensures the correctness of the longest streak calculation by setting a streak for daily habits and checking the longest streak.
  
- **Analytics**:
  - **Analyze Streaks by Periodicity**: Updates streaks for daily and weekly habits and verifies the longest streaks for each frequency.
  - **Fetch Today's Completion Rate**: Sets the last completed date for daily habits to today and verifies the completion rate.
