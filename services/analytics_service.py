from datetime import datetime
from models.habit import HabitManager


def display_analytics(user_id):
    habit_manager = HabitManager(user_id)
    print("\nAnalytics Progress")
    print("1. Monthly Progress")
    print("2. Longest Overall Streak")
    print("3. Longest Streak for a each Habit")
    print("4. Return to Main Menu")

    choice = input("Select an option (1-4): ")

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
        print("\nReturning to Main Menu...")


def fetch_today_completion_rate(user_id):
    habit_manager = HabitManager(user_id)
    return habit_manager.get_today_completion_rate()
