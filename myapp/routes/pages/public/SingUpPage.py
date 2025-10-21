from flask import render_template, Blueprint, Response

singUpPage = Blueprint("singUpPage", __name__)

@singUpPage.route("/singUpPage")
@singUpPage.route("/singUpPage/<user_type>/<msg>", methods=["GET"])
def SingUpPage( user_type:str = "physical_person", msg:str = "") -> Response:
    return render_template("singUp.html", message = msg, user_type = user_type)