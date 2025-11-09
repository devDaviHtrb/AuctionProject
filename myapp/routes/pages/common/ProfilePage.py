from flask import render_template, Blueprint, Response, session
import myapp.repositories.UserRepository as user_repository

profile = Blueprint("profilePage", __name__)

@profile.route("/profile")

def ProfilePage() -> Response:
    user = user_repository.get_by_id(session["user_id"])
    print(user)
    return render_template("Profile.html", name=session["username"], email=user.email, photo_url = user.photo )
