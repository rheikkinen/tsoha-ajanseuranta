from db import db
import users

def create(name):
	user_id = users.user_id()
	if user_id == 0:
		return False
	# Add the category into the database
	sql = "INSERT INTO categories (user_id, name) values (:user_id, :name)"
	result = db.session.execute(sql, {"user_id":user_id, "name":name})
	db.session.commit()
	return True
