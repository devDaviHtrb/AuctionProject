from myapp.models.Bids import bids
from myapp.models.Users import users
from typing import Tuple, Optional

def bidIsValid(bid:bids) -> Optional[users]:
    user = users.query.get(bid.user_id)
    if(user.wallet < bid.bid_value):
        return None
    return user

def last_bid(product_id:int, chunk_size:int = 10) -> Optional[Tuple[bids, users]]:
    offset = 0
    while True:
        consulted_bids = bids.get_bids_filter(
            product_id = product_id,
            offset = offset,
            chunk_size = chunk_size
        )

        if not consulted_bids:
            return

        for bid in consulted_bids:
            bid_user = bidIsValid(bid)
            if(bid_user):
                return bid, bid_user