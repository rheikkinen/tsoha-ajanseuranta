from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Route for the main page
@app.route("/")
def index():
    # Login check
    try:
        user_id = session["user_id"]
    except:
        return render_template("index.html")
    # If the user is logged in, get all the activities created by the logged-in user
    sql = "SELECT id, name, totaltime FROM activities WHERE user_id=:user_id ORDER by totaltime DESC"
    result = db.session.execute(sql, {"user_id":user_id})
    activities = result.fetchall()
    return render_template("index.html", activities=activities)

# Login function
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # Check that the submitted username exists
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return render_template("error.html", error="Syöttämäsi tunnus tai salasana on väärin.")
    else:
        # If username exists, check that the password is correct
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["user_id"] = user.id
        else:
            return render_template("error.html", error="Väärä salasana!")
    # If login succeeded, return to main page
    return redirect("/")

# Logout function
@app.route("/logout")
def logout():
    del session["user_id"]
    return redirect("/")

# Route for the form where user can register
@app.route("/new-user")
def new_user():
    return render_template("new-user.html")

# Function for adding a new user to the database    
@app.route("/add-user", methods=["POST"])
def add_user():
    username = request.form["username"]
    password = request.form["password"]
    password2 = request.form["password_again"]
    # Check validity of the submitted username and password(s)
    if username == "" or password == "":
        return render_template("error.html", error="Käyttäjätunnus ja salasana eivät saa olla tyhjät.")
    if len(username) > 50:
        return render_template("error.html", error="Käyttäjätunnus on liian pitkä! (Max 50 merkkiä)")
    if len(password) < 6:
        return render_template("error.html", error="Salasanassa on oltava vähintään 6 merkkiä.")
    if len(password) > 100:
        return render_template("error.html", error="Salasana on liian pitkä.")
    if password != password2:
        return render_template("error.html", error="Salasanat eivät täsmää!")
    else:
        hash_value = generate_password_hash(password)
        # Try to add the user to the database
        try:
            sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
            db.session.execute(sql, {"username":username, "password":hash_value})
            db.session.commit()
        # If error occurs, go to error page
        except:
            return render_template("error.html", error="Tunnuksen luonti epäonnistui.")
    return redirect("/")
    
# Route for the form where user can create a new activity to track
@app.route("/new-activity")
def new_activity():
    # Login check
    try:
        user_id = session["user_id"]
    except:
        return render_template("error.html", error="Et ole kirjautunut sisään!")
    return render_template("new-activity.html")

# Function for creating a new activity and adding it to database
@app.route("/create-activity", methods=["POST"])
def create_activity():
    user_id = session["user_id"]
    # Get the name of the activity from the form    
    name = request.form["name"]
    if len(name) > 30 or name == "":
        return render_template("error.html", error="Aktiviteetin nimessä on oltava vähintään 1 merkki ja enintään 30 merkkiä.")
    # Add the activity into the database with initial totaltime 0:00:00
    sql = "INSERT INTO activities (user_id, name, totaltime) values (:user_id, :name, NOW() - NOW())"
    result = db.session.execute(sql, {"user_id":user_id, "name":name})
    db.session.commit()
    # Return to main page
    return redirect("/")
    
# Route for the activity's info page
@app.route("/<int:id>/<activity_name>")
def show_info(id, activity_name):
    # Login check
    try:
        user_id = session["user_id"]
    except:
        return render_template("error.html", error="Et ole kirjautunut sisään!")  
    # Check that the logged-in user is the creator of this activity
    sql = "SELECT user_id FROM activities WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    owner_id = result.fetchone()[0]
    if user_id != owner_id:
        return render_template("error.html", error="Sinulla ei ole oikeutta nähdä tätä sivua.")
    # Get the entries' start and end times, end date and length in minutes
    sql = "SELECT id, to_char(start, 'HH24:MI') AS start_time, to_char(stop, 'HH24:MI') AS end_time, to_char(stop, 'FMDD.FMMM.YYYY') AS date, floor(EXTRACT(EPOCH FROM (stop - start)))::integer/60 AS length FROM entries WHERE activity_id=:id ORDER BY stop DESC"
    result = db.session.execute(sql, {"id":id})
    entries = result.fetchall()
    return render_template("activity.html", entries=entries, activity_name=activity_name, activity_id=id)

# Route for the form where the user can add a time entry for a particular activity
@app.route("/<int:id>/activity-entry")
def activity_entry(id):
    # Login check
    try:
        user_id = session["user_id"]
    except:
        return render_template("error.html", error="Et ole kirjautunut sisään!")
    # Check that the logged-in user is the creator of this activity
    sql = "SELECT user_id FROM activities WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    owner_id = result.fetchone()[0]
    if user_id != owner_id:
        return render_template("error.html", error="Sinulla ei ole oikeutta nähdä tätä sivua.")
    # Get the name of the activity from the database
    sql = "SELECT name FROM activities WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    name = result.fetchone()[0]
    return render_template("activity-entry.html", name=name, id=id)

# Function for adding the activity entry into the database
@app.route("/add-entry", methods=["POST"])
def add_entry():
    user_id = session["user_id"]
    # Get datetimes from the form
    start_time = request.form["starttime"]
    end_time = request.form["endtime"]
    # Check validity of submitted datetimes
    if start_time == "" or end_time == "":
        return render_template("error.html", error="Suoritukselle täytyy valita aloitus- ja päättymisaika!")
    if start_time >= end_time:
        return render_template("error.html", error="Suorituksen aloitusajan täytyy olla ennen päättymisaikaa!")
    # Get the id of the corresponding activity
    activity_id = int(request.form["id"])
    # Convert datetime strings to SQL timestamp format
    sql = "SELECT to_timestamp(:start_time, 'YYYY-MM-DD THH24H:MI')"
    result = db.session.execute(sql, {"start_time":start_time})
    start_timestamp = result.fetchone()[0]
    sql = "SELECT to_timestamp(:end_time, 'YYYY-MM-DD THH24H:MI')"
    result = db.session.execute(sql, {"end_time":end_time})
    end_timestamp = result.fetchone()[0]
    # Limit the max length of the entry to 24 hours
    sql = "SELECT EXTRACT(EPOCH FROM (:end_timestamp - :start_timestamp))::integer AS length"
    result = db.session.execute(sql, {"end_timestamp":end_timestamp, "start_timestamp":start_timestamp})
    length = result.fetchone()[0] # length in seconds
    if length > 86400:
        return render_template("error.html", error="Suorituksen maksimipituus on rajattu 24 tuntiin.")
    # Insert an entry with the activity_id and the timestamps into database
    sql = "INSERT INTO entries (activity_id, start, stop) values " \
          "(:activity_id, :start_timestamp, :end_timestamp)"
    result = db.session.execute(sql, {"activity_id":activity_id, "start_timestamp":start_timestamp, "end_timestamp":end_timestamp})
    # Update the total time spent on the corresponding activity
    sql = "UPDATE activities SET totaltime = totaltime + (:end_timestamp - :start_timestamp) WHERE id=:activity_id"
    result = db.session.execute(sql, {"activity_id":activity_id, "end_timestamp":end_timestamp, "start_timestamp":start_timestamp})
    # Commit changes
    db.session.commit()
    # Return to main page
    return redirect("/")
    
# Route for the page where user can edit and delete an entry
@app.route("/<int:activity_id>/<activity_name>/<int:entry_id>/edit-entry")
def edit_entry(activity_id, activity_name, entry_id):
    # Login check
    try:
        user_id = session["user_id"]
    except:
        return render_template("error.html", error="Et ole kirjautunut sisään!")
    # Check that the logged-in user is the creator of the entry
    sql = "SELECT user_id FROM activities WHERE id=:activity_id"
    result = db.session.execute(sql, {"activity_id":activity_id})
    owner_id = result.fetchone()[0]
    sql = "SELECT activity_id FROM entries WHERE id=:entry_id"
    result = db.session.execute(sql, {"entry_id":entry_id})
    valid_activity_id = result.fetchone()[0]
    if user_id != owner_id or activity_id != valid_activity_id:
        return render_template("error.html", error="Sinulla ei ole oikeutta nähdä tätä sivua.")
        
    return render_template("edit-entry.html", entry_id=entry_id)
    
# Function for deleting an activity entry
@app.route("/delete-entry", methods=["POST"])
def delete_entry():
    entry_id = request.form["entry_id"]
    # Get the id of the corresponding activity
    sql = "SELECT activity_id FROM entries WHERE id=:entry_id"
    result = db.session.execute(sql, {"entry_id":entry_id})
    activity_id = result.fetchone()[0]
    # Get the length of the entry being deleted 
    sql = "SELECT (stop - start) AS length FROM entries WHERE id=:entry_id"
    result = db.session.execute(sql, {"entry_id":entry_id})
    length = result.fetchone()[0]
    try:
        sql = "DELETE FROM entries WHERE id=:entry_id"
        result = db.session.execute(sql, {"entry_id":entry_id})
        db.session.commit()
        # Substract the length of the deleted entry from the activity's totaltime
        sql = "UPDATE activities SET totaltime = totaltime - :length WHERE id=:activity_id"
        result = db.session.execute(sql, {"length":length, "activity_id":activity_id})
        db.session.commit()
    except:
        return render_template("error.html", error="Aktiviteetin poistaminen ei onnistunut.")
    return redirect("/")
