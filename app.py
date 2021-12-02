from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route("/")
def index():
    sql = "SELECT id, name, totaltime FROM activities ORDER by totaltime DESC"
    result = db.session.execute(sql)
    activities = result.fetchall()
    return render_template("index.html", activities=activities)

@app.route("/new-activity")
def new_activity():
    return render_template("new-activity.html")

@app.route("/create-activity", methods=["POST"])
def create_activity():
    name = request.form["name"]
    sql = "INSERT INTO activities (name, totaltime) values (:name, NOW() - NOW())"
    result = db.session.execute(sql, {"name":name})
    db.session.commit()
    return redirect("/")

@app.route("/activity-entry/<int:id>")
def activity_entry(id):
    sql = "SELECT name FROM activities WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    name = result.fetchone()[0]
    return render_template("activity-entry.html", name=name, id=id)

@app.route("/add-entry", methods=["POST"])
def add_entry():
    # get datetimes from the form
    start_time = request.form["starttime"]
    end_time = request.form["endtime"]
    
    # check validity of submitted datetimes
    if start_time == "" or end_time == "":
        return render_template("error.html", error="Suoritukselle täytyy valita aloitus- ja päättymisaika!")
    if start_time >= end_time:
        return render_template("error.html", error="Suorituksen aloitusajan täytyy olla ennen päättymisaikaa!")

    # get the id of the corresponding activity
    activity_id = int(request.form["id"])

    # convert datetime strings to SQL timestamp format
    sql = "SELECT to_timestamp(:start_time, 'YYYY-MM-DD THH24H:MI')"
    result = db.session.execute(sql, {"start_time":start_time})
    start_timestamp = result.fetchone()[0]
    sql = "SELECT to_timestamp(:end_time, 'YYYY-MM-DD THH24H:MI')"
    result = db.session.execute(sql, {"end_time":end_time})
    end_timestamp = result.fetchone()[0]
    
    # insert an entry with the activity_id and the timestamps into database
    sql = "INSERT INTO entries (activity_id, start, stop) values " \
          "(:activity_id, :start_timestamp, :end_timestamp)"
    result = db.session.execute(sql, {"activity_id":activity_id, "start_timestamp":start_timestamp, "end_timestamp":end_timestamp})

    # update the total time spent on the corresponding activity
    sql = "UPDATE activities SET totaltime = totaltime + (:end_timestamp - :start_timestamp) WHERE id=:activity_id"
    result = db.session.execute(sql, {"activity_id":activity_id, "end_timestamp":end_timestamp, "start_timestamp":start_timestamp})
    # commit changes
    db.session.commit()
    return redirect("/")
