from app import app
from flask import render_template, request, redirect
import users, activities, entries

@app.route("/")
def index():
	list = activities.get_list()
	return render_template("index.html", activities=list)

@app.route("/login", methods=["POST"])
def login():
	username = request.form["username"]
	password = request.form["password"]
	if not users.login(username, password):
		return render_template("error.html", error="Syöttämäsi tunnus tai salasana on väärin.")
    # If login succeeded, return to main page
	return redirect("/")

@app.route("/logout")
def logout():
	users.logout()
	return redirect("/")

# Route for the form where user can register
@app.route("/new-user")
def new_user():
	return render_template("new-user.html")

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
	if users.register(username, password):
		return redirect("/")
	else:
		return render_template("error.html", error="Käyttäjätilin luominen ei onnistunut.")
    
# Route for the form where user can create a new activity to track
@app.route("/new-activity")
def new_activity():
	return render_template("new-activity.html")

@app.route("/create-activity", methods=["POST"])
def create_activity():
	# Get the name of the activity from the form    
	name = request.form["name"]
	if len(name) > 30 or name == "":
		return render_template("error.html", error="Aktiviteetin nimessä on oltava vähintään 1 merkki ja enintään 30 merkkiä.")
	activities.create(name)
	return redirect("/")
    
# Route for the activity's info page
@app.route("/<int:id>/<activity_name>")
def show_info(id, activity_name):
    # Check that the logged-in user is the creator of this activity
	if not activities.owner(id):
		return render_template("error.html", error="Sinulla ei ole oikeutta nähdä tätä sivua.")
	list = entries.get_list(id)
	return render_template("activity.html", entries=list, activity_name=activity_name, activity_id=id)

# Route for the form where the user can add a time entry for a particular activity
@app.route("/<int:id>/activity-entry")
def activity_entry(id):
	if not activities.owner(id):
		return render_template("error.html", error="Sinulla ei ole oikeutta nähdä tätä sivua.")
    # Get the name of the activity from the database
	name = activities.get_name(id)
	return render_template("activity-entry.html", name=name, id=id)

@app.route("/add-entry", methods=["POST"])
def add_entry():
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
	entries.add_entry(activity_id, start_time, end_time)
    # Return to main page
	return redirect("/")
    
# Route for the page where user can edit and delete an entry
@app.route("/<int:activity_id>/<activity_name>/<int:entry_id>/edit-entry")
def edit_entry(activity_id, activity_name, entry_id):
    # Check that the logged-in user is the creator of the entry
	if not entries.owner(entry_id):
		return render_template("error.html", error="Sinulla ei ole oikeutta nähdä tätä sivua.")
	return render_template("edit-entry.html", entry_id=entry_id)
    
@app.route("/delete-entry", methods=["POST"])
def delete_entry():
	entry_id = request.form["entry_id"]
	print("Poistettavan entryn id =", entry_id)
	activity_id = entries.activity_id(entry_id)
	print("activity_id =", activity_id)
	if not entries.delete(entry_id, activity_id):
		return render_template("error.html", error="Suorituksen poistaminen ei onnistunut.")
	return redirect("/")
