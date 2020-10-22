from datetime import datetime
from flaskDemo import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	fname = db.Column(db.String(20), unique=True, nullable=False)
	lname = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(20), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)

	def __repr__(self):
		return f"User('{self.fname}', '{self.lname}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	def __repr__(self):
		return f"User('{self.fname}', '{self.lname}', '{self.email}', '{self.image_file}')"