from myapp.services.GetLastBid import last_bid
from myapp.models.Products import products
from myapp.setup.InitSqlAlchemy import db
from myapp.models.Payments import payments
from typing import Optional
from datetime import datetime

INTERN_MONEY = "intern_money"
RECEIVED = "received"

def set_winner(product: products) -> None:
    winner_bid, winner_user = last_bid(product.product_id, chunk_size=10)
    if(not winner_bid or not winner_user):
        return 

    seller_user = product.get_user()

    bid_value = winner_bid.bid_value

    winner_user.wallet -= bid_value 
    winner_bid.winner = True
    seller_user.wallet += bid_value

    # changing owner
    product.user_id = winner_user.user_id

    db.session.commit()

    data = {
        "amount":                   bid_value,
        "confirmation_datetime":    datetime.utcnow(),
        "payer_user_id":            seller_user.user_id,
        "payee_user_id":            winner_user.user_id,
        "payment_method":           INTERN_MONEY,
        "payment_status":           RECEIVED
    }
    payments.save_item(data)