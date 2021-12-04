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

# The route for the main page
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

# Return a form where user can register
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

# Return a form where user can create a new activity to track
@app.route("/new-activity")
def new_activity():
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
    # Add the activity into the database with initial totaltime 0:00:00
    sql = "INSERT INTO activities (user_id, name, totaltime) values (:user_id, :name, NOW() - NOW())"
    result = db.session.execute(sql, {"user_id":user_id, "name":name})
    db.session.commit()
    # Return to main page
    return redirect("/")

# Route for the form where user can add a time entry for a particular activity
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
    print("Kirjautuneen käyttäjän id on", user_id, type(user_id)) #POISTA!!!!!!!!!!!!!!!!!
    print("Aktiviteetin user_id on", owner_id, type(owner_id)) #POISTA!!!!!!!!!!!!!!!!!!!!
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
