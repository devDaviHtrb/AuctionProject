from sqlalchemy.exc import SQLAlchemyError
from myapp.setup.InitSqlAlchemy import db
from myapp.models.Bids import bids
from myapp.models.Users import users
from myapp.models.Products import products
import myapp.repositories.BidRepository as bid_repository
import myapp.repositories.ProductRepository as product_repository
import myapp.repositories.PaymentRepository as payment_repository
from datetime import datetime
from typing import Optional

INTERN_MONEY = "intern_money"
RECEIVED = "received"

def make_bid(user_id: int, product_id: int, value: int) -> Optional[str]:
    try:
        with db.session.begin(): 
            product = db.session.query(products).with_for_update().get(product_id)
            if (not product or product_repository.get_status(product) != "active"):
                return "Invalid Product"

            user = users.query.get(user_id)
            if (user.wallet < value):
                return "Insufficient funds"

            last_bid = db.session.query(bids).filter_by(
                product_id = product_id
            ).order_by(
                bids.bid_value.desc()
            ).with_for_update().first()

            if (last_bid and value <= last_bid.bid_value):
                return "Bid must be higher than current highest bid"

            bid_repository.save_item({
                "bid_value":    value,
                "user_id":      user_id,
                "product_id":   product_id
            })

        db.session.commit()

    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error:", e)
        return "Error processing bid"
