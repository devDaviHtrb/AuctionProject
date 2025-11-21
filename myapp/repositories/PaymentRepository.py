from myapp.models.PaymentStatuses import payment_statuses
from myapp.models.PaymentMethods import payment_methods
from myapp.models.Payments import payments
from myapp.setup.InitSqlAlchemy import db
from typing import Dict, Any, Optional
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker


def default_save(data:Dict[str, Any]) -> Optional[payments]:
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

    new_payment = payments(**data)
    db.session.add(new_payment)
    db.session.flush()
    db.session.commit()
    return new_payment

def save_item(data:Dict[str, Any], session:Optional[sessionmaker] = None) -> Optional[payments]:

    if (session is None):
        return default_save(data)
    
    payment_method_id = session.execute(
        select(payment_methods.payment_method_id)
        .where(payment_methods.payment_method == data.get("payment_method", "other").lower())
    ).scalar_one_or_none()

    payment_status_id = session.execute(
        select(payment_statuses.payment_status_id)
        .where(payment_statuses.payment_status == data.get("payment_status", "other").lower())
    ).scalar_one_or_none()

    data["payment_method"] = payment_method_id
    data["payment_status"] = payment_status_id

    new_payment = payments(**data)
    session.add(new_payment)

    session.flush()
    session.commit()

    return new_payment




def get_method(payment:payments) -> payment_methods:
    return payment_methods.query.get(payment.payment_method)

def get_status(payment:payments) -> payment_statuses:
    return payment_statuses.query.get(payment.payment_status)

def set_status(payment:payments, new_status:str) -> None:
    new_fk = select(
        payment_statuses.payment_status_id
    ).where(
        payment_statuses.payment_status == new_status.lower()
    ).first()

    if(new_fk):
        payment.payment_status = new_fk
        db.session.commit()

def get_by_id(wanted_id:int) -> Optional[payments]:
    return payments.query.get(wanted_id)