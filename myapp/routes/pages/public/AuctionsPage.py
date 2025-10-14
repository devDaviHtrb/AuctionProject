from flask import render_template, Blueprint

auctions = Blueprint("auctions", __name__)

@auctions.route("/auctions")
def Auctions():
    return render_template("index.html")