from flask import render_template, Blueprint, abort
from myapp.models.Images import images
from myapp.models.Products import products
from myapp.models.Categories import categories
from myapp.models.LegalInfos import legal_infos
from myapp.models.Users import users

auction = Blueprint("auctionPage", __name__)

@auction.route("/auction/<roomToken>")
def AuctionPage(roomToken):
    product = products.query.filter_by(product_room=roomToken).first()
    if (not product):
        abort(401)
    product_images = images.query.filter_by(product_id = product.product_id).all()

    return render_template(
        "Auction.html",
        product = product,
        product_images = product_images,
        products = products.query.order_by(products.product_room).limit(3).all(),
        product_category = categories.query.get(product.category).category_name,
        product_user = users.query.get(product.user_id).name,
        product_legal = legal_infos.query.filter_by(product_id = product.product_id).first()
    )