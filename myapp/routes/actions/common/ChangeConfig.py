
from flask import Blueprint, request, Response, redirect, session, url_for
from typing import Tuple
from myapp.services.ChangeLPData import change_lp_data
from myapp.services.ChangePPData import change_pp_data
from myapp.utils.LinksUrl import CONFIG_PAGE
from myapp.utils.Unmask import unmask
from myapp.utils.Validations.validations import is_cpf, User_validation
from myapp.setup.InitSqlAlchemy import db
import myapp.repositories.UserRepository as user_repository
import myapp.repositories.PhysicalPersonRepository as physical_person_repository

change_config_bp = Blueprint("changeConfig", __name__)

HOUR = 3600
DAY = HOUR*24

#called after the user press the button for save the changes in config page
#the inputs values will be wrote with cookies values
#input ids must have the same name as cookies
@change_config_bp.route("/changeConfig", methods=["POST"])
def change_config() -> Response:
    username = request.form["username"]
    name = request.form["name"]

    if session.get("username")!=username:
        if not User_validation(username=username):
            return redirect(url_for(CONFIG_PAGE, msg="There are an user with this username")), 400
        
    current_user = user_repository.get_by_id(session.get("user_id"))

    if session["user_type"]=="physical_person":
        change_pp_data(request, current_user)
    elif session["user_type"] == "legal_person":
       change_lp_data(request, current_user)
            

    cpf = request.form.get("cpf", None)
    if cpf:
        cpf = unmask(cpf)
        if is_cpf(cpf):
            if not User_validation(cpf=cpf):
                return redirect(url_for(CONFIG_PAGE, msg="There are an user with this CPF")), 400
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
