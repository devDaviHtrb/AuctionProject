from flask import render_template, Blueprint

loginPage = Blueprint("loginPage", __name__)


@loginPage.route("/loginPage", methods=["GET"])
@loginPage.route("/loginPage/<msg>", methods=["GET"])

def LoginPage(msg=""):
    return render_template("Login.html", message = msg)