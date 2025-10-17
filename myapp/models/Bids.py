from __future__ import annotations
from myapp.setup.InitSqlAlchemy import db
from myapp.models.Products import products
from myapp.models.ProductStatuses import product_statuses 
from typing import Dict, Any, List
from datetime import datetime
from sqlalchemy import ForeignKey, func

class bids(db.Model):
    bid_id = db.Column(db.Integer, primary_key=True)
    bid_value =  db.Column(db.DECIMAL(12, 2), nullable=False)
    bid_datetime =  db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    winner = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, ForeignKey("users.user_id"))

    product_id = db.Column(db.Integer, ForeignKey("products.product_id"))

    @classmethod
    def save_item(cls, data: Dict[str, Any]) -> bids:
        new_bid = cls(**data)
        db.session.add(new_bid)
        db.session.flush()
        db.session.commit()
        return new_bid
    
    @classmethod
    def get_bids_filter(cls, product_id: int, offset:int, chunk_size:int) -> List[bids]:
        return db.session.query(cls).filter(
            cls.product_id == product_id
        ).order_by(
            cls.bid_datetime.desc()
        ).offset(
            offset
        ).limit(
            chunk_size
        ).all()
    
    @classmethod
    def get_last_bids_actives(cls) -> List[bids]:
        latest_bid_subq = (
            db.session.query(
                cls.product_id,
                func.max(cls.bid_datetime).label("latest_datetime")
            ).group_by(
                cls.product_id
            ).subquery()
        )

        return db.session.query(cls).join(
            products,
            products.product_id == cls.product_id
        ).join(
            products,
            products.product_status == product_statuses.product_status_id
        ).join(
            latest_bid_subq,
            (latest_bid_subq.c.product_id == cls.product_id) &
            (latest_bid_subq.c.latest_datetime == cls.bid_datetime)
        ).filter(
            product_statuses.status_name == "ACTIVE"
        ).all()