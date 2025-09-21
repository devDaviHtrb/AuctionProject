from myapp.setup.InitSqlAlchemy import db
from sqlalchemy import ForeignKey
class bids(db.Model):
    bid_id = db.Column(db.Integer, primary_key=True)
    bid_value =  db.Column(db.DECIMAL(12, 2), nullable=False)
    bid_datetime =  db.Column(db.DateTime, nullable=False)
    winner = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("users.user_id"))