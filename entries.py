from db import db
import users, activities

def get_list(activity_id):
	# Get the entries' start and end times, end date and length in minutes
	sql = "SELECT id, to_char(start, 'HH24:MI') AS start_time, to_char(stop, 'HH24:MI') AS end_time, " \
    	  "to_char(stop, 'FMDD.FMMM.YYYY') AS date, floor(EXTRACT(EPOCH FROM (stop - start)))::integer/60 AS length " \
    	  "FROM entries WHERE activity_id=:activity_id ORDER BY stop DESC"
	result = db.session.execute(sql, {"activity_id":activity_id})
	return result.fetchall()

def add_entry(activity_id, start, end):
	user_id = users.user_id()
	start_time = to_timestamp(start)
	end_time = to_timestamp(end)
	# Add entry to the database
	sql = "INSERT INTO entries (activity_id, start, stop) values " \
          "(:activity_id, :start_time, :end_time) RETURNING (stop - start) AS length"
	result = db.session.execute(sql, {"activity_id":activity_id, "start_time":start_time, "end_time":end_time})
	length = result.fetchone()[0]
	# Update the totaltime of the activity
	activities.update(activity_id, length, add=True)
	
def delete(entry_id, activity_id):
	try:
		sql = "DELETE FROM entries WHERE id=:entry_id RETURNING (stop - start) AS length"
		result = db.session.execute(sql, {"entry_id":entry_id})
		db.session.commit()
	except:
		return False
	# Update the totaltime of the activity
	length = result.fetchone()[0]
	activities.update(activity_id, length, add=False)
	return True
	
def owner(entry_id):
	user_id = users.user_id()
	sql = "SELECT activity_id FROM entries WHERE id=:entry_id"
	result = db.session.execute(sql, {"entry_id":entry_id})
	activity_id = result.fetchone()[0]
	return activities.owner(activity_id)
	
def activity_id(entry_id):
	sql = "SELECT activity_id FROM entries WHERE id=:entry_id"
	result = db.session.execute(sql, {"entry_id":entry_id})
	return result.fetchone()[0]
	
def to_timestamp(datetime):
	sql = "SELECT to_timestamp(:datetime, 'YYYY-MM-DD THH24H:MI')"
	result = db.session.execute(sql, {"datetime":datetime})
	return result.fetchone()[0]
