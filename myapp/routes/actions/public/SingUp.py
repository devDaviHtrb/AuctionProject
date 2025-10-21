import myapp.services.Messages as msgs
from flask import Blueprint, jsonify, url_for, request, Response
from myapp.models.Users import users
from myapp.services.AuthTokens import add_token
from myapp.services.CreateUser import create_user
from myapp.utils.Validations.GeneralValidation import general_validation
from myapp.utils.LinksUrl import wait_sing_up, AUTH_CONFIRM
from typing import Tuple

singUp = Blueprint("singUp", __name__)

@singUp.route("/singUp", methods=["POST"])
def SingUp() -> Tuple[Response, int]:

    resp, code = general_validation(request)
    data = resp.get("data")

    if (resp.get("Type") != "Valid"):
        return resp, code
        
    token = add_token(
         data = data,
         type = "create"
    )
    msgs.auth_message(
        email =     data.get("email"),
        content =   url_for(AUTH_CONFIRM, token=token, _external=True)
    )

    return wait_sing_up(), 303

