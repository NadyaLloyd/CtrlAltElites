import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, ADDCourse, UpdateCourse, ADDAssignment, UpdateAssignment, ADDGrade, UpdateGrade
from flaskDemo.models import User, Post, Assignment, Grade, Course
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from flask_mysqldb import MySQL


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

@app.route("/managecourse", methods=['GET', 'POST'])
def managecourse():
    
    return render_template('managecourse.html')

@app.route("/addcourse", methods=['GET', 'POST'])
def addcourse():
    form = ADDCourse()
    if form.validate_on_submit():
        adds = Course(CourseId=form.CourseId.data, CourseName=form.CourseName.data, CourseCredit=form.CourseCredit.data, Semester=form.Semester.data)
        db.session.add(adds)
        db.session.commit()
        flash('Course Added', 'success')
        return redirect(url_for('courselist'))
    return render_template('addcourse.html', form=form, legend='Add Purchase')

@app.route("/courselist", methods=['GET', 'POST'])
def courselist():
    results = db.session.query(Course)\
              .add_columns(Course.CourseId, Course.CourseName)
    return render_template('courselist.html', joined_m_n=results)

@app.route("/course1/<CourseId>")
@login_required
def course1(CourseId):
    course = db.session.query(Course).filter_by(CourseId=CourseId).first()
    return render_template('course_u_d.html', course=course)

@app.route("/course_delete/<CourseId>", methods=['POST'])
@login_required
def course_delete(CourseId):
    course = db.session.query(Course).filter_by(CourseId=CourseId).first()
    db.session.delete(course)
    db.session.commit()
    flash('The Course has been removed!', 'success')
    return redirect(url_for('courselist'))


@app.route("/course/<CourseId>/update", methods=['GET', 'POST'])
@login_required
def course_update(CourseId):
    course = db.session.query(Course).filter_by(CourseId=CourseId).first()
    currentcor = course.CourseId
    form = UpdateCourse()
    if form.validate_on_submit():       
        course.CourseId=form.CourseId.data
        course.CourseName=form.CourseName.data
        course.CourseCredit=form.CourseCredit.data
        course.Semester=form.Semester.data
        db.session.commit()
        flash('Your Course has been Updated', 'success')
        return redirect(url_for('courselist'))
    elif request.method == 'GET':              

        form.CourseId.data = course.CourseId
        form.CourseName.data = course.CourseName
        form.CourseCredit.data = course.CourseCredit
        form.Semester.data = course.Semester
    return render_template('addcourse.html', form=form, legend='Update Course')

@app.route("/home", methods=["GET", "POST"])
def home():
  	return render_template("home.html", content="Testing",is_navbar = "true", is_studentName = "true")

#@app.route("/managecourse")
#def managecourse():
	#return render_template("managecourse.html", content="Testing",is_navbar = "true", is_studentName = "true")

@app.route("/manageassignment")
def manageassignment():
	return render_template("manageassignment.html", content="Testing",is_navbar = "true", is_studentName = "true")

@app.route("/addassignment", methods=['GET', 'POST'])
def addassignment():
    form = ADDAssignment()
    if form.validate_on_submit():
        adds = Assignment(AssignmentId=form.AssignmentId.data, AssignmentName=form.AssignmentName.data, AssignmentPoints=form.AssignmentPoints.data, AssignmentDescription=form.AssignmentDescription.data, CourseId=form.CourseId.data)
        db.session.add(adds)
        db.session.commit()
        flash('Assignment Added', 'success')
        return redirect(url_for('assignmentlist'))
    return render_template('addassignment.html', form=form, legend='Add Purchase')

@app.route("/assignmentlist", methods=['GET', 'POST'])
def assignmentlist():
    results = db.session.query(Assignment)\
              .add_columns(Assignment.AssignmentId, Assignment.AssignmentName)
    return render_template('assignmentlist.html', joined_m_n=results)

@app.route("/assignment1/<AssignmentId>")
@login_required
def assignment1(AssignmentId):
    assignment = db.session.query(Assignment).filter_by(AssignmentId=AssignmentId).first()
    return render_template('assignment_u_d.html', assignment=assignment)

@app.route("/assignment_delete/<AssignmentId>", methods=['POST'])
@login_required
def assignment_delete(CourseId):
    assignment = db.session.query(Assignment).filter_by(AssignmentId=AssignmentId).first()
    db.session.delete(assignment)
    db.session.commit()
    flash('The Assignment has been removed!', 'success')
    return redirect(url_for('assignmentlist'))

@app.route("/assignment/<AssignmentId>/update", methods=['GET', 'POST'])
@login_required
def assignment_update(AssignmentId):
    assignment = db.session.query(Assignment).filter_by(AssignmentId=AssignmentId).first()
    currentass = assignment.AssignmentId
    form = UpdateAssignment()
    if form.validate_on_submit():       
        assignment.AssignmentId=form.AssignmentId.data
        assignment.AssignmentName=form.AssignmentName.data
        assignment.AssignmentPoints=form.AssignmentPoints.data
        assignment.AssignmentDescription=form.AssignmentDescription.data
        assignment.CourseId=form.CourseId.data
        db.session.commit()
        flash('Your Assignment has been Updated', 'success')
        return redirect(url_for('assignmentlist'))
    elif request.method == 'GET':              

        form.AssignmentId.data = assignment.AssignmentId
        form.AssignmentName.data = assignment.AssignmentName
        form.AssignmentPoints.data = assignment.AssignmentPoints
        form.AssignmentDescription.data = assignment.AssignmentDescription
    return render_template('addassignment.html', form=form, legend='Update Assignment')


@app.route("/managegrades")
def managegrades():
	return render_template("managegrades.html", content="Testing",is_navbar = "true", is_studentName = "true")

@app.route("/addgrade", methods=['GET', 'POST'])
def addgrade():
    form = ADDGrade()
    if form.validate_on_submit():
        adds = Grade(GradeId=form.GradeId.data, GradeValue=form.GradeValue.data, GradeCategory=form.GradeCategory.data, CourseId=form.CourseId.data)
        db.session.add(adds)
        db.session.commit()
        flash('Grade Added', 'success')
        return redirect(url_for('gradelist'))
    return render_template('addgrade.html', form=form, legend='Add Grade')

@app.route("/gradelist", methods=['GET', 'POST'])
def gradelist():
    results = db.session.query(Grade)\
              .add_columns(Grade.GradeId, Grade.GradeValue, Grade.CourseId)
    return render_template('gradelist.html', joined_m_n=results)

@app.route("/grade1/<GradeId>")
@login_required
def grade1(GradeId):
    grade = db.session.query(Grade).filter_by(GradeId=GradeId).first()
    return render_template('grade_u_d.html', grade=grade)

@app.route("/grade_delete/<GradeId>", methods=['POST'])
@login_required
def grade_delete(CourseId):
    grade = db.session.query(Grade).filter_by(GradeId=GradeId).first()
    db.session.delete(grade)
    db.session.commit()
    flash('The Grade has been removed!', 'success')
    return redirect(url_for('gradelist'))

@app.route("/grade/<GradeId>/update", methods=['GET', 'POST'])
@login_required
def grade_update(GradeId):
    grade = db.session.query(Grade).filter_by(GradeId=GradeId).first()
    currentgra = grade.GradeId
    form = UpdateGrade()
    if form.validate_on_submit():       
        grade.GradeId=form.GradeId.data
        grade.GradeValue=form.GradeValue.data
        grade.GradeCategory=form.GradeCategory.data
        grade.CourseId=form.CourseId.data
        db.session.commit()
        flash('Your Grade has been Updated', 'success')
        return redirect(url_for('gradelist'))
    elif request.method == 'GET':              

        form.GradeId.data = grade.GradeId
        form.GradeValue.data = grade.GradeValue
        form.GradeCategory.data = grade.GradeCategory
        form.CourseId.data = grade.CourseId
    return render_template('addgrade.html', form=form, legend='Update Grade')

@app.route("/goals")
def goals():
	return render_template("goals.html", content="Testing",is_navbar = "true", is_studentName = "true")
