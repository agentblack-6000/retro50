import os
import urllib.parse

from flask import redirect, render_template, request, session, flash
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
    special_char =['$', '@', '#', '%', '!']

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


# def get_ten_weeks():
#     next_ten = []
#     base = datetime.datetime.today()
#     for i in range(0, 10):
#         next_ten.append((base + datetime.timedelta(days=(i * 7))))

#     return next_ten

# def find_week(weeks):
#     today = datetime.datetime.today()
#     today_day = today.day
#     today_month = today.month
#     today_year = today.year

#     last_week = weeks[len(weeks) - 1]
#     last_week_day = last_week.day
#     last_week_month = last_week.month
#     last_week_year = last_week.year

#     today = datetime.datetime(year=today_year, month=today_month, day=today_day)
#     last_week = datetime.datetime(year=last_week_year, month=last_week_month, day=last_week_day)

#     if today > last_week:
#         weeks.pop(0)
#         new_week = last_week + datetime.timedelta(days=7)
#         weeks.append(new_week)

#     for week in weeks:
#         current_week_day = week.date().day
#         current_week_month = week.date().month
#         current_week_year = week.date().year
#         current_week = datetime.datetime(year=current_week_year, month=current_week_month, day=current_week_day)

#         try:
#             next_week = weeks[weeks.index(week) + 1]
#         except IndexError:
#             next_week = weeks[len(weeks) - 1]

#         next_week_day = next_week.date().day
#         next_week_month = next_week.date().month
#         next_week_year = next_week.date().year
#         next_week = datetime.datetime(year=next_week_year, month=next_week_month, day=next_week_day)

#         if today == current_week:
#             return weeks.index(week) + 1
#         elif current_week < today < next_week:
#             return weeks.index(week) + 1
#         else:
#             pass


# def shift_weeks():
#     today = datetime.datetime.today()
#     today_day = today.day
#     today_month = today.month
#     today_year = today.year

#     last_week = weeks[len(weeks) - 1]
#     last_week_day = last_week.day
#     last_week_month = last_week.month
#     last_week_year = last_week.year

#     today = datetime.datetime(year=today_year, month=today_month, day=today_day)
#     last_week = datetime.datetime(year=last_week_year, month=last_week_month, day=last_week_day)

#     if today > last_week:
#         return True

#     return False
