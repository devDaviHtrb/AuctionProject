from flask import render_template, Blueprint, Response, session
from myapp.models.Users import users
from myapp.setup.InitSqlAlchemy import db

profile = Blueprint("profilePage", __name__)

@profile.route("/profile")

def ProfilePage() -> Response:
    user = users.query.filter_by(user_id = session["user_id"]).first()


    return render_template("Profile.html", name=session["username"], email=user.email, photo_url = user.photo )