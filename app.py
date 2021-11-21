from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    sql = "SELECT id, name, totaltime FROM activities ORDER by totaltime DESC"
    result = db.session.execute(sql)
    activities = result.fetchall()
    return render_template("index.html", activities=activities)

@app.route("/new-activity")
def newactivity():
    return render_template("new-activity.html")

@app.route("/create-activity", methods=["POST"])
def create_activity():
    name = request.form["name"]
    sql = "INSERT INTO activities (name, totaltime) values (:name, NOW() - NOW())"
    result = db.session.execute(sql, {"name":name})
    db.session.commit()
    return redirect("/")

#@app.route("/activity-entry", methods=["POST"])
#def activityentry():
#    return render_template("activity-entry.html")

def add_entry():
    pass

