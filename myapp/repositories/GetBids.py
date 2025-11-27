from decimal import Decimal
from typing import Dict, Any
from myapp.models.Products import products
from myapp.setup.InitSqlAlchemy import db
from myapp.models.Users import users
from myapp.models.Bids import bids
from myapp.models.Images import images
from myapp.models.Categories import categories


def get_main_image(product_id):
    img = images.query.filter_by(product_id=product_id, principal_image=True).first()
    return img.image if img else None


def get_product_category(category_id):
    cat = categories.query.filter_by(category_id=category_id).first()
    return cat.category_name if cat else None


def get_active_user_bids(user_id):

    rows = (
        db.session.query(bids, products)
        .join(products, bids.product_id == products.product_id)
        .filter(bids.user_id == user_id)
        .order_by(bids.product_id, bids.bid_value.desc())
        .all()
    )

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

        highest_global_bid = (
            bids.query
            .filter_by(product_id=pid)
            .order_by(bids.bid_value.desc())
            .first()
        )

        status = (
            "top"
            if highest_global_bid and highest_global_bid.bid_id == my_bid.bid_id
            else "outbid"
        )

        active_bids.append({
            "bid": my_bid,
            "product": product,
            "status": status,
            "image_url": get_main_image(pid),
            "category": get_product_category(product.category),
            "high_bid": highest_global_bid.bid_value
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
        print(get_main_image(bid.product_id),flush=True)
        winner_bids.append({
            "bid": bid,
            "product": product,
            "status": "winner",
            "image_url": get_main_image(bid.product_id),
            "category": get_product_category(product.category)
        })

    return winner_bids



def get_interesting_user_bids(user_id:int) -> Dict[str, Any]:
    active_bids = get_active_user_bids(user_id)
    winner_bids = get_winner_bids(user_id)
    return {
        "bids":                 active_bids+winner_bids,
        "active_bids_number":   len(active_bids),
        "winner_bids_number":   len(winner_bids)
    }

def get_all_user_bids(user_id:int) -> Dict[str, Any]:
    all_bids = bids.query.filter_by(user_id = user_id).all()
    winner_bids = get_winner_bids(user_id)
    return{
        "bids":                 all_bids,
        "all_bids_number":      len(all_bids),
        "winner_bids_number":   len(winner_bids)
    }

