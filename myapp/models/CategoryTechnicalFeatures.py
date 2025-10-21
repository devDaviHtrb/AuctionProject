from myapp.setup.InitSqlAlchemy import db
from myapp.models.TechnicalFeatures import technical_features
from sqlalchemy import ForeignKey, select
from typing import List
class category_technical_features(db.Model):
    technical_feature_id = db.Column(db.Integer, ForeignKey("technical_features.technical_feature_id"),primary_key=True)
    category_id = db.Column(db.Integer, ForeignKey("categories.category_id"), primary_key=True)



