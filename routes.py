from app import app
from flask import render_template, request, redirect, abort
import users, categories, activities, entries

@app.route("/")
def index():
	list = activities.get_list()
	return render_template("index.html", activities=list)

@app.route("/login", methods=["POST"])
def login():
	username = request.form["username"]
	password = request.form["password"]
	if not users.login(username, password):
		return render_template("index.html", error="Syöttämäsi tunnus tai salasana on väärin.")
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
	errors = []
    # Check validity of the submitted username and password(s)
	if username == "" or password == "":
		return render_template("new-user.html", error="Käyttäjätunnus ja salasana eivät saa olla tyhjät.", username=username)
	if len(username) > 50:
		errors.append("Käyttäjätunnus on liian pitkä! (Max 50 merkkiä)")
		#return render_template("error.html", error="Käyttäjätunnus on liian pitkä! (Max 50 merkkiä)")
	if len(password) < 6 or len(password) > 100:
		errors.append("Salasanassa on oltava vähintään 6 ja enintään 100 merkkiä.")
		#return render_template("error.html", error="Salasanassa on oltava vähintään 6 merkkiä.")
	if password != password2:
		errors.append("Salasanat eivät täsmää.")
		#return render_template("error.html", error="Salasanat eivät täsmää!")
	if len(errors) >= 1:
		return render_template("new-user.html", errors=errors, username=username)
	if users.register(username, password):
		return redirect("/")
	else:
		return render_template("new-user.html", error="Käyttäjätilin luominen ei onnistunut.")

@app.route("/new-category")
def new_category():
	# Login check
	if users.user_id() != 0:
		return render_template("new-category.html")
	else:
		print("Sinun on kirjauduttava sisään!")
		return redirect("/")

@app.route("/create-category", methods=["POST"])
def create_category():
	csrf_token = request.form["csrf_token"]
	if not users.check(csrf_token):
		abort(403)
	name = request.form["name"]
	if len(name) > 30 or name == "":
		return render_template("new-category.html", error="Nimessä on oltava vähintään 1 ja enintään 30 merkkiä.")
	categories.create(name)
	return redirect("/")
	
# Route for the form where user can create a new activity to track
@app.route("/new-activity")
def new_activity():
	# Login check
	if users.user_id() != 0:
		list = categories.get_list()
		return render_template("new-activity.html", categories=list)
	else:
		return redirect("/")

@app.route("/create-activity", methods=["POST"])
def create_activity():
	csrf_token = request.form["csrf_token"]
	if not users.check(csrf_token):
		abort(403)
	# Get the name of the activity from the form    
	name = request.form["name"]
	if len(name) > 30 or name == "":
		return render_template("new-activity.html", error="Nimessä on oltava vähintään 1 merkki ja enintään 30 merkkiä.")
	category_id = request.form["category"]
	if category_id == "default":
		activities.create(name, 0)
	else:
		activities.create(name, category_id)
	return redirect("/")
    
# Route for the activity's info page
@app.route("/activity/<activity_name>", methods=["POST", "GET"])
def show_activity(activity_name):
	if request.method == "POST":
		activity_id = request.form["a_id"]
		# Check that the user is the owner of the activity
		if activities.owner(activity_id):
			list = entries.get_list(activity_id)
			return render_template("activity.html", entries=list, activity_name=activity_name, activity_id=activity_id)
		else:
			return redirect("/")
	else:
		return redirect("/")

# Route for the page where user can edit an existing activity
@app.route("/edit-activity", methods=["POST"])
def edit_activity():
	activity_id = request.form["a_id"]
	csrf_token = request.form["csrf_token"]
	if not users.check(csrf_token) or not activities.owner(activity_id):
		abort(403)
	name = request.form["a_name"]
	# Get list of user's categories
	list = categories.get_list()
	# Get the current category of the activity
	category = activities.get_category(activity_id)
	return render_template("edit-activity.html", activity_id=activity_id, current_name=name, categories=list, current_category=category)
	
@app.route("/update-activity", methods=["POST"])
def update_activity():
	csrf_token = request.form["csrf_token"]
	activity_id = request.form["a_id"]
	if not users.check(csrf_token) or not activities.owner(activity_id):
		abort(403)
	new_name = request.form["new_name"]
	if len(new_name) > 30 or new_name == "":
		# Get list of user's categories
		list = categories.get_list()
		# Get the current category of the activity
		category = activities.get_category(activity_id)
		error = "Aktiviteetin nimessä on oltava vähintään 1 merkki ja enintään 30 merkkiä."
		return render_template("edit-activity.html", error=error, activity_id=activity_id, current_name=new_name, categories=list, current_category=category)
	category_id = request.form["category"]
	if not activities.update(activity_id, new_name, int(category_id)):
		return redirect("/")
	return redirect("/")
		
# Route for the form where the user can add a time entry for the activity
@app.route("/new-entry", methods=["POST", "GET"])
def activity_entry():
	# Login check
	if users.user_id() != 0:
		name = request.form["a_name"]
		activity_id = request.form["a_id"]
		return render_template("activity-entry.html", name=name, activity_id=activity_id)
	else:
		return redirect("/")

@app.route("/add-entry", methods=["POST"])
def add_entry():
	if not users.check(request.form["csrf_token"]):
		abort(403)
	# Get the id of the corresponding activity
	activity_id = int(request.form["a_id"])
    # Get datetimes from the form
	start_time = request.form["starttime"]
	end_time = request.form["endtime"]
    # Check validity of submitted datetimes
	if start_time == "" or end_time == "":
		return render_template("activity-entry.html", error="Suoritukselle täytyy valita aloitus- ja päättymisaika!", activity_id=activity_id)
	if start_time >= end_time:
		return render_template("activity-entry.html", error="Suorituksen aloitusajan täytyy olla ennen päättymisaikaa!", start=start_time, end=end_time, activity_id=activity_id)
	entries.new(activity_id, start_time, end_time)
    # Return to main page
	return redirect("/")
    
# Route for the page where user can edit and delete an entry
@app.route("/edit-entry", methods=["POST"])
def edit_entry():
	entry_id = request.form["e_id"]
	csrf_token = request.form["csrf_token"]
	if not users.check(csrf_token) or not entries.owner(entry_id):
		abort(403)
	entry = entries.get_times(entry_id)
	return render_template("edit-entry.html", entry_id=entry_id, entry=entry)
	
@app.route("/update-entry", methods=["POST"])
def update_entry():
	entry_id = request.form["e_id"]
	csrf_token = request.form["csrf_token"]
	if not users.check(csrf_token) or not entries.owner(entry_id):
		abort(403)
	# Get updated datetimes from the form
	start_time = request.form["starttime"]
	end_time = request.form["endtime"]
    # Check validity of submitted datetimes
	if start_time == "" or end_time == "":
		entry = entries.get_times(entry_id)
		return render_template("edit-entry.html", error="Suoritukselle täytyy valita aloitus- ja päättymisaika!", entry_id=entry_id, entry=entry)
	if start_time >= end_time:
		entry = entries.get_times(entry_id)
		return render_template("edit-entry.html", error="Suorituksen aloitusajan täytyy olla ennen päättymisaikaa!", entry_id=entry_id, entry=entry)
	entries.update(entry_id, start_time, end_time)
	return redirect("/")
	
@app.route("/delete-entry", methods=["POST"])
def delete_entry():
	entry_id = request.form["e_id"]
	csrf_token = request.form["csrf_token"]
	if not users.check(csrf_token) or not entries.owner(entry_id):
		abort(403)
	activity_id = entries.activity_id(entry_id)
	if not entries.delete(entry_id, activity_id):
		return render_template("index.html", error="Suorituksen poistaminen ei onnistunut.")
	return redirect("/")
