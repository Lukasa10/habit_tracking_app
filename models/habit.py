import sqlite3
from datetime import datetime , timedelta


class Habit:
    def __init__(self, habit_id, user_id, title, description, frequency, created_at,
                 last_completed=None, streak=0, db_path="habit_tracker.db"):
        self.habit_id = habit_id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.frequency = frequency
        self.created_at = datetime.strptime(created_at, '%Y-%m-%d').date() if isinstance(created_at, str) else created_at
        self.last_completed = datetime.strptime(last_completed, '%Y-%m-%d').date() if last_completed and isinstance(last_completed, str) else last_completed
        self.streak = streak
        self.db_path = db_path

    def save_to_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if self.habit_id is None:
                cursor.execute('''
                    INSERT INTO habits (user_id, title, description, frequency, created_at, last_completed, streak) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (self.user_id, self.title, self.description, self.frequency, self.created_at, self.last_completed,
                      self.streak))
                self.habit_id = cursor.lastrowid
            else:
                cursor.execute('''
                    UPDATE habits 
                    SET title = ?, description = ?, frequency = ?, created_at = ?, last_completed = ?, streak = ? 
                    WHERE id = ?
                ''', (self.title, self.description, self.frequency, self.created_at, self.last_completed, self.streak,
                      self.habit_id))
            conn.commit()

    def delete(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM habits WHERE id = ?', (self.habit_id,))
            conn.commit()

    def complete(self):
        self.last_completed = datetime.now().date()
        self.streak += 1
        self.save_to_db()

    def reset_streak(self):
        self.streak = 0
        self.save_to_db()

    def was_missed(self):
        if not self.last_completed:
            return False
        next_due = self.next_due_date()
        today = datetime.now().date()
        return today > next_due

    def get_completion_rate(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM records WHERE habit_id = ? AND completed = 1', (self.habit_id,))
            completed_count = cursor.fetchone()[0]
            possible_completions = self.calculate_possible_completions()
            if possible_completions == 0:
                return 0
            return (completed_count / possible_completions) * 100

    def calculate_possible_completions(self):
        created_at_date = datetime.strptime(self.created_at, '%Y-%m-%d').date()
        today = datetime.now().date()
        delta_days = (today - created_at_date).days

        if self.frequency == 'Daily':
            return delta_days
        elif self.frequency == 'Weekly':
            return delta_days // 7
        elif self.frequency == 'Monthly':
            return delta_days // 30
        else:
            return 0

    def next_due_date(self):
        # If never completed, use the created_at date
        base_date = self.last_completed if self.last_completed else self.created_at

        if self.frequency == 'Daily':
            return base_date + timedelta(days=1)
        elif self.frequency == 'Weekly':
            return base_date + timedelta(weeks=1)
        elif self.frequency == 'Monthly':
            # This approximation assumes 30 days as a month for simplicity
            return base_date + timedelta(days=30)
        else:
            raise ValueError("Invalid frequency")

    def get_motivational_message(self):
        if self.streak < 5:
            return "Getting started!"
        elif self.streak < 10:
            return "You're on a roll!"
        elif self.streak < 20:
            return "Amazing! Keep going!"
        elif self.streak < 30:
            return "You're crushing it!"
        elif self.streak < 50:
            return "Incredible! Don't stop now!"
        elif self.streak < 100:
            return "You're an inspiration!"
        else:
            return "Legend status!"


class HabitManager:
    def __init__(self, user_id, db_path="habit_tracker.db"):
        self.user_id = user_id
        self.db_path = db_path

    def add_habit(self, title, description, frequency):
        created_at = datetime.now().strftime('%Y-%m-%d')

        habit = Habit(None, self.user_id, title, description, frequency, created_at, db_path=self.db_path)
        habit.save_to_db()
        return habit

    def edit_habit(self, habit_id, title=None, description=None, frequency=None):
        habit = self.get_habit_by_id(habit_id)
        if habit:
            # If the user input is not blank, update the value; otherwise, keep the current value
            habit.title = title if title.strip() else habit.title
            habit.description = description if description.strip() else habit.description
            habit.frequency = frequency if frequency.strip() else habit.frequency

            habit.save_to_db()
            return habit
        return None

    def add_preset_habits(self):  # Fixed: Added 'self' parameter
        preset_habits = [
            {"title": "Drink Water", "description": "Drink at least 8 glasses of water", "frequency": "Daily"},
            {"title": "Morning Exercise", "description": "At least 30 minutes of exercise", "frequency": "Daily"},
            {"title": "Read a Book", "description": "Read for at least 15 minutes", "frequency": "Daily"},
            {"title": "Meditate", "description": "Meditate for 10 minutes to clear your mind", "frequency": "Daily"},
            {"title": "No Junk Food", "description": "Avoid eating junk food", "frequency": "Daily"}
        ]

        for habit in preset_habits:
            self.add_habit(habit['title'], habit['description'], habit['frequency'])

    def delete_habit(self, habit_id):
        habit = self.get_habit_by_id(habit_id)
        if habit:
            habit.delete()

    def get_habits(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM habits WHERE user_id = ?", (self.user_id,))
            habits = [Habit(row['id'], self.user_id, row['title'],
                            row['description'], row['frequency'], row['created_at'], row['last_completed'],
                            row['streak'], self.db_path) for row in cursor.fetchall()]
            return habits

    def remind_habits(self):
        today = datetime.now().date()
        habits_to_remind = []
        habits = self.get_habits()
        for habit in habits:
            if habit.last_completed is None or habit.next_due_date() <= today:
                habits_to_remind.append(habit)
        return habits_to_remind

    def get_habit_by_id(self, habit_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row  # Ensure dictionary-like access to columns
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM habits WHERE id = ?", (habit_id,))
            row = cursor.fetchone()
            if row:
                return Habit(row['id'], self.user_id, row['title'], row['description'], row['frequency'],
                             row['created_at'], row['last_completed'], row['streak'], self.db_path)
            return None

    def reset_missed_streaks(self):
        habits = self.get_habits()
        for habit in habits:
            if habit.was_missed():
                habit.reset_streak()
                habit.save_to_db()
