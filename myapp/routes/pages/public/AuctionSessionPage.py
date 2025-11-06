from flask import render_template, Blueprint, abort
from myapp.models.Images import images
from myapp.models.Products import products
from myapp.models.Categories import categories
from myapp.models.LegalInfos import legal_infos
from myapp.models.Users import users
from myapp.models.ProductStatuses import product_statuses
import myapp.repositories.ProductRepository as product_repository

auction = Blueprint("auctionPage", __name__)

@auction.route("/auction/<roomToken>")
def AuctionPage(roomToken):
    product = products.query.join(
        product_statuses,
        product_statuses.product_status_id == products.product_status,
        isouter = True
    ).filter(products.product_room == roomToken).first()
    if (not product):
        abort(400)
    product_images = images.query.filter_by(product_id = product.product_id).all()
    pdts = products.query.distinct().join(
        images,
        images.product_id == products.product_id,
        isouter = True
    ).join(
        product_statuses,
        product_statuses.product_status_id == products.product_status,
        isouter=True
    ).order_by(
        products.product_room
    ).filter(
        products.product_room != roomToken,
        product_statuses.product_status != "canceled",
        product_statuses.product_status != "finished"
    ).limit(3).all()
    print([curr.product_name for curr in pdts])
    return render_template(
        "Auction.html",
        product = product,
        product_images = product_images,
        products = pdts,
        product_category = categories.query.get(product.category).category_name,
        product_user = users.query.get(product.user_id).name,
        product_legal = legal_infos.query.filter_by(product_id = product.product_id).first(),
        technical_features = product_repository.get_technical_features_values(product)
    )