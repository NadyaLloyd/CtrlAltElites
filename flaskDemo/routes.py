from flask import render_template, url_for, flash, redirect
from flaskDemo import app
from flaskDemo.forms import RegistrationForm, LoginForm
from flaskDemo.models import User, Post


@app.route("/")
def index():
	return render_template("index.html", content="Testing")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            # flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
    
@app.route("/registration", methods=["GET", "POST"])
def registration():
	form = RegistrationForm()
	if form.validate_on_submit():
		# flash(f'Welcome, {form.fname.data}!', 'success')
		return redirect(url_for('home'))
	return render_template("registration.html", title="Registration", form=form)

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
