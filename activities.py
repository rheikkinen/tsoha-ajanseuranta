from db import db
import users

def get_list():
	#TODO: intervals day, week, month
	user_id = users.user_id()
	sql = "SELECT A.id, A.name, SUM(E.stop - E.start) AS total " \
		  "FROM activities A LEFT JOIN entries E ON A.id=E.activity_id " \
		  "WHERE A.user_id=:user_id GROUP BY A.id"
	result = db.session.execute(sql, {"user_id":user_id})
	return result.fetchall()
	
def create(name, category_id):
	user_id = users.user_id()
	if user_id == 0:
		return False
	if category_id == 0:
		sql = "INSERT INTO activities (user_id, name) VALUES (:user_id, :name)"
		result = db.session.execute(sql, {"user_id":user_id, "name":name})
	else:
		sql = "INSERT INTO activities (user_id, category_id, name) VALUES (:user_id, :category_id, :name)"
		result = db.session.execute(sql, {"user_id":user_id, "category_id":category_id, "name":name})
	db.session.commit()
	return True
    
def owner(activity_id):
	user_id = users.user_id()
	# Check that the logged-in user is the creator of this activity
	sql = "SELECT user_id FROM activities WHERE id=:activity_id"
	result = db.session.execute(sql, {"activity_id":activity_id})
	owner_id = result.fetchone()[0]
	return user_id == owner_id
    
def get_name(activity_id):
	sql = "SELECT name FROM activities WHERE id=:activity_id"
	result = db.session.execute(sql, {"activity_id":activity_id})
	return result.fetchone()[0]
