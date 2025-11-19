from decimal import Decimal
from myapp.models.Products import products
from myapp.setup.InitSqlAlchemy import db
from myapp.models.Users import users
from myapp.models.Bids import bids


def get_active_user_bids(user_id):


    rows = db.session.query(bids, products).join(products, bids.product_id == products.product_id).filter(bids.user_id == user_id).order_by(bids.product_id, bids.bid_value.desc()).all()
    
    if not rows:
        return []

    highest_user_bids = {}
    for bid, product in rows:
        pid = bid.product_id
        if pid not in highest_user_bids:
            highest_user_bids[pid] = {
                "bid": bid,
                "product": product
            }

    active_bids = []

 
    for pid, data in highest_user_bids.items():
        my_bid = data["bid"]
        product = data["product"]

        if product.product_status == 3:
            continue

        highest_global_bid = bids.query.filter_by(product_id=pid).order_by(bids.bid_value.desc()).first()
        
        status =  "top" if highest_global_bid and highest_global_bid.bid_id == my_bid.bid_id else "outbid"

        active_bids.append({
            "bid": my_bid,
            "product": product,
            "status": status
        })
    return active_bids




def get_winner_bids(user_id):

    rows = (
        db.session.query(bids, products)
        .join(products, bids.product_id == products.product_id)
        .filter(
            bids.user_id == user_id,
            bids.winner == True,
            products.product_status == 4
        )
        .all()
    )

    winner_bids = []

    for bid, product in rows:
        winner_bids.append({
            "bid": bid,
            "product": product,
            "status":"winner"
        })

    return winner_bids


def get_interesting_user_bids(user_id):
    return get_active_user_bids(user_id)+get_winner_bids(user_id)