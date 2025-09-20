from flask import render_template, Blueprint, Response

singInPage = Blueprint("singInPageLegalEntity", __name__)

@singInPage.route("/singInPage", methods=["GET"])
@singInPage.route("/singInPage/<msg>", methods=["GET"])
def SingInPageLegalEntity(msg: str="") -> Response:
    return render_template("SingInPerson.html", message = msg)