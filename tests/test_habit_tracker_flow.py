import sys
import os

# Ensure the project root directory is in PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from models.habit import HabitManager
from models.users import User
from services.analytics_service import analyze_streaks_by_periodicity, fetch_today_completion_rate
from db.database import create_tables, get_db_connection
import sqlite3
from datetime import datetime, timedelta

@pytest.fixture(scope="module")
def setup_database():
    create_tables()

    db_path = "habit_tracker.db"

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username = 'test_user'")
        cursor.execute("DELETE FROM habits")
        conn.commit()

    user = User(None, "test_user", "test_password", db_path=db_path)
    user.save_to_db()
    user_id = user.get_user_id()
    habit_manager = HabitManager(user_id, db_path=db_path)

    habit_manager.add_preset_habits()

    yield habit_manager, user_id, db_path

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username = 'test_user'")
        cursor.execute("DELETE FROM habits WHERE user_id = ?", (user_id,))
        conn.commit()

def test_registration_and_login(setup_database):
    habit_manager, user_id, db_path = setup_database

    unique_username = f"new_user_{datetime.now().timestamp()}"
    new_user = User(None, unique_username, "new_password", db_path=db_path)
    new_user.save_to_db()
    new_user_id = new_user.get_user_id()
    print(f"Expected user ID: not None, Actual: {new_user_id}")
    assert new_user_id is not None, f"Expected user ID to be not None, got {new_user_id}"

    user = User.get_user_by_username(unique_username, db_path=db_path)
    print(f"Expected user: not None, Actual: {user}")
    assert user is not None, "Expected user to be not None"
    print(f"Expected hashed password: not 'new_password', Actual: {user.password}")
    assert user.password != "new_password", f"Expected password to be hashed, got {user.password}"

def test_add_habit(setup_database):
    habit_manager, user_id, db_path = setup_database
    habit = habit_manager.add_habit("Test Habit", "This is a test habit", "Daily")
    print(f"Expected habit ID: not None, Actual: {habit.habit_id}")
    assert habit.habit_id is not None, f"Expected habit ID to be not None, got {habit.habit_id}"
    print(f"Expected title: 'Test Habit', Actual: {habit.title}")
    assert habit.title == "Test Habit", f"Expected title to be 'Test Habit', got {habit.title}"

def test_complete_habit(setup_database):
    habit_manager, user_id, db_path = setup_database
    habit = habit_manager.add_habit("Complete Habit Test", "This is to test completing a habit", "Daily")
    habit.complete()
    print(f"Expected streak: 1, Actual: {habit.streak}")
    assert habit.streak == 1, f"Expected streak to be 1, got {habit.streak}"
    print(f"Expected completion: 1, Actual: {habit.completion}")
    assert habit.completion == 1, f"Expected completion to be 1, got {habit.completion}"

def test_reset_streak(setup_database):
    habit_manager, user_id, db_path = setup_database
    habit = habit_manager.add_habit("Reset Streak Test", "This is to test resetting a streak", "Daily")
    habit.complete()
    habit.reset_streak()
    print(f"Expected streak after reset: 0, Actual: {habit.streak}")
    assert habit.streak == 0, f"Expected streak to be 0, got {habit.streak}"

def test_longest_streak(setup_database):
    habit_manager, user_id, db_path = setup_database
    habits = habit_manager.get_habits()
    for habit in habits:
        if habit.frequency == 'Daily':
            habit.streak = 10
            habit.save_to_db()

    longest_streak, habit_title = habit_manager.get_longest_overall_streak()
    print(f"Expected longest streak: 10, Actual: {longest_streak}")
    assert longest_streak == 10, f"Expected longest streak to be 10, got {longest_streak}"
    print(f"Expected habit title: not None, Actual: {habit_title}")
    assert habit_title is not None, "Expected habit title to be not None"

def test_analyze_streaks_by_periodicity(setup_database):
    habit_manager, user_id, db_path = setup_database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("UPDATE habits SET streak = 5 WHERE frequency = 'Daily' AND user_id = ?", (user_id,))
    cursor.execute("UPDATE habits SET streak = 3 WHERE frequency = 'Weekly' AND user_id = ?", (user_id,))
    conn.commit()

    cursor.execute("SELECT id, title, frequency, streak FROM habits WHERE user_id = ?", (user_id,))
    habits = cursor.fetchall()
    print("Habits after update:")
    for habit in habits:
        print(habit)

    cursor.execute("""
        SELECT frequency, MAX(streak) as longest_streak
        FROM habits
        WHERE user_id = ?
        GROUP BY frequency
        ORDER BY frequency
    """, (user_id,))

    results = cursor.fetchall()
    print("Results from the query:", results)

    print(f"Expected number of results: 2, Actual: {len(results)}")
    assert len(results) == 2, f"Expected 2 results, got {len(results)}"
    print(f"Expected frequency for first result: 'Daily', Actual: {results[0][0]}")
    assert results[0][0] == 'Daily', f"Expected 'Daily', got {results[0][0]}"
    print(f"Expected longest streak for 'Daily': 5, Actual: {results[0][1]}")
    assert results[0][1] == 5, f"Expected longest streak for 'Daily' to be 5, got {results[0][1]}"
    print(f"Expected frequency for second result: 'Weekly', Actual: {results[1][0]}")
    assert results[1][0] == 'Weekly', f"Expected 'Weekly', got {results[1][0]}"
    print(f"Expected longest streak for 'Weekly': 3, Actual: {results[1][1]}")
    assert results[1][1] == 3, f"Expected longest streak for 'Weekly' to be 3, got {results[1][1]}"

def test_fetch_today_completion_rate(setup_database):
    habit_manager, user_id, db_path = setup_database

    habits = habit_manager.get_habits()
    today = datetime.now().date()

    for habit in habits:
        if habit.frequency == 'Daily':
            habit.last_completed = today
            habit.save_to_db()

    # Ensure no Weekly habits affect the calculation
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM habits WHERE frequency = 'Weekly' AND user_id = ?", (user_id,))
    conn.commit()

    completion_rate = fetch_today_completion_rate(user_id)
    print(f"Expected completion rate: 100, Actual: {completion_rate}")
    assert completion_rate == 100, f"Expected completion rate to be 100, got {completion_rate}"
