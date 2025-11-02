from flask import render_template, Blueprint, request, session

configPage = Blueprint("configPage", __name__)

@configPage.route("/configPage")
@configPage.route("/configPage/<msg>")
def ConfigPage(msg=None):
    return render_template("Config.html", email=session.get("email"), username=session.get("username"), name=session.get("name"), msg=msg)