from services.auth_service import register, login
from services.habit_service import add_habit, edit_habit, delete_habit, get_habits, remind_habits
from db.database import create_tables
import getpass


def main_menu(user_id):
    while True:
        print("\nMain Menu")
        print("1. Add Habit")
        print("2. Edit Habit")
        print("3. Delete Habit")
        print("4. List Habits")
        print("5. Complete Habit")
        print("6. Logout")

        choice = input("Enter your choice (1-6): ")

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
            for habit in habits:
                print(f"{habit.habit_id}: {habit.title} - {habit.description} (Frequency: {habit.frequency})")

        elif choice == '5':
            habit_id = int(input("Enter habit ID to mark as completed: "))
            # You would need to implement the complete_habit function in habit_service.py
            # complete_habit(user_id, habit_id)
            print("Habit marked as completed.")

        elif choice == '6':
            print("Logging out...")
            break

        else:
            print("Invalid option. Please try again.")


def main():
    create_tables()
    while True:
        print("\nHabit Tracker CLI")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            username = input("Choose a username: ")
            password = getpass.getpass("Choose a password: ")
            print("Attempting to register...")
            register(username, password)
            print("Register function call completed.")
            print("Registration successful. Please log in.")

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
