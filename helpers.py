from flask import redirect, session, flash
from functools import wraps


def login_required(f):
    # Decorate routes to require login.

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def validate_password(password):
    """Checks if password is of the correct length, is alphanumeric, and has special chars"""
    special_char = ['$', '@', '#', '%', '!']

    if len(password) < 6:
        flash('Password length should be at least 6 characters long.')
        return False
    elif not any(char.isdigit() for char in password):
        return False
    elif not any(char in special_char for char in password):
        flash('Password should contain speical characters ($, @, #, %, !).')
        return False
    elif not any(char.isupper() for char in password):
        flash('Password should contain at least one uppercase letter.')
        return False
    elif not any(char.islower() for char in password):
        flash('Password should contain at least one lowercase letter.')
        return False
    else:
        return True
