import sqlite3
import bcrypt
from db.database import get_db_connection


class User:
    def __init__(self, user_id, username, password, db_path="habit_tracker.db"):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.db_path = db_path

    def save_to_db(self):
        hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (self.username, hashed_password))
            self.user_id = cursor.lastrowid
            conn.commit()

    @classmethod
    def get_user_by_username(cls, username, db_path="habit_tracker.db"):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user_row = cursor.fetchone()
            if user_row:
                return cls(*user_row, db_path=db_path)
            return None
