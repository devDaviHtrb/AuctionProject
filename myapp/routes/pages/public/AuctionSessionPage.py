from flask import render_template, Blueprint, abort, Response
import myapp.repositories.ProductRepository as product_repository
import myapp.repositories.UserRepository as user_repository

auction = Blueprint("auctionPage", __name__)

@auction.route("/auction/<string:roomToken>")
def AuctionPage(roomToken: str) -> Response:
    product = product_repository.get_a_and_status_by_room_id(roomToken)
    if (not product):
        abort(400)

    product_images = product_repository.get_images(product)
    pdts = product_repository.get_and_images_and_status_diffents_valids_randomly(product)
    last_bids = product_repository.get_value_datetime_username_of_last_bids(product)
    last_bid = last_bids.first()
    category = product_repository.get_category(product)
    legal_info = product_repository.get_legal_info(product)
    user = user_repository.get_by_id(product.user_id)
    technical_feature = product_repository.get_technical_features_values(product)


    return render_template(
        "Auction.html",
        product = product,
        product_images = product_images,
        products = pdts,
        product_category = category,
        product_user = user.name,
        product_legal = legal_info,
        technical_features = technical_feature,
        last_bid = last_bid,
        last_bids = last_bids,
        
    )
