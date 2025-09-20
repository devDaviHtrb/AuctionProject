
from flask import render_template, Blueprint,redirect, session, url_for, Response
from flask_login import login_required



home = Blueprint("home", __name__)

@home.route("/")
@login_required
def Home() -> Response:
    if session.get("User") == None:
        return redirect(url_for("loginPage.LoginPage"))
    
    return render_template("index.html")


