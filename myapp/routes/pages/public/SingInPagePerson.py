from flask import render_template, Blueprint

singInPage = Blueprint("singInPagePerson", __name__)

@singInPage.route("/singInPage", methods=["GET"])
@singInPage.route("/singInPage/<msg>", methods=["GET"])
def SingInPagePerson(msg=""):
    return render_template("SingInPerson.html", message = msg)