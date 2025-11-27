from myapp.setup.InitSqlAlchemy import db
from sqlalchemy import ForeignKey

class category_technical_features(db.Model):
    technical_feature_id = db.Column(db.Integer, ForeignKey("technical_features.technical_feature_id", ondelete="CASCADE"),primary_key=True)
    category_id = db.Column(db.Integer, ForeignKey("categories.category_id", ondelete="CASCADE"), primary_key=True)
