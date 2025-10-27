from flask import Blueprint, Response, session, request, jsonify
from myapp.utils.Validations.AdressValidation import adress_validation
import myapp.repositories.AddressRepository as address_repository
from typing import Tuple

address_bp = Blueprint("userAddress")

@address_bp.route("/new/address", methods = ["POST"])
def user_address() -> Tuple[Response, int]:
    user_id = session.get("user_id")
    street_name = request.form.get("street_name", None)
    street_number = request.form.get("street_number", None)
    apt =request.form.get("apt", None)
    zip_code = request.form.get("zip_code", None)
    district =request.form.get("district", None)
    city = request.form.get("city", None)
    state = request.form.get("state", None)
    principal_address = request.form.get("principal_adress", None)

    data = {
        "user_id":              user_id,
        "street_name":          street_name,
        "street_number":        street_number,
        "zip_code":             zip_code,
        "district":             district,
        "city":                 city,
        "state":                state,
        "principal_address":    principal_address
    }
    missingInfo = [k for k in data if data[k] is None]
    if (missingInfo):
        return jsonify({
            "Error":        "Missing info",
            "MissigInfo":   missingInfo
        }), 400
    data["apt"] = apt

    if(not adress_validation(
        zip_code,
        district,
        state,
        city
    )):
        return jsonify({
            "Error": "Fake info"
        }), 400
    
    address_repository.save_item(data)
    return jsonify({
        "Address": data
    }), 201