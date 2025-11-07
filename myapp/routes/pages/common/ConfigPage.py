from flask import render_template, Blueprint, request, session

configPage = Blueprint("configPage", __name__)

@configPage.route("/configPage")
@configPage.route("/configPage/<msg>")
def ConfigPage(msg=None):
    user_type = session.get("user_type")

    return render_template("Config.html", email=session.get("email"), username=session.get("username"), name=session.get("name"), msg=msg, photo=session.get("user_photo"), user_type = session.get("user_type"), gender = session.get("gender"), cellphone1 = session.get("cellphone1", ""), cellphone2 = session.get("cellphone2", ""), landline = session.get("landline", ""), cpf=session.get("cpf", None), rg=session.get("rg", None))