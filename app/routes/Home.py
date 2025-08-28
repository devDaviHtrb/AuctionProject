from flask import render_template, Blueprint, request, redirect, url_for


home = Blueprint("home", __name__)

@home.route("/")
def Home():
    if request.cookies.get("User") == None:
        return redirect(url_for("login.Login"))
    
    return render_template("index.html")