from flask import Blueprint, jsonify, request, redirect, session, url_for
from myapp.models.Addresses import addresses
from myapp.models.Users import users
from myapp.repositories.AddressRepository import change_adress
from myapp.setup.InitSqlAlchemy import db
from myapp.utils.LinksUrl import CONFIG_PAGE
from myapp.utils.Validations.AdressValidation import adress_validation

updateAddress = Blueprint("updateAdress", __name__)


@updateAddress.route("/updateAddress/<int:address_id>", methods=["POST"])
def update_address(address_id):
    addr = addresses.query.get(address_id)
    
    if not addr or addr.user_id != session.get("user_id"):
        return redirect(url_for(CONFIG_PAGE, msg="Invalid address"))

    street_name = request.form["street_name"]
    street_number = request.form["street_number"]
    apt = request.form.get("apt")
    zip_code = request.form["zip_code"]
    district = request.form["district"]
    city = request.form["city"]
    state = request.form["state"]
    principal_address = "principal_address" in request.form

    if(not adress_validation(
        zip_code,
        district,
        state,
        city
    )):
        return redirect(url_for(CONFIG_PAGE, msg="fake info")), 400

    change_adress(address_id=address_id, request=request, user_id= session.get("user_id") )



    return redirect(url_for(CONFIG_PAGE, msg="Address updated"))