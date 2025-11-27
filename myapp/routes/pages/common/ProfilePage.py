from flask import render_template, Blueprint, Response, session
from myapp.repositories.GetBids import get_all_user_bids
import myapp.repositories.UserRepository as user_repository
import myapp.repositories.ProductRepository as product_repository

profile = Blueprint("profilePage", __name__)

@profile.route("/profile")
@profile.route("/profile/<string:username>")

def ProfilePage(username:str = None) -> Response:
    user = None
    if not username:
        user_id = session["user_id"]
        user = user_repository.get_by_id(user_id)
        username = user.username
    else:
        user = user_repository.get_by_username(username)

    data = get_all_user_bids(user.user_id)

    tbids = data.get("bids", []) 
    
    limit_bids = []#[{}]
    for i in range(min(len(tbids), 3)):
        # shit my friends, It's so amazing...
        product = product_repository.get_by_id(tbids.product_id)
        limit_bids.append({
            "bids":     tbids[i],
            "photo":    product_repository.get_images(tbids.product_id)[0],
            "status":   product_repository.get_status(product),
            "name":     product.product_name,
            "room":     product.product_room,

        })

    user_params = {
        "username": user.username,
        "name":     user.name,
    }
    if(user.username == session["username"]):
        user_params["wallet"] = user.wallet

    all_cnt = data.get("all_bids_number", 0)
    winner_cnt = data.get("winner_bids_number", 0)
    pdts_cnt = len(product_repository.get_bids_by_user(user))

    return render_template(
        "Profile.html",
        user_param =   user_params,
        bids =          limit_bids,
        bought_count =  winner_cnt,
        total_bids =    all_cnt,
        listed_items =  pdts_cnt
    )
