from db import db
import users

def get_list():
	user_id = users.user_id()
	sql = "SELECT id, name, totaltime FROM activities WHERE user_id=:user_id ORDER by totaltime DESC"
	result = db.session.execute(sql, {"user_id":user_id})
	return result.fetchall()
	
def create(name):
	user_id = users.user_id()
	if user_id == 0:
		return False
	# Add the activity into the database with initial totaltime 0:00:00
	sql = "INSERT INTO activities (user_id, name, totaltime) values (:user_id, :name, NOW() - NOW())"
	result = db.session.execute(sql, {"user_id":user_id, "name":name})
	db.session.commit()
	return True
    
def owner(activity_id):
	user_id = users.user_id()
	# Check that the logged-in user is the creator of this activity
	sql = "SELECT user_id FROM activities WHERE id=:activity_id"
	result = db.session.execute(sql, {"activity_id":activity_id})
	owner_id = result.fetchone()[0]
	return user_id == owner_id

def update(activity_id, length, add):
	"""Increase the total time if add=True. Substract if add=False."""
	if add:
		sql = "UPDATE activities SET totaltime = totaltime + :length WHERE id=:activity_id"
	else:
		sql = "UPDATE activities SET totaltime = totaltime - :length WHERE id=:activity_id"
	result = db.session.execute(sql, {"activity_id":activity_id, "length":length})
	db.session.commit()
    
def get_name(activity_id):
	sql = "SELECT name FROM activities WHERE id=:activity_id"
	result = db.session.execute(sql, {"activity_id":activity_id})
	return result.fetchone()[0]
