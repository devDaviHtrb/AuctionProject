from flask import render_template, Blueprint, request

configPage = Blueprint("configPage", __name__)

@configPage.route("/configPage")
def ConfigPage():
    return render_template("Config.html", StyleMode= request.cookies.get("StyleMode"), AnonymousMode =  request.cookies.get("AnonymousMode"), AccessibilityMode=request.cookies.get("AccessibilityMode"))