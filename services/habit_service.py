from models.habit import HabitManager


def add_habit(user_id, title, description, frequency):
    habit_manager = HabitManager(user_id)
    return habit_manager.add_habit(title, description, frequency)


def edit_habit(user_id, habit_id, title=None, description=None, frequency=None):
    habit_manager = HabitManager(user_id)
    return habit_manager.edit_habit(habit_id, title, description, frequency)


def delete_habit(user_id, habit_id):
    habit_manager = HabitManager(user_id)
    habit_manager.delete_habit(habit_id)


def get_habits(user_id):
    habit_manager = HabitManager(user_id)
    return habit_manager.get_habits()


def remind_habits(user_id):
    habit_manager = HabitManager(user_id, "habit_tracker.db")
    return habit_manager.remind_habits()


def complete_habit(user_id, habit_id):
    habit_manager = HabitManager(user_id)
    habit = habit_manager.get_habit_by_id(habit_id)
    if habit:
        habit.complete()
        message = habit.get_motivational_message()
        return True, message
    return False, ""
