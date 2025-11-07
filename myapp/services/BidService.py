from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, and_
from myapp.setup.InitSqlAlchemy import db
from myapp.models.Bids import bids
from myapp.models.Users import users
from myapp.models.Products import products
from myapp.models.ProductStatuses import product_statuses
import myapp.repositories.BidRepository as bid_repository
import myapp.repositories.ProductRepository as product_repository
import myapp.repositories.PaymentRepository as payment_repository
from datetime import datetime
from typing import Optional, Tuple, Dict, Any
from decimal import Decimal



INTERN_MONEY = "intern_money"
RECEIVED = "received"

def make_bid(user_id: int, product: products, value: int) -> Tuple[bool, Dict[str, Any]]:
    product_id = product.product_id
    try:
        if not product or product_repository.get_status(product) != "occurring":
            return False, "Invalid Product"

        user = users.query.get(user_id)
        if user.wallet < value:
            return False, "Insufficient funds"

        last_bid = (
            db.session.query(bids)
            .filter_by(product_id=product_id)
            .order_by(bids.bid_value.desc())
            .with_for_update()
            .first()
        )

        if last_bid and value <= last_bid.bid_value:
            return False, "Bid must be higher than current highest bid"

        subquery = (
            db.session.query(
                bids.product_id,
                func.max(bids.bid_value).label('max_value')
            ).group_by(bids.product_id).subquery()
        )

        # Query principal: junta os dados do produto e filtra apenas lances vencedores do usuário
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
            return False, "The sum of all your bids exceeds your balance."

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
        return False, "Error processing bid"
