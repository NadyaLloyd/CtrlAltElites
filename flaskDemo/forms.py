from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, DateField, SelectField, HiddenField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskDemo.models import User, Assignment, Grade, Course

CourseId = Course.query.with_entities(Course.CourseId, Course.CourseName).distinct()
result2=list()
for row in CourseId:
    rowDict=row._asdict()
    result2.append(rowDict)
myChoices = [(row['CourseId'],row['CourseName']) for row in result2]

class RegistrationForm(FlaskForm):
	fname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
	lname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email already exists. Please choose different one')


class LoginForm(FlaskForm):	
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
	fname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
	lname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
	submit = SubmitField('Update')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('Email already exists. Please choose different one')

class ADDCourse(FlaskForm) :
        CourseId = IntegerField('CourseId', validators=[DataRequired()])
        CourseName = StringField('CourseName', validators=[DataRequired()])
        CourseCredit = IntegerField('CourseCredit', validators=[DataRequired()])
        Semester = IntegerField('Semester', validators=[DataRequired()])
        Add = SubmitField('Add Course')

        def validate_pid(self, CourseId):
            course = Course.query.filter_by(CourseId=CourseId.data).first()
            if course:
                raise ValidationError('CourseId already taken please choose different Id')

class UpdateCourse(FlaskForm) :
        CourseId = HiddenField("")
        CourseName = StringField('CourseName', validators=[DataRequired()])
        CourseCredit = IntegerField('CourseCredit', validators=[DataRequired()])
        Semester = IntegerField('Semester', validators=[DataRequired()])
        Add = SubmitField('Update Course')

class ADDAssignment(FlaskForm) :
        AssignmentId = IntegerField('AssignmentId', validators=[DataRequired()])
        AssignmentName = StringField('AssignmentName', validators=[DataRequired()])
        AssignmentPoints = IntegerField('AssignmentPoints', validators=[DataRequired()])
        AssignmentDescription = StringField('AssignmentDescription', validators=[DataRequired()])
        CourseId = SelectField('CourseName', choices=myChoices, coerce=int) 
        Add = SubmitField('Add Assignment')

        def validate_pid(self, AssignmentId):
            assignment = Assignment.query.filter_by(AssignmentId=AssignmentId.data).first()
            if assignment:
                raise ValidationError('AssignmentId already taken. Please choose different Id')

class UpdateAssignment(FlaskForm) :
        AssignmentId = HiddenField("")
        AssignmentName = StringField('AssignmentName', validators=[DataRequired()])
        AssignmentPoints = IntegerField('AssignmentPoints', validators=[DataRequired()])
        AssignmentDescription = StringField('AssignmentDescription', validators=[DataRequired()])
        CourseId = SelectField('CourseName', choices=myChoices, coerce=int) 
        Add = SubmitField('Update Assignment')

class ADDGrade(FlaskForm) :
        GradeId = IntegerField('GradeId', validators=[DataRequired()])
        GradeValue = StringField('GradeValue', validators=[DataRequired()])
        GradeCategory = StringField('GradeCategory', validators=[DataRequired()])
        CourseId = SelectField('CourseName', choices=myChoices, coerce=int) 
        Add = SubmitField('Add Grade')

        def validate_pid(self, GradeId):
            grade = Grade.query.filter_by(GradeId=GradeId.data).first()
            if Grade:
                raise ValidationError('GradeId already taken please choose different Id')                

class UpdateGrade(FlaskForm) :
        GradeId = HiddenField("")
        GradeValue = StringField('GradeValue', validators=[DataRequired()])
        GradeCategory = StringField('GradeCategory', validators=[DataRequired()])
        CourseId = SelectField('CourseName', choices=myChoices, coerce=int) 
        Add = SubmitField('Update Grade')
