from myapp.models.Bids import bids
from myapp.models.Products import products
from myapp.models.ProductStatuses import product_statuses
from myapp.models.Users import users
from myapp.setup.InitSqlAlchemy import db
from sqlalchemy import func
from typing import Dict, Any, List, Optional

def save_item(data: Dict[str, Any]) -> bids:
    new_bid = bids(**data)
    db.session.add(new_bid)
    db.session.flush()
    db.session.commit()
    return new_bid

def get_bids_filter(product_id: int, offset:int, chunk_size:int) -> List[bids]:
    return db.session.query(bids).filter(
        bids.product_id == product_id
    ).order_by(
        bids.bid_datetime.desc()
    ).offset(
        offset
    ).limit(
        chunk_size
    ).all()

def get_last_bids_actives() -> List[bids]:
    latest_bid_subq = (
        db.session.query(
            bids.product_id,
            func.max(bids.bid_datetime).label("latest_datetime")
        ).group_by(
            bids.product_id
        ).subquery()
    )

    return db.session.query().join(
        products,
        products.product_id == bids.product_id
    ).join(
        products,
        products.product_status == product_statuses.product_status_id
    ).join(
        latest_bid_subq,
        (latest_bid_subq.c.product_id == bids.product_id) &
        (latest_bid_subq.c.latest_datetime == bids.bid_datetime)
    ).filter(
        product_statuses.status_name == "active"
    ).all()

def is_valid(bid:bids, ignores:List[int]) -> Optional[users]:
    user = users.query.get(bid.user_id)
    if(user.wallet < bid.bid_value or bid.bid_id in ignores):
        return None
    return user
