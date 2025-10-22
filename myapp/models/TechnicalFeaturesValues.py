from __future__ import annotations
from myapp.setup.InitSqlAlchemy import db
from sqlalchemy import ForeignKey
class technical_features_values(db.Model):
    technical_feature_id = db.Column(db.Integer, ForeignKey("technical_features.technical_feature_id"),primary_key=True)
    category_id = db.Column(db.Integer, ForeignKey("categories.category_id"),primary_key=True)
    value =  db.Column(db.String(255), nullable=False)
    product_id = db.Column(db.Integer, ForeignKey("products.product_id"), primary_key=True)

    @classmethod
    def save_item(cls, data) -> technical_features_values:
        new_technical_features_values = cls(**data)
        db.session.add(new_technical_features_values)
        db.session.flush()
        db.session.commit()