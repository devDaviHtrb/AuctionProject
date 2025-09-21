from myapp.setup.InitSqlAlchemy import db
from sqlalchemy import ForeignKey
class payments(db.Model):
    payment_id = db.Column(db.Integer, primary_key=True)
    amount =  db.Column(db.DECIMAL(10, 2), nullable=False)
    payment_method =db.Column(db.SmallInteger, nullable=False)
    payment_status =db.Column(db.SmallInteger, nullable=False)
    payer =  db.Column(db.String(255), nullable=False)
    payee =  db.Column(db.String(255), nullable=False)
    opening_datetime =  db.Column(db.DateTime, nullable=False)
    due_datetime =  db.Column(db.DateTime, nullable=False)
    confirmation_datetime =  db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, ForeignKey("users.user_id"))