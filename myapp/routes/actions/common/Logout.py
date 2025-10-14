
from flask import Blueprint, redirect, session, url_for, Response

logout = Blueprint("logout", __name__)


@logout.route("/logout", methods=["GET", "POST"])
def Logout() -> Response:
    session["id"] = None
    session["username"] = None
    session["admin"] = None
    return redirect(url_for("home.Home"))