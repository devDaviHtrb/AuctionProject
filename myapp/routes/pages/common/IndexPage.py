from flask import render_template, Blueprint

index = Blueprint("index", __name__)

@index.route("/index")
def Index():
    return render_template("index.html")