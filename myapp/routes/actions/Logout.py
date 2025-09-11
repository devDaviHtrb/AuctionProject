from flask import Blueprint, make_response, redirect, request, session, url_for


logout = Blueprint("logout", __name__)


@logout.route("/logout", methods=["POST"])
def Logout():
    session.clear()
    return redirect(url_for("home.Home"))