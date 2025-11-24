from myapp.models.PaymentMethods import payment_methods
from typing import Optional

def get_by_methdo(wanted_method:str) -> Optional[payment_methods]:
    return payment_methods.query.filter_by(payment_method = wanted_method.capitalize()).first()