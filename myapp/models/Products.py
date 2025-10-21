from __future__ import annotations
import secrets
from myapp.models.Users import users
from myapp.models.ProductStatuses import product_statuses
from myapp.models.Categories import categories
from myapp.models.TechnicalFeatures import technical_features
from myapp.models.CategoryTechnicalFeatures import category_technical_features
from sqlalchemy import ForeignKey, select
from myapp.setup.InitSqlAlchemy import db
from typing import List, Dict, Any, Optional

class products(db.Model):
    product_id =  db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255), nullable=False)
    product_room = db.Column(db.String(64), unique=True, nullable=False, default=lambda:secrets.token_urlsafe(16))
    description =  db.Column(db.Text, nullable=True)
    min_bid = db.Column(db.DECIMAL(12, 2), nullable=False, default = float(0))
    start_datetime =  db.Column(db.DateTime, nullable=True)
    product_status = db.Column(db.Integer, ForeignKey("product_statuses.product_status_id"), default = 1) #sorry :/ ..........
    street_name = db.Column(db.String(255), nullable=True)
    street_number = db.Column(db.String(6), nullable=True)
    apt = db.Column(db.String(80), nullable=True)
    zip_code = db.Column(db.CHAR(9), nullable=True)
    district = db.Column(db.String(80), nullable=True)
    city = db.Column(db.String(80), nullable=True)
    state = db.Column(db.CHAR(2), nullable=True)
    user_id = db.Column(db.Integer, ForeignKey("users.user_id"))
    #FK 
    category = db.Column(db.Integer, ForeignKey("categories.category_id"), default = 1)

    #changes
    end_datetime = db.Column(db.DateTime, nullable=True)
    duration = db.Column(db.Integer, nullable = False) # In Seconds

    @classmethod
    def save_item(cls, data:Dict[str, Any]) -> products:
        if(data.get("product_status", None)):
            data["product_status"] = select(
                product_statuses.product_status_id
            ).where(
                product_statuses.product_status == data["product_status"]
            )
        if(data.get("category", None)):
            data["category"] = select(
                categories.category_id
            ).where(
                categories.category_name == data["category"]
            )
        new_product = cls(**data)
        db.session.add(new_product)
        db.session.flush()
        db.session.commit()
        return new_product
    
    def get_user(self) -> Optional[users]:
        return users.query.get(self.user_id)
    
    def get_status(self) -> str:
        stmt = select(product_statuses).where(
            product_statuses.product_status_id == self.product_status
        )
        result = db.session.execute(stmt).scalar()
        return result.product_status  # integrity never return None
    
    def set_status(self, new_status:str) -> None:
        new_fk = select(product_statuses.product_status_id).where(
            product_statuses.product_status == new_status.lower()
        ).first()

        if (new_fk):
            self.product_status = new_fk
            db.session.commit()

    @classmethod
    def get_actives(cls) -> List[products]:
        query = db.session.query(cls).join(
            product_statuses,
            cls.product_status == product_statuses.product_status_id
        ).filter(
            product_statuses.status_name == "active"
        )

        return query.all()
    
    def get_technical_feature_id_by_category_id(self) -> List[technical_features]:
        return 