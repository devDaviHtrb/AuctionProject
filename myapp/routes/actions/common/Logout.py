
from flask import Blueprint, redirect, url_for, Response
from flask_login import logout_user
logout = Blueprint("logout", __name__)


@logout.route("/logout", methods=["GET", "POST"])
def Logout() -> Response:
    logout_user()
    return redirect(url_for("home.Home"))