from __future__ import annotations
from myapp.setup.InitSqlAlchemy import db
from sqlalchemy import ForeignKey
from datetime import datetime

class payments(db.Model):
    payment_id = db.Column(db.Integer, primary_key=True)
    amount =  db.Column(db.DECIMAL(10, 2), nullable=False)
    opening_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    due_datetime =  db.Column(db.Date, nullable=False, default=datetime.utcnow) #change for date
    confirmation_datetime =  db.Column(db.DateTime, nullable=True)

    payer_user_id =  db.Column(db.Integer, ForeignKey("users.user_id"))
    payee_user_id =  db.Column(db.Integer, ForeignKey("users.user_id"))

    payment_method = db.Column(db.Integer, ForeignKey("payment_methods.payment_method_id"))
    payment_status = db.Column(db.Integer, ForeignKey("payment_statuses.payment_status_id"))

    asaas_payment_id = db.Column(db.Integer, nullable = True)


    
        