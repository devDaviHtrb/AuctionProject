import secrets
from myapp.setup.InitSqlAlchemy import db
from sqlalchemy import ForeignKey, select
from myapp.models.ProductStatuses import product_statuses
from __future__ import annotations
from typing import List

class products(db.Model):
    product_id =  db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255), nullable=False)
    product_room = db.Column(db.String(64), unique=True, nullable=False, default=lambda:secrets.token_urlsafe(16))
    description =  db.Column(db.Text, nullable=True)
    min_bid = db.Column(db.DECIMAL(12, 2), nullable=True)
    start_datetime =  db.Column(db.DateTime, nullable=True)
    product_status = db.Column(db.Integer, ForeignKey("product_statuses.product_status_id")) # delete this shit hlfck my brothers
    street_name = db.Column(db.String(255), nullable=True)
    street_number = db.Column(db.String(6), nullable=True)
    apt = db.Column(db.String(80), nullable=True)
    zip_code = db.Column(db.CHAR(9), nullable=True)
    district = db.Column(db.String(80), nullable=True)
    city = db.Column(db.String(80), nullable=True)
    state = db.Column(db.CHAR(2), nullable=True)
    user_id = db.Column(db.Integer, ForeignKey("users.user_id"))
    category_id = db.Column(db.Integer, ForeignKey("categories.category_id"))

    #changes
    end_datetime = db.Column(db.DateTime, nullable=True)
    duration = db(db.Integer, nullable = True) # In Seconds

    
    def get_status(self) -> str:
        stmt = select(product_statuses).where(
            product_statuses.product_status_id == self.product_status
        )
        result = db.session.execute(stmt).scalar()
        return result.product_status  # integrity never return None

    @classmethod
    def get_actives(cls) -> List[products]:
        query = db.session.query(cls).join(
            product_statuses,
            cls.product_status == product_statuses.product_status_id
        ).filter(
            product_statuses.status_name == "ACTIVE"
        )

        return query.all()

