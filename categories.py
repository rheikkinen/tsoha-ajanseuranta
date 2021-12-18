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
	
def get_list():
	"""Get list of the categories created by the user"""
	user_id = users.user_id()
	sql = "SELECT id, name FROM categories WHERE user_id=:user_id"
	result = db.session.execute(sql, {"user_id":user_id})
	return result.fetchall()