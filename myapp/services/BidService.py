from typing import Optional, Dict, Any
from myapp.models.Bids import bids
from myapp.models.Users import users
from myapp.models.Products import products

winners: Dict[int, bids] = {}
"""
{
    product : bid -> It's a bid class of alchemy
}
"""

def restart() -> int:
    chgs = 0
    last_bids = bids.get_last_bids_actives()
    for bid in last_bids:
        chgs += 1
        winners[bid.product_id] = bid
    return chgs


def set_winner(data:Dict[str, Any], product_id:int) -> None:
    new_bid = bids.add_item(data)
    winners[product_id] = new_bid

def make_bid(bid: Dict[str, Any]) -> Optional[str]:
    user_id = bid.get("user_id")
    product_id = bid.get("product_id")
    value = bid.get("value")

    user = users.query.get(user_id)
    wallet = user.wallet

    data = {
        "bid_value":    value,
        "user_id":      user_id,
        "product_id":   product_id
    }

    if(not product_id in winners):

        product = products.query.get(product_id)
        if(not product or product.get_status() != "active"):
            return "Invalid Product"
        
        min_bid = product.min_bid
        if(not min_bid or wallet >= min_bid):
            set_winner(data, product_id)
            return 
        
        return "Bid Amount Must Be Greater Than Minimum Amount"
    
    if (wallet < value):
        return "Don't Have Enough Money"
    if(bid <= winners[product_id].value):
        return "Bid Amount Must Be Greater Than Minimum Amount"
    
    set_winner(data, product_id)

    return 