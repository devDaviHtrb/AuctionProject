from typing import Optional, Dict, Any
from myapp.models.Bids import bids
from myapp.models.Users import users

winners: Dict[int, bids] = {}
"""
{
    product : bid -> It's a bid class of alchemy
}
"""

def restart() -> None:
    pass


def make_bid(bid: Dict[str, Any]) -> Optional[str]:
    user_id = bid.get("user_id")
    product_id = bid.get("product_id")
    value = bid.get("value")

    if(not product_id in winners):
        return "Invalid Product"
    
    user = users.query.get(user_id)
    if (user.wallet < value):
        return "Don't Have Enough Money"
    if(bid <= winners[product_id].value):
        return "Bid Amount Must Be Greater Than Minimum Amount"
    
    data = {
        "bid_value":    value,
        "user_id":      user_id,
        "product_id":   product_id
    }
    
    new_bid = bids.add_item(data)
    winners[product_id] = new_bid

    return 