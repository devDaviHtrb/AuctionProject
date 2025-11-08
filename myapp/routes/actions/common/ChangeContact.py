from flask import Blueprint, request, Response, redirect, session, url_for
from myapp.models.Users import users
from myapp.utils.LinksUrl import CONFIG_PAGE
from myapp.setup.InitSqlAlchemy import db
from typing import Tuple
from myapp.utils.Validations.validations import is_phone_number

change_contact_bp = Blueprint("changeContact", __name__)

@change_contact_bp.route("/changeContact", methods=["POST"])
def change_contact() -> Response:
    cellphone1 = request.form.get("cellphone1", None)
    cellphone2 = request.form.get("cellphone2", None)
    landline = request.form.get("landline", None)
    phones = [cellphone1, cellphone2, landline]
    
    for phone in phones:
        if phone != None:
            unf_phone = phone
            phone = phone.replace(" ", "")
            phone =  phone.replace("\n", "")
            phone = phone.replace("(", "")
            phone = phone.replace(")", "")
            phone = phone.replace("-", "")
            phones[phones.index(unf_phone)] = phone
    for phone in phones:
        if phone != None and phone!="":
            if not is_phone_number(phone):
                return redirect(url_for(CONFIG_PAGE, msg="invalid cellphone"))


    user_id = session.get("user_id")
    current_user = users.query.filter_by(user_id=user_id).first()

    current_user.cellphone1 = cellphone1
    current_user.cellphone2 = cellphone2
    current_user.landline = landline

    session["cellphone1"] = phones[0]
    session["cellphone2"] = phones[1]
    session["landline"] = phones[2]

    db.session.commit()

    return redirect(url_for(CONFIG_PAGE, msg="sucessful"))
