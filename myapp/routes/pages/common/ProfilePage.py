from flask import render_template, Blueprint, Response


profile = Blueprint("profilePage", __name__)


@profile.route("/profile")

def ProfilePage() -> Response:
    return render_template("Profile.html")