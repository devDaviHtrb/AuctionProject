from flask import render_template, Blueprint, Response


profile = Blueprint("profile", __name__)


@profile.route("/profile")

def Profile() -> Response:
    return render_template("Profile.html")