from __future__ import annotations
from myapp.setup.InitSqlAlchemy import db
from myapp.models.PaymentMethods import payment_methods
from myapp.models.PaymentStatuses import payment_statuses
from typing import Optional, Dict, Any
from sqlalchemy import ForeignKey, select
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


    @classmethod
    def save_item(cls, data:Dict[str, Any]) -> Optional[payments]:
        data["payment_method"] = select(
            payment_methods.payment_method_id
        ).where(
            payment_methods.payment_method== data.get("payment_method", "other").lower()
        ).first()

        data["payment_status"] = select(
            payment_statuses.payment_status_id
        ).where(
            payment_statuses.payment_status == data.get("payment_status", "other").lower()
        ).first()

        new_payment = cls(**data)
        db.session.add(new_payment)
        db.session.flush()
        db.session.commit()
        return new_payment

    def get_method(self) -> payment_methods:
        return payment_methods.query.get(self.payment_method)

    def get_status(self) -> payment_statuses:
        return payment_statuses.query.get(self.payment_status)
    
    def set_status(self, new_status:str) -> None:
        new_fk = select(
            payment_statuses.payment_status_id
        ).where(
            payment_statuses.payment_status == new_status.lower()
        ).first()

        if(new_fk):
            self.payment_status = new_fk
            db.session.commit()
        