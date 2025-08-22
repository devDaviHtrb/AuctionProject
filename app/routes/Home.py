from flask import render_template, Blueprint


home = Blueprint("home", __name__)

@home.route("/")
def Home():
    return render_template("index.html")