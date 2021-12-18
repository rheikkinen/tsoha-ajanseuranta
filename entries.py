from db import db
import users, activities

def get_list(activity_id):
	# Get the entries' start and end times, end date and length in minutes
	sql = "SELECT id, to_char(start, 'HH24:MI') AS start_time, to_char(stop, 'HH24:MI') AS end_time, " \
    	  "to_char(stop, 'FMDD.FMMM.YYYY') AS date, floor(EXTRACT(EPOCH FROM (stop - start)))::integer/60 AS length " \
    	  "FROM entries WHERE activity_id=:activity_id ORDER BY stop DESC"
	result = db.session.execute(sql, {"activity_id":activity_id})
	return result.fetchall()
	
def get_times(entry_id):
	# Get entry's start and end time as datetime strings
	sql = """SELECT to_char(start, 'YYYY-MM-DD"T"HH24:MI') AS start_time,
		  to_char(stop, 'YYYY-MM-DD"T"HH24:MI') AS end_time
		  FROM entries WHERE id=:entry_id"""
	result = db.session.execute(sql, {"entry_id":entry_id})
	return result.fetchone()

def new(activity_id, start, end):
	start_time = to_timestamp(start)
	end_time = to_timestamp(end)
	# Add entry to the database
	try:
		sql = "INSERT INTO entries (activity_id, start, stop) values " \
          "(:activity_id, :start_time, :end_time) RETURNING (stop - start) AS length"
		result = db.session.execute(sql, {"activity_id":activity_id, "start_time":start_time, "end_time":end_time})
		db.session.commit()
		return True
	except:
		return False
		
def update(entry_id, start, end):
	start_time = to_timestamp(start)
	end_time = to_timestamp(end)
	# Try to update the start and end time of the entry
	try:
		sql = "UPDATE entries SET start = :start_time, stop = :end_time WHERE id=:entry_id"
		result = db.session.execute(sql, {"entry_id":entry_id, "start_time":start_time, "end_time":end_time})
		db.session.commit()
		return True
	except:
		return False
	
def delete(entry_id, activity_id):
	try:
		sql = "DELETE FROM entries WHERE id=:entry_id RETURNING (stop - start) AS length"
		result = db.session.execute(sql, {"entry_id":entry_id})
		db.session.commit()
		return True
	except:
		return False
	
def owner(entry_id):
	user_id = users.user_id()
	sql = "SELECT user_id FROM activities A JOIN entries E ON E.activity_id=A.id WHERE E.id=:entry_id"
	result = db.session.execute(sql, {"entry_id":entry_id})
	owner_id = result.fetchone()[0]
	return user_id == owner_id
	
def activity_id(entry_id):
	sql = "SELECT activity_id FROM entries WHERE id=:entry_id"
	result = db.session.execute(sql, {"entry_id":entry_id})
	return result.fetchone()[0]
	
def to_timestamp(datetime):
	sql = "SELECT to_timestamp(:datetime, 'YYYY-MM-DD THH24H:MI')"
	result = db.session.execute(sql, {"datetime":datetime})
	return result.fetchone()[0]
