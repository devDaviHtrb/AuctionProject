
from flask import Blueprint, request, Response, redirect, session, url_for
from myapp.utils.LinksUrl import CONFIG_PAGE
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
    

    existing_user = user_repository.get_by_username(username)
    if existing_user:
        if existing_user.user_id != session.get("user_id"):
            return redirect(url_for(CONFIG_PAGE, msg="There are an user with this username"))
    
    current_user = user_repository.get_by_id(session.get("user_id"))
    current_user.username = username
    current_user.name = name
    physical_person=  physical_person_repository.get_by_id(current_user.user_id)
    if physical_person:
        gender = request.form["gender"]
        physical_person.gender = gender
        session["gender"] = gender

    
    db.session.commit()

    session["name"] = name
    session["username"] = username
    

    return redirect(url_for(CONFIG_PAGE, msg="sucessful"))
