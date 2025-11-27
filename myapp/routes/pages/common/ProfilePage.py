from flask import render_template, Blueprint, Response, session
import myapp.repositories.UserRepository as user_repository
#import myapp.repositories.

profile = Blueprint("profilePage", __name__)

@profile.route("/profile/<string: username>")

def ProfilePage(username:str) -> Response:
    user = user_repository.get_by_id(session["user_id"])

    if(user.username == username):
        return render_template("Profile.html")
