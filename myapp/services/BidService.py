from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, and_
from myapp.setup.InitSqlAlchemy import db
from myapp.models.Bids import bids
from myapp.models.Users import users
from myapp.models.Products import products
from myapp.models.ProductStatuses import product_statuses
import myapp.repositories.BidRepository as bid_repository
import myapp.repositories.ProductRepository as product_repository
from typing import Tuple, Dict, Any
from decimal import Decimal

#=============================== ERRORS ===============================
MISSING_INFO =      101 # Missing Informations
INVALID_PRODUCT =   102 # Invalid Product
INSUFICIENT_FUNDS = 103 # Insuficient funds
BID_VALUE_ERROR =   104 # Bid must be higher than current highest bid
OTHER_BIDS_ERROR =  105 # The sum of all your bids exceeds your balance
PROCESS_ERROR =     106 # Error processing bid
#======================================================================

def make_bid(user_id: int, product: products, value: int) -> Tuple[bool, Dict[str, Any]]:
    product_id = product.product_id
    try:
        if not product or product_repository.get_status(product) != "occurring":
            return False, INVALID_PRODUCT

        user = users.query.get(user_id)
        if user.wallet < value:
            return False, INSUFICIENT_FUNDS

        last_bid = (
            db.session.query(bids)
            .filter_by(product_id=product_id)
            .order_by(bids.bid_value.desc())
            .with_for_update()
            .first()
        )

        if last_bid and value <= last_bid.bid_value:
            return False, BID_VALUE_ERROR

        subquery = (
            db.session.query(
                bids.product_id,
                func.max(bids.bid_value).label('max_value')
            ).group_by(bids.product_id).subquery()
        )

        active_bids = (
            db.session.query(bids).join(
                subquery, and_(
                bids.product_id == subquery.c.product_id,
                bids.bid_value == subquery.c.max_value
                )
            ).join(
                products,
                bids.product_id == products.product_id
            ).join(
                product_statuses,
                product_statuses.product_status_id == products.product_status
            ).filter(
                product_statuses.product_status_id == product.product_status,
                bids.product_id != product.product_id,
                bids.user_id == user.user_id, 
            )
        )
        

        t_sum = sum([current.bid_value for current in active_bids], Decimal('0'))
        if t_sum + Decimal(value) > user.wallet:
            return False, OTHER_BIDS_ERROR

        new_bid = bid_repository.save_item({
            "bid_value": value,
            "user_id": user_id,
            "product_id": product_id
        })

        product.min_bid = value

        db.session.commit()

        return True, new_bid

    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error:", e)
        return False, PROCESS_ERROR
