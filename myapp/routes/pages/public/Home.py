from flask import render_template, Blueprint,redirect, session, url_for

home = Blueprint("home", __name__)

@home.route("/")
def Home():
    if session.get("User") == None:
        return redirect(url_for("loginPage.LoginPage"))
    
    return render_template("index.html")


