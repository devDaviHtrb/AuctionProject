from flask import Blueprint, Response, redirect, session, request, jsonify, url_for
from myapp.models.Addresses import addresses
from myapp.utils.LinksUrl import CONFIG_PAGE
from myapp.utils.Validations.AdressValidation import adress_validation
import myapp.repositories.AddressRepository as address_repository
from typing import Tuple

address_bp = Blueprint("userAddress", __name__)


@address_bp.route("/new/address", methods=["POST"])
def user_address() -> Tuple[Response, int]:
    user_id = session.get("user_id")

    street_name = request.form.get("street_name", None)
    street_number = request.form.get("street_number", None)
    apt = request.form.get("apt", None)
    zip_code = request.form.get("zip_code", None)
    district = request.form.get("district", None)
    city = request.form.get("city", None)
    state = request.form.get("uf", None)
    principal_address = True if request.form.get("principal_address", None) else False

    data = {
        "user_id": user_id,
        "street_name": street_name,
        "street_number": street_number,
        "zip_code": zip_code,
        "district": district,
        "city": city,
        "state": state,
        "principal_address": principal_address
    }

    missingInfo = [k for k in data if data[k] and k != "principal_address" is None]
    if missingInfo:
        return jsonify({
            "Error": "Missing info",
            "MissigInfo": missingInfo
        }), 400
    
    data["apt"] = apt

    if not adress_validation(zip_code, district, state, city):
        return redirect(url_for(CONFIG_PAGE, msg=state))

    if principal_address:
        current_principal = addresses.query.filter_by(
            user_id=user_id,
            principal_address=True
        ).first()

        if current_principal:
            current_principal.principal_address = False
            

    address_repository.save_item(data)

    return jsonify({
        "Address": data,
        "success": True
    }), 201






@address_bp.route("/api/addresses", methods=["GET"])
def api_addresses():

   
    user_addresses = addresses.query.filter_by(user_id=session.get("user_id")).all()


    result = [{
        "address_id": addr.address_id,
        "street_name": addr.street_name,
        "street_number": addr.street_number,
        "apt": addr.apt,
        "district": addr.district,
        "city": addr.city,
        "state":addr.state,
        "zip_code": addr.zip_code,
        "principal_address": addr.principal_address
    } for addr in user_addresses]

    return jsonify(result)


