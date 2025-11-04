import myapp.services.Messages as msgs
from flask import Blueprint, url_for, request, Response
from myapp.services.AuthTokens import add_token
from myapp.utils.Validations.GeneralUserValidation import general_validation
from myapp.utils.LinksUrl import wait_sign_up, AUTH_CONFIRM
from typing import Tuple

sign_up_bp = Blueprint("signUp", __name__)

@sign_up_bp.route("/signUp", methods=["POST"])
def sign_up() -> Tuple[Response, int]:

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

    return wait_sign_up(), 200

