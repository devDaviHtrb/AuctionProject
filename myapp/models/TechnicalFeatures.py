from myapp.setup.InitSqlAlchemy import db
from sqlalchemy import ForeignKey

class technical_features(db.Model):
    technical_feature_id = db.Column(db.Integer, primary_key=True)
    technical_feature_name = db.Column(db.String(80), nullable=False)