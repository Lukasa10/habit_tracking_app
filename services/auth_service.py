import bcrypt
from models.users import User


def register(username, password):
    user = User(None, username, password)
    user.save_to_db()


def login(username, password):
    user = User.get_user_by_username(username)
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
        return user.user_id
    return None
