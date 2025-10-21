from flask import render_template, Blueprint,redirect, session, url_for, Response

home = Blueprint("changePassworPage", __name__)

@home.route("/change_now/<string:token>")
def ChangePassword(token:str) -> Response:
    return render_template("ChangePasswordPage.html", token = token)


