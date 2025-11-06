
from flask import Blueprint, request, Response, redirect, session, url_for
from myapp.models.Users import users
from myapp.models.LegalPerson import legal_persons
from myapp.models.PhysicalPerson import physical_persons
from myapp.utils.LinksUrl import CONFIG_PAGE, configPage
from typing import Tuple
from myapp.utils.Validations.UserValidation import User_validation
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
    current_user.username = username
    current_user.name = name
    physical_person=  physical_persons.query.filter_by(user_id=current_user.user_id)
    if physical_person:
        gender = request.form["gender"]
        physical_person.gender = gender
        session["gender"] = gender

    
    db.session.commit()

    session["name"] = name
    session["username"] = username
    

    return redirect(url_for(CONFIG_PAGE, msg="sucessful"))
