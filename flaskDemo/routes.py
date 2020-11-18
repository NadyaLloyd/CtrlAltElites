from flask import render_template, url_for, flash, redirect
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm
from flaskDemo.models import User, Post
from flask_login import login_user, current_user, logout_user


@app.route("/")
def index():
	return render_template("index.html", content="Testing")

@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user)
			return redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check username and password', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route("/registration", methods=["GET", "POST"])
def registration():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(fname=form.fname.data,lname=form.lname.data,email=form.email.data, password=hashed_password )
		db.session.add(user)
		db.session.commit()
		flash(f'Welcome, {form.fname.data}!', 'success')
		return redirect(url_for('login'))
	return render_template("registration.html", title="Registration", form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route("/addcourse")
def addcourse():
	return render_template("addcourse.html", content="Testing")

@app.route("/editcourse")
def editcourse():
	return render_template("editcourse.html", content="Testing")

@app.route("/home", methods=["GET", "POST"])
def home():
  	return render_template("home.html", content="Testing",is_navbar = "true", is_studentName = "true")

@app.route("/managecourse")
def managecourse():
	return render_template("managecourse.html", content="Testing",is_navbar = "true", is_studentName = "true")

@app.route("/manageassignment")
def manageassignment():
	return render_template("manageassignment.html", content="Testing",is_navbar = "true", is_studentName = "true")

@app.route("/managegrades")
def managegrades():
	return render_template("managegrades.html", content="Testing",is_navbar = "true", is_studentName = "true")

@app.route("/goals")
def goals():
	return render_template("goals.html", content="Testing",is_navbar = "true", is_studentName = "true")
