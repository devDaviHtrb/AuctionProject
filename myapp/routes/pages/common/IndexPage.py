from flask import render_template, Blueprint

index = Blueprint("indexPage", __name__)

@index.route("/index")
def IndexPage():
    return render_template("index.html")