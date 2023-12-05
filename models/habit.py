import sqlite3
from datetime import datetime, timedelta


class Habit:
    def __init__(self, habit_id, user_id, title, description, frequency, created_at, last_completed=None, streak=0,
                 db_path="habit_tracker.db"):
        self.habit_id = habit_id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.frequency = frequency
        self.created_at = created_at
        self.last_completed = last_completed
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

    @classmethod
    def get_habit_by_id(cls, habit_id, db_path="habit_tracker.db"):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM habits WHERE id = ?', (habit_id,))
            habit_row = cursor.fetchone()
            if habit_row:
                return cls(habit_id, *habit_row[1:], db_path=db_path)
            return None

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


class HabitManager:
    def __init__(self, user_id, db_path="habit_tracker.db"):
        self.user_id = user_id
        self.db_path = db_path

    def add_habit(self, title, description, frequency):
        habit = Habit(None, self.user_id, title, description, frequency, db_path=self.db_path)
        habit.save_to_db()
        return habit

    def edit_habit(self, habit_id, title=None, description=None, frequency=None):
        habit = Habit.get_habit_by_id(habit_id, db_path=self.db_path)
        if habit:
            if title is not None:
                habit.title = title
            if description is not None:
                habit.description = description
            if frequency is not None:
                habit.frequency = frequency
            habit.save_to_db()
            return habit
        return None

    def delete_habit(self, habit_id):
        habit = Habit.get_habit_by_id(habit_id, db_path=self.db_path)
        if habit:
            habit.delete()

    def get_habits(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM habits WHERE user_id = ?', (self.user_id,))
            habit_rows = cursor.fetchall()
            return [Habit(*row, db_path=self.db_path) for row in habit_rows]


    def remind_habits(self):
        today = datetime.now().date()
        habits_to_remind = []
        habits = self.get_habits()
        for habit in habits:
            # Assuming the next_due_date method has been implemented in the Habit class as shown earlier
            if habit.next_due_date() <= today:
                habits_to_remind.append(habit)
        return habits_to_remind
