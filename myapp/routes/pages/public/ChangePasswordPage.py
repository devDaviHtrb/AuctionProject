from flask import render_template, Blueprint,redirect, session, url_for, Response

home = Blueprint("changePasswordPage", __name__)

@home.route("/change/now")
@home.route("/change/now/<string:token>")
def ChangePasswordPage(token:str = None) -> Response:
    return render_template("ChangePasswordPage.html", token = token)


