import bcrypt
from models.users import User
from models.habit import HabitManager


def register(username, password):
    # Check if the user already exists
    existing_user = User.get_user_by_username(username)
    if existing_user:
        return "User with this username already exists."

    user = User(None, username, password)
    user.save_to_db()

    user_id = user.get_user_id()

    # Now, add preset habits for this user
    habit_manager = HabitManager(user_id)
    habit_manager.add_preset_habits()

    return "Registration successful."

def login(username, password):
    user = User.get_user_by_username(username)
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
        return user.user_id
    return None
