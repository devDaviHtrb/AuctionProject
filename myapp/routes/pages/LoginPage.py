from flask import redirect, render_template, Blueprint, request, make_response, url_for

from myapp.services.InitSession import init_session
from myapp.services.setCookies import set_cookies

loginPage = Blueprint("loginPage", __name__)
@loginPage.route("/loginPage", methods=["POST", "GET"])
@loginPage.route("/loginPage/<msg>", methods=["POST", "GET"])
def LoginPage(msg=""):
    return render_template("Login.html", message = msg)