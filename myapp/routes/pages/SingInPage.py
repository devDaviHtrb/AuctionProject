from flask import render_template, Blueprint

singInPage = Blueprint("singInPage", __name__)

@singInPage.route("/singInPage", methods=["GET"])
@singInPage.route("/singInPage/<msg>", methods=["GET"])
def SingInPage(msg=""):
    return render_template("SingIn.html", message = msg)