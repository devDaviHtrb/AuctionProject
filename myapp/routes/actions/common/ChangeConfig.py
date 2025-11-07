
from flask import Blueprint, request, Response, redirect, session, url_for
from myapp.models.Users import users
from myapp.models.LegalPerson import legal_persons
from myapp.models.PhysicalPerson import physical_persons
from myapp.utils.LinksUrl import CONFIG_PAGE, configPage
from typing import Tuple
from myapp.utils.Unmask import unmask
from myapp.utils.Validations.validations import is_cpf, is_rg
from myapp.setup.InitSqlAlchemy import db

change_config_bp = Blueprint("changeConfig", __name__)

HOUR = 3600
DAY = HOUR*24

#called after the user press the button for save the changes in config page
#the inputs values will be wrote with cookies values
#input ids must have the same name as cookies
@change_config_bp.route("/changeConfig", methods=["POST"])
def change_config() -> Tuple[Response, int]:
    username = request.form["username"]
    name = request.form["name"]

    existing_user = users.query.filter_by(username=username).first()

    if existing_user:
        if existing_user.user_id != session.get("user_id"):
            return redirect(url_for(CONFIG_PAGE, msg="There are an user with this username")), 400
        
    current_user = users.query.filter_by(user_id=session.get("user_id")).first()

    if session["user_type"]=="physical_person":
        physical_person=  physical_persons.query.filter_by(user_id=current_user.user_id)
        gender = request.form["gender"]
        rg = request.form.get("rg", None)
        if rg:
            rg = unmask(rg)
            if is_rg(rg):
                physical_person.rg = rg
                session["rg"] = rg
            else:
                return redirect(url_for(CONFIG_PAGE, msg="Invalid Rg")), 400

        physical_person.gender = gender
        session["gender"] = gender
    

    cpf = request.form.get("cpf", None)
    if cpf:
        cpf = unmask(cpf)
        if is_cpf(cpf):
            current_user.cpf = cpf
            session["cpf"] = cpf
        else:
            return redirect(url_for(CONFIG_PAGE, msg="Invalid CPF")), 400
            
    current_user.username = username
    current_user.name = name
    
    db.session.commit()

    session["name"] = name
    session["username"] = username
    

    return redirect(url_for(CONFIG_PAGE, msg="sucessful"))
