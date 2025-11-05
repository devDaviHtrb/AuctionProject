from flask import render_template, Blueprint

auctions = Blueprint("auctionsPage", __name__)

@auctions.route("/auctions")
def AuctionsPage():
    return render_template("Auctions.html")