from flask import render_template, Blueprint, Response

home = Blueprint("changePasswordPage", __name__)

@home.route("/change/now")
@home.route("/change/now/<string:token>")
def ChangePasswordPage(token:str = None) -> Response:
    return render_template("ChangePasswordPage.html", token = token)
