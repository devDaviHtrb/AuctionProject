from flask import render_template, Blueprint, Response

singInPage = Blueprint("singInPage", __name__)

@singInPage.route("/singInPage/<user_type>/<msg>", methods=["GET"])
def SingInPage( user_type, msg: str="") -> Response:
    return render_template("SingIn.html", message = msg, user_type = user_type)