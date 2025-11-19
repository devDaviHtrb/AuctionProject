

from flask import Blueprint, Response, redirect, request, session, url_for

from myapp.services.GeneralChangeConfig import general_change_config
from myapp.utils.LinksUrl import CONFIG_PAGE
from myapp.utils.Validations.UserValidation import User_validation


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
        
    general_change_config(name, username, request)
    

    return redirect(url_for(CONFIG_PAGE, msg="sucessful"))
