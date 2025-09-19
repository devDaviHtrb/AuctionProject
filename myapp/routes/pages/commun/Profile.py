from flask import render_template, Blueprint


profile = Blueprint("profile", __name__)


@profile.route("/profile")

def Profile():
    return render_template("Profile.html")