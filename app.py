import os

from cs50 import SQL
import datetime
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, request, render_template, session, redirect, flash

from flask import Flask
from helpers import login_required, validate_password

app = Flask(__name__)

app.jinja_env.filters["str"] = str

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///timetable.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/login", methods=["GET", "POST"])
def login():
    # User reached route via POST (requested login)
    if request.method == "POST":

        # Ensure username exists
        if not request.form.get("username"):
            flash("Invalid username")
            return redirect("/login")

        # Ensure password exists
        elif not request.form.get("password"):
            flash("Invalid password")
            return redirect("/login")

        # Querying database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # len(rows) checks to see if username exists in database and check_password_hash() ensures password matches
        if len(rows) != 1 or not check_password_hash(rows[0]["password_hash"], request.form.get("password")):
            flash("Username/password not found.")
            return redirect("/login")

        # Get rid of any saved user_id
        session.clear()

        # Save the user_id to query databases
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (requested webpage)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    # Get rid of any saved user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():

    # Route reached via GET (requested webpage)
    if request.method == "GET":
        return render_template("register.html")
    else:
        # Gets the username, password, and confirmation from the form
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Checks if the password or confirmation is blank or don't match
        if password == '' or confirmation == '' or password != confirmation:
            flash("Password and/or confirmation blank or do not match.")
            return redirect("/register")

        # Checks to see if username exists and is not blank
        if username == None or username == '':
            flash("Invalid username")
            return redirect("/register")

        if not validate_password(password):
            return redirect("/register")

        # Checks if username is already taken
        usernames = db.execute("SELECT username FROM users;")
        for user in usernames:
            if username == user['username']:
                flash("Sorry, username already taken!")
                return redirect("/register")

        # Generates hashed password to store in the database
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

        # Updates the database with the new values
        db.execute("INSERT INTO users(username, password_hash) VALUES(?, ?)", username, hashed_password)

        return render_template("login.html")


@app.route("/")
@login_required
def index():
    user = session.get("user_id")

    subjects = db.execute("SELECT * FROM subjects WHERE user_id = ?", user)

    for subject in subjects:
        for i in range(10):
            level = int(subject[f"proficiency_{i + 1}"])
            color = ""
            if level == 1:
                color = "#FF0000"
            elif level == 2:
                color = "#FF3300"
            elif level == 3:
                color = "#ff6600"
            elif level == 4:
                color = "#ff9900"
            elif level == 5:
                color = "#FFCC00"
            elif level == 6:
                color = "#FFFF00"
            elif level == 7:
                color = "#ccff00"
            elif level == 8:
                color = "#65fa02"
            elif level == 9:
                color = "#1bfa02"
            elif level == 10:
                color = "#09f005"
            else:
                color = "white"

            subject[f'color_{i + 1}'] = color

    return render_template("index.html", subjects=subjects)


@app.route("/about")
@login_required
def about():
    return render_template("about.html")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    user = session.get("user_id")

    if request.method == "GET":
        return render_template("add.html")
    else:
        subject = request.form.get("subject")
        subjects = db.execute("SELECT * FROM subjects WHERE user_id = ?", user)

        subject_names = []
        for subject_name in subjects:
            subject_names.append(subject_name['subject'].lower())

        if not subject or subject == "_" or subject == "" or subject.lower() in subject_names:
            flash("Invalid subject/subject already in database")
            return redirect("/")

        today = datetime.datetime.today().strftime("%d/%m/%y")
        db.execute("INSERT INTO subjects (user_id, subject, start_date) VALUES (?, ?, ?)", user, subject, today)
        flash(f"Added subject: {subject}")
        return redirect("/")


@app.route("/log", methods=["GET", "POST"])
@login_required
def log_revision():
    user = session.get("user_id")

    if request.method == "GET":
        subjects = db.execute("SELECT * FROM subjects WHERE user_id = ?", user)
        return render_template("revision.html", subjects=subjects)
    else:
        log = request.form.get("revisionLog")

        if log == "" or not log:
            flash("Invalid Subject")
            return redirect("/")

        proficiency = int(request.form.get("proficiency"))
        if proficiency < 0 or proficiency > 10 or not proficiency or proficiency == "":
            flash("Invalid proficiency")
            return redirect("/")

        today = datetime.datetime.today().strftime("%d/%m/%y")
        revision_num = int(db.execute("SELECT revision_num FROM subjects WHERE subject = ? AND user_id = ?", log, user)[0]['revision_num']) + 1

        if revision_num == 10:
            flash("Can't update, table full!")
            return redirect("/")
        else:
            db.execute(f"UPDATE subjects SET revision_{revision_num} = ?, proficiency_{revision_num} = ?, revision_num = ? WHERE subject = ? AND user_id = ?", today, proficiency, revision_num, log, user)
            return redirect("/")


@app.route("/changepwd", methods=["GET", "POST"])
@login_required
def change_password():
    user = session.get("user_id")

    if request.method == "GET":
        return render_template("password.html")
    else:
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Checks if the password or confirmation is blank or don't match
        if password == '' or confirmation == '' or password != confirmation:
            flash("Password and/or confirmation blank or do not match.")
            return redirect("/changepwd")

        if not validate_password(password):
            return redirect("/changepwd")

        # Generates hashed password to store in the database
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

        db.execute("UPDATE users SET password_hash = ? WHERE id = ?", hashed_password, user)

        logout()
        return redirect("/")


@app.route("/timer", methods=["GET", "POST"])
@login_required
def timer():
    if request.method == "GET":
        return render_template("timer.html")


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    user = session.get("user_id")
    subjects = db.execute("SELECT * FROM subjects WHERE user_id = ?", user)

    if request.method == "GET":
        return render_template("delete.html", subjects=subjects)
    else:
        subject = request.form.get("subject")

        subject_names = []
        for subject_name in subjects:
            subject_names.append(subject_name['subject'])

        if not subject or subject == "_" or subject == "" or subject not in subject_names:
            flash("Invalid subject")
            return redirect("/")

        db.execute("DELETE FROM subjects WHERE subject = ? AND user_id = ?", subject, user)
        flash("Deleted successfully")
        return redirect("/")


@app.route("/reset", methods=["POST"])
@login_required
def reset_timetable():
    user = session.get("user_id")

    db.execute("DELETE FROM subjects WHERE user_id = ?", user)
    flash("Deleted timetable succesfully")
    return redirect("/")

@app.route("/resetsubj", methods=["POST"])
@login_required
def reset_subject():
    user = session.get("user_id")
    subjects = db.execute("SELECT * FROM subjects WHERE user_id = ?", user)
    subject = request.form.get("resetSubject")

    subject_names = []
    for subject_name in subjects:
        subject_names.append(subject_name['subject'])

    if not subject or subject == "_" or subject == "" or subject not in subject_names:
        flash("Invalid subject")
        return redirect("/")

    db.execute("DELETE FROM subjects WHERE user_id = ? AND subject = ?", user, subject)
    today = datetime.datetime.today().strftime("%d/%m/%y")
    db.execute("INSERT INTO subjects (user_id, subject, start_date) VALUES (?, ?, ?)", user, subject, today)
    flash(f"Reset {subject} succesfully")
    return redirect("/")