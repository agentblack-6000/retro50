# retro50
#### Description:
Welcome to retro50, a Flask web app implementing a retrospective revision timetable for Harvard's CS50's final project!

Visit the project here(implemented in Railway)-
[Retro50](https://retro50-production.up.railway.app)

Incase the link doesn't work, visit the offical repo for the project-
[retro50 repo](https://github.com/agentblack-6000/retro50)

## Project Overview
retro50 was designed to help students study and revise using a retrospective revision timetable, implemented in Flask. Using a SQLite database, it logs revision entries, keeps track of the subjects, and stores the timetable itself, which is managed by the logic in ```app.py```

## Project Files
The project is a Flask application and has a ```templates/``` directory to manage the webpages and the ```static/``` directory to manage the styling, and a little bit of JS in situations where it is easier to update the DOM without reloading the page, as seen in-
- ```revision.html```  uses a bit of JS in ```<script>``` tags to display the proficiency slider value(used to log revisions in a retrospective revision timetable)

- The JS logic for ```timer.html```, implemented in ```timer.js```, made in Javascript instead of Python as it is easier to constantly update the DOM using JS

#### ```templates/```
All of the templates extend from ```layout.html``` making it easy to add/remove basic elements from each page.

In addition to this, each webpage is also web accessible, with inputs containg proper ```aria-label``` attributes and ```<label>``` tags, and the color scheme is also fairly simple to ensure everyone can use retro50.

#### ```static/```
Contains ```images/```, the stylesheet, and ```timer.js``` to manage ```timer.html```

#### ```app.py```
Handles the logic of each of the routes, controls database queries, and some specific logic required for each route, as well as the Flask session. The most important routes implemented are-
- register(/register)- Adds new users to the database, validating their usernames and passwords
- index(/)- Queries for the user_id and and all the subjects, and assigns a color key to each subject based on proficiency, which is used in ```index.html``` to render the color-coded retrospective revision timetable.
- add(/add)- First checks if the subject is not already in the database, and then adds the subject to the database.
- delete(/delete)- First checks if the subject is in the database and then deletes the record from the table.
- about(/about)- Renders the about page
- the login and logout routes

Additional features implemented-
- timer(/timer)- A basic implementation of a Pomodoro timer to help in study sessions, with a link to the Wikipedia page
- change password(/changepwd)- Updates the user's current password after validating it
- reset timetable(/reset)- Deletes the entire timetable, instead of making the user delete each subject one by one to save time
- reset subject(/resetsubj)- Deletes and adds the subject to the timetable, clearing the revision log, useful after exams/tests are over to prepare for the next one.


#### ```helpers.py```
Contains a login decorator implemented in CS50 to ensure users are logged in while accessing certain routes and a ```validate_password()``` function, which are implemented in a separate file to-
- Keep the logic for the routes and database queries separate
- Easier to implement new functionality for the application without cluttering the ```app.py``` file.

#### ```timetable.db```
A SQLite database where the subjects, timetable, and users are stored, managed using CS50's library in ```app.py```. Contains a table for the users, storing username and password hash, and the subjects table, containing the revision dates and proficiency logs, all of which is put together in ```index.html``` to render the timetable.

## How do I get started?
retro50's goal is to be easy to use and quick to learn, with the only requirement being to register for an account which requires only a username and a password.

After registering for an account and logging in, you will be able to view your retrospective revision timetable, add and delete subjects, use the Pomodoro timer implemented in ```timer.html```, log revisions in your timetable, and change your password.

## How do I clone the repository?
Run the following command-
```
git clone https://github.com/agentblack-6000/retro50.git
```

## Project Updates
This web app was built as a final project for CS50, although future plans entail-
- Using Django instead of Flask
- Using PostgreSQL and the actual SQLAlchemy library instead of SQLite and the CS50 library
- Adding fancier JS to detect password strength
- A small forum (also implemented by PostgreSQL) for students to publish helpful resources and questions

## Credits
The project would not have been possible without these libraries-
- The CS50 library
- Flask
- Werkzeug