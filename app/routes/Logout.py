from flask import Blueprint, make_response, redirect, request, url_for


logout = Blueprint("logout", __name__)


@logout.route("/logout", methods=["POST"])
def Logout():
    if request.method =="POST":
        response = make_response(redirect(url_for("login.Login")))
        response.delete_cookie("User")
        return response