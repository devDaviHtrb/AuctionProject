from flask import render_template, Blueprint, abort, Response
from myapp.utils.Async import run_async_functions
import myapp.repositories.ProductRepository as product_repository
import myapp.repositories.UserRepository as user_repository

auction = Blueprint("auctionPage", __name__)

@auction.route("/auction/<string:roomToken>")
def AuctionPage(roomToken: str) -> Response:
    product = product_repository.get_a_and_status_by_room_id(roomToken)
    if (not product):
        abort(404)

    product_images = product_repository.get_images(product)

    # parameters(list[func, *args, **kargs])
    results = run_async_functions([
        (
            product_repository.get_and_images_and_status_diffents_valids_randomly,
            (product,),
            {}
        ),
        (
            product_repository.get_value_datetime_username_of_last_bids,
            (product,),
            {}
        ),
        (
            product_repository.get_category,
            (product,),
            {}
        ),
        (
            product_repository.get_legal_info,
            (product,),
            {}
        ),
        (
            user_repository.get_by_id,
            (product.user_id,),
            {}
        ),
        (
            product_repository.get_technical_features_name_and_values,
            (product,),
            {}
        )
    ])

    print("debug:", results, flush=True)
    pdts =              results[0]
    last_bids =         results[1]
    category =          results[2]
    legal_info =        results[3]
    user =              results[4]
    technical_feature = results[5]

    last_bid =          last_bids.first()


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
