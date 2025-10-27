from flask import render_template, Blueprint, Response

signUpPage = Blueprint("signUpPage", __name__)

@signUpPage.route("/signUpPage")
@signUpPage.route("/signUpPage", methods=["GET"])
def SignUpPage(msg:str = "") -> Response:
    return render_template("SignUp.html", message = msg)
