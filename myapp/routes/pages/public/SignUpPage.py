from flask import render_template, Blueprint, Response

signUpPage = Blueprint("signUpPage", __name__)

@signUpPage.route("/signUpPage")
@signUpPage.route("/signUpPage/<user_type>", methods=["GET"])
@signUpPage.route("/signUpPage/<user_type>/<msg>", methods=["GET"])
def SignUpPage( user_type:str = "physical_person", msg:str = "") -> Response:
    return render_template("SignUp.html", message = msg, user_type = user_type)
