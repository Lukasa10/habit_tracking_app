from services.auth_service import register, login
from services.habit_service import add_habit, edit_habit, delete_habit, get_habits, remind_habits, complete_habit
from services.analytics_service import display_analytics, fetch_today_completion_rate
from db.database import create_tables
import getpass


def main_menu(user_id):
    while True:
        today_completion_rate = fetch_today_completion_rate(user_id)
        print(f"\nToday's Completion Rate: {today_completion_rate:.2f}%")
        reminder_mapping = {}
        if today_completion_rate < 100:
            print("\nYour current reminders:")
            reminders = remind_habits(user_id)

            if reminders:
                for index, habit in enumerate(reminders, start=1):
                    print(f"{index}: {habit.title} - {habit.description}")
                    reminder_mapping[index] = habit.habit_id
            else:
                print("No reminders left for today.")
        else:
            print("\nYou have completed all your reminders for today!")

        print("\nMain Menu")
        print("1. Add Habit")
        print("2. Edit Habit")
        print("3. Delete Habit")
        print("4. List Habits")
        print("5. Complete Reminder")
        print("6. Analytical progress")
        print("7. Logout")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            title = input("Enter habit title: ")
            description = input("Enter habit description: ")
            frequency = input("Enter habit frequency (Daily, Weekly, Monthly): ")
            add_habit(user_id, title, description, frequency)
            print("Habit added successfully.")

        elif choice == '2':
            habit_id = int(input("Enter habit ID to edit: "))
            title = input("Enter new title (leave blank to keep current): ")
            description = input("Enter new description (leave blank to keep current): ")
            frequency = input("Enter new frequency (Daily, Weekly, Monthly, leave blank to keep current): ")
            edit_habit(user_id, habit_id, title, description, frequency)
            print("Habit updated successfully.")

        elif choice == '3':
            habit_id = int(input("Enter habit ID to delete: "))
            delete_habit(user_id, habit_id)
            print("Habit deleted successfully.")

        elif choice == '4':
            habits = get_habits(user_id)
            print('here are the list of your habits: ')
            if habits:
                print("\nYour Habits:")
                for habit in habits:
                    created_at_str = habit.created_at.strftime("%Y-%m-%d")
                    print(f"Habit ID: {habit.habit_id}, Title: {habit.title}, Created on: {created_at_str}")
            else:
                print("You have no habits set up yet.")

        elif choice == '5':
            reminder_number = int(input("Enter reminder number to mark as completed: "))
            if reminder_number in reminder_mapping:
                habit_id = reminder_mapping[reminder_number]
                success, message = complete_habit(user_id, habit_id)
                if success:
                    print(f"Reminder {reminder_number} completed: {message}")
                else:
                    print("Error completing the reminder. Please try again.")
            else:
                print("Invalid reminder number. Please try again.")

        elif choice == '6':
            display_analytics(user_id)

        elif choice == '7':
            print("Logging out...")
            break

        else:
            print("Invalid option. Please try again.")


def main():
    create_tables()
    while True:
        print("\nWelcome to Habit Tracker")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            username = input("Choose a username: ")
            password = getpass.getpass("Choose a password: ")
            print("Attempting to register...")
            registration_result = register(username, password)
            if registration_result == "Registration successful.":

                print("Registration successful. Please log in.")
            else:
                print(registration_result)

        elif choice == '2':
            username = input("Enter your username: ")
            password = getpass.getpass("Enter your password: ")
            user_id = login(username, password)
            if user_id:
                print("Login successful.")
                main_menu(user_id)
            else:
                print("Invalid username or password.")

        elif choice == '3':
            print("Exiting the program.")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
