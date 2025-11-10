from myapp.models.Bids import bids
from myapp.models.Products import products
from myapp.models.ProductStatuses import product_statuses
from myapp.models.Users import users
from myapp.setup.InitSqlAlchemy import db
from myapp.setup.InitCache import cache, cache_key
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


def is_valid(bid:bids, ignores:List[int]) -> Optional[users]:
    user = users.query.get(bid.user_id)
    if(user.wallet < bid.bid_value or bid.bid_id in ignores):
        return None
    return user
