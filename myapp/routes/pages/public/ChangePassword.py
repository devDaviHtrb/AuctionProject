from flask import render_template, Blueprint,redirect, session, url_for, Response

home = Blueprint("changePassword", __name__)

@home.route("/")
def changePassword() -> Response:
    return render_template("ChangePasswordPage.html")


