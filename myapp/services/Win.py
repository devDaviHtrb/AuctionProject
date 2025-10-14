from myapp.services.GetLastBid import last_bid
from myapp.models.Products import products
from myapp.models.Users import users
from myapp.models.Bids import bids
from typing import Optional

def set_winner(product: products) -> Optional[str]:
    winner_bid, winner_user = last_bid(product.product_id, chunk_size=10)
    if(not winner_bid or not winner_user):
        return

    bid_value = winner_bid.bid_value
    winner_user.wallet -= bid_value 
    winner_bid.winner = True
