from flask import Request, session
from myapp.utils.Validations.validations import *
from myapp.utils.GetMissingInfo import get_missing_info
from typing import Dict, Tuple, Any

datakey = [
    "product_name",
    "description",
    "min_bid",
    "start_datetime",
    "product_status",
    "street_name",
    "street_number",
    "apt",
    "zip_code",
    "district",
    "city",
    "state",
    "category",
    "end_datetime",
    "duration",
    "photos"
]

nullAbleValues = [
    "description",
    "min_bid",
    "start_datetime",
    "product_status",   #FK    
    "street_name",
    "street_number",
    "apt",
    "zip_code",
    "district",
    "city",
    "state",
    "category",         #FK
    "end_datetime"
]
def general_validation(request:Request) -> Tuple[Dict[str, Any], int]:
    data, code = get_missing_info(
        request,
        datakey,
        nullAbleValues
    )
    data["user_id"] = session.get("user_id")
    if (code != 200):
        return data, code

    if (data.get("zip_code", None) and data.get("district", None) and data.get("state", None) and data.get("city", None)):
        if not adress_validation(data["zip_code"], data["district"], data["state"], data["city"]): #without contractions
            return {
                 "Type":    "InputError",
                 "content": "Invalid location data"
            }, 400
    
    return data, 200