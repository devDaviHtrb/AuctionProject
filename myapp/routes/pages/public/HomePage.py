from flask import render_template, Blueprint,redirect, session, url_for

home = Blueprint("homePage", __name__)

@home.route("/")
def HomePage():
    if session.get("User") == None:
        return redirect(url_for("loginPage.LoginPage"))
    
    return render_template("index.html")


