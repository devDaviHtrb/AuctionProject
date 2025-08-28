from flask import redirect, render_template, Blueprint, request, make_response, url_for

profile = Blueprint("profile", __name__)


@profile.route("/profile")
def Profile():
    return render_template("Profile.html")