from flask import render_template, Blueprint

from myapp.models.Products import products

auction = Blueprint("auctionPage", __name__)

@auction.route("/auction/<roomToken>")
def AuctionPage(roomToken):
    product = products.query.filter_by(product_room=roomToken).first()
    return render_template("Auction.html", product = product)