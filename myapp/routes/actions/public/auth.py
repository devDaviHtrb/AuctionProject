from flask import Blueprint, Response, url_for, redirect, request
from myapp.services.CreateUser import create_user
from myapp.services.Messages import auth_message
from myapp.utils.AuthPending import *
from myapp.models.Users import users
from werkzeug.security import generate_password_hash
from secrets import token_hex
from typing import Dict, Any, Tuple

auth_bp = Blueprint("auth", __name__)
SING_IN = "/singIn"
RESEND = "/auth/change/"

def wait_sing_in() -> Response:
    return redirect(
        url_for(
            "waitingPage.WaitingPage",
            link=SING_IN,
            _external=True
        )
    )

def wait_resend(email:str) -> Response:
    return redirect(
        url_for(
            "waitingPage.WaitingPage",
            link= RESEND + email,
            _external=True
            )
        )

def login() -> Response:
    return redirect(url_for("loginPage.LoginPage"))

def sing_in() -> Response:
    return redirect(url_for("singInPage.SingInPage"))


@auth_bp.route("/auth/set/<string:token>", methods = ["POST", "GET"])
def auth(token:str) -> Response:
    data = get_by_pending(token)
    new_passord = request.form.get("new_password", None)
    if (not data): #not token
        return sing_in()
    
    #change password
    if (new_passord):
        user = users.get_by_email(
            data.get("email")
        )
        if (not user):
            return sing_in()
        user.password = generate_password_hash(new_passord)
    #new user
    else:
        create_user(data)
    pop_by_pending(token)
    return login()

@auth_bp.route("/auth/change/<string:email>")
def changePassword(email:str) -> Response:
    data = get_by_emails_dict(email)

    if (not data):
        if(not users.get_by_email(email)):
            return sing_in()
        
        token = add_in({"email": email})
        auth_message(email = email, content = url_for("auth.auth", token=token, _external=True))
        return wait_resend(email)
    
    token = data.get(email)
    auth_message(email = email, content = url_for("auth.auth", token=token, _external=True))
    return wait_resend(email)

        

