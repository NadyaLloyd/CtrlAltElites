import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskDemo.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


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
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
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
	return redirect(url_for('index'))

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/Profile_pics', picture_fn)

	output_size = (125,125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)

	i.save(picture_path)

	return picture_fn

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.fname = form.fname.data
		current_user.lname = form.lname.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your Account has been updated!', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.fname.data = current_user.fname
		form.lname.data = current_user.lname
		form.email.data = current_user.email
	image_file = url_for('static', filename='Profile_pics/' + current_user.image_file)
	return render_template("account.html", title="Account",image_file=image_file,form=form,is_navbar = "true") 

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
