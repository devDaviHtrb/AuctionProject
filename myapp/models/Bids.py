from __future__ import annotations
from myapp.setup.InitSqlAlchemy import db
from typing import Dict, Any, List
from datetime import datetime
from sqlalchemy import ForeignKey
class bids(db.Model):
    bid_id = db.Column(db.Integer, primary_key=True)
    bid_value =  db.Column(db.DECIMAL(12, 2), nullable=False)
    bid_datetime =  db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    winner = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, ForeignKey("users.user_id"))

    product_id = db.Column(db.Integer, ForeignKey("products.product_id"))

    def add_item(cls, data: Dict[str, Any]) -> bids:
        new_bid = cls(**data)
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