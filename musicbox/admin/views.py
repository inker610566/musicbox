from .. import app
from flask import request, session, render_template
import secret

@app.route("/admin/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		if request.form["username"] == secret.username and request.form["password"] == secret.password:
			session["sid"] = "A"
			# redirection
			return render_template("admin/login_success.htmld")
	return render_template("admin/login.htmld")
