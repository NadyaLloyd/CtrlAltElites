from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)


@app.route("/home")
def home():
	return render_template("home.html", content="Testing")


@app.route("/managecourse")
def managecourse():
	return render_template("managecourse.html", content="Testing")

@app.route("/manageassignment")
def manageassignment():
	return render_template("manageassignment.html", content="Testing")

@app.route("/managegrades")
def managegrades():
	return render_template("managegrades.html", content="Testing")

@app.route("/goals")
def goals():
	return render_template("goals.html", content="Testing")


if __name__ == "__main__":
	app.run(debug=True)