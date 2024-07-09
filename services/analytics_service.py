import sqlite3
from models.habit import HabitManager

def display_analytics(user_id):
    habit_manager = HabitManager(user_id)
    print("\nAnalytics Progress")
    print("1. Monthly Progress")
    print("2. Longest Overall Streak")
    print("3. Longest Streak for each Habit")
    print("4. Longest Streak by Periodicity")
    print("5. Return to Main Menu")

    choice = input("Select an option (1-5): ")

    if choice == '1':
        monthly_completion_rate, most_frequent, least_frequent = habit_manager.get_monthly_completion_rate()
        print(f"\nMonthly Completion Rate: {monthly_completion_rate:.2f}%")
        print(f"Most Frequently Completed Habit: {most_frequent}")
        print(f"Least Frequently Completed Habit: {least_frequent}")
    elif choice == '2':
        longest_streak, habit_title = habit_manager.get_longest_overall_streak()
        print(f"The longest overall streak is {longest_streak} days, achieved by habit '{habit_title}'.")
    elif choice == '3':
        habits_info = habit_manager.get_habits_sorted_by_frequency_and_streak()
        for habit in habits_info:
            habit_id, title, completion_count, streak = habit
            print(f"Habit ID: {habit_id}, Title: '{title}', Completions: {completion_count}, Streak: {streak} days")
    elif choice == '4':
        analyze_streaks_by_periodicity(user_id)
    elif choice == '5':
        print("\nReturning to Main Menu...")

def fetch_today_completion_rate(user_id):
    habit_manager = HabitManager(user_id)
    return habit_manager.get_today_completion_rate()

def analyze_streaks_by_periodicity(user_id):
    conn = sqlite3.connect("habit_tracker.db")  # Ensure the database path is correct
    cursor = conn.cursor()

    # This SQL query groups habits by their frequency and finds the maximum streak for each frequency
    cursor.execute("""
        SELECT frequency, MAX(streak) as longest_streak
        FROM habits
        WHERE user_id = ?
        GROUP BY frequency
        ORDER BY frequency
    """, (user_id,))

    results = cursor.fetchall()  # Fetches all the grouped records from the database
    if results:
        print("\nLongest Streaks by Periodicity:")
        for result in results:
            print(f"Frequency: {result[0]}, Longest Streak: {result[1]} days")
    else:
        print("\nNo habits found to analyze.")
