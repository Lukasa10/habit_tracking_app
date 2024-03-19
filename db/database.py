import sqlite3
import logging

DATABASE_NAME = "habit_tracker.db"


def get_db_connection():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logging.error(f"Error connecting to database: {e}")
        raise


def create_tables():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    frequency TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    last_completed DATE,
                    streak INTEGER DEFAULT 0,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS completions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER NOT NULL,
                    completion_date DATE NOT NULL,
                    FOREIGN KEY(habit_id) REFERENCES habits(id)
                );
            """)
            conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Error creating tables: {e}")
        raise
