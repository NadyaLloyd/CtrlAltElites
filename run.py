from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)


@app.route("/")
def index():
	return render_template("index.html", content="Testing")

@app.route("/logIn", methods=["GET", "POST"] )
def logIn():
	return render_template("logIn.html", content="Testing")

@app.route("/signup")
def signup():
	return render_template("signup.html", content="Testing")

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


if __name__ == "__main__":
	app.run(debug=True)