from flask import Blueprint, Response, url_for, redirect, request, make_response
from myapp.services.CreateUser import create_user
from myapp.services.InitSession import init_session
from myapp.services.Messages import auth_message
from myapp.utils.AuthPending import *
from myapp.models.Users import users
from werkzeug.security import generate_password_hash
from myapp.services.setCookies import set_cookies
from myapp.utils.LinksUrl import *


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth/<string:type>/<string:token>", methods = ["POST", "GET"])
def auth(type:str, token:str) -> Response:
    token_data = get_by_pending(token)

    if (not token_data): #not token
        return sing_in()
    
    if(type == "login"):       
        response = make_response(init_session(users.query.filter_by(user_id = token_data.get("user_id")).first()))
        set_cookies(request, response)
        pop_by_pending(token)
        return profile()
    
    elif(type == "create"):
        create_user(token_data)

    elif(type == "reset"):
        user = users.get_by_email(
            token_data.get("email")
        )
        new_password = request.form.get("new_password", None)
        if (not user or not new_password):
            return sing_in()
        user.save_password(new_password)

    else:
        return sing_in()
    
    pop_by_pending(token)
    return login()

@auth_bp.route("/auth/resend/<string:email>")
def resend(email:str) -> Response:
    token = get_by_emails_dict(email)
    if (not token):
        return login()
    auth_message(
        email = email,
        content = url_for("auth.auth", type = "login", token = token)
    )
    return wait_login(email)

@auth_bp.route("/auth/change/<string:email>")
def changePassword(email:str) -> Response:
    token_data = get_by_emails_dict(email)
    if (not token_data):
        if(not users.get_by_email(email)): # no have users with this email
            return sing_in()
        
        #add in token
        token = add_in({"email": email})
        auth_message(email = email, content = url_for("auth.auth", type = "reset",token=token, _external=True))
        return wait_change(email)

    # if token exists resend email   
    token = token_data.get(email)
    auth_message(email = email, content = url_for("auth.auth", type = "reset", token=token, _external=True))
    return wait_change(email)

        

