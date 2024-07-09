import unittest
from models.habit import HabitManager
from models.users import User
from db.database import create_tables, get_db_connection
import sqlite3
from datetime import datetime, timedelta


class TestHabitFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        create_tables()

        # Use main database
        cls.db_path = "habit_tracker.db"

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE username = 'test_user'")
            cursor.execute("DELETE FROM habits")
            conn.commit()

        cls.user = User(None, "test_user", "test_password", db_path=cls.db_path)
        cls.user.save_to_db()
        cls.user_id = cls.user.get_user_id()
        cls.habit_manager = HabitManager(cls.user_id, db_path=cls.db_path)

    @classmethod
    def tearDownClass(cls):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE username = 'test_user'")
            cursor.execute("DELETE FROM habits WHERE user_id = ?", (cls.user_id,))
            conn.commit()

    def test_add_habit(self):
        habit = self.habit_manager.add_habit("Test Habit", "This is a test habit", "Daily")
        print(f"Expected habit ID: not None, Actual: {habit.habit_id}")
        print(f"Expected title: 'Test Habit', Actual: {habit.title}")
        self.assertIsNotNone(habit.habit_id)
        self.assertEqual(habit.title, "Test Habit")

    def test_complete_habit(self):
        habit = self.habit_manager.add_habit("Complete Habit Test", "This is to test completing a habit", "Daily")
        habit.complete()
        print(f"Expected streak: 1, Actual: {habit.streak}")
        print(f"Expected completion: 1, Actual: {habit.completion}")
        self.assertEqual(habit.streak, 1)
        self.assertEqual(habit.completion, 1)

    def test_reset_streak(self):
        habit = self.habit_manager.add_habit("Reset Streak Test", "This is to test resetting a streak", "Daily")
        habit.complete()
        habit.reset_streak()
        print(f"Expected streak after reset: 0, Actual: {habit.streak}")
        self.assertEqual(habit.streak, 0)

    def test_longest_streak(self):
        habits = self.habit_manager.get_habits()
        for habit in habits:
            if habit.frequency == 'Daily':
                habit.streak = 10
                habit.save_to_db()

        longest_streak, habit_title = self.habit_manager.get_longest_overall_streak()
        print(f"Expected longest streak: 10, Actual: {longest_streak}")
        print(f"Expected habit title: not None, Actual: {habit_title}")
        self.assertEqual(longest_streak, 10)
        self.assertIsNotNone(habit_title)


if __name__ == '__main__':
    unittest.main()
