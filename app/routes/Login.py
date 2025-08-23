from flask import render_template, Blueprint


login = Blueprint("login", __name__)

@login.route("/login")
def Login():
    return render_template("Login.html")