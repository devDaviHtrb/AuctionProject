from flask import render_template, Blueprint
from flask_login import login_required

profile = Blueprint("profile", __name__)


@profile.route("/profile")

def Profile():
    return render_template("Profile.html")