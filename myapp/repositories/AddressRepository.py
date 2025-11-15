from flask import request
from myapp.models.Addresses import addresses
from myapp.setup.InitSqlAlchemy import db
from typing import Dict, Any

def save_item(data:Dict[str, Any]) -> addresses:
    new_address = addresses(**data)
    db.session.add(new_address)
    db.session.flush()
    db.session.commit()
    return new_address

def change_adress(address_id, request, user_id):
    addr = addresses.query.get(address_id)
    
    addr.street_name = request.form["street_name"]
    addr.street_number = request.form["street_number"]
    addr.apt = request.form.get("apt")
    addr.zip_code = request.form["zip_code"]
    addr.district = request.form["district"]
    addr.city = request.form["city"]
    addr.state = request.form["state"]
    addr.principal_address = "principal_address" in request.form


    if addr.principal_address:
        addresses.query.filter(
            addresses.user_id == addr.user_id,
            addresses.address_id != addr.address_id
        ).update({"principal_address": False})

    db.session.commit()
