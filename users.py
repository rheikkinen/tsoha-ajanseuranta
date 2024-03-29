from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex

def login(username, password):
	sql = "SELECT id, password FROM users WHERE username=:username"
	result = db.session.execute(sql, {"username":username})
	user = result.fetchone()
	if not user:
		return False
	if check_password_hash(user.password, password):
		session["user_id"] = user.id
		# Set a secret token for this session
		session["csrf_token"] = token_hex(16)
		return True
	else:
		return False
        	
def logout():
	del session["user_id"]
	del session["csrf_token"]
	
def register(username, password):
	hash_value = generate_password_hash(password)
    # Try to add the user to the database
	try:
		sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
		db.session.execute(sql, {"username":username, "password":hash_value})
		db.session.commit()
	except:
		return False
	# If the registration is successful, log the user in
	return login(username, password)

def user_id():
	return session.get("user_id", 0)
	
def check(csrf_token):
	return session["csrf_token"] == csrf_token

