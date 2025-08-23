from flask import render_template, Blueprint


config = Blueprint("config", __name__)

@config.route("/config")
def Config():
    return render_template("Config.html")