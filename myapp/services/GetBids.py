from myapp.models.Products import products
from myapp.setup.InitSqlAlchemy import db
from myapp.models.Users import users
from myapp.models.Bids import bids
from flask import session

def get_active_user_bids(user_id):

    rows = (
        db.session.query(users, bids, products)
        .join(bids, users.user_id == bids.user_id)
        .join(products, products.product_id == bids.product_id)
        .filter(users.user_id == user_id)
        .all()
    )

    if not rows:
        return []

 
    highest_user_bids = {}  

    for user, bid, product in rows:
        pid = bid.product_id

        if pid not in highest_user_bids:
            highest_user_bids[pid] = {"bid": bid, "product": product}
        else:
           
            if bid.bid_value > highest_user_bids[pid]["bid"].bid_value:
                highest_user_bids[pid] = {"bid": bid, "product": product}


    user_bids = []
    product_ids = []

    for pid, data in highest_user_bids.items():
        user_bids.append({"bid": data["bid"], "product": data["product"], "status": ""})
        product_ids.append(pid)

   
    all_bids = (
        db.session.query(bids)
        .filter(bids.product_id.in_(product_ids))
        .all()
    )

 
    all_bids_by_product = {}
    for bid in all_bids:
        pid = bid.product_id
        if pid not in all_bids_by_product:
            all_bids_by_product[pid] = []
        all_bids_by_product[pid].append(bid)

   
    for entry in user_bids:
        my_bid = entry["bid"]
        pid = my_bid.product_id

   
        highest = None
        for b in all_bids_by_product[pid]:
            if highest is None or b.bid_value > highest.bid_value:
                highest = b

        if highest.bid_id == my_bid.bid_id:
            entry["status"] = "top"
        else:
            entry["status"] = "outbid"

    active_bids = [
        entry for entry in user_bids
        if entry["product"].product_status != 3
    ]

    return active_bids



def get_winner_bids(user_id, ended_status_code=3): #I don't know the code


    rows = (
        db.session.query(users, bids, products)
        .join(bids, users.user_id == bids.user_id)
        .join(products, products.product_id == bids.product_id)
        .filter(users.user_id == user_id)
        .all()
    )

    if not rows:
        return []


    highest_user_bids = {} 

    for user, bid, product in rows:
        pid = bid.product_id

        if pid not in highest_user_bids:
            highest_user_bids[pid] = {"bid": bid, "product": product}
        else:
        
            if bid.bid_value > highest_user_bids[pid]["bid"].bid_value:
                highest_user_bids[pid] = {"bid": bid, "product": product}


    product_ids = []
    user_top_bids = []  

    for pid, data in highest_user_bids.items():
        product = data["product"]
        if product.product_status == ended_status_code:
            product_ids.append(pid)
            user_top_bids.append({"bid": data["bid"], "product": product})

    if not product_ids:
        return []


    all_bids = (
        db.session.query(bids)
        .filter(bids.product_id.in_(product_ids))
        .all()
    )


    all_bids_by_product = {}
    for b in all_bids:
        pid = b.product_id
        if pid not in all_bids_by_product:
            all_bids_by_product[pid] = []
        all_bids_by_product[pid].append(b)


    winner_bids = []

    for entry in user_top_bids:
        my_bid = entry["bid"]
        pid = my_bid.product_id


        highest = None
        for b in all_bids_by_product[pid]:
            if highest is None or b.bid_value > highest.bid_value:
                highest = b

        if highest and my_bid.bid_id == highest.bid_id:
            winner_bids.append({"bid": my_bid, "product": entry["product"]})

  

    return winner_bids
